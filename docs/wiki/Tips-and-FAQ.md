# Tips and FAQ

**Does it have to be Antigravity/Gemini?**
No. Any coding agent that can read files in your repo and work on a branch works: Codex, Cursor, another Claude
session, and so on.

**Do I need both skills?**
No, but they're built to work together. `project-handoff` alone is still useful for any long project.

**Why does Claude refuse to just fix the bug itself?**
That's the point of `agent-coordinator`: Claude's tokens go to planning and review. If you *want* Claude to do
it, say so; your request wins.

**My skill upload fails on claude.ai.**
A skill's name can't contain "claude" or "anthropic", and the description can't contain `<` or `>`. Rename it in the `name:` line and the folder. If you edited a skill from this repo, run `python scripts/validate.py`: it checks for these.

**Line endings got mangled.**
Both skills tell Claude to keep each file's existing line endings (CRLF stays CRLF). If it happens anyway, point
Claude at the file and ask it to check with `file <name>`.

**Git fails with `.lock` errors.**
Claude needs permission to delete files in the repo folder (git creates and removes lock files). Grant delete
permission when asked.

**Don't commit copyrighted stuff.**
Game files, ROMs, saves, assets and binaries stay out of the repo. Have users supply their own files. The prompt
template's constraints say this so the agent doesn't forget.

**How big should HANDOFF.md be?**
About 100 lines / 10 KB. Every new chat pays for every line of it on every turn. If it keeps growing, history is
leaking in: dated progress belongs in `MILESTONES.md`, and findings belong in the research docs. See
[[Memory Model]] for the token math.

**Can I use prompt caching instead of handoffs?**
Caching makes re-read tokens cheaper, but they still fill the context window, and models get worse at using
information buried in a long context. Handoffs fix both problems; caching only helps with one.

**Will my coding agent actually read AGENTS.md?**
Many coding agents load `AGENTS.md` automatically. If yours reads a different file, Claude adds a one-line pointer
there. Every prompt also lists `AGENTS.md` first under "Read first", so it gets read either way.

**I switched coding agents. What changes?**
Tell Claude. It adds (or replaces) the agent-specific section in `AGENTS.md` before the next prompt, with that
app's tools, limits and quirks. Everything else stays the same.

**Is there a quick way to see where a project is?**
`Use agent-coordinator. Status.` It reads two files and answers in about five lines.

**What Python do the scripts need?**
Python 3.9 or newer, standard library only, so there's nothing to `pip install`. On Windows, `python` from
python.org or the Microsoft Store works.

**Does the pre-commit hook work on Windows?**
Yes. Git for Windows runs hooks with its own shell, from PowerShell, cmd and GUI clients alike. Python must be on
your PATH. To skip it once on purpose: `git commit --no-verify`, though CI still checks on push.

**The copyright guard flagged a file I made myself.**
Add its path to `.publish-allowlist` with a comment saying what it is, e.g.
`tests/fixtures/tiny.sav  # 64 bytes, made by hand for the parser test`.

**How do I test changes to the skills themselves?**
The scripts have automated tests. For what a skill makes Claude do, walk through the matching rows of
`tests/SCENARIOS.md` in a fresh chat.

**Where do the check scripts go: `scripts/` or `docs/scripts/`?**
Either. `scripts/` at the repo root is the default; use `docs/scripts/` if you'd rather keep all the workflow files
under `docs/`. Claude, the pre-commit hook and both workflow templates look in both and use whichever your project
has. Keep all the scripts in one of them, not split between the two. The full layout is in the README under
"Where everything goes".

**Where do the skills themselves go?**
- Claude apps: upload each zip from the latest release in **Customize → Skills**.
- Claude Code: `~/.claude/skills/<skill>/` for all projects (`%USERPROFILE%\.claude\skills\` on Windows), or
  `<project>/.claude/skills/<skill>/` for one.
