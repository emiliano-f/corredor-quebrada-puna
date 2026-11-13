"""Docs guard: fail a PR whose code changes are not reflected in the docs.

Rules (compared against the PR base, default origin/main):
- src/corredor/sources/** changed  → docs/SCRAPING.md or docs/FUENTES.md must change;
- src/corredor/models.py or src/corredor/storage/** changed → docs/DATOS.md must change;
- any change at all → CHANGELOG.md must change.
Skipped when the PR has the label `no-docs` (env PR_LABELS, comma-separated).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

SKIP_LABEL = "no-docs"


@dataclass(frozen=True)
class Rule:
    name: str
    triggers: tuple[str, ...]
    required_any: tuple[str, ...]


RULES: tuple[Rule, ...] = (
    Rule(
        "sources",
        ("src/corredor/sources/",),
        ("docs/SCRAPING.md", "docs/FUENTES.md"),
    ),
    Rule(
        "data model",
        ("src/corredor/models.py", "src/corredor/storage/"),
        ("docs/DATOS.md",),
    ),
)


def _matches(path: str, prefix: str) -> bool:
    return path == prefix or (prefix.endswith("/") and path.startswith(prefix))


def check(changed: Iterable[str]) -> list[str]:
    """Return human-readable errors for the set of changed paths (empty = OK)."""
    files = {c.strip() for c in changed if c.strip()}
    if not files:
        return []
    errors = []
    for rule in RULES:
        hit = sorted(f for f in files if any(_matches(f, t) for t in rule.triggers))
        if hit and not files.intersection(rule.required_any):
            errors.append(
                f"{rule.name}: {', '.join(hit)} changed but none of "
                f"{', '.join(rule.required_any)} was updated"
            )
    if "CHANGELOG.md" not in files:
        errors.append('CHANGELOG.md: add a line under "## [Unreleased]"')
    return errors


def has_skip_label(labels: str | None) -> bool:
    return SKIP_LABEL in {x.strip() for x in (labels or "").split(",")}


def changed_files(base: str) -> list[str]:
    git = shutil.which("git")
    if git is None:
        raise SystemExit("git not found")
    out = subprocess.run(  # noqa: S603 — fixed argv, no shell
        [git, "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.splitlines()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=os.environ.get("DOCS_CHECK_BASE", "origin/main"))
    args = parser.parse_args(argv)
    if has_skip_label(os.environ.get("PR_LABELS")):
        print(f"docs-check: skipped (label {SKIP_LABEL})")
        return 0
    errors = check(changed_files(args.base))
    for err in errors:
        print(f"docs-check: {err}", file=sys.stderr)
    if not errors:
        print("docs-check: OK")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
