"""Pipeline orchestration and the `corredor` CLI (typer). User-facing text in Spanish."""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path
from typing import Annotated

import pandas as pd
import typer

from corredor import __version__
from corredor.config import AppConfig, Settings, load_config
from corredor.http import FetchError, PoliteFetcher
from corredor.models import Article, JamaEstado
from corredor.reports import lineage, report_header, write_manifest
from corredor.sources.generic import GenericOptions, build_sources
from corredor.sources.jama import append_jsonl, build_collectors
from corredor.storage.repository import DuckDBRepository

app = typer.Typer(
    help="Corredor Quebrada–Puna: catálogo de cortes y alertas para RN 9 y RN 52.",
    no_args_is_help=True,
    add_completion=False,
)

NOT_READY_EXIT = 2


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=_version_callback, is_eager=True, help="Muestra la versión."
        ),
    ] = False,
) -> None:
    """Corredor Quebrada–Puna."""


def _not_ready(stage: str) -> None:
    typer.echo(f"La etapa '{stage}' todavía no está implementada.", err=True)
    raise typer.Exit(NOT_READY_EXIT)


ConfigOpt = Annotated[Path | None, typer.Option("--config", help="Ruta a config.yaml.")]


@app.command()
def manifest(config: ConfigOpt = None) -> None:
    """Escribe data/manifest.json (versión, commit, SCHEMA_VERSION, hash de fuentes)."""
    settings = Settings()
    cfg = load_config(config or settings.config_path)
    path = write_manifest(settings.data_dir, lineage(cfg))
    typer.echo(f"Manifiesto escrito en {path}")


def build_fetcher(cfg: AppConfig, settings: Settings) -> PoliteFetcher:
    """The single PoliteFetcher of a run (so the robots exemption is logged once)."""
    http = cfg.http
    exempt = [e.host for e in http.robots_exempt_hosts]
    if exempt:
        typer.echo(
            f"robots.txt omitido (ADR 0002) solo para: {', '.join(sorted(exempt))}", err=True
        )
    return PoliteFetcher(
        http.user_agent,
        settings.cache_dir,
        min_interval_s=http.min_interval_s,
        timeout_s=http.timeout_s,
        retries=http.retries,
        robots_ttl_s=http.robots_ttl_h * 3600,
        not_found_ttl_s=http.not_found_ttl_h * 3600,
        robots_exempt_hosts=exempt,
    )


@app.command()
def clima(
    config: ConfigOpt = None,
    hasta: Annotated[
        str | None, typer.Option(help="Última fecha (AAAA-MM-DD); por defecto, hoy.")
    ] = None,
) -> None:
    """Descarga el clima horario de Open-Meteo (2016→hoy) y calcula los antecedentes."""
    from corredor.storage.repository import DuckDBRepository
    from corredor.weather.backfill import fetch_points, grid_report, saved_cells, write_outputs
    from corredor.weather.openmeteo import OpenMeteoClient

    settings = Settings()
    cfg = load_config(config or settings.config_path)
    end = date.fromisoformat(hasta) if hasta else date.today()
    fetcher = build_fetcher(cfg, settings)
    client = OpenMeteoClient(fetcher, settings.data_dir / "clima", cfg.clima)
    repo = DuckDBRepository(settings.db_path)
    try:
        run = fetch_points(client, cfg.puntos, cfg.clima.desde, end, repo)
    finally:
        repo.close()
        fetcher.close()
    paths = write_outputs(run, settings.data_dir / "clima")
    report = Path("reports") / "clima_grilla.md"
    report.parent.mkdir(exist_ok=True)
    report.write_text(
        grid_report(
            saved_cells(settings.data_dir / "clima", [p.id for p in cfg.puntos]),
            lineage(cfg),
            cfg.clima.modelo_historico,
        ),
        encoding="utf-8",
    )
    used = client.ledger.used_today()
    typer.echo(
        f"Clima: {len(run.done)}/{len(cfg.puntos)} puntos, {run.days} días en clima_diario; "
        f"{report} y {len(paths)} archivos en {settings.data_dir / 'clima'}. "
        f"Llamadas Open-Meteo hoy: {used:.1f}/{cfg.clima.max_llamadas_diarias:.0f}."
    )
    if run.error:
        typer.echo(
            f"Clima incompleto ({run.error}). Lo descargado quedó en caché: "
            "volvé a correr `make clima` (mañana, si se llegó al tope diario).",
            err=True,
        )
        raise typer.Exit(1)


