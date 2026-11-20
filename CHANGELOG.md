# Changelog

## v1.5.0
Fixes from two outside reviews (Qwen and Gemini), each checked against the code before changing anything.

### Fixed
- **Pre-commit hook on Windows.** The hook picked `python3` just because the name existed, and on Windows that's
  often the Microsoft Store shortcut, which fails. It now uses the first of `python3`, `python`, `py` that actually
  runs, and says how to fix it if none do.
- **`check-safe-to-publish.py`** missed files with non-ASCII names (`Pokémon.gb` passed). It now reads git's file
  list safely, and with `--staged` it checks the staged copy of each file (what will be committed), not the one on
  disk. It also blocks `.rom` files and common secrets: `.env`, `.pem`, `.key`, `.p12`, `.pfx`, `id_rsa`,
  `id_ed25519`, `credentials.json`.
- **`check-report.py`** rejected a valid stopped report that kept the template's heading
  (`## Stopped because (only if status is "stopped")`), and read the unfilled `done | stopped | partial` line as
  "done". Empty sections and an empty Tests code block now fail.
- **`check-prompt.py`** let known facts written as bullets skip the confirmed/unverified check. Bullets are now
  flagged (use the table, or write "None."), empty required sections fail, and the Branch must name the tag in
  backticks.
- **`check-research.py`** now works from any folder in the repo, prints paths with `/` on Windows, ignores
  commented-out examples in `INDEX.md` and `#` lines inside code blocks, and flags stamps that name a tool missing
  from the Tool versions table. Research docs missing from the index, or a missing index, now fail (CI still uses
  `--warn-only`).
- **`check-handoff.py`** follows Markdown links from HANDOFF.md's own folder, the way GitHub does, so
  a link to `docs/research/a.md` written inside `docs/HANDOFF.md` (which GitHub opens as
  `docs/docs/research/a.md`) is caught as broken. A Lesson that mentions
  `docs/reports/` no longer passes for the agent-summary line, and `(x2).` with trailing punctuation is recognised.
- **`detect-mode.py`** finds Antigravity's `.agents/rules/` folder, and exits 1 (with a JSON error under `--json`)
  when the folder doesn't exist.
- Tests now fail if a template gains a `<placeholder>` that its check script doesn't catch.

### Changed
- The agent now **pushes its branch** when it writes its report (AGENTS.md, PROMPT.md), since the coordinator reads
  the report from `origin`.
- The agent no longer edits `docs/HANDOFF.md` or `docs/MILESTONES.md` (the coordinator owns them), and the skill
  says how to resolve doc conflicts at merge.
- The skill says plainly that the check scripts check shape, not truth, so the review steps after them still matter.
- README: Claude Code install now uses the release zips, which include `templates/`.
- README: one line under the neural-network table saying this is a borrowed design, not a neural network
  (nothing is trained), with a link to where the comparison stops.

### Upgrading
- Re-upload `agent-coordinator.zip` (or replace its folder in `~/.claude/skills/`, including `templates/`).
- In each project, copy the new `templates/scripts/*.py` and `templates/hooks/pre-commit` over the old ones, then
  reinstall the hook: `cp scripts/hooks/pre-commit .git/hooks/pre-commit`.
