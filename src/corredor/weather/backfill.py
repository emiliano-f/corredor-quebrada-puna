"""Weather stage: hourly archive per point → clima_diario, features and grid-cell report."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import pandas as pd

from corredor.http import FetchError
from corredor.models import CriticalPoint
from corredor.reports import Lineage, report_header
from corredor.storage.repository import Repository
from corredor.weather.features import antecedent_features, daily_weather
from corredor.weather.openmeteo import (
    CallBudgetExceeded,
    GridCell,
    OpenMeteoClient,
    OpenMeteoError,
    shared_cells,
)

GRID_COLUMNS = [
    "punto_id",
    "modelo",
    "lat_grilla",
    "lon_grilla",
    "elev_grilla_m",
    "elev_punto_m",
    "diferencia_m",
    "comparte_celda_con",
]


@dataclass
class WeatherRun:
    hourly: list[pd.DataFrame] = field(default_factory=list)
    cells: list[GridCell] = field(default_factory=list)
    days: int = 0
    done: list[str] = field(default_factory=list)
    error: str | None = None


def fetch_points(
    client: OpenMeteoClient,
    points: Sequence[CriticalPoint],
    start: date,
    end: date,
    repo: Repository,
) -> WeatherRun:
    """Grid cells for every point (cheap), then the full-range archive per point.

    Daily rows go to clima_diario. Stops at the first request that fails (daily cap, API
    error, network) and keeps what was done: cached requests cost no calls, so the next
    run resumes where this one stopped.
    """
    run = WeatherRun()
    point = None
    try:
        for point in points:
            run.cells.extend(client.grid_cells(point))
        for point in points:
            hourly = client.history(point, start, end)
            run.days += repo.upsert("clima_diario", daily_weather(hourly, point.id))
            run.hourly.append(hourly.assign(punto_id=point.id))
            run.done.append(point.id)
    except (CallBudgetExceeded, OpenMeteoError, FetchError) as exc:
        run.error = f"{point.id if point else '-'}: {exc}"
    return run


def grid_table(cells: Sequence[GridCell]) -> pd.DataFrame:
    shared = shared_cells(cells)
    rows = []
    for c in cells:
        mates = shared.get((c.modelo, c.lat_grilla, c.lon_grilla), [])
        rows.append(
            {
                "punto_id": c.punto_id,
                "modelo": c.modelo,
                "lat_grilla": c.lat_grilla,
                "lon_grilla": c.lon_grilla,
                "elev_grilla_m": c.elev_grilla_m,
                "elev_punto_m": c.elev_punto_m,
                "diferencia_m": c.diferencia_m,
                "comparte_celda_con": ", ".join(m for m in mates if m != c.punto_id),
            }
        )
    return pd.DataFrame(rows, columns=GRID_COLUMNS)


def write_outputs(run: WeatherRun, clima_dir: Path) -> list[Path]:
    """Write the run's points, keeping rows of points this run did not reach."""
    clima_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    if run.hourly:
        hourly = _merge(clima_dir / "horario.parquet", pd.concat(run.hourly, ignore_index=True))
        paths.append(clima_dir / "horario.parquet")
        hourly.to_parquet(paths[-1], index=False)
        paths.append(clima_dir / "antecedentes.parquet")
        antecedent_features(hourly).to_parquet(paths[-1], index=False)
    paths.append(clima_dir / "grilla.parquet")
    _with_mates(_merge(paths[-1], grid_table(run.cells))).to_parquet(paths[-1], index=False)
    return paths


def _with_mates(grid: pd.DataFrame) -> pd.DataFrame:
    """Recompute `comparte_celda_con` over every row, kept and fresh."""
    key = ["modelo", "lat_grilla", "lon_grilla"]
    members: dict[tuple[object, ...], list[str]] = {}
    for row in grid[[*key, "punto_id"]].itertuples(index=False):
        members.setdefault(tuple(row[:3]), []).append(str(row[3]))
    grid = grid.copy()
    grid["comparte_celda_con"] = [
        ", ".join(m for m in members[tuple(r[:3])] if m != r[3])
        for r in grid[[*key, "punto_id"]].itertuples(index=False)
    ]
    return grid


def _merge(path: Path, fresh: pd.DataFrame) -> pd.DataFrame:
    if not path.exists():
        return fresh
    old = pd.read_parquet(path)
    keep = old[~old["punto_id"].isin(fresh["punto_id"].unique())]
    if keep.empty:
        return fresh
    return pd.concat([keep, fresh], ignore_index=True)


def _fmt(value: float | None, digits: int = 0) -> str:
    return "s/d" if value is None else f"{value:.{digits}f}"


def grid_report(
    cells: Sequence[GridCell],
    info: Lineage,
    modelo_historico: str,
) -> str:
    """reports/clima_grilla.md: model, grid cell and elevation per point (Spanish)."""
    out = [report_header("Clima: modelo, celda de grilla y elevación por punto", info)]
    out.append(
        f"Datos: Open-Meteo Historical Weather API, modelo `{modelo_historico}` "
        "(ERA5 + ERA5-Land, ECMWF/Copernicus), licencia CC BY 4.0. "
        "Son datos de reanálisis en grilla, no mediciones de una estación en el punto.\n\n"
        "- `Elev. punto`: la elevación real del punto según el modelo digital de elevación "
        "de 90 m (Copernicus GLO-90) que Open-Meteo usa para corregir la temperatura.\n"
        "- `Elev. celda`: la elevación media de la celda del modelo (`elevation=nan`).\n"
        "- La lluvia y la nieve salen de ERA5 (celdas de 0,25°, ~28 km); "
        "la temperatura, de ERA5-Land (0,1°, ~11 km).\n\n"
    )
    groups = shared_cells(cells)
    for model in dict.fromkeys(c.modelo for c in cells):
        out.append(f"## Celdas `{model}`\n\n")
        out.append(
            "| Punto | Celda (lat, lon) | Elev. celda (m) | Elev. punto (m) | "
            "Celda − punto (m) | Comparte celda con |\n"
            "|---|---|---:|---:|---:|---|\n"
        )
        for c in (c for c in cells if c.modelo == model):
            mates = [
                m for m in groups.get((model, c.lat_grilla, c.lon_grilla), []) if m != c.punto_id
            ]
            out.append(
                f"| {c.punto_id} | {c.lat_grilla:.2f}, {c.lon_grilla:.2f} | "
                f"{_fmt(c.elev_grilla_m)} | {_fmt(c.elev_punto_m)} | "
                f"{_fmt(c.diferencia_m)} | {', '.join(mates) or '—'} |\n"
            )
        out.append("\n")
    out.append("## Puntos que comparten celda\n\n")
    if not groups:
        out.append("Ningún punto comparte celda.\n")
    for (model, lat, lon), ids in sorted(groups.items()):
        out.append(f"- `{model}` ({lat:.2f}, {lon:.2f}): {', '.join(ids)}\n")
    return "".join(out)
