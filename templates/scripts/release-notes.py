#!/usr/bin/env python3
"""Prints the CHANGELOG.md section for one release, to use as its GitHub Release notes.

Copy this file to scripts/release-notes.py in your project, then run:

    python scripts/release-notes.py v1.4.0               # prints the notes
    python scripts/release-notes.py v1.4.0 > notes.md    # saves them to a file

It finds the heading for that version in CHANGELOG.md ("## v1.4.0", "## 1.4.0" or "## [1.4.0] - 2026-11-17"),
prints everything up to the next "## " heading, and adds a "Full Changelog" link when it can work out the
previous version and the GitHub repo.

The release workflow in templates/github/release.yml runs this automatically when you push a tag.

Exit code 0 = notes printed, 1 = no section for that version (the message says how to add one).
Only uses the Python standard library.
"""
import os
import re
import sys
from pathlib import Path


def norm(v: str) -> str:
    """'v1.4.0', '1.4.0' and '[1.4.0]' all become '1.4.0'."""
    return v.strip().strip("[]").lstrip("vV")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/release-notes.py <version>   e.g. v1.4.0")
        return 1
    want = norm(sys.argv[1])
    path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("CHANGELOG.md")
    if not path.exists():
        print(f"Can't find {path}. Run this from the repo root, or pass the path as a second argument.")
        return 1

    lines = path.read_text(encoding="utf-8").splitlines()
    heading = re.compile(r"^##\s+\[?v?([0-9][^\]\s]*)\]?")
    versions = [(i, norm(m.group(1))) for i, l in enumerate(lines) if (m := heading.match(l))]

    for n, (i, v) in enumerate(versions):
        if v != want:
            continue
        # Body: up to the next "## " heading of any kind.
        end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
        body = "\n".join(lines[i + 1:end]).strip()
        if not body:
            print(f"The section for {sys.argv[1]} in {path} is empty. Add what changed under its heading.")
            return 1
        prev = versions[n + 1][1] if n + 1 < len(versions) else None
        repo = os.environ.get("GITHUB_REPOSITORY")  # set automatically inside GitHub Actions
        tag = sys.argv[1]
        prefix = "v" if tag.lower().startswith("v") else ""
        if prev and repo:
            body += f"\n\n**Full Changelog**: https://github.com/{repo}/compare/{prefix}{prev}...{tag}"
        print(body)
        return 0

    print(
        f"No section for {sys.argv[1]} in {path}. Add a heading like '## {sys.argv[1]}' with what changed, "
        "commit it, then tag again."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
