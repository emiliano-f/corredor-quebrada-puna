"""Dashboard data bundle: every number comes from the pipeline tables (AGENTS.md rule 4).

`build_bundle` is pure (no I/O): the CLI reads the tables, GeoJSON, Jama snapshots and the
forecast, and passes them in. Missing data stays None/empty and the UI says so.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from corredor.calibration.thresholds import ThresholdCalibrator
from corredor.config import AppConfig
from corredor.models import CriticalPoint, JamaEstado
from corredor.reports import Lineage
from corredor.tablero.forecast import PronosticoPunto

BUNDLE_VERSION = 1
EARTH_KM = 6371.0
JAMA_STALE = timedelta(hours=6)
JAMA_DAYS = 7
GEO_FILES = ("rutas", "ferrocarril", "contexto", "puntos")
MAP_WIDTH = 1000.0
LOCAL_OFFSET = timedelta(hours=-3)  # Jujuy: UTC-3 all year (no DST since 2009)
WEATHER_GROUPS: dict[str, tuple[str, ...]] = {
    "aluvion": ("aluvion",),
    "crecida": ("crecida",),
    "lluvia": ("aluvion", "crecida"),
    "nieve": ("nieve",),
}
LICENCIAS = [
    {"nombre": "Open-Meteo (CC BY 4.0)", "url": "https://open-meteo.com/en/license"},
    {
        "nombre": "© colaboradores de OpenStreetMap (ODbL 1.0)",
        "url": "https://www.openstreetmap.org/copyright",
    },
]


@dataclass
class BundleInputs:
    cfg: AppConfig
    lineage: Lineage
    eventos: pd.DataFrame
    articulos: pd.DataFrame
    jama: Sequence[JamaEstado]
    grilla: pd.DataFrame
    geo: Mapping[str, dict[str, Any]]
    pronostico: Mapping[str, PronosticoPunto]
    pronostico_hora: datetime | None
    uso: list[dict[str, str]]
    now: datetime


def local_iso(ts: datetime) -> str:
    return (ts.astimezone(UTC) + LOCAL_OFFSET).strftime("%Y-%m-%d %H:%M")


def _plain(v: Any) -> Any:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if isinstance(v, date | datetime):
        return v.isoformat()
    return v.item() if hasattr(v, "item") else v


# ------------------------------------------------------------------ geo
class Projection:
    """Equirectangular projection to an SVG box MAP_WIDTH wide (y grows southwards)."""

    def __init__(self, coords: Sequence[tuple[float, float]]) -> None:
        lons, lats = [c[0] for c in coords], [c[1] for c in coords]
        self.lon0, self.lat0 = min(lons), max(lats)
        self.kx = math.cos(math.radians((min(lats) + max(lats)) / 2))
        span = (max(lons) - self.lon0) * self.kx or 1.0
        self.scale = MAP_WIDTH / span
        self.height = (self.lat0 - min(lats)) * self.scale

    def xy(self, lon: float, lat: float) -> tuple[float, float]:
        return (
            round((lon - self.lon0) * self.kx * self.scale, 1),
            round((self.lat0 - lat) * self.scale, 1),
        )

    def path(self, line: Sequence[Sequence[float]]) -> str:
        pts = [self.xy(c[0], c[1]) for c in line]
        return "M" + "L".join(f"{x},{y}" for x, y in pts)


def _lines(geom: Mapping[str, Any]) -> list[Sequence[Sequence[float]]]:
    t, c = geom["type"], geom["coordinates"]
    lines: list[Sequence[Sequence[float]]] = {
        "LineString": [c],
        "MultiLineString": c,
        "Polygon": c,
    }.get(t, [r for p in c for r in p] if t == "MultiPolygon" else [])
    return lines


def geo_layers(geo: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    coords: list[tuple[float, float]] = []
    for fc in geo.values():
        for f in fc["features"]:
            g = f["geometry"]
            if g["type"] == "Point":
                coords.append((g["coordinates"][0], g["coordinates"][1]))
            for line in _lines(g):
                coords += [(p[0], p[1]) for p in line]
    proj = Projection(coords)
    lines = [
        {"capa": name, "id": f["properties"].get("id") or f["properties"].get("tipo", ""),
         "d": " ".join(proj.path(line) for line in _lines(f["geometry"]))}
        for name in ("rutas", "ferrocarril") for f in geo.get(name, {}).get("features", [])
    ]  # fmt: skip
    lugares = []
    for name in ("contexto", "puntos"):
        for f in geo.get(name, {}).get("features", []):
            if f["geometry"]["type"] != "Point":
                continue
            x, y = proj.xy(*f["geometry"]["coordinates"][:2])
            p = f["properties"]
            lugares.append({"capa": name, "id": p.get("id", ""), "tipo": p.get("tipo", "punto"),
                            "nombre": p.get("nombre", ""), "x": x, "y": y})  # fmt: skip
    return {
        "ancho": MAP_WIDTH,
        "alto": round(proj.height, 1),
        "lineas": lines,
        "lugares": lugares,
        "atribucion": LICENCIAS[1],
    }


# ------------------------------------------------------------------ events
def _records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return [{str(k): v for k, v in r.items()} for r in frame.to_dict("records")]


def _events(inp: BundleInputs, stable: frozenset[str]) -> list[dict[str, Any]]:
    """Every `ClosureEvent` field (read through the model, so new fields flow through),
    with `fuentes` replaced by `notas_medios` (outlet, headline, URL) and `estable`."""
    from corredor.catalog import frame_to_events

    names = {s.id: s.nombre for s in inp.cfg.fuentes}
    arts = {str(a["url"]): a for a in _records(inp.articulos)} if not inp.articulos.empty else {}
    out = []
    for ev in sorted(frame_to_events(inp.eventos), key=lambda e: (e.fecha, e.evento_id)):
        refs = [arts[u] for u in ev.fuentes if u in arts]
        row = ev.model_dump(mode="json", exclude={"fuentes"})
        row["id"] = row["evento_id"]
        row["estable"] = any(str(a["source_id"]) in stable for a in refs)
        row["notas_medios"] = [
            {"medio": names.get(str(a["source_id"]), str(a["source_id"])),
             "titular": str(a["titular"]), "url": str(a["url"])}
            for a in refs
        ]  # fmt: skip
        out.append(row)
    return out


def nearest_point(lat: float, lon: float, points: Sequence[CriticalPoint]) -> tuple[str, float]:
    """(point id, great-circle distance in km) of the critical point closest to (lat, lon).

    Same formula as `puntoMasCercano` in tablero/src/app.js (phone geolocation)."""

    def km(p: CriticalPoint) -> float:
        dlat, dlon = math.radians(p.lat - lat), math.radians(p.lon - lon)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat)) * math.cos(math.radians(p.lat)) * math.sin(dlon / 2) ** 2
        )
        return 2 * EARTH_KM * math.asin(math.sqrt(a))

    best = min(points, key=km)
    return best.id, km(best)


def _por_anio(events: Sequence[Mapping[str, Any]]) -> list[dict[str, int]]:
    years: dict[int, list[int]] = {}
    for e in events:
        row = years.setdefault(int(str(e["fecha"])[:4]), [0, 0])
        row[0 if e["estable"] else 1] += 1
    return [{"anio": y, "estables": a, "solo_nuevas": b} for y, (a, b) in sorted(years.items())]


# ------------------------------------------------------------------ Jama
def _ms_hhmm(v: Any) -> Any:
    return (
        f"{int(v) // 3_600_000:02d}:{int(v) % 3_600_000 // 60_000:02d}" if isinstance(v, int) else v
    )


def _display(row: Mapping[str, Any]) -> dict[str, Any]:
    out = {}
    for k, v in sorted(row.items()):
        if k == "FECHA" and isinstance(v, int):
            v = datetime.fromtimestamp(v / 1000, tz=UTC).date().isoformat()
        elif k in {"HORA", "ADESDE", "AHASTA"}:
            v = _ms_hhmm(v)
        out[k] = v
    return out


def jama_records(snap: JamaEstado) -> list[dict[str, Any]]:
    """Allowlisted payload records (already filtered at collection) as display values.

    The first is the crossing itself; argentina.gob.ar may append Jama Norte/Sur while their
    status differs from the usual one.
    """
    if not snap.payload_json:
        return []
    rows = json.loads(snap.payload_json)
    rows = rows if isinstance(rows, list) else [rows]
    return [_display(r) for r in rows if isinstance(r, dict)]


def _estado_jama(fuente: str, records: Sequence[Mapping[str, Any]]) -> str:
    keys = ("TRANSITABILIDAD",) if fuente == "mop_cl" else ("estado_prioridad", "estado_vialidad")
    parts = []
    for i, f in enumerate(records):
        vals = " / ".join(str(f[k]) for k in keys if f.get(k)) or "sin estado"
        parts.append(vals if i == 0 else f"{f.get('nombre_paso') or 'otro registro'}: {vals}")
    return " · ".join(parts) if parts else "sin estado"


def jama_section(snaps: Sequence[JamaEstado], now: datetime) -> dict[str, Any]:
    ordered = sorted(snaps, key=lambda s: s.fetched_at)
    ultimos = {}
    for s in ordered:
        ultimos[s.fuente] = s
    fuentes = []
    for fuente, s in sorted(ultimos.items()):
        recs = jama_records(s)
        age = now - s.fetched_at
        fuentes.append(
            {"fuente": fuente, "fetched_at": local_iso(s.fetched_at), "error": s.error,
             "estado": _estado_jama(fuente, recs), "campos": recs[0] if recs else {},
             "otros": recs[1:],
             "horas": round(age.total_seconds() / 3600, 1), "vieja": age > JAMA_STALE}
        )  # fmt: skip
    since = now - timedelta(days=JAMA_DAYS)
    linea = [
        {"fuente": s.fuente, "fetched_at": local_iso(s.fetched_at), "error": s.error,
         "estado": _estado_jama(s.fuente, jama_records(s))}
        for s in ordered if s.fetched_at >= since
    ]  # fmt: skip
    return {
        "ultimos": fuentes,
        "linea": linea,
        "vieja": any(f["vieja"] for f in fuentes) or not fuentes,
    }


# ------------------------------------------------------------------ points, limits
def _cells(grilla: pd.DataFrame) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if grilla.empty:
        return out
    for r in _records(grilla[grilla["modelo"] == "era5"]):
        mates = str(r["comparte_celda_con"] or "").replace(";", ",").split(",")
        out[str(r["punto_id"])] = {
            "comparte_con": [m.strip() for m in mates if m.strip()],
            "diferencia_m": _plain(r["diferencia_m"]),
        }
    return out


def _limitaciones(
    events: Sequence[Mapping[str, Any]], cells: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    train_end = ThresholdCalibrator().train_end.isoformat()
    test = {
        g: len({(e["punto_id"], e["fecha"]) for e in events
                if e["causa"] in causes and e["punto_id"] and e["fecha"] > train_end})
        for g, causes in WEATHER_GROUPS.items()
    }  # fmt: skip
    diffs = [c["diferencia_m"] for c in cells.values() if c["diferencia_m"] is not None]
    return {
        "eventos": len(events),
        "un_medio": sum(1 for e in events if e["n_medios"] <= 1),
        "dos_o_mas": sum(1 for e in events if e["n_medios"] >= 2),
        "con_fuente_estable": sum(1 for e in events if e["estable"]),
        "solo_nuevas": sum(1 for e in events if not e["estable"]),
        "sin_punto": sum(1 for e in events if not e["punto_id"]),
        "prueba_desde": train_end,
        "dias_evento_prueba": test,
        "dif_elevacion_min_m": min(diffs) if diffs else None,
        "dif_elevacion_max_m": max(diffs) if diffs else None,
        "puntos_celda_compartida": sum(1 for c in cells.values() if c["comparte_con"]),
    }


def build_bundle(inp: BundleInputs) -> dict[str, Any]:
    cfg = inp.cfg
    from corredor.catalog import stable_sources

    stable = stable_sources(cfg)
    events = _events(inp, stable)
    cells = _cells(inp.grilla)
    umbrales = [u.model_dump() | {"es_percentil": u.es_percentil} for u in cfg.umbrales_elegidos]
    puntos = []
    for p in cfg.puntos:
        fc = inp.pronostico.get(p.id)
        puntos.append(
            {
                "id": p.id, "nombre": p.nombre, "ruta": p.ruta, "km": p.km, "lat": p.lat,
                "lon": p.lon, "verificado": p.verificado, "nota_geo": p.nota_geo,
                "celda": cells.get(p.id),
                "eventos": sum(1 for e in events if e["punto_id"] == p.id),
                "pronostico": None if fc is None else {
                    "horizontes": fc.horizontes, "error": fc.error,
                    "clima_desde": _plain(fc.clima_desde), "clima_hasta": _plain(fc.clima_hasta),
                },
            }
        )  # fmt: skip
    lin = inp.lineage
    return {
        "encabezado": {
            "bundle_version": BUNDLE_VERSION,
            "version": lin.version,
            "git_commit": lin.git_commit,
            "schema_version": lin.schema_version,
            "generado": local_iso(inp.now),
            "pronostico_hora": local_iso(inp.pronostico_hora) if inp.pronostico_hora else None,
            "pronostico_modelo": cfg.clima.modelo_pronostico,
            "pronostico_horas": cfg.clima.pronostico_horas,
            "climatologia_desde": cfg.clima.pronostico_historico_desde.isoformat(),
            "modelo_historico": cfg.clima.modelo_historico,
        },
        "umbrales": umbrales,
        "puntos": puntos,
        "eventos": events,
        "por_anio": _por_anio(events),
        "jama": jama_section(inp.jama, inp.now),
        "limitaciones": _limitaciones(events, cells),
        "mapa": geo_layers(inp.geo),
        "uso": inp.uso,
        "fuentes": [{"nombre": s.nombre, "url": s.base_url} for s in cfg.enabled_sources()],
        "licencias": LICENCIAS,
    }


def read_geo(geo_dir: Path) -> dict[str, dict[str, Any]]:
    return {
        n: json.loads((geo_dir / f"{n}.geojson").read_text(encoding="utf-8"))
        for n in GEO_FILES
        if (geo_dir / f"{n}.geojson").exists()
    }


def markdown_blocks(text: str) -> list[dict[str, str]]:
    """Tiny Markdown subset (#/## headings, '- ' items, paragraphs) → text-only blocks."""
    blocks: list[dict[str, str]] = []
    para: list[str] = []

    def flush() -> None:
        if para:
            blocks.append({"tipo": "p", "texto": " ".join(para)})
            para.clear()

    for raw in text.splitlines():
        line = raw.strip().replace("**", "").replace("`", "")
        if not line:
            flush()
        elif line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            blocks.append({"tipo": "h1" if level == 1 else "h2", "texto": line.lstrip("# ")})
        elif line.startswith("- "):
            flush()
            blocks.append({"tipo": "li", "texto": line[2:]})
        elif raw.startswith("  ") and blocks and blocks[-1]["tipo"] == "li" and not para:
            blocks[-1]["texto"] += " " + line
        else:
            para.append(line)
    flush()
    return blocks
