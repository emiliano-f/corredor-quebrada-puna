"""Configuration: config.yaml (yaml.safe_load) + environment variables (pydantic-settings)."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from corredor.http import validate_hostname
from corredor.models import CriticalPoint, SourceConfig


class RobotsExemption(BaseModel):
    """A documented public API host whose robots.txt targets crawlers (ADR 0002)."""

    model_config = ConfigDict(extra="forbid")

    host: str
    motivo: str = Field(min_length=1)
    terminos_url: HttpUrl

    @field_validator("host")
    @classmethod
    def _exact_host(cls, value: str) -> str:
        return validate_hostname(value)


class HttpConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_agent: str
    min_interval_s: float = Field(default=2.5, ge=2.0)
    timeout_s: float = 30.0
    retries: int = Field(default=3, ge=0)
    robots_ttl_h: float = 24.0
    not_found_ttl_h: float = 1.0
    robots_exempt_hosts: list[RobotsExemption] = Field(default_factory=list)

    @field_validator("robots_exempt_hosts")
    @classmethod
    def _unique_hosts(cls, value: list[RobotsExemption]) -> list[RobotsExemption]:
        hosts = [e.host for e in value]
        if len(hosts) != len(set(hosts)):
            raise ValueError("robots_exempt_hosts: duplicated host")
        return value


class BackfillConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    desde: date = date(2016, 1, 1)
    max_requests_per_run: int = Field(default=2000, ge=1)
    muestra_sitemaps: list[str] = Field(default_factory=list)


class ClimaConfig(BaseModel):
    """Open-Meteo settings (free tier: non-commercial, CC BY 4.0)."""

    model_config = ConfigDict(extra="forbid")

    desde: date = date(2016, 1, 1)
    zona_horaria: str = "America/Argentina/Jujuy"
    modelo_historico: str = "era5_seamless"
    modelo_pronostico: str = "best_match"
    # Cells recorded per point: era5 = precipitation/snowfall grid, era5_land = temperature.
    modelos_grilla: list[str] = Field(default_factory=lambda: ["era5", "era5_land"])
    # Weighted Open-Meteo calls per UTC day; the client stops with an error above it.
    max_llamadas_diarias: float = Field(default=500, gt=0, lt=10_000)
    archive_url: str = "https://archive-api.open-meteo.com/v1/archive"
    forecast_url: str = "https://api.open-meteo.com/v1/forecast"
    historical_forecast_url: str = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    elevation_url: str = "https://api.open-meteo.com/v1/elevation"


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    http: HttpConfig
    backfill: BackfillConfig = Field(default_factory=BackfillConfig)
    clima: ClimaConfig = Field(default_factory=ClimaConfig)
    puntos: list[CriticalPoint]
    fuentes: list[SourceConfig]

    def enabled_sources(self) -> list[SourceConfig]:
        return [s for s in self.fuentes if s.enabled]

    def sources_hash(self) -> str:
        """Stable hash of the `fuentes` section, for data lineage."""
        payload = json.dumps(
            [s.model_dump(mode="json") for s in self.fuentes], sort_keys=True, ensure_ascii=False
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


class Settings(BaseSettings):
    """Runtime settings from env vars. The pipeline runs without any key."""

    model_config = SettingsConfigDict(env_prefix="CORREDOR_", extra="ignore")

    config_path: Path = Path("config.yaml")
    data_dir: Path = Path("data")
    llm_api_key: SecretStr | None = Field(default=None, validation_alias="LLM_API_KEY")

    @property
    def cache_dir(self) -> Path:
        return self.data_dir / "cache"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "corredor.duckdb"


def load_config(path: Path) -> AppConfig:
    with path.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    return AppConfig.model_validate(raw)
