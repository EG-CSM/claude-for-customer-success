#!/usr/bin/env python3
"""
fix-reasoning-protocol-step1.py — Correct the Reasoning Protocol Step 1
"Use when" reference across all CS suite SKILL.md files.

PROBLEM:
  The generated Reasoning Protocol Step 1 reads:
    "does the request match the `Use when` triggers?"

  CS suite skills use Claude Code slash command format: trigger precision
  lives in the frontmatter `description:` field — there is no "Use when /
  Do NOT use for" body block. The reference is broken.

FIX:
  Replace the broken reference with format-accurate language:
    "does the request match this skill's intended use?"

SCOPE:
  All SKILL.md files across the 4 plugins (csm, renewals, onboarding, cs-ops).
  Applies to config skills (cold-start-interview, customize) and standard skills
  alike — both carry the same broken Step 1 text.

IDEMPOTENT:
  The substitution is a no-op if the old text is not present (already applied
  or never existed).

Usage:
  python3 scripts/fix-reasoning-protocol-step1.py
  python3 scripts/fix-reasoning-protocol-step1.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PLUGINS: list[str] = ["csm", "renewals", "onboarding", "cs-ops"]

OLD_TEXT = (
    "1. **Confirm skill activation** — does the request match the "
    "`Use when` triggers? If not, name the better skill."
)

NEW_TEXT = (
    "1. **Confirm skill activation** — does the request match this skill's "
    "intended use? If not, name the better skill."
)

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def find_skill_files(repo_root: Path) -> list[Path]:
    """Return all SKILL.md files across the 4 plugins."""
    results: list[Path] = []
    for plugin in PLUGINS:
        plugin_dir = repo_root / plugin / "skills"
        if not plugin_dir.exists():
            continue
        results.extend(sorted(plugin_dir.rglob("SKILL.md")))
    return results


def patch_file(path: Path, *, dry_run: bool) -> str:
    """
    Apply the Step 1 substitution to a single file.
    Returns a status string: UPDATED | SKIPPED | MISSING
    """
    if not path.exists():
        return "MISSING"

    text = path.read_text(encoding="utf-8")

    if OLD_TEXT not in text:
        return "SKIPPED"  # already applied or not present

    patched = text.replace(OLD_TEXT, NEW_TEXT, 1)

    if not dry_run:
        path.write_text(patched, encoding="utf-8")

    return "UPDATED"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix Reasoning Protocol Step 1 'Use when' reference in CS suite SKILL.md files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing any files.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.resolve()

    skill_files = find_skill_files(repo_root)
    if not skill_files:
        print("ERROR: No SKILL.md files found. Run from inside the repo.", file=sys.stderr)
        return 2

    if args.dry_run:
        print("[DRY RUN — no files will be written]\n")

    updated = skipped = missing = 0

    for path in skill_files:
        rel = path.relative_to(repo_root)
        status = patch_file(path, dry_run=args.dry_run)

        if status == "UPDATED":
            updated += 1
            action = "WOULD UPDATE" if args.dry_run else "UPDATED"
            print(f"{action:12s}  {rel}")
        elif status == "SKIPPED":
            skipped += 1
            # Verbose only — skip clutters output for 41 files
        elif status == "MISSING":
            missing += 1
            print(f"MISSING       {rel}")

    print(f"\n{'─' * 60}")
    if args.dry_run:
        print(f"Would update : {updated}  |  Would skip : {skipped}  |  Missing : {missing}")
    else:
        print(f"Updated      : {updated}  |  Skipped    : {skipped}  |  Missing  : {missing}")

    if missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
