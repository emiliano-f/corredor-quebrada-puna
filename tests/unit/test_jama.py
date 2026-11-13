import functools
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
import pytest
import respx
from typer.testing import CliRunner

from corredor.config import AppConfig, load_config
from corredor.http import PoliteFetcher
from corredor.models import SourceConfig
from corredor.pipeline import app
from corredor.sources.jama import (
    ArgentinaGobArJama,
    MopChileJama,
    append_jsonl,
    build_collectors,
    read_jsonl,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "jama"
MOP_HOST = "https://rest-sit.mop.gob.cl"
AR_HOST = "https://www.argentina.gob.ar"
MOP_QUERY = (
    f"{MOP_HOST}/arcgis/rest/services/VIALIDAD/Pasos_Fronterizos/MapServer/0/query"
    "?where=OBJECTID%3D7&outFields=%2A&f=json"
)
AR_LIST = f"{AR_HOST}/seguridad/pasosinternacionales/listado"
NOW = datetime(2026, 11, 13, 21, 0, tzinfo=UTC)


def fixture(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def cfg() -> AppConfig:
    return load_config(ROOT / "config.yaml")


def source(cfg: AppConfig, source_id: str) -> SourceConfig:
    return next(s for s in cfg.fuentes if s.id == source_id)


class NoSleepClock:
    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def fetcher(tmp_path: Path, clock: NoSleepClock | None = None) -> PoliteFetcher:
    clock = clock or NoSleepClock()
    return PoliteFetcher(
        "corredor-test/0.1 (+https://example.org)",
        tmp_path / "cache",
        client=httpx.Client(),
        retries=0,
        sleep=clock.sleep,
        clock=clock,
        wall_clock=lambda: NOW.timestamp(),
    )


def mock_robots() -> None:
    respx.get(f"{MOP_HOST}/robots.txt").respond(404)
    respx.get(f"{AR_HOST}/robots.txt").respond(
        200, text="User-agent: *\nCrawl-delay: 10\nDisallow: /user/\n"
    )


def test_config_enables_both_collectors(cfg: AppConfig) -> None:
    built = build_collectors(cfg.fuentes, fetcher=object())  # type: ignore[arg-type]
    assert [type(c) for c in built] == [MopChileJama, ArgentinaGobArJama]


def test_mop_url(cfg: AppConfig) -> None:
    c = MopChileJama(source(cfg, "jama_mop_cl"), fetcher=object())  # type: ignore[arg-type]
    assert c.url() == MOP_QUERY


def test_mop_records_keep_raw_attributes(cfg: AppConfig) -> None:
    c = MopChileJama(source(cfg, "jama_mop_cl"), fetcher=object())  # type: ignore[arg-type]
    [rec] = c.records(fixture("mop_cl_query.json"))
    assert rec["OBJECTID"] == 7
    assert rec["PASO"] == "JAMA"
    assert rec["TRANSITABILIDAD"] == "TRÁNSITO SIN RESTRICCIÓN"
    assert "CADENAS" in rec


def test_argentina_keeps_only_jama_when_extras_at_baseline(cfg: AppConfig) -> None:
    c = ArgentinaGobArJama(source(cfg, "jama_argentina_gob_ar"), fetcher=object())  # type: ignore[arg-type]
    recs = c.records(fixture("argentina_listado.json"))
    assert [r["id"] for r in recs] == [19]
    assert recs[0]["nombre_paso"] == "Jama"
    assert recs[0]["estado_prioridad"] == "ABIERTO"


def test_argentina_adds_extra_when_its_status_changes(cfg: AppConfig) -> None:
    data = fixture("argentina_listado.json")
    next(r for r in data if r["id"] == 101)["estado_prioridad"] = "ABIERTO"
    c = ArgentinaGobArJama(source(cfg, "jama_argentina_gob_ar"), fetcher=object())  # type: ignore[arg-type]
    assert [r["id"] for r in c.records(data)] == [19, 101]


@respx.mock
def test_snapshot_ok_both_sources(cfg: AppConfig, tmp_path: Path) -> None:
    mock_robots()
    respx.get(MOP_QUERY).respond(200, json=fixture("mop_cl_query.json"))
    respx.get(AR_LIST).respond(200, json=fixture("argentina_listado.json"))
    rows = [c.snapshot() for c in build_collectors(cfg.fuentes, fetcher(tmp_path))]
    assert [r.fuente for r in rows] == ["mop_cl", "argentina_gob_ar"]
    assert all(r.error is None and r.fetched_at == NOW for r in rows)
    mop = json.loads(rows[0].payload_json or "")
    assert mop[0]["OBJECTID"] == 7
    ar = json.loads(rows[1].payload_json or "")
    assert [r["id"] for r in ar] == [19]


@respx.mock
def test_snapshot_bypasses_cache(cfg: AppConfig, tmp_path: Path) -> None:
    mock_robots()
    route = respx.get(MOP_QUERY).respond(200, json=fixture("mop_cl_query.json"))
    f = fetcher(tmp_path)
    c = MopChileJama(source(cfg, "jama_mop_cl"), f)
    c.snapshot()
    c.snapshot()
    assert route.call_count == 2


@respx.mock
def test_argentina_honors_crawl_delay(cfg: AppConfig, tmp_path: Path) -> None:
    mock_robots()
    respx.get(AR_LIST).respond(200, json=fixture("argentina_listado.json"))
    clock = NoSleepClock()
    c = ArgentinaGobArJama(source(cfg, "jama_argentina_gob_ar"), fetcher(tmp_path, clock))
    c.snapshot()
    c.snapshot()
    assert clock.sleeps[-1] == pytest.approx(10.0)


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        (httpx.Response(500), "HTTP 500"),
        (httpx.Response(404), "HTTP 404"),
        (httpx.Response(200, text="<html>no</html>"), "JSON inválido"),
        (httpx.Response(200, json={"error": {"code": 400}}), "error ArcGIS"),
        (httpx.Response(200, json={"features": []}), "OBJECTID 7 no está"),
        (httpx.Response(200, json={"features": 1}), "respuesta inesperada (TypeError"),
    ],
)
@respx.mock
def test_mop_failures_become_error_rows(
    cfg: AppConfig, tmp_path: Path, response: httpx.Response, expected: str
) -> None:
    mock_robots()
    respx.get(MOP_QUERY).mock(return_value=response)
    row = MopChileJama(source(cfg, "jama_mop_cl"), fetcher(tmp_path), now=lambda: NOW).snapshot()
    assert row.payload_json is None
    assert row.error is not None
    assert expected in row.error
    assert row.fetched_at == NOW


