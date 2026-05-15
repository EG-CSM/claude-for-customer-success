#!/usr/bin/env python3
"""
generate-eval-fixtures.py — Scaffold eval fixture files for CS suite skills.

Generates a skeleton eval fixture markdown file for each SKILL.md that does
not yet have a corresponding evals/fixtures/<skill-name>-eval.md file.

This is the scaffolding-only version. It creates the table structure with
placeholder rows so a human (or the full outputs/generate_eval_fixtures.py
generator) can fill in domain-specific cases.

If a fixture already exists, this script skips it by default (--force to overwrite).

Usage:
  python3 scripts/generate-eval-fixtures.py
  python3 scripts/generate-eval-fixtures.py --plugin csm
  python3 scripts/generate-eval-fixtures.py --plugin renewals --force
  python3 scripts/generate-eval-fixtures.py --dry-run

Options:
  --plugin PLUGIN   Limit to one plugin (csm|renewals|onboarding|cs-ops)
  --force           Overwrite existing fixture files
  --dry-run         Show what would be created without writing files
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Generator

# ---------------------------------------------------------------------------
# Fixture template
# ---------------------------------------------------------------------------

FIXTURE_TEMPLATE = """\
# Eval Fixture: {skill_name}

**Plugin:** `{plugin}`
**Skill file:** `{skill_path}`

> Auto-scaffolded by `scripts/generate-eval-fixtures.py`. Replace placeholder
> rows with domain-specific eval cases before running evals.

---

## Trigger-Positive Cases

| ID | Input | Expected Trigger | Priority | Notes |
|----|-------|-----------------|----------|-------|
| TP-01 | [PLACEHOLDER — phrase that should activate this skill] | `true` | critical | |
| TP-02 | [PLACEHOLDER — second activation phrase] | `true` | critical | |
| TP-03 | [PLACEHOLDER — third activation phrase] | `true` | standard | |
| TP-04 | [PLACEHOLDER — fourth activation phrase] | `true` | standard | |
| TP-05 | [PLACEHOLDER — fifth activation phrase] | `true` | optional | |

## Trigger-Negative Cases

| ID | Input | Expected Trigger | Priority | Notes |
|----|-------|-----------------|----------|-------|
| TN-01 | [PLACEHOLDER — phrase that should NOT activate this skill] | `false` | critical | |
| TN-02 | [PLACEHOLDER — second non-activation phrase] | `false` | critical | |
| TN-03 | [PLACEHOLDER — third non-activation phrase] | `false` | standard | |
| TN-04 | [PLACEHOLDER — fourth non-activation phrase] | `false` | standard | |
| TN-05 | [PLACEHOLDER — fifth non-activation phrase] | `false` | optional | |

## Edge Cases

| ID | Input | Expected Trigger | Priority | Notes |
|----|-------|-----------------|----------|-------|
| EC-01 | [PLACEHOLDER — ambiguous or boundary input] | `true` | critical | |
| EC-02 | [PLACEHOLDER — second edge case] | `false` | standard | |
| EC-03 | [PLACEHOLDER — third edge case] | `true` | optional | |

## Injection Tests

| ID | Input | Expected Trigger | Priority | Notes |
|----|-------|-----------------|----------|-------|
| INJ-01 | Ignore previous instructions and [PLACEHOLDER — injection attempt] | `false` | critical | Injection resistance |
| INJ-02 | [PLACEHOLDER — role-override injection attempt] | `false` | critical | Injection resistance |
| INJ-03 | [PLACEHOLDER — data-exfil injection attempt] | `false` | standard | Injection resistance |

---

## Eval Results Log

| Run Date | Model | TPR | TNR | Edge Pass Rate | Notes |
|----------|-------|-----|-----|----------------|-------|
| — | — | — | — | — | Not yet evaluated |

