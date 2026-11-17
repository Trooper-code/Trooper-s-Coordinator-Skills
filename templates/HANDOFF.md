# <Project> handoff

<!-- Copy to docs/HANDOFF.md. Keep it under ~100 lines / 10 KB: it's the current state and the next step,
     not history. Dated progress goes in MILESTONES.md; findings go in the research docs. -->

## Setup
| What | Where |
|------|-------|
| Repo | `<path>` |
| Tools / versions | `<compiler, emulator, SDK...>` |
| Test data (never committed) | `<path>` |

## How it works now
<Short summary of the current working state. What's confirmed, and which tag holds it.
Full details: `docs/research/<topic>.md`.>

## Where it stops
<Latest real test result, and the exact log/capture that shows it.>

## In progress
- <Coding agent>: `docs/prompts/<MILESTONE>-<slug>.md` on branch `<branch>`.

## Rules
- <One line each.>

## First thing to do
1. Read MILESTONES §<N> and `docs/research/<topic>.md` §<section>.
2. Run all the tests.
3. Spot-check the agent's claims against the real files and logs.
4. List bugs, then gaps, then nitpicks.
5. Give the user test steps. Merge and tag if it works, or write the follow-up prompt if it doesn't.

## Lessons
- <One line per trap, grouped by theme. Keep about 10-12.>

[Paste the coding agent's latest summary here]

---
