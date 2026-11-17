# Research import mode

For "Use agent-coordinator. Import research:" followed by pasted or attached results from a research tool (Gemini
Deep Research, ChatGPT deep research, Perplexity, a forum thread, a wiki dump). The goal: turn a long report into
**labeled, filed, checkable claims** without trusting any of it yet.

1. **Split it into claims.** One claim = one checkable statement: an offset, a format detail, a version, a
   behavior, a tool recommendation. Drop filler, summaries and opinions. Keep each claim's own cited source (URL,
   doc, forum post) if the report gave one.
2. **Label every claim `unverified`**, with its source: `[unverified | source: Gemini Deep Research 2026-11-17,
   citing <url>]`. A research report is a lead, never proof, however confident it sounds.
3. **Compare against what's known.** Look each claim's topic up in `docs/research/INDEX.md` and read only those
   sections. Then sort each claim:
   - **contradicts a confirmed fact** → don't file it as true. List it under "Conflicts" for the user: the claim,
     the confirmed fact, and the evidence behind the confirmed one. Confirmed beats unverified until something
     is re-tested.
   - **matches a confirmed fact** → add the new source next to the existing fact. Don't create a duplicate.
   - **new** → file it.
4. **File the new claims** in the research doc sections they belong to, as unverified, with the source. A topic
   with no section gets a new section and a line in `docs/research/INDEX.md`. Don't paste the raw report into the
   docs. If the user wants it kept, save it whole as `docs/research/sources/<date>-<tool>.md` and link to it.
5. **Spot-check cheaply, if at all.** At most 2–3 quick checks of the claims the next milestone depends on most
   (e.g. open a cited page). Anything deeper is the coding agent's job.
6. **Write a verify prompt** (`docs/prompts/<MILESTONE>-verify-<topic>.md`) for the claims that matter for the
   next milestone. Ask the agent to prove or disprove each with evidence, update its label to confirmed (stamped)
   or wrong, and report. Leave claims that don't matter yet as unverified.
7. **Commit** the research doc changes and the prompt. **Reply** with: how many claims were filed, the conflicts
   (if any), the claims queued for verification, and the one line to paste into the agent.
