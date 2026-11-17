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

## Adding it to an existing project
For a project that already has code or docs but no `HANDOFF.md`:

- **Claude Code:** `/agent-coordinator Adopt my existing project. Repo: <url or folder>. Coding agent: <...>.`
- **Claude apps:** `Use agent-coordinator. Adopt my existing project. Repo: <url or folder>. Coding agent: <...>.`

What happens:

| Step | What Claude does | Why |
|------|------------------|-----|
| Scan | Reads README, `docs/`, TODO/ROADMAP/CHANGELOG-style notes, build and test setup, `git log`, branches, tags. About 15–20 tool calls, no code tracing. | Learn what the project already knows without spending the coordinator's tokens on investigation. |
| Inventory | Maps your existing files onto the workflow's: roadmap → `MILESTONES.md`, notes → research docs. | Reuse, don't duplicate. Your files are linked, never moved or overwritten. |
| Create | Adds only what's missing: `docs/MILESTONES.md`, `docs/HANDOFF.md`, `docs/research/`, `docs/prompts/`. | The workflow needs these four; everything else stays as you had it. |
| Label | Marks facts from old docs **unverified** until tested; notes docs that contradict the code as gaps. | Old docs drift. Treating them as confirmed is how bad facts spread (see [[Memory Model]]). |
| Plan | Builds milestones from half-done branches, failing tests, TODOs and research gaps. Asks 1–3 questions only for real judgment calls. | The plan comes from the project's actual state, not a blank slate. |
| First prompt | M1, or an **M0 survey** if big parts of the code are undocumented: the agent maps them into `docs/research/` with citations. | Code tracing is the agent's job. The survey fills long-term memory before real work starts. |
| Commit | One docs-only commit, existing line endings kept. | Easy to review, and easy to revert. |

You don't need to choose between "start" and "adopt": Claude picks the mode from the repo. An empty repo gets the
kickoff, a repo with code but no `HANDOFF.md` gets adopted, and a repo with `HANDOFF.md` just continues.

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
