"""Abstract news source. Every source is built from (SourceConfig, Fetcher)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import date
from typing import ClassVar

from corredor.http import Fetcher
from corredor.models import Article, SourceConfig


class NewsSource(ABC):
    """Lists article METADATA (url, date, headline, short lede) since a date.

    PARSER_VERSION is bumped whenever the parsing logic of the class changes; every
    Article row stores it together with the source id.
    """

    PARSER_VERSION: ClassVar[int] = 1

    def __init__(self, config: SourceConfig, fetcher: Fetcher) -> None:
        self.config = config
        self.fetcher = fetcher

    @property
    def source_id(self) -> str:
        return self.config.id

    @abstractmethod
    def list_articles(self, since: date) -> Iterable[Article]:
        """Yield articles published on or after `since` (metadata only)."""
