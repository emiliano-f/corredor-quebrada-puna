"""Vialidad Nacional news: the national HTML listing, filtered to Jujuy / RN 9 / RN 52."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import date, datetime
from urllib.parse import urljoin

from selectolax.lexbor import LexborHTMLParser

from corredor.extraction import patterns
from corredor.models import Article
from corredor.sources.base import NewsSource

LEDE_MAX = 300


def short(text: str, limit: int = LEDE_MAX) -> str:
    """Collapse whitespace and cut to `limit` chars (metadata only, never the body)."""
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def is_jujuy_corridor(text: str) -> bool:
    """Jujuy or a corridor place, or RN 52 (entirely in Jujuy). RN 9 alone is not enough:
    it also crosses Córdoba, Santiago del Estero, Tucumán and Salta."""
    if "jujuy" in patterns.norm(text) or patterns.places(text):
        return True
    return "RN52" in patterns.routes(text)


class VialidadNacionalSource(NewsSource):
    """`{base_url}?page=N` (N from 0, 16 items per page, newest first, since 2018-10).

    Each item (`a.panel`) carries the URL, `<time datetime>`, `<h3>` headline and a short
    lede, so article pages are never fetched. `params.max_paginas` caps one run.
    """

    PARSER_VERSION = 1

    def page_url(self, page: int) -> str:
        return self.config.base_url if page == 0 else f"{self.config.base_url}?page={page}"

    def list_articles(self, since: date) -> Iterable[Article]:
        max_pages = int(self.config.params.get("max_paginas", 100))
        seen: set[str] = set()
        for page in range(max_pages):
            result = self.fetcher.get(self.page_url(page))
            if not result.ok:
                return
            items = list(self.parse_listing(result.text, result.url, result.fetched_at))
            new = [a for a in items if a.url not in seen]
            if not new:
                return
            seen.update(a.url for a in new)
            for article in new:
                if article.fecha >= since and is_jujuy_corridor(
                    f"{article.titular} {article.bajada}"
                ):
                    yield article
            if all(a.fecha < since for a in new):
                return

    def parse_listing(self, html: str, page_url: str, fetched_at: datetime) -> Iterator[Article]:
        tree = LexborHTMLParser(html)
        for node in tree.css("a.panel"):
            href = node.attributes.get("href")
            time = node.css_first("time")
            title = node.css_first("h3")
            if not href or "/noticias/" not in href or time is None or title is None:
                continue
            stamp = time.attributes.get("datetime") or ""
            try:
                fecha = date.fromisoformat(stamp[:10])
            except ValueError:
                continue
            lede = " ".join(p.text(strip=True) for p in node.css("p") if p.text(strip=True))
            yield Article(
                source_id=self.source_id,
                parser_version=self.PARSER_VERSION,
                url=urljoin(page_url, href),
                fecha=fecha,
                fecha_fuente="published_time",
                titular=short(title.text(strip=True)),
                bajada=short(lede),
                fetched_at=fetched_at,
            )
