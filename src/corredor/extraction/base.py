"""Abstract event extractor."""

from __future__ import annotations

from abc import ABC, abstractmethod

from corredor.models import Article, ClosureEvent


class EventExtractor(ABC):
    @abstractmethod
    def extract(self, article: Article) -> list[ClosureEvent]:
        """Closure events mentioned in one article's metadata (may be empty)."""
