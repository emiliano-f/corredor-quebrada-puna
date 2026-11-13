import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

from corredor.geo.geometry import haversine_m, project, stitch
from corredor.geo.points import CriticalPointRegistry, verification_report
from corredor.geo.routes import (
    ATTRIBUTION,
    Q_MILESTONES,
    Q_RN9,
    Q_RN52,
    Q_TREN,
    Q_TREN_NODES,
    GeoData,
    OsmElement,
    OverpassClient,
    OverpassError,
    OverpassExporter,
    RouteLine,
    fit_km_offset,
    parse_ref,
    write_geojson,
)
from corredor.http import FetchError, FetchResult
from corredor.models import CriticalPoint

FIX = Path(__file__).resolve().parents[1] / "fixtures" / "geo"
ENDPOINT = "https://overpass.test/api/interpreter"

BY_QUERY = {
    Q_RN9: "overpass_rn9.json",
    Q_RN52: "overpass_rn52.json",
    Q_MILESTONES: "overpass_milestones.json",
    Q_TREN: "overpass_tren.json",
    Q_TREN_NODES: "overpass_tren_nodes.json",
}


def _result(url: str, body: bytes, status: int = 200) -> FetchResult:
    return FetchResult(url, status, body, {"content-type": "application/json"}, datetime.now(UTC))


class FixtureFetcher:
    """Answers Overpass queries from recorded, trimmed fixtures (no network)."""

    def __init__(self, fail_hosts: tuple[str, ...] = ()) -> None:
        self.fail_hosts = fail_hosts
        self.urls: list[str] = []

    def get(self, url: str) -> FetchResult:
        self.urls.append(url)
        parts = urlsplit(url)
        if parts.hostname in self.fail_hosts:
            raise FetchError(f"HTTP 504 for {url}")
        ql = parse_qs(parts.query)["data"][0]
        name = BY_QUERY.get(ql, "overpass_objects.json" if "out center tags" in ql else "")
        if not name:
            raise AssertionError(f"unexpected query {ql}")
        return _result(url, (FIX / name).read_bytes())


@pytest.fixture(scope="module")
def geodata() -> GeoData:
    return OverpassExporter(FixtureFetcher(), endpoints=[ENDPOINT]).build()


# ------------------------------------------------------------------ geometry
def test_haversine_one_degree_latitude() -> None:
    assert haversine_m((0.0, 0.0), (1.0, 0.0)) == pytest.approx(111_195, rel=1e-3)


def test_project_chainage_and_distance() -> None:
    line = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
    p = project((0.001, 1.5), line)
    assert p.chainage_m == pytest.approx(1.5 * 111_195, rel=1e-3)
    assert p.distance_m == pytest.approx(111, abs=2)
    with pytest.raises(ValueError, match="two vertices"):
        project((0, 0), [(0.0, 0.0)])


def test_stitch_orders_reversed_segments_and_bridges_gaps() -> None:
    a = [(0.0, 0.0), (0.0, 0.01)]
    b = [(0.0, 0.03), (0.0, 0.0201)]  # reversed; ~11 m gap to `c`
    c = [(0.0, 0.02), (0.0, 0.0101)]  # ~11 m gap to `a`
    line = stitch([a, b, c], start=(0.0, 0.0), end=(0.0, 0.03), gap_m=50)
    assert line[0] == (0.0, 0.0)
    assert line[-1] == (0.0, 0.03)
    assert [v[1] for v in line] == sorted(v[1] for v in line)
    with pytest.raises(ValueError, match="not connected"):
        stitch([a, [(1.0, 1.0), (1.0, 1.01)]], (0.0, 0.0), (1.0, 1.01), gap_m=50)


def test_stitch_does_not_bridge_inside_a_connected_way() -> None:
    hairpin = [(0.0, 0.0), (0.001, 0.0), (0.002, 0.0), (0.002, 0.0001), (0.0, 0.0001)]
    nxt = [(0.0, 0.0001), (0.0, 0.01)]  # ends ~11 m from the hairpin start
    line = stitch([hairpin, nxt], start=(0.0, 0.0), end=(0.0, 0.01), gap_m=50)
    assert line[:5] == hairpin


# ------------------------------------------------------------------ Overpass client
def test_parse_ref() -> None:
    assert parse_ref("way/297669793") == ("way", 297669793)
    with pytest.raises(ValueError, match="invalid OSM ref"):
        parse_ref("calle/1")


