"""Identity guard (pre-commit): reject commits whose author or committer email does not
end in @users.noreply.github.com. Workflow commits by github-actions[bot] do not run
pre-commit, so they are not affected.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys

NOREPLY_SUFFIX = "@users.noreply.github.com"
_IDENT = re.compile(r"^(?P<name>.*?)\s*<(?P<email>[^>]*)>")


def email_of(ident: str) -> str | None:
    m = _IDENT.match(ident.strip())
    return m.group("email").strip() if m else None


def check_ident(role: str, ident: str) -> str | None:
    email = email_of(ident)
    if email is None:
        return f"{role}: cannot parse identity"
    if not email.lower().endswith(NOREPLY_SUFFIX):
        return f"{role} email must end in {NOREPLY_SUFFIX} (got a non-noreply address)"
    return None


def git_var(name: str) -> str:
    git = shutil.which("git")
    if git is None:
        raise SystemExit("git not found")
    out = subprocess.run(  # noqa: S603 — fixed argv, no shell
        [git, "var", name], capture_output=True, text=True, check=True
    )
    return out.stdout


def main() -> int:
    errors = [
        err
        for role, var in (("author", "GIT_AUTHOR_IDENT"), ("committer", "GIT_COMMITTER_IDENT"))
        if (err := check_ident(role, git_var(var))) is not None
    ]
    for err in errors:
        print(f"identity-guard: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
