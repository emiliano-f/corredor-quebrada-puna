"""Weather clients: Open-Meteo archive + forecast, cached to Parquet under data/.

Every request goes through the injected `Fetcher` (PoliteFetcher in production), so the
rate limit, User-Agent, TLS, retries and HTTP cache apply. The robots.txt check is
skipped only for the Open-Meteo API hosts listed in config.yaml (ADR 0002).

Free-tier terms (https://open-meteo.com/en/terms): non-commercial, < 600 calls/min,
5,000/h, 10,000/day, CC BY 4.0. Calls are counted with Open-Meteo's weighting (a request
for more than 2 weeks or more than 10 variables counts as several calls) in a per-day
ledger; `CallLedger.reserve` raises before a request would exceed the daily cap.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlencode

import pandas as pd

from corredor.config import ClimaConfig
from corredor.http import Fetcher, FetchResult
from corredor.models import CriticalPoint

# Open-Meteo hourly variable → our column name.
HOURLY_VARIABLES: dict[str, str] = {
    "precipitation": "precipitacion_mm",
    "snowfall": "nieve_cm",
    "temperature_2m": "temp_c",
}
WEATHER_COLUMNS = list(HOURLY_VARIABLES.values())
# Archive data near today is still being produced (ERA5 lags ~5 days): when the cache is
# extended, the last REFRESH_DAYS of the cached range are fetched again.
REFRESH_DAYS = 7
# A cached archive is reused for coordinates this close (one unit of the 5-decimal key).
SAME_POINT_DEG = 1.5e-5
FORECAST_PAST_HOURS = 7 * 24


class WeatherClient(Protocol):
    def history(self, point: CriticalPoint, start: date, end: date) -> pd.DataFrame: ...

    def forecast(self, point: CriticalPoint, hours: int) -> pd.DataFrame: ...


class OpenMeteoError(RuntimeError):
    """Open-Meteo answered with an error or an unexpected payload."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class CallBudgetExceeded(RuntimeError):  # noqa: N818 — reads better in the CLI message
    """The next request would exceed the configured daily call cap."""


def call_weight(n_variables: int, n_days: float, n_models: int = 1, n_locations: int = 1) -> float:
    """Open-Meteo's API-call weight (formula from open-meteo.com/en/pricing)."""
    variables_weight = n_variables * max(n_models, 1) / 10.0
    time_weight = n_days / 14.0
    return max(1.0, max(variables_weight, time_weight * variables_weight)) * n_locations


class CallLedger:
    """Weighted Open-Meteo calls per UTC day, persisted as JSON so every run counts."""

    def __init__(
        self,
        path: Path,
        max_per_day: float,
        today: Callable[[], date] = lambda: datetime.now(tz=UTC).date(),
    ) -> None:
        self.path = path
        self.max_per_day = max_per_day
        self._today = today

    def _load(self) -> dict[str, float]:
        if not self.path.exists():
            return {}
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return {str(k): float(v) for k, v in raw.items()}

    def _save(self, counts: dict[str, float]) -> None:
        keep = sorted(counts)[-7:]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({k: round(counts[k], 3) for k in keep}, indent=1), encoding="utf-8"
        )

    def used_today(self) -> float:
        return self._load().get(self._today().isoformat(), 0.0)

    def reserve(self, weight: float) -> None:
        counts = self._load()
        key = self._today().isoformat()
        used = counts.get(key, 0.0)
        if used + weight > self.max_per_day:
            raise CallBudgetExceeded(
                f"Open-Meteo: {used:.1f} + {weight:.1f} llamadas superaría el tope diario de "
                f"{self.max_per_day:.0f} (clima.max_llamadas_diarias)"
            )
        counts[key] = used + weight
        self._save(counts)

    def refund(self, weight: float) -> None:
        counts = self._load()
        key = self._today().isoformat()
        counts[key] = max(0.0, counts.get(key, 0.0) - weight)
        self._save(counts)


