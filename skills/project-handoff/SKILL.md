---
name: project-handoff
description: Use when the user asks to update or prepare the handoff, wrap up a session, or switch chats, or when the context is getting large. Writes findings to the repo docs, updates docs/HANDOFF.md, and commits.
---

# Project handoff (end of session / chat switch)

Goal: nothing learned in this session is lost, and the paste into the next chat stays small. The next chat starts
from `docs/HANDOFF.md` (plus the coding agent's latest summary, if you use one) and must know exactly what to do first.

Principle: **the repo docs are the record; HANDOFF.md is a short index into them.** Every new chat pays for every
line of HANDOFF.md, so it holds the current state and the next step, not history. Budget: about 100 lines / 10 KB.

## Files this skill expects (create them if missing)
- `docs/HANDOFF.md` — the handoff itself.
- `docs/MILESTONES.md` — the status board: milestones, a dated progress log, and the "Next" step.
- Research docs — `RESEARCH.md` or `docs/research/*.md` — where findings live (formats, offsets, protocols, how things work).
- `docs/prompts/` — prompts for the coding agent (see the agent-coordinator skill).

Starter templates: `templates/` in https://github.com/Trooper-code/Trooper-s-Coordinator-Skills

## Steps

1. **Check what's already written.** Findings should already be in the docs (rule: document in the same session).
   Run `git status` and `git log --oneline -5` in each repo first; often only HANDOFF.md is left. Don't re-document
   what's committed.

   **Collect anything not yet recorded.** For each finding, note:
   - its status: **confirmed** (tested for real, or proven by a run/capture), **unverified** (read from code or docs
     only), or **wrong** (an old claim that turned out false);
   - the evidence: file and log names, addresses, offsets, commands.
   Include negative results ("tried X, it didn't happen"), the user's own test observations, and tooling bugs found
   in review.

2. **Write missing findings to the research docs first.** Put each finding in the section it belongs to and fix old
   claims that were wrong. Don't just append a session diary.

3. **Update the status board** (`docs/MILESTONES.md`):
   - add a dated progress-log entry for each finished step or finding;
   - replace the old "Next" line with the real next step: who does it (user / coding agent / Claude), the prompt
     path, and the branch name.

4. **If the next step is research or a big fix, write the coding-agent prompt** to
   `docs/prompts/<MILESTONE>-<slug>.md` (format in the agent-coordinator skill), and give the user the one-line
   instruction to paste into the agent.

5. **Update `docs/HANDOFF.md`** with this structure:
   - **Setup**: tools, versions, and a table of folders/paths (only change what changed).
   - **How it works now**: a short summary of the current working state (what's confirmed, which tag holds it),
     with pointers to the research docs. Rewrite it; don't append. **No history** — dated progress belongs in
     MILESTONES only.
   - **Where it stops**: the latest real test result and the exact log/capture that shows it.
   - **In progress**: who is doing what, with prompt path and branch.
   - **Rules**: one line each (project rules, constraints, paused work).
   - **First thing to do**: concrete steps for the next session, e.g.:
     - read MILESTONES §N and the named doc sections;
     - run all the tests;
     - spot-check the coding agent's claims against the real files and logs;
     - check any new output by hand;
     - list bugs, then gaps, then nitpicks;
     - give the user test steps;
     - merge and tag if it works, or write the follow-up prompt if it doesn't.
   - **Lessons**: one line per trap, grouped by theme. Merge a new lesson into an existing line when it's the same
     idea; keep about 10–12 lines. Once a lesson is enforced by the prompt template's constraints or acceptance
     checks, drop it here.
   - Leave out the user's personal preferences (their profile/settings already supply them).
   - End with the placeholder line `[Paste the coding agent's latest summary here]`. If an old pasted summary is
     there, **replace** it with the placeholder — once reviewed, it's stale, and what was true is in the docs now.

   **Before cutting any fact from HANDOFF.md, grep the research docs for it.** If it isn't there, move it there
   first. Compare sizes (`wc -l -c`) before and after and stay near the budget.

6. **Preserve line endings.** Check each file (`file x`, or count CRs) before editing, and edit with a
   read-modify-write that keeps them (CRLF stays CRLF, LF stays LF). Never re-type a file from tool output. Do each
   file's edits in one script (anchor on section headings, assert each anchor exists), not many small edits.

7. **Commit** each repo separately with a clear message and the project's git identity. If git fails on `.lock`
   files, ask for delete permission on the repo folder. Docs-only changes don't need the full test suite.

8. **Tell the user, briefly** (a few lines, not a recap of the session):
   - what was recorded and where (commit hashes);
   - the switch routine: run anything you asked for (logs, captures) → give the coding agent its prompt → new chat →
     paste HANDOFF.md → replace the placeholder with the agent's summary;
   - anything they must run first.

9. **If the user then pastes the coding agent's summary into this chat**, save them a step:
   - replace the placeholder in `docs/HANDOFF.md` with the summary, headed
     `**<Agent>'s <step> summary (unreviewed):**`, keeping line endings (read-modify-write script);
   - commit it;
   - reply with a short confirmation and **one ready-to-copy prompt in a code block** for the new session, e.g.
     "Continue my <project>. Read `<repo>/docs/HANDOFF.md` and do its 'First thing to do'. The agent's summary is
     already at the bottom of it."

## Do this unprompted
When the context gets large, or at the end of a review round, suggest a fresh session and offer to run these steps.

## Starting a new session from a handoff
Read HANDOFF.md, the status board and the research docs it points to **before doing anything else**, then do its
"First thing to do".
