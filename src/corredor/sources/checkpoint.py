"""Resumable per-source checkpoint (one JSON file per source under data/checkpoints/).

Keys are collection units: a month ("2024-02") for sitemaps, a year window ("2024") for
WordPress. Each unit records a status so an empty month is never confused with a month
whose fetch failed (HANDOFF §7.2.9):

- ok: processed completely;
- empty: the listing answered 2xx with no entries;
- missing: the listing answered 404 (the outlet has no file for that unit);
- error: a fetch failed (retried on the next run; cached pages cost nothing).

Units cut short by the per-run request cap are not recorded, so the next run redoes them.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

CheckpointStatus = Literal["ok", "empty", "missing", "error"]
DONE_STATUSES: frozenset[str] = frozenset({"ok", "empty", "missing"})


class Checkpoint:
    def __init__(self, path: Path | None) -> None:
        """`path=None` keeps the checkpoint in memory only (tests, dry runs)."""
        self.path = path
        self._units: dict[str, dict[str, Any]] = {}
        if path is not None and path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            self._units = dict(raw.get("units", {}))

    def get(self, key: str) -> dict[str, Any] | None:
        return self._units.get(key)

    def is_done(self, key: str) -> bool:
        entry = self._units.get(key)
        return entry is not None and entry.get("status") in DONE_STATUSES

    def mark(self, key: str, status: CheckpointStatus, **info: Any) -> None:
        self._units[key] = {
            "status": status,
            "updated_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
            **info,
        }
        self._save()

    def units(self) -> dict[str, dict[str, Any]]:
        return dict(self._units)

    def _save(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = {"units": dict(sorted(self._units.items()))}
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, self.path)
