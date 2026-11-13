"""Optional LLM extractor (integration step). Only used when LLM_API_KEY is set.

Article text is untrusted data: delimited in the prompt, no tools, and the output is
validated against ClosureEvent; invalid output is dropped and logged.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from corredor.extraction.base import EventExtractor
from corredor.models import Article, ClosureEvent


class LLMClient(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class LLMExtractor(EventExtractor):
    def __init__(self, client: LLMClient, cache_dir: Path) -> None:
        self.client = client
        self.cache_dir = cache_dir

    def extract(self, article: Article) -> list[ClosureEvent]:
        raise NotImplementedError("LLMExtractor: pendiente (integración)")
