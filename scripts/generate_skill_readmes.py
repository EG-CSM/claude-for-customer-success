#!/usr/bin/env python3
"""
generate_skill_readmes.py

Reads claude-for-cs-agent-capability-model.yaml and produces one README.md
per skill under docs/skill-readmes/<domain>/<skill-name>/README.md.

Fields included:  summary, intended_tasks, out_of_scope, invocation_cues,
                  produces_artifacts, required_context, approval_needed,
                  constraints (user-facing only), related_skills

Fields excluded:  anti_cues, execution_profile, tools_used, known_failure_modes,
                  success_criteria, consumes_files, argument_hint, priority,
                  risk_level, version, owner

Usage:
    python3 scripts/generate_skill_readmes.py
    python3 scripts/generate_skill_readmes.py --dry-run   # print to stdout only
    python3 scripts/generate_skill_readmes.py --domain csm  # one domain only
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "docs" / "claude-for-cs-agent-capability-model.yaml"
OUTPUT_ROOT = REPO_ROOT / "docs" / "skill-readmes"

# ── Governance constraints to surface in README ────────────────────────────────
# Exclude internal config_skill label; include human-facing restrictions.

EXCLUDE_CONSTRAINTS = {"config_skill"}


def user_facing_constraints(constraints: list[str] | None) -> list[str]:
    """Filter out internal constraint labels not relevant to end users."""
    if not constraints:
        return []
    return [c for c in constraints if c not in EXCLUDE_CONSTRAINTS]


# ── Formatting helpers ─────────────────────────────────────────────────────────

def bullet_list(items: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    return "\n".join(f"{prefix}- {item}" for item in items)


def invocation_examples(cues: list[str]) -> str:
    """Turn raw invocation cue strings into natural example prompts."""
    examples = []
    for cue in cues:
        # Strip surrounding quotes if present
        cue = cue.strip().strip('"').strip("'")
        if cue:
            examples.append(f'- "{cue}"')
    return "\n".join(examples)


def skill_id_to_slug(skill_id: str) -> str:
    """cs-ops.capacity-planner → capacity-planner"""
    return skill_id.split(".", 1)[-1] if "." in skill_id else skill_id


def skill_id_to_domain(skill_id: str) -> str:
    """cs-ops.capacity-planner → cs-ops"""
    return skill_id.split(".", 1)[0] if "." in skill_id else skill_id


def coerce_list(value: Any) -> list[str]:
    """Ensure a YAML field is always a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


# ── README template ────────────────────────────────────────────────────────────

def render_readme(skill: dict) -> str:
    skill_id: str = skill.get("id", "unknown")
    name: str = skill.get("name", skill_id_to_slug(skill_id))
    domain: str = skill_id_to_domain(skill_id)
    summary: str = skill.get("summary", "").strip()

    intended_tasks = coerce_list(skill.get("intended_tasks"))
    out_of_scope = coerce_list(skill.get("out_of_scope"))
    invocation_cues = coerce_list(skill.get("invocation_cues"))
    produces_artifacts = coerce_list(skill.get("produces_artifacts"))
    required_context = coerce_list(skill.get("required_context"))
    related_skills = coerce_list(skill.get("related_skills"))
    approval_needed: bool = skill.get("approval_needed", False)
    raw_constraints = coerce_list(skill.get("constraints"))
    constraints = user_facing_constraints(raw_constraints)

    # ── Build sections ──────────────────────────────────────────────────────────

    lines: list[str] = []

    # Title
    lines.append(f"# {skill_id}")
    lines.append("")

    # Summary
    lines.append(summary)
    lines.append("")

    # What it does (tasks)
    if intended_tasks:
        lines.append("## Use it for")
        lines.append("")
        lines.append(bullet_list(intended_tasks))
        lines.append("")

    # Out of scope
    if out_of_scope:
        lines.append("## Don't use it for")
        lines.append("")
        lines.append(bullet_list(out_of_scope))
        lines.append("")

    # How to trigger
    if invocation_cues:
        lines.append("## How to trigger it")
        lines.append("")
        lines.append("Say something like:")
        lines.append("")
        lines.append(invocation_examples(invocation_cues))
        lines.append("")

    # What you get
    if produces_artifacts:
        lines.append("## What you get")
        lines.append("")
        lines.append(bullet_list(produces_artifacts))
        lines.append("")

    # Prerequisites
    filtered_prereqs = [r for r in required_context if r.lower() not in ("none", "none — bootstraps from zero")]
    if filtered_prereqs:
        lines.append("## Prerequisites")
        lines.append("")
        lines.append(bullet_list(filtered_prereqs))
        lines.append("")

    # Governance
    governance_lines: list[str] = []
    if approval_needed:
        governance_lines.append("**Approval required** — output must be reviewed before distribution.")
    if constraints:
        for c in constraints:
            governance_lines.append(f"- {c}")

    if governance_lines:
        lines.append("## Governance")
        lines.append("")
        lines.append("\n".join(governance_lines))
        lines.append("")

    # See also
    if related_skills:
        lines.append("## See also")
        lines.append("")
        lines.append(bullet_list(related_skills))
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(f"*Domain: `{domain}` · Skill ID: `{skill_id}`*")
    lines.append("")

    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate per-skill READMEs from capability model YAML.")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout; don't write files.")
    parser.add_argument("--domain", help="Limit output to one domain (e.g. csm, rev-ops).")
    args = parser.parse_args()

    if not YAML_PATH.exists():
        print(f"ERROR: YAML not found at {YAML_PATH}", file=sys.stderr)
        sys.exit(1)

    with YAML_PATH.open() as f:
        data = yaml.safe_load(f)

    skills: list[dict] = data.get("skills", [])

    if not skills:
        print("No skills found in YAML.", file=sys.stderr)
        sys.exit(1)

    generated = 0
    skipped = 0

    for skill in skills:
        skill_id = skill.get("id", "")
        if not skill_id:
            print(f"WARNING: skill entry missing id — skipping: {skill}", file=sys.stderr)
            skipped += 1
            continue

        domain = skill_id_to_domain(skill_id)
        slug = skill_id_to_slug(skill_id)

        if args.domain and domain != args.domain:
            continue

        readme_content = render_readme(skill)

        if args.dry_run:
            print(f"\n{'='*60}")
            print(f"  {skill_id}")
            print(f"{'='*60}\n")
            print(readme_content)
        else:
            out_dir = OUTPUT_ROOT / domain / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / "README.md"
            out_path.write_text(readme_content, encoding="utf-8")
            print(f"  ✓ {out_path.relative_to(REPO_ROOT)}")

        generated += 1

    print(f"\nDone — {generated} README(s) generated, {skipped} skipped.")


if __name__ == "__main__":
    main()