@dataclass(frozen=True)
class ResponseMeta:
    """Location metadata Open-Meteo returns with every response."""

    latitude: float
    longitude: float
    elevation: float | None
    utc_offset_seconds: int


@dataclass(frozen=True)
class GridCell:
    """The grid cell a point falls in for one model, and its elevation vs the point's."""

    punto_id: str
    modelo: str
    lat_grilla: float
    lon_grilla: float
    elev_grilla_m: float | None
    elev_punto_m: float | None

    @property
    def diferencia_m(self) -> float | None:
        if self.elev_grilla_m is None or self.elev_punto_m is None:
            return None
        return self.elev_grilla_m - self.elev_punto_m


class OpenMeteoClient:
    def __init__(
        self,
        fetcher: Fetcher,
        cache_dir: Path,
        config: ClimaConfig | None = None,
        *,
        ledger: CallLedger | None = None,
        now: Callable[[], datetime] = lambda: datetime.now(tz=UTC),
    ) -> None:
        self.fetcher = fetcher
        self.cache_dir = cache_dir
        self.config = config or ClimaConfig()
        self.ledger = ledger or CallLedger(
            cache_dir / "llamadas_openmeteo.json",
            self.config.max_llamadas_diarias,
            today=lambda: now().astimezone(UTC).date(),
        )
        self._now = now

    # ------------------------------------------------------------------ history
    def history(self, point: CriticalPoint, start: date, end: date) -> pd.DataFrame:
        """Hourly precipitation (mm), snowfall (cm) and 2 m temperature (°C), local time.

        One request for the whole range (split by year only if the API rejects it with a
        400); a cached range for the same (lat, lon, start) is
        reused and only its tail (last REFRESH_DAYS days) plus the missing days are fetched.
        """
        if end < start:
            raise ValueError("end before start")
        model = self.config.modelo_historico
        cached = self._find_cached(point, model, start, end)
        if cached is not None:
            frame, cached_end = cached
            if cached_end >= end:
                return _slice(frame, start, end)
            tail_start = max(start, cached_end - timedelta(days=REFRESH_DAYS))
            tail = self._fetch_archive(point, model, tail_start, end)
            merged = pd.concat([frame[frame["time"] < pd.Timestamp(tail_start)], tail])
            self._write_cache(point, model, start, end, merged)
            return _slice(merged, start, end)
        try:
            frame = self._fetch_archive(point, model, start, end)
        except OpenMeteoError as exc:
            if exc.status != 400 or start.year == end.year:
                raise
            frame = pd.concat(
                [
                    self._fetch_archive(
                        point, model, max(start, date(y, 1, 1)), min(end, date(y, 12, 31))
                    )
                    for y in range(start.year, end.year + 1)
                ],
                ignore_index=True,
            )
        self._write_cache(point, model, start, end, frame)
        return frame

    def _fetch_archive(
        self, point: CriticalPoint, model: str, start: date, end: date
    ) -> pd.DataFrame:
        params = self._archive_params(point, model, start, end, list(HOURLY_VARIABLES))
        n_days = (end - start).days + 1
        data, _ = self._get_json(self.config.archive_url, params, len(HOURLY_VARIABLES), n_days)
        return parse_hourly(data)

    def _archive_params(
        self,
        point: CriticalPoint,
        model: str,
        start: date,
        end: date,
        variables: Sequence[str],
        **extra: str,
    ) -> dict[str, str]:
        return {
            "latitude": _coord(point.lat),
            "longitude": _coord(point.lon),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "hourly": ",".join(variables),
            "models": model,
            "timezone": self.config.zona_horaria,
            **extra,
        }

    # ------------------------------------------------------------------ forecast
    def forecast(self, point: CriticalPoint, hours: int) -> pd.DataFrame:
        """Hourly forecast for the next `hours`, preceded by the last 7 days.

        Column `pronostico` is True for hours after the current hour. The URL carries the
        hour window, so the HTTP and Parquet caches hold one forecast per hour.
        """
        if not 1 <= hours <= 16 * 24:
            raise ValueError("hours must be between 1 and 384")
        model = self.config.modelo_pronostico
        offset = timedelta(seconds=self._utc_offset_seconds())
        now_local = (self._now().astimezone(UTC) + offset).replace(
            minute=0, second=0, microsecond=0, tzinfo=None
        )
        first = now_local - timedelta(hours=FORECAST_PAST_HOURS)
        last = now_local + timedelta(hours=hours)
        path = self._cache_path(
            "pronostico", point, model, f"{first:%Y%m%dT%H}", f"{last:%Y%m%dT%H}"
        )
        if path.exists():
            frame = pd.read_parquet(path)
        else:
            params = {
                "latitude": _coord(point.lat),
                "longitude": _coord(point.lon),
                "hourly": ",".join(HOURLY_VARIABLES),
                "models": model,
                "timezone": self.config.zona_horaria,
                "start_hour": f"{first:%Y-%m-%dT%H:%M}",
                "end_hour": f"{last:%Y-%m-%dT%H:%M}",
            }
            n_days = (FORECAST_PAST_HOURS + hours) / 24
            data, _ = self._get_json(
                self.config.forecast_url, params, len(HOURLY_VARIABLES), n_days
            )
            frame = parse_hourly(data)
            path.parent.mkdir(parents=True, exist_ok=True)
            frame.to_parquet(path, index=False)
        frame = frame.copy()
        frame["pronostico"] = frame["time"] > pd.Timestamp(now_local)
        return frame

    def _utc_offset_seconds(self) -> int:
        # Argentina has had no DST since 2009: Jujuy is UTC-3 all year.
        tz = self.config.zona_horaria
        if tz.startswith("America/Argentina/"):
            return -3 * 3600
        offset = pd.Timestamp(self._now()).tz_convert(tz).utcoffset()
        return int(offset.total_seconds()) if offset is not None else 0

    # ------------------------------------------------------------------ grid cells
    def grid_cells(self, point: CriticalPoint) -> list[GridCell]:
        """Per model in `modelos_grilla`: cell centre and cell elevation vs the point.

        The point elevation is what Open-Meteo uses for downscaling (90 m DEM, default
        request); the cell elevation comes from `elevation=nan` (downscaling disabled).
        """
        day = self.config.desde
        dem = self._meta(point, self.config.modelo_historico, day)
        cells = []
        for model in self.config.modelos_grilla:
            meta = self._meta(point, model, day, elevation="nan")
            cells.append(
                GridCell(
                    punto_id=point.id,
                    modelo=model,
                    lat_grilla=round(meta.latitude, 4),
                    lon_grilla=round(meta.longitude, 4),
                    elev_grilla_m=meta.elevation,
                    elev_punto_m=dem.elevation,
                )
            )
        return cells

    def _meta(self, point: CriticalPoint, model: str, day: date, **extra: str) -> ResponseMeta:
        params = self._archive_params(point, model, day, day, ["precipitation"], **extra)
        _, meta = self._get_json(self.config.archive_url, params, 1, 1)
        return meta

    # ------------------------------------------------------------------ plumbing
    def _get_json(
        self, base_url: str, params: dict[str, str], n_variables: int, n_days: float
    ) -> tuple[dict[str, Any], ResponseMeta]:
        url = f"{base_url}?{urlencode(params)}"
        peek = getattr(self.fetcher, "cached", None)
        result = peek(url) if callable(peek) else None
        if result is None:
            weight = call_weight(n_variables, n_days)
            self.ledger.reserve(weight)
            result = self.fetcher.get(url)
            if result.from_cache:
                self.ledger.refund(weight)
        data = _decode(result)
        return data, _response_meta(data)

    def _cache_path(
        self, kind: str, point: CriticalPoint, model: str, start: str, end: str
    ) -> Path:
        name = f"{_coord(point.lat)}_{_coord(point.lon)}_{start}_{end}.parquet"
        return self._cache_folder(kind, model) / name

    def _cache_folder(self, kind: str, model: str) -> Path:
        """Hourly series depend on the timezone, so it is part of the cache key."""
        return self.cache_dir / kind / model / self.config.zona_horaria.replace("/", "_")

    def _write_cache(
        self, point: CriticalPoint, model: str, start: date, end: date, frame: pd.DataFrame
    ) -> None:
        path = self._cache_path("archivo", point, model, start.isoformat(), end.isoformat())
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(path, index=False)

    def _find_cached(
        self, point: CriticalPoint, model: str, start: date, end: date
    ) -> tuple[pd.DataFrame, date] | None:
        """Best cached archive for the point, tolerating 5-decimal rounding noise (~1 m)."""
        folder = self._cache_folder("archivo", model)
        best: tuple[date, Path] | None = None
        for path in folder.glob("*.parquet") if folder.exists() else ():
            try:
                lat, lon, s_start, s_end = path.stem.split("_")
                c_lat, c_lon = float(lat), float(lon)
                c_start, c_end = date.fromisoformat(s_start), date.fromisoformat(s_end)
            except ValueError:
                continue
            near = (
                abs(c_lat - point.lat) <= SAME_POINT_DEG
                and abs(c_lon - point.lon) <= SAME_POINT_DEG
            )
            if near and c_start <= start and (best is None or c_end > best[0]):
                best = (c_end, path)
        if best is None or best[0] < start:
            return None
        return pd.read_parquet(best[1]), best[0]


