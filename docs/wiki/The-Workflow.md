# The Workflow

## Roles
| Who | Job |
|-----|-----|
| **Claude** (coordinator) | Splits work into milestones, writes the agent's prompts, reviews its branches, merges and tags. |
| **Coding agent** (e.g. Antigravity/Gemini) | Research, tracing, investigations, big fixes, bulk code. Works on a branch. **Never merges.** |
| **You** | Pass prompts and summaries between the two, and test on your real machine. |
| **The repo** | The memory. Findings, status and the next step live in committed docs. |

## Starting a new project
Open a fresh chat and kick it off:

- **Claude Code:** `/agent-coordinator Start a new project: <name>. Repo: <url or folder>. Goal: <...>. Coding agent: <...>.`
- **Claude apps:** `Use agent-coordinator. Start a new project: <name>. Repo: <url or folder>. Goal: <...>. Coding agent: <...>.`

Claude asks for repo access (and 1–3 questions only if the goal is unclear), scaffolds `docs/MILESTONES.md`,
`docs/HANDOFF.md`, `docs/research/` and `docs/prompts/`, plans the milestones, writes the first agent prompt, commits,
and hands you the line to paste into the agent. If the repo already has a `HANDOFF.md`, it continues from that
instead of starting over.

## The loop
1. **Plan.** Tell Claude the goal. It breaks it into milestones in `docs/MILESTONES.md`.
2. **Prompt.** Claude writes `docs/prompts/<MILESTONE>-<slug>.md`, commits it, and gives you one line to paste
   into the agent.
3. **Work.** The agent reads the prompt, works on its own branch, writes findings into the docs, and reports back.
4. **Review.** Paste the agent's summary into Claude. Claude re-runs the tests, spot-checks the claims and lists
   **bugs → gaps → nitpicks**.
5. **Test.** Claude gives you exact test steps: what to do and what you should see.
6. **Merge or retry.** It works → Claude merges and tags it (e.g. `m2-p1`). It doesn't → Claude writes the
   follow-up prompt, and you go back to step 3.
7. **Handoff.** When the chat gets long, or at the end of a review round, say "update the handoff" and start a
   new chat. See [[Session Handoffs]].

## What Claude should *not* do
Open new investigations or do big bug fixes itself. If checking something needs more than ~10 tool calls of new
tracing, it goes into the next prompt instead. That rule is what keeps the expensive model cheap.

## When to use a swarm / multi-agent mode
Only when the task splits into **independent** parts (unrelated subsystems, or build + tests + docs at once).
It burns quota fast. Never use it for one linear trace or a small fix.
