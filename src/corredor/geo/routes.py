"""OSM data via Overpass: route lines (RN 9, RN 52, Tren Solar railway), context points and
GeoJSON export. Every coordinate comes from OpenStreetMap (© OpenStreetMap contributors, ODbL).

Overpass fair use: a handful of small queries per run, all through `PoliteFetcher`
(robots.txt, >= 2 s per host, custom User-Agent, permanent cache under data/cache).
"""

from __future__ import annotations

import json
import logging
import statistics
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import quote

from corredor.geo.geometry import LatLon, line_length_m, project, stitch
from corredor.http import Fetcher, FetchError
from corredor.models import CriticalPoint

log = logging.getLogger(__name__)

# overpass-api.de disallows /api/ in robots.txt; these mirrors have no rules against it.
OVERPASS_ENDPOINTS: tuple[str, ...] = (
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
)

ATTRIBUTION = "© OpenStreetMap contributors"
LICENSE = "ODbL-1.0 (https://opendatacommons.org/licenses/odbl/1-0/)"
COPYRIGHT_URL = "https://www.openstreetmap.org/copyright"

RN9_BBOX = "-24.2,-65.6,-23.15,-65.25"  # S,W,N,E: San Salvador de Jujuy (km 1692) → Huacalera+
RN52_RELATION = 1745344
TREN_SOLAR_RELATION = 17730839
PASO_DE_JAMA_NODE = 311458189

# Context points: OSM objects checked by hand (see docs/DATOS.md): (ref, tipo, nombre, nota).
CONTEXT_OBJECTS: tuple[tuple[str, str, str, str], ...] = (
    ("node/13735789123", "litio", "Cauchari-Olaroz", ""),
    (
        "way/209386890",
        "litio",
        "Salar de Olaroz",
        "La operación Olaroz no está mapeada en OSM como objeto con nombre; "
        "se muestra el centro del salar, no la planta",
    ),
)

Q_RN9 = f'[out:json][timeout:50];way["highway"]["ref"~"^(RN ?)?9$"]({RN9_BBOX});out geom;'
Q_RN52 = f"[out:json][timeout:50];rel({RN52_RELATION});out geom;"
Q_MILESTONES = '[out:json][timeout:50];node["highway"="milestone"](-24.3,-67.2,-23.0,-65.2);out;'
Q_TREN = f"[out:json][timeout:50];rel({TREN_SOLAR_RELATION});out geom;"
Q_TREN_NODES = f"[out:json][timeout:50];rel({TREN_SOLAR_RELATION});node(r);out;"


class OverpassError(FetchError):
    """Overpass answered with an error remark or every endpoint failed."""


@dataclass(frozen=True)
class OsmElement:
    ref: str  # "node/123"
    lat: float
    lon: float
    tags: Mapping[str, str] = field(default_factory=dict)

    @property
    def latlon(self) -> LatLon:
        return (self.lat, self.lon)

    @property
    def name(self) -> str:
        return self.tags.get("name", "")


def parse_ref(ref: str) -> tuple[str, int]:
    kind, _, num = ref.partition("/")
    if kind not in ("node", "way", "relation") or not num.isdigit():
        raise ValueError(
            f"invalid OSM ref: {ref!r} (expected node/<id>, way/<id> or relation/<id>)"
        )
    return kind, int(num)


