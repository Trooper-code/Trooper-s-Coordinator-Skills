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
Setup · How it works now · Where it stops · In progress · Rules · First thing to do · Lessons · the summary
placeholder. **Around 100 lines max.** No history: dated progress goes in `MILESTONES.md`, and findings go in the
research docs.

## Rules that keep it small
- Before cutting a fact from `HANDOFF.md`, make sure it's in the research docs.
- Rewrite "How it works now"; don't append to it.
- Merge a new lesson into an existing one if it's the same idea. Keep about 10–12.
- After review, the agent's pasted summary is stale. Replace it with the placeholder.

Why the rules look like this, in ML terms: [[Memory Model]].
