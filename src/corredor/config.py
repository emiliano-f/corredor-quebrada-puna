"""Configuration: config.yaml (yaml.safe_load) + environment variables (pydantic-settings)."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from corredor.models import CriticalPoint, SourceConfig


class HttpConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_agent: str
    min_interval_s: float = Field(default=2.5, ge=2.0)
    timeout_s: float = 30.0
    retries: int = Field(default=3, ge=0)
    robots_ttl_h: float = 24.0
    not_found_ttl_h: float = 24.0


class BackfillConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    desde: date = date(2016, 1, 1)
    max_requests_per_run: int = Field(default=2000, ge=1)
    muestra_sitemaps: list[str] = Field(default_factory=list)


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    http: HttpConfig
    backfill: BackfillConfig = Field(default_factory=BackfillConfig)
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