@respx.mock
def test_network_error_becomes_error_row(cfg: AppConfig, tmp_path: Path) -> None:
    mock_robots()
    respx.get(AR_LIST).mock(side_effect=httpx.ConnectTimeout("timeout"))
    row = ArgentinaGobArJama(
        source(cfg, "jama_argentina_gob_ar"), fetcher(tmp_path), now=lambda: NOW
    ).snapshot()
    assert row.error is not None
    assert "ConnectTimeout" in row.error


@respx.mock
def test_robots_disallow_becomes_error_row(cfg: AppConfig, tmp_path: Path) -> None:
    respx.get(f"{AR_HOST}/robots.txt").respond(200, text="User-agent: *\nDisallow: /\n")
    row = ArgentinaGobArJama(
        source(cfg, "jama_argentina_gob_ar"), fetcher(tmp_path), now=lambda: NOW
    ).snapshot()
    assert row.error is not None
    assert "DisallowedByRobots" in row.error


@respx.mock
def test_argentina_malformed_listing_becomes_error_row(cfg: AppConfig, tmp_path: Path) -> None:
    mock_robots()
    respx.get(AR_LIST).respond(200, json=[{"id": [19]}])
    row = ArgentinaGobArJama(
        source(cfg, "jama_argentina_gob_ar"), fetcher(tmp_path), now=lambda: NOW
    ).snapshot()
    assert row.payload_json is None
    assert row.error is not None
    assert "respuesta inesperada (TypeError" in row.error


def test_argentina_missing_jama_is_error(cfg: AppConfig, tmp_path: Path) -> None:
    c = ArgentinaGobArJama(source(cfg, "jama_argentina_gob_ar"), fetcher=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="no están en el listado"):
        c.records([{"id": 27}])


def test_jsonl_roundtrip(tmp_path: Path) -> None:
    from corredor.models import JamaEstado

    path = tmp_path / "snapshots" / "jama_estado.jsonl"
    rows = [
        JamaEstado(fuente="mop_cl", fetched_at=NOW, payload_json='[{"OBJECTID": 7}]'),
        JamaEstado(fuente="argentina_gob_ar", fetched_at=NOW, error="HTTP 500"),
    ]
    assert append_jsonl(path, rows[:1]) == 1
    assert append_jsonl(path, rows[1:]) == 1
    assert path.read_text(encoding="utf-8").count("\n") == 2
    assert read_jsonl(path) == rows


@respx.mock
def test_cli_appends_and_exits_zero_on_source_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path / "data"))
    clock = NoSleepClock()
    monkeypatch.setattr(
        "corredor.pipeline.PoliteFetcher",
        functools.partial(PoliteFetcher, sleep=clock.sleep, clock=clock),
    )
    mock_robots()
    respx.get(MOP_QUERY).respond(200, json=fixture("mop_cl_query.json"))
    respx.get(AR_LIST).respond(503)
    out = tmp_path / "snapshots" / "jama_estado.jsonl"
    args = ["snapshot-jama", "--config", str(ROOT / "config.yaml"), "--salida", str(out)]
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    rows = read_jsonl(out)
    assert [r.fuente for r in rows] == ["mop_cl", "argentina_gob_ar"]
    assert rows[0].error is None
    assert rows[1].error is not None
    assert "503" in rows[1].error
    assert "2 línea(s)" in result.output
