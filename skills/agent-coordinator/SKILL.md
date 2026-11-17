---
name: agent-coordinator
description: Use on projects where a separate coding agent (e.g. Antigravity/Gemini, Codex, another Claude) does the research and heavy coding, and when starting a new project with one. Claude kicks the project off, writes the agent's prompts, reviews its branches, merges and tags.
---

# Agent coordinator (Claude as the brain)

Split the work by strength and cost:
- **Claude = the brain.** Plans milestones, writes the agent's prompts, reviews its work, merges and tags.
- **Coding agent = the hands.** Does the research, tracing, investigations, big fixes and bulk code.
- **The user = the tester.** Runs the build on their real machine and reports what they see.
- **The repo = the memory.** Everything learned lives in committed docs, not in any chat.

Claude saves its tokens for judgment. It does **not** open new investigations or do major bug fixes itself — those
go to the agent as a prompt.

## Starting a new project (kickoff)
Run this when the user starts a fresh project, e.g. `/agent-coordinator` in Claude Code, or a message like
"Start a new project: <name>. Repo: <url or folder>. Goal: <...>. Coding agent: <...>."

If the repo already has `docs/HANDOFF.md`, this is **not** a new project: read HANDOFF.md, the status board and the
research docs it points to, then do its "First thing to do" instead.

1. **Get access.** Ask for the repo (GitHub link or local folder) if you don't have it. On a local folder, also ask
   for delete permission (git creates and removes `.lock` files).
2. **Scope.** If the goal is truly unclear, ask 1–3 sharp questions: what "done" looks like, which coding agent,
   and hard constraints (platform, language, what must never be committed). Otherwise start.
3. **Scaffold the memory** (don't overwrite files that already exist):
   - `docs/MILESTONES.md`: milestones M1..Mn, each with a one-line done-criterion; a progress log; a "Next" line.
   - `docs/HANDOFF.md`: setup and folder table, rules, "First thing to do", and the last line
     `[Paste the coding agent's latest summary here]`.
   - `docs/research/` (or `RESEARCH.md`) for findings, and `docs/prompts/` for agent prompts.
   Starter templates: `templates/` in https://github.com/Trooper-code/Trooper-s-Coordinator-Skills
4. **Write the first prompt** for M1 to `docs/prompts/M1-<slug>.md` (format below). If M1 is pure research, the
   agent's job is to fill `docs/research/`, not to write code.
5. **Commit** the scaffolding with a clear message.
6. **Reply briefly:** the milestone list, the one-line instruction to paste into the agent, and "paste its summary
   back here when it's done".

## Milestones and branches
- Break milestone-sized work into milestones. Each gets its own feature branch.
- **The agent never merges.** Claude reviews the branch, then merges and tags it (e.g. `m5-p4a`) once the user has
  tested it and it works.
- Track status in `docs/MILESTONES.md` (milestones, dated progress log, current "Next" step).

## Writing a prompt
Prompts go in `docs/prompts/<MILESTONE>-<slug>.md`, committed. They must be **self-contained** — the agent has none of
this chat's context. Sections:

1. **Read first** — the exact docs/files to read before starting.
2. **Goal** — one or two sentences.
3. **Branch** — the name, and which tag to branch from.
4. **Known facts** — exact paths, addresses, offsets, values; each marked **confirmed** or **unverified**.
5. **Tasks** — numbered.
6. **Tools** — name the agent's skills/tools that fit, and why (see below).
7. **Constraints** — e.g. never commit copyrighted or third-party files, tests must not touch real user data, logs
   or ports, keep existing line endings, git identity, **don't merge**.
8. **Acceptance checks** — which tests must pass; every claim must cite its evidence (file, address, log).
9. **Report back** — what the summary must contain: what changed, what's confirmed vs unverified, test results,
   open questions.

Then give the user a one-line instruction to paste into the agent, e.g.
"Read and follow `docs/prompts/M5-p4b-save-format.md`."

### Naming tools in prompts
Name the agent's tools when they fit, and say why. Examples:
- Process skills (e.g. superpowers): `systematic-debugging` (root cause before fixes), `test-driven-development`,
  `writing-plans`, `brainstorming`, `verification-before-completion`.
- Reverse-engineering / analysis tools (e.g. an MCP decompiler toolkit): use for disassembly, xrefs, struct layouts.
  Their claims still need proof (emulation, a real run) before they count as confirmed. If a tool has
  high-privilege features (debuggers, process control), the prompt must keep it **read-only** on the user's files.
- Multi-agent "swarm" modes: only for big tasks that split into **independent** parts (several unrelated
  subsystems, or build + tests + docs at once). They burn quota fast — never for one linear trace or a small fix.
  A swarm prompt must spell out each worker's part, files and done-criteria, and say the verifiers run the repo's
  tests.

## Reviewing the agent's work
The agent has been wrong before. Verify, don't trust:
1. Re-run its tests and proofs yourself.
2. Spot-check the addresses, offsets and claims it cites against the real files and logs.
3. Decode or check its output by hand.
4. List results as **bugs**, then **gaps**, then **nitpicks**.

**Budget rule:** if checking a claim needs new tracing beyond what the agent cited (roughly more than ~10 tool
calls), stop. Put it in the next prompt instead.

After review:
- **Works** → give the user exact test steps (what to do, what they should see). Once they confirm, merge, tag,
  and record it in the docs.
- **Doesn't work** → write the follow-up prompt with the bugs and gaps as tasks.

## Documentation rule
Every finding goes into the repo docs in the same session, marked **confirmed**, **unverified** or **wrong**, with
the evidence. Fix old claims that turned out wrong. Keep each file's existing line endings.

## Session handoffs
Pair this with the **project-handoff** skill. Suggest a handoff at the end of each review round or when context gets
large. The switch routine:
1. Claude updates and commits `docs/HANDOFF.md`.
2. The user runs whatever Claude asked for (logs, captures).
3. The user gives the agent its prompt.
4. New Claude chat: paste HANDOFF.md, with the agent's summary at the bottom.

Context stays small, and nothing gets lost between chats.
