"""Threshold calibration: one rule per weather cause, time split (integration step)."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

import pandas as pd

from corredor.models import ClosureEvent, ValidationResult


class ThresholdCalibrator:
    def __init__(self, train_end: date = date(2022, 12, 31)) -> None:
        self.train_end = train_end

    def candidates(
        self, events: Sequence[ClosureEvent], features: pd.DataFrame
    ) -> list[ValidationResult]:
        raise NotImplementedError("ThresholdCalibrator: pendiente (integración)")
