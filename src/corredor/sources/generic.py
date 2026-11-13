"""Config-driven generic sources: WordPress REST API, monthly sitemaps and RSS feeds.

New outlets that fit one of these classes are added in config.yaml, not in code
(docs/SCRAPING.md). Every request goes through the injected Fetcher (PoliteFetcher in
production: robots.txt, Crawl-delay, rate limit, cache). Only metadata is kept: URL,
date, headline and a short lede; article bodies are never stored.
"""

from __future__ import annotations

import json
import re
import zlib
from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Any, ClassVar, Final
from urllib.parse import urlencode, urljoin, urlsplit

from selectolax.lexbor import LexborHTMLParser

from corredor.extraction import patterns
from corredor.http import DisallowedByRobots, Fetcher, FetchError, FetchResult
from corredor.models import Article, FechaFuente, FiltroSlug, MetodoFuente, SourceConfig
from corredor.sources.base import NewsSource
from corredor.sources.checkpoint import Checkpoint, CheckpointStatus

BAJADA_MAX_CHARS: Final = 300
MAX_DECOMPRESSED_BYTES: Final = 64 * 1024 * 1024
GZIP_MAGIC: Final = b"\x1f\x8b"


# --------------------------------------------------------------------------- helpers
def plain_text(fragment: str) -> str:
    """Untrusted HTML fragment → plain text (tags dropped, entities decoded, spaces collapsed).

    The result is stored as text; any HTML output must still escape it.
    """
    if "<" in fragment:
        tree = LexborHTMLParser(f"<body>{fragment}</body>")
        tree.strip_tags(["script", "style", "noscript", "template"])
        body = tree.body
        fragment = body.text(separator=" ") if body is not None else ""
    else:
        fragment = unescape(fragment)
    return re.sub(r"\s+", " ", fragment).strip()


def short_lede(text: str, max_chars: int = BAJADA_MAX_CHARS) -> str:
    """Keep only a short lede: at most `max_chars`, cut at a word boundary."""
    text = re.sub(r"\s*\[(?:…|&hellip;|\.\.\.)\]\s*$", "…", text.strip())
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0].rstrip(" ,;:.")
    return cut + "…"


def parse_iso_date(value: str | None) -> date | None:
    """ISO 8601 date/datetime → the calendar date as written (local date of the outlet)."""
    if not value:
        return None
    value = value.strip()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def decompress_if_gzip(content: bytes, limit: int = MAX_DECOMPRESSED_BYTES) -> bytes:
    """Gunzip `.xml.gz` payloads, refusing anything that inflates beyond `limit` bytes."""
    if not content.startswith(GZIP_MAGIC):
        return content
    inflater = zlib.decompressobj(16 + zlib.MAX_WBITS)
    out = inflater.decompress(content, limit)
    if inflater.unconsumed_tail:
        raise ValueError(f"decompressed payload exceeds {limit} bytes")
    if not inflater.eof:
        raise ValueError("truncated gzip payload")
    return out


