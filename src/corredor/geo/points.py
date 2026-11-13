"""Critical points registry (verification and geocoding: Child C, feature/geo)."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol

from corredor.models import CriticalPoint, Ruta


class Geocoder(Protocol):
    def geocode(self, query: str) -> tuple[float, float] | None: ...


class CriticalPointRegistry:
    def __init__(self, points: Iterable[CriticalPoint], geocoder: Geocoder | None = None) -> None:
        self._points = {p.id: p for p in points}
        self.geocoder = geocoder

    def get(self, point_id: str) -> CriticalPoint:
        return self._points[point_id]

    def all(self) -> list[CriticalPoint]:
        return list(self._points.values())

    def by_route(self, ruta: Ruta) -> Sequence[CriticalPoint]:
        return [p for p in self._points.values() if p.ruta == ruta]

    def __len__(self) -> int:
        return len(self._points)
