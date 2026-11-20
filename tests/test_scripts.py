#!/usr/bin/env python3
"""Tests for every script in templates/scripts/ (except check-handoff.py, see test_check_handoff.py).

Run locally with:  python tests/test_scripts.py
CI runs it on every push. Each test builds a throwaway repo in a temp folder, runs a script against it, and checks
the exit code and the message. Only uses the Python standard library (plus git, for the publish check).
"""
import json
import os
import re
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

    def test_non_ascii_name_is_checked(self):
        write(self.repo, "roms/Pokémon.gb", b"\x00rom")
        self.git("add", "-A")
        code, out = run("check-safe-to-publish.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn("Pokémon.gb: looks like a Game Boy ROM", out)
        code, out = run("check-safe-to-publish.py", "--staged", cwd=self.repo)
        self.assertEqual(code, 1, out)

    def test_staged_checks_the_staged_copy_not_the_disk(self):
        write(self.repo, "blob.dat", b"\x00" * (6 * 1024 * 1024))
        self.git("add", "blob.dat")
        write(self.repo, "blob.dat", "small now")  # edited after git add; the big copy is what gets committed
        code, out = run("check-safe-to-publish.py", "--staged", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn("blob.dat: a 6.0 MB binary", out)

    def test_secrets_blocked(self):
        write(self.repo, ".env", "TOKEN=abc")
        write(self.repo, "keys/server.pem", "-----BEGIN PRIVATE KEY-----")
        self.git("add", "-A")
        code, out = run("check-safe-to-publish.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn(".env: looks like a secrets file", out)
        self.assertIn("server.pem: looks like a private key", out)


class Hook(Temp):
    """The pre-commit hook finds the scripts in scripts/ or docs/scripts/."""

    def setUp(self):
        super().setUp()
        self.git("init", "-q")

    def install(self, scripts_dir):
        (self.repo / scripts_dir).mkdir(parents=True, exist_ok=True)
        (self.repo / scripts_dir / "check-safe-to-publish.py").write_bytes(
            (SCRIPTS / "check-safe-to-publish.py").read_bytes())
        hook = self.repo / ".git" / "hooks" / "pre-commit"
        hook.write_bytes((ROOT / "templates" / "hooks" / "pre-commit").read_bytes())
        hook.chmod(0o755)

    def commit(self):
        return subprocess.run(["git", "commit", "-qm", "t"], cwd=self.repo, capture_output=True, text=True,
                              env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                   "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})

    def test_blocks_rom_with_scripts_at_root(self):
        self.install("scripts")
        write(self.repo, "game.gb", b"\x00")
        self.git("add", "-A")
        r = self.commit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Game Boy ROM", r.stdout + r.stderr)

    def test_blocks_rom_with_scripts_under_docs(self):
        self.install("docs/scripts")
        write(self.repo, "game.gb", b"\x00")
        self.git("add", "-A")
        r = self.commit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Game Boy ROM", r.stdout + r.stderr)

    def test_clean_commit_passes(self):
        self.install("docs/scripts")
        write(self.repo, "main.c", "x")
        self.git("add", "-A")
        self.assertEqual(self.commit().returncode, 0)

    @unittest.skipIf(os.name == "nt", "fakes python3 with a shell script")
    def test_broken_python3_falls_back(self):
        """Like the Windows Store 'python3' shortcut: on PATH, but fails when run."""
        fake = self.repo / ".fakebin"
        write(self.repo, ".fakebin/python3", "#!/bin/sh\necho 'Python was not found' >&2\nexit 9\n").chmod(0o755)
        (fake / "python").symlink_to(sys.executable)
        self.install("scripts")
        write(self.repo, "game.gb", b"\x00")
        self.git("add", "game.gb")
        r = subprocess.run(["git", "commit", "-qm", "t"], cwd=self.repo, capture_output=True, text=True,
                           env={**os.environ, "PATH": f"{fake}{os.pathsep}{os.environ['PATH']}",
                                "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                                "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Game Boy ROM", r.stdout + r.stderr)


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

    def test_unlisted_doc_fails(self):
        write(self.repo, "docs/research/save.md", "# Save\n")
        write(self.repo, "docs/research/net.md", "# Net\n")
        write(self.repo, "docs/research/INDEX.md", "| a | [save.md](save.md) |\n")
        code, out = run("check-research.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn("  - docs/research/net.md", out)

    def test_runs_from_a_subfolder(self):
        (self.repo / ".git").mkdir()
        write(self.repo, "docs/HANDOFF.md", HANDOFF_VERSIONS)
        write(self.repo, "docs/research/a.md", "x [confirmed @ t | dotnet=7.0]\n")
        write(self.repo, "src/x.c", "x")
        code, out = run("check-research.py", cwd=self.repo / "src")
        self.assertEqual(code, 1, out)
        self.assertIn("docs/research/a.md:1: proven on t with dotnet 7.0; now 8.0.1", out)

    def test_comments_and_code_blocks_ignored(self):
        write(self.repo, "docs/research/save.md", "# Save\n```\n# not a heading\n```\n")
        write(self.repo, "docs/research/INDEX.md",
              "<!-- example: [x](example.md) -->\n| a | [save.md](save.md) |\n| b | [s](save.md#not-a-heading) |\n")
        code, out = run("check-research.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertNotIn("example.md", out)
        self.assertIn("no heading for #not-a-heading", out)

    def test_unknown_tool_in_stamp(self):
        write(self.repo, "docs/HANDOFF.md", HANDOFF_VERSIONS)
        write(self.repo, "docs/research/a.md", "x [confirmed @ t | xenia=1.2.3]\n")
        write(self.repo, "docs/research/INDEX.md", "| a | [a.md](a.md) |\n")
        code, out = run("check-research.py", cwd=self.repo)
        self.assertEqual(code, 1, out)
        self.assertIn("docs/research/a.md:1: 'xenia'", out)


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

    def test_stopped_with_template_heading_passes(self):
        stopped = GOOD_REPORT.replace("**Status:** done", "**Status:** stopped").replace(
            "## Open questions", '## Stopped because (only if status is "stopped")\nFailed 3 times.\n\n## Open questions')
        code, out = self.check(stopped)
        self.assertEqual(code, 0, out)

    def test_unfilled_status_line(self):
        code, out = self.check(GOOD_REPORT.replace("**Status:** done", "**Status:** done | stopped | partial"))
        self.assertEqual(code, 1)
        self.assertIn("Status", out)

    def test_empty_sections_and_test_block(self):
        bad = GOOD_REPORT.replace("- SaveIO.cs: header parser (`abc1234`)", "") \
                         .replace("dotnet test\nPassed: 12, Failed: 0\n", "")
        code, out = self.check(bad)
        self.assertEqual(code, 1)
        self.assertIn("'## What changed' is empty", out)
        self.assertIn("no filled-in code block", out)


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

    def test_bullet_facts_flagged(self):
        bad = GOOD_PROMPT.replace("| Header is 0x40 bytes | confirmed | capture a.sav |",
                                  "| Header is 0x40 bytes | confirmed | capture a.sav |\n\n- Checksum is CRC32")
        code, out = self.check(bad)
        self.assertEqual(code, 1)
        self.assertIn("'Checksum is CRC32' is a bullet", out)

    def test_facts_none_allowed(self):
        ok = re.sub(r"\| Fact .*?capture a\.sav \|", "None.", GOOD_PROMPT, flags=re.S)
        code, out = self.check(ok)
        self.assertEqual(code, 0, out)

    def test_empty_goal_and_weak_branch(self):
        bad = GOOD_PROMPT.replace("Parse the 0x40-byte save header.", "") \
                         .replace("`m2-save-format`, branched from tag `m1`.", "Not a tag, work on `main`.")
        code, out = self.check(bad)
        self.assertEqual(code, 1)
        self.assertIn("'## Goal' is empty", out)
        self.assertIn("tag to branch from", out)


# ---------------------------------------------------------------- placeholder lists stay in step with the templates
class Placeholders(unittest.TestCase):
    """Each checker keeps a list of its template's <placeholders>. If a template gains a new one, this fails."""

    def caught(self, script, template):
        src = (SCRIPTS / script).read_text(encoding="utf-8")
        pattern = re.search(r'PLACEHOLDER = (re\.compile\(.*?\))\n', src, re.S).group(1)
        rx = eval(pattern, {"re": re})
        text = re.sub(r"<!--.*?-->", "", (ROOT / "templates" / template).read_text(encoding="utf-8"), flags=re.S)
        missed = [m for m in re.findall(r"<[^<>\n]+>", text) if not rx.fullmatch(m)]
        self.assertEqual(missed, [], f"{script} doesn't catch these placeholders from templates/{template}")

    def test_prompt(self):
        self.caught("check-prompt.py", "PROMPT.md")

    def test_report(self):
        self.caught("check-report.py", "REPORT.md")


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

    def test_scripts_under_docs_are_found(self):
        write(self.repo, "src/a.c", "x")
        write(self.repo, "docs/scripts/check-handoff.py", "x")
        write(self.repo, "docs/scripts/check-safe-to-publish.py", "x")
        r = self.mode()
        self.assertEqual(r["scripts_dir"], "docs/scripts")
        self.assertIn("docs/scripts/check-handoff.py", r["have"])
        self.assertIn("docs/scripts/check-report.py", r["missing"])
        self.assertNotIn("scripts/check-handoff.py", r["missing"])

    def test_scripts_default_to_repo_root(self):
        write(self.repo, "src/a.c", "x")
        r = self.mode()
        self.assertEqual(r["scripts_dir"], "scripts")
        self.assertIn("scripts/check-handoff.py", r["missing"])

    def test_handoff_is_continue(self):
        write(self.repo, "src/a.c", "x")
        write(self.repo, "docs/HANDOFF.md", "# h")
        self.assertEqual(self.mode()["mode"], "continue")

    def test_antigravity_rules_folder_found(self):
        write(self.repo, "src/a.c", "x")
        write(self.repo, ".agents/rules/style.md", "---\ntrigger: always_on\n---\n")
        self.assertIn(".agents/rules", self.mode()["rules_files"])

    def test_missing_folder_json_error(self):
        code, out = run("detect-mode.py", str(self.repo / "nope"), "--json", cwd=self.repo)
        self.assertEqual(code, 1)
        self.assertIn("error", json.loads(out))


if __name__ == "__main__":
    unittest.main(verbosity=2)
