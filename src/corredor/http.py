"""PoliteFetcher: the only way the pipeline talks to news sites and public APIs.

Rules (HANDOFF §7.3, AGENTS.md):
- identifies itself with a clear User-Agent;
- robots.txt per RFC 9309 (own matcher: longest match wins, `*` and `$` wildcards):
  2xx → apply rules; 4xx → no restrictions; 5xx, timeout or network error → assume
  everything is disallowed (retry later); an HTML body served as /robots.txt counts as
  "no rules". Cached per host for `robots_ttl_s`;
- per-host interval = max(min_interval_s, Crawl-delay), and never below 2 s; redirects
  are followed by hand (max 5), each hop checked against robots.txt and throttled;
- TLS verification always on (no option to disable it);
- `robots_exempt_hosts`: exact hostnames of documented public APIs whose robots.txt
  targets crawlers (ADR 0002). For those hosts ONLY the robots.txt check is skipped;
  rate limit, User-Agent, TLS, timeouts, retries and cache are unchanged;
- disk cache under data/: only 2xx (and 304) are cached; 404 is cached with a short TTL;
  429 and 5xx are retried with exponential backoff honouring Retry-After (a Retry-After
  above MAX_RETRY_AFTER_S fails instead of retrying early) and never cached.
"""

from __future__ import annotations

import email.utils
import hashlib
import json
import logging
import re
import time
from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol
from urllib.parse import unquote, urljoin, urlsplit

import httpx
from tenacity import (
    RetryCallState,
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

MIN_INTERVAL_FLOOR_S = 2.0
MAX_RETRY_AFTER_S = 600.0
MAX_REDIRECTS = 5
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})
_HOSTNAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$")

logger = logging.getLogger(__name__)


class FetchError(Exception):
    """A request could not be completed (after retries)."""


class DisallowedByRobots(FetchError):  # noqa: N818 — name fixed by the approved design
    """robots.txt forbids this URL, or robots.txt could not be read (RFC 9309 §2.3.1.4)."""


class RetryableStatusError(FetchError):
    def __init__(self, url: str, status: int, retry_after_s: float | None) -> None:
        super().__init__(f"HTTP {status} for {url}")
        self.status = status
        self.retry_after_s = retry_after_s


@dataclass(frozen=True)
class FetchResult:
    url: str
    status: int
    content: bytes
    headers: Mapping[str, str]
    fetched_at: datetime
    from_cache: bool = False

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    @property
    def text(self) -> str:
        return self.content.decode(_charset(self.headers), errors="replace")


class Fetcher(Protocol):
    """What sources depend on (lets tests inject a fake)."""

    def get(self, url: str, *, refresh: bool = False) -> FetchResult: ...


class RobotsRules:
    """robots.txt rules for one user agent, matched per RFC 9309.

    The group for our product token is used if present, otherwise the `*` group. The
    longest matching rule wins (Allow wins ties); `*` and a trailing `$` are supported.
    """

    def __init__(self, body: str, user_agent: str) -> None:
        token = user_agent.split("/")[0].strip().lower()
        groups: dict[str, list[tuple[bool, str]]] = {}
        delays: dict[str, float] = {}
        agents: list[str] = []
        in_rules = False
        for raw in body.splitlines():
            line = raw.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            key, value = (part.strip() for part in line.split(":", 1))
            key = key.lower()
            if key == "user-agent":
                if in_rules:
                    agents, in_rules = [], False
                agents.append(value.lower())
                groups.setdefault(value.lower(), [])
            elif key in ("allow", "disallow"):
                in_rules = True
                if value:
                    for agent in agents:
                        groups[agent].append((key == "allow", value))
            elif key == "crawl-delay":
                in_rules = True
                try:
                    delay = float(value)
                except ValueError:
                    continue
                for agent in agents:
                    delays[agent] = delay
        chosen = token if token in groups else "*"
        self.rules = [
            (allow, _robots_pattern(path), len(unquote(path)))
            for allow, path in groups.get(chosen, [])
        ]
        self.crawl_delay = delays.get(chosen)

    def can_fetch(self, url: str) -> bool:
        parts = urlsplit(url)
        target = unquote((parts.path or "/") + (f"?{parts.query}" if parts.query else ""))
        if target == "/robots.txt":
            return True
        best: tuple[int, bool] | None = None
        for allow, pattern, length in self.rules:
            if pattern.match(target) and (
                best is None or length > best[0] or (length == best[0] and allow)
            ):
                best = (length, allow)
        return True if best is None else best[1]


def _robots_pattern(path: str) -> re.Pattern[str]:
    anchored = path.endswith("$")
    body = path[:-1] if anchored else path
    regex = ".*".join(re.escape(unquote(chunk)) for chunk in body.split("*"))
    return re.compile(regex + ("$" if anchored else ""))


@dataclass
class _RobotsEntry:
    parser: RobotsRules | None  # None = no rules (allow all)
    disallow_all: bool
    expires_at: float


@dataclass
class _HostState:
    last_request_at: float | None = None
    robots: _RobotsEntry | None = None


