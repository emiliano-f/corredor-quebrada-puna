"""Dashboard bundle, forecast risk and static site (offline: no network)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from corredor.config import AppConfig, UmbralElegido, load_config
from corredor.models import CriticalPoint, JamaEstado
from corredor.reports import Lineage
from corredor.tablero.bundle import (
    BundleInputs,
    build_bundle,
    jama_section,
    markdown_blocks,
    nearest_point,
    read_geo,
)
from corredor.tablero.forecast import Climatologia, evaluar, fetch_forecasts, riesgo_punto
from corredor.tablero.site import render, safe_json, write_site
from corredor.weather.openmeteo import CallBudgetExceeded

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "tablero" / "src"
NOW = datetime(2026, 11, 14, 12, 0, tzinfo=UTC)
NOW_LOCAL = datetime(2026, 11, 14, 9, 0)
EVIL = '<script>document.title="XSS"</script><img src=x onerror="document.title=\'XSS\'">'
URL = "https://www.elsubmarinojujuy.com.ar/nota-1"
SVG_NS = "http://www.w3.org/2000/svg"


@pytest.fixture(scope="module")
def cfg() -> AppConfig:
    return load_config(ROOT / "config.yaml")


def hourly(start: datetime, hours: int, rain: float) -> pd.DataFrame:
    times = pd.date_range(start, periods=hours, freq="h")
    return pd.DataFrame({"time": times, "precipitacion_mm": rain, "nieve_cm": 0.0, "temp_c": 5.0})


class FakeClient:
    def __init__(self, rain: float = 1.0, fail: Exception | None = None) -> None:
        self.rain, self.fail = rain, fail

    def forecast(self, point: CriticalPoint, hours: int) -> pd.DataFrame:
        if self.fail:
            raise self.fail
        return hourly(NOW_LOCAL - timedelta(hours=168), 168 + hours + 1, self.rain)

    def historical_forecast(
        self, point: CriticalPoint, start: date, end: date, model: str
    ) -> pd.DataFrame:
        if self.fail:
            raise self.fail
        days = pd.date_range(start, end, freq="D")
        rng = np.random.default_rng(0)
        frames = [
            hourly(d.to_pydatetime(), 24, float(r))
            for d, r in zip(days, rng.gamma(0.3, 0.5, len(days)), strict=True)
        ]
        return pd.concat(frames, ignore_index=True)


def inputs(cfg: AppConfig, **kw: Any) -> BundleInputs:
    p = cfg.puntos[0]
    eventos = pd.DataFrame(
        [{"evento_id": "e1", "fecha": date(2024, 2, 1), "ruta": p.ruta, "punto_id": p.id,
          "paraje": "", "causa": "aluvion", "tipo_corte": "total", "fuentes": [URL],
          "n_medios": 1, "notas": "", "metodo": "reglas", "confianza": "alta"}]
    )  # fmt: skip
    articulos = pd.DataFrame([{"url": URL, "source_id": "elsubmarino", "titular": EVIL}])
    grilla = pd.DataFrame(
        [{"punto_id": p.id, "modelo": "era5", "lat_grilla": -24.0, "lon_grilla": -65.5,
          "diferencia_m": 900.0, "comparte_celda_con": cfg.puntos[1].id}]
    )  # fmt: skip
    base: dict[str, Any] = {
        "cfg": cfg, "eventos": eventos, "articulos": articulos, "jama": [], "grilla": grilla,
        "lineage": Lineage(version="0.1.0", git_commit="abc1234", schema_version=2,
                           sources_hash="h", generated_at=NOW),
        "geo": read_geo(ROOT / "assets" / "geo"), "pronostico": {}, "pronostico_hora": None,
        "uso": markdown_blocks("# Uso\n\n- item"), "now": NOW,
    }  # fmt: skip
    base.update(kw)
    return BundleInputs(**base)


def forecasts(cfg: AppConfig, umbrales: list[UmbralElegido], **kw: Any) -> dict[str, Any]:
    return fetch_forecasts(
        kw.pop("client", FakeClient()), cfg.puntos[:2], umbrales, model="best_match", hours=72,
        clim_start=date(2024, 1, 1), now_local=NOW_LOCAL,
    )  # fmt: skip


def test_bundle_header_and_schema(cfg: AppConfig) -> None:
    b = build_bundle(inputs(cfg, pronostico=forecasts(cfg, []), pronostico_hora=NOW))
    assert set(b) >= {"encabezado", "umbrales", "puntos", "eventos", "por_anio", "jama",
                      "limitaciones", "mapa", "uso", "fuentes", "licencias"}  # fmt: skip
    h = b["encabezado"]
    assert (h["version"], h["git_commit"], h["schema_version"]) == ("0.1.0", "abc1234", 2)
    assert h["generado"] == "2026-11-14 09:00"
    assert h["pronostico_hora"] == "2026-11-14 09:00"
    assert len(b["puntos"]) == len(cfg.puntos)
    p0 = b["puntos"][0]
    assert p0["eventos"] == 1
    assert p0["celda"]["comparte_con"] == [cfg.puntos[1].id]
    assert b["puntos"][5]["pronostico"] is None  # not fetched → missing, not invented
    (e,) = b["eventos"]
    assert e["notas_medios"][0] == {"medio": "El Submarino Jujuy", "titular": EVIL, "url": URL}
    assert b["por_anio"] == [{"anio": 2024, "estables": 1, "solo_nuevas": 0}]
    assert b["limitaciones"]["un_medio"] == 1
    assert b["limitaciones"]["dias_evento_prueba"]["lluvia"] == 1
    assert b["mapa"]["lineas"]
    assert b["mapa"]["lugares"]
    json.dumps(b)  # serialisable


def test_empty_thresholds_are_pending(cfg: AppConfig) -> None:
    assert cfg.umbrales_elegidos == []
    b = build_bundle(inputs(cfg, pronostico=forecasts(cfg, [])))
    assert b["umbrales"] == []
    for p in b["puntos"][:2]:
        for h in p["pronostico"]["horizontes"].values():
            assert h["estado"] == "pendiente"
            assert h["evaluaciones"] == []


def test_percentile_uses_forecast_model_climatology() -> None:
    clim = Climatologia.from_hourly(hourly(datetime(2024, 1, 1), 24 * 60, 1.0))  # 24 mm/day
    assert clim.desde == date(2024, 1, 1)
    when = datetime(2024, 2, 1)  # DJF, same season as the climatology
    assert clim.percentil("lluvia_24h_mm", 24.0, when) == 50.0
    assert clim.percentil("lluvia_24h_mm", 30.0, when) == 100.0
    assert clim.percentil("lluvia_24h_mm", 0.0, when) == 0.0
    assert clim.percentil("lluvia_24h_mm", 24.0, datetime(2024, 7, 1)) is None  # no JJA data


def test_percentile_threshold_alerts_and_mm_is_not_comparable(cfg: AppConfig) -> None:
    pct = UmbralElegido(grupo="lluvia", variable="lluvia_24h_mm_pct", umbral=95)
    mm = UmbralElegido(grupo="lluvia", variable="lluvia_24h_mm", umbral=10)
    clim = Climatologia.from_hourly(hourly(datetime(2025, 11, 1), 24 * 40, 0.05))
    wet = hourly(NOW_LOCAL - timedelta(hours=168), 168 + 73, 2.0)
    r = riesgo_punto(cfg.puntos[0], wet, clim, [pct, mm], NOW_LOCAL)
    hoy = r.horizontes["hoy"]
    assert hoy["estado"] == "alerta"
    pct_eval, mm_eval = hoy["evaluaciones"]
    assert pct_eval["estado"] == "alerta"
    assert pct_eval["percentil"] == 100.0
    assert mm_eval["estado"] == "no_comparable"
    assert mm_eval["valor"] == 48.0
    only_mm = riesgo_punto(cfg.puntos[0], wet, clim, [mm], NOW_LOCAL)
    assert only_mm.horizontes["72h"]["estado"] == "no_comparable"


def test_failed_download_is_missing(cfg: AppConfig) -> None:
    pct = UmbralElegido(grupo="nieve", variable="nieve_24h_cm_pct", umbral=90)
    out = forecasts(cfg, [pct], client=FakeClient(fail=CallBudgetExceeded("tope")))
    r = out[cfg.puntos[0].id]
    assert "tope diario" in (r.error or "")
    assert r.horizontes["hoy"]["estado"] == "sin_datos"
    assert r.horizontes["hoy"]["variables"]["nieve_24h_cm"] == {"valor": None, "percentil": None}


def test_threshold_config_is_validated() -> None:
    with pytest.raises(ValidationError):
        UmbralElegido(grupo="lluvia", variable="lluvia_3h_mm_pct", umbral=95)
    with pytest.raises(ValidationError):
        UmbralElegido(grupo="lluvia", variable="lluvia_24h_mm_pct", umbral=150)


def snap(fuente: str, age_h: float) -> JamaEstado:
    payload = json.dumps([{"TRANSITABILIDAD": "CERRADO", "HORA": 28_800_000}])
    return JamaEstado(fuente=fuente, fetched_at=NOW - timedelta(hours=age_h), payload_json=payload)  # type: ignore[arg-type]


def test_jama_stale_flag() -> None:
    fresh = jama_section([snap("mop_cl", 30), snap("mop_cl", 1)], NOW)
    assert fresh["vieja"] is False
    assert fresh["ultimos"][0]["estado"] == "CERRADO"
    assert fresh["ultimos"][0]["campos"]["HORA"] == "08:00"
    assert len(fresh["linea"]) == 2
    stale = jama_section([snap("mop_cl", 7)], NOW)
    assert stale["vieja"] is True
    assert stale["ultimos"][0]["vieja"] is True
    assert jama_section([], NOW)["vieja"] is True
    old = jama_section([snap("mop_cl", 24 * 8), snap("mop_cl", 2)], NOW)
    assert len(old["linea"]) == 1  # last 7 days only


def test_scraped_headline_cannot_break_out(cfg: AppConfig) -> None:
    html = render(build_bundle(inputs(cfg)), SRC)
    assert "<script>document" not in html
    assert "<img" not in html
    block = re.search(r'<script type="application/json" id="datos">(.*?)</script>', html, re.S)
    assert block is not None
    assert json.loads(block.group(1))["eventos"][0]["notas_medios"][0]["titular"] == EVIL
    assert "\u2028" not in safe_json({"t": "a\u2028b"})


def test_app_js_has_no_html_sinks() -> None:
    js = (SRC / "app.js").read_text(encoding="utf-8")
    for sink in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(",
                 "new Function", "fetch(", "XMLHttpRequest"):  # fmt: skip
        assert sink not in js


def _http_outside_links(data: Any, key: str = "") -> list[str]:
    if isinstance(data, dict):
        return [x for k, v in data.items() for x in _http_outside_links(v, k)]
    if isinstance(data, list):
        return [x for v in data for x in _http_outside_links(v, key)]
    if isinstance(data, str) and re.search(r"https?://", data) and key != "url":
        return [f"{key}={data}"]
    return []


def test_dist_references_no_external_resources(cfg: AppConfig, tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    size = write_site(build_bundle(inputs(cfg)), dist, SRC)
    assert size < 5 * 1024 * 1024
    for f in dist.rglob("*"):
        text = f.read_text(encoding="utf-8")
        if f.suffix == ".json":
            assert _http_outside_links(json.loads(text)) == []  # urls only as <a href> links
            continue
        block = re.search(
            r'(<script type="application/json" id="datos">)(.*?)(</script>)', text, re.S
        )
        if block:
            assert _http_outside_links(json.loads(block.group(2))) == []
            text = text.replace(block.group(2), "")
        text = re.sub(r'<a [^>]*href="https?://[^"]*"', "<a", text).replace(SVG_NS, "")
        assert not re.search(r"https?://|//[a-z0-9.-]+\.[a-z]{2,}/", text, re.I), f.name
        assert "url(" not in text
        assert "@import" not in text
    head = (dist / "index.html").read_text(encoding="utf-8")
    m = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', head)
    assert m is not None
    assert "default-src 'none'" in m.group(1)
    assert "http" not in m.group(1)


CHROME = next(
    (shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)),
    None,
)


@pytest.mark.skipif(CHROME is None, reason="no headless browser")
def test_headline_renders_as_text_in_browser(cfg: AppConfig, tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    write_site(build_bundle(inputs(cfg)), dist, SRC)
    url = (dist / "index.html").as_uri() + "#historial"
    dom = subprocess.run(  # noqa: S603 — fixed argv, local file
        [str(CHROME), "--headless=new", "--no-sandbox", "--disable-gpu", "--dump-dom", url],
        capture_output=True, text=True, timeout=90, check=True,
    ).stdout  # fmt: skip
    assert "&lt;script&gt;document.title=" in dom  # shown as text
    assert "<title>XSS</title>" not in dom
    assert '<img src="x"' not in dom
    assert "1 de 1 eventos" in dom


def test_markdown_blocks() -> None:
    blocks = markdown_blocks("# T\n\nUno\ndos.\n\n## S\n\n- a **b**\n  sigue\n- `c`\n")
    assert blocks == [
        {"tipo": "h1", "texto": "T"},
        {"tipo": "p", "texto": "Uno dos."},
        {"tipo": "h2", "texto": "S"},
        {"tipo": "li", "texto": "a b sigue"},
        {"tipo": "li", "texto": "c"},
    ]


def test_bundle_without_events_table(cfg: AppConfig) -> None:
    b = build_bundle(inputs(cfg, eventos=pd.DataFrame(), articulos=pd.DataFrame()))
    assert b["eventos"] == []
    assert b["por_anio"] == []
    assert b["limitaciones"]["eventos"] == 0


def test_tiny_raw_value_still_alerts() -> None:
    u = UmbralElegido(grupo="nieve", variable="nieve_24h_cm_pct", umbral=95)
    (e,) = evaluar([u], {"nieve_24h_cm": 0.04}, {"nieve_24h_cm": 99.0})
    assert e.estado == "alerta"  # compared unrounded, like the calibration


def test_jama_extra_records_are_kept() -> None:
    main = {"id": 19, "nombre_paso": "Jama", "estado_prioridad": "ABIERTO",
            "estado_vialidad": "HABILITADA"}  # fmt: skip
    norte = {"id": 90, "nombre_paso": "Jama Norte", "estado_prioridad": "CERRADO",
             "estado_vialidad": "NIEVE"}  # fmt: skip
    payload = json.dumps([main, norte])
    s = JamaEstado(fuente="argentina_gob_ar", fetched_at=NOW, payload_json=payload)
    out = jama_section([s], NOW)
    (u,) = out["ultimos"]
    assert u["estado"] == "ABIERTO / HABILITADA · Jama Norte: CERRADO / NIEVE"
    assert u["campos"]["nombre_paso"] == "Jama"
    assert u["otros"][0]["nombre_paso"] == "Jama Norte"
    assert out["linea"][0]["estado"] == u["estado"]


def test_events_follow_the_model(cfg: AppConfig) -> None:
    from corredor.models import ClosureEvent

    (e,) = build_bundle(inputs(cfg))["eventos"]
    assert set(ClosureEvent.model_fields) - {"fuentes"} <= set(e)
    assert e["metodo"] == "reglas"
    assert e["hora"] is None


def test_nearest_point(cfg: AppConfig) -> None:
    p = cfg.puntos[3]
    pid, km = nearest_point(p.lat + 0.001, p.lon, cfg.puntos)
    assert pid == p.id
    assert 0.1 < km < 0.12


@pytest.mark.skipif(CHROME is None, reason="no headless browser")
def test_nearest_point_in_browser_matches_python(cfg: AppConfig, tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    write_site(build_bundle(inputs(cfg)), dist, SRC)
    lat, lon = -23.70, -65.70
    pid, km = nearest_point(lat, lon, cfg.puntos)
    name = next(p.nombre for p in cfg.puntos if p.id == pid)
    url = (dist / "index.html").as_uri() + f"#cerca/{lat},{lon}"
    dom = subprocess.run(  # noqa: S603 — fixed argv, local file
        [str(CHROME), "--headless=new", "--no-sandbox", "--disable-gpu", "--dump-dom", url],
        capture_output=True, text=True, timeout=90, check=True,
    ).stdout  # fmt: skip
    assert f"{name} (" in dom
    assert f"a {km:.1f} km" in dom
