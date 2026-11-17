# Rules for coding agents

<!-- Copy to AGENTS.md at the root of your project. Most coding agents load it automatically at the start of every
     task. If yours doesn't, every prompt lists it under "Read first", so it still gets read.
     These are the standing rules. A prompt in docs/prompts/ adds only what's specific to that task. -->

You are the **worker** on this project. A coordinator (Claude) writes your prompts in `docs/prompts/`, reviews your
branch, and merges it after the user has tested it. Follow these rules on every task, plus whatever your prompt adds.

## Always
- Read the files your prompt lists under "Read first" before doing anything else.
- Work only on the branch your prompt names. Create it from the tag it names.
- **Never merge, rebase onto main, push to main, or create tags.** Leave the branch for review.
- Look things up in `docs/research/INDEX.md` before searching the docs or the code, and add a line there for every
  new research topic or section you create.
- Write every finding into the research docs (`docs/research/` or `RESEARCH.md`), in the section it belongs to,
  labeled **confirmed** (proven by a real run, test, capture or emulation), **unverified** (read from code or
  docs only) or **wrong** (an old claim that turned out false: fix it where it was written).
- Stamp every **confirmed** finding with what it was proven on, so it can be re-checked when tools change:
  `[confirmed @ <your branch> | <tool>=<version>, <tool>=<version>]`, using the tool names from the
  "Tool versions" table in `docs/HANDOFF.md`.
- Don't reopen a settled choice. Check `docs/DECISIONS.md` first; if new facts change the answer, say so in your
  report instead of changing course.
- Every claim cites its evidence: file, address/offset, log, capture or test name.
- Keep each file's existing line endings (CRLF stays CRLF, LF stays LF).
- Commit with the project's git identity. Small commits with clear messages.

## Never
- Commit copyrighted or third-party files: games, ROMs, saves, assets, proprietary binaries or code. Reference them
  by path; the user supplies their own.
- Touch real user data, real logs, real save files or real network ports in tests. Use copies and fixtures.
- Change files outside the repo, or install system-wide software, without the prompt saying so.

## Tool versions
Before you start, record the versions you're using (compiler, SDK, emulator, loaders, mods: whatever the project
lists under "Tool versions" in `docs/HANDOFF.md`). If any differ from that table, say so at the top of your report.
Version mismatches are a common hidden cause of bugs.

## Stop and report
Stop working and write your report (below) when any of these happen. A clear "here's what I know and where I'm
stuck" is more useful than more attempts.
- The same fix or approach has failed **3 times**.
- You need a file, tool, permission or piece of information you don't have.
- What you find **contradicts a fact marked confirmed** in the docs or your prompt.
- The task turns out much bigger than the prompt expected (e.g. it needs changes in areas the prompt didn't mention).
- Your prompt's own stop conditions are met.

## Your report
When you finish or stop, write `docs/reports/<MILESTONE>-<slug>.md` using the format in
`docs/reports/TEMPLATE.md`, check it with `python scripts/check-report.py <your report>`, commit it on your
branch, and reply with its path plus a 3-line summary. The coordinator reads
the report from your branch, so it must stand on its own.

## Agent-specific constraints: <agent name>
<!-- Start from your agent's profile in templates/agents/ (Antigravity, Codex, Claude Code, Cursor, generic).
     The coordinator fills this in for the coding agent you use: its tools, which ones fit which jobs, permission
     limits, and quirks. Example for an agent with a reverse-engineering toolkit and a multi-agent mode:
- <Toolkit>: use for disassembly, xrefs and struct layouts. Read-only on game files; never attach to the runtime
  install. Its claims need emulation or a real run before they count as confirmed.
- <Multi-agent mode>: only for tasks that split into independent parts. Never for one linear trace or a small fix.
- Process skills to use when they fit: systematic-debugging (root cause before fixes), test-driven-development,
  verification-before-completion.
-->
