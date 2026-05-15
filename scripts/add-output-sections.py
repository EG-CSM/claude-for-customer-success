#!/usr/bin/env python3
"""
add-output-sections.py — Append ## Output section to SKILL.md files missing it.

Inserts the section immediately before ## Guardrails (or ## Reviewer note if no
Guardrails present, or at end of file as fallback).
"""
from pathlib import Path
import re
import sys

BASE = Path(__file__).parent.parent

# Map: skill path (relative to BASE) → ## Output section content
OUTPUT_SECTIONS: dict[str, str] = {

    # ── cs-ops ────────────────────────────────────────────────────────────────

    "cs-ops/skills/capacity-planner/SKILL.md": """\
## Output

Mode-specific capacity assessment — format driven by `--current` (default), `--plan`,
or `--model` flag. Each mode produces a structured markdown report with: current state
summary, utilisation metrics, identified gaps or risks, and recommended actions.
See **Current capacity assessment** section for field-level detail.

""",

    "cs-ops/skills/data-quality-check/SKILL.md": """\
## Output

Data quality audit report — format driven by `--quick` (default) or `--full` flag.
Produces a structured markdown report with: coverage summary table, field-level
completeness scores, data gap inventory, and prioritised remediation actions.
See **Full data quality audit** section for field-level detail.

""",

    "cs-ops/skills/health-model-review/SKILL.md": """\
## Output

Health model audit report — format driven by `--quick` (default) or `--full` flag.
Produces a structured markdown report with: scoring signal inventory, weight
justifications, threshold analysis, benchmark comparison, and recommended changes.
See **Full health model audit** section for field-level detail.

""",

    "cs-ops/skills/metric-dashboard/SKILL.md": """\
## Output

Dashboard narrative — format driven by cadence flag (`--weekly`, `--monthly`,
`--quarterly`, `--board`, `--csm-performance`). Each mode produces a structured
markdown report with appropriate KPIs, trend commentary, and action items.
See mode-specific sections for field-level structure.

""",

    "cs-ops/skills/playbook-auditor/SKILL.md": """\
## Output

Playbook audit report — format driven by `--standard` (default) or `--full` flag.
Produces a structured markdown report with: scenario coverage matrix, play
effectiveness ratings, gap inventory, and prioritised improvement recommendations.
See **Full playbook audit** section for field-level detail.

""",

    "cs-ops/skills/process-doc/SKILL.md": """\
## Output

Process documentation artifact — format driven by the document-type flag
(`--csm-handoff`, `--playbook-governance`, `--data-quality`, `--escalation`,
`--segment-change`, `--sop`). Each mode produces a structured markdown document
ready for team review and adoption. See mode-specific sections for field-level structure.

""",

    "cs-ops/skills/segment-analyzer/SKILL.md": """\
## Output

Segment analysis report — format driven by `--quick` (default) or `--full` flag.
Produces a structured markdown report with: segment health summary, ICP alignment
scores, misfit account inventory, and recommended segment or coverage adjustments.
See **Full segment analysis** section for field-level detail.

""",

    # ── csm ───────────────────────────────────────────────────────────────────

    "csm/skills/call-prep/SKILL.md": """\
## Output

Call preparation brief — single structured markdown document. Sections vary by
detected call type (EBR, renewal, health check, expansion, escalation, kickoff).
All briefs include: account context snapshot, attendee profiles, agenda, key
questions, and suggested next step. See **Brief structure** section for field-level detail.

""",

    "csm/skills/escalation-memo/SKILL.md": """\
## Output

Escalation memo — format driven by lifecycle flag (`--open`, `--update`, `--close`).
Each mode produces a structured markdown document ready for internal distribution
or customer delivery. See mode-specific sections for field-level structure.

""",

    "csm/skills/health-score-review/SKILL.md": """\
## Output

Health review report — format driven by `--single` (default) or `--triage` flag.
Single-account mode produces a structured markdown brief with signal inventory,
score justification, and recommended actions. Portfolio triage produces a ranked
table with risk tier, primary driver, and next action per account.

""",

    "csm/skills/qbr-builder/SKILL.md": """\
## Output

QBR presentation document — structured markdown with executive summary, period
review (goals vs. actuals), value delivered, key metrics, strategic themes, and
next-period plan. Adapts depth to `--exec` or `--full` flag. See **QBR structure**
section for field-level detail.

""",

    "csm/skills/renewal-readiness/SKILL.md": """\
## Output

Renewal readiness output — format driven by flag (`--brief`, `--timeline`,
`--customer-summary`). Internal brief covers risk rating, deal health, and
recommended actions. Timeline produces a milestone table. Customer-facing summary
produces a value-forward narrative. See mode-specific sections for field-level structure.

""",

    "csm/skills/risk-flag/SKILL.md": """\
## Output

Risk flag report — format driven by `--standard` (default) or `--escalation-memo`
flag. Standard output produces a structured risk summary with signal inventory,
severity tier, and recommended response actions. Escalation memo mode produces a
full internal memo. See mode-specific sections for field-level structure.

""",

    "csm/skills/stakeholder-map/SKILL.md": """\
## Output

Stakeholder map — format driven by `--standard` (default) or `--sponsor-risk` flag.
Standard output: contact table with role, influence tier, sentiment, and engagement
recommendation. Sponsor risk mode adds executive vulnerability assessment and
mitigation actions. See mode-specific sections for field-level structure.

""",

    "csm/skills/success-plan-builder/SKILL.md": """\
## Output

Success plan document — format driven by `--draft` (default) or `--review` flag.
Draft mode produces a full structured plan with goals, milestones, metrics, and
owner assignments. Review mode produces a gap analysis against an existing plan.
See **Success plan structure** section for field-level detail.

""",

    "csm/skills/taro-play-runner/SKILL.md": """\
## Output

Play execution package — structured markdown with: selected play name and rationale,
account-contextualised action steps, ready-to-use deliverables (email draft, agenda,
talking points, or action plan depending on play type), and success criteria.
See **Play execution output** section for field-level detail.

""",

    "csm/skills/value-statement/SKILL.md": """\
## Output

Value statement output — format driven by flag (`--internal`, `--customer`,
`--exec-brief`, `--ae-handoff`). Ranges from internal analysis with ROI evidence
to customer-facing narratives to AE handoff packages. See mode-specific sections
for field-level structure.

""",

    # ── onboarding ────────────────────────────────────────────────────────────

    "onboarding/skills/blocker-review/SKILL.md": """\
## Output

Blocker review output — format driven by flag (`--diagnose`, `--escalate`, `--log`).
Diagnose mode: structured diagnostic report with blocker inventory, severity tiers,
root cause analysis, and recommended actions. Escalate mode: escalation brief.
Log mode: CRM-ready note. See mode-specific sections for field-level structure.

""",

    "onboarding/skills/handoff-doc/SKILL.md": """\
## Output

Onboarding handoff output — format driven by flag (`--draft`, `--readiness`,
`--summary`). Draft mode: full structured handoff document. Readiness mode:
graduation checklist with go/no-go recommendation. Summary mode: concise async
handoff note. See mode-specific sections for field-level structure.

""",

    "onboarding/skills/milestone-tracker/SKILL.md": """\
## Output

Milestone tracking output — format driven by flag (`--status`, `--portfolio`,
`--flag`). Status mode: per-account milestone table with RAG status and next action.
Portfolio mode: cross-account summary table. Flag mode: at-risk milestone alert.
See mode-specific sections for field-level structure.

""",

    "onboarding/skills/ttv-analysis/SKILL.md": """\
## Output

Time-to-Value analysis output — format driven by flag (`--account`, `--portfolio`,
`--patterns`). Account mode: single-account TtV calculation with contributing
factors and acceleration recommendations. Portfolio mode: ranked table. Patterns
mode: cohort analysis with systemic findings. See mode-specific sections for
field-level structure.

""",
}