def _xml_text(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<![CDATA[") and raw.endswith("]]>"):
        return raw[9:-3]
    return unescape(raw)


def _xml_blocks(xml: str, tag: str) -> list[str]:
    return re.findall(rf"<{tag}(?:\s[^>]*)?>(.*?)</{tag}>", xml, flags=re.S)


def _xml_field(block: str, tag: str) -> str | None:
    m = re.search(rf"<{re.escape(tag)}(?:\s[^>]*)?>(.*?)</{re.escape(tag)}>", block, flags=re.S)
    return _xml_text(m.group(1)) if m else None


def _same_site(url: str, base_url: str) -> bool:
    def host(u: str) -> str:
        netloc = urlsplit(u).netloc.lower()
        return netloc[4:] if netloc.startswith("www.") else netloc

    return urlsplit(url).scheme in ("http", "https") and host(url) == host(base_url)


# --------------------------------------------------------------------------- shared state
class RequestCapReached(Exception):  # noqa: N818 — control flow, not an error
    """The per-run request cap (backfill.max_requests_per_run) was reached."""


@dataclass
class CollectionStats:
    """What one run of a source did; printed by `corredor recolectar` and reported in PRs.

    raw: entries listed by the outlet (WP: sum of X-WP-Total over every search; sitemap:
    URLs in the monthly files; RSS: feed items). unique: distinct entries inspected.
    selected: articles yielded after the source filter (WP/RSS: patterns.is_candidate on
    headline + lede; sitemap: patterns.slug_level), by_level counts the sitemap levels.
    """

    requests: int = 0
    raw: int = 0
    unique: int = 0
    selected: int = 0
    by_level: Counter[str] = field(default_factory=Counter)
    pages_missing: int = 0
    offsite_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    units: dict[str, str] = field(default_factory=dict)
    capped: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "requests": self.requests,
            "raw": self.raw,
            "unique": self.unique,
            "selected": self.selected,
            "by_level": dict(self.by_level),
            "pages_missing": self.pages_missing,
            "offsite_skipped": self.offsite_skipped,
            "errors": self.errors,
            "units": self.units,
            "capped": self.capped,
        }


@dataclass(frozen=True)
class GenericOptions:
    """Run options shared by the generic sources (injected by build_sources)."""

    checkpoint_dir: Path | None = None
    max_requests: int | None = None
    sample_months: tuple[str, ...] | None = None
    today: date | None = None


class _GenericSource(NewsSource):
    def __init__(
        self, config: SourceConfig, fetcher: Fetcher, options: GenericOptions | None = None
    ) -> None:
        super().__init__(config, fetcher)
        self.options = options or GenericOptions()
        self.stats = CollectionStats()
        ckpt_dir = self.options.checkpoint_dir
        self.checkpoint = Checkpoint(ckpt_dir / f"{config.id}.json" if ckpt_dir else None)

    @property
    def today(self) -> date:
        return self.options.today or datetime.now(tz=UTC).date()

    def _start(self, since: date) -> date:
        desde = self.config.archivo_desde
        return max(since, desde) if desde else since

    def _get(self, url: str, *, refresh: bool = False) -> FetchResult:
        cap = self.options.max_requests
        if cap is not None and self.stats.requests >= cap:
            self.stats.capped = True
            raise RequestCapReached(url)
        result = self.fetcher.get(url, refresh=refresh)
        if not result.from_cache:
            self.stats.requests += 1
        return result

    def _error(self, message: str) -> None:
        self.stats.errors.append(message)

    def _skip(self, key: str, open_now: bool) -> bool:
        """Done units are skipped only if they were already closed when collected."""
        entry = self.checkpoint.get(key)
        return not open_now and self.checkpoint.is_done(key) and bool(entry and entry.get("closed"))

    def _refresh(self, key: str, open_now: bool) -> bool:
        """Bypass the HTTP cache for open units and for units last collected while open."""
        entry = self.checkpoint.get(key)
        return open_now or (entry is not None and not entry.get("closed", False))

    def _mark(self, key: str, status: CheckpointStatus, **info: Any) -> None:
        self.stats.units[key] = status
        self.checkpoint.mark(key, status, **info)

    def _article(
        self,
        *,
        url: str,
        fecha: date,
        fecha_fuente: FechaFuente,
        titular: str,
        bajada: str,
        fetched_at: datetime,
        filtro_slug: FiltroSlug | None = None,
    ) -> Article:
        self.stats.selected += 1
        if filtro_slug is not None:
            self.stats.by_level[filtro_slug] += 1
        return Article(
            source_id=self.source_id,
            parser_version=self.PARSER_VERSION,
            url=url,
            fecha=fecha,
            fecha_fuente=fecha_fuente,
            titular=titular,
            bajada=short_lede(bajada),
            fetched_at=fetched_at,
            filtro_slug=filtro_slug,
        )


