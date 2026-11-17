# The check scripts

Copied into each project's `scripts/` folder from `templates/scripts/`. All of them use only the Python standard
library, explain each problem in plain English with how to fix it, and exit 1 when something needs fixing.

| Script | Run it | What it catches |
|--------|--------|-----------------|
| `detect-mode.py <repo>` | before kickoff/adopt, if you can run commands | which mode the repo needs, which workflow files exist or are missing, existing agent rules files and planning notes |
| `check-prompt.py <prompt>` | after writing every agent prompt, before handing it over | missing sections, `AGENTS.md` not first in Read first, unlabeled known facts, no report path, leftover placeholders |
| `check-report.py <report>` | first thing on review | no status, a stopped report without a reason, findings without a label or evidence, tests without output, leftover placeholders |
| `check-research.py` | on review, and whenever the Tool versions table changes | confirmed facts proven on older tool versions (version drift), broken or missing research index entries |
| `check-handoff.py` | before every handoff commit | over budget, missing sections, no summary line, dead paths; notes lessons marked `(x2)` to promote into rules |
| `check-safe-to-publish.py` | pre-commit hook (`--staged`) and CI | ROMs, disc images, console executables, saves, emulator states, binaries over 5 MB; exceptions go in `.publish-allowlist` |
| `release-notes.py <tag>` | in release mode, and by the release workflow | the tag's section of `CHANGELOG.md`, printed as release notes |

**If you can't run commands** (no shell, no repo access), do the same checks by reading the files, and say that
you checked by hand.

**If a script is missing** from a project, copy it from this skill's `templates/scripts/` folder (in the release
zip) or from `templates/scripts/` in https://github.com/Trooper-code/Trooper-s-Coordinator-Skills.
