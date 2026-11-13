"""Antecedent weather features: 24/48/72 h, 7 d, max hourly, snow (Child D).

Input is the hourly frame from `OpenMeteoClient.history` (local time). Windows end at the
last hour of each day (23:00–24:00), so a closure dated `fecha` sees the rain accumulated
up to the end of that day. Any missing hour inside a window makes that feature NaN:
gaps are never filled with zeros.
"""

from __future__ import annotations

from datetime import date

import pandas as pd

from corredor.models import WeatherDay

# feature column → (source column, window in hours, aggregation)
FEATURES: dict[str, tuple[str, int, str]] = {
    "lluvia_24h_mm": ("precipitacion_mm", 24, "sum"),
    "lluvia_48h_mm": ("precipitacion_mm", 48, "sum"),
    "lluvia_72h_mm": ("precipitacion_mm", 72, "sum"),
    "lluvia_7d_mm": ("precipitacion_mm", 7 * 24, "sum"),
    "lluvia_max_horaria_24h_mm": ("precipitacion_mm", 24, "max"),
    "lluvia_max_horaria_72h_mm": ("precipitacion_mm", 72, "max"),
    "nieve_24h_cm": ("nieve_cm", 24, "sum"),
    "nieve_72h_cm": ("nieve_cm", 72, "sum"),
    "nieve_7d_cm": ("nieve_cm", 7 * 24, "sum"),
}
FEATURE_COLUMNS = list(FEATURES)


def _regular_hourly(df: pd.DataFrame) -> pd.DataFrame:
    """Index by hour over full days, inserting NaN rows for missing hours."""
    if "time" not in df.columns:
        raise ValueError("hourly frame needs a 'time' column")
    frame = df.drop_duplicates("time", keep="last").set_index("time").sort_index()
    if frame.empty:
        return frame
    first = frame.index.min().normalize()
    last = frame.index.max().normalize() + pd.Timedelta(hours=23)
    return frame.reindex(pd.date_range(first, last, freq="h"))


def antecedent_features(df: pd.DataFrame) -> pd.DataFrame:
    """Hourly (time, precipitacion_mm, nieve_cm) → one row per day with FEATURE_COLUMNS.

    If `punto_id` is present the features are computed per point.
    """
    if "punto_id" in df.columns:
        parts = [
            antecedent_features(group.drop(columns="punto_id")).assign(punto_id=pid)
            for pid, group in df.groupby("punto_id", sort=True)
        ]
        if not parts:
            return pd.DataFrame(columns=["punto_id", "fecha", *FEATURE_COLUMNS])
        out = pd.concat(parts, ignore_index=True)
        return out[["punto_id", "fecha", *FEATURE_COLUMNS]]
    hourly = _regular_hourly(df)
    if hourly.empty:
        return pd.DataFrame(columns=["fecha", *FEATURE_COLUMNS])
    computed = {}
    for name, (column, window, how) in FEATURES.items():
        rolling = hourly[column].rolling(window, min_periods=window)
        computed[name] = rolling.sum() if how == "sum" else rolling.max()
    frame = pd.DataFrame(computed, index=hourly.index)
    end_of_day = frame[pd.DatetimeIndex(frame.index).hour == 23]
    out = end_of_day.reset_index(names="time")
    out.insert(0, "fecha", out.pop("time").dt.date)
    return out


def daily_weather(df: pd.DataFrame, punto_id: str) -> list[WeatherDay]:
    """Hourly frame → `clima_diario` rows; a day with any missing hour gets None values."""
    hourly = _regular_hourly(df)
    if hourly.empty:
        return []
    by_day = hourly.groupby(pd.DatetimeIndex(hourly.index).date)
    complete = by_day.count().eq(24)
    precip = by_day["precipitacion_mm"].sum().where(complete["precipitacion_mm"])
    snow = by_day["nieve_cm"].sum().where(complete["nieve_cm"])
    tmax = by_day["temp_c"].max().where(complete["temp_c"])
    tmin = by_day["temp_c"].min().where(complete["temp_c"])
    pmax = by_day["precipitacion_mm"].max().where(complete["precipitacion_mm"])

    def value(series: pd.Series, day: date) -> float | None:
        v = series.loc[day]
        return None if pd.isna(v) else round(float(v), 2)

    return [
        WeatherDay(
            punto_id=punto_id,
            fecha=day,
            precipitacion_mm=value(precip, day),
            nieve_cm=value(snow, day),
            temp_max_c=value(tmax, day),
            temp_min_c=value(tmin, day),
            precip_max_horaria_mm=value(pmax, day),
        )
        for day in precip.index
    ]
