from pathlib import Path

import pytest
import respx

from corredor.geo.points import NOMINATIM_URL, NominatimGeocoder
from corredor.http import DisallowedByRobots, PoliteFetcher

UA = "corredor-test/0.1 (+https://example.org)"
ROBOTS = "https://nominatim.openstreetmap.org/robots.txt"
# Shape of a Nominatim jsonv2 /search answer, trimmed; coordinates are OSM node/198429516.
HIT = [{"place_id": 1, "osm_type": "node", "osm_id": 198429516, "lat": "-23.5769014",
        "lon": "-65.393396", "display_name": "Tilcara, Jujuy, Argentina"}]  # fmt: skip


class Clock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, s: float) -> None:
        self.sleeps.append(s)
        self.now += s


def fetcher(tmp_path: Path, clock: Clock) -> PoliteFetcher:
    return PoliteFetcher(UA, tmp_path / "cache", sleep=clock.sleep, clock=clock, retries=0)


@respx.mock
def test_geocode_parses_caches_and_sends_user_agent(tmp_path: Path) -> None:
    clock = Clock()
    respx.get(ROBOTS).respond(200, text="User-agent: *\nDisallow: /reverse\n")
    route = respx.get(url__startswith=NOMINATIM_URL).respond(200, json=HIT)
    geo = NominatimGeocoder(fetcher(tmp_path, clock))
    assert geo.geocode("Tilcara, Jujuy, Argentina") == (-23.5769014, -65.393396)
    assert geo.geocode("Tilcara, Jujuy, Argentina") == (-23.5769014, -65.393396)
    assert route.call_count == 1
    assert route.calls[0].request.headers["User-Agent"] == UA
    assert "countrycodes=ar" in str(route.calls[0].request.url)
    # a new instance (next run) is served from the on-disk cache
    assert NominatimGeocoder(fetcher(tmp_path, clock)).geocode("Tilcara, Jujuy, Argentina")
    assert route.call_count == 1


@respx.mock
def test_geocode_waits_between_requests(tmp_path: Path) -> None:
    clock = Clock()
    respx.get(ROBOTS).respond(200, text="User-agent: *\nAllow: /\n")
    respx.get(url__startswith=NOMINATIM_URL).respond(200, json=[])
    geo = NominatimGeocoder(fetcher(tmp_path, clock))
    geo.geocode("a")
    geo.geocode("b")
    assert clock.sleeps
    assert min(clock.sleeps) >= 1.0


@respx.mock
def test_geocode_stops_when_robots_disallows_search(tmp_path: Path) -> None:
    respx.get(ROBOTS).respond(200, text="User-agent: *\nDisallow: /search\n")
    search = respx.get(url__startswith=NOMINATIM_URL).respond(200, json=HIT)
    with pytest.raises(DisallowedByRobots):
        NominatimGeocoder(fetcher(tmp_path, Clock())).geocode("Tilcara")
    assert search.call_count == 0
