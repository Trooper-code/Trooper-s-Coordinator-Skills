# Profile: OpenAI Codex

Status of these facts as of 2026-11: **unverified** in this repo (from Codex's documentation and the
[AGENTS.md spec](https://agents.md)). Confirm against Codex's current docs and update this line.

---

## Agent-specific constraints: Codex

**How it loads rules.** Codex reads `AGENTS.md` at the repo root, plus nested `AGENTS.md` files closer to the
files being edited (unverified). This file is loaded automatically, and no pointer file is needed.

**Tools.** Name the ones you have:
- Its sandboxed shell, for builds and tests. Run the acceptance checks from your prompt there.
- Any MCP servers configured for this project (list them here).

**Permission limits.**
- Keep the sandbox's default network and file restrictions unless the prompt says otherwise.
- Never run commands that touch files outside the repo.

**Quirks.**
- If the sandbox blocks a build or test step, stop and report it under "Stopped because". Don't work around the
  sandbox.
