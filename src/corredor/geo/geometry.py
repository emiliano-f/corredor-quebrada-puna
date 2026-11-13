"""Small spherical-geometry helpers (no GIS dependency): distances and chainage."""

from __future__ import annotations

import heapq
import itertools
import math
from collections.abc import Sequence
from dataclasses import dataclass

EARTH_RADIUS_M = 6_371_008.8

LatLon = tuple[float, float]


def haversine_m(a: LatLon, b: LatLon) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return 2 * EARTH_RADIUS_M * math.asin(min(1.0, math.sqrt(h)))


def line_length_m(line: Sequence[LatLon]) -> float:
    return sum(haversine_m(line[i], line[i + 1]) for i in range(len(line) - 1))


@dataclass(frozen=True)
class Projection:
    """Closest point of a polyline to a target point."""

    point: LatLon
    distance_m: float
    chainage_m: float


def project(target: LatLon, line: Sequence[LatLon]) -> Projection:
    """Project `target` onto `line` (local equirectangular approximation per segment).

    `chainage_m` is the distance along the line from its first vertex to the projection.
    """
    if len(line) < 2:
        raise ValueError("line needs at least two vertices")
    best: Projection | None = None
    walked = 0.0
    for a, b in itertools.pairwise(line):
        seg = haversine_m(a, b)
        point, frac = _closest_on_segment(target, a, b)
        dist = haversine_m(target, point)
        if best is None or dist < best.distance_m:
            best = Projection(point=point, distance_m=dist, chainage_m=walked + frac * seg)
        walked += seg
    assert best is not None  # noqa: S101 — loop runs at least once (len(line) >= 2)
    return best


def _closest_on_segment(p: LatLon, a: LatLon, b: LatLon) -> tuple[LatLon, float]:
    kx = math.cos(math.radians(p[0]))
    ax, ay = a[1] * kx, a[0]
    bx, by = b[1] * kx, b[0]
    px, py = p[1] * kx, p[0]
    dx, dy = bx - ax, by - ay
    norm = dx * dx + dy * dy
    frac = 0.0 if norm == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / norm))
    return (a[0] + frac * (b[0] - a[0]), a[1] + frac * (b[1] - a[1])), frac


def stitch(
    segments: Sequence[Sequence[LatLon]], start: LatLon, end: LatLon, gap_m: float
) -> list[LatLon]:
    """Shortest path through OSM way geometries from the vertex nearest `start` to the one
    nearest `end`. Way ends closer than `gap_m` are bridged (OSM relations often have small
    gaps or both carriageways); the result is one ordered polyline of OSM vertices.
    """
    adj: dict[LatLon, list[tuple[LatLon, float]]] = {}

    def link(a: LatLon, b: LatLon, w: float) -> None:
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))

    root: dict[LatLon, LatLon] = {}

    def find(v: LatLon) -> LatLon:
        while root.setdefault(v, v) != v:
            root[v] = root[root[v]]
            v = root[v]
        return v

    for seg in segments:
        for a, b in itertools.pairwise(seg):
            link(a, b, haversine_m(a, b))
            root[find(a)] = find(b)
    ends = [v for seg in segments if seg for v in (seg[0], seg[-1])]
    for i, a in enumerate(ends):
        for b in ends[i + 1 :]:
            d = haversine_m(a, b)
            # Bridge only separate pieces: a bridge inside a connected piece would cut curves.
            if 0 < d <= gap_m and find(a) != find(b):
                link(a, b, d)
                root[find(a)] = find(b)
    if not adj:
        raise ValueError("no geometry to stitch")
    source = min(adj, key=lambda v: haversine_m(v, start))
    target = min(adj, key=lambda v: haversine_m(v, end))
    dist = {source: 0.0}
    prev: dict[LatLon, LatLon] = {}
    queue: list[tuple[float, LatLon]] = [(0.0, source)]
    while queue:
        d, u = heapq.heappop(queue)
        if u == target:
            break
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist.get(v, math.inf):
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(queue, (d + w, v))
    if target not in dist:
        raise ValueError("start and end are not connected")
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return path[::-1]
