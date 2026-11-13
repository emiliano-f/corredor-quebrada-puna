"""Weather clients (Open-Meteo archive + forecast, cached to Parquet: Child D)."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Protocol

import pandas as pd

from corredor.models import CriticalPoint


class WeatherClient(Protocol):
    def history(self, point: CriticalPoint, start: date, end: date) -> pd.DataFrame: ...

    def forecast(self, point: CriticalPoint, hours: int) -> pd.DataFrame: ...


class OpenMeteoClient:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir

    def history(self, point: CriticalPoint, start: date, end: date) -> pd.DataFrame:
        raise NotImplementedError("OpenMeteoClient.history: pendiente (hija D)")

    def forecast(self, point: CriticalPoint, hours: int) -> pd.DataFrame:
        raise NotImplementedError("OpenMeteoClient.forecast: pendiente (hija D)")