class OverpassClient:
    """Runs Overpass QL through a `Fetcher`, trying mirrors in order."""

    def __init__(self, fetcher: Fetcher, endpoints: Sequence[str] = OVERPASS_ENDPOINTS) -> None:
        if not endpoints:
            raise ValueError("at least one Overpass endpoint is required")
        self.fetcher = fetcher
        self.endpoints = tuple(endpoints)

    def query(self, ql: str) -> list[dict[str, Any]]:
        errors: list[str] = []
        for endpoint in self.endpoints:
            try:
                result = self.fetcher.get(f"{endpoint}?data={quote(ql)}")
            except FetchError as exc:
                log.warning("Overpass %s falló: %s", endpoint, exc)
                errors.append(f"{endpoint}: {exc}")
                continue
            if not result.ok:
                errors.append(f"{endpoint}: HTTP {result.status}")
                continue
            data = json.loads(result.text)
            remark = str(data.get("remark", ""))
            if "error" in remark.lower():
                # A cached partial answer must not be trusted: clear data/cache to retry.
                raise OverpassError(f"Overpass {endpoint}: {remark}")
            elements: list[dict[str, Any]] = data.get("elements", [])
            return elements
        raise OverpassError("todos los endpoints de Overpass fallaron: " + "; ".join(errors))

    def objects(self, refs: Iterable[str]) -> dict[str, OsmElement]:
        """Fetch nodes/ways/relations by id (ways and relations get their bbox center)."""
        ids: dict[str, list[int]] = {"node": [], "way": [], "relation": []}
        for ref in refs:
            kind, num = parse_ref(ref)
            ids[kind].append(num)
        parts = "".join(
            f"{'rel' if kind == 'relation' else kind}(id:{','.join(map(str, sorted(set(nums))))});"
            for kind, nums in ids.items()
            if nums
        )
        if not parts:
            return {}
        elements = self.query(f"[out:json][timeout:50];({parts});out center tags;")
        return {e.ref: e for e in map(to_element, elements) if e is not None}


def to_element(raw: Mapping[str, Any]) -> OsmElement | None:
    if "lat" in raw:
        lat, lon = raw["lat"], raw["lon"]
    elif "center" in raw:
        lat, lon = raw["center"]["lat"], raw["center"]["lon"]
    else:
        return None
    return OsmElement(f"{raw['type']}/{raw['id']}", float(lat), float(lon), raw.get("tags", {}))


def way_geometries(elements: Iterable[Mapping[str, Any]]) -> list[list[LatLon]]:
    """Way geometries from `out geom` (plain ways, or ways that are members of a relation)."""
    out: list[list[LatLon]] = []
    for e in elements:
        members = e.get("members", [e]) if e["type"] == "relation" else [e]
        for m in members:
            if (
                m.get("type") == "way"
                and m.get("geometry")
                and m.get("role", "") in ("", "forward")
            ):
                out.append([(float(p["lat"]), float(p["lon"])) for p in m["geometry"]])
    return out


@dataclass(frozen=True)
class RouteLine:
    """An ordered polyline with a km reference: km = km_offset + chainage / 1000."""

    id: str
    nombre: str
    coords: list[LatLon]
    km_offset: float
    fuente: str
    fuente_km: str
    km_residuo: float | None = None  # max |milestone km - fitted km|, when milestones exist

    @property
    def length_km(self) -> float:
        return line_length_m(self.coords) / 1000

    def km_at(self, point: LatLon) -> tuple[float, float]:
        """(km, distance to the line in metres) for the projection of `point`."""
        p = project(point, self.coords)
        return self.km_offset + p.chainage_m / 1000, p.distance_m


def fit_km_offset(
    coords: Sequence[LatLon], milestones: Iterable[OsmElement], max_dist_m: float = 50.0
) -> tuple[float, float, list[str]] | None:
    """Median of (milestone km - chainage) over milestones within `max_dist_m` of the line."""
    offsets: list[float] = []
    used: list[str] = []
    for m in milestones:
        try:
            km = float(m.tags.get("distance", ""))
        except ValueError:
            continue
        p = project(m.latlon, coords)
        if p.distance_m <= max_dist_m:
            offsets.append(km - p.chainage_m / 1000)
            used.append(m.ref)
    if not offsets:
        return None
    offset = statistics.median(offsets)
    return offset, max(abs(o - offset) for o in offsets), used


