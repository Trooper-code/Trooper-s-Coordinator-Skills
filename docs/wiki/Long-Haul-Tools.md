# Long-Haul Tools

Features for projects that run for months: releases without hand-written notes, research you can trust, memory
that notices when it goes stale, and a guard against publishing what you shouldn't. All added in v1.4.0.

| Tool | Say / run | Section |
|------|-----------|---------|
| Release mode | `Use agent-coordinator. Release v1.2.0.` | [Release mode](#release-mode) |
| Research import | `Use agent-coordinator. Import research:` + paste | [Research import](#research-import) |
| Copyright guard | automatic: pre-commit hook + CI | [Copyright guard](#copyright-guard) |
| Version-aware facts | `python scripts/check-research.py` | [Version-aware facts](#version-aware-facts) |
| Decisions log | `docs/DECISIONS.md` | [Decisions log](#decisions-log) |
| Research index | `docs/research/INDEX.md` | [Research index](#research-index) |
| Lessons → rules | `(x2)` on a lesson | [Lessons become rules](#lessons-become-rules) |
| Check scripts | `scripts/*.py` | [The check scripts](#the-check-scripts) |

## Release mode
When milestones are merged and tested, say `Use agent-coordinator. Release v1.2.0.`
1. Claude reads what changed since the last tag: the milestone log, the merged agent reports and `git log`. It
   doesn't open code.
2. It picks the version if you didn't: a new feature is minor, fixes only is a patch, and anything that breaks how
   users use it is major. It says why in one line.
3. It writes the `CHANGELOG.md` entry **for your users**, with New / Changed / Fixed sections and an Upgrading
   section when they need to do something.
4. It checks the entry with `release-notes.py`, commits, and tags. If it can't push tags from where it's running,
   it gives you the two commands.
5. The release workflow ([`release.yml`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/github/workflows/release.yml)) creates the GitHub Release
   with that section as its notes, and attaches whatever your build step puts in `dist/`.

Between releases, every merged milestone adds a line under `## Unreleased`, so the changelog writes itself as
you go.

## Research import
Deep-research tools write confident, well-cited reports that are sometimes wrong. Import mode treats them as
**leads**:

| Step | What Claude does |
|------|------------------|
| Split | One checkable claim per item: an offset, a format detail, a version, a behavior. Filler and opinion are dropped. |
| Label | Every claim is **unverified**, with its source: `[unverified \| source: Gemini Deep Research 2026-11-17, citing <url>]`. |
| Compare | Looks each topic up in the research index and reads only those sections. |
| Conflicts | A claim that contradicts a **confirmed** fact is listed for you, never filed as true. Confirmed beats unverified until something is re-tested. |
| Duplicates | A claim that matches a known fact adds a source to it, not a second copy. |
| File | New claims go into the right sections, with index lines for new topics. The raw report is saved under `docs/research/sources/` only if you want it kept. |
| Verify | The claims the next milestone depends on go into a verify prompt: the agent proves or disproves each one and stamps the result. |

Claude does at most 2–3 quick spot-checks itself. Deeper checking is the agent's job, which keeps the coordinator
cheap.

## Copyright guard
[`check-safe-to-publish.py`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/scripts/check-safe-to-publish.py) blocks:
- **game data**: cartridge ROMs (`.gb`, `.gba`, `.nds`, `.n64`, `.sfc`...), disc images (`.iso`,
  `.chd`, `.rvz`...), console executables and packages (`.xex`, `.xbe`, `.pkg`, `.self`...);
- **personal data**: save files, memory cards and emulator save states;
- **any binary over 5 MB**, whatever its name.

It runs in two places:
- **Before every commit:** install the hook once with `cp scripts/hooks/pre-commit .git/hooks/pre-commit` (Git
  for Windows runs it too). It checks only what you're committing.
- **On every push:** [`checks.yml`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/github/workflows/checks.yml) checks every tracked file, so a
  commit made without the hook is still caught.

Exceptions you made yourself (a tiny test save) go in `.publish-allowlist`, one pattern per line, with a comment
saying why. It's a check on names, sizes and binary contents: it stops accidents, not someone determined to get
around it.

## Version-aware facts
Confirmed facts carry a stamp of what they were proven on:

    Save header is 0x40 bytes. [confirmed @ m3-p1 | xenia-canary=1.2.3, dotnet=8.0.1]

The tool names match the **Tool versions** table in `HANDOFF.md`. When that table changes, `check-research.py`
lists every fact proven on an older version:

    docs/research/save.md:14: proven on m3-p1 with xenia-canary 1.2.3; now 1.3.0. Re-check it.

Claude adds re-checking those facts to the next prompt, and the agent re-stamps each one or marks it **wrong**.
Emulator and tool updates are where "confirmed" offsets quietly break; this catches it the next time the
versions are written down.

## Decisions log
[`DECISIONS.md`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/DECISIONS.md) holds one short entry per real decision:
- **Decided** and **Rejected**: what was chosen and what wasn't;
- **Why**: linked to the research behind it;
- **Revisit if**: what would change the answer;
- **Supersedes**: the earlier entry it replaces, if any.

The research docs record what's *true*; this records what was *chosen* and why. New chats read it instead of
reopening settled questions. New facts get a new entry that supersedes the old one, so the history stays.

## Research index
[`research/INDEX.md`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/research/INDEX.md) has one line per topic: a link to the file and section,
and its status. Claude and the agent look things up there before skimming docs or code, which keeps reads small.
`check-research.py` fails on entries that point to a missing file or heading, and lists research docs that
aren't indexed yet. In [[Memory Model]] terms, it's the address table for the external memory.

## Lessons become rules
A lesson that's hit a second time gets `(x2)` at the end of its line in `HANDOFF.md`. `check-handoff.py`
prints a note for it, and Claude promotes it:
- into `AGENTS.md`, as a rule for the agent;
- into a check script, if it can be automated;
- or into the prompt template.

Then it's removed from Lessons. Lessons stay a short list of new traps, not a growing pile of old ones.

## The check scripts
All in [`templates/scripts/`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/scripts). They need Python 3.9 or newer and nothing else.

| Script | When | Catches |
|--------|------|---------|
| `check-prompt.py` | after writing a prompt | missing sections, `AGENTS.md` not first, unlabeled facts, placeholders |
| `check-report.py` | first step of review | no status, stop without a reason, findings without a label or evidence, tests without output |
| `check-research.py` | review, version changes | version drift, broken index entries |
| `check-handoff.py` | before a handoff commit | budget, sections, dead paths, lessons to promote |
| `check-safe-to-publish.py` | hook and CI | game data, saves, big binaries |
| `release-notes.py` | release | a version's changelog section as notes |
| `detect-mode.py` | before kickoff/adopt | which mode the repo needs; which workflow files exist or are missing |
