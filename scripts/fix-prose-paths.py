#!/usr/bin/env python3
"""
fix-prose-paths.py — Convert root-relative backtick path references to
explicit document-relative paths, resolving the 25 WARN findings from
validate-cross-links.py.

Idempotent: each substitution is a no-op if already applied.
"""

import sys
from pathlib import Path

BASE = Path(__file__).parent.parent  # repo root

# (file_path_relative_to_root, old_backtick_string, new_backtick_string)
SUBSTITUTIONS = [
    # ── Config schema files (4 × 2 = 8 WARNs) ───────────────────────────
    ("csm/reference/config-schema.md",
     "`scripts/check-config-completeness.py`",
     "`../../scripts/check-config-completeness.py`"),
    ("csm/reference/config-schema.md",
     "`shared/cs-domain-model.md`",
     "`../../shared/cs-domain-model.md`"),

    ("renewals/reference/config-schema.md",
     "`scripts/check-config-completeness.py`",
     "`../../scripts/check-config-completeness.py`"),
    ("renewals/reference/config-schema.md",
     "`shared/cs-domain-model.md`",
     "`../../shared/cs-domain-model.md`"),

    ("onboarding/reference/config-schema.md",
     "`scripts/check-config-completeness.py`",
     "`../../scripts/check-config-completeness.py`"),
    ("onboarding/reference/config-schema.md",
     "`shared/cs-domain-model.md`",
     "`../../shared/cs-domain-model.md`"),

    ("cs-ops/reference/config-schema.md",
     "`scripts/check-config-completeness.py`",
     "`../../scripts/check-config-completeness.py`"),
    ("cs-ops/reference/config-schema.md",
     "`shared/cs-domain-model.md`",
     "`../../shared/cs-domain-model.md`"),

    # ── Agent doc files (5 WARNs) ────────────────────────────────────────
    ("cs-ops/agents/portfolio-segment-digest.md",
     "`cs-ops/CLAUDE.md`",
     "`../CLAUDE.md`"),

    ("csm/agents/churn-signal-digest.md",
     "`csm/CLAUDE.md`",
     "`../CLAUDE.md`"),

    ("csm/agents/health-watcher.md",
     "`csm/CLAUDE.md`",
     "`../CLAUDE.md`"),

    # cross-plugin: renewals/agents/ → csm/CLAUDE.md  (2 levels up, then into csm/)
    ("renewals/agents/renewal-scanner.md",
     "`csm/CLAUDE.md`",
     "`../../csm/CLAUDE.md`"),

    ("onboarding/agents/onboarding-milestone-tracker.md",
     "`onboarding/CLAUDE.md`",
     "`../CLAUDE.md`"),

    # ── Skill files (4 WARNs) ────────────────────────────────────────────
    ("cs-ops/skills/customize/SKILL.md",
     "`cs-ops/CLAUDE.md`",
     "`../../CLAUDE.md`"),

    ("cs-ops/skills/process-doc/SKILL.md",
     "`cs-ops/CLAUDE.md`",
     "`../../CLAUDE.md`"),

    ("onboarding/skills/success-criteria/SKILL.md",
     "`onboarding/CLAUDE.md`",
     "`../../CLAUDE.md`"),

    ("renewals/skills/cold-start-interview/SKILL.md",
     "`renewals/CLAUDE.md`",
     "`../../CLAUDE.md`"),

    # ── Managed cookbook files (8 WARNs) ─────────────────────────────────
    # README.md is depth 1 → relative prefix is ../
    ("managed-agent-cookbooks/README.md",
     "`csm/CLAUDE.md`",
     "`../csm/CLAUDE.md`"),
    ("managed-agent-cookbooks/README.md",
     "`renewals/CLAUDE.md`",
     "`../renewals/CLAUDE.md`"),
    ("managed-agent-cookbooks/README.md",
     "`cs-ops/CLAUDE.md`",
     "`../cs-ops/CLAUDE.md`"),
    ("managed-agent-cookbooks/README.md",
     "`onboarding/CLAUDE.md`",
     "`../onboarding/CLAUDE.md`"),

    # subdirectory cookbooks are depth 2 → relative prefix is ../../
    ("managed-agent-cookbooks/health-watcher/cookbook.md",
     "`csm/CLAUDE.md`",
     "`../../csm/CLAUDE.md`"),

    ("managed-agent-cookbooks/portfolio-segment-digest/README.md",
     "`cs-ops/CLAUDE.md`",
     "`../../cs-ops/CLAUDE.md`"),

    ("managed-agent-cookbooks/portfolio-segment-digest/cookbook.md",
     "`cs-ops/CLAUDE.md`",
     "`../../cs-ops/CLAUDE.md`"),

    ("managed-agent-cookbooks/renewal-scanner/cookbook.md",
     "`csm/CLAUDE.md`",
     "`../../csm/CLAUDE.md`"),
]


def apply_substitutions() -> int:
    files_changed = 0
    total_replacements = 0

    # Accumulate all substitutions per file before writing
    from collections import defaultdict
    per_file: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for rel, old, new in SUBSTITUTIONS:
        per_file[rel].append((old, new))

    for rel_path, subs in per_file.items():
        fpath = BASE / rel_path
        if not fpath.exists():
            print(f"MISSING  {rel_path}")
            continue

        text = fpath.read_text(encoding="utf-8")
        original = text
        file_count = 0

        for old, new in subs:
            count = text.count(old)
            if count == 0:
                # Already applied or not present — skip silently
                continue
            text = text.replace(old, new)
            file_count += count
            print(f"  REPLACE  ({count}×) {old!r} → {new!r}")

        if text != original:
            fpath.write_text(text, encoding="utf-8")
            print(f"UPDATED  {rel_path}  ({file_count} replacement(s))")
            files_changed += 1
            total_replacements += file_count
        else:
            print(f"SKIPPED  {rel_path}  (already correct or no matches)")

    print(f"\nDone — {files_changed} file(s) updated, {total_replacements} total replacement(s).")
    return 0


if __name__ == "__main__":
    sys.exit(apply_substitutions())
