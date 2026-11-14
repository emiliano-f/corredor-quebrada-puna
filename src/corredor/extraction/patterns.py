"""Shared regex for source filters (WordPress, sitemaps) and the RuleBasedExtractor.

Fixed per HANDOFF §7.1. Every helper normalises its input with `norm()` (lowercase, no
accents, hyphens/underscores/slashes → spaces), so patterns are written without accents.
Negative phrases ("Corte Suprema", "corte de luz", "cierre de campaña", foreign volcanoes…)
are removed from the text BEFORE the positive patterns are evaluated.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Final, Literal
from urllib.parse import urlsplit

SlugLevel = Literal["B", "C_solo_ruta"]


def norm(text: str) -> str:
    """Lowercase, strip accents (NFKD: 'º' → 'o', 'á' → 'a'), separators → spaces."""
    decomposed = unicodedata.normalize("NFKD", text.lower())
    plain = "".join(c for c in decomposed if not unicodedata.combining(c))
    plain = re.sub(r"[-_/|]+", " ", plain)
    return re.sub(r"\s+", " ", plain).strip()


def _rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern)


# "Ruta Nacional Nº 52" → "ruta nacional no 52"; also nro, n°, numero, nac., rn9, rn 52.
_ROUTE_NUM_PREFIX: Final = r"(?:(?:n|no|nro|n°|n\.o|numero)\.? ?)?"
ROUTE: Final = _rx(
    r"\b(?:ruta (?:nacional |nac\.? )?" + _ROUTE_NUM_PREFIX + r"(?P<n1>9|52)"
    r"|rn ?(?P<n2>9|52))(?![\d])"
)

PLACE: Final = _rx(
    r"\b(?:yala|lozano|(?<!papa )leon(?! x[iv])|volcan|los filtros|barcena|tumbaya"
    r"|purmamarca|chalala|lipan|potrerillos"
    r"|ron?qui angosto|ranqui angosto|saladillo|salinas grandes|susques|jama|maimara"
    r"|tilcara|huacalera|humahuaca|uquia|quebrada de humahuaca)\b"
)

# Closure terms. "cerro" (mountain) and "cerros" are deliberately excluded; the accented
# past tense "cerró" is matched on the raw text by RAW_CERRO instead.
CLOSURE: Final = _rx(
    r"\b(?:cortes?|cortad[ao]s?|cort(?:a|an|aron|ara|aran|aria|arian)"
    r"|cierres?|cierra\w*|cerr(?:aron|aran|ado|ada|ados|adas|ar|ara|arian)"
    r"|interrump\w*|interrupci\w*|intransitables?|inhabilitad[ao]s?|desvios?"
    r"|bloque(?:o|ada|ado|an|aron)|clausur\w*"
    r"|(?:ruta|rn|transito|paso|camino|circulacion)(?: nacional)?(?: \d+)? se corto"
    r"|corto(?= (?:la ruta|el transito|el paso|la circulacion|el camino)))\b"
)
RAW_CERRO: Final = re.compile(r"\bcerró\b")
# A suggested alternate route ("circular por ruta 52", "desvío por la ruta 9", "usar la
# ruta 52") is not a closure of that route; "circular con precaución por la ruta 9" is.
ALT_ROUTE: Final = _rx(
    r"\b(?<!\bno )(?:(?:circular|circulen|desvios?|desviad[ao]s?|desvian|alternativa)"
    r" (?:por|a traves de|via)|usar|utilizar|tomar) (?:(?:la|el) )?(?:ruta (?:nacional |nac\.? )?"
    + _ROUTE_NUM_PREFIX
    + r"(?:9|52)|rn ?(?:9|52))(?![\d])(?! con precaucion)"
)
# South of Yala (San Salvador de Jujuy, Alto Comedero, Palpalá): out of the corridor scope.
SOUTH: Final = _rx(r"\b(?:san salvador de jujuy|alto comedero|palpala|chango mas)\b")
# Paso de Jama side of the closure.
SIDE_CL: Final = _rx(
    r"\b(?:lado chileno|chile|chilen[ao]s?|san pedro de atacama|calama|ruta 27|ch ?-? ?27)\b"
)
SIDE_AR: Final = _rx(r"\b(?:lado argentino|del lado de argentina|susques)\b")
JAMA_DESTINATION: Final = _rx(
    r"\b(?:camino|rumbo|acceso|ruta \d+|ruta nacional \d+|rn ?\d+|que (?:une|conduce|lleva|va))"
    r" (?:a|al|hacia) (?:el )?(?:paso (?:internacional )?(?:de )?)?jama\b"
)
WIND: Final = _rx(r"\b(?:vientos?|rafagas?)\b")
# Weather named without a specific cause ("cerrado por condiciones climáticas").
CLIMATE_IMPLICIT: Final = _rx(
    r"\b(?:condiciones (?:climaticas|meteorologic\w*|del tiempo)|mal tiempo|temporal(?:es)?"
    r"|inclemencias?(?: climaticas)?)\b"
)
REOPENING: Final = _rx(r"\b(?:habilit\w*|rehabilit\w*|reabr\w*|reapert\w*)\b")
TRAFFIC: Final = _rx(r"\b(?:transitabilidad|transito|km \d+|kilometro \d+)\b")

CAUSE_GROUPS: Final[dict[str, re.Pattern[str]]] = {
    "aluvion": _rx(
        r"\b(?:alud(?:es)?|aluvion(?:es)?|aluvional(?:es)?|derrumbes?|desmoronamientos?"
        r"|deslaves?|barro|piedras|socav\w*|lluvias?)\b"
    ),
    "crecida": _rx(r"\b(?:crecidas?|desbordes?|rios?|anegamientos?|anegad[ao]s?)\b"),
    "nieve": _rx(r"\b(?:nevadas?|nieve|viento blanco|hielo|escarcha|cadenas)\b"),
    "meteo_generico": _rx(r"\b(?:temporal(?:es)?|tormentas?|granizo)\b"),
    "protesta": _rx(r"\b(?:piquetes?|protestas?|manifestaci\w*)\b"),
    "obra": _rx(r"\b(?:obras?|bacheo)\b"),
    "accidente": _rx(r"\b(?:accidentes?|vuelcos?|volco|choques?)\b"),
}
# A road cut by organised people is a protest even without the word "protesta".
PROTEST_CUT: Final = _rx(
    r"\b(?:cortes?|corta|cortan|cortaron|piquetes?|bloqueos?|bloque(?:an|aron|ada|ado))\b"
)
PROTEST_ACTORS: Final = _rx(
    r"\b(?:comunidad(?:es)?(?! educativ)|comuneros?|vecin[ao]s|manifestantes|docentes|trabajadores"
    r"|gremio(?:s|ales)?|autoconvocad[ao]s)\b"
)
# Actors stranded by the cut ("docentes varados por el corte", "dejó varados a docentes")
# are not protesters.
_STRANDED: Final = r"(?: \w+){0,5} (?:varad\w*|quedaron|evacuad\w*|afectad\w*|damnificad\w*)"
_STRANDED_BEFORE: Final = re.compile(
    r"\b(?:varad\w*|evacuad\w*|afectad\w*|damnificad\w*)(?: \w+){0,2} $"
)


def is_protest_cut(normalized: str) -> bool:
    """A cut/blockade term and a protest actor in the same text, the actor not stranded."""
    if not PROTEST_CUT.search(normalized):
        return False
    return any(
        not re.match(_STRANDED, normalized[m.end() :])
        and not _STRANDED_BEFORE.search(normalized[max(0, m.start() - 60) : m.start()])
        for m in PROTEST_ACTORS.finditer(normalized)
    )


# Vehicle/accident/freight stories ("otro") count only with an explicit closure term.
VEHICLE: Final = _rx(
    r"\b(?:accidentes?|choques?|colisi\w*|vuelcos?|volc(?:o|aron|ado|ada)|despist\w*"
    r"|siniestros?|transporte de carga|carga pesada)\b"
)
VEHICLE_CLOSURE: Final = _rx(
    r"\b(?:cortes?|cortad[ao]s?|cort(?:a|an|aron)|interrump\w*|interrupci\w*"
    r"|cerrad[ao]s?|cerr(?:aron|aran)|cierres?|cierra\w*|clausur\w*|intransitables?|inhabilitad[ao]s?"
    r"|bloque(?:o|os|ada|adas|ado|ados|an|aron)|media calzada)\b"
)
# Incidents only signal a closure when a closure term is also present.
INCIDENT_GROUPS: Final = frozenset({"accidente"})

NEGATIVES: Final = _rx(
    r"\bcorte suprema\b"
    r"|\bcortes? (?:de|del) (?:luz|agua|energia|electricidad|gas|suministro|servicio"
    r"|cinta|pelo|cabello|boleto|carne|presupuesto)\b"
    r"|\bcierres? (?:de|del) (?:la )?(?:campana|temporada|festival|ano|listas|ciclo"
    r"|inscripcion\w*|ejercicio|edicion|carnaval|mes)\b"
    r"|\bvolcan(?:es)? (?:de fuego|lascar|villarrica|etna|popocatepetl|osorno|calbuco"
    r"|llaima|copahue|hunga|kilauea|taal)\b"
    r"|\bministerio de (?:infraestructura|obras publicas)\b"
    r"|\bobras? (?:publicas|sociales?|de teatro|de arte)\b"
)

_CMS_ID_SUFFIX: Final = re.compile(r"[-_]n?\d{4,}(?:\.html?)?$")


def strip_negatives(normalized: str) -> str:
    return NEGATIVES.sub(" ", normalized)


def _clean(text: str) -> str:
    return strip_negatives(norm(text))


def without_alternates(normalized: str) -> str:
    return ALT_ROUTE.sub(" ", normalized)


def routes(text: str) -> set[str]:
    """Routes named in the text, leaving out suggested alternate routes (ALT_ROUTE)."""
    found = set()
    for m in ROUTE.finditer(without_alternates(_clean(text))):
        found.add("RN" + (m.group("n1") or m.group("n2")))
    return found


def places(text: str) -> set[str]:
    return {m.group(0) for m in PLACE.finditer(_clean(text))}


def is_corridor(text: str) -> bool:
    cleaned = _clean(text)
    return bool(ROUTE.search(cleaned) or PLACE.search(cleaned))


def is_closure(text: str) -> bool:
    cleaned = _clean(text)
    return bool(CLOSURE.search(cleaned) or RAW_CERRO.search(text.lower()))


# Words that tie a closure term to the road itself, or "en/entre <corridor place>".
ROAD: Final = _rx(
    r"\b(?:rutas?|rn ?\d+|transito|transitabilidad|calzada|carril(?:es)?|camino"
    r"|circulacion|vehicul\w*|vialidad|banquina|automovilistas|conductores"
    r"|paso (?:de jama|internacional|fronterizo)|km \d+|kilometro \d+)\b"
)
# "corte en Volcán", "cortada totalmente entre Purmamarca y …": right after the closure term.
AT_PLACE: Final = _rx(
    r" (?:(?:total|parcial)(?:mente)? )?(?:en|entre|a la altura de|hacia) " + PLACE.pattern[2:]
)
ROAD_WINDOW: Final = 60
# Extraction-only negatives (kept out of NEGATIVES so the source filters don't change).
SERVICE_CUT: Final = _rx(
    r"\binterrupci\w* (?:del? |de la )?(?:servicio|suministro|energia|luz|agua)\b"
)


# Drug seizures / security operations: only a closure term next to a road word counts.
POLICE_OP: Final = _rx(
    r"\b(?:incaut\w*|decomis\w*|secuestr\w*|cocaina|marihuana|estupefacientes?|drogas?"
    r"|narco\w*|contrabando|procedimientos?)\b"
)
# Border closed for administrative / health reasons (not weather): causa "otro" + note.
HEALTH_CLOSURE: Final = _rx(
    r"\b(?:covid\w*|coronavirus|pandemia|cuarentena|contagios|brote"
    r"|(?:emergencia|medidas?|razones|motivos|protocolos?) sanitari\w*)\b"
)
# "cierre de fronteras" alone is administrative only if no weather cause is named.
BORDER_CLOSURE: Final = _rx(r"\bcierr\w* (?:de )?(?:las |los )?(?:fronteras|limites)\b")
ADMIN_NOTE: Final = "cierre administrativo/sanitario (no meteorológico)"


def is_road_closure(text: str) -> bool:
    """A closure/reopening term within ROAD_WINDOW characters of a road word, or at a place.

    With a police-operation term (POLICE_OP) only a closure term (not a reopening one:
    "paso no habilitado") next to a road word counts."""
    cleaned = SERVICE_CUT.sub(" ", _clean(text))
    strict = bool(POLICE_OP.search(cleaned))
    for rx in (CLOSURE,) if strict else (CLOSURE, REOPENING):
        for m in rx.finditer(cleaned):
            loose = m.group(0).startswith("intransitab") or AT_PLACE.match(cleaned, m.end())
            if loose and not strict:
                return True
            around = cleaned[max(0, m.start() - ROAD_WINDOW) : m.end() + ROAD_WINDOW]
            if ROAD.search(around):
                return True
    raw = text.lower()
    if strict:
        return any(
            ROAD.search(_clean(raw[max(0, m.start() - ROAD_WINDOW) : m.end() + ROAD_WINDOW]))
            for m in RAW_CERRO.finditer(raw)
        )
    return bool(RAW_CERRO.search(raw) and ROAD.search(cleaned))


def is_admin_closure(text: str, weather: bool) -> bool:
    """Health closure, or a border closure when the text names no weather cause."""
    cleaned = _clean(text)
    return bool(HEALTH_CLOSURE.search(cleaned) or (not weather and BORDER_CLOSURE.search(cleaned)))


def is_reopening(text: str) -> bool:
    return bool(REOPENING.search(_clean(text)))


def causes(text: str) -> set[str]:
    """Cause groups present in the text (incident groups only with a closure term)."""
    cleaned = _clean(text)
    found = {name for name, rx in CAUSE_GROUPS.items() if rx.search(cleaned)}
    if found & INCIDENT_GROUPS and not is_closure(text):
        found -= INCIDENT_GROUPS
    return found


def has_cause_or_closure(text: str) -> bool:
    return bool(is_closure(text) or is_reopening(text) or causes(text))


def is_candidate(text: str) -> bool:
    """Corridor (route or place) AND a closure/reopening/cause signal."""
    return is_corridor(text) and has_cause_or_closure(text)


def term_regex(term: str) -> re.Pattern[str]:
    """Word-boundary regex for a search term on normalised text ('alud' never hits 'salud')."""
    t = re.escape(norm(term))
    if t == "alud":
        return re.compile(r"\balud(?:es)?\b")
    return re.compile(rf"\b{t}\b")


WP_SEARCH_TERMS: Final = (
    "Lipán",
    "Jama",
    "Volcán",
    "Purmamarca",
    "Susques",
    "Bárcena",
    "Tumbaya",
    "Salinas Grandes",
    "Maimará",
    "Huacalera",
    "aluvión",
    "alud",
    "derrumbe",
    "desmoronamiento",
    "nevada",
    "crecida",
)
"""Server-side WordPress search terms (generic words like "ruta 9" or "corte" are noise)."""


def search_variants(term: str) -> list[str]:
    """The term with and without accents (WordPress accent-insensitivity depends on collation)."""
    plain = "".join(c for c in unicodedata.normalize("NFKD", term) if not unicodedata.combining(c))
    return [term] if plain == term else [term, plain]


def url_text(url: str) -> str:
    """Normalised full URL path (not just the last segment), without CMS id suffixes."""
    path = urlsplit(url).path.rstrip("/")
    segments = [_CMS_ID_SUFFIX.sub("", seg) for seg in path.split("/") if seg]
    return norm(" ".join(segments))


def slug_level(url: str) -> SlugLevel | None:
    """Sitemap filter C (HANDOFF §3.3): 'B' = corridor + cause/closure/traffic term;
    'C_solo_ruta' = names RN 9 / RN 52 without such a term; None = skip."""
    text = url_text(url)
    if is_corridor(text) and (has_cause_or_closure(text) or TRAFFIC.search(_clean(text))):
        return "B"
    if routes(text):
        return "C_solo_ruta"
    return None