def parse_hourly(data: dict[str, Any]) -> pd.DataFrame:
    """Open-Meteo `hourly` block → DataFrame(time, precipitacion_mm, nieve_cm, temp_c)."""
    hourly = data.get("hourly")
    if not isinstance(hourly, dict) or "time" not in hourly:
        raise OpenMeteoError("respuesta sin bloque 'hourly'")
    frame = pd.DataFrame({"time": pd.to_datetime(hourly["time"], format="%Y-%m-%dT%H:%M")})
    for api_name, column in HOURLY_VARIABLES.items():
        values = hourly.get(api_name)
        if values is None or len(values) != len(frame):
            raise OpenMeteoError(f"variable '{api_name}' ausente o incompleta")
        frame[column] = pd.Series(values, dtype="float64")
    return frame


def _decode(result: FetchResult) -> dict[str, Any]:
    try:
        data = json.loads(result.content)
    except json.JSONDecodeError as exc:
        raise OpenMeteoError(f"HTTP {result.status}: respuesta no es JSON") from exc
    if not isinstance(data, dict):
        raise OpenMeteoError(f"HTTP {result.status}: respuesta inesperada")
    if not result.ok or data.get("error"):
        raise OpenMeteoError(
            f"HTTP {result.status}: {data.get('reason', 'error')}", status=result.status
        )
    return data


def _response_meta(data: dict[str, Any]) -> ResponseMeta:
    try:
        elevation = data.get("elevation")
        return ResponseMeta(
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            elevation=None
            if elevation is None or math.isnan(float(elevation))
            else float(elevation),
            utc_offset_seconds=int(data.get("utc_offset_seconds", 0)),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise OpenMeteoError("respuesta sin latitud/longitud") from exc


def _slice(frame: pd.DataFrame, start: date, end: date) -> pd.DataFrame:
    lo, hi = pd.Timestamp(start), pd.Timestamp(end) + pd.Timedelta(days=1)
    out = frame[(frame["time"] >= lo) & (frame["time"] < hi)]
    return out.reset_index(drop=True)


def _coord(value: float) -> str:
    return f"{value:.5f}"


def shared_cells(cells: Sequence[GridCell]) -> dict[tuple[str, float, float], list[str]]:
    """(modelo, lat, lon) → point ids, only for cells shared by two or more points."""
    groups: dict[tuple[str, float, float], list[str]] = {}
    for cell in cells:
        groups.setdefault((cell.modelo, cell.lat_grilla, cell.lon_grilla), []).append(cell.punto_id)
    return {k: v for k, v in groups.items() if len(v) > 1}
