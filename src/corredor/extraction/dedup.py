"""Event deduplication (integration step): same route + point, dates within N days."""

from __future__ import annotations

from collections.abc import Sequence

from corredor.models import ClosureEvent


class EventDeduplicator:
    """Merges duplicates; n_medios excludes sources with `republica: true`."""

    def __init__(self, window_days: int = 2, republishers: frozenset[str] = frozenset()) -> None:
        self.window_days = window_days
        self.republishers = republishers

    def merge(self, events: Sequence[ClosureEvent]) -> list[ClosureEvent]:
        raise NotImplementedError("EventDeduplicator: pendiente (integración)")
