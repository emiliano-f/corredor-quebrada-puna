"""Config-driven generic sources (implemented by Child A, feature/generic-sources).

New outlets that fit one of these classes are added in config.yaml, not in code.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date

from corredor.http import Fetcher
from corredor.models import Article, MetodoFuente, SourceConfig
from corredor.sources.base import NewsSource


class WordPressApiSource(NewsSource):
    """/wp-json/wp/v2/posts?search=<term>&after=&before=, by yearly date windows."""

    def list_articles(self, since: date) -> Iterable[Article]:
        raise NotImplementedError("WordPressApiSource: pendiente (hija A)")


class SitemapSource(NewsSource):
    """Monthly sitemap → slug filter (patterns.slug_level) → article page metadata."""

    def list_articles(self, since: date) -> Iterable[Article]:
        raise NotImplementedError("SitemapSource: pendiente (hija A)")


class RssSource(NewsSource):
    def list_articles(self, since: date) -> Iterable[Article]:
        raise NotImplementedError("RssSource: pendiente (hija A)")


GENERIC_CLASSES: dict[MetodoFuente, type[NewsSource]] = {
    "wordpress_api": WordPressApiSource,
    "sitemap": SitemapSource,
    "rss": RssSource,
}

# Custom parsers register here by source id (Child B): {"eltribunojujuy": ElTribunoSource}
CUSTOM_CLASSES: dict[str, type[NewsSource]] = {}


class UnknownSourceError(LookupError):
    pass


def build_sources(configs: Iterable[SourceConfig], fetcher: Fetcher) -> list[NewsSource]:
    """Instantiate every enabled news source (snapshot collectors are not news sources)."""
    built: list[NewsSource] = []
    for cfg in configs:
        if not cfg.enabled or cfg.metodo == "snapshot":
            continue
        if cfg.metodo == "custom":
            cls = CUSTOM_CLASSES.get(cfg.id)
        else:
            cls = GENERIC_CLASSES.get(cfg.metodo)
        if cls is None:
            raise UnknownSourceError(f"no class for source {cfg.id!r} (metodo={cfg.metodo})")
        built.append(cls(cfg, fetcher))
    return built