# --------------------------------------------------------------------------- WordPress
class WordPressApiSource(_GenericSource):
    """`/wp-json/wp/v2/posts?search=<term>&after=&before=`, one window per calendar year.

    Searches only patterns.WP_SEARCH_TERMS (each with and without accents), merges the
    results by post id and keeps posts whose headline + excerpt pass
    patterns.is_candidate (word-boundary, accent-insensitive: 'alud' never hits 'salud').
    A year window is checkpointed once every term was paged through; the current year is
    always re-run. params: api_path (default /wp-json/wp/v2/posts), per_page (default 100).
    """

    PARSER_VERSION: ClassVar[int] = 1
    FIELDS: ClassVar[str] = "id,date,link,title,excerpt"

    def _api_url(self) -> str:
        path = str(self.config.params.get("api_path", "/wp-json/wp/v2/posts"))
        return urljoin(self.config.base_url.rstrip("/") + "/", path.lstrip("/"))

    def _windows(self, since: date) -> Iterator[tuple[str, date, date]]:
        start, end = self._start(since), self.today + timedelta(days=1)
        for year in range(start.year, self.today.year + 1):
            lo, hi = max(start, date(year, 1, 1)), min(end, date(year + 1, 1, 1))
            if lo < hi:
                yield str(year), lo, hi

    def list_articles(self, since: date) -> Iterable[Article]:
        try:
            for key, lo, hi in self._windows(since):
                open_now = hi > self.today
                if self._skip(key, open_now):
                    self.stats.units[key] = "skipped"
                    continue
                refresh = self._refresh(key, open_now)
                yield from self._window(key, lo, hi, refresh=refresh, closed=not open_now)
        except RequestCapReached:
            return

    def _window(
        self, key: str, lo: date, hi: date, *, refresh: bool, closed: bool
    ) -> Iterator[Article]:
        seen: set[int] = set()
        failed = False
        terms = self.config.params.get("terms", patterns.WP_SEARCH_TERMS)
        for term in terms:
            for variant in patterns.search_variants(str(term)):
                try:
                    yield from self._search(variant, lo, hi, seen, refresh=refresh)
                except FetchError as exc:
                    if isinstance(exc, DisallowedByRobots):
                        raise
                    failed = True
                    self._error(f"{key} {variant!r}: {exc}")
        self._mark(key, "error" if failed else "ok", closed=closed, posts=len(seen))

    def _search(
        self, term: str, lo: date, hi: date, seen: set[int], *, refresh: bool = False
    ) -> Iterator[Article]:
        per_page = int(self.config.params.get("per_page", 100))
        page = 1
        while True:
            query = {
                "search": term,
                "after": f"{lo - timedelta(days=1):%Y-%m-%d}T23:59:59",
                "before": f"{hi:%Y-%m-%d}T00:00:00",
                "per_page": per_page,
                "page": page,
                "orderby": "date",
                "order": "asc",
                "_fields": self.FIELDS,
            }
            result = self._get(f"{self._api_url()}?{urlencode(query)}", refresh=refresh)
            if result.status == 400 and page > 1:  # rest_post_invalid_page_number
                return
            if not result.ok:
                raise FetchError(f"HTTP {result.status} for {result.url}")
            posts = json.loads(result.content)
            if not isinstance(posts, list):
                raise FetchError(f"unexpected WP payload for {result.url}")
            if page == 1:
                self.stats.raw += int(result.headers.get("x-wp-total", len(posts)) or 0)
            for post in posts:
                article = self._post(post, seen, result.fetched_at)
                if article is not None:
                    yield article
            total_pages = int(result.headers.get("x-wp-totalpages", page) or page)
            if page >= total_pages or len(posts) < per_page:
                return
            page += 1

    def _post(self, post: Any, seen: set[int], fetched_at: datetime) -> Article | None:
        if not isinstance(post, dict) or not isinstance(post.get("id"), int):
            return None
        if post["id"] in seen:
            return None
        seen.add(post["id"])
        self.stats.unique += 1
        titular = plain_text(str((post.get("title") or {}).get("rendered", "")))
        bajada = plain_text(str((post.get("excerpt") or {}).get("rendered", "")))
        fecha = parse_iso_date(post.get("date"))
        link = str(post.get("link", ""))
        if fecha is None or not titular or not link.startswith(("http://", "https://")):
            return None
        if not patterns.is_candidate(f"{titular}. {bajada}"):
            return None
        return self._article(
            url=link,
            fecha=fecha,
            fecha_fuente="published_time",
            titular=titular,
            bajada=bajada,
            fetched_at=fetched_at,
        )


