from collections.abc import Callable
from pathlib import Path

import httpx
import pytest

from corredor.http import PoliteFetcher

UA = "corredor-test/0.1 (+https://example.org)"
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


class _FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def make_fetcher(tmp_path: Path) -> Callable[..., PoliteFetcher]:
    """PoliteFetcher with a fake clock (no real sleeps); HTTP is mocked with respx."""

    def factory(**kw: object) -> PoliteFetcher:
        clock = _FakeClock()
        return PoliteFetcher(
            UA,
            tmp_path / "cache",
            client=httpx.Client(),
            sleep=clock.sleep,
            clock=clock,
            wall_clock=clock,
            **kw,  # type: ignore[arg-type]
        )

    return factory
