"""Forecast → risk (issue #26).

The forecast comes from `clima.modelo_pronostico`, not from ERA5, so its values are turned
into a percentile of THE SAME model's climatology (Historical Forecast API, same point,
`clima.pronostico_historico_desde` → yesterday, same season) and only then compared with a
percentile threshold. A threshold in mm/cm is shown but marked not comparable.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Literal, Protocol

import numpy as np
import pandas as pd

from corredor.calibration.thresholds import percentile_of, season
from corredor.config import UmbralElegido
from corredor.models import CriticalPoint
from corredor.weather.features import FEATURES, _regular_hourly, antecedent_features

HORIZONTES: dict[str, int] = {"hoy": 0, "24h": 24, "72h": 72}
Estado = Literal["alerta", "sin_alerta", "no_comparable", "sin_datos", "pendiente"]


class ForecastClient(Protocol):
    def forecast(self, point: CriticalPoint, hours: int) -> pd.DataFrame: ...

    def historical_forecast(
        self, point: CriticalPoint, start: date, end: date, model: str
    ) -> pd.DataFrame: ...


def features_at(hourly: pd.DataFrame, times: Sequence[pd.Timestamp]) -> list[dict[str, float]]:
    """Feature values for windows ending at each hour in `times` (NaN if any hour is missing)."""
    reg = _regular_hourly(hourly[["time", "precipitacion_mm", "nieve_cm"]])
    rolled = {}
    for name, (column, window, how) in FEATURES.items():
        r = reg[column].rolling(window, min_periods=window)
        rolled[name] = r.sum() if how == "sum" else r.max()
    frame = pd.DataFrame(rolled, index=reg.index)
    out = []
    for t in times:
        row = frame.loc[t] if t in frame.index else pd.Series(np.nan, index=frame.columns)
        out.append({str(k): float(v) for k, v in row.to_dict().items()})
    return out


@dataclass
class Climatologia:
    """Daily antecedent features of the forecast model, by season, for one point."""

    por_estacion: dict[tuple[str, str], np.ndarray]
    desde: date | None
    hasta: date | None

    @classmethod
    def from_hourly(cls, hourly: pd.DataFrame) -> Climatologia:
        hourly = hourly.dropna(subset=["precipitacion_mm", "nieve_cm"], how="all")
        daily = antecedent_features(hourly[["time", "precipitacion_mm", "nieve_cm"]])
        groups: dict[tuple[str, str], np.ndarray] = {}
        if daily.empty:
            return cls(groups, None, None)
        seasons = [season(d.month) for d in daily["fecha"]]
        for feat in FEATURES:
            col = pd.Series(daily[feat].to_numpy(dtype=float), index=seasons)
            for s in sorted(set(seasons)):
                vals = col.loc[[x == s for x in seasons]].dropna().to_numpy()
                groups[(feat, s)] = np.sort(vals)
        return cls(groups, min(daily["fecha"]), max(daily["fecha"]))

    def percentil(self, feature: str, value: float, when: datetime) -> float | None:
        clim = self.por_estacion.get((feature, season(when.month)))
        if clim is None or clim.size == 0 or np.isnan(value):
            return None
        return float(percentile_of(clim, np.array([value]))[0])


@dataclass
class Evaluacion:
    grupo: str
    variable: str
    umbral: float
    unidad: str
    estado: Estado
    valor: float | None
    percentil: float | None


def _num(v: float | None, digits: int = 1) -> float | None:
    return None if v is None or np.isnan(v) else round(float(v), digits)


def evaluar(
    umbrales: Sequence[UmbralElegido], feats: dict[str, float], pcts: dict[str, float | None]
) -> list[Evaluacion]:
    out = []
    for u in umbrales:
        value = feats.get(u.base)
        raw = None if value is None or np.isnan(value) else float(value)
        pct = pcts.get(u.base)
        unidad = "percentil" if u.es_percentil else ("cm" if u.base.endswith("_cm") else "mm")
        estado: Estado
        if not u.es_percentil:
            estado = "no_comparable"
        elif raw is None or pct is None:
            estado = "sin_datos"
        else:  # same alarm rule as the calibration: >= threshold and a wet/snowy window
            estado = "alerta" if pct >= u.umbral and raw > 0 else "sin_alerta"
        out.append(Evaluacion(u.grupo, u.variable, u.umbral, unidad, estado, _num(raw), _num(pct)))
    return out


def estado_global(evals: Sequence[Evaluacion]) -> Estado:
    estados = {e.estado for e in evals}
    if not evals:
        return "pendiente"
    order: tuple[Estado, ...] = ("alerta", "sin_datos", "sin_alerta")
    for e in order:
        if e in estados:
            return e
    return "no_comparable"


@dataclass
class PronosticoPunto:
    punto_id: str
    horizontes: dict[str, dict[str, object]] = field(default_factory=dict)
    clima_desde: date | None = None
    clima_hasta: date | None = None
    error: str | None = None


def riesgo_punto(
    point: CriticalPoint,
    hourly: pd.DataFrame | None,
    clim: Climatologia | None,
    umbrales: Sequence[UmbralElegido],
    now_local: datetime,
    error: str | None = None,
) -> PronosticoPunto:
    """Risk per horizon (hoy = window ending now; 24h/72h = ending now + N hours)."""
    out = PronosticoPunto(point.id, error=error)
    if clim is not None:
        out.clima_desde, out.clima_hasta = clim.desde, clim.hasta
    base = pd.Timestamp(now_local).floor("h")
    times = [base + timedelta(hours=h) for h in HORIZONTES.values()]
    values = features_at(hourly, times) if hourly is not None and not hourly.empty else None
    for (name, _), t, i in zip(HORIZONTES.items(), times, range(len(times)), strict=True):
        feats = values[i] if values else {f: float("nan") for f in FEATURES}
        pcts = {
            f: (clim.percentil(f, v, t.to_pydatetime()) if clim is not None else None)
            for f, v in feats.items()
        }
        evals = evaluar(umbrales, feats, pcts)
        out.horizontes[name] = {
            "hasta": t.strftime("%Y-%m-%d %H:%M"),
            "estado": estado_global(evals),
            "variables": {
                f: {"valor": _num(feats[f]), "percentil": _num(pcts[f])} for f in FEATURES
            },
            "evaluaciones": [e.__dict__ for e in evals],
        }
    return out


def _motivo(exc: Exception) -> str:
    from corredor.weather.openmeteo import CallBudgetExceeded

    if isinstance(exc, CallBudgetExceeded):
        return "se alcanzó el tope diario de llamadas a Open-Meteo"
    return "no se pudo descargar (sin red o error de la API)"


def fetch_forecasts(
    client: ForecastClient,
    points: Sequence[CriticalPoint],
    umbrales: Sequence[UmbralElegido],
    *,
    model: str,
    hours: int,
    clim_start: date,
    now_local: datetime,
) -> dict[str, PronosticoPunto]:
    """Forecast for every point first (cheap), then each point's model climatology.

    A failure (no network, daily call cap) leaves that part missing; never a made-up value.
    """
    from corredor.http import FetchError
    from corredor.weather.openmeteo import CallBudgetExceeded, OpenMeteoError

    errors = (FetchError, OpenMeteoError, CallBudgetExceeded, OSError, ValueError)
    hourly: dict[str, pd.DataFrame | None] = {}
    notes: dict[str, list[str]] = {p.id: [] for p in points}
    for p in points:
        try:
            hourly[p.id] = client.forecast(p, hours)
        except errors as exc:
            hourly[p.id] = None
            notes[p.id].append(f"Pronóstico: {_motivo(exc)}.")
    clim_end = now_local.date() - timedelta(days=1)
    out = {}
    for p in points:
        clim = None
        try:
            clim = Climatologia.from_hourly(
                client.historical_forecast(p, clim_start, clim_end, model)
            )
        except errors as exc:
            notes[p.id].append(f"Climatología del modelo de pronóstico: {_motivo(exc)}.")
        out[p.id] = riesgo_punto(
            p, hourly[p.id], clim, umbrales, now_local, " ".join(notes[p.id]) or None
        )
    return out
