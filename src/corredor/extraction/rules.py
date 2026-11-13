"""Rule-based extractor: route, km, known places and cause keywords from article metadata.

Only the headline, the short lede and the URL path are read (the body is never stored).
One article yields at most one event; deduplication merges events across outlets.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from typing import Final

from corredor.extraction import patterns as p
from corredor.extraction.base import EventExtractor
from corredor.models import Article, Causa, ClosureEvent, Confianza, CriticalPoint, Ruta, TipoCorte

# Normalised place name (patterns.PLACE) → critical point id. Places without a point
# (Humahuaca, Uquía, Saladillo…) still mark the article as corridor, without punto_id.
PLACE_POINTS: Final[Mapping[str, str]] = {
    "barcena": "rn9_cuesta_barcena",
    "volcan": "rn9_volcan",
    "los filtros": "rn9_volcan",
    "tumbaya": "rn9_tumbaya",
    "maimara": "rn9_maimara",
    "tilcara": "rn9_tilcara",
    "huacalera": "rn9_huacalera",
    "purmamarca": "rn52_purmamarca_chalala",
    "chalala": "rn52_purmamarca_chalala",
    "lipan": "rn52_lipan_bajo",
    "potrerillos": "rn52_abra_potrerillos",
    "ronqui angosto": "rn52_ronqui_angosto",
    "roqui angosto": "rn52_ronqui_angosto",
    "ranqui angosto": "rn52_ronqui_angosto",
    "salinas grandes": "rn52_salinas_grandes",
    "susques": "rn52_susques",
    "jama": "rn52_paso_jama",
}
RN9_PLACES: Final = frozenset({"humahuaca", "uquia", "quebrada de humahuaca"})
LIPAN_SNOW_POINT: Final = "rn52_abra_potrerillos"
KM_TOLERANCE: Final = 5.0

# patterns.CAUSE_GROUPS name → ClosureEvent.causa ("temporal"/"tormenta" alone is "otro").
CAUSE_MAP: Final[Mapping[str, Causa]] = {
    "aluvion": "aluvion",
    "crecida": "crecida",
    "nieve": "nieve",
    "protesta": "protesta",
    "obra": "obra",
    "accidente": "accidente",
    "meteo_generico": "otro",
}

KM: Final = re.compile(r"\b(?:km|kilometro) (\d{1,4}(?:[.,]\d+)?)\b")
TOTAL: Final = re.compile(r"\b(?:total(?:mente)?|intransitables?|ambos carriles|ambas manos)\b")
PARTIAL: Final = re.compile(
    r"\b(?:parcial(?:mente)?|media calzada|un carril|una mano|intermitente|demoras)\b"
)
CAUTION: Final = re.compile(r"\b(?:precaucion|cadenas|transitar con)\b")


def _first_position(rx: re.Pattern[str], text: str) -> int | None:
    m = rx.search(text)
    return m.start() if m else None


class RuleBasedExtractor(EventExtractor):
    PARSER_VERSION: Final = 1

    def __init__(self, points: Sequence[CriticalPoint]) -> None:
        self.points = list(points)
        self._by_id = {pt.id: pt for pt in self.points}

    @staticmethod
    def text_of(article: Article) -> str:
        return " . ".join(
            t for t in (article.titular, article.bajada, p.url_text(article.url)) if t
        )

    def extract(self, article: Article) -> list[ClosureEvent]:
        text = self.text_of(article)
        if not p.is_corridor(text) or not (p.is_closure(text) or p.is_reopening(text)):
            return []
        cleaned = p.strip_negatives(p.norm(text))
        causa = self._cause(cleaned)
        point = self._point(cleaned, causa)
        km = self._km(cleaned)
        routes = p.routes(text)
        ruta = self._route(point, routes, cleaned)
        if point is None and km is not None and ruta != "otra":
            point = self._nearest(ruta, km)
        confianza: Confianza = "alta" if point and causa != "otro" else "media"
        if point is None and len(routes) != 1:
            confianza = "baja"
        places = sorted(p.places(text))
        return [
            ClosureEvent(
                evento_id=hashlib.sha1(  # noqa: S324 — identifier, not security
                    f"{article.source_id}|{article.url}".encode()
                ).hexdigest()[:16],
                fecha=article.fecha,
                ruta=ruta,
                punto_id=point.id if point else None,
                km=km,
                paraje=", ".join(places),
                causa=causa,
                tipo_corte=self._kind(cleaned),
                fuentes=[article.url],
                n_medios=1,
                metodo="reglas",
                confianza=confianza,
            )
        ]

    @staticmethod
    def _cause(cleaned: str) -> Causa:
        found = {
            name: pos
            for name, rx in p.CAUSE_GROUPS.items()
            if (pos := _first_position(rx, cleaned)) is not None
        }
        if not found:
            return "otro"
        specific = {k: v for k, v in found.items() if k != "meteo_generico"} or found
        return CAUSE_MAP[min(specific, key=lambda k: (specific[k], k))]

    def _point(self, cleaned: str, causa: Causa) -> CriticalPoint | None:
        matches = sorted((m.start(), m.group(0)) for m in p.PLACE.finditer(cleaned))
        for _, place in matches:
            pid = PLACE_POINTS.get(place)
            if pid == "rn52_lipan_bajo" and causa == "nieve":
                pid = LIPAN_SNOW_POINT
            if pid is not None and pid in self._by_id:
                return self._by_id[pid]
        return None

    @staticmethod
    def _km(cleaned: str) -> float | None:
        m = KM.search(cleaned)
        return float(m.group(1).replace(",", ".")) if m else None

    @staticmethod
    def _route(point: CriticalPoint | None, routes: set[str], cleaned: str) -> Ruta:
        if point is not None:
            return point.ruta
        if routes == {"RN9"} or (not routes and any(pl in cleaned for pl in RN9_PLACES)):
            return "RN9"
        if routes == {"RN52"}:
            return "RN52"
        return "otra"

    def _nearest(self, ruta: Ruta, km: float) -> CriticalPoint | None:
        candidates = [
            (abs(pt.km - km), pt.id, pt)
            for pt in self.points
            if pt.ruta == ruta and pt.km is not None and abs(pt.km - km) <= KM_TOLERANCE
        ]
        return min(candidates)[2] if candidates else None

    @staticmethod
    def _kind(cleaned: str) -> TipoCorte:
        if TOTAL.search(cleaned):
            return "total"
        if PARTIAL.search(cleaned):
            return "parcial"
        if CAUTION.search(cleaned):
            return "precaucion"
        return "desconocido"
