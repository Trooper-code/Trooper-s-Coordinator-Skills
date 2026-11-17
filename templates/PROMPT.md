# <MILESTONE>-<slug>: <short title>

<!-- Copy to docs/prompts/<MILESTONE>-<slug>.md in your project. The coding agent has none of your chat's
     context, so everything it needs must be in this file or in the files listed under "Read first". -->

## Read first
- `docs/HANDOFF.md`, section "How it works now"
- `docs/MILESTONES.md`, section <N>
- `docs/research/<topic>.md`

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
3. Write every finding into `docs/research/<topic>.md`, marked confirmed / unverified / wrong, with evidence.

## Tools
- `systematic-debugging`: find the root cause before changing code.
- `test-driven-development`: write the failing test first.
- <Any analysis tool, and why it fits. Keep it read-only on the user's files.>

## Constraints
- Never commit copyrighted or third-party files (games, ROMs, saves, assets, binaries).
- Tests must not touch real user data, real logs or real ports.
- Keep each file's existing line endings.
- Commit with the project's git identity.
- **Do not merge.** Leave the branch for review.

## Acceptance checks
- `<test command>` passes.
- Every claim in your report cites its evidence (file, address/offset, log or test name).

## Report back
- What changed (files, commits).
- Each finding: confirmed / unverified / wrong, with evidence.
- Test results (paste the summary line).
- Open questions and anything you couldn't finish.
