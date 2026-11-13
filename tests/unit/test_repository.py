from datetime import date
from pathlib import Path

import pytest

from corredor.models import WeatherDay
from corredor.storage.repository import DuckDBRepository, UnknownTableError


def test_upsert_replaces_by_key(tmp_path: Path) -> None:
    repo = DuckDBRepository(tmp_path / "db.duckdb")
    rows = [
        WeatherDay(punto_id="p1", fecha=date(2024, 1, 1), precipitacion_mm=1.0),
        WeatherDay(punto_id="p1", fecha=date(2024, 1, 2), precipitacion_mm=2.0),
    ]
    assert repo.upsert("clima_diario", rows) == 2
    repo.upsert(
        "clima_diario", [WeatherDay(punto_id="p1", fecha=date(2024, 1, 2), precipitacion_mm=9.0)]
    )
    df = repo.read("clima_diario").sort_values("fecha")
    assert len(df) == 2
    assert df["precipitacion_mm"].tolist() == [1.0, 9.0]
    out = repo.export_parquet(tmp_path / "parquet")
    assert [p.name for p in out] == ["clima_diario.parquet"]
    repo.close()


def test_unknown_table_rejected() -> None:
    repo = DuckDBRepository(":memory:")
    with pytest.raises(UnknownTableError):
        repo.upsert('x"; DROP TABLE y; --', [{"a": 1}])
    with pytest.raises(UnknownTableError):
        repo.read("nope")


def test_read_missing_table_is_empty() -> None:
    repo = DuckDBRepository(":memory:")
    assert repo.read("eventos").empty
    assert repo.upsert("eventos", []) == 0
