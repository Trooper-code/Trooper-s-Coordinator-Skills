#!/usr/bin/env python3
"""Tests for every script in templates/scripts/ (except check-handoff.py, see test_check_handoff.py).

Run locally with:  python tests/test_scripts.py
CI runs it on every push. Each test builds a throwaway repo in a temp folder, runs a script against it, and checks
the exit code and the message. Only uses the Python standard library (plus git, for the publish check).
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "templates" / "scripts"


def run(script: str, *args: str, cwd: Path, env: dict | None = None) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *args], cwd=cwd, capture_output=True,
                       text=True, env={**os.environ, **(env or {})})
    return r.returncode, r.stdout + r.stderr


def write(base: Path, rel: str, content: str | bytes = "x") -> Path:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        p.write_bytes(content)
    else:
        p.write_text(textwrap.dedent(content).lstrip("\n"))
    return p


class Temp(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True,
                       env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


# ---------------------------------------------------------------- release-notes.py
CHANGELOG = """
# Changelog

## Unreleased
- not yet

## v1.4.0
- Release mode
- Copyright guard

## v1.3.0
- AGENTS.md
"""


class ReleaseNotes(Temp):
    def test_prints_section_with_compare_link(self):
        write(self.repo, "CHANGELOG.md", CHANGELOG)
        code, out = run("release-notes.py", "v1.4.0", cwd=self.repo, env={"GITHUB_REPOSITORY": "me/repo"})
        self.assertEqual(code, 0, out)
        self.assertIn("- Release mode", out)
        self.assertNotIn("AGENTS.md", out)
        self.assertNotIn("not yet", out)
        self.assertIn("compare/v1.3.0...v1.4.0", out)

    def test_oldest_release_has_no_compare_link(self):
        write(self.repo, "CHANGELOG.md", CHANGELOG)
        code, out = run("release-notes.py", "v1.3.0", cwd=self.repo, env={"GITHUB_REPOSITORY": "me/repo"})
        self.assertEqual(code, 0, out)
        self.assertIn("AGENTS.md", out)
        self.assertNotIn("compare", out)

    def test_missing_version_explains_fix(self):
        write(self.repo, "CHANGELOG.md", CHANGELOG)
        code, out = run("release-notes.py", "v9.9.9", cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("Add a heading like '## v9.9.9'", out)

    def test_bracket_style_headings(self):
        write(self.repo, "CHANGELOG.md", "## [2.0.0] - 2026-11-17\n- big\n\n## [1.0.0] - 2026-01-01\n- first\n")
        code, out = run("release-notes.py", "2.0.0", cwd=self.repo)
        self.assertEqual(code, 0, out)
        self.assertIn("- big", out)


# ---------------------------------------------------------------- check-safe-to-publish.py
class SafeToPublish(Temp):
    def setUp(self):
        super().setUp()
        self.git("init", "-q")

    def test_clean_repo_passes(self):
        write(self.repo, "src/main.c", "int main(){}")
        self.git("add", "-A")
        code, out = run("check-safe-to-publish.py", cwd=self.repo)
        self.assertEqual(code, 0, out)

    def test_rom_and_save_blocked(self):
        write(self.repo, "roms/pokered.gb", b"\x00rom")
        write(self.repo, "saves/game.sav", b"\x00save")
        self.git("add", "-A")
        code, out = run("check-safe-to-publish.py", cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("pokered.gb: looks like a Game Boy ROM", out)
        self.assertIn("game.sav: looks like a save file", out)
        self.assertIn("git rm --cached", out)

    def test_large_binary_blocked_large_text_allowed(self):
        write(self.repo, "big.bin", b"\x00" * (6 * 1024 * 1024))
        write(self.repo, "big.txt", "a" * (6 * 1024 * 1024))
        self.git("add", "-A")
        code, out = run("check-safe-to-publish.py", cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("big.bin: a 6.0 MB binary", out)
        self.assertNotIn("big.txt", out)

    def test_allowlist(self):
        write(self.repo, "tests/fixtures/tiny.sav", b"\x00")
        write(self.repo, ".publish-allowlist", "tests/fixtures/*.sav  # made from scratch\n")
        self.git("add", "-A")
        code, out = run("check-safe-to-publish.py", cwd=self.repo)
        self.assertEqual(code, 0, out)

    def test_staged_only_checks_staged_files(self):
        write(self.repo, "ok.c", "x")
        self.git("add", "-A")
        self.git("commit", "-qm", "init")
        write(self.repo, "new.iso", b"\x00")  # not staged
        code, out = run("check-safe-to-publish.py", "--staged", cwd=self.repo)
        self.assertEqual(code, 0, out)
        self.git("add", "new.iso")
        code, out = run("check-safe-to-publish.py", "--staged", cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("new.iso", out)


# ---------------------------------------------------------------- check-research.py
HANDOFF_VERSIONS = """
# Handoff
## Tool versions
| Tool | Version |
|------|---------|
| xenia-canary | 1.3.0 |
| dotnet | 8.0.1 |
## Lessons
- x
"""


class Research(Temp):
    def test_drift_found(self):
        write(self.repo, "docs/HANDOFF.md", HANDOFF_VERSIONS)
        write(self.repo, "docs/research/save.md", """
            # Save format
            ## Header
            Header is 0x40 bytes. [confirmed @ m3-p1 | xenia-canary=1.2.3, dotnet=8.0.1]
            Checksum is CRC32. [confirmed @ m4 | dotnet=8.0.1]
            """)
        write(self.repo, "docs/research/INDEX.md", "| Header | [save.md § Header](save.md#header) |\n")
        code, out = run("check-research.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn("save.md:3: proven on m3-p1 with xenia-canary 1.2.3; now 1.3.0", out)
        self.assertNotIn("CRC32", out)

    def test_no_drift_and_index_ok(self):
        write(self.repo, "docs/HANDOFF.md", HANDOFF_VERSIONS)
        write(self.repo, "docs/research/save.md", "# Save\n## Header (0x00–0x3F)\nok [confirmed @ m4 | dotnet=8.0.1]\n")
        write(self.repo, "docs/research/INDEX.md",
              "| Header | [save.md § Header](save.md#header-0x000x3f) |\n")
        code, out = run("check-research.py", cwd=self.repo)
        self.assertEqual(code, 0, out)
        self.assertIn("Version drift: none (1 stamped", out)
        self.assertIn("every entry resolves", out)

    def test_broken_index_entries(self):
        write(self.repo, "docs/HANDOFF.md", HANDOFF_VERSIONS)
        write(self.repo, "docs/research/save.md", "# Save\n## Header\n")
        write(self.repo, "docs/research/net.md", "# Net\n")
        write(self.repo, "docs/research/INDEX.md",
              "| a | [save.md](save.md#footer) |\n| b | [gone.md](gone.md) |\n")
        code, out = run("check-research.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn("no heading for #footer", out)
        self.assertIn("gone.md, which doesn't exist", out)
        self.assertIn("docs/research/net.md", out)  # unlisted

    def test_warn_only(self):
        write(self.repo, "docs/HANDOFF.md", HANDOFF_VERSIONS)
        write(self.repo, "docs/research/a.md", "x [confirmed @ t | dotnet=7.0]\n")
        code, _ = run("check-research.py", "--warn-only", cwd=self.repo)
        self.assertEqual(code, 0)


# ---------------------------------------------------------------- check-report.py
GOOD_REPORT = """
# Report: M2-save-format

