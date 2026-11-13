"""Release helpers. Only the integration session or the owner runs them.

`main` is protected (PR + CI required), so a release takes two steps:

- `make release BUMP=patch|minor|major` (`release.py bump`): from an up-to-date `main`,
  create `release/vX.Y.Z`, bump pyproject with uv, move the CHANGELOG "Unreleased"
  entries to a dated section, commit "chore(release): vX.Y.Z", push and open a PR. No tag.
  A `.devN` version is finalized instead of bumped (0.1.0.dev0 -> 0.1.0).
- `make tag` (`release.py tag`): after that PR is merged, on an up-to-date `main`, check
  the version is final, create the annotated tag vX.Y.Z and push only the tag, which
  triggers `.github/workflows/release.yml`.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

UNRELEASED = "## [Unreleased]"
_FINAL = re.compile(r"^\d+\.\d+\.\d+$")
_DEV = re.compile(r"\.dev\d+$")
_SECTION = re.compile(r"^## \[", re.MULTILINE)


class ReleaseError(RuntimeError):
    pass


def roll_changelog(text: str, version: str, today: date) -> str:
    """Move the Unreleased body under a new '## [version] - date' heading."""
    start = text.find(UNRELEASED)
    if start == -1:
        raise ReleaseError("CHANGELOG.md has no '## [Unreleased]' section")
    body_start = start + len(UNRELEASED)
    nxt = _SECTION.search(text, body_start)
    body_end = nxt.start() if nxt else len(text)
    body = text[body_start:body_end].strip("\n")
    if not body.strip():
        raise ReleaseError("Unreleased section is empty: nothing to release")
    new_section = f"{UNRELEASED}\n\n## [{version}] - {today.isoformat()}\n\n{body}\n\n"
    return text[:start] + new_section + text[body_end:].lstrip("\n")


def changelog_section(text: str, version: str) -> str:
    """Body of the '## [version]' section (used for the GitHub Release notes)."""
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n", text, re.MULTILINE)
    if not m:
        raise ReleaseError(f"no CHANGELOG section for {version}")
    nxt = _SECTION.search(text, m.end())
    return text[m.end() : nxt.start() if nxt else len(text)].strip() + "\n"


def is_final(version: str) -> bool:
    return bool(_FINAL.match(version))


def bump_arg(current: str, bump: str) -> str:
    """uv `--bump` value: finalize a .devN version, otherwise bump as requested."""
    return "stable" if _DEV.search(current) else bump


def _run(*argv: str) -> str:
    exe = shutil.which(argv[0])
    if exe is None:
        raise ReleaseError(f"{argv[0]} not found")
    out = subprocess.run([exe, *argv[1:]], capture_output=True, text=True, check=False)  # noqa: S603 — fixed argv, no shell
    if out.returncode != 0:
        raise ReleaseError(f"{' '.join(argv)} failed: {out.stderr.strip()}")
    return out.stdout.strip()


def _require_clean_main() -> None:
    if _run("git", "status", "--porcelain"):
        raise ReleaseError("working tree is not clean")
    if _run("git", "rev-parse", "--abbrev-ref", "HEAD") != "main":
        raise ReleaseError("run it from main")
    _run("git", "fetch", "origin", "main", "--tags")
    if _run("git", "rev-parse", "HEAD") != _run("git", "rev-parse", "origin/main"):
        raise ReleaseError("main is not up to date with origin/main (git pull --ff-only)")


def _version() -> str:
    return _run("uv", "version", "--short")


def open_release_pr(bump: str, changelog: Path) -> str:
    _require_clean_main()
    current = _version()
    arg = bump_arg(current, bump)
    version = _run("uv", "version", "--bump", arg, "--dry-run", "--short", "--no-sync")
    branch = f"release/v{version}"
    _run("git", "switch", "-c", branch)
    _run("uv", "version", "--bump", arg, "--no-sync")
    changelog.write_text(
        roll_changelog(changelog.read_text(encoding="utf-8"), version, date.today()),
        encoding="utf-8",
    )
    _run("uv", "lock")
    _run("git", "add", "pyproject.toml", "uv.lock", str(changelog))
    _run("git", "commit", "-m", f"chore(release): v{version}")
    _run("git", "push", "-u", "origin", branch)
    notes = changelog_section(changelog.read_text(encoding="utf-8"), version)
    if shutil.which("gh") is None:
        print(f"gh not found: open a PR from {branch} to main by hand.")
        return version
    body = (
        f"Release v{version} ({current} -> {version}).\n\n{notes}\n"
        "After merging: `git switch main && git pull --ff-only && make tag`."
    )
    url = _run(
        "gh",
        "pr",
        "create",
        "--base",
        "main",
        "--head",
        branch,
        "--title",
        f"chore(release): v{version}",
        "--body",
        body,
        "--label",
        "no-docs",
    )
    print(url)
    return version


def push_tag(changelog: Path) -> str:
    _require_clean_main()
    version = _version()
    if not is_final(version):
        raise ReleaseError(f"version {version} is not final (merge the release PR first)")
    tag = f"v{version}"
    if _run("git", "tag", "--list", tag):
        raise ReleaseError(f"tag {tag} already exists")
    changelog_section(changelog.read_text(encoding="utf-8"), version)
    _run("git", "tag", "-a", tag, "-m", tag)
    _run("git", "push", "origin", f"refs/tags/{tag}")
    return tag


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    rel = sub.add_parser("bump", help="open the release PR")
    rel.add_argument("bump", choices=["patch", "minor", "major"])
    sub.add_parser("tag", help="tag the merged release on main")
    notes = sub.add_parser("notes", help="print a version's CHANGELOG section")
    notes.add_argument("version")
    args = parser.parse_args()
    changelog = Path("CHANGELOG.md")
    try:
        if args.cmd == "bump":
            version = open_release_pr(args.bump, changelog)
            print(f"Release PR for v{version} opened. After merging it run: make tag")
        elif args.cmd == "tag":
            print(f"Pushed {push_tag(changelog)}; release.yml publishes the GitHub Release.")
        else:
            sys.stdout.write(changelog_section(changelog.read_text(encoding="utf-8"), args.version))
    except ReleaseError as exc:
        print(f"release: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
