"""Storage: Repository interface + DuckDB implementation (+ Parquet export).

SQL safety: table names are validated against TABLE_KEYS (allowlist) and quoted; data
never goes into SQL strings — rows are passed as a registered DataFrame.
"""

from __future__ import annotations

import types
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal, Protocol, Union, get_args, get_origin

import duckdb
import pandas as pd
from pydantic import BaseModel

from corredor.models import Article, ClosureEvent, CriticalPoint, JamaEstado, WeatherDay

# Primary key per table. Adding a table = adding it here + documenting it in docs/DATOS.md.
TABLE_KEYS: dict[str, tuple[str, ...]] = {
    "articulos": ("source_id", "url"),
    "eventos": ("evento_id",),
    "puntos": ("id",),
    "clima_diario": ("punto_id", "fecha"),
    "jama_estado": ("fuente", "fetched_at"),
}

TABLE_MODELS: dict[str, type[BaseModel]] = {
    "articulos": Article,
    "eventos": ClosureEvent,
    "puntos": CriticalPoint,
    "clima_diario": WeatherDay,
    "jama_estado": JamaEstado,
}

Row = BaseModel | Mapping[str, Any]

_SCALAR_TYPES: dict[type, str] = {
    str: "VARCHAR",
    int: "BIGINT",
    float: "DOUBLE",
    bool: "BOOLEAN",
    date: "DATE",
    datetime: "TIMESTAMPTZ",
}


def duckdb_type(annotation: Any) -> str:
    """DuckDB column type for a pydantic field annotation (Optional is unwrapped)."""
    origin = get_origin(annotation)
    if origin in (Union, types.UnionType):
        args = [a for a in get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return duckdb_type(args[0])
        return "VARCHAR"
    if origin is Literal:
        values = get_args(annotation)
        return "BIGINT" if all(isinstance(v, int) for v in values) else "VARCHAR"
    if origin is list:
        (inner,) = get_args(annotation)
        return duckdb_type(inner) + "[]"
    for py_type, sql in _SCALAR_TYPES.items():
        if annotation is py_type:
            return sql
    return "VARCHAR"


def create_table_sql(table: str) -> str:
    model = TABLE_MODELS[table]
    cols = ", ".join(
        f"{_quote(name)} {duckdb_type(field.annotation)}"
        for name, field in model.model_fields.items()
    )
    return f"CREATE TABLE IF NOT EXISTS {_quote(table)} ({cols})"


class UnknownTableError(KeyError):
    pass


class Repository(Protocol):
    def upsert(self, table: str, rows: Sequence[Row]) -> int: ...

    def read(self, table: str) -> pd.DataFrame: ...


def _to_frame(rows: Sequence[Row]) -> pd.DataFrame:
    records = [r.model_dump() if isinstance(r, BaseModel) else dict(r) for r in rows]
    return pd.DataFrame.from_records(records)


def _quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


class DuckDBRepository:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path) if str(path) != ":memory:" else None
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._con = duckdb.connect(str(path))

    def _keys(self, table: str) -> tuple[str, ...]:
        if table not in TABLE_KEYS:
            raise UnknownTableError(table)
        return TABLE_KEYS[table]

    def _exists(self, table: str) -> bool:
        row = self._con.execute(
            "SELECT count(*) FROM information_schema.tables WHERE table_name = ?", [table]
        ).fetchone()
        return bool(row and row[0])

    def upsert(self, table: str, rows: Sequence[Row]) -> int:
        """Insert rows, replacing existing rows with the same primary key."""
        keys = self._keys(table)
        if not rows:
            return 0
        frame = _to_frame(rows).drop_duplicates(subset=list(keys), keep="last")
        qt = _quote(table)
        cols = ", ".join(_quote(k) for k in keys)
        self._con.register("incoming", frame)
        try:
            self._con.execute("BEGIN TRANSACTION")
            try:
                self._con.execute(create_table_sql(table))
                self._con.execute(
                    f"DELETE FROM {qt} WHERE ({cols}) IN (SELECT {cols} FROM incoming)"  # noqa: S608 — allowlisted identifiers
                )
                self._con.execute(f"INSERT INTO {qt} BY NAME SELECT * FROM incoming")  # noqa: S608 — allowlisted, quoted identifier
            except Exception:
                self._con.execute("ROLLBACK")
                raise
            self._con.execute("COMMIT")
        finally:
            self._con.unregister("incoming")
        return len(frame)

    def read(self, table: str) -> pd.DataFrame:
        self._keys(table)
        if not self._exists(table):
            return pd.DataFrame()
        return self._con.execute(f"SELECT * FROM {_quote(table)}").df()  # noqa: S608 — allowlisted, quoted identifier

    def export_parquet(self, out_dir: Path) -> list[Path]:
        out_dir.mkdir(parents=True, exist_ok=True)
        written = []
        for table in TABLE_KEYS:
            if self._exists(table):
                path = out_dir / f"{table}.parquet"
                self.read(table).to_parquet(path, index=False)
                written.append(path)
        return written

    def close(self) -> None:
        self._con.close()
