#!/usr/bin/env python3
"""Checks the repo before anything is merged or released.

1. Every skills/<name>/SKILL.md has valid frontmatter that claude.ai and Claude Code will accept:
   - a `name` that matches its folder, is lowercase-hyphenated, at most 64 chars,
     and doesn't contain "claude" or "anthropic" (claude.ai rejects those);
   - a `description` that is present, at most 1024 chars, with no angle brackets.
2. Every relative Markdown link in the repo points at a file that exists.
3. Every wiki [[Page Name]] link in docs/wiki points at a page that exists.

Run it locally with:  python scripts/validate.py
Exit code 0 = all good, 1 = something to fix (each problem is printed with how to fix it).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def fail(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def parse_frontmatter(text):
    """Returns the frontmatter as a dict of simple `key: value` lines, or None if there isn't any."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


# 1. Skills
skill_dirs = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
if not skill_dirs:
    errors.append("skills/: no skill folders found")
for d in skill_dirs:
    f = d / "SKILL.md"
    if not f.exists():
        fail(d, "missing SKILL.md (every skill folder needs one)")
        continue
    fm = parse_frontmatter(f.read_text(encoding="utf-8"))
    if fm is None:
        fail(f, "no frontmatter. The file must start with '---', then name/description lines, then '---'")
        continue
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != d.name:
        fail(f, f"name '{name}' doesn't match the folder name '{d.name}'. Make them the same")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "-"):
        fail(f, f"name '{name}' must be lowercase letters, digits and single hyphens")
    if len(name) > 64:
        fail(f, f"name is {len(name)} chars; the limit is 64")
    if re.search(r"claude|anthropic", name, re.I):
        fail(f, f"name '{name}' contains 'claude' or 'anthropic', which claude.ai won't save. Rename it")
    if not desc:
        fail(f, "missing description. It's what decides when the skill is used")
    elif len(desc) > 1024:
        fail(f, f"description is {len(desc)} chars; the limit is 1024")
    elif re.search(r"[<>]", desc):
        fail(f, "description contains < or >, which skill uploads reject")

# 2. Relative Markdown links
link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
for md in ROOT.rglob("*.md"):
    if ".git" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore code blocks
    for target in link_re.findall(text):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path = target.split("#")[0]
        if path and not (md.parent / path).resolve().exists():
            fail(md, f"broken link '{target}' (no such file)")

# 3. Wiki links
wiki = ROOT / "docs" / "wiki"
if wiki.exists():
    pages = {p.stem for p in wiki.glob("*.md")}
    for md in wiki.glob("*.md"):
        for page in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", md.read_text(encoding="utf-8")):
            if page.strip().replace(" ", "-") not in pages:
                fail(md, f"wiki link [[{page}]] has no page (expected docs/wiki/{page.strip().replace(' ', '-')}.md)")

if errors:
    print("Found problems:\n  " + "\n  ".join(errors))
    sys.exit(1)
print(f"OK: {len(skill_dirs)} skills valid, all links resolve.")
