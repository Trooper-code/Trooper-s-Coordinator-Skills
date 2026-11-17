# Changelog

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
