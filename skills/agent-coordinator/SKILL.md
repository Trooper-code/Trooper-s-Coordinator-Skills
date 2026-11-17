---
name: agent-coordinator
description: Use on projects where a separate coding agent (e.g. Antigravity/Gemini, Codex, another Claude) does the research and heavy coding, and when starting a new project with one, adding one to an existing project, or asking for project status. Claude sets the project up, writes the agent's prompts, reviews its branches, merges and tags.
---

# Agent coordinator (Claude as the brain)

Split the work by strength and cost:
- **Claude = the brain.** Plans milestones, writes the agent's prompts, reviews its work, merges and tags.
- **Coding agent = the hands.** Does the research, tracing, investigations, big fixes and bulk code.
- **The user = the tester.** Runs the build on their real machine and reports what they see.
- **The repo = the memory.** Everything learned lives in committed docs, not in any chat.

Claude saves its tokens for judgment. It does **not** open new investigations or do major bug fixes itself — those
go to the agent as a prompt.

Starter templates for every file below: `templates/` in https://github.com/Trooper-code/Trooper-s-Coordinator-Skills

## Pick the mode
| The user says / the repo has | Mode |
|------------------------------|------|
| "status", "where are we" | **Status** (below) |
| repo has `docs/HANDOFF.md` | **Continue**: read HANDOFF.md, the status board and the docs it points to, then do its "First thing to do" |
| repo has code or docs, no HANDOFF.md | **Adopt** (below) |
| empty repo, or nothing yet | **Kickoff** (below) |

## Status
For "Use agent-coordinator. Status." or "where are we on <project>?". Cheap on purpose:
- Read **only** `docs/MILESTONES.md` and `docs/HANDOFF.md` (and `git log --oneline -5` if you have the repo).
- Answer in about five lines: current milestone and its state, what's in progress and who has it, the last tested
  result, the next step, and anything waiting on the user.
- Don't review, test or open other files unless asked.

## Kickoff (new project)
E.g. `/agent-coordinator Start a new project: <name>. Repo: <url or folder>. Goal: <...>. Coding agent: <...>.`

1. **Get access.** Ask for the repo (GitHub link or local folder) if you don't have it. On a local folder, also ask
   for delete permission (git creates and removes `.lock` files).
2. **Scope.** If the goal is truly unclear, ask 1–3 sharp questions: what "done" looks like, which coding agent,
   and hard constraints (platform, language, what must never be committed). Otherwise start.
