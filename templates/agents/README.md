# Agent profiles

Ready-made `## Agent-specific constraints` sections for common coding agents. When you name your agent, the
coordinator starts from its profile here instead of asking everything from scratch. It still asks which tools you
actually have installed, and fills in the gaps.

| Agent | Profile | Loads `AGENTS.md`? |
|-------|---------|--------------------|
| Google Antigravity | [antigravity.md](antigravity.md) | Yes (official docs) |
| OpenAI Codex | [codex.md](codex.md) | Yes (unverified here) |
| Claude Code | [claude-code.md](claude-code.md) | Via a one-line `CLAUDE.md` pointer |
| Cursor | [cursor.md](cursor.md) | Yes (unverified here) |
| Anything else | [generic.md](generic.md) | Listed under "Read first" in every prompt |

**How to use one:** copy everything below the `---` line of the profile into your `AGENTS.md`, replacing the empty
`## Agent-specific constraints: <agent name>` section. Then remove the tools you don't have.

**Facts are labeled.** Like everything else in this workflow, each claim about an agent is marked **confirmed**
(checked against the tool's own docs, with a link) or **unverified** (from secondary sources or memory). Agents
change fast. If you find something wrong, fix it and open a pull request: that's how these profiles stay useful.

**Adding a profile:** copy `generic.md`, fill it in for your agent, add a row to the table above, and open a PR.