class PoliteFetcher:
    def __init__(
        self,
        user_agent: str,
        cache_dir: Path,
        *,
        min_interval_s: float = 2.5,
        timeout_s: float = 30.0,
        retries: int = 3,
        robots_ttl_s: float = 24 * 3600,
        not_found_ttl_s: float = 3600,
        client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        wall_clock: Callable[[], float] = time.time,
        robots_exempt_hosts: Collection[str] = (),
    ) -> None:
        if not user_agent.strip():
            raise ValueError("user_agent is required")
        self.robots_exempt_hosts = frozenset(validate_hostname(h) for h in robots_exempt_hosts)
        if self.robots_exempt_hosts:
            logger.info(
                "robots.txt check skipped (ADR 0002) for: %s",
                ", ".join(sorted(self.robots_exempt_hosts)),
            )
        self.user_agent = user_agent
        self.cache_dir = cache_dir
        self.min_interval_s = max(min_interval_s, MIN_INTERVAL_FLOOR_S)
        self.retries = retries
        self.robots_ttl_s = robots_ttl_s
        self.not_found_ttl_s = not_found_ttl_s
        self._client = client or httpx.Client(timeout=timeout_s)
        self._client.headers["User-Agent"] = user_agent
        self._sleep = sleep
        self._clock = clock
        self._wall_clock = wall_clock
        self._hosts: dict[str, _HostState] = {}

    # ------------------------------------------------------------------ public API
    def get(self, url: str, *, refresh: bool = False) -> FetchResult:
        """GET `url` politely. Raises DisallowedByRobots or FetchError.

        `refresh=True` skips the cache read (live status endpoints) but still caches.
        """
        cached = None if refresh else self._cache_read(url)
        if cached is not None:
            return cached
        if not self.allowed(url):
            raise DisallowedByRobots(url)
        result = self._request_with_retries(url)
        self._cache_write(result)
        return result

    def is_robots_exempt(self, url: str) -> bool:
        return (urlsplit(url).hostname or "") in self.robots_exempt_hosts

    def allowed(self, url: str) -> bool:
        if self.is_robots_exempt(url):
            return True
        entry = self._robots_for(url)
        if entry.disallow_all:
            return False
        if entry.parser is None:
            return True
        return entry.parser.can_fetch(url)

    def interval_for(self, url: str) -> float:
        if self.is_robots_exempt(url):
            return self.min_interval_s
        entry = self._robots_for(url)
        delay: float = 0.0
        if entry.parser is not None and entry.parser.crawl_delay is not None:
            delay = entry.parser.crawl_delay
        return max(self.min_interval_s, delay)

    def _known_interval(self, url: str) -> float:
        """Like interval_for, but only from an already cached robots.txt (never fetches)."""
        state = self._hosts.get(_host_key(url))
        entry = state.robots if state is not None else None
        if entry is None or entry.parser is None or entry.parser.crawl_delay is None:
            return self.min_interval_s
        return max(self.min_interval_s, entry.parser.crawl_delay)

    def close(self) -> None:
        self._client.close()

    # ------------------------------------------------------------------ robots.txt
    def _robots_for(self, url: str) -> _RobotsEntry:
        host = _host_key(url)
        state = self._hosts.setdefault(host, _HostState())
        now = self._clock()
        if state.robots is not None and state.robots.expires_at > now:
            return state.robots
        state.robots = self._fetch_robots(host)
        return state.robots

    def _fetch_robots(self, host: str) -> _RobotsEntry:
        robots_url = f"{host}/robots.txt"
        self._throttle(host, self.min_interval_s)
        try:
            resp = self._client.get(robots_url, follow_redirects=False)
            # RFC 9309 §2.3.1.2: follow at least five consecutive redirects.
            for _ in range(MAX_REDIRECTS):
                if not resp.has_redirect_location:
                    break
                robots_url = urljoin(robots_url, resp.headers["location"])
                self._throttle(_host_key(robots_url), self._known_interval(robots_url))
                resp = self._client.get(robots_url, follow_redirects=False)
        except httpx.HTTPError:
            return self._robots_entry(None, disallow_all=True, ttl=self._robots_retry_ttl())
        if resp.has_redirect_location:
            return self._robots_entry(None, disallow_all=False)
        status = resp.status_code
        if 200 <= status < 300:
            body = resp.text
            if _looks_like_html(resp.headers.get("content-type", ""), body):
                return self._robots_entry(None, disallow_all=False)
            return self._robots_entry(RobotsRules(body, self.user_agent), disallow_all=False)
        if 400 <= status < 500:
            return self._robots_entry(None, disallow_all=False)
        return self._robots_entry(None, disallow_all=True, ttl=self._robots_retry_ttl())

    def _robots_entry(
        self, parser: RobotsRules | None, *, disallow_all: bool, ttl: float | None = None
    ) -> _RobotsEntry:
        return _RobotsEntry(
            parser=parser,
            disallow_all=disallow_all,
            expires_at=self._clock() + (self.robots_ttl_s if ttl is None else ttl),
        )

    def _robots_retry_ttl(self) -> float:
        return min(self.robots_ttl_s, 3600.0)

    # ------------------------------------------------------------------ requests
    def _request_with_retries(self, url: str) -> FetchResult:
        retrying = Retrying(
            stop=stop_after_attempt(self.retries + 1),
            wait=_RetryAfterWait(),
            retry=retry_if_exception_type((RetryableStatusError, httpx.TransportError)),
            sleep=self._sleep,
            reraise=True,
        )
        try:
            return retrying(self._request_once, url)
        except RetryableStatusError:
            raise
        except httpx.HTTPError as exc:
            raise FetchError(f"{type(exc).__name__} for {url}: {exc}") from exc

    def _request_once(self, url: str) -> FetchResult:
        target = url
        for _ in range(MAX_REDIRECTS + 1):
            self._throttle(_host_key(target), self.interval_for(target))
            resp = self._client.get(target, follow_redirects=False)
            if not resp.has_redirect_location:
                break
            target = urljoin(target, resp.headers["location"])
            if not self.allowed(target):
                raise DisallowedByRobots(f"{url} redirects to {target}")
        else:
            raise FetchError(f"too many redirects for {url}")
        if resp.status_code in RETRYABLE_STATUS:
            retry_after = _parse_retry_after(resp.headers.get("retry-after"))
            if retry_after is not None and retry_after > MAX_RETRY_AFTER_S:
                raise FetchError(
                    f"HTTP {resp.status_code} for {url}: server asks to wait {retry_after:.0f} s"
                )
            raise RetryableStatusError(url, resp.status_code, retry_after)
        return FetchResult(
            url=url,
            status=resp.status_code,
            content=resp.content,
            headers=dict(resp.headers),
            fetched_at=datetime.fromtimestamp(self._wall_clock(), tz=UTC),
        )

    def _throttle(self, host: str, interval: float) -> None:
        state = self._hosts.setdefault(host, _HostState())
        if state.last_request_at is not None:
            wait = state.last_request_at + interval - self._clock()
            if wait > 0:
                self._sleep(wait)
        state.last_request_at = self._clock()

    # ------------------------------------------------------------------ disk cache
    def _cache_paths(self, url: str) -> tuple[Path, Path]:
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        folder = self.cache_dir / urlsplit(url).netloc.replace(":", "_")
        return folder / f"{key}.body", folder / f"{key}.json"

    def _cache_read(self, url: str) -> FetchResult | None:
        body_path, meta_path = self._cache_paths(url)
        if not meta_path.exists() or not body_path.exists():
            return None
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        expires_at = meta.get("expires_at")
        if expires_at is not None and float(expires_at) <= self._wall_clock():
            return None
        return FetchResult(
            url=url,
            status=int(meta["status"]),
            content=body_path.read_bytes(),
            headers=meta.get("headers", {}),
            fetched_at=datetime.fromisoformat(meta["fetched_at"]),
            from_cache=True,
        )

    def _cache_write(self, result: FetchResult) -> None:
        if result.ok or result.status == 304:
            expires_at = None
        elif result.status == 404:
            expires_at = self._wall_clock() + self.not_found_ttl_s
        else:
            return
        body_path, meta_path = self._cache_paths(result.url)
        body_path.parent.mkdir(parents=True, exist_ok=True)
        body_path.write_bytes(result.content)
        meta = {
            "url": result.url,
            "status": result.status,
            "headers": {k: v for k, v in result.headers.items() if k.lower() != "set-cookie"},
            "fetched_at": result.fetched_at.isoformat(),
            "expires_at": expires_at,
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")


class _RetryAfterWait:
    """Exponential backoff, but never shorter than the server's Retry-After."""

    def __init__(self) -> None:
        self._exp = wait_exponential(multiplier=2, min=2, max=120)

    def __call__(self, retry_state: RetryCallState) -> float:
        base = float(self._exp(retry_state))
        outcome = retry_state.outcome
        exc = outcome.exception() if outcome is not None else None
        if isinstance(exc, RetryableStatusError) and exc.retry_after_s is not None:
            return max(base, exc.retry_after_s)
        return base


def validate_hostname(host: str) -> str:
    """An exact, lowercase hostname: no scheme, port, path or wildcard."""
    if not _HOSTNAME_RE.fullmatch(host):
        raise ValueError(f"exact hostname required (no scheme, port, path or wildcard): {host!r}")
    return host


def _host_key(url: str) -> str:
    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        raise ValueError(f"absolute URL required: {url!r}")
    return f"{parts.scheme}://{parts.netloc}"


def _looks_like_html(content_type: str, body: str) -> bool:
    if "html" in content_type.lower():
        return True
    head = body.lstrip()[:100].lower()
    return head.startswith(("<!doctype html", "<html"))


def _parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return float(value)
    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return max(0.0, (parsed - datetime.now(tz=UTC)).total_seconds())


def _charset(headers: Mapping[str, str]) -> str:
    for key, value in headers.items():
        if key.lower() == "content-type" and "charset=" in value:
            return value.split("charset=", 1)[1].split(";")[0].strip() or "utf-8"
    return "utf-8"
