"""El Tribuno de Jujuy: topic tag pages (`/ttag/<tag>/<n>`).

The site has no deep archive in its sitemaps (only the latest ~200 notes) and section
listings stop after a few pages, but tag pages go back years (`/ttag/ruta-52` reaches
2014). A page number past the end returns page 1 again, so paging stops as soon as a page
brings no new notes.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator
from datetime import date, datetime
from urllib.parse import urljoin, urlsplit

from selectolax.lexbor import LexborHTMLParser

from corredor.extraction import patterns
from corredor.models import Article
from corredor.sources.base import NewsSource
from corredor.sources.vialidadnacional import short

# /<seccion>/2019-11-27-1-0-0-trabajos-en-la-ruta-52 (also /nota/<same>)
_URL_DATE = re.compile(r"/(\d{4})-(\d{1,2})-(\d{1,2})-\d{1,2}-\d{1,2}-\d{1,2}-[^/]+$")


def note_key(url: str) -> str:
    """Last path segment: the same note is linked as /nota/… and /<seccion>/…."""
    return urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]


def url_date(url: str) -> date | None:
    m = _URL_DATE.search(urlsplit(url).path)
    if m is None:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


class ElTribunoSource(NewsSource):
    """Walks `params.tags`; keeps notes that mention the corridor (route or place).

    Tag pages shift as notes are added, so they are always re-fetched (`refresh=True`).
    """

    PARSER_VERSION = 1

    def tag_url(self, tag: str, page: int) -> str:
        base = f"{self.config.base_url.rstrip('/')}/ttag/{tag}"
        return base if page == 1 else f"{base}/{page}"

    def list_articles(self, since: date) -> Iterable[Article]:
        max_pages = int(self.config.params.get("max_paginas", 20))
        seen: set[str] = set()
        for tag in self.config.params.get("tags", []):
            tag_seen: set[str] = set()
            for page in range(1, max_pages + 1):
                result = self.fetcher.get(self.tag_url(tag, page), refresh=True)
                if not result.ok:
                    break
                items = list(self.parse_listing(result.text, result.url, result.fetched_at))
                new = [a for a in items if note_key(a.url) not in tag_seen]
                if not new:
                    break
                tag_seen.update(note_key(a.url) for a in new)
                for article in new:
                    key = note_key(article.url)
                    if key in seen or article.fecha < since:
                        continue
                    seen.add(key)
                    text = f"{article.titular} {article.bajada} {patterns.url_text(article.url)}"
                    if patterns.is_corridor(text):
                        yield article

    def parse_listing(self, html: str, page_url: str, fetched_at: datetime) -> Iterator[Article]:
        tree = LexborHTMLParser(html)
        for node in tree.css("article.nota"):
            link = node.css_first(".nota__titulo a") or node.css_first("a[aria-label]")
            if link is None:
                continue
            href = link.attributes.get("href")
            if not href:
                continue
            url = urljoin(page_url, href)
            fecha = url_date(url)
            title = link.text(strip=True) or (link.attributes.get("aria-label") or "")
            if fecha is None or not title.strip():
                continue
            lede_node = node.css_first(".nota__introduccion")
            yield Article(
                source_id=self.source_id,
                parser_version=self.PARSER_VERSION,
                url=url,
                fecha=fecha,
                fecha_fuente="fallback",
                titular=short(title),
                bajada=short(lede_node.text(strip=True)) if lede_node else "",
                fetched_at=fetched_at,
            )
