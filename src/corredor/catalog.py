"""Event catalog: extraction + dedup over `articulos`, and the quality/review reports.

Every number in the reports is computed here from the persisted tables (articulos,
eventos); nothing is typed by hand.
"""

from __future__ import annotations

import csv
import random
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from datetime import timedelta
from pathlib import Path
from typing import Final

import pandas as pd

from corredor.config import AppConfig
from corredor.extraction.base import EventExtractor
from corredor.extraction.dedup import ArticleRef, EventDeduplicator
from corredor.models import Article, ClosureEvent, SourceConfig

SEED = 42
SAMPLE_SIZE = 20
# Stratified manual-review sample: events per stratum (other causes pooled in "otras").
STRATA: Final[dict[str, int]] = {"aluvion": 8, "crecida": 8, "nieve": 8, "otras": 6}
EVENT_COLUMNS = (
    "evento_id", "fecha", "ruta", "punto_id", "km", "paraje", "causa", "tipo_corte",
    "n_medios", "metodo", "confianza",
)  # fmt: skip
REVIEW_COLUMNS = (
    "estrato", *EVENT_COLUMNS, "titular", "url", "ok_fecha", "ok_punto", "ok_causa",
    "comentario",
)  # fmt: skip
LABELS = ("ok_fecha", "ok_punto", "ok_causa")
YES = frozenset({"1", "si", "sí", "s", "ok", "true", "x", "y", "yes"})
NO = frozenset({"0", "no", "n", "false", "mal"})


def stable_sources(cfg: AppConfig) -> frozenset[str]:
    """Outlets with archive since 2016-01-01 or earlier (HANDOFF §3.4 item 17)."""
    return frozenset(
        s.id
        for s in cfg.fuentes
        if s.enabled and s.archivo_desde and s.archivo_desde <= cfg.backfill.desde
    )


def article_refs(articles: pd.DataFrame) -> dict[str, ArticleRef]:
    if articles.empty:
        return {}
    return {
        str(r.url): ArticleRef(source_id=str(r.source_id), titular=str(r.titular))
        for r in articles.itertuples()
    }


def frame_to_articles(frame: pd.DataFrame) -> list[Article]:
    if frame.empty:
        return []
    records = frame.to_dict(orient="records")
    return [Article.model_validate({k: _plain(v) for k, v in r.items()}) for r in records]


def frame_to_events(frame: pd.DataFrame) -> list[ClosureEvent]:
    if frame.empty:
        return []
    records = frame.to_dict(orient="records")
    return [ClosureEvent.model_validate({k: _plain(v) for k, v in r.items()}) for r in records]


def _plain(value: object) -> object:
    if hasattr(value, "tolist"):
        return value.tolist()  # numpy arrays (list columns)
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    return value


def build_events(
    articles: Sequence[Article],
    extractors: Sequence[EventExtractor],
    dedup: EventDeduplicator,
) -> tuple[list[ClosureEvent], int]:
    """(merged events, raw event count). The first extractor that finds an event wins."""
    raw: list[ClosureEvent] = []
    for article in articles:
        for extractor in extractors:
            found = extractor.extract(article)
            if found:
                raw.extend(found)
                break
    refs = {a.url: ArticleRef(a.source_id, a.titular) for a in articles}
    return dedup.merge(raw, refs), len(raw)


def _table(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def _counts(counter: Mapping[object, int], label: str) -> str:
    rows = sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))
    return _table([label, "eventos"], [(k if k is not None else "(sin punto)", v) for k, v in rows])


def _event_sources(ev: ClosureEvent, refs: Mapping[str, ArticleRef]) -> set[str]:
    return {refs[u].source_id for u in ev.fuentes if u in refs}


