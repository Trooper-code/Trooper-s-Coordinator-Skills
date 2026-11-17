---
name: agent-coordinator
description: Use on projects where a separate coding agent (e.g. Antigravity/Gemini, Codex, another Claude) does the research and heavy coding, and when starting a new project with one, adding one to an existing project, importing research results, cutting a release, or asking for project status. Claude sets the project up, writes the agent's prompts, reviews its branches, merges and tags.
---

# Agent coordinator (Claude as the brain)

Split the work by strength and cost:
- **Claude = the brain.** Plans milestones, writes the agent's prompts, reviews its work, merges and tags.
- **Coding agent = the hands.** Does the research, tracing, investigations, big fixes and bulk code.
- **The user = the tester.** Runs the build on their real machine and reports what they see.
- **The repo = the memory.** Everything learned lives in committed docs, not in any chat.

Claude saves its tokens for judgment. It does **not** open new investigations or do major bug fixes itself — those
go to the agent as a prompt.

**Templates and scripts** for every file below: this skill's `templates/` folder (included in the release zips),
or `templates/` in https://github.com/Trooper-code/Trooper-s-Coordinator-Skills. Detail for some modes is in this
skill's `reference/` folder; read that file when the mode comes up.

## Pick the mode
| The user says / the repo has | Mode |
|------------------------------|------|
| "status", "where are we" | **Status** (below) |
| "release v…", "cut a release", "tag this" | **Release**: follow `reference/release.md` |
| "import research", pasted deep-research results | **Research import**: follow `reference/research-import.md` |
| repo has `docs/HANDOFF.md` | **Continue**: read HANDOFF.md, the status board and the docs it points to, then do its "First thing to do" |
| repo has code or docs, no HANDOFF.md | **Adopt** (below) |
| empty repo (or only README/LICENSE/.gitignore) | **Kickoff** (below) |

If you can run commands, `python templates/scripts/detect-mode.py <repo>` decides the last three and lists the
workflow files the repo has and is missing.

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
2. **Scope.** If the goal is truly unclear, ask 1–3 sharp questions: what "done" looks like, which coding agent and
   which of its tools the user has, and hard constraints (platform, language, what must never be committed).
   Otherwise start.
