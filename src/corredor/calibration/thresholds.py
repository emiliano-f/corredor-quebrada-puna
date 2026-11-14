"""Threshold calibration: one rule per weather cause, same for every point, time split.

Weather causes only: aluvion and crecida are compared with rain features, nieve with snow
features. Every feature is offered in two forms (Emiliano picks the final rule):
  * absolute (mm / cm): candidates = quantiles of the feature on train event days;
  * per-cell seasonal percentile: the value's percentile within that point's own
    2016–2022 climatology for the same season (DJF/MAM/JJA/SON). Points in the same
    ERA5 cell share the series, so this is the per-cell percentile. It absorbs the
    per-cell ERA5 bias, so one percentile rule works for every point.
Fit on 2016-01-01..train_end, evaluated on the days after it (test). Day level, per point:
  * hit: an event at the point on day d with an alarm on d or d-1 (news can lag a day);
  * miss: an event without such an alarm (also when the weather is missing);
  * false alarm: an alarm day with no event at that point on d or d+1.
An alarm needs feature >= threshold and a raw value > 0 (a dry day is never an alarm).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, timedelta
from typing import Final, Literal

import numpy as np
import pandas as pd

from corredor.models import Causa, ClosureEvent, Threshold, ValidationResult

RAIN: Final = (
    "lluvia_24h_mm",
    "lluvia_48h_mm",
    "lluvia_72h_mm",
    "lluvia_7d_mm",
    "lluvia_max_horaria_24h_mm",
    "lluvia_max_horaria_72h_mm",
)
SNOW: Final = ("nieve_24h_cm", "nieve_72h_cm", "nieve_7d_cm")
CAUSE_FEATURES: Final[dict[Causa, tuple[str, ...]]] = {
    "aluvion": RAIN,
    "crecida": RAIN,
    "nieve": SNOW,
}
Grupo = tuple[tuple[Causa, ...], tuple[str, ...]]
SEPARATE: Final[dict[str, Grupo]] = {c: ((c,), f) for c, f in CAUSE_FEATURES.items()}
# Variant: aluvion and crecida pooled into one rain cause.
MERGED: Final[dict[str, Grupo]] = {
    "lluvia": (("aluvion", "crecida"), RAIN),
    "nieve": (("nieve",), SNOW),
}
ABS_QUANTILES: Final = (0.1, 0.25, 0.5, 0.75)
PERCENTILES: Final = (80.0, 90.0, 95.0, 98.0, 99.0)
PCT_UNIT: Final = "percentil estacional"
PCT_SUFFIX: Final = "_pct"
Periodo = Literal["train", "test"]


def season(month: int) -> str:
    return ("DJF", "DJF", "MAM", "MAM", "MAM", "JJA", "JJA", "JJA", "SON", "SON", "SON", "DJF")[
        month - 1
    ]


def percentile_of(clim: np.ndarray, vals: np.ndarray) -> np.ndarray:
    """Mid-rank percentile (0–100) of each value within the sorted climatology; NaN stays NaN."""
    less = np.searchsorted(clim, vals, side="left")
    equal = np.searchsorted(clim, vals, side="right") - less
    pct = (less + 0.5 * equal) / clim.size * 100.0
    return np.where(np.isnan(vals), np.nan, pct)


def unit_of(feature: str) -> str:
    return "cm" if feature.endswith("_cm") else "mm"


class ThresholdCalibrator:
    def __init__(
        self,
        train_end: date = date(2022, 12, 31),
        clim_start: date = date(2016, 1, 1),
        groups: Mapping[str, Grupo] = SEPARATE,
    ) -> None:
        self.train_end = train_end
        self.clim_start = clim_start
        self.groups = dict(groups)

    def prepare(self, features: pd.DataFrame) -> pd.DataFrame:
        """Features + `<feature>_pct` (seasonal percentile in the point's train climatology)."""
        df = features.copy()
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
        df["estacion"] = [season(d.month) for d in df["fecha"]]
        clim_mask = (df["fecha"] >= self.clim_start) & (df["fecha"] <= self.train_end)
        for feature in sorted({f for fs in CAUSE_FEATURES.values() for f in fs}):
            if feature not in df.columns:
                continue
            out = pd.Series(np.nan, index=df.index)
            for idx in df.groupby(["punto_id", "estacion"]).groups.values():
                group = df.loc[idx, feature]
                clim = np.sort(group[clim_mask.loc[idx]].dropna().to_numpy())
                if clim.size == 0:
                    continue
                out.loc[idx] = percentile_of(clim, group.to_numpy(dtype=float))
            df[feature + PCT_SUFFIX] = out
        return df

    def _period(self, d: date) -> Periodo:
        return "train" if d <= self.train_end else "test"

    @staticmethod
    def _event_days(
        events: Sequence[ClosureEvent], causes: tuple[Causa, ...]
    ) -> set[tuple[str, date]]:
        return {(e.punto_id, e.fecha) for e in events if e.causa in causes and e.punto_id}

    def compare(self, events: Sequence[ClosureEvent], features: pd.DataFrame) -> pd.DataFrame:
        """Train medians on event vs non-event days (same points and seasons as the events)."""
        df = self.prepare(features)
        train = df[(df["fecha"] >= self.clim_start) & (df["fecha"] <= self.train_end)]
        rows = []
        for causa, (causes, feats) in self.groups.items():
            days = {k for k in self._event_days(events, causes) if self._period(k[1]) == "train"}
            if not days:
                continue
            keys = list(zip(train["punto_id"], train["fecha"], strict=True))
            is_event = pd.Series([k in days for k in keys], index=train.index)
            ctx = {(pid, season(d.month)) for pid, d in days}
            in_ctx = pd.Series(
                [
                    (pid, s) in ctx
                    for pid, s in zip(train["punto_id"], train["estacion"], strict=True)
                ],
                index=train.index,
            )
            for feat in feats:
                if feat not in train.columns:
                    continue
                ev = train.loc[is_event, feat].dropna()
                non = train.loc[~is_event & in_ctx, feat].dropna()
                rows.append(
                    {
                        "causa": causa,
                        "variable": feat,
                        "dias_evento": len(ev),
                        "mediana_evento": float(ev.median()) if len(ev) else np.nan,
                        "mediana_sin_evento": float(non.median()) if len(non) else np.nan,
                        "pct_mediana_evento": float(
                            train.loc[is_event, feat + PCT_SUFFIX].dropna().median()
                        )
                        if len(ev)
                        else np.nan,
                    }
                )
        return pd.DataFrame(rows)

    def candidates(
        self, events: Sequence[ClosureEvent], features: pd.DataFrame
    ) -> list[ValidationResult]:
        df = self.prepare(features)
        df = df[df["fecha"] >= self.clim_start]
        results: list[ValidationResult] = []
        for causa, (causes, feats) in self.groups.items():
            days = self._event_days(events, causes)
            train_days = [k for k in days if self._period(k[1]) == "train"]
            if not train_days:
                continue
            for feat in feats:
                if feat not in df.columns:
                    continue
                indexed = df.set_index(["punto_id", "fecha"])
                on_event = indexed[feat].reindex(train_days).dropna()
                on_event = on_event[on_event > 0]
                absolute = (
                    sorted({round(float(on_event.quantile(q)), 1) for q in ABS_QUANTILES} - {0.0})
                    if len(on_event)
                    else []
                )
                for value in absolute:
                    th = Threshold(
                        causa=causes[0],
                        grupo=causa,
                        variable=feat,
                        umbral=value,
                        unidad=unit_of(feat),
                    )
                    results += self._evaluate(th, indexed, feat, feat, days)
                for value in PERCENTILES:
                    th = Threshold(
                        causa=causes[0],
                        grupo=causa,
                        variable=feat + PCT_SUFFIX,
                        umbral=value,
                        unidad=PCT_UNIT,
                    )
                    results += self._evaluate(th, indexed, feat + PCT_SUFFIX, feat, days)
        return results

    def _evaluate(
        self,
        th: Threshold,
        indexed: pd.DataFrame,
        column: str,
        raw: str,
        days: set[tuple[str, date]],
    ) -> list[ValidationResult]:
        alarm_mask = (indexed[column] >= th.umbral) & (indexed[raw] > 0)
        alarms = set(indexed.index[alarm_mask.fillna(False).to_numpy()])
        counts = {p: [0, 0, 0] for p in ("train", "test")}
        one = timedelta(days=1)
        for pid, d in days:
            hit = (pid, d) in alarms or (pid, d - one) in alarms
            counts[self._period(d)][0 if hit else 1] += 1
        for pid, d in alarms:
            if (pid, d) not in days and (pid, d + one) not in days:
                counts[self._period(d)][2] += 1
        return [
            ValidationResult(
                threshold=th, periodo=p, aciertos=c[0], fallos=c[1], falsas_alarmas=c[2]
            )
            for p, c in counts.items()
        ]
