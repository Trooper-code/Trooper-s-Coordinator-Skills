# Profile: Cursor

Status of these facts as of 2026-11: **unverified** in this repo. Confirm against Cursor's current rules docs.

---

## Agent-specific constraints: Cursor

**How it loads rules.** Cursor reads `AGENTS.md` at the repo root, plus `.cursor/rules/*.mdc` (unverified). If
your version doesn't load `AGENTS.md`, add `.cursor/rules/agents.mdc` that tells it to follow `AGENTS.md`, with
frontmatter setting it to always apply.

**Tools.**
- Agent mode's terminal, for builds and tests.
- Any MCP servers configured for this project (list them here).

**Permission limits.**
- Don't auto-run commands that touch files outside the repo.
- Never push to `main` or create tags.

**Quirks.**
- Edits accepted in the editor aren't commits. Commit your changes and your report on the branch before reporting
  done.
