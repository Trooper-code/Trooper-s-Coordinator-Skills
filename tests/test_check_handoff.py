#!/usr/bin/env python3
"""Tests for templates/scripts/check-handoff.py. Runs in CI; run locally with: python tests/test_check_handoff.py

Builds throwaway repos in a temp folder and checks that a good handoff passes and each kind of problem is caught.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "templates" / "scripts" / "check-handoff.py"

GOOD = """# Test handoff
## Setup
Rules: `AGENTS.md`
## Tool versions
| dotnet | 8.0.1 |
## How it works now
See `docs/research/save.md`. Pattern: `docs/prompts/<x>.md`.
## Where it stops
ok
## In progress
- agent on `docs/prompts/M1-a.md`, report `docs/reports/M1-a.md` on its branch
## Rules
- x
## First thing to do
1. run tests
## Lessons
- x

[Paste Antigravity's latest summary here]

---
"""


def run(handoff_text, make_files=True):
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        (repo / ".git").mkdir()
        (repo / "docs" / "research").mkdir(parents=True)
        (repo / "docs" / "prompts").mkdir()
        if make_files:
            (repo / "AGENTS.md").write_text("x")
            (repo / "docs" / "research" / "save.md").write_text("x")
            (repo / "docs" / "prompts" / "M1-a.md").write_text("x")
        (repo / "docs" / "HANDOFF.md").write_text(handoff_text)
        r = subprocess.run([sys.executable, "-I", str(CHECKER), str(repo / "docs" / "HANDOFF.md")],
                           capture_output=True, text=True)
        return r.returncode, r.stdout


cases = [
    ("good handoff passes", GOOD, True, 0, "OK"),
    ("missing referenced file", GOOD, False, 1, "doesn't exist"),
    ("over line budget", GOOD.replace("- x\n", "- x\n" * 130, 1), True, 1, "budget"),
    ("missing section", GOOD.replace("## Tool versions", "## Versions"), True, 1, "missing section '## Tool versions'"),
    ("pasted summary with its own headings passes",
     GOOD.replace("[Paste Antigravity's latest summary here]",
                  "**Antigravity's M1 summary (unreviewed):**\n## What changed\n- stuff"), True, 0, "OK"),
    ("repeated lesson prints a promote note", GOOD.replace("## Lessons\n- x", "## Lessons\n- tests wrote real logs (x2)"),
     True, 0, "promote it to a rule"),
    ("no summary line", GOOD.replace("[Paste Antigravity's latest summary here]", ""), True, 1, "agent-summary line"),
    ("a lesson mentioning docs/reports/ doesn't count as the summary line",
     GOOD.replace("## Lessons\n- x", "## Lessons\n- read docs/reports/ from the branch")
         .replace("[Paste Antigravity's latest summary here]", ""), True, 1, "agent-summary line"),
    ("markdown links are followed from HANDOFF.md's folder",
     GOOD.replace("## Rules\n- x", "## Rules\n- [save](research/save.md)"), True, 0, "OK"),
    ("markdown link written from the repo root is broken on GitHub",
     GOOD.replace("## Rules\n- x", "## Rules\n- [save](docs/research/save.md)"), True, 1, "doesn't exist"),
    ("repeat marker with trailing punctuation", GOOD.replace("## Lessons\n- x", "## Lessons\n- tests wrote real logs (x2)."),
     True, 0, "promote it to a rule"),
]
failed = 0
for name, text, files, want_code, want_text in cases:
    code, out = run(text, files)
    ok = code == want_code and want_text in out
    print(("PASS" if ok else "FAIL") + f": {name}")
    if not ok:
        failed += 1
        print(f"  exit {code}, output:\n{out}")
sys.exit(1 if failed else 0)