def quality_report(
    cfg: AppConfig, articles: pd.DataFrame, events: Sequence[ClosureEvent], header: str
) -> str:
    refs = article_refs(articles)
    by_id: dict[str, SourceConfig] = {s.id: s for s in cfg.fuentes}
    stable = stable_sources(cfg)
    local = {s.id for s in cfg.fuentes if s.local}
    sitemap_ids = {s.id for s in cfg.fuentes if s.metodo == "sitemap"}
    wp_ids = {s.id for s in cfg.fuentes if s.metodo == "wordpress_api"}
    out = [header]
    raw = sum(len(e.fuentes) for e in events)
    out.append(
        "Conteos calculados desde las tablas `articulos` y `eventos`. Un artículo aporta como "
        "máximo un evento; el dedup junta artículos del mismo corte (ver docs/DATOS.md).\n\n"
    )
    out.append(f"- Artículos: **{len(articles)}**\n- Eventos (tras dedup): **{len(events)}**\n")
    ratio = f"{raw / len(events):.2f}" if events else "—"
    out.append(
        f"- Menciones antes del dedup: **{raw}** → ratio de dedup **{ratio}** menciones/evento\n"
    )
    one = sum(1 for e in events if e.n_medios <= 1)
    out.append(f"- Eventos con 1 medio: **{one}**; con 2+ medios: **{len(events) - one}**\n")
    metodo = Counter(e.metodo for e in events)
    out.append(
        f"- Método: reglas **{metodo.get('reglas', 0)}**, LLM **{metodo.get('llm', 0)}**\n\n"
    )

    out.append("## Por fuente\n\n")
    art_by = Counter(articles["source_id"]) if not articles.empty else Counter()
    ev_by: Counter[str] = Counter()
    for e in events:
        ev_by.update(_event_sources(e, refs))
    rows = []
    for sid in sorted(set(art_by) | set(ev_by)):
        src = by_id.get(sid)
        tags = [t for t, on in (("estable", sid in stable), ("local", sid in local),
                                ("republica", bool(src and src.republica))) if on]  # fmt: skip
        rows.append((sid, src.metodo if src else "?", ", ".join(tags), art_by[sid], ev_by[sid]))
    out.append(_table(["fuente", "método", "marcas", "artículos", "eventos"], rows))
    if not articles.empty and "filtro_slug" in articles:
        filt = Counter(str(v) for v in articles["filtro_slug"].dropna())
        only_c = sum(
            1
            for e in events
            if e.fuentes
            and all(u in refs and _filtro(articles, u) == "C_solo_ruta" for u in e.fuentes)
        )
        share = f"{only_c / len(events):.1%}" if events else "—"
        out.append(
            f"\nSitemaps: artículos por filtro B **{filt.get('B', 0)}**, C_solo_ruta "
            f"**{filt.get('C_solo_ruta', 0)}**. Eventos que vienen **solo** de páginas "
            f"C_solo_ruta: **{only_c}** ({share}). Decisión (Emiliano, 2026-11-13): se mantiene el "
            "filtro C aunque el aporte sea < 5 %; la regla del 5 % era por costo de descarga, y "
            "las páginas quedan en caché y el incremento nocturno es de un mes.\n"
        )

    out.append("\n## Por año (fuentes estables vs nuevas)\n\n")
    years: dict[int, list[int]] = {}
    for e in events:
        row = years.setdefault(e.fecha.year, [0, 0])
        row[0 if _event_sources(e, refs) & stable else 1] += 1
    out.append(_table(["año", "con fuente estable", "solo fuentes nuevas"],
                      [(y, *v) for y, v in sorted(years.items())]))  # fmt: skip
    out.append("\n## Por ruta\n\n" + _counts(Counter(e.ruta for e in events), "ruta"))
    out.append("\n## Por causa\n\n" + _counts(Counter(e.causa for e in events), "causa"))
    out.append("\n## Por punto crítico\n\n" + _counts(Counter(e.punto_id for e in events), "punto"))

    only_local = [e for e in events if (s := _event_sources(e, refs)) and s <= local]
    local_names = ", ".join(sorted(local)) or "ninguno"
    out.append(
        f"\n## Solo medios locales chicos\n\n{len(only_local)} eventos aparecen solo en "
        f"medios marcados `local: true` ({local_names}).\n"
    )

    out.append("\n## Chequeo de recall (WordPress vs sitemaps)\n\n")
    wp_events = [e for e in events if _event_sources(e, refs) & wp_ids]
    sm_dates = {(e.ruta, e.fecha) for e in events if _event_sources(e, refs) & sitemap_ids}
    window = range(-2, 3)
    unmatched = [
        e for e in wp_events
        if not any((e.ruta, e.fecha + timedelta(days=k)) in sm_dates for k in window)
    ]  # fmt: skip
    out.append(
        f"{len(unmatched)} de {len(wp_events)} eventos de medios WordPress no tienen ningún "
        "evento de medios de sitemap en la misma ruta ±2 días. Los sitemaps hoy cubren solo "
        "los meses de muestra, así que este número mide sobre todo esa diferencia de cobertura.\n"
    )

    out.append(f"\n## Muestra aleatoria de {SAMPLE_SIZE} eventos (semilla {SEED})\n\n")
    sample = random.Random(SEED).sample(  # noqa: S311 — reproducible sample
        list(events), min(SAMPLE_SIZE, len(events))
    )
    out.append(_table(
        ["fecha", "ruta", "punto", "causa", "medios", "titular"],
        [(e.fecha, e.ruta, e.punto_id or "—", e.causa, e.n_medios, _link(e, refs))
         for e in sorted(sample, key=lambda e: (e.fecha, e.evento_id))],
    ))  # fmt: skip
    return "".join(out)


