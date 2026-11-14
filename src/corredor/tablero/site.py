"""Render the static site: one self-contained index.html (+ sw.js), no network at runtime.

Script and style are inlined and allowed by sha256 hashes in a Content-Security-Policy meta
tag with no external origin. The data bundle goes in a `<script type="application/json">`
block with `<`, `>`, `&` escaped, so scraped text can never close the tag; the app reads it
with JSON.parse and renders it with textContent only.
"""

from __future__ import annotations

import base64
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

SRC_DIR = Path("tablero/src")
DIST_DIR = Path("tablero/dist")
SIZE_BUDGET = 5 * 1024 * 1024


def _sha256(text: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'"


def safe_json(data: Any) -> str:
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for ch, esc in (("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026")):
        text = text.replace(ch, esc)
    return text.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def csp(script: str, style: str) -> str:
    return (
        f"default-src 'none'; script-src {_sha256(script)}; style-src {_sha256(style)}; "
        "img-src data:; worker-src 'self'; manifest-src 'none'; base-uri 'none'; "
        "form-action 'none'"
    )


def render(bundle: dict[str, Any], src_dir: Path = SRC_DIR) -> str:
    template = (src_dir / "index.html").read_text(encoding="utf-8")
    script = (src_dir / "app.js").read_text(encoding="utf-8")
    style = (src_dir / "styles.css").read_text(encoding="utf-8")
    return (
        template.replace("{{CSP}}", csp(script, style))
        .replace("{{STYLE}}", style)
        .replace("{{SCRIPT}}", script)
        .replace("{{DATOS}}", safe_json(bundle))
    )


def write_site(bundle: dict[str, Any], dist: Path = DIST_DIR, src_dir: Path = SRC_DIR) -> int:
    """Write dist/ (index.html, sw.js, datos.json) and return its total size in bytes."""
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True)
    (dist / "index.html").write_text(render(bundle, src_dir), encoding="utf-8")
    shutil.copy(src_dir / "sw.js", dist / "sw.js")
    (dist / "datos.json").write_text(safe_json(bundle), encoding="utf-8")
    return sum(p.stat().st_size for p in dist.rglob("*") if p.is_file())
