"""Storage: Repository interface + DuckDB implementation (+ Parquet export).

SQL safety: table names are validated against TABLE_KEYS (allowlist) and quoted; data
never goes into SQL strings — rows are passed as a registered DataFrame.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Protocol

import duckdb
import pandas as pd
from pydantic import BaseModel

# Primary key per table. Adding a table = adding it here + documenting it in docs/DATOS.md.
TABLE_KEYS: dict[str, tuple[str, ...]] = {
    "articulos": ("source_id", "url"),
    "eventos": ("evento_id",),
    "puntos": ("id",),
    "clima_diario": ("punto_id", "fecha"),
    "jama_estado": ("fuente", "fetched_at"),
}

Row = BaseModel | Mapping[str, Any]


class UnknownTableError(KeyError):
    pass


class Repository(Protocol):
    def upsert(self, table: str, rows: Sequence[Row]) -> int: ...

    def read(self, table: str) -> pd.DataFrame: ...


def _to_frame(rows: Sequence[Row]) -> pd.DataFrame:
    records = [r.model_dump(mode="json") if isinstance(r, BaseModel) else dict(r) for r in rows]
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
        self._con.register("incoming", frame)
        try:
            if not self._exists(table):
                self._con.execute(f"CREATE TABLE {qt} AS SELECT * FROM incoming")  # noqa: S608 — allowlisted, quoted identifier
            else:
                cols = ", ".join(_quote(k) for k in keys)
                self._con.execute(
                    f"DELETE FROM {qt} WHERE ({cols}) IN (SELECT {cols} FROM incoming)"  # noqa: S608 — allowlisted identifiers
                )
                self._con.execute(f"INSERT INTO {qt} BY NAME SELECT * FROM incoming")  # noqa: S608 — allowlisted, quoted identifier
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
