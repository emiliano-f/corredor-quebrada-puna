from datetime import date
from pathlib import Path

import pandas as pd

from corredor.config import ClimaConfig
from corredor.models import CriticalPoint
from corredor.reports import Lineage
from corredor.storage.repository import DuckDBRepository
from corredor.weather.backfill import fetch_points, grid_report, write_outputs
from corredor.weather.openmeteo import GridCell, OpenMeteoClient

from .test_openmeteo import NOW, POINT, FakeFetcher

INFO = Lineage(
    version="0.1.0", git_commit="abc1234", schema_version=1, sources_hash="f" * 16, generated_at=NOW
)
TWIN = CriticalPoint(id="rn9_twin", nombre="Gemelo", ruta="RN9", lat=-23.91709, lon=-65.46402)


def test_fetch_points_loads_clima_diario_and_outputs(tmp_path: Path) -> None:
    client = OpenMeteoClient(FakeFetcher(), tmp_path / "clima", ClimaConfig(), now=lambda: NOW)
    repo = DuckDBRepository(tmp_path / "db.duckdb")
    run = fetch_points(client, [POINT, TWIN], date(2016, 1, 1), date(2016, 1, 8), repo)
    assert run.error is None
    assert run.done == ["rn9_volcan", "rn9_twin"]
    assert run.days == 16
    daily = repo.read("clima_diario")
    repo.close()
    assert len(daily) == 16
    assert daily["precipitacion_mm"].notna().all()
    paths = write_outputs(run, tmp_path / "clima")
    assert [p.name for p in paths] == ["horario.parquet", "antecedentes.parquet", "grilla.parquet"]
    feats = pd.read_parquet(paths[1])
    assert set(feats["punto_id"]) == {"rn9_volcan", "rn9_twin"}
    grid = pd.read_parquet(paths[2])
    assert set(grid["comparte_celda_con"]) == {"rn9_twin", "rn9_volcan"}
    report = grid_report(run.cells, INFO, "era5_seamless")
    assert report.startswith("# Clima: modelo, celda de grilla y elevación por punto")
    assert "`era5` (-24.00, -65.50): rn9_volcan, rn9_twin" in report
    assert "| rn9_volcan | -24.00, -65.50 |" in report


def test_fetch_points_stops_at_cap_and_keeps_done(tmp_path: Path) -> None:
    cfg = ClimaConfig(max_llamadas_diarias=7.5)
    client = OpenMeteoClient(FakeFetcher(), tmp_path / "clima", cfg, now=lambda: NOW)
    repo = DuckDBRepository(tmp_path / "db.duckdb")
    other = TWIN.model_copy(update={"id": "rn9_other", "lat": -23.5})
    run = fetch_points(client, [POINT, other], date(2016, 1, 1), date(2016, 1, 8), repo)
    repo.close()
    assert run.done == ["rn9_volcan"]
    assert len(run.cells) == 4
    assert run.error is not None
    assert run.error.startswith("rn9_other: ")
    assert "tope diario" in run.error


def test_grid_report_without_shared_cells_or_elevation() -> None:
    cells = [GridCell("a", "era5", -24.0, -65.5, None, 2000.0)]
    report = grid_report(cells, INFO, "era5_seamless")
    assert "Ningún punto comparte celda." in report
    assert "| a | -24.00, -65.50 | s/d | 2000 | s/d | — |" in report
