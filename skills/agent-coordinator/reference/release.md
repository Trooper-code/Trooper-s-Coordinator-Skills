# Release mode

For "Use agent-coordinator. Release v1.4.0." (or "cut a release", "tag this"). Run it only after the milestones in
the release are merged and the user has tested them.

1. **Collect what changed since the last release.** Read `docs/MILESTONES.md` (progress log entries since the last
   tag), the merged reports in `docs/reports/`, and `git log --oneline <last-tag>..HEAD`. Don't open code.
2. **Pick the version** if the user didn't: a new feature → minor (1.3.0 → 1.4.0); fixes only → patch (1.3.0 →
   1.3.1); a change that breaks how users use it (file format, settings, removed features) → major. Say which and
   why in one line.
3. **Write the `CHANGELOG.md` entry** under `## v<version>`, newest at the top (create the file if missing).
   Moving an `## Unreleased` section's items into it counts. Write for the project's users, not for developers:
   - **New**: features, in plain English, with how to use each;
   - **Changed** / **Fixed**: what users will notice;
   - **Upgrading**: anything users must do (re-download, settings moved, saves to back up). Leave it out if nothing.
   Link to docs where they help. No commit hashes or internal milestone names unless the project's users use them.
4. **Check it renders as notes:** `python scripts/release-notes.py v<version>` prints the section. Fix the
   heading if it says there's no section.
5. **Commit** the changelog on `main` ("Release v<version>").
6. **Tag and push:** `git tag -a v<version> -m "v<version>: <one-line summary>"` and `git push origin v<version>`.
   If you can't push tags from here, give the user exactly those two commands in a code block.
7. **The release builds itself** if the project has `.github/workflows/release.yml` (template:
   `templates/github/workflows/release.yml`): it uses the changelog section as the release notes and attaches
   whatever the build step puts in `dist/`. If the project has no release workflow, give the user the notes
   (the output of step 4) in a code block to paste into GitHub's release form.
8. **Tell the user:** the version, what to check on the Releases page (title, notes, attached files), and the
   test steps for the release build if there's a binary.
