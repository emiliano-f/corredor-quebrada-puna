from datetime import date
from pathlib import Path

import duckdb
import pytest

from corredor.models import ClosureEvent, WeatherDay
from corredor.storage.repository import DuckDBRepository, UnknownTableError, duckdb_type


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


def _event(**kw: object) -> ClosureEvent:
    base = {
        "evento_id": "e1",
        "fecha": date(2024, 2, 1),
        "ruta": "RN52",
        "causa": "aluvion",
        "tipo_corte": "total",
        "fuentes": ["https://a"],
        "n_medios": 1,
        "metodo": "reglas",
        "confianza": "alta",
    }
    return ClosureEvent.model_validate({**base, **kw})


def test_schema_comes_from_models_not_first_batch() -> None:
    repo = DuckDBRepository(":memory:")
    repo.upsert("eventos", [_event(hora=None, km=None)])
    repo.upsert("eventos", [_event(evento_id="e2", hora="10:30", km=46.5)])
    df = repo.read("eventos").set_index("evento_id")
    assert df.loc["e2", "hora"] == "10:30"
    assert df.loc["e2", "km"] == 46.5
    assert list(df.loc["e2", "fuentes"]) == ["https://a"]


def test_failed_upsert_keeps_existing_rows() -> None:
    repo = DuckDBRepository(":memory:")
    repo.upsert("clima_diario", [WeatherDay(punto_id="p1", fecha=date(2024, 1, 1))])
    bad = {"punto_id": "p1", "fecha": date(2024, 1, 1), "columna_inexistente": 1}
    with pytest.raises(duckdb.Error):
        repo.upsert("clima_diario", [bad])
    assert len(repo.read("clima_diario")) == 1


@pytest.mark.parametrize(
    ("annotation", "sql"),
    [(str | None, "VARCHAR"), (float | None, "DOUBLE"), (list[str], "VARCHAR[]"), (date, "DATE")],
)
def test_duckdb_type(annotation: object, sql: str) -> None:
    assert duckdb_type(annotation) == sql
