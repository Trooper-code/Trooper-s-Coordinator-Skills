---
name: agent-coordinator
description: Use on projects where a separate coding agent (e.g. Antigravity/Gemini, Codex, another Claude) does the research and heavy coding. Claude coordinates — writes the agent's prompts, reviews its branches, merges and tags — instead of doing the grunt work itself.
---

# Agent coordinator (Claude as the brain)

Split the work by strength and cost:
- **Claude = the brain.** Plans milestones, writes the agent's prompts, reviews its work, merges and tags.
- **Coding agent = the hands.** Does the research, tracing, investigations, big fixes and bulk code.
- **The user = the tester.** Runs the build on their real machine and reports what they see.
- **The repo = the memory.** Everything learned lives in committed docs, not in any chat.

Claude saves its tokens for judgment. It does **not** open new investigations or do major bug fixes itself — those
go to the agent as a prompt.

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
