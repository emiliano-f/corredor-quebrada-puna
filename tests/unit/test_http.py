from pathlib import Path

import httpx
import pytest
import respx

from corredor.http import (
    DisallowedByRobots,
    FetchError,
    PoliteFetcher,
    RetryableStatusError,
    RobotsRules,
)

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


@pytest.mark.parametrize(
    ("robots", "path", "allowed"),
    [
        ("User-agent: *\nAllow: /\nDisallow: /privado\n", "/privado/x", False),
        ("User-agent: *\nAllow: /\nDisallow: /privado\n", "/publico", True),
        ("User-agent: *\nDisallow: /a\nAllow: /a/b\n", "/a/b/c", True),
        ("User-agent: *\nDisallow: /*.pdf$\n", "/doc.pdf", False),
        ("User-agent: *\nDisallow: /*.pdf$\n", "/doc.pdf.html", True),
        ("User-agent: *\nDisallow: /*?s=\n", "/buscar?s=ruta", False),
        ("User-agent: *\nDisallow: /\n", "/robots.txt", True),
        ("User-agent: other\nDisallow: /\n", "/x", True),
        ("User-agent: *\nDisallow: /\n\nUser-agent: corredor-test\nAllow: /\n", "/x", True),
        ("User-agent: *\nDisallow:\n", "/x", True),
        ("User-agent: *\nDisallow: /privado\n", "/%70rivado", False),
        ("User-agent: *\nDisallow: /private\nAllow: /%70%72%69\n", "/private", False),
        ("User-agent: *\nDisallow: /%C3%B1u\n", "/ñu", False),
    ],
)
def test_robots_rules_rfc9309(robots: str, path: str, allowed: bool) -> None:
    assert RobotsRules(robots, UA).can_fetch(f"{BASE}{path}") is allowed


def test_robots_crawl_delay_per_group() -> None:
    rules = RobotsRules("User-agent: a\nCrawl-delay: 30\n\nUser-agent: *\nCrawl-delay: 10\n", UA)
    assert rules.crawl_delay == 10


@respx.mock
def test_redirect_to_disallowed_path_raises(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(200, text="User-agent: *\nDisallow: /privado\n")
    respx.get(f"{BASE}/a").respond(301, headers={"Location": "/privado/a"})
    target = respx.get(f"{BASE}/privado/a").respond(200, text="no")
    with pytest.raises(DisallowedByRobots):
        make(tmp_path, clock).get(f"{BASE}/a")
    assert target.call_count == 0


@respx.mock
def test_redirect_hops_are_throttled(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    respx.get(f"{BASE}/a").respond(302, headers={"Location": f"{BASE}/b"})
    respx.get(f"{BASE}/b").respond(200, text="ok")
    f = make(tmp_path, clock, min_interval_s=2.5)
    assert f.get(f"{BASE}/a").text == "ok"
    assert clock.sleeps.count(2.5) == 2


@respx.mock
def test_retry_after_above_cap_fails_instead_of_retrying_early(
    tmp_path: Path, clock: FakeClock
) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    route = respx.get(f"{BASE}/x").respond(429, headers={"Retry-After": "900"})
    with pytest.raises(FetchError, match="900"):
        make(tmp_path, clock, retries=3).get(f"{BASE}/x")
    assert route.call_count == 1


@respx.mock
def test_robots_redirect_is_followed(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(
        301, headers={"Location": "https://www.news.example/robots.txt"}
    )
    respx.get("https://www.news.example/robots.txt").respond(
        200, text="User-agent: *\nDisallow: /privado\n"
    )
    respx.get(f"{BASE}/x").respond(200, text="ok")
    f = make(tmp_path, clock)
    assert f.get(f"{BASE}/x").ok
    with pytest.raises(DisallowedByRobots):
        f.get(f"{BASE}/privado/y")


@respx.mock
def test_304_without_location_is_returned(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)
    respx.get(f"{BASE}/x").respond(304)
    assert make(tmp_path, clock).get(f"{BASE}/x").status == 304


@respx.mock
def test_robots_redirect_uses_known_crawl_delay(tmp_path: Path, clock: FakeClock) -> None:
    other = "https://cdn.example"
    respx.get(f"{other}/robots.txt").respond(200, text="User-agent: *\nCrawl-delay: 10\n")
    respx.get(f"{other}/page").respond(200, text="ok")
    respx.get(f"{BASE}/robots.txt").respond(301, headers={"Location": f"{other}/robots.txt"})
    respx.get(f"{BASE}/x").respond(200, text="ok")
    f = make(tmp_path, clock)
    f.get(f"{other}/page")
    clock.sleeps.clear()
    f.get(f"{BASE}/x")
    assert clock.sleeps[0] == pytest.approx(10)


EXEMPT = "https://api.exempt.example"


@respx.mock
def test_exempt_host_skips_only_robots(tmp_path: Path, clock: FakeClock) -> None:
    robots = respx.get(f"{EXEMPT}/robots.txt").respond(200, text="User-agent: *\nDisallow: /\n")
    route = respx.get(url__regex=rf"{EXEMPT}/v1/\w+").respond(200, text="{}")
    f = make(tmp_path, clock, robots_exempt_hosts=["api.exempt.example"])
    assert f.allowed(f"{EXEMPT}/v1/a")
    f.get(f"{EXEMPT}/v1/a")
    f.get(f"{EXEMPT}/v1/b")
    assert f.get(f"{EXEMPT}/v1/a").from_cache
    assert robots.call_count == 0
    assert route.call_count == 2
    assert route.calls[0].request.headers["User-Agent"] == UA
    assert clock.sleeps[-1] == pytest.approx(2.5)


@respx.mock
def test_non_listed_host_still_blocked_by_robots(tmp_path: Path, clock: FakeClock) -> None:
    respx.get(f"{BASE}/robots.txt").respond(200, text="User-agent: *\nDisallow: /\n")
    respx.get("https://sub.api.exempt.example/robots.txt").respond(
        200, text="User-agent: *\nDisallow: /\n"
    )
    f = make(tmp_path, clock, robots_exempt_hosts=["api.exempt.example"])
    with pytest.raises(DisallowedByRobots):
        f.get(f"{BASE}/x")
    with pytest.raises(DisallowedByRobots):
        f.get("https://sub.api.exempt.example/v1/a")


@respx.mock
def test_exempt_host_still_retries_and_never_caches_5xx(tmp_path: Path, clock: FakeClock) -> None:
    route = respx.get(f"{EXEMPT}/v1/a").respond(503)
    f = make(tmp_path, clock, retries=1, robots_exempt_hosts=["api.exempt.example"])
    with pytest.raises(RetryableStatusError):
        f.get(f"{EXEMPT}/v1/a")
    assert route.call_count == 2


def test_exemption_logged_once_per_fetcher(
    tmp_path: Path, clock: FakeClock, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level("INFO", logger="corredor.http"):
        make(tmp_path, clock, robots_exempt_hosts=["b.example.org", "a.example.org"])
    assert [r.getMessage() for r in caplog.records] == [
        "robots.txt check skipped (ADR 0002) for: a.example.org, b.example.org"
    ]


@pytest.mark.parametrize(
    "host",
    [
        "*.open-meteo.com",
        "https://api.open-meteo.com",
        "api.open-meteo.com:443",
        "api",
        "API.x.com",
    ],
)
def test_exemption_requires_exact_hostname(tmp_path: Path, clock: FakeClock, host: str) -> None:
    with pytest.raises(ValueError, match="exact hostname"):
        make(tmp_path, clock, robots_exempt_hosts=[host])