@app.command()
def recolectar(
    config: ConfigOpt = None,
    fuente: Annotated[
        list[str] | None,
        typer.Option("--fuente", help="Id de fuente (repetible). Por defecto, todas las activas."),
    ] = None,
    muestra: Annotated[
        bool,
        typer.Option(
            "--muestra/--completo",
            help="Sitemaps: solo los meses de backfill.muestra_sitemaps (por defecto).",
        ),
    ] = True,
    lote: Annotated[int, typer.Option(help="Artículos por escritura en DuckDB.")] = 200,
) -> None:
    """Recolecta metadatos de artículos (fuentes genéricas y custom) y los guarda en `articulos`."""
    settings = Settings()
    cfg = load_config(config or settings.config_path)
    options = GenericOptions(
        checkpoint_dir=settings.data_dir / "checkpoints",
        max_requests=cfg.backfill.max_requests_per_run,
        sample_months=tuple(cfg.backfill.muestra_sitemaps) if muestra else None,
    )
    fetcher = build_fetcher(cfg, settings)
    repo = DuckDBRepository(settings.db_path)
    try:
        sources = build_sources(cfg.fuentes, fetcher, options, only=fuente)
        if not sources:
            typer.echo("No hay fuentes activas para recolectar.", err=True)
            raise typer.Exit(1)
        failed: list[str] = []
        for source in sources:
            typer.echo(f"→ {source.source_id}")
            batch: list[Article] = []
            total = 0
            failure: str | None = None
            try:
                for article in source.list_articles(cfg.backfill.desde):
                    batch.append(article)
                    if len(batch) >= lote:
                        total += repo.upsert("articulos", batch)
                        batch = []
            except FetchError as exc:
                failure = f"{type(exc).__name__}: {exc}"
            finally:
                # Checkpoints are written as units finish: persist what they yielded first.
                total += repo.upsert("articulos", batch)
            stats = getattr(source, "stats", None)
            summary = stats.as_dict() if stats is not None else {}
            if failure is not None:
                failed.append(source.source_id)
                summary["errors"] = [*summary.get("errors", []), failure]
            out = settings.data_dir / "recoleccion" / f"{source.source_id}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
            typer.echo(
                f"  {total} artículos guardados; listados: {summary.get('raw', '?')}, "
                f"seleccionados: {summary.get('selected', '?')}, "
                f"requests: {summary.get('requests', '?')}, "
                f"errores: {len(summary.get('errors', []))}"
                + (" (se alcanzó el tope de requests por corrida)" if summary.get("capped") else "")
            )
            if failure is not None:
                typer.echo(f"  fuente interrumpida: {failure}", err=True)
        if failed:
            typer.echo(f"Fuentes interrumpidas: {', '.join(failed)}", err=True)
            raise typer.Exit(1)
    finally:
        repo.close()
        fetcher.close()


REPORTS_DIR = Path("reports")
REVIEW_CSV = REPORTS_DIR / "revision_manual.csv"
JAMA_JSONL = Path("snapshots") / "jama_estado.jsonl"


def _load_jsonl(path: Path) -> list[JamaEstado]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(JamaEstado.model_validate_json(line))
    return rows


@app.command()
def datos(
    config: ConfigOpt = None,
    jama: Annotated[
        Path | None,
        typer.Option(help="JSONL de la rama data-snapshots (por defecto data/snapshots/…)."),
    ] = None,
) -> None:
    """Extrae y deduplica eventos de `articulos`, carga puntos y Jama, exporta Parquet.

    Sin red: usa lo que dejaron `corredor recolectar`, `corredor clima` y el JSONL de Jama.
    """
    from corredor.catalog import build_events, frame_to_articles
    from corredor.extraction.dedup import EventDeduplicator
    from corredor.extraction.rules import RuleBasedExtractor

    settings = Settings()
    cfg = load_config(config or settings.config_path)
    if settings.llm_api_key is not None:
        typer.echo(
            "LLM_API_KEY está definida, pero todavía no hay proveedor de LLM configurado: "
            "se usan solo las reglas.",
            err=True,
        )
    repo = DuckDBRepository(settings.db_path)
    try:
        repo.upsert("puntos", cfg.puntos)
        jama_path = jama or settings.data_dir / JAMA_JSONL
        n_jama = repo.upsert("jama_estado", _load_jsonl(jama_path)) if jama_path.exists() else 0
        articles = frame_to_articles(repo.read("articulos"))
        republishers = frozenset(s.id for s in cfg.fuentes if s.republica)
        events, raw = build_events(
            articles, [RuleBasedExtractor(cfg.puntos)], EventDeduplicator(2, republishers)
        )
        repo.replace("eventos", events)
        paths = repo.export_parquet(settings.data_dir / "parquet")
    finally:
        repo.close()
    typer.echo(
        f"Datos: {len(articles)} artículos → {raw} menciones → {len(events)} eventos; "
        f"{n_jama} snapshots de Jama ({'sin archivo' if not n_jama else jama_path}); "
        f"{len(paths)} tablas en {settings.data_dir / 'parquet'}."
    )


