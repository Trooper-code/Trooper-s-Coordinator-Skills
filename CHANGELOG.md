# Changelog

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
