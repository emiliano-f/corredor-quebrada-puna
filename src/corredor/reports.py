"""Reports (markdown) and data lineage (manifest + report header)."""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel

from corredor import __version__
from corredor.config import AppConfig
from corredor.models import SCHEMA_VERSION


class Lineage(BaseModel):
    version: str
    git_commit: str
    schema_version: int
    sources_hash: str
    generated_at: datetime


def git_commit(repo_dir: Path | None = None) -> str:
    git = shutil.which("git")
    if git is None:
        return "unknown"
    try:
        out = subprocess.run(  # noqa: S603 — fixed argv, no shell
            [git, "rev-parse", "--short", "HEAD"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return "unknown"
    return out.stdout.strip() or "unknown"


def lineage(config: AppConfig, repo_dir: Path | None = None) -> Lineage:
    return Lineage(
        version=__version__,
        git_commit=git_commit(repo_dir),
        schema_version=SCHEMA_VERSION,
        sources_hash=config.sources_hash(),
        generated_at=datetime.now(tz=UTC),
    )


def write_manifest(data_dir: Path, info: Lineage) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "manifest.json"
    path.write_text(
        json.dumps(info.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def report_header(title: str, info: Lineage) -> str:
    """Header every generated report starts with (Spanish, user-facing)."""
    return (
        f"# {title}\n\n"
        f"> Generado: {info.generated_at:%Y-%m-%d %H:%M} UTC · versión `{info.version}` · "
        f"commit `{info.git_commit}` · SCHEMA_VERSION {info.schema_version} · "
        f"fuentes `{info.sources_hash}`\n\n"
    )