def _filtro(articles: pd.DataFrame, url: str) -> str | None:
    match = articles.loc[articles["url"] == url, "filtro_slug"]
    return None if match.empty or pd.isna(match.iloc[0]) else str(match.iloc[0])


def _link(ev: ClosureEvent, refs: Mapping[str, ArticleRef]) -> str:
    url = ev.fuentes[0]
    title = refs[url].titular if url in refs else url
    return f"[{title.replace('|', '/').strip()}]({url})"


def write_review(
    events: Sequence[ClosureEvent], refs: Mapping[str, ArticleRef], path: Path
) -> bool:
    """Write the manual-review CSV unless one already has labels (never overwrite them)."""
    if path.exists() and any(read_labels(path)[label] for label in LABELS):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        for stratum, e in review_sample(events):
            url = e.fuentes[0]
            row = {
                "estrato": stratum,
                **{k: getattr(e, k) for k in EVENT_COLUMNS},
                "titular": refs[url].titular if url in refs else "",
                "url": url,
            }
            writer.writerow({k: _cell(v) for k, v in row.items()})
    return True


def stratum_of(causa: str) -> str:
    return causa if causa in STRATA else "otras"


def review_sample(events: Sequence[ClosureEvent]) -> list[tuple[str, ClosureEvent]]:
    """STRATA[s] random events per stratum (fixed seed; fewer if the stratum is smaller)."""
    rng = random.Random(SEED)  # noqa: S311 — reproducible sample
    ordered = sorted(events, key=lambda e: (e.fecha, e.evento_id))
    out: list[tuple[str, ClosureEvent]] = []
    for stratum, size in STRATA.items():
        pool = [e for e in ordered if stratum_of(e.causa) == stratum]
        picked = rng.sample(pool, min(size, len(pool)))
        out += [(stratum, e) for e in sorted(picked, key=lambda e: (e.fecha, e.evento_id))]
    return out


def _cell(value: object) -> object:
    """Neutralise spreadsheet formulas in untrusted text (CSV injection)."""
    if isinstance(value, str) and value[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + value
    return value


def read_labels(path: Path, stratum: str | None = None) -> dict[str, list[bool]]:
    """Labels per field; only rows of `stratum` when given."""
    labels: dict[str, list[bool]] = {label: [] for label in LABELS}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if stratum is not None and (row.get("estrato") or "") != stratum:
                continue
            for label in LABELS:
                value = (row.get(label) or "").strip().lower()
                if value in YES:
                    labels[label].append(True)
                elif value in NO:
                    labels[label].append(False)
    return labels


def _precision(vals: Sequence[bool]) -> str:
    return f"{sum(vals) / len(vals):.0%} (n={len(vals)})" if vals else "— (n=0)"


def precision_report(path: Path, header: str) -> str:
    rows = []
    for stratum in (None, *STRATA):
        labels = read_labels(path, stratum)
        rows.append((stratum or "todos", *(_precision(labels[label]) for label in LABELS)))
    sizes = ", ".join(f"{s} {n}" for s, n in STRATA.items())
    return (
        header + f"Etiquetas leídas de `{path}` (valores sí: 1/si/ok/x; no: 0/no/mal; vacío = sin "
        f"etiquetar). Muestra estratificada por causa (semilla {SEED}: {sizes}); n = filas "
        "etiquetadas en ese campo. Precisión = correctos / etiquetados.\n\n"
        + _table(["estrato", *(label.removeprefix("ok_") for label in LABELS)], rows)
    )
