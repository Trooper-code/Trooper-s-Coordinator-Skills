# Reviewing Agent Work

Agents are confidently wrong sometimes. The review exists so nothing unproven gets merged.

## What Claude does
1. **Re-run the tests and proofs** the agent says passed.
2. **Spot-check the claims** (addresses, offsets, file paths) against the real files and logs.
3. **Check the output by hand**: decode a byte, read a log line, open the file.
4. **List the results** in this order:
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

## Confirmed / unverified / wrong
Every finding in the docs gets one of these:
- **confirmed**: proven by a real test, run, capture or emulation;
- **unverified**: read from code or docs, not yet tested;
- **wrong**: an old claim that turned out false. Fix it where it was written; don't just add a note.
