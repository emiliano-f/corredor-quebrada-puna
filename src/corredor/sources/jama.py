"""Paso de Jama status snapshot collectors (one request per source per run).

Each collector fetches its source once with the PoliteFetcher (cache bypassed: these are
live status endpoints), keeps only the raw Jama record(s) and returns one JamaEstado row.
A failed request or an unexpected payload never raises: it becomes a row with `error`.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar
from urllib.parse import urlencode

from corredor.http import Fetcher, FetchError, FetchResult
from corredor.models import FuenteJama, JamaEstado, SourceConfig

JsonRecord = dict[str, Any]


class PayloadError(ValueError):
    """The source answered, but not with the expected Jama record."""


class JamaCollector(ABC):
    FUENTE: ClassVar[FuenteJama]
    PARSER_VERSION: ClassVar[int] = 1

    def __init__(
        self,
        config: SourceConfig,
        fetcher: Fetcher,
        now: Callable[[], datetime] = lambda: datetime.now(tz=UTC),
    ) -> None:
        self.config = config
        self.fetcher = fetcher
        self._now = now

    @property
    def source_id(self) -> str:
        return self.config.id

    @abstractmethod
    def url(self) -> str:
        """The single URL requested per run."""

    @abstractmethod
    def records(self, data: Any) -> list[JsonRecord]:
        """Raw Jama record(s) from the decoded JSON body. Raises PayloadError."""

    def snapshot(self) -> JamaEstado:
        try:
            result = self.fetcher.get(self.url(), refresh=True)
        except FetchError as exc:
            return self._error(f"{type(exc).__name__}: {exc}", self._now())
        try:
            payload = self.records(_decode(result))
        except PayloadError as exc:
            return self._error(str(exc), result.fetched_at)
        except (TypeError, ValueError, KeyError, AttributeError) as exc:
            return self._error(
                f"respuesta inesperada ({type(exc).__name__}: {exc})", result.fetched_at
            )
        return JamaEstado(
            fuente=self.FUENTE,
            fetched_at=result.fetched_at.astimezone(UTC),
            payload_json=json.dumps(payload, ensure_ascii=False, sort_keys=True),
        )

    def _error(self, message: str, at: datetime) -> JamaEstado:
        return JamaEstado(fuente=self.FUENTE, fetched_at=at.astimezone(UTC), error=message)


class MopChileJama(JamaCollector):
    """ArcGIS MapServer layer of Vialidad MOP Chile; Jama is one OBJECTID."""

    FUENTE = "mop_cl"

    @property
    def objectid(self) -> int:
        return int(self.config.params["objectid"])

    def url(self) -> str:
        query = urlencode({"where": f"OBJECTID={self.objectid}", "outFields": "*", "f": "json"})
        return f"{self.config.base_url.rstrip('/')}/query?{query}"

    def records(self, data: Any) -> list[JsonRecord]:
        if not isinstance(data, dict):
            raise PayloadError("respuesta ArcGIS inesperada (no es un objeto JSON)")
        if "error" in data:
            raise PayloadError(f"error ArcGIS: {json.dumps(data['error'], ensure_ascii=False)}")
        found = [
            f["attributes"]
            for f in data.get("features") or []
            if isinstance(f, dict)
            and isinstance(f.get("attributes"), dict)
            and f["attributes"].get("OBJECTID") == self.objectid
        ]
        if not found:
            raise PayloadError(f"OBJECTID {self.objectid} no está en la respuesta")
        return found


class ArgentinaGobArJama(JamaCollector):
    """argentina.gob.ar crossings listing (JSON with every crossing; only Jama is kept).

    `params.ids` are always stored. `params.ids_si_cambian` (Jama Norte/Sur, not open to
    traffic) are stored only while their status differs from `params.estado_base`.
    """

    FUENTE = "argentina_gob_ar"

    def url(self) -> str:
        return self.config.base_url

    def records(self, data: Any) -> list[JsonRecord]:
        if not isinstance(data, list):
            raise PayloadError("listado inesperado (no es una lista JSON)")
        by_id = {r.get("id"): r for r in data if isinstance(r, dict)}
        ids: list[int] = list(self.config.params.get("ids", []))
        missing = [i for i in ids if i not in by_id]
        if missing:
            raise PayloadError(f"ids {missing} no están en el listado")
        out = [by_id[i] for i in ids]
        base: Mapping[str, Any] = self.config.params.get("estado_base", {})
        for extra in self.config.params.get("ids_si_cambian", []):
            record = by_id.get(extra)
            if record is not None and any(record.get(k) != v for k, v in base.items()):
                out.append(record)
        return out


COLLECTORS: dict[str, type[JamaCollector]] = {
    "jama_mop_cl": MopChileJama,
    "jama_argentina_gob_ar": ArgentinaGobArJama,
}


def build_collectors(configs: Iterable[SourceConfig], fetcher: Fetcher) -> list[JamaCollector]:
    """Every enabled `snapshot` source that has a collector class."""
    built: list[JamaCollector] = []
    for cfg in configs:
        if not cfg.enabled or cfg.metodo != "snapshot":
            continue
        cls = COLLECTORS.get(cfg.id)
        if cls is None:
            raise LookupError(f"no collector for snapshot source {cfg.id!r}")
        built.append(cls(cfg, fetcher))
    return built


def append_jsonl(path: Path, rows: Iterable[JamaEstado]) -> int:
    """Append one JSON line per row; returns how many lines were written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [row.model_dump_json() + "\n" for row in rows]
    with path.open("a", encoding="utf-8") as fh:
        fh.writelines(lines)
    return len(lines)


def read_jsonl(path: Path) -> list[JamaEstado]:
    """Rows of a snapshots file (for loading `jama_estado`); blank lines are skipped."""
    with path.open(encoding="utf-8") as fh:
        return [JamaEstado.model_validate_json(line) for line in fh if line.strip()]


def _decode(result: FetchResult) -> Any:
    if not result.ok:
        raise PayloadError(f"HTTP {result.status}")
    try:
        return json.loads(result.content)
    except ValueError as exc:
        raise PayloadError(f"JSON inválido: {exc}") from exc