- Copy the two new lines from `templates/AGENTS.md` (push your branch; don't edit HANDOFF.md/MILESTONES.md) into
  your project's `AGENTS.md`.
- `check-research.py` without `--warn-only` now fails on research docs missing from `INDEX.md`. Add them, or keep
  `--warn-only`.

## v1.4.1
- **Scripts in `docs/scripts/`.** The check scripts can now live in `docs/scripts/` as well as `scripts/`. The
  coordinator looks in both when it scans a project, `detect-mode.py` reports which one a repo uses, and the
  pre-commit hook and both workflow templates find the scripts in either folder.
- README: new "Where everything goes" section: where the skills go for each Claude app, and a full map of a
  project's files. Wiki FAQ: both questions.

### Upgrading
- Re-upload `agent-coordinator.zip` and `project-handoff.zip` (or replace both folders in `~/.claude/skills/`).
- Projects that already have the hook or workflows: copy the new `templates/hooks/pre-commit` and
  `templates/github/workflows/*.yml` over the old ones only if you want to move your scripts to `docs/scripts/`.

## v1.4.0

### New
- **Release mode.** `Use agent-coordinator. Release v1.2.0.` collects what changed since the last tag, writes the
  `CHANGELOG.md` entry for your users (with an Upgrading section when needed), and tags it. A new release workflow
  template creates the GitHub Release with that section as its notes. This repo's own releases now work the same way.
- **Research import.** `Use agent-coordinator. Import research:` + a deep-research report. Claims are filed as
  unverified with their sources; contradictions of confirmed facts are flagged, not filed; the claims the next
  milestone needs go into a verify prompt for the coding agent.
- **Copyright guard.** `check-safe-to-publish.py`, a pre-commit hook and a CI workflow block ROMs, disc images,
  console executables, saves, emulator states and binaries over 5 MB, with plain-English fixes. Exceptions go in
  `.publish-allowlist`.
- **Version-aware facts.** Confirmed findings are stamped with the tool versions they were proven on
  (`[confirmed @ m3-p1 | xenia-canary=1.2.3]`). `check-research.py` lists facts proven on older versions when the
  Tool versions table changes, and Claude adds re-checking them to the next prompt.
- **Decisions log** (`docs/DECISIONS.md`): decided, rejected, why, revisit-if. Settled questions stay settled.
- **Research index** (`docs/research/INDEX.md`): one line per topic, checked for dead links.
- **Lessons become rules.** A lesson hit twice gets `(x2)`; the handoff checker flags it for promotion into
  `AGENTS.md`, a check script or the prompt template.
- **Report and prompt linters.** `check-report.py` (first step of every review) and `check-prompt.py` (before every
  prompt goes out).
- **Agent profiles** in `templates/agents/` for Antigravity, Codex, Claude Code and Cursor, plus a generic one. Each
  fact is labeled confirmed or unverified. Antigravity's rules loading is confirmed against its docs.
- **Skill tests.** `tests/test_scripts.py` (25 tests across every script), `detect-mode.py` implementing the skill's
  mode table, a validator check that every file a skill mentions exists, and `tests/SCENARIOS.md`, a 12-row
  checklist for testing skill behavior in a live chat.

### Changed
- `agent-coordinator`: new Release and Research import modes; kickoff scaffolds the decisions log, research index,
  check scripts, hook and workflows; adopt runs the copyright guard and indexes existing research; reviews start
  with `check-report.py` and `check-research.py`. Mode details moved into `reference/` files to keep the skill short.
- `project-handoff`: stamps, index lines and decisions as part of saving findings; runs `check-research.py` when
  versions change; promotes repeated lessons.
- Release zips now bundle the `templates/` folder inside each skill, so Claude can copy templates into a project
  without fetching anything.
- `AGENTS.md`, `PROMPT.md`, `REPORT.md` and `HANDOFF.md` templates: index-first lookups, stamping, decisions,
  `check-report.py` before reporting.
- README: "Why I built this" section on the neural-network inspiration; "Built for the long haul" section; full
  command table. Wiki: new **Inspiration** and **Long-Haul Tools** pages; Memory Model gains a staleness section.

### Upgrading
- Re-upload both skill zips (or replace both folders in `~/.claude/skills/`).
- Existing projects: `Use agent-coordinator. Adopt my existing project.` adds the new files without touching yours.
  Install the hook with `cp scripts/hooks/pre-commit .git/hooks/pre-commit`.

## v1.3.0
- **`AGENTS.md`: the agent's standing rules.** New template. Holds the always/never rules, the tool-versions rule,
  stop conditions and the report format, so prompts only carry task-specific constraints. Kickoff and adopt create
  it (adopt adds missing sections to an existing rules file instead of replacing it).
- **Agent-specific constraints.** Whenever you name your coding agent, Claude writes an
  `## Agent-specific constraints: <agent>` section for that app: how it loads rules (with a pointer file if it reads
  a different one), its tools and when to use each, permission limits for high-privilege tools, and known quirks.
  It asks which tools you have instead of guessing. Switching agents updates the section.
- **Agent reports in the repo.** The agent writes `docs/reports/<MILESTONE>-<slug>.md` (new `REPORT.md` template)
  and commits it on its branch. Claude reads it from the branch, so summaries no longer need pasting between apps.
  Pasting still works as a fallback.
- **Stop conditions.** The agent stops and reports after 3 failed attempts, missing access, a contradicted confirmed
  fact, or a task much bigger than expected. Prompts can add their own.
- **Tool versions.** New table in `HANDOFF.md`. The agent reports the versions it used, and Claude checks them first
  on review.
- **Handoff checker.** New `templates/scripts/check-handoff.py`: checks size budget, required sections, the
  agent-summary line, and that every path `HANDOFF.md` points to exists. `project-handoff` runs it before every
  commit. Tested in CI (`scripts/test_check_handoff.py`).
- **Status mode.** `Use agent-coordinator. Status.` reads only `MILESTONES.md` and `HANDOFF.md` and answers in about
  five lines.
- **Abandon rule.** After two failed review rounds, or when a fix heads the wrong way, Claude keeps the branch for
  reference, records why, and restarts from the last good tag.
- README: new "What keeps the agent on track" section; both loops and Quick start updated. Wiki: new
  "Agent Rules and Reports" page; Workflow, Prompts, Reviewing, Handoffs, Memory Model and FAQ updated.

## v1.2.0
- **agent-coordinator: adopt an existing project.** New mode for projects that already have code or docs but no
  `HANDOFF.md`. Claude scans the README, docs, notes, build/test setup and git history (reading, not tracing code),
  maps what exists onto the workflow's files, creates only the missing ones (`MILESTONES.md`, `HANDOFF.md`,
  `docs/research/`, `docs/prompts/`), labels what it learned as unverified until tested, plans milestones from the
  project's real state, and writes the first agent prompt (an M0 survey if the code is undocumented).
- **Automatic mode pick.** Claude chooses kickoff, adopt or continue from what's in the repo, so either command works.
- README: "Add it to an existing project" in Quick start. Wiki: "Adding it to an existing project" on The Workflow.

## v1.1.0
- **agent-coordinator: new-project kickoff.** `/agent-coordinator Start a new project: ...` (Claude Code) or
  `Use agent-coordinator. Start a new project: ...` (Claude apps). Claude gets repo access, asks 1–3 scope questions
  only if needed, scaffolds the docs, plans milestones, writes the first prompt and commits.
- README: kickoff and continue commands in Quick start; the handoff explained with its own diagram.

## v1.0.0
- First release: `agent-coordinator` and `project-handoff` skills, templates, validator, CI with release zips,
  README and wiki (including the Memory Model page).
