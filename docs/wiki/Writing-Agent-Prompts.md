# Writing Agent Prompts

The agent has **none of your Claude chat's context**. A good prompt is one it can run start to finish without
asking you anything. Template: [`templates/PROMPT.md`](https://github.com/Trooper-code/Trooper-s-Coordinator-Skills/blob/main/templates/PROMPT.md).

## The sections
| Section | Why it's there |
|---------|----------------|
| **Read first** | `AGENTS.md` first (the standing rules), then the docs this task needs, so the agent doesn't re-research what's known. |
| **Goal** | One or two sentences. What should be true when it's done. |
| **Branch** | The name, and which tag to branch from. Keeps work isolated. |
| **Known facts** | Exact paths, addresses, offsets, values, each marked **confirmed** or **unverified**. Stops the agent from treating guesses as truth. |
| **Tasks** | Numbered steps. |
| **Tools** | Name the agent's skills/tools that fit, and say why (e.g. `systematic-debugging` for "find the root cause before fixing"). |
| **Task-specific constraints** | Only what `AGENTS.md` doesn't already say, e.g. "keep it .NET 8". The standing rules (don't merge, no copyrighted files, line endings) live in `AGENTS.md`. See [[Agent Rules and Reports]]. |
| **Stop and report if** | The `AGENTS.md` stop conditions plus any for this task, e.g. "the checksum isn't CRC32". |
| **Acceptance checks** | Which tests must pass. Every claim must cite evidence. |
| **Report** | Write `docs/reports/<MILESTONE>-<slug>.md` from the template and commit it on the branch, so Claude reads it from the repo. |

## Tips
- **Mark everything confirmed or unverified.** The fastest way to waste an agent run is to hand it a wrong
  "fact" with no flag on it.
- **Exact beats vague.** `0x8012A4C0 in main.bin` is better than "the function that loads saves".
- **Ask for evidence.** "Every claim must cite a file and address" makes the agent show its work, and makes
  your review a spot-check instead of a re-investigation.
- **Keep it read-only on your real files.** Especially with tools that can attach debuggers or control processes.
- **One prompt, one branch, one goal.** If it has two goals, it's two prompts.
- **Give it a way out.** A specific stop condition ("if the header isn't 0x40 bytes, stop") is cheaper than an
  agent guessing for an hour.
