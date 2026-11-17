# <MILESTONE>-<slug>: <short title>

<!-- Copy to docs/prompts/<MILESTONE>-<slug>.md in your project. The coding agent has none of your chat's
     context, so everything it needs must be in this file, in AGENTS.md, or in the files under "Read first".
     Standing rules (don't merge, no copyrighted files, line endings, evidence, stop conditions, report format)
     live in AGENTS.md. Only add constraints here that are specific to this task. -->

## Read first
- `AGENTS.md` (standing rules, including your agent-specific section)
- `docs/HANDOFF.md`, sections "How it works now" and "Tool versions"
- `docs/MILESTONES.md`, section <N>
- `docs/research/INDEX.md`, then `docs/research/<topic>.md`
- `docs/DECISIONS.md` entries <D#> (only if this task touches a past decision)

## Goal
<One or two sentences: what should be true when this is done.>

## Branch
`<milestone>-<slug>`, branched from tag `<last-good-tag>`.

## Known facts
| Fact | Status | Evidence |
|------|--------|----------|
| <e.g. Save header is 0x40 bytes> | confirmed | <test run / capture name> |
| <e.g. Checksum is CRC32 over 0x40..end> | unverified | <read from source, not tested> |

## Tasks
1. <...>
2. <...>
3. Write every finding into `docs/research/<topic>.md`, labeled, with evidence.

## Tools
- `systematic-debugging`: find the root cause before changing code.
- <Any other tool, and why it fits this task.>

## Task-specific constraints
- <Only what AGENTS.md doesn't already say, e.g. "don't change the public file format", "keep it .NET 8".>

## Stop and report if
- The AGENTS.md stop conditions are met (3 failed attempts, missing access, contradicts a confirmed fact, task
  much bigger than expected), or:
- <Task-specific, e.g. "the checksum isn't CRC32", "the fix needs changes outside SaveIO/">.

## Acceptance checks
- `<test command>` passes.
- Every finding in the report cites its evidence.

## Report
Write `docs/reports/<MILESTONE>-<slug>.md` using `docs/reports/TEMPLATE.md`, commit it on the branch, and reply with its
path plus a 3-line summary.