def _features(settings: Settings) -> pd.DataFrame:
    path = settings.data_dir / "clima" / "antecedentes.parquet"
    if not path.exists():
        typer.echo(f"Falta {path}: corré `make clima` primero.", err=True)
        raise typer.Exit(1)
    return pd.read_parquet(path)


@app.command()
def calibrar(config: ConfigOpt = None) -> None:
    """Calibra umbrales por causa y escribe reports/validacion.md."""
    from corredor.calibration.report import section
    from corredor.calibration.thresholds import ThresholdCalibrator
    from corredor.catalog import article_refs, frame_to_events, stable_sources

    settings = Settings()
    cfg = load_config(config or settings.config_path)
    repo = DuckDBRepository(settings.db_path)
    try:
        events = frame_to_events(repo.read("eventos"))
        refs = article_refs(repo.read("articulos"))
    finally:
        repo.close()
    features = _features(settings)
    stable = stable_sources(cfg)
    stable_events = [
        e for e in events if {refs[u].source_id for u in e.fuentes if u in refs} & stable
    ]
    cal = ThresholdCalibrator()
    text = (
        report_header("Validación de umbrales", lineage(cfg))
        + (
            "Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. "
            "Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba "
            "2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = "
            "día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia "
            "local (ver docs/DATOS.md): por eso cada variable va también como percentil de "
            "su celda en la misma estación. Cada sección trae también la variante con aluvión y "
            'crecida juntos como una sola causa "lluvia". Junto a cada número va n = días-evento '
            "(punto, fecha) del período en que se basa; en prueba, n < 10 se marca "
            '"muestra chica". Vos elegís la regla final.\n\n'
            f"Fuentes estables (archivo desde ≤ {cfg.backfill.desde}): "
            f"{', '.join(sorted(stable))}.\n\n"
        )
        + section("Todas las fuentes", cal, events, features)
        + "\n"
        + section("Solo fuentes estables", cal, stable_events, features)
    )
    out = REPORTS_DIR / "validacion.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    typer.echo(f"Calibración: {len(events)} eventos ({len(stable_events)} estables) → {out}")


@app.command()
def precision(
    config: ConfigOpt = None,
    archivo: Annotated[Path, typer.Option(help="CSV etiquetado.")] = REVIEW_CSV,
) -> None:
    """Lee reports/revision_manual.csv y reporta la precisión por campo."""
    from corredor.catalog import precision_report

    if not archivo.exists():
        typer.echo(f"Falta {archivo}: corré `make reporte` y etiquetalo.", err=True)
        raise typer.Exit(1)
    settings = Settings()
    cfg = load_config(config or settings.config_path)
    out = REPORTS_DIR / "precision.md"
    out.write_text(
        precision_report(archivo, report_header("Precisión de la extracción", lineage(cfg))),
        encoding="utf-8",
    )
    typer.echo(f"Precisión → {out}")


@app.command()
def reporte(config: ConfigOpt = None) -> None:
    """Genera reports/calidad_catalogo.md y reports/revision_manual.csv."""
    from corredor.catalog import article_refs, frame_to_events, quality_report, write_review

    settings = Settings()
    cfg = load_config(config or settings.config_path)
    repo = DuckDBRepository(settings.db_path)
    try:
        articles = repo.read("articulos")
        events = frame_to_events(repo.read("eventos"))
    finally:
        repo.close()
    REPORTS_DIR.mkdir(exist_ok=True)
    out = REPORTS_DIR / "calidad_catalogo.md"
    out.write_text(
        quality_report(cfg, articles, events, report_header("Calidad del catálogo", lineage(cfg))),
        encoding="utf-8",
    )
    wrote = write_review(events, article_refs(articles), REVIEW_CSV)
    typer.echo(
        f"Reporte → {out}; "
        + (f"{REVIEW_CSV} nuevo" if wrote else f"{REVIEW_CSV} ya etiquetado, no se pisa")
    )


