# Trooper's Coordinator Skills

Skills I made while doing agentic coding with two agents. They keep context small, cut token use on expensive
models, and give the two agents a clear split of the work.

The idea: **Claude is the coordinator** (plans, writes prompts, reviews, merges). **A second coding agent**
(I use Antigravity with Gemini, but any agent works) **does the grunt work**: research, tracing, big fixes.
**The repo is the memory**, so you can start a fresh chat at any time and lose nothing.

## The skills

| Skill | What it does |
|-------|--------------|
| [`agent-coordinator`](skills/agent-coordinator/SKILL.md) | Makes Claude act as the coordinator: writes self-contained prompts for the coding agent, reviews its branches (bugs → gaps → nitpicks), merges and tags. Keeps Claude out of expensive investigations. |
| [`project-handoff`](skills/project-handoff/SKILL.md) | Ends a session cleanly: writes every finding to the repo docs, updates a short `docs/HANDOFF.md`, and commits, so the next chat starts with full context from one small paste. |

They work on their own, but they're built to be used together.

## Install

**Claude Code**: copy the folders from `skills/` into `~/.claude/skills/` (all your projects) or
`<your-project>/.claude/skills/` (one project).

**Claude apps (claude.ai / desktop / mobile)**: zip one skill folder (e.g. `agent-coordinator/` with its
`SKILL.md` inside) and upload it in your skills settings. Do it once per skill.

**Already have a skill with the same name?** Rename the folder and the `name:` line in its `SKILL.md` first,
or the two will clash.

## Quick start

1. Copy the files from [`templates/`](templates) into your project's `docs/` folder:
   `HANDOFF.md`, `MILESTONES.md`, and `PROMPT.md` (the prompt template goes in `docs/prompts/`).
2. Tell Claude what you want to build. It breaks the work into milestones and writes the first prompt to
   `docs/prompts/`.
3. Give your coding agent the one-line instruction Claude hands you (e.g.
   "Read and follow `docs/prompts/M1-save-format.md`").
4. When the agent finishes, paste its summary back to Claude. Claude reviews the branch and gives you test steps.
   If it works, Claude merges and tags it. If not, Claude writes the follow-up prompt.
5. When the chat gets long, say **"update the handoff"**, then start a new chat and paste `docs/HANDOFF.md`.

**Full guide:** see the [wiki](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/wiki) for the
whole workflow, how to write good prompts, how to review agent work, and the handoff routine.

## Repo layout

```
skills/
  agent-coordinator/SKILL.md
  project-handoff/SKILL.md
templates/
  HANDOFF.md      -> docs/HANDOFF.md
  MILESTONES.md   -> docs/MILESTONES.md
  PROMPT.md       -> docs/prompts/<MILESTONE>-<slug>.md
```

## Contributing

Issues and pull requests are welcome, especially if you adapt these for another coding agent (Codex, Cursor,
another Claude, etc.) and want to share what you changed.

## License

[MIT](LICENSE). Use them, change them, share them.