def insert_output_section(path: Path, section_text: str) -> bool:
    """Insert section_text before ## Guardrails (or ## Reviewer note, or at EOF)."""
    content = path.read_text()

    # Already has it — skip
    if re.search(r"^##\s+Output", content, re.MULTILINE | re.IGNORECASE):
        print(f"  SKIP (already has ## Output): {path}")
        return False

    # Find insertion point: before ## Guardrails
    anchor = re.search(r"^(##\s+Guardrails)", content, re.MULTILINE | re.IGNORECASE)
    if not anchor:
        # Fallback: before ## Reviewer note
        anchor = re.search(r"^(##\s+Reviewer)", content, re.MULTILINE | re.IGNORECASE)

    if anchor:
        insert_pos = anchor.start()
        new_content = content[:insert_pos] + section_text + content[insert_pos:]
    else:
        # Last resort: append at end
        new_content = content.rstrip() + "\n\n" + section_text

    path.write_text(new_content)
    print(f"  ADDED: {path.relative_to(BASE)}")
    return True


def main() -> None:
    modified = 0
    for rel_path, section in OUTPUT_SECTIONS.items():
        full_path = BASE / rel_path
        if not full_path.exists():
            print(f"  MISSING: {rel_path}")
            continue
        if insert_output_section(full_path, section):
            modified += 1

    print(f"\nDone. Modified {modified} file(s).")


if __name__ == "__main__":
    main()