def test_client_falls_back_to_next_endpoint() -> None:
    fetcher = FixtureFetcher(fail_hosts=("down.test",))
    client = OverpassClient(fetcher, ["https://down.test/api/interpreter", ENDPOINT])
    assert client.query(Q_MILESTONES)
    assert [urlsplit(u).hostname for u in fetcher.urls] == ["down.test", "overpass.test"]


def test_client_raises_when_all_endpoints_fail() -> None:
    client = OverpassClient(FixtureFetcher(fail_hosts=("overpass.test",)), [ENDPOINT])
    with pytest.raises(OverpassError, match="todos los endpoints"):
        client.query(Q_MILESTONES)


class HtmlThenFixtureFetcher(FixtureFetcher):
    def get(self, url: str) -> FetchResult:
        if urlsplit(url).hostname == "html.test":
            self.urls.append(url)
            return _result(url, b"<html>busy</html>")
        return super().get(url)


def test_client_skips_endpoint_with_non_json_answer() -> None:
    fetcher = HtmlThenFixtureFetcher()
    client = OverpassClient(fetcher, ["https://html.test/api/interpreter", ENDPOINT])
    assert client.query(Q_MILESTONES)
    assert [urlsplit(u).hostname for u in fetcher.urls] == ["html.test", "overpass.test"]


class RemarkFetcher:
    def get(self, url: str) -> FetchResult:
        body = {"elements": [], "remark": "runtime error: Query timed out"}
        return _result(url, json.dumps(body).encode())


def test_client_rejects_overpass_error_remark() -> None:
    with pytest.raises(OverpassError, match="timed out"):
        OverpassClient(RemarkFetcher(), [ENDPOINT]).query(Q_MILESTONES)


def test_objects_query_groups_ids() -> None:
    fetcher = FixtureFetcher()
    found = OverpassClient(fetcher, [ENDPOINT]).objects(
        ["node/5112503888", "way/297669793", "relation/12345428"]
    )
    ql = parse_qs(urlsplit(fetcher.urls[0]).query)["data"][0]
    assert "node(id:5112503888);way(id:297669793);rel(id:12345428);" in ql
    assert found["way/297669793"].name == "Cuesta de Lipán"


# ------------------------------------------------------------------ routes
def test_rn9_km_calibrated_with_milestones(geodata: GeoData) -> None:
    rn9 = geodata.routes["RN9"]
    assert rn9.km_residuo is not None
    assert rn9.km_residuo < 1.0
    km, dist = rn9.km_at((-24.1595425, -65.3825085))  # milestone km 1699
    assert km == pytest.approx(1699, abs=1.0)
    assert dist < 50


def test_rn52_starts_at_rn9_junction(geodata: GeoData) -> None:
    rn52 = geodata.routes["RN52"]
    assert rn52.km_offset == 0
    assert geodata.routes["RN9"].km_at(rn52.coords[0])[1] < 50
    km, dist = rn52.km_at((-23.6991545, -65.6595493))  # Abra Potrerillos
    assert 30 < km < 45
    assert dist < 50


def test_tren_solar_stations_in_line_order(geodata: GeoData) -> None:
    names = [c.nombre for c in geodata.context if c.tipo == "estacion_tren_solar"]
    assert names[0] == "Volcán"
    assert names[-1] == "Tilcara"
    assert "Purmamarca" in names
    assert len(names) == 6
    assert geodata.routes["tren_solar"].length_km == pytest.approx(41.8, abs=1)
    litio = {c.nombre for c in geodata.context if c.tipo == "litio"}
    assert litio == {"Cauchari-Olaroz", "Salar de Olaroz"}


def test_fit_km_offset_ignores_far_and_untagged_milestones() -> None:
    line = [(0.0, 0.0), (0.0, 1.0)]
    ms = [
        OsmElement("node/1", 0.0, 0.5, {"distance": "100"}),
        OsmElement("node/2", 0.5, 0.5, {"distance": "999"}),  # 55 km away
        OsmElement("node/3", 0.0, 0.2, {"name": "km 5"}),
    ]
    fit = fit_km_offset(line, ms)
    assert fit is not None
    offset, residual, used = fit
    assert used == ["node/1"]
    assert residual == 0
    assert offset == pytest.approx(100 - 55.6, abs=0.1)
    assert fit_km_offset(line, ms[1:]) is None


