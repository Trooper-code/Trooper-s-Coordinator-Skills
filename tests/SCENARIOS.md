# Skill scenarios

The scripts are tested automatically (`tests/test_scripts.py`, `tests/test_check_handoff.py`), and
`scripts/validate.py` checks that every file a skill mentions exists. What a skill makes *Claude do* can't run in
CI, because it needs a live Claude session. These scenarios are the checklist for that: run the ones a change
touches before tagging a release.

**How to run one:** make a scratch repo as described, start a fresh Claude chat with the skills installed, send the
message, and compare what happens with **Expect**. Note any miss in the PR or as an issue.

| # | Setup | Send | Expect |
|---|-------|------|--------|
| S1 | Empty repo (README and LICENSE only) | `Use agent-coordinator. Start a new project: demo. Repo: <url>. Goal: a CLI that renames files. Coding agent: Antigravity.` | **Kickoff.** Asks which Antigravity tools you have; writes `AGENTS.md` with an Antigravity section; scaffolds docs, scripts, hook, workflows; writes the M1 prompt that passes `check-prompt.py`; commits; gives one line for the agent and the hook install command. |
| S2 | Repo with code, a `TODO.md` and a `CLAUDE.md`, no `docs/HANDOFF.md` | `Use agent-coordinator. Adopt my existing project. Repo: <url>. Coding agent: Codex.` | **Adopt.** Scans without tracing code; adds to `CLAUDE.md` rather than replacing it; creates only missing files; labels facts from old docs unverified; runs the publish check; plans milestones; one docs-only commit. |
| S3 | Repo with `docs/HANDOFF.md` | either command from S1 or S2 | **Continue.** Reads the handoff and does its "First thing to do". Doesn't scaffold anything. |
| S4 | Any set-up repo | `Use agent-coordinator. Status.` | About five lines from `MILESTONES.md` and `HANDOFF.md` only. No other files opened. |
| S5 | Agent branch whose report has a finding labeled "probably" and no evidence | `The agent's done with M2.` | Reads the report from the branch; `check-report.py` fails; sends it back to the agent (or lists the gap) instead of reviewing on. |
| S6 | Agent branch whose report says `**Status:** stopped` (3 failed attempts) | `The agent's done with M2.` | Doesn't redo the work. Works out what the agent needs and writes it into the next prompt. |
| S7 | A branch that has failed two review rounds | `Still broken, same as last time.` | **Abandon rule.** Keeps the branch, records why, keeps confirmed findings, new prompt from the last good tag. |
| S8 | `HANDOFF.md` Tool versions bumped (e.g. emulator 1.2 → 1.3); research has stamped facts on 1.2 | `Update the handoff.` | Runs `check-research.py`; the next prompt includes re-checking the drifted facts. |
| S9 | Any set-up repo | `Use agent-coordinator. Import research:` + a pasted deep-research report that contradicts one confirmed fact | Claims filed as unverified with sources; the contradiction listed as a conflict, not filed as true; a verify prompt for the claims the next milestone needs. |
| S10 | Merged milestones since the last tag, `## Unreleased` in `CHANGELOG.md` | `Use agent-coordinator. Release v1.1.0.` | Changelog entry written for users; `release-notes.py v1.1.0` prints it; tag commands run or handed over; says what to check on the Releases page. |
| S11 | A staged `.gb` file | `git commit` (with the hook installed) | Commit blocked, with a plain-English reason and how to fix it. |
| S12 | `HANDOFF.md` with a lesson ending `(x2)` | `Update the handoff.` | The lesson is promoted into `AGENTS.md`, a check, or the prompt template, and removed from Lessons. |