# --------------------------------------------------------------------------- sitemaps
@dataclass(frozen=True)
class SitemapEntry:
    loc: str
    lastmod: str | None = None
    news_date: str | None = None
    news_title: str | None = None


_URLSET_END: Final = re.compile(r"</(?:\w+:)?urlset\s*>|<(?:\w+:)?urlset\b[^>]*/>", re.I)


def parse_sitemap(xml: str) -> list[SitemapEntry]:
    """`<url>` entries of a sitemap (plain or Google News). Regex, no XML entity expansion."""
    entries = []
    for block in _xml_blocks(xml, "url"):
        loc = _xml_field(block, "loc")
        if not loc:
            continue
        entries.append(
            SitemapEntry(
                loc=loc.strip(),
                lastmod=_xml_field(block, "lastmod"),
                news_date=_xml_field(block, "news:publication_date"),
                news_title=_xml_field(block, "news:title"),
            )
        )
    return entries


@dataclass(frozen=True)
class PageMeta:
    titular: str = ""
    bajada: str = ""
    published: date | None = None


def _iter_ld(node: Any) -> Iterator[dict[str, Any]]:
    if isinstance(node, list):
        for item in node:
            yield from _iter_ld(item)
    elif isinstance(node, dict):
        yield node
        yield from _iter_ld(node.get("@graph"))


def parse_article_meta(html: str) -> PageMeta:
    """Headline, lede and publication date from an article page's <head> metadata.

    Date order: meta article:published_time → meta itemprop=datePublished → JSON-LD
    datePublished. Never reads the article body.
    """
    tree = LexborHTMLParser(html)
    metas: dict[str, str] = {}
    for node in tree.css("meta"):
        attrs = node.attributes
        key = attrs.get("property") or attrs.get("name") or attrs.get("itemprop")
        content = attrs.get("content")
        if key and content and content.strip() and key.lower() not in metas:
            metas[key.lower()] = content.strip()
    ld_date: date | None = None
    ld_headline = ""
    for script in tree.css('script[type="application/ld+json"]'):
        try:
            data = json.loads(script.text())
        except ValueError:
            continue
        for obj in _iter_ld(data):
            ld_date = ld_date or parse_iso_date(str(obj.get("datePublished") or "") or None)
            ld_headline = ld_headline or str(obj.get("headline") or "")
    published = (
        parse_iso_date(metas.get("article:published_time"))
        or parse_iso_date(metas.get("datepublished"))
        or ld_date
    )
    title_node = tree.css_first("title")
    titular = (
        metas.get("og:title")
        or metas.get("twitter:title")
        or ld_headline
        or (title_node.text() if title_node is not None else "")
    )
    bajada = metas.get("og:description") or metas.get("description") or ""
    bajada = bajada or metas.get("twitter:description", "")
    return PageMeta(titular=plain_text(titular), bajada=plain_text(bajada), published=published)


def _month_range(start: date, end: date) -> list[str]:
    months, y, m = [], start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return months


