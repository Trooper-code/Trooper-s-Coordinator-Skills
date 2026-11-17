# Profile: Google Antigravity

Status of these facts as of 2026-11: rules loading is **confirmed** against
[Antigravity's rules docs](https://antigravity.google/docs/rules); the rest is **unverified**.

---

## Agent-specific constraints: Antigravity

**How it loads rules.** Antigravity reads `AGENTS.md` and `GEMINI.md` from the workspace folder and every parent
up to the repo root, plus `.agents/rules/*.md` (confirmed). This file is loaded automatically, and no pointer file
is needed.
- If a `GEMINI.md` exists too, keep it from contradicting this file. Reported (unverified): `GEMINI.md` wins when
  the two conflict.
- Rule files in `.agents/rules/` need YAML frontmatter with a `trigger` (confirmed). `AGENTS.md` doesn't.
- Reported (unverified): a 12,000-character limit per rule file. Keep this file well under it.

**Tools.** Use these when they fit, and say which one you used in your report:
- Process skills (e.g. superpowers): `systematic-debugging` before any fix, `test-driven-development` for new
  code, `verification-before-completion` before reporting done.
- Reverse-engineering or analysis MCP toolkits (decompilers, static analysis): for disassembly, xrefs, struct
  layouts. Their output is **unverified** until proven by emulation, a test or a real run.
- Multi-agent / swarm modes: only when the prompt says the task splits into independent parts. Never for one
  linear trace or a small fix, because they use quota much faster.

**Permission limits.**
- High-privilege tools (debuggers, process attach, shell): read-only on game files, and never attach to the user's
  real runtime install. Work on copies.
- No network calls to live game or online services.

**Quirks.**
- Long runs can drift from the prompt. Re-read your prompt's Goal and Stop conditions before writing the report.
- Commit the report on your branch. Don't only paste it in chat: the coordinator reads it from the repo.