@dataclass(frozen=True)
class ContextPoint:
    tipo: str  # "estacion_tren_solar" | "litio"
    nombre: str
    element: OsmElement
    nota: str = ""


@dataclass
class GeoData:
    routes: dict[str, RouteLine]  # "RN9", "RN52", "tren_solar"
    context: list[ContextPoint]


class OverpassExporter:
    """Builds RN 9, RN 52 and the Volcán–Tilcara railway from OSM and writes GeoJSON."""

    def __init__(self, fetcher: Fetcher, endpoints: Sequence[str] = OVERPASS_ENDPOINTS) -> None:
        self.fetcher = fetcher
        self.client = OverpassClient(fetcher, endpoints)

    # ------------------------------------------------------------------ building
    def build(self) -> GeoData:
        milestones = [e for e in map(to_element, self.client.query(Q_MILESTONES)) if e]
        rn9 = self._rn9(milestones)
        rn52 = self._rn52(rn9)
        tren, stations = self._tren_solar()
        lithium = self.client.objects(ref for ref, _, _, _ in CONTEXT_OBJECTS)
        context = list(stations)
        for ref, tipo, nombre, nota in CONTEXT_OBJECTS:
            if ref not in lithium:
                raise OverpassError(f"objeto de contexto {ref} no encontrado en OSM")
            context.append(ContextPoint(tipo, nombre, lithium[ref], nota))
        return GeoData({"RN9": rn9, "RN52": rn52, "tren_solar": tren}, context)

    def _rn9(self, milestones: list[OsmElement]) -> RouteLine:
        segs = way_geometries(self.client.query(Q_RN9))
        if not segs:
            raise OverpassError("RN 9: Overpass no devolvió geometría")
        south = min((v for s in segs for v in s), key=lambda v: v[0])
        north = max((v for s in segs for v in s), key=lambda v: v[0])
        coords = stitch(segs, south, north, gap_m=300)
        fit = fit_km_offset(coords, milestones)
        if fit is None:
            raise OverpassError("RN 9: sin hitos kilométricos OSM sobre la traza")
        offset, residual, used = fit
        span = sorted(
            offset + project(m.latlon, coords).chainage_m / 1000
            for m in milestones
            if m.ref in used
        )
        return RouteLine(
            id="RN9",
            nombre="Ruta Nacional 9",
            coords=coords,
            km_offset=offset,
            fuente=f"OSM ways highway ref=RN9 en bbox {RN9_BBOX}",
            fuente_km=(
                f"OSM: distancia sobre la traza RN 9 calibrada con {len(used)} hitos "
                f"({', '.join(used)}; residuo máx. {residual:.1f} km). Los hitos están "
                f"entre km {span[0]:.0f} y {span[-1]:.0f}: más al norte el km es extrapolado "
                "sobre la geometría OSM y puede diferir de la progresiva oficial"
            ),
            km_residuo=residual,
        )

    def _rn52(self, rn9: RouteLine) -> RouteLine:
        segs = way_geometries(self.client.query(Q_RN52))
        if not segs:
            raise OverpassError("RN 52: Overpass no devolvió geometría")
        jama = self.client.objects([f"node/{PASO_DE_JAMA_NODE}"]).get(f"node/{PASO_DE_JAMA_NODE}")
        if jama is None:
            raise OverpassError("RN 52: nodo Paso de Jama no encontrado")
        ends = [v for s in segs for v in (s[0], s[-1])]
        junction = min(ends, key=lambda v: project(v, rn9.coords).distance_m)
        coords = stitch(segs, junction, jama.latlon, gap_m=300)
        return RouteLine(
            id="RN52",
            nombre="Ruta Nacional 52",
            coords=coords,
            km_offset=0.0,
            fuente=f"OSM relation/{RN52_RELATION} (Ruta Nacional 52)",
            fuente_km=(
                f"OSM: distancia sobre relation/{RN52_RELATION} desde el empalme con RN 9 "
                "(km 0 supuesto; sin hitos OSM ni progresiva oficial verificada)"
            ),
        )

    def _tren_solar(self) -> tuple[RouteLine, list[ContextPoint]]:
        segs = way_geometries(self.client.query(Q_TREN))
        nodes = [e for e in map(to_element, self.client.query(Q_TREN_NODES)) if e and e.name]
        by_name: dict[str, OsmElement] = {}
        for n in nodes:
            by_name.setdefault(n.name, n)
        if not segs or "Volcán" not in by_name or "Tilcara" not in by_name:
            raise OverpassError("Tren Solar: faltan vías o paradas Volcán/Tilcara en OSM")
        coords = stitch(segs, by_name["Volcán"].latlon, by_name["Tilcara"].latlon, gap_m=100)
        line = RouteLine(
            id="tren_solar",
            nombre="Tren Solar de la Quebrada: Volcán ↔ Tilcara",
            coords=coords,
            km_offset=0.0,
            fuente=f"OSM relation/{TREN_SOLAR_RELATION} (route=train)",
            fuente_km=f"OSM: distancia sobre relation/{TREN_SOLAR_RELATION} desde Volcán",
        )
        stations = sorted(by_name.values(), key=lambda n: line.km_at(n.latlon)[0])
        return line, [ContextPoint("estacion_tren_solar", n.name, n) for n in stations]

    # ------------------------------------------------------------------ export
    def export(self, out_dir: Path, points: Sequence[CriticalPoint] = ()) -> list[Path]:
        return write_geojson(self.build(), out_dir, points)


