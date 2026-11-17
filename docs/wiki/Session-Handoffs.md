# Session Handoffs

Long chats get expensive and forgetful. The fix: **the repo docs are the record, and `docs/HANDOFF.md` is a short
index into them.** Template: [`templates/HANDOFF.md`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/HANDOFF.md).

## When to hand off
- At the end of every session.
- At the end of a review round.
- Whenever the chat feels long. Claude should suggest it on its own.

## The switch routine
1. Say **"update the handoff"**. Claude writes any unrecorded findings to the docs, updates `MILESTONES.md` and
   `HANDOFF.md`, and commits.
2. Run anything Claude asked for (logs, captures, tests).
3. Give the coding agent its prompt.
4. Open a new Claude chat, paste `HANDOFF.md`, and replace the last line,
   `[Paste the coding agent's latest summary here]`, with the agent's summary.

**Shortcut:** if you paste the agent's summary into the *old* chat instead, Claude puts it into `HANDOFF.md` for
you, commits it, and hands you a one-line prompt for the new chat.

## What goes in HANDOFF.md
Setup · Tool versions · How it works now · Where it stops · In progress · Rules · First thing to do · Lessons · the summary
placeholder. **Around 100 lines max.** No history: dated progress goes in `MILESTONES.md`, and findings go in the
research docs.

## Rules that keep it small
- Before cutting a fact from `HANDOFF.md`, make sure it's in the research docs.
- Rewrite "How it works now"; don't append to it.
- Merge a new lesson into an existing one if it's the same idea. Keep about 10–12.
- After review, the agent's pasted summary is stale. Replace it with the placeholder.

Why the rules look like this, in ML terms: [[Memory Model]].

## Check it before committing
`project-handoff` runs `python scripts/check-handoff.py` before every handoff commit. It fails if `HANDOFF.md`:
- is over budget (120 lines / 10 KB);
- is missing a required section;
- doesn't end with the agent-summary line;
- points to a repo path that doesn't exist (except agent reports, which live on the agent's branch until merged).

Each problem says how to fix it. Copy the script from
[`templates/scripts/check-handoff.py`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/scripts/check-handoff.py),
and edit the settings at the top if your project needs different limits or sections.

## Agent reports change the routine
Since v1.3.0 the agent commits its report to `docs/reports/` on its branch, so step 4 of the switch routine no longer
needs the summary pasted: the new chat reads the report from the branch. If the new chat can read your repo, you
don't even paste `HANDOFF.md`, just say `Read docs/HANDOFF.md and do its "First thing to do"`. Pasting the summary
still works if your agent can't commit.

## Lessons that keep coming back
A lesson hit a second time gets `(x2)` at the end of its line. The checker prints a note, and Claude promotes the
lesson into `AGENTS.md`, a check script or the prompt template, then removes it from the handoff. See
[[Long-Haul Tools]].
