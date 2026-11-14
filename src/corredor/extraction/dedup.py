"""Event deduplication: one closure reported by several outlets becomes one event.

Two events are the same closure when they share the route, their points are compatible
(equal, or at least one without point) and their dates are within `window_days`, and
  * same point and compatible causes (same family — aluvión and crecida are one rain
    family — or one of them "otro"), or
  * at least one without point and the same cause family (neither "otro"), or
  * at least one without point and similar headlines (Jaccard of normalised tokens >=
    `min_jaccard`, both with >= `min_tokens` tokens).
A follow-up article (FOLLOW_UP: schedules, "habilitan", "reabren", "sigue cortada",
works after a closure…) joins a cluster on the same route with compatible points within
`follow_days` of any member and inherits the cluster's cause; without a shared point, a
follow-up that names its own cause needs the same cause family, and a located event only
absorbs point-less clusters of a compatible family.
Clusters grow by single linkage over events sorted by date. The merged event keeps
`fecha` = `fecha_inicio` (first article) and `fecha_fin` (last article). `n_medios` counts
distinct outlets, excluding those with `republica: true`.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from corredor.extraction.patterns import norm
from corredor.models import ClosureEvent, Confianza, Lado, TipoCorte

STOPWORDS = frozenset(
    "a al ante con de del desde el en entre es la las lo los para por que se sin su sobre tras "  # noqa: SIM905
    "un una y o e ya hoy".split()
)
FOLLOW_UP = re.compile(
    r"\b(?:habilit\w*|rehabilit\w*|reabr\w*|reapert\w*|sigue cortad\w*|continua cortad\w*"
    r"|sigue el corte|continua el corte|continua cerrad\w*|sigue cerrad\w*|siguen los cortes"
    r"|horarios?|alternativa|desvios?|trabajos|limpieza|pueden circular|restablec\w*)\b"
)
_FAMILY: dict[str, str] = {"aluvion": "lluvia", "crecida": "lluvia"}
REPUBLISHER_NOTE = "solo fuente que republica"
_CONFIANZA: dict[Confianza, int] = {"baja": 0, "media": 1, "alta": 2}
_TIPO: dict[TipoCorte, int] = {"desconocido": 0, "precaucion": 1, "parcial": 2, "total": 3}


@dataclass(frozen=True)
class ArticleRef:
    """What dedup needs to know about the article behind each event URL."""

    source_id: str
    titular: str = ""


def tokens(text: str) -> frozenset[str]:
    return frozenset(
        t for t in norm(text).replace(".", " ").replace(",", " ").split() if t not in STOPWORDS
    )


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


@dataclass
class _Cluster:
    events: list[ClosureEvent] = field(default_factory=list)
    titles: list[frozenset[str]] = field(default_factory=list)
    follow: list[bool] = field(default_factory=list)

    @property
    def point(self) -> str | None:
        return next((e.punto_id for e in self.events if e.punto_id), None)


def family(causa: str) -> str:
    return _FAMILY.get(causa, causa)


def _compatible(a: _Cluster, b: _Cluster) -> bool:
    """Cause families agree, or one of the clusters has no cause yet (only "otro")."""
    fa = {family(e.causa) for e in a.events if e.causa != "otro"}
    fb = {family(e.causa) for e in b.events if e.causa != "otro"}
    return not fa or not fb or bool(fa & fb)


def is_follow_up(titular: str) -> bool:
    return bool(FOLLOW_UP.search(norm(titular)))


class EventDeduplicator:
    """Merges duplicates; n_medios excludes sources with `republica: true`."""

    def __init__(
        self,
        window_days: int = 2,
        republishers: frozenset[str] = frozenset(),
        min_jaccard: float = 0.5,
        min_tokens: int = 5,
        follow_days: int = 7,
    ) -> None:
        self.follow_days = follow_days
        self.window_days = window_days
        self.republishers = republishers
        self.min_jaccard = min_jaccard
        self.min_tokens = min_tokens

    def merge(
        self, events: Sequence[ClosureEvent], articles: Mapping[str, ArticleRef] | None = None
    ) -> list[ClosureEvent]:
        refs = articles or {}
        clusters: list[_Cluster] = []
        order = sorted(events, key=lambda e: (e.fecha, e.punto_id is None, e.fuentes, e.evento_id))
        for ev in order:
            raw_title = " ".join(refs[u].titular for u in ev.fuentes if u in refs)
            title, follow = tokens(raw_title), is_follow_up(raw_title)
            scored = [
                (score, i) for i, c in enumerate(clusters)
                if (score := self._score(c, ev, title, follow)) is not None
            ]  # fmt: skip
            if not scored:
                clusters.append(_Cluster())
                target = clusters[-1]
            else:
                target = clusters[min(scored)[1]]
                if ev.punto_id is not None:  # a located event absorbs point-less matches
                    for i in sorted((i for _, i in scored), reverse=True):
                        other = clusters[i]
                        near = abs((other.events[0].fecha - ev.fecha).days) <= self.window_days
                        if (
                            other is not target
                            and other.point is None
                            and near
                            and _compatible(other, target)
                        ):
                            target.events.extend(other.events)
                            target.titles.extend(other.titles)
                            target.follow.extend(other.follow)
                            del clusters[i]
            target.events.append(ev)
            target.titles.append(title)
            target.follow.append(follow)
        return [self._combine(c, refs) for c in clusters]

    def _score(
        self, cluster: _Cluster, ev: ClosureEvent, title: frozenset[str], follow: bool
    ) -> tuple[int, int, int] | None:
        """(point rank, day gap, -size) if `ev` belongs to `cluster`, else None; lower wins."""
        point = cluster.point
        if ev.punto_id is not None and point is not None and ev.punto_id != point:
            return None
        rank = 0 if ev.punto_id is not None and ev.punto_id == point else 1
        best: int | None = None
        for other, other_title, other_follow in zip(
            cluster.events, cluster.titles, cluster.follow, strict=True
        ):
            if other.ruta != ev.ruta:
                continue
            gap = abs((ev.fecha - other.fecha).days)
            ok = False
            if (
                follow
                and not other_follow
                and other.tipo_corte != "precaucion"  # a warning is not a closure
                and 0 <= (ev.fecha - other.fecha).days <= (self.follow_days)
            ):
                # schedules, reopenings, works after a closure extend it; without a shared
                # point a follow-up with its own cause needs the same cause family
                located = ev.punto_id is not None and point is not None
                own = ev.causa not in ("otro", "obra")  # "obra" here: works after the closure
                ok = located or not own or family(other.causa) in ("otro", family(ev.causa))
            elif gap <= self.window_days:
                fam_a, fam_b = family(ev.causa), family(other.causa)
                located = ev.punto_id is not None and point is not None
                vague = "otro" in (fam_a, fam_b)
                ok = fam_a == fam_b != "otro" or (
                    vague and (located or self._similar(title, other_title))
                )
            if ok and (best is None or gap < best):
                best = gap
        # ties: the event with more mentions (a follow-up joins the main closure)
        return None if best is None else (rank, best, -len(cluster.events))

    def _similar(self, a: frozenset[str], b: frozenset[str]) -> bool:
        if min(len(a), len(b)) < self.min_tokens:
            return False
        return jaccard(a, b) >= self.min_jaccard

    def _combine(self, cluster: _Cluster, refs: Mapping[str, ArticleRef]) -> ClosureEvent:
        evs = cluster.events
        if len(evs) == 1 and not refs:
            return evs[0].model_copy(
                update={"fecha_inicio": evs[0].fecha, "fecha_fin": evs[0].fecha}
            )
        urls = sorted({u for e in evs for u in e.fuentes})
        outlets = {refs[u].source_id if u in refs else u for u in urls}
        lead = [e for e, f in zip(evs, cluster.follow, strict=True) if not f] or evs
        causes = [e.causa for e in lead if e.causa != "otro"] or [
            e.causa for e in evs if e.causa != "otro"
        ]
        evs = sorted(evs, key=lambda e: (e.fecha, e.evento_id))
        first = evs[0]
        n_medios = len(outlets - self.republishers)
        notas = {e.notas for e in evs if e.notas} | ({REPUBLISHER_NOTE} if n_medios == 0 else set())
        return first.model_copy(
            update={
                "evento_id": hashlib.sha1(  # noqa: S324 — identifier, not security
                    "|".join(
                        [first.fecha.isoformat(), first.ruta, cluster.point or "", *urls]
                    ).encode()
                ).hexdigest()[:16],
                "punto_id": next((e.punto_id for e in evs if e.punto_id), None),
                "km": next((e.km for e in evs if e.km is not None), None),
                "paraje": ", ".join(sorted({x for e in evs for x in e.paraje.split(", ") if x})),
                "causa": max(set(causes), key=lambda c: (causes.count(c), c)) if causes else "otro",
                "tipo_corte": max((e.tipo_corte for e in evs), key=_TIPO.__getitem__),
                "fuentes": urls,
                "fecha": first.fecha,
                "fecha_inicio": first.fecha,
                "fecha_fin": max(e.fecha for e in evs),
                "n_medios": n_medios,
                "metodo": "llm" if any(e.metodo == "llm" for e in evs) else "reglas",
                "confianza": "baja"
                if n_medios == 0
                else max((e.confianza for e in evs), key=_CONFIANZA.__getitem__),
                "notas": "; ".join(sorted(notas)),
                "lado": _side(e.lado for e in evs),
            }
        )


def _side(sides: Iterable[str | None]) -> Lado | None:
    """Most informative side over the merged mentions (AR + CL → ambos)."""
    found = set(sides)
    if "ambos" in found or {"AR", "CL"} <= found:
        return "ambos"
    order: tuple[Lado, ...] = ("CL", "AR", "desconocido")
    return next((lado for lado in order if lado in found), None)