class SitemapSource(_GenericSource):
    """Monthly sitemap → slug filter C (patterns.slug_level) → article page <head> metadata.

    params.sitemap_mensual: URL template with {yyyymm} (also {yyyy} and {mm}). Months
    come from GenericOptions.sample_months when given, otherwise every month from
    max(since, archivo_desde) to today. Each month is checkpointed (ok | empty | missing |
    error); the current month is always re-run. URLs outside the outlet's site are skipped.
    """

    PARSER_VERSION: ClassVar[int] = 1

    def __init__(
        self, config: SourceConfig, fetcher: Fetcher, options: GenericOptions | None = None
    ) -> None:
        super().__init__(config, fetcher, options)
        template = config.params.get("sitemap_mensual")
        if not isinstance(template, str) or not any(t in template for t in ("{yyyymm}", "{yyyy}")):
            raise ValueError(f"{config.id}: params.sitemap_mensual with {{yyyymm}} is required")
        self.template = template
        self._seen: set[str] = set()

    def month_url(self, month: str) -> str:
        yyyy, mm = month.split("-")
        return self.template.format(yyyymm=yyyy + mm, yyyy=yyyy, mm=mm)

    def months(self, since: date) -> list[str]:
        start = self._start(since)
        if self.options.sample_months is not None:
            first = f"{start:%Y-%m}"
            for month in self.options.sample_months:
                if month < first:
                    self.stats.units[month] = "before_archive"
            return [m for m in self.options.sample_months if m >= first]
        return _month_range(start, self.today)

    def list_articles(self, since: date) -> Iterable[Article]:
        current = f"{self.today:%Y-%m}"
        try:
            for month in self.months(since):
                open_now = month >= current
                if self._skip(month, open_now):
                    self.stats.units[month] = "skipped"
                    continue
                refresh = self._refresh(month, open_now)
                yield from self._month(month, refresh=refresh, closed=not open_now)
        except RequestCapReached:
            return

    def _month(
        self, month: str, *, refresh: bool = False, closed: bool = True
    ) -> Iterator[Article]:
        url = self.month_url(month)
        try:
            result = self._get(url, refresh=refresh)
        except DisallowedByRobots:
            raise
        except FetchError as exc:
            self._error(f"{month}: {exc}")
            self._mark(month, "error", closed=closed, error=str(exc))
            return
        if result.status == 404:
            self._mark(month, "missing", closed=closed, http_status=404)
            return
        if not result.ok:
            self._error(f"{month}: HTTP {result.status}")
            self._mark(month, "error", closed=closed, http_status=result.status)
            return
        try:
            xml = decompress_if_gzip(result.content).decode("utf-8", errors="replace")
        except (ValueError, zlib.error) as exc:
            self._error(f"{month}: {exc}")
            self._mark(month, "error", closed=closed, error=str(exc))
            return
        if not _URLSET_END.search(xml):
            self._error(f"{month}: not a complete sitemap (no closing </urlset>)")
            self._mark(month, "error", closed=closed, error="incomplete sitemap")
            return
        entries = parse_sitemap(xml)
        self.stats.raw += len(entries)
        if not entries:
            self._mark(month, "empty", closed=closed, urls=0)
            return
        failed, selected = 0, 0
        for entry in entries:
            if entry.loc in self._seen:
                continue
            self._seen.add(entry.loc)
            self.stats.unique += 1
            if not _same_site(entry.loc, self.config.base_url):
                self.stats.offsite_skipped += 1
                continue
            level = patterns.slug_level(entry.loc)
            if level is None:
                continue
            article, ok = self._page(entry, level)
            failed += 0 if ok else 1
            if article is not None:
                selected += 1
                yield article
        status: CheckpointStatus = "error" if failed else "ok"
        self._mark(
            month, status, closed=closed, urls=len(entries), selected=selected, page_errors=failed
        )

    def _page(self, entry: SitemapEntry, level: FiltroSlug) -> tuple[Article | None, bool]:
        """Article metadata for one selected URL; (article, fetched_without_error)."""
        meta, fetched_at, ok = PageMeta(), datetime.now(tz=UTC), True
        try:
            result = self._get(entry.loc)
        except DisallowedByRobots:
            raise
        except FetchError as exc:
            self._error(f"{entry.loc}: {exc}")
            ok = False
        else:
            fetched_at = result.fetched_at
            if result.ok:
                meta = parse_article_meta(result.text)
            elif result.status in (404, 410):
                self.stats.pages_missing += 1
            else:
                self._error(f"{entry.loc}: HTTP {result.status}")
                ok = False
        titular = meta.titular or plain_text(entry.news_title or "")
        fecha_fuente: FechaFuente = "published_time"
        fecha = meta.published
        if fecha is None:
            fecha_fuente = "fallback"
            fecha = parse_iso_date(entry.news_date) or parse_iso_date(entry.lastmod)
        if fecha is None or not titular:
            return None, ok
        article = self._article(
            url=entry.loc,
            fecha=fecha,
            fecha_fuente=fecha_fuente,
            titular=titular,
            bajada=meta.bajada,
            fetched_at=fetched_at,
            filtro_slug=level,
        )
        return article, ok