**Prompt:** `docs/prompts/M2-save-format.md`
**Branch:** `m2-save-format` (from tag `m1`) · **Last commit:** `abc1234`
**Status:** done

## Tool versions
| Tool | Version used | Matches HANDOFF.md? |
|------|--------------|---------------------|
| dotnet | 8.0.1 | yes |

## What changed
- SaveIO.cs: header parser (`abc1234`)

## Findings
| Finding | Status | Evidence |
|---------|--------|----------|
| Header is 0x40 bytes | confirmed | test HeaderSize passes on fixture a.sav |
| Checksum is CRC32 | unverified | read from decompiled loader at 0x8012A4C0 |

## Tests
```
dotnet test
Passed: 12, Failed: 0
```

## Open questions
- None.
"""


class Report(Temp):
    def check(self, text):
        write(self.repo, "r.md", text)
        return run("check-report.py", "r.md", cwd=self.repo)

    def test_good(self):
        code, out = self.check(GOOD_REPORT)
        self.assertEqual(code, 0, out)

    def test_bad_label_and_missing_evidence(self):
        bad = GOOD_REPORT.replace("| confirmed | test HeaderSize", "| probably | test HeaderSize") \
                         .replace("read from decompiled loader at 0x8012A4C0", "")
        code, out = self.check(bad)
        self.assertEqual(code, 1)
        self.assertIn("labeled 'probably'", out)
        self.assertIn("has no evidence", out)

    def test_stopped_needs_reason(self):
        code, out = self.check(GOOD_REPORT.replace("**Status:** done", "**Status:** stopped"))
        self.assertEqual(code, 1)
        self.assertIn("Stopped because", out)

    def test_template_itself_fails(self):
        code, out = run("check-report.py", str(ROOT / "templates" / "REPORT.md"), cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("placeholders", out)


# ---------------------------------------------------------------- check-prompt.py
GOOD_PROMPT = """
# M2-save-format: parse the save header