3. **Scaffold the memory** (don't overwrite files that already exist):
   - `AGENTS.md`: the agent's standing rules, **with the agent-specific section filled in** (see "The agent's rules
     file" below).
   - `docs/MILESTONES.md`: milestones M1..Mn, each with a one-line done-criterion; a progress log; a "Next" line.
   - `docs/HANDOFF.md`: setup, **tool versions**, rules, "First thing to do", and the summary placeholder as the last
     line.
   - `docs/research/` (or `RESEARCH.md`), `docs/prompts/`, and `docs/reports/TEMPLATE.md` (the report format).
   - `scripts/check-handoff.py`.
4. **Write the first prompt** for M1 to `docs/prompts/M1-<slug>.md`. If M1 is pure research, the agent's job is to
   fill `docs/research/`, not to write code.
5. **Commit** the scaffolding with a clear message.
6. **Reply briefly:** the milestone list, the one-line instruction to paste into the agent, and "tell me when it's
   done; its report will be in `docs/reports/` on its branch".

## Adopt (existing project)
E.g. `/agent-coordinator Adopt my existing project. Repo: <url or folder>. Coding agent: <...>.`

The goal: learn what the project already knows, plan from it, and add only the docs that are missing. The scan is
**reading docs and repo structure, not investigating code**: anything that needs tracing goes to the agent.

1. **Get access**, as in the kickoff.
2. **Scan** (budget: about 15–20 tool calls). Read, don't trace:
   - top-level layout, build files and test setup (language, how it builds, how tests run, **which tool versions**);
   - `README`, everything under `docs/`, and files like `RESEARCH.md`, `NOTES.md`, `TODO.md`, `ROADMAP.md`,
     `CHANGELOG.md`, `CONTRIBUTING.md`;
   - any existing agent rules files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.github/copilot-instructions.md`;
   - `git log --oneline -30`, branches (`git branch -a`) and tags: what was done last, what's half-finished;
   - TODO/FIXME comments, if they're cheap to list (`git grep -n "TODO\|FIXME"`).
3. **Inventory.** Map what exists onto the files this workflow needs:

   | Needed | Use what's there if it does the job |
   |--------|--------------------------------------|
   | `AGENTS.md` (agent rules) | an existing rules file: add the missing sections to it, don't replace it |
   | `docs/MILESTONES.md` (status board) | an existing roadmap or TODO list: link it, don't copy it |
   | `docs/research/` or `RESEARCH.md` (findings) | existing notes/research docs: keep them where they are |
   | `docs/prompts/`, `docs/reports/TEMPLATE.md` | — |
   | `docs/HANDOFF.md`, `scripts/check-handoff.py` | — |

   **Create only what's missing. Never overwrite, move or rename the user's files.** Point to them instead.
4. **Label what you learned.** Facts from existing docs or comments are **unverified** until tested or proven.
   Mark something **confirmed** only with evidence (a passing test, a real run). Note contradictions between docs
   and code as gaps.
5. **Plan ahead** from what you found: finish half-done branches, fix failing tests, close TODOs, fill research gaps.
   Write milestones M1..Mn with done-criteria into `docs/MILESTONES.md`, and a "Next" line. If direction is a real
   judgment call (rewrite vs. fix, which feature first), ask 1–3 sharp questions before committing to the plan.
6. **Write the first prompt.** If large parts of the code are undocumented, make it **M0: survey**: the agent maps
   those areas into `docs/research/`, with every claim cited and labeled. Otherwise, write the prompt for M1.
7. **Write `docs/HANDOFF.md`** (including the tool versions you found) and run `python scripts/check-handoff.py`.
8. **Commit** the new docs only, in one commit (e.g. "Add coordinator docs"). Keep each existing file's line
   endings; match the repo's style for new ones.
9. **Reply briefly:** what you learned, the files you created or extended, the milestone plan, anything that needs
   the user's call, and the one line to paste into the agent.

## The agent's rules file (AGENTS.md)
Standing rules live in `AGENTS.md` at the repo root, so each prompt only carries what's specific to its task. Most
coding agents load it automatically. It holds: always/never rules (never merge; no copyrighted or third-party
files; tests never touch real data, logs or ports; keep line endings; evidence for every claim), the tool-versions
rule, the stop conditions, the report format, and an **agent-specific section**.

**Agent-specific constraints are required.** Whenever the user names their coding agent (kickoff, adopt, or a
later switch), fill in `## Agent-specific constraints: <agent>` for that app:
- **How it loads rules.** If you know it reads a different file (e.g. `GEMINI.md`, `CLAUDE.md`, `.cursor/rules/`),
  add a one-line pointer file there ("Follow AGENTS.md"). If you aren't sure whether it loads `AGENTS.md`, say so,
  ask the user, and keep `AGENTS.md` under "Read first" in every prompt so it's read either way.
- **Its tools, and when to use each**: process skills, analysis/reverse-engineering toolkits, multi-agent modes.
  Ask the user which ones they have installed rather than guessing.
- **Permission limits** for high-privilege tools (debuggers, process control, shell, network): e.g. read-only on
  game files, never attach to the runtime install.
- **Known quirks** that cost time (e.g. a sandbox without network, a tool whose claims need a separate proof).
- Mark anything you're not sure about as **unverified**, and fix it when the agent or the user corrects it.

If the user switches agents, add a new agent-specific section (or replace the old one) before the next prompt.

## Milestones and branches
- Break milestone-sized work into milestones. Each gets its own feature branch.
- **The agent never merges.** Claude reviews the branch, then merges and tags it (e.g. `m5-p4a`) once the user has
  tested it and it works.
- Track status in `docs/MILESTONES.md` (milestones, dated progress log, current "Next" step).

## Writing a prompt
Prompts go in `docs/prompts/<MILESTONE>-<slug>.md`, committed. They must be **self-contained**: the agent has none
of this chat's context. Sections:

1. **Read first**: `AGENTS.md` first, then the exact docs/files for this task.
2. **Goal**: one or two sentences.
3. **Branch**: the name, and which tag to branch from.
4. **Known facts**: exact paths, addresses, offsets, values; each marked **confirmed** or **unverified**.
5. **Tasks**: numbered.
6. **Tools**: name the agent's tools that fit this task, and why.
7. **Task-specific constraints**: only what `AGENTS.md` doesn't already say.
8. **Stop and report if**: the AGENTS.md stop conditions, plus any specific to this task (e.g. "the checksum
   isn't CRC32", "the fix needs changes outside SaveIO/").
9. **Acceptance checks**: which tests must pass; every claim cites its evidence.
10. **Report**: write `docs/reports/<MILESTONE>-<slug>.md` using `docs/reports/TEMPLATE.md`, commit it on the
    branch, and reply with its path plus a 3-line summary.

Then give the user a one-line instruction to paste into the agent, e.g.
"Read and follow `docs/prompts/M5-p4b-save-format.md`."

### Naming tools in prompts
Name the agent's tools when they fit, and say why. Examples:
- Process skills (e.g. superpowers): `systematic-debugging` (root cause before fixes), `test-driven-development`,
  `writing-plans`, `brainstorming`, `verification-before-completion`.
- Reverse-engineering / analysis tools (e.g. an MCP decompiler toolkit): use for disassembly, xrefs, struct layouts.
  Their claims still need proof (emulation, a real run) before they count as confirmed. If a tool has
  high-privilege features (debuggers, process control), keep it **read-only** on the user's files.
- Multi-agent "swarm" modes: only for big tasks that split into **independent** parts (several unrelated
  subsystems, or build + tests + docs at once). They burn quota fast — never for one linear trace or a small fix.
  A swarm prompt must spell out each worker's part, files and done-criteria, and say the verifiers run the repo's
  tests.

## Reviewing the agent's work
The agent's report is in the repo: `docs/reports/<MILESTONE>-<slug>.md` on its branch. Read it from there
(`git fetch origin <branch>` then `git show origin/<branch>:docs/reports/<file>`, or check out the branch). Only
ask the user to paste a summary if the report isn't there.

The agent has been wrong before. Verify, don't trust:
1. **Check tool versions** in the report against `docs/HANDOFF.md`. A mismatch is a bug until explained.
2. Re-run its tests and proofs yourself.
3. Spot-check the addresses, offsets and claims it cites against the real files and logs.
4. Decode or check its output by hand.
5. List results as **bugs**, then **gaps**, then **nitpicks**.

**Budget rule:** if checking a claim needs new tracing beyond what the agent cited (roughly more than ~10 tool
calls), stop. Put it in the next prompt instead.

If the agent **stopped** (its report says which stop condition), don't redo its work: decide what it needs (access,
a file, a corrected fact, a smaller task) and write that into the next prompt.

After review:
- **Works** → give the user exact test steps (what to do, what they should see). Once they confirm, merge, tag,
  and record it in the docs (the report merges with the branch).
- **Doesn't work** → write the follow-up prompt with the bugs and gaps as tasks.
- **Abandon instead** when a branch has failed **two review rounds**, or the fix is heading the wrong way (growing
  workarounds, touching areas the milestone shouldn't). Then:
  1. keep the branch (rename it `abandoned/<name>` if the user agrees) so nothing is lost;
  2. record why in the research docs and as a Lesson in HANDOFF.md, and keep any confirmed findings;
  3. write a fresh prompt that starts from the **last good tag**, with what was learned as known facts.

## Documentation rule
Every finding goes into the repo docs in the same session, marked **confirmed**, **unverified** or **wrong**, with
the evidence. Fix old claims that turned out wrong. Keep each file's existing line endings. Keep the
**Tool versions** table in HANDOFF.md current whenever a version changes.

## Session handoffs
Pair this with the **project-handoff** skill. Suggest a handoff at the end of each review round or when context gets
large. The switch routine:
1. Claude updates `docs/HANDOFF.md`, runs `python scripts/check-handoff.py`, and commits.
2. The user runs whatever Claude asked for (logs, captures).
3. The user gives the agent its prompt.
4. New Claude chat: paste HANDOFF.md (or, if the chat can read the repo, just "Read docs/HANDOFF.md and do its First
   thing to do"). The agent's report is already on its branch, so nothing else needs pasting.

Context stays small, and nothing gets lost between chats.
