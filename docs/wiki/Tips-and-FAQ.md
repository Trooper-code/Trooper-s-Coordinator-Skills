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
A skill's name can't contain "claude" or "anthropic". Rename it in the `name:` line and the folder.

**Line endings got mangled.**
Both skills tell Claude to keep each file's existing line endings (CRLF stays CRLF). If it happens anyway, point
Claude at the file and ask it to check with `file <name>`.

**Git fails with `.lock` errors.**
Claude needs permission to delete files in the repo folder (git creates and removes lock files). Grant delete
permission when asked.

**Don't commit copyrighted stuff.**
Game files, ROMs, saves, assets and binaries stay out of the repo. Have users supply their own files. The prompt
template's constraints say this so the agent doesn't forget.