## Read first
- `AGENTS.md`
- `docs/HANDOFF.md`

## Goal
Parse the 0x40-byte save header.

## Branch
`m2-save-format`, branched from tag `m1`.

## Known facts
| Fact | Status | Evidence |
|------|--------|----------|
| Header is 0x40 bytes | confirmed | capture a.sav |

## Tasks
1. Write the parser.

## Stop and report if
- The AGENTS.md stop conditions are met.

## Acceptance checks
- `dotnet test` passes.

## Report
Write `docs/reports/M2-save-format.md`.
"""


class Prompt(Temp):
    def check(self, text):
        write(self.repo, "p.md", text)
        return run("check-prompt.py", "p.md", cwd=self.repo)

    def test_good(self):
        code, out = self.check(GOOD_PROMPT)
        self.assertEqual(code, 0, out)

    def test_agents_md_must_be_first(self):
        code, out = self.check(GOOD_PROMPT.replace("- `AGENTS.md`\n- `docs/HANDOFF.md`",
                                                   "- `docs/HANDOFF.md`\n- `AGENTS.md`"))
        self.assertEqual(code, 1)
        self.assertIn("AGENTS.md first", out)

    def test_unlabeled_fact_and_missing_section(self):
        bad = GOOD_PROMPT.replace("| confirmed | capture", "| maybe | capture").replace("## Stop and report if", "## Stops")
        code, out = self.check(bad)
        self.assertEqual(code, 1)
        self.assertIn("labeled confirmed or unverified", out)
        self.assertIn("missing section '## Stop and report if'", out)

    def test_template_itself_fails(self):
        code, out = run("check-prompt.py", str(ROOT / "templates" / "PROMPT.md"), cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("placeholders", out)


# ---------------------------------------------------------------- detect-mode.py (the skill's mode table)
class DetectMode(Temp):
    def mode(self):
        code, out = run("detect-mode.py", str(self.repo), "--json", cwd=self.repo)
        self.assertEqual(code, 0, out)
        return json.loads(out)

    def test_empty_repo_is_kickoff(self):
        self.assertEqual(self.mode()["mode"], "kickoff")

    def test_github_starter_files_still_kickoff(self):
        write(self.repo, "README.md", "# x")
        write(self.repo, "LICENSE", "MIT")
        write(self.repo, ".gitignore", "bin/")
        self.assertEqual(self.mode()["mode"], "kickoff")

    def test_code_without_handoff_is_adopt(self):
        write(self.repo, "src/Program.cs", "class P{}")
        write(self.repo, "CLAUDE.md", "rules")
        write(self.repo, "TODO.md", "- x")
        r = self.mode()
        self.assertEqual(r["mode"], "adopt")
        self.assertIn("CLAUDE.md", r["rules_files"])
        self.assertIn("TODO.md", r["notes"])
        self.assertIn("AGENTS.md", r["missing"])

    def test_handoff_is_continue(self):
        write(self.repo, "src/a.c", "x")
        write(self.repo, "docs/HANDOFF.md", "# h")
        self.assertEqual(self.mode()["mode"], "continue")


if __name__ == "__main__":
    unittest.main(verbosity=2)
