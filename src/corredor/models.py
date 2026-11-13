"""Data models shared by every stage.

Frozen after the foundation PR: children may only ADD optional fields (and say so in
their PR). Any table/column change bumps SCHEMA_VERSION once, in the integration PR.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION = 1

Ruta = Literal["RN9", "RN52", "otra"]
Causa = Literal["aluvion", "crecida", "nieve", "accidente", "protesta", "obra", "otro"]
TipoCorte = Literal["total", "parcial", "precaucion", "desconocido"]
Metodo = Literal["reglas", "llm"]
Confianza = Literal["alta", "media", "baja"]
FechaFuente = Literal["published_time", "fallback"]
MetodoFuente = Literal["wordpress_api", "sitemap", "rss", "custom", "snapshot"]
FiltroSlug = Literal["B", "C_solo_ruta"]
FuenteJama = Literal["mop_cl", "argentina_gob_ar"]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SourceConfig(_Model):
    """One outlet from config.yaml `fuentes`."""

    id: str
    nombre: str
    base_url: str
    metodo: MetodoFuente
    tier: Literal[1, 2]
    enabled: bool = False
    archivo_desde: date | None = None
    republica: bool = False
    local: bool = False
    oficial: bool = False
    params: dict[str, Any] = Field(default_factory=dict)


class Article(_Model):
    """News metadata only: never the article body."""

    source_id: str
    parser_version: int
    url: str
    fecha: date
    fecha_fuente: FechaFuente
    titular: str
    bajada: str = ""
    fetched_at: datetime
    filtro_slug: FiltroSlug | None = None


class ClosureEvent(_Model):
    evento_id: str
    fecha: date
    hora: str | None = None
    ruta: Ruta
    punto_id: str | None = None
    km: float | None = None
    paraje: str = ""
    causa: Causa
    tipo_corte: TipoCorte
    duracion_horas: float | None = None
    fuentes: list[str]
    n_medios: int = Field(ge=0)
    metodo: Metodo
    confianza: Confianza
    notas: str = ""


class CriticalPoint(_Model):
    id: str
    nombre: str
    ruta: Ruta
    km: float | None = None
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    verificado: bool = False
    fuente_geo: str = ""
    fuente_km: str = ""


class WeatherDay(_Model):
    punto_id: str
    fecha: date
    precipitacion_mm: float | None = None
    nieve_cm: float | None = None
    temp_max_c: float | None = None
    temp_min_c: float | None = None
    precip_max_horaria_mm: float | None = None


class Threshold(_Model):
    causa: Causa
    variable: str
    umbral: float
    unidad: str


class ValidationResult(_Model):
    threshold: Threshold
    periodo: Literal["train", "test"]
    aciertos: int = Field(ge=0)
    fallos: int = Field(ge=0)
    falsas_alarmas: int = Field(ge=0)


class JamaEstado(_Model):
    """One raw Paso de Jama status snapshot (one line in snapshots/jama_estado.jsonl)."""

    fuente: FuenteJama
    fetched_at: datetime
    payload_json: str | None = None
    error: str | None = None
