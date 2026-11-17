# Reviewing Agent Work

Agents are confidently wrong sometimes. The review exists so nothing unproven gets merged.

## What Claude does
0. **Read the report** from the agent's branch: `docs/reports/<MILESTONE>-<slug>.md`. If the agent stopped, the
   report says which stop condition and what it needs.
1. **Check tool versions** in the report against the table in `HANDOFF.md`. A mismatch is a bug until explained.
2. **Re-run the tests and proofs** the agent says passed.
3. **Spot-check the claims** (addresses, offsets, file paths) against the real files and logs.
4. **Check the output by hand**: decode a byte, read a log line, open the file.
5. **List the results** in this order:
   - **Bugs**: wrong or broken.
   - **Gaps**: missing, untested or unproven.
   - **Nitpicks**: style, naming, small cleanups.

## The budget rule
If checking a claim needs new tracing beyond what the agent cited (roughly more than ~10 tool calls), Claude
stops and puts it in the next prompt. Reviewing is spot-checking, not redoing the work.

## After the review
- **It works** → Claude gives you exact test steps. You test on your machine. Claude merges, tags, and records it
  in the docs.
- **It doesn't** → Claude turns the bugs and gaps into the next prompt.

## The abandon rule
When a branch has **failed two review rounds**, or the fix is heading the wrong way (growing workarounds, touching
areas the milestone shouldn't), Claude stops patching:
1. keeps the branch (renamed `abandoned/<name>` if you agree), so nothing is lost;
2. records why in the research docs and as a Lesson in `HANDOFF.md`, and keeps any confirmed findings;
3. writes a fresh prompt from the **last good tag**, with what was learned as known facts.

Patching a bad branch again and again costs more than restarting with better facts.

## When the agent stopped
Claude doesn't redo the agent's work. It reads why it stopped (missing access, a contradicted fact, a task that
grew) and fixes that in the next prompt: grant the access, correct the fact, or split the task.

## Confirmed / unverified / wrong
Every finding in the docs gets one of these:
- **confirmed**: proven by a real test, run, capture or emulation;
- **unverified**: read from code or docs, not yet tested;
- **wrong**: an old claim that turned out false. Fix it where it was written; don't just add a note.
