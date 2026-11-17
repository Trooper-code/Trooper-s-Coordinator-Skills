# <Project> handoff

<!-- Copy to docs/HANDOFF.md. Keep it under ~100 lines / 10 KB: it's the current state and the next step,
     not history. Dated progress goes in MILESTONES.md; findings go in the research docs; agent reports go in
     docs/reports/. Check it with: python scripts/check-handoff.py -->

## Setup
| What | Where |
|------|-------|
| Repo | `<path>` |
| Coding agent | `<agent>` (rules: `AGENTS.md`) |
| Test data (never committed) | `<path>` |

## Tool versions
| Tool | Version |
|------|---------|
| <compiler / SDK / emulator / loader / mod> | <exact version> |

## How it works now
<Short summary of the current working state. What's confirmed, and which tag holds it.
Full details: `docs/research/<topic>.md`.>

## Where it stops
<Latest real test result, and the exact log/capture that shows it.>

## In progress
- <Coding agent>: `docs/prompts/<MILESTONE>-<slug>.md` on branch `<branch>`.
  Report (when done): `docs/reports/<MILESTONE>-<slug>.md` on that branch.

## Rules
- <One line each.>

## First thing to do
1. Read MILESTONES §<N> and `docs/research/<topic>.md` §<section>.
2. Read the agent's report from its branch (see "In progress").
3. Run all the tests. Check its tool versions against the table above.
4. Spot-check its claims against the real files and logs.
5. List bugs, then gaps, then nitpicks.
6. Give the user test steps. Merge and tag if it works; follow-up prompt if not (or abandon, per the skill's rule).

## Lessons
- <One line per trap, grouped by theme. Keep about 10-12.>

[Paste the coding agent's latest summary here, or leave this line if its report is in docs/reports/]

---