def _collection(features: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "type": "FeatureCollection",
        "attribution": ATTRIBUTION,
        "license": LICENSE,
        "copyright": COPYRIGHT_URL,
        "features": features,
    }


def _line_feature(line: RouteLine) -> dict[str, Any]:
    return {
        "type": "Feature",
        "properties": {
            "id": line.id,
            "nombre": line.nombre,
            "longitud_km": round(line.length_km, 2),
            "km_inicio": round(line.km_offset, 2),
            "km_fin": round(line.km_offset + line.length_km, 2),
            "fuente": line.fuente,
            "fuente_km": line.fuente_km,
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [[round(lon, 6), round(lat, 6)] for lat, lon in line.coords],
        },
    }


def _point_feature(lat: float, lon: float, props: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "type": "Feature",
        "properties": dict(props),
        "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
    }


def write_geojson(data: GeoData, out_dir: Path, points: Sequence[CriticalPoint] = ()) -> list[Path]:
    """rutas.geojson, ferrocarril.geojson, contexto.geojson (+ puntos.geojson if `points`)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tren = data.routes["tren_solar"]
    files: dict[str, dict[str, Any]] = {
        "rutas.geojson": _collection([_line_feature(data.routes[r]) for r in ("RN9", "RN52")]),
        "ferrocarril.geojson": _collection([_line_feature(tren)]),
        "contexto.geojson": _collection(
            [
                _point_feature(
                    c.element.lat,
                    c.element.lon,
                    {
                        "tipo": c.tipo,
                        "nombre": c.nombre,
                        "osm": c.element.ref,
                        "fuente": f"OSM {c.element.ref}",
                        "nota": c.nota,
                    },
                )
                for c in data.context
            ]
        ),
    }
    if points:
        files["puntos.geojson"] = _collection(
            [
                _point_feature(
                    p.lat,
                    p.lon,
                    {
                        "id": p.id,
                        "nombre": p.nombre,
                        "ruta": p.ruta,
                        "km": p.km,
                        "verificado": p.verificado,
                        "osm": p.osm,
                        "fuente_geo": p.fuente_geo,
                        "fuente_km": p.fuente_km,
                        "nota_geo": p.nota_geo,
                    },
                )
                for p in points
            ]
        )
    paths = []
    for name, payload in files.items():
        path = out_dir / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        paths.append(path)
    return paths