def test_write_geojson_keeps_attribution_and_lonlat(geodata: GeoData, tmp_path: Path) -> None:
    point = _point("p", "node/5112503888")
    paths = write_geojson(geodata, tmp_path, [point])
    assert {p.name for p in paths} == {
        "rutas.geojson",
        "ferrocarril.geojson",
        "contexto.geojson",
        "puntos.geojson",
    }
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["type"] == "FeatureCollection"
        assert data["attribution"] == ATTRIBUTION
        assert "ODbL" in data["license"]
    pts = json.loads((tmp_path / "puntos.geojson").read_text(encoding="utf-8"))
    assert pts["features"][0]["geometry"]["coordinates"] == [point.lon, point.lat]


# ------------------------------------------------------------------ points
def _point(pid: str, osm: str, ruta: str = "RN52", **kw: object) -> CriticalPoint:
    return CriticalPoint.model_validate(
        {"id": pid, "nombre": pid, "ruta": ruta, "lat": -23.7, "lon": -65.5, "osm": osm, **kw}
    )


def _elements() -> dict[str, OsmElement]:
    return OverpassClient(FixtureFetcher(), [ENDPOINT]).objects(["node/1"])


def test_verify_sets_sources_from_osm(geodata: GeoData) -> None:
    reg = CriticalPointRegistry([_point("chalala", "node/5112503888")])
    (check,) = reg.verify(_elements(), geodata.routes)
    p = reg.get("chalala")
    assert p.verificado
    assert check.problemas == []
    assert (p.lat, p.lon) == (-23.734053, -65.516582)  # from OSM, not from config
    assert p.km == pytest.approx(5.8, abs=0.2)
    assert p.fuente_geo.startswith("OSM node/5112503888")
    assert "relation/1745344" in p.fuente_km


def test_verify_flags_relation_missing_and_far_points(geodata: GeoData) -> None:
    rn52: RouteLine = geodata.routes["RN52"]
    far = RouteLine("RN52", "x", [(-23.0, -65.0), (-23.0, -64.9)], 0, "f", "fk")
    reg = CriticalPointRegistry(
        [
            _point("salinas_rel", "relation/12345428"),
            _point("missing", "node/42"),
            _point("sin_osm", ""),
        ]
    )
    checks = {c.point.id: c for c in reg.verify(_elements(), {"RN52": rn52})}
    assert not reg.get("salinas_rel").verificado
    assert "relación OSM" in checks["salinas_rel"].problemas[0]
    assert "no encontrado" in reg.get("missing").nota_geo
    assert "sin objeto OSM" in reg.get("sin_osm").nota_geo
    reg2 = CriticalPointRegistry([_point("chalala", "node/5112503888")])
    (c,) = reg2.verify(_elements(), {"RN52": far})
    assert not c.point.verificado
    assert "de la traza" in c.problemas[0]


def test_verify_flags_wrong_route_order(geodata: GeoData) -> None:
    reg = CriticalPointRegistry(
        [_point("abra", "node/2795046332"), _point("chalala", "node/5112503888")]
    )
    checks = reg.verify(_elements(), geodata.routes)
    assert checks[1].order_problem
    assert not checks[0].order_problem
    report = verification_report(checks, [_point("abra", "node/2795046332")])
    assert "| chalala |" in report
    assert "**no**" in report
    assert "Puntos verificados: 2 de 2." in report


class StubGeocoder:
    def __init__(self, hit: tuple[float, float] | None) -> None:
        self.hit = hit

    def geocode(self, query: str) -> tuple[float, float] | None:
        return self.hit


def test_geocoder_fallback_is_never_verified(geodata: GeoData) -> None:
    reg = CriticalPointRegistry([_point("x", "")], geocoder=StubGeocoder((-23.1, -65.2)))
    (c,) = reg.verify({}, geodata.routes)
    assert (c.point.lat, c.point.lon) == (-23.1, -65.2)
    assert not c.point.verificado
    assert "Nominatim" in c.point.fuente_geo
    reg = CriticalPointRegistry([_point("y", "")], geocoder=StubGeocoder(None))
    (c,) = reg.verify({}, geodata.routes)
    assert (c.point.lat, c.point.lon) == (-23.7, -65.5)
    assert "sin resultado" in c.point.nota_geo


def test_report_cell_escapes_pipes_and_newlines() -> None:
    from corredor.geo.points import _md_cell

    assert _md_cell("a | b\nc") == "a \\| b c"
