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
from corredor.models import (
    Article,
    Causa,
    ClosureEvent,
    Confianza,
    CriticalPoint,
    Lado,
    Ruta,
    TipoCorte,
)

# Normalised place name (patterns.PLACE) → critical point id. Places without a point
# (Humahuaca, Uquía, Saladillo…) still mark the article as corridor, without punto_id.
PLACE_POINTS: Final[Mapping[str, str]] = {
    "yala": "rn9_yala_lozano",
    "lozano": "rn9_yala_lozano",
    "leon": "rn9_leon",
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
JAMA_POINT: Final = "rn52_paso_jama"
# Yala–León stretch: accidents count only with a total closure of the route.
TOTAL_ONLY_ACCIDENT: Final = frozenset({"rn9_yala_lozano", "rn9_leon"})
KM_TOLERANCE: Final = 5.0

# patterns.CAUSE_GROUPS name → ClosureEvent.causa ("temporal"/"tormenta" alone is "otro").
WEATHER_CAUSES: Final[frozenset[Causa]] = frozenset({"aluvion", "crecida", "nieve"})
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
    PARSER_VERSION: Final = 4

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
        if not p.is_corridor(text) or not p.is_road_closure(text):
            return []
        cleaned = p.strip_negatives(p.norm(text))
        if p.SOUTH.search(cleaned) and not p.PLACE.search(cleaned):
            return []  # entirely south of Yala: out of scope
        causa = self._cause(cleaned)
        weather = causa in WEATHER_CAUSES
        admin = (weather or causa == "otro") and p.is_admin_closure(text, weather)
        if admin:
            causa = "otro"  # border closed for health/administrative reasons, not weather
        routes = p.routes(text)
        found = self._points(cleaned, causa)
        if len(routes) == 1:  # an explicitly named route wins over places on the other one
            found = [pt for pt in found if pt.ruta in routes]
        notas = p.ADMIN_NOTE if admin else ""
        if causa == "otro" and not admin and p.WIND.search(cleaned):
            notas = "viento"
        tipo = self._kind(cleaned, p.is_reopening(text) and not p.is_closure(text))
        if len(found) > 1:
            return [
                ev for pt in found
                if (ev := self._event(article, pt, causa, tipo, notas, cleaned, text, multi=True))
            ]  # fmt: skip
        point = found[0] if found else None
        km = self._km(cleaned)
        ruta = self._route(point, routes, cleaned)
        if point is None and km is not None and ruta != "otra":
            point = self._nearest(ruta, km)
        confianza: Confianza = "alta" if point and causa != "otro" else "media"
        if point is None and len(routes) != 1:
            confianza = "baja"
        ev = self._event(article, point, causa, tipo, notas, cleaned, text, ruta, km, confianza)
        return [ev] if ev else []

    def _event(
        self,
        article: Article,
        point: CriticalPoint | None,
        causa: Causa,
        tipo: TipoCorte,
        notas: str,
        cleaned: str,
        text: str,
        ruta: Ruta | None = None,
        km: float | None = None,
        confianza: Confianza = "alta",
        multi: bool = False,
    ) -> ClosureEvent | None:
        pid = point.id if point else None
        if causa == "accidente" and pid in TOTAL_ONLY_ACCIDENT and tipo != "total":
            return None
        lado: Lado | None = None
        if pid == JAMA_POINT:
            cl, ar = bool(p.SIDE_CL.search(cleaned)), bool(p.SIDE_AR.search(cleaned))
            lado = "ambos" if cl and ar else "CL" if cl else "AR" if ar else "desconocido"
            if (
                lado in ("CL", "ambos")
                and tipo in ("precaucion", "desconocido")
                and p.is_closure(text)
            ):
                tipo = "total"  # the Chilean side closed: the corridor is closed
        key = f"{article.source_id}|{article.url}" + (f"|{pid}" if multi else "")
        return ClosureEvent(
            evento_id=hashlib.sha1(key.encode()).hexdigest()[:16],  # noqa: S324 — identifier
            fecha=article.fecha,
            ruta=point.ruta if (multi and point) else (ruta or "otra"),
            punto_id=pid,
            km=km,
            paraje=", ".join(sorted(p.places(text))),
            causa=causa,
            tipo_corte=tipo,
            fuentes=[article.url],
            n_medios=1,
            metodo="reglas",
            confianza="alta" if multi and causa != "otro" else ("media" if multi else confianza),
            notas=notas,
            lado=lado,
        )

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

    def _points(self, cleaned: str, causa: Causa) -> list[CriticalPoint]:
        """Distinct critical points named in the text, in order of appearance."""
        out: list[CriticalPoint] = []
        for m in p.PLACE.finditer(cleaned):
            pid = PLACE_POINTS.get(m.group(0))
            if pid == "rn52_lipan_bajo" and causa == "nieve":
                pid = LIPAN_SNOW_POINT
            if pid is not None and pid in self._by_id and self._by_id[pid] not in out:
                out.append(self._by_id[pid])
        return out

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
    def _kind(cleaned: str, reopening_only: bool = False) -> TipoCorte:
        if not reopening_only and TOTAL.search(cleaned):
            return "total"
        if PARTIAL.search(cleaned):
            return "parcial"
        if CAUTION.search(cleaned):
            return "precaucion"
        return "desconocido"