# --------------------------------------------------------------------------- RSS
class RssSource(_GenericSource):
    """RSS 2.0 feed (params.feed_url, default <base_url>/feed/). Only recent items: a feed
    has no archive. Items pass patterns.is_candidate on title + description; items
    without a parseable pubDate are dropped (a date is never invented)."""

    PARSER_VERSION: ClassVar[int] = 1

    def feed_url(self) -> str:
        default = self.config.base_url.rstrip("/") + "/feed/"
        return str(self.config.params.get("feed_url", default))

    def list_articles(self, since: date) -> Iterable[Article]:
        try:
            result = self._get(self.feed_url(), refresh=True)
        except RequestCapReached:
            return
        if not result.ok:
            raise FetchError(f"HTTP {result.status} for {result.url}")
        for block in _xml_blocks(result.text, "item"):
            self.stats.raw += 1
            article = self._item(block, since, result.fetched_at)
            if article is not None:
                yield article

    def _item(self, block: str, since: date, fetched_at: datetime) -> Article | None:
        titular = plain_text(_xml_field(block, "title") or "")
        link = (_xml_field(block, "link") or "").strip()
        bajada = plain_text(_xml_field(block, "description") or "")
        fecha = _rfc822_date(_xml_field(block, "pubDate"))
        if not titular or not link.startswith(("http://", "https://")) or fecha is None:
            return None
        self.stats.unique += 1
        if fecha < since or not patterns.is_candidate(f"{titular}. {bajada}"):
            return None
        return self._article(
            url=link,
            fecha=fecha,
            fecha_fuente="published_time",
            titular=titular,
            bajada=bajada,
            fetched_at=fetched_at,
        )


def _rfc822_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value.strip()).date()
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------------- registry
GENERIC_CLASSES: dict[MetodoFuente, type[_GenericSource]] = {
    "wordpress_api": WordPressApiSource,
    "sitemap": SitemapSource,
    "rss": RssSource,
}

# Custom parsers register here by source id (Child B): {"eltribunojujuy": ElTribunoSource}
CUSTOM_CLASSES: dict[str, type[NewsSource]] = {}


class UnknownSourceError(LookupError):
    pass


def build_sources(
    configs: Iterable[SourceConfig],
    fetcher: Fetcher,
    options: GenericOptions | None = None,
    *,
    only: Sequence[str] | None = None,
) -> list[NewsSource]:
    """Instantiate every enabled news source (snapshot collectors are not news sources).

    `options` is passed to the generic classes; `only` restricts to those source ids.
    """
    built: list[NewsSource] = []
    for cfg in configs:
        if not cfg.enabled or cfg.metodo == "snapshot":
            continue
        if only is not None and cfg.id not in only:
            continue
        if cfg.metodo == "custom":
            custom = CUSTOM_CLASSES.get(cfg.id)
            if custom is None:
                raise UnknownSourceError(f"no class for source {cfg.id!r} (metodo=custom)")
            built.append(custom(cfg, fetcher))
            continue
        generic = GENERIC_CLASSES.get(cfg.metodo)
        if generic is None:
            raise UnknownSourceError(f"no class for source {cfg.id!r} (metodo={cfg.metodo})")
        built.append(generic(cfg, fetcher, options))
    return built