GEO_DIR = Path("assets/geo")
GEO_REPORT = Path("reports/geo_verificacion.md")
OVERPASS_TIMEOUT_S = 120.0


@app.command()
def geo(
    config: ConfigOpt = None,
    salida: Annotated[Path, typer.Option(help="Carpeta de los GeoJSON.")] = GEO_DIR,
    informe: Annotated[Path, typer.Option(help="Informe de verificación.")] = GEO_REPORT,
) -> None:
    """Exporta RN 9, RN 52 y el Tren Solar desde OSM y verifica los puntos críticos."""
    from corredor.geo.points import CriticalPointRegistry, verification_report
    from corredor.geo.routes import ATTRIBUTION, LICENSE, OverpassExporter, write_geojson

    settings = Settings()
    cfg = load_config(config or settings.config_path)
    fetcher = PoliteFetcher(
        cfg.http.user_agent,
        settings.cache_dir,
        min_interval_s=cfg.http.min_interval_s,
        timeout_s=max(cfg.http.timeout_s, OVERPASS_TIMEOUT_S),
        retries=cfg.http.retries,
    )
    try:
        exporter = OverpassExporter(fetcher)
        data = exporter.build()
        registry = CriticalPointRegistry(cfg.puntos)
        checks = registry.verify(exporter.client.objects(registry.osm_refs()), data.routes)
    finally:
        fetcher.close()
    paths = write_geojson(data, salida, registry.all())
    body = verification_report(checks, cfg.puntos)
    informe.parent.mkdir(parents=True, exist_ok=True)
    informe.write_text(
        report_header("Verificación de puntos críticos (OpenStreetMap)", lineage(cfg))
        + body
        + f"\nDatos: {ATTRIBUTION}, licencia {LICENSE}.\n",
        encoding="utf-8",
    )
    for path in [*paths, informe]:
        typer.echo(f"Escrito {path}")
    if "**no**" in body or any(c.order_problem for c in checks):
        typer.echo(
            "config.yaml difiere de OSM o tiene puntos fuera de orden: revisá el informe.",
            err=True,
        )
        raise typer.Exit(1)


DEFAULT_JAMA_OUT = Path("snapshots/jama_estado.jsonl")


@app.command("snapshot-jama")
def snapshot_jama(
    config: ConfigOpt = None,
    salida: Annotated[
        Path, typer.Option("--salida", help="Archivo JSONL al que se agregan las líneas.")
    ] = DEFAULT_JAMA_OUT,
) -> None:
    """Guarda el estado actual del Paso de Jama en snapshots/jama_estado.jsonl.

    Una request por fuente; si una fuente falla se guarda la línea con `error` y el
    comando termina igual con código 0.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    settings = Settings()
    cfg = load_config(config or settings.config_path)
    fetcher = PoliteFetcher(
        cfg.http.user_agent,
        settings.cache_dir,
        min_interval_s=cfg.http.min_interval_s,
        timeout_s=cfg.http.timeout_s,
        retries=cfg.http.retries,
        robots_ttl_s=cfg.http.robots_ttl_h * 3600,
        not_found_ttl_s=cfg.http.not_found_ttl_h * 3600,
    )
    try:
        rows = [collector.snapshot() for collector in build_collectors(cfg.fuentes, fetcher)]
    finally:
        fetcher.close()
    if not rows:
        typer.echo("No hay fuentes de snapshot de Jama habilitadas en la configuración.", err=True)
        raise typer.Exit(1)
    append_jsonl(salida, rows)
    for row in rows:
        estado = f"error: {row.error}" if row.error else "ok"
        typer.echo(f"{row.fuente} {row.fetched_at.isoformat()} {estado}")
    typer.echo(f"{len(rows)} línea(s) agregada(s) a {salida}")


if __name__ == "__main__":  # pragma: no cover
    app()
