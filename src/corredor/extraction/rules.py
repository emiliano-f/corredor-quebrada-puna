"""Rule-based extractor (integration step): route, km, known places, cause keywords."""

from __future__ import annotations

from collections.abc import Sequence

from corredor.extraction.base import EventExtractor
from corredor.models import Article, ClosureEvent, CriticalPoint


class RuleBasedExtractor(EventExtractor):
    def __init__(self, points: Sequence[CriticalPoint]) -> None:
        self.points = list(points)

    def extract(self, article: Article) -> list[ClosureEvent]:
        raise NotImplementedError("RuleBasedExtractor: pendiente (integración)")
