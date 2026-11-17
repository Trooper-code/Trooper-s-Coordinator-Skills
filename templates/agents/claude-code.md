# Profile: Claude Code (as the worker agent)

Status of these facts as of 2026-11: **unverified** in this repo. Confirm against Claude Code's current memory and
`CLAUDE.md` docs.

Use this when a second Claude Code session is the coding agent, separate from the coordinator chat.

---

## Agent-specific constraints: Claude Code

**How it loads rules.** Claude Code reads `CLAUDE.md`. Create a `CLAUDE.md` at the repo root containing just:

    @AGENTS.md

The `@` line imports this file (unverified: check that your version supports imports). If the repo already has a
`CLAUDE.md`, add that line to it instead of replacing it.

**Tools.**
- Skills installed in the session (e.g. superpowers process skills): `systematic-debugging` before any fix,
  `test-driven-development` for new code, `verification-before-completion` before reporting done.
- Subagents: only for independent parts of a big task, never for one linear trace.

**Permission limits.**
- Don't approve commands that touch files outside the repo or your branch.
- Never push to `main` or create tags.

**Quirks.**
- A worker session must not load the `agent-coordinator` skill as if it were the coordinator. If it does, ignore it:
  your job is this prompt, on this branch.
