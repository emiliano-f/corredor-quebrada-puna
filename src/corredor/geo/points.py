"""Critical points: registry, verification against OSM route lines, Nominatim geocoding.

Coordinates are never invented: they come from an OSM object (config `osm`) or from
Nominatim, and a point is only `verificado` when its OSM object is a node/way within
`max_offset_m` of the route line. Anything else is kept but flagged in `nota_geo`.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol
from urllib.parse import urlencode

from corredor.geo.routes import OsmElement, RouteLine, parse_ref
from corredor.http import Fetcher
from corredor.models import CriticalPoint, Ruta

log = logging.getLogger(__name__)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
MAX_OFFSET_M = 500.0


class Geocoder(Protocol):
    def geocode(self, query: str) -> tuple[float, float] | None: ...


class NominatimGeocoder:
    """Nominatim /search over a `Fetcher` (PoliteFetcher: custom User-Agent, >= 2 s per host
    — stricter than Nominatim's 1 req/s —, robots.txt, on-disk cache) plus an in-run memo.

    `DisallowedByRobots` is not swallowed: if Nominatim forbids /search we stop and report.
    """

    def __init__(
        self, fetcher: Fetcher, base_url: str = NOMINATIM_URL, country: str = "ar"
    ) -> None:
        self.fetcher = fetcher
        self.base_url = base_url
        self.country = country
        self._memo: dict[str, tuple[float, float] | None] = {}

    def url_for(self, query: str) -> str:
        params = {"q": query, "format": "jsonv2", "limit": "1", "countrycodes": self.country}
        return f"{self.base_url}?{urlencode(params)}"

    def geocode(self, query: str) -> tuple[float, float] | None:
        if query in self._memo:
            return self._memo[query]
        result = self.fetcher.get(self.url_for(query))
        found: tuple[float, float] | None = None
        if result.ok:
            hits = json.loads(result.text)
            if hits:
                found = (float(hits[0]["lat"]), float(hits[0]["lon"]))
        self._memo[query] = found
        return found


@dataclass(frozen=True)
class PointCheck:
    point: CriticalPoint
    distancia_m: float | None
    problemas: list[str] = field(default_factory=list)


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

    def verified(self) -> list[CriticalPoint]:
        return [p for p in self._points.values() if p.verificado]

    def __len__(self) -> int:
        return len(self._points)

    def osm_refs(self) -> list[str]:
        return [p.osm for p in self._points.values() if p.osm]

    def verify(
        self,
        elements: Mapping[str, OsmElement],
        routes: Mapping[str, RouteLine],
        max_offset_m: float = MAX_OFFSET_M,
    ) -> list[PointCheck]:
        """Re-derive lat/lon/km/sources of every point from OSM; replace the registry's points."""
        checks = [self._verify_one(p, elements, routes, max_offset_m) for p in self.all()]
        _check_order(checks)
        self._points = {c.point.id: c.point for c in checks}
        return checks

    def _verify_one(
        self,
        p: CriticalPoint,
        elements: Mapping[str, OsmElement],
        routes: Mapping[str, RouteLine],
        max_offset_m: float,
    ) -> PointCheck:
        if not p.osm:
            return self._geocode_fallback(p)
        kind, _ = parse_ref(p.osm)
        el = elements.get(p.osm)
        if el is None:
            return _unverified(p, None, f"objeto {p.osm} no encontrado en OSM")
        route = routes[p.ruta]
        km, dist = route.km_at(el.latlon)
        problems: list[str] = []
        if kind == "relation":
            problems.append("relación OSM: el centro del bbox no es un punto de la ruta")
        if dist > max_offset_m:
            problems.append(f"a {dist:.0f} m de la traza (> {max_offset_m:.0f} m)")
        label = el.name or "sin nombre"
        updated = p.model_copy(
            update={
                "lat": round(el.lat, 6),
                "lon": round(el.lon, 6),
                "km": round(km, 1),
                "verificado": not problems,
                "fuente_geo": f"OSM {p.osm} ('{label}'), a {dist:.0f} m de la traza {p.ruta}",
                "fuente_km": route.fuente_km,
                "nota_geo": p.nota_geo or "; ".join(problems),
            }
        )
        return PointCheck(updated, dist, problems)

    def _geocode_fallback(self, p: CriticalPoint) -> PointCheck:
        if self.geocoder is None:
            return _unverified(p, None, "sin objeto OSM ni geocodificador")
        hit = self.geocoder.geocode(f"{p.nombre}, Jujuy, Argentina")
        if hit is None:
            return _unverified(p, None, "Nominatim sin resultado")
        updated = p.model_copy(
            update={
                "lat": round(hit[0], 6),
                "lon": round(hit[1], 6),
                "verificado": False,
                "fuente_geo": f"Nominatim '{p.nombre}' (sin verificar)",
            }
        )
        return _unverified(updated, None, "geocodificado con Nominatim: revisar a mano")


def _unverified(p: CriticalPoint, dist: float | None, reason: str) -> PointCheck:
    note = p.nota_geo or reason
    return PointCheck(p.model_copy(update={"verificado": False, "nota_geo": note}), dist, [reason])


def _check_order(checks: list[PointCheck]) -> None:
    """Points of a route must be listed in increasing km (config order = road order)."""
    last: dict[str, tuple[float, str]] = {}
    for c in checks:
        km = c.point.km
        if km is None:
            continue
        prev = last.get(c.point.ruta)
        if prev is not None and km < prev[0]:
            c.problemas.append(f"orden: km {km:.1f} < km {prev[0]:.1f} de {prev[1]}")
        last[c.point.ruta] = (km, c.point.id)


def verification_report(checks: Sequence[PointCheck], current: Sequence[CriticalPoint]) -> str:
    """Markdown table (Spanish) comparing OSM-derived values with config.yaml."""
    cur = {p.id: p for p in current}
    lines = [
        "| id | ruta | km | lat, lon | dist. traza (m) | verificado | coincide con config.yaml | "
        "observaciones |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c in checks:
        p = c.point
        same = _same(p, cur.get(p.id))
        dist = "—" if c.distancia_m is None else f"{c.distancia_m:.0f}"
        km = "—" if p.km is None else f"{p.km:.1f}"
        obs = _md_cell("; ".join(c.problemas)) or "—"
        lines.append(
            f"| {p.id} | {p.ruta} | {km} | {p.lat:.5f}, {p.lon:.5f} | {dist} | "
            f"{'sí' if p.verificado else 'no'} | {'sí' if same else '**no**'} | {obs} |"
        )
    n = sum(c.point.verificado for c in checks)
    lines.append("")
    lines.append(f"Puntos verificados: {n} de {len(checks)}.")
    return "\n".join(lines) + "\n"


def _md_cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def _same(a: CriticalPoint, b: CriticalPoint | None) -> bool:
    if b is None:
        return False
    keys = ("lat", "lon", "km", "verificado", "fuente_geo", "fuente_km")
    return all(getattr(a, k) == getattr(b, k) for k in keys)
