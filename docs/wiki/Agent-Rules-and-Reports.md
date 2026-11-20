# Agent Rules and Reports

Two files keep the coding agent on track: `AGENTS.md` tells it the rules before it starts, and its **report**
tells Claude what happened when it finishes.

## AGENTS.md

Template: [`templates/AGENTS.md`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/AGENTS.md). It goes at the root of your project. Most coding
agents load it automatically at the start of every task. Every prompt also lists it first under "Read first", so it
gets read even by an agent that doesn't load it on its own.

| Section | What it says |
|---------|--------------|
| Always | Work only on the named branch; look things up in the research index first; label findings confirmed / unverified / wrong with evidence, and **stamp** confirmed ones with the tool versions; don't reopen settled decisions; keep line endings. |
| Never | Merge, rebase onto main or tag; commit copyrighted or third-party files; touch real user data, logs, saves or ports in tests. |
| Tool versions | Record the versions you used; flag any that differ from `HANDOFF.md`. |
| Stop and report | 3 failed attempts, missing access, contradicts a confirmed fact, task much bigger than expected. |
| Your report | Write `docs/reports/<MILESTONE>-<slug>.md`, commit it on the branch and push the branch (never main). |
| Agent-specific constraints | Written by Claude for the agent *you* use (see below). |

### Agent-specific constraints
Ready-made profiles for Antigravity, Codex, Claude Code and Cursor live in
[`templates/agents/`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/tree/main/templates/agents), each
fact labeled confirmed or unverified. Claude starts from the profile for your agent, then asks which tools you have.

When you name your coding agent (at kickoff, when adopting a project, or when you switch agents), Claude fills in
`## Agent-specific constraints: <agent>`. It covers:

- **How the agent loads rules.** If it reads a different file (`GEMINI.md`, `CLAUDE.md`, `.cursor/rules/`...),
  Claude adds a one-line pointer there: "Follow AGENTS.md".
- **Its tools, and when to use each.** Process skills, analysis or reverse-engineering toolkits, multi-agent modes.
  Claude asks which ones you have installed rather than guessing.
- **Permission limits** for high-privilege tools: debuggers, process control, shell, network. For example, a
  reverse-engineering toolkit stays read-only on game files and never attaches to the runtime install.
- **Known quirks** that cost time: a sandbox with no network, a tool whose claims need separate proof.

Anything Claude isn't sure about is marked **unverified** until you or the agent confirm it.

**Why one file:** standing rules used to be copied into every prompt's Constraints section. Now prompts carry only
task-specific constraints. They're shorter, and a rule can't be left out of one by accident.

## Reports

Template: [`templates/REPORT.md`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/REPORT.md), copied into your project as
`docs/reports/TEMPLATE.md`.

The agent writes `docs/reports/<MILESTONE>-<slug>.md`, checks it with `check-report.py`, and commits it **on its
branch**:

| Section | Why Claude needs it |
|---------|---------------------|
| Status | done / stopped (which condition) / partial |
| Tool versions | Checked first against `HANDOFF.md`. A mismatch is a bug until explained. |
| What changed | Files and commits, so the review knows where to look |
| Findings | Each claim, its label, and its evidence: the spot-check list |
| Tests | The exact command and its summary line, to re-run |
| Stopped because | What was tried and what's needed, so the next prompt fixes the blocker instead of repeating it |
| Open questions | Decisions for you or Claude |

Claude reads it straight from the branch (`git show origin/<branch>:docs/reports/<file>`). You don't paste
summaries between apps, and the report becomes part of the repo's long-term memory once the branch merges. If your
agent can't commit, pasting its summary still works as a fallback.

## Stop conditions
An agent that keeps trying when it's stuck burns the most quota for the least result. Stopping turns that into a
useful report. The defaults are in `AGENTS.md`. Each prompt can add its own under **Stop and report if**, e.g.
"the checksum isn't CRC32", or "the fix needs changes outside SaveIO/".