3. **Scaffold the memory** (don't overwrite files that already exist):
   - `AGENTS.md`, with the agent-specific section filled in (see "The agent's rules file").
   - `docs/MILESTONES.md`, `docs/HANDOFF.md` (with **Tool versions**), `docs/DECISIONS.md`,
     `docs/research/INDEX.md`, `docs/prompts/`, `docs/reports/TEMPLATE.md`, `CHANGELOG.md`.
   - `scripts/`: the check scripts (see `reference/scripts.md`).
   - Safety and releases: `templates/hooks/pre-commit` copied to `scripts/hooks/pre-commit` (hooks themselves
     aren't committed, so the user installs it once with `cp scripts/hooks/pre-commit .git/hooks/pre-commit`), plus
     `.github/workflows/checks.yml` and `.github/workflows/release.yml`.
4. **Write the first prompt** for M1 to `docs/prompts/M1-<slug>.md` and run `check-prompt.py` on it. If M1 is pure
   research, the agent's job is to fill `docs/research/`, not to write code.
5. **Commit** the scaffolding with a clear message.
6. **Reply briefly:** the milestone list, the one-line instruction to paste into the agent, the hook install
   command, and "tell me when it's done; its report will be in `docs/reports/` on its branch".

## Adopt (existing project)
E.g. `/agent-coordinator Adopt my existing project. Repo: <url or folder>. Coding agent: <...>.`

Learn what the project already knows, plan from it, and add only the docs that are missing. The scan is **reading
docs and repo structure, not investigating code**: anything that needs tracing goes to the agent.

1. **Get access**, as in the kickoff.
2. **Scan** (budget: about 15–20 tool calls; `detect-mode.py` does the inventory in one). Read, don't trace:
   - top-level layout, build files and test setup (language, how it builds and tests, **which tool versions**);
   - `README`, everything under `docs/`, `RESEARCH.md`, `NOTES.md`, `TODO.md`, `ROADMAP.md`, `CHANGELOG.md`;
   - existing agent rules files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/`, `.agents/rules/`);
   - `git log --oneline -30`, branches and tags: what was done last, what's half-finished;
   - TODO/FIXME comments, if cheap to list (`git grep -n "TODO\|FIXME"`).
3. **Inventory.** Map what exists onto the workflow's files. Reuse what does the job: link an existing roadmap from
   `MILESTONES.md`, keep existing research docs where they are and index them, and add missing sections to an
   existing rules file instead of replacing it. **Create only what's missing. Never overwrite, move or rename the
   user's files.**
4. **Label what you learned.** Facts from existing docs or comments are **unverified** until tested. Note
   contradictions between docs and code as gaps. Record past choices you can see (a library picked, a format
   chosen) in `DECISIONS.md` only if the docs say why; otherwise list them as open questions.
5. **Run `check-safe-to-publish.py`** on the whole repo. If anything is flagged, tell the user first: removing a
   committed file from history is their call.
6. **Plan ahead**: finish half-done branches, fix failing tests, close TODOs, fill research gaps. Milestones with
   done-criteria into `docs/MILESTONES.md`. Real judgment calls (rewrite vs. fix, which feature first) → ask 1–3
   sharp questions before committing to the plan.
7. **First prompt.** Large parts of the code undocumented → **M0: survey** (the agent maps them into
   `docs/research/` and the index, every claim cited and labeled). Otherwise, M1.
8. **Write `docs/HANDOFF.md`**, run `check-handoff.py`, and commit the new docs in one commit (e.g. "Add coordinator
   docs"), keeping each existing file's line endings.
9. **Reply briefly:** what you learned, files created or extended, the plan, anything that needs the user's call,
   and the one line to paste into the agent.

## The agent's rules file (AGENTS.md)
Standing rules live in `AGENTS.md` at the repo root, so prompts only carry what's specific to their task. It holds
always/never rules, the tool-versions and stamping rules, the stop conditions, the report format, and an
**agent-specific section**.

**Agent-specific constraints are required.** Whenever the user names their coding agent (kickoff, adopt, or a
switch), fill in `## Agent-specific constraints: <agent>`:
- **Start from the profile** in `templates/agents/` (Antigravity, Codex, Claude Code, Cursor, generic). Keep its
  confirmed/unverified labels.
- **Ask which tools the user has installed**, and remove the ones they don't.
- **How it loads rules.** If the profile says the agent reads another file, create the pointer it describes. If
  unsure, say so and keep `AGENTS.md` first under "Read first" in every prompt.
- **Permission limits** for high-privilege tools, and **known quirks**.
- When the user or the agent corrects a profile fact, fix it in `AGENTS.md`, and suggest fixing the shared profile
  upstream too.

## Milestones and branches
- Break milestone-sized work into milestones. Each gets its own feature branch.
- **The agent never merges.** Claude reviews the branch, then merges and tags it (e.g. `m5-p4a`) once the user has
  tested it and it works.
- Track status in `docs/MILESTONES.md` (milestones, dated progress log, current "Next" step).

## Writing a prompt
Prompts go in `docs/prompts/<MILESTONE>-<slug>.md`, committed, **self-contained** (the agent has none of this chat's
context). Sections, as in `templates/PROMPT.md`:

1. **Read first**: `AGENTS.md` first; then `docs/research/INDEX.md` and the sections this task needs; any
   `DECISIONS.md` entries it touches.
2. **Goal**: one or two sentences.
3. **Branch**: the name, and which tag to branch from.
4. **Known facts**: exact paths, addresses, offsets, values; each **confirmed** or **unverified**, with evidence.
5. **Tasks**: numbered. If `check-research.py` found facts proven on older tool versions that this task relies on,
   re-checking them is a task.
6. **Tools**: the agent's tools that fit this task, and why.
7. **Task-specific constraints**: only what `AGENTS.md` doesn't already say.
8. **Stop and report if**: the AGENTS.md stop conditions, plus any for this task.
9. **Acceptance checks**: which tests must pass; every claim cites its evidence.
10. **Report**: `docs/reports/<MILESTONE>-<slug>.md`, committed on the branch.

Run `check-prompt.py` on it, fix what it reports, then give the user a one-line instruction for the agent, e.g.
"Read and follow `docs/prompts/M5-p4b-save-format.md`."

**Naming tools.** Process skills (e.g. superpowers: `systematic-debugging`, `test-driven-development`,
`verification-before-completion`); analysis or reverse-engineering toolkits (their claims need proof by emulation,
a test or a real run; keep high-privilege features read-only on the user's files); multi-agent "swarm" modes only
for big tasks that split into independent parts — a swarm prompt spells out each worker's part, files and
done-criteria, and says the verifiers run the repo's tests.

## Reviewing the agent's work
Read the report from the branch: `git fetch origin <branch>` then
`git show origin/<branch>:docs/reports/<file>`. Only ask the user to paste a summary if the report isn't there.

The agent has been wrong before. Verify, don't trust:
1. **`check-report.py`** on the report. A report that fails goes back to the agent, unless the gaps are trivial.
2. **Tool versions** in the report against `docs/HANDOFF.md`. A mismatch is a bug until explained.
3. Re-run its tests and proofs yourself.
4. Spot-check the addresses, offsets and claims it cites against the real files and logs. Check that confirmed
   findings are **stamped** (`[confirmed @ <branch> | tool=version]`) and new sections are in the research index;
   run `check-research.py`.
5. Decode or check its output by hand.
6. List results as **bugs**, then **gaps**, then **nitpicks**.

**Budget rule:** if checking a claim needs new tracing beyond what the agent cited (roughly more than ~10 tool
calls), stop. Put it in the next prompt instead.

If the agent **stopped**, don't redo its work: decide what it needs (access, a file, a corrected fact, a smaller
task) and write that into the next prompt.

After review:
- **Works** → give the user exact test steps (what to do, what they should see). Once they confirm, merge, tag, add
  a line under `## Unreleased` in `CHANGELOG.md`, and record it in the docs.
- **Doesn't work** → write the follow-up prompt with the bugs and gaps as tasks.
- **Abandon instead** after **two failed review rounds**, or when the fix heads the wrong way: keep the branch
  (rename it `abandoned/<name>` if the user agrees), record why in the research docs and as a Lesson, keep any
  confirmed findings, and write a fresh prompt from the **last good tag**.

## Keeping the memory sharp
- **Decisions.** When the user makes a real choice between options (a format, a library, rewrite vs. fix), add an
  entry to `docs/DECISIONS.md`: decided, rejected, why, revisit-if. Before reopening a settled question, read its
  entry; new facts get a **new** entry that supersedes the old one.
- **Research index.** Every research topic has one line in `docs/research/INDEX.md` pointing to its file and
  section. Look things up there first; keep it current when sections move.
- **Version-aware facts.** Confirmed facts carry a stamp of the tag and tool versions they were proven on. Whenever
  the Tool versions table changes, run `check-research.py` and put re-checking the listed facts into the next
  prompt.
- **Lessons become rules.** A lesson hit a second time gets `(x2)` in HANDOFF.md, then moves into `AGENTS.md` (a
  rule for the agent), a check script (if it can be automated), or the prompt template.
- **Findings rule.** Every finding goes into the repo docs in the same session, labeled **confirmed**,
  **unverified** or **wrong**, with evidence. Fix old claims that turned out wrong. Keep line endings.
- **Safe to publish.** Nothing copyrighted or personal gets committed: the pre-commit hook and CI run
  `check-safe-to-publish.py`. Users supply their own game files.

## Session handoffs
Pair this with the **project-handoff** skill. Suggest a handoff at the end of each review round or when context gets
large. The switch routine:
1. Claude updates `docs/HANDOFF.md`, runs `check-handoff.py`, and commits.
2. The user runs whatever Claude asked for (logs, captures).
3. The user gives the agent its prompt.
4. New Claude chat: paste HANDOFF.md (or, if the chat can read the repo, "Read docs/HANDOFF.md and do its First
   thing to do"). The agent's report is already on its branch, so nothing else needs pasting.
