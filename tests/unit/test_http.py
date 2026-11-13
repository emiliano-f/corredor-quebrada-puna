from pathlib import Path

import httpx
import pytest
import respx

from corredor.http import DisallowedByRobots, FetchError, PoliteFetcher, RetryableStatusError

UA = "corredor-test/0.1 (+https://example.org)"
BASE = "https://news.example"


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


def make(tmp_path: Path, clock: FakeClock, **kw: object) -> PoliteFetcher:
    return PoliteFetcher(
        UA,
        tmp_path / "cache",
        client=httpx.Client(),
        sleep=clock.sleep,
        clock=clock,
        wall_clock=clock,
        **kw,  # type: ignore[arg-type]
    )


@respx.mock
def test_sends_user_agent_and_caches_2xx(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(200, text="User-agent: *\nDisallow: /privado\n")
    route = respx.get(f"{BASE}/a").respond(200, text="hola")
    f = make(tmp_path, clock)
    r1 = f.get(f"{BASE}/a")
    r2 = f.get(f"{BASE}/a")
    assert r1.text == "hola"
    assert not r1.from_cache
    assert r2.from_cache
    assert route.call_count == 1
    assert route.calls[0].request.headers["User-Agent"] == UA


@respx.mock
def test_robots_disallow_raises(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(200, text="User-agent: *\nDisallow: /privado\n")
    f = make(tmp_path, clock)
    with pytest.raises(DisallowedByRobots):
        f.get(f"{BASE}/privado/x")


@respx.mock
def test_robots_4xx_means_no_restrictions(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    respx.get(f"{BASE}/x").respond(200, text="ok")
    assert make(tmp_path, clock).get(f"{BASE}/x").ok


@pytest.mark.parametrize("status", [500, 503])
@respx.mock
def test_robots_5xx_means_disallow_all(tmp_path: Path, clock: FakeClock, status: int) -> None:
    respx.get(f"{BASE}/robots.txt").respond(status)
    with pytest.raises(DisallowedByRobots):
        make(tmp_path, clock).get(f"{BASE}/x")


@respx.mock
def test_robots_network_error_means_disallow_all(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").mock(side_effect=httpx.ConnectTimeout("t"))
    with pytest.raises(DisallowedByRobots):
        make(tmp_path, clock).get(f"{BASE}/x")


@respx.mock
def test_robots_html_counts_as_no_rules(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(
        200, text="<!DOCTYPE html><html>Disallow: /</html>", headers={"content-type": "text/html"}
    )
    respx.get(f"{BASE}/x").respond(200, text="ok")
    assert make(tmp_path, clock).get(f"{BASE}/x").ok


@respx.mock
def test_robots_cached_with_ttl(tmp_path: Path, clock: FakeClock) -> None:
    robots = respx.get(f"{BASE}/robots.txt").respond(200, text="User-agent: *\nAllow: /\n")
    respx.get(url__regex=rf"{BASE}/p\d").respond(200, text="ok")
    f = make(tmp_path, clock, robots_ttl_s=100)
    f.get(f"{BASE}/p1")
    f.get(f"{BASE}/p2")
    assert robots.call_count == 1
    clock.now += 101
    f.get(f"{BASE}/p3")
    assert robots.call_count == 2


@respx.mock
def test_crawl_delay_raises_interval(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(200, text="User-agent: *\nCrawl-delay: 10\n")
    respx.get(url__regex=rf"{BASE}/p\d").respond(200, text="ok")
    f = make(tmp_path, clock, min_interval_s=2.5)
    assert f.interval_for(f"{BASE}/p1") == 10
    f.get(f"{BASE}/p1")
    f.get(f"{BASE}/p2")
    assert clock.sleeps[-1] == pytest.approx(10)


def test_min_interval_floor(tmp_path: Path, clock: FakeClock) -> None:
    assert make(tmp_path, clock, min_interval_s=0.1).min_interval_s == 2.0


@respx.mock
def test_429_is_retried_with_retry_after_and_not_cached(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    route = respx.get(f"{BASE}/x")
    route.side_effect = [
        httpx.Response(429, headers={"Retry-After": "30"}),
        httpx.Response(200, text="ok"),
    ]
    f = make(tmp_path, clock, retries=2)
    assert f.get(f"{BASE}/x").text == "ok"
    assert 30 in [round(s) for s in clock.sleeps]


@respx.mock
def test_persistent_5xx_raises_and_is_not_cached(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    route = respx.get(f"{BASE}/x").respond(503)
    f = make(tmp_path, clock, retries=1)
    with pytest.raises(RetryableStatusError):
        f.get(f"{BASE}/x")
    assert route.call_count == 2
    route.respond(200, text="ok")
    assert f.get(f"{BASE}/x").text == "ok"


@respx.mock
def test_transport_error_becomes_fetch_error(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    respx.get(f"{BASE}/x").mock(side_effect=httpx.ConnectError("boom"))
    with pytest.raises(FetchError):
        make(tmp_path, clock, retries=1).get(f"{BASE}/x")


@respx.mock
def test_404_cached_with_short_ttl(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    route = respx.get(f"{BASE}/gone").respond(404)
    f = make(tmp_path, clock, not_found_ttl_s=60)
    assert f.get(f"{BASE}/gone").status == 404
    assert f.get(f"{BASE}/gone").from_cache
    clock.now += 61
    f.get(f"{BASE}/gone")
    assert route.call_count == 2


def test_tls_verification_is_on_by_default(tmp_path: Path, clock: FakeClock) -> None:
    f = PoliteFetcher(UA, tmp_path, sleep=clock.sleep, clock=clock)
    pool = f._client._transport._pool  # type: ignore[attr-defined]
    assert pool._ssl_context.verify_mode.name == "CERT_REQUIRED"
    f.close()


def test_rejects_empty_user_agent(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="user_agent"):
        PoliteFetcher(" ", tmp_path)