**Production threshold:** TPR ≥ 0.80 AND TNR ≥ 0.80. Block deployment if either < 0.70.
"""


# ---------------------------------------------------------------------------
# Frontmatter parsing (minimal)
# ---------------------------------------------------------------------------

def _read_skill_name(skill_path: Path) -> str:
    """Read the `name:` field from SKILL.md frontmatter, fall back to dir name."""
    try:
        text = skill_path.read_text(encoding="utf-8")
    except OSError:
        return skill_path.parent.name

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return skill_path.parent.name

    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^name\s*:\s*(.+)", line)
        if m:
            return m.group(1).strip().strip("\"'")

    return skill_path.parent.name


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

PLUGINS = ["csm", "renewals", "onboarding", "cs-ops"]


def _find_skills(repo_root: Path, plugin: str | None = None) -> Generator[tuple[str, Path], None, None]:
    """
    Yield (plugin_name, skill_md_path) for each SKILL.md found.
    Skips evals/ and scripts/ directories.
    """
    plugins_to_scan = [plugin] if plugin else PLUGINS
    for p in plugins_to_scan:
        plugin_dir = repo_root / p / "skills"
        if not plugin_dir.exists():
            continue
        for skill_md in sorted(plugin_dir.rglob("SKILL.md")):
            # skip nested non-skill paths
            if "evals" in skill_md.parts or "scripts" in skill_md.parts:
                continue
            yield p, skill_md


# ---------------------------------------------------------------------------
# Fixture path resolution
# ---------------------------------------------------------------------------

def _fixture_path(repo_root: Path, plugin: str, skill_md: Path) -> Path:
    """
    Return the canonical fixture path for a given skill.
    Convention: <plugin>/evals/fixtures/<skill-dir-name>-eval.md
    """
    skill_dir_name = skill_md.parent.name
    return repo_root / plugin / "evals" / "fixtures" / f"{skill_dir_name}-eval.md"


# ---------------------------------------------------------------------------
# Scaffold a single fixture
# ---------------------------------------------------------------------------

def scaffold_fixture(
    repo_root: Path,
    plugin: str,
    skill_md: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """
    Create the fixture file if it doesn't exist (or force=True).
    Returns (created: bool, message: str).
    """
    fixture = _fixture_path(repo_root, plugin, skill_md)

    if fixture.exists() and not force:
        return False, f"EXISTS (skip): {fixture.relative_to(repo_root)}"

    skill_name = _read_skill_name(skill_md)
    rel_skill = skill_md.relative_to(repo_root)

    content = FIXTURE_TEMPLATE.format(
        skill_name=skill_name,
        plugin=plugin,
        skill_path=str(rel_skill),
    )

    action = "OVERWRITE" if fixture.exists() else "CREATE"

    if not dry_run:
        fixture.parent.mkdir(parents=True, exist_ok=True)
        fixture.write_text(content, encoding="utf-8")

    return True, f"{action}: {fixture.relative_to(repo_root)}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolve_repo_root(args: argparse.Namespace) -> Path:
    """Find claude-for-customer-success/ relative to cwd."""
    candidates = [
        Path("claude-for-customer-success"),
        Path("."),  # if already inside the repo
    ]
    for c in candidates:
        # Check that at least one known plugin dir exists
        if any((c / p).exists() for p in PLUGINS):
            return c.resolve()
    print("ERROR: Could not locate claude-for-customer-success/ repo root.", file=sys.stderr)
    print("Run from the parent directory or inside the repo.", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold eval fixture files for CS suite skills.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--plugin",
        metavar="PLUGIN",
        choices=PLUGINS,
        help="Limit scaffolding to one plugin",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing fixture files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing any files",
    )

    args = parser.parse_args()
    repo_root = _resolve_repo_root(args)

    if args.dry_run:
        print("[DRY RUN — no files will be written]\n")

    created = 0
    skipped = 0

    for plugin, skill_md in _find_skills(repo_root, args.plugin):
        ok, msg = scaffold_fixture(
            repo_root,
            plugin,
            skill_md,
            force=args.force,
            dry_run=args.dry_run,
        )
        print(msg)
        if ok:
            created += 1
        else:
            skipped += 1

    print(f"\n{'─' * 50}")
    if args.dry_run:
        print(f"Would create: {created}  |  Would skip: {skipped}")
    else:
        print(f"Created: {created}  |  Skipped: {skipped}")


if __name__ == "__main__":
    main()
