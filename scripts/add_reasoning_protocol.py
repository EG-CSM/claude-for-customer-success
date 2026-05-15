#!/usr/bin/env python3
"""
Task 6: Add ## Reasoning Protocol section to all 41 SKILL.md files.

Insertion point: after ## Pre-flight block ends, before the next ##-level section.
Idempotent: skips any file that already contains ## Reasoning Protocol.
"""

import os
import re

BASE = "/Users/toddceby/claude-cowork/projects/agent-building/claude-for-customer-success"

# ---------------------------------------------------------------------------
# Per-skill guardrail text for step 4 of the Reasoning Protocol.
# Keys: "plugin/skill-name"
# ---------------------------------------------------------------------------

NO_GUARDRAILS = (
    "No domain guardrails apply — this skill configures the environment "
    "rather than generating outputs."
)

GUARDRAIL_MAP = {
    # ── CSM plugin ──────────────────────────────────────────────────────────
    "csm/account-research": (
        "G1 (health scores are heuristics — do not frame as churn probability), "
        "G2 (expansion signals require economic buyer qualification), "
        "G4 (no escalation triage without a named escalation path), "
        "G5 (confidentiality check before distributing portfolio-level financial data), "
        "G7 (flag any stale data with source date and staleness indicator)."
    ),
    "csm/call-prep": (
        "G1 (health scores are heuristics — do not frame as churn probability), "
        "G2 (expansion signals require economic buyer qualification), "
        "G5 (confidentiality check before distributing internal account data externally)."
    ),
    "csm/cold-start-interview": NO_GUARDRAILS,
    "csm/customize": NO_GUARDRAILS,
    "csm/escalation-memo": (
        "G3 (any revenue impact language must carry commitment language + Finance validation callout), "
        "G4 (verify a named escalation path is configured before generating the memo), "
        "G5 (confidentiality check before distributing the memo beyond the CS team)."
    ),
    "csm/health-score-review": (
        "G1 (health scores are heuristics — never frame as churn predictions), "
        "G4 (no escalation triage without a named escalation path in config), "
        "G5 (confidentiality check before distributing portfolio-level health data), "
        "G7 (flag any stale health data with source date and staleness indicator)."
    ),
    "csm/qbr-builder": (
        "G2 (expansion signals require economic buyer qualification before inclusion), "
        "G3 (revenue-related content must carry commitment language + Finance validation callout)."
    ),
    "csm/renewal-readiness": (
        "G2 (expansion signals require economic buyer qualification), "
        "G3 (revenue projections carry commitment language + Finance validation callout)."
    ),
    "csm/risk-flag": (
        "G1 (health scores are heuristics — do not frame as churn predictions), "
        "G3 (any revenue impact framing carries commitment language), "
        "G4 (no escalation triage without a named escalation path)."
    ),
    "csm/stakeholder-map": (
        "G1 (health scores referenced in stakeholder context are heuristics only), "
        "G5 (confidentiality check before distributing stakeholder contact data externally)."
    ),
    "csm/success-plan-builder": (
        "G3 (revenue outcome targets carry commitment language + Finance validation callout), "
        "G5 (confidentiality check before distributing the plan beyond the CS team)."
    ),
    "csm/taro-play-runner": (
        "G2 (expansion signals require economic buyer qualification), "
        "G4 (no escalation triage without a named escalation path), "
        "G6 (TARO play outputs are leads for CSM judgment — not prescriptions)."
    ),
    "csm/value-statement": (
        "G2 (expansion value claims require economic buyer qualification), "
        "G3 (revenue value language carries commitment language + Finance validation callout), "
        "G5 (confidentiality check before distributing internal metrics externally)."
    ),

    # ── Renewals plugin ─────────────────────────────────────────────────────
    "renewals/customize": NO_GUARDRAILS,
    "renewals/cold-start-interview": NO_GUARDRAILS,
    "renewals/risk-assessment": (
        "G1 (health scores are heuristics — never frame risk level as a churn prediction)."
    ),
    "renewals/churn-analysis": (
        "G1 (health scores and churn signals are heuristics — do not present as predictive certainty)."
    ),
    "renewals/contract-review": (
        "G7 (flag any contract data that is stale relative to the configured staleness threshold)."
    ),
    "renewals/expansion-signal": (
        "G2 (expansion ARR is not counted until an economic buyer has been qualified)."
    ),
    "renewals/negotiation-prep": (
        "G4 (verify a named escalation path is configured before generating negotiation guidance)."
    ),
    "renewals/price-increase-prep": (
        "G3 (price impact projections carry commitment language + Finance validation callout)."
    ),
    "renewals/renewal-forecast": (
        "G2 (expansion ARR not included until economic buyer qualified), "
        "G3 (all forecast figures carry commitment language + Finance/RevOps validation callout), "
        "G4 (verify a named escalation path before surfacing at-risk forecast items), "
        "G7 (flag any stale pipeline or health data with source date and staleness indicator)."
    ),
    "renewals/executive-summary": (
        "G3 (revenue and forecast figures carry commitment language + Finance validation callout), "
        "G5 (confidentiality check before distributing portfolio-level financial data)."
    ),

    # ── Onboarding plugin ───────────────────────────────────────────────────
    "onboarding/customize": NO_GUARDRAILS,
    "onboarding/cold-start-interview": NO_GUARDRAILS,
    "onboarding/success-criteria": (
        "G7 (flag any account data used that is stale relative to the configured staleness threshold)."
    ),
    "onboarding/kickoff-prep": (
        "G7 (flag any account or deal data that is stale relative to the configured staleness threshold)."
    ),
    "onboarding/blocker-review": (
        "G4 (verify a named escalation path is configured before generating triage output)."
    ),
    "onboarding/handoff-doc": (
        "G7 (flag any milestone or engagement data that is stale relative to the configured staleness threshold)."
    ),
    "onboarding/onboarding-plan": (
        "G7 (flag any account or success-criteria data that is stale relative to the configured staleness threshold)."
    ),
    "onboarding/milestone-tracker": (
        "G7 (flag any milestone status data that is stale — always include source date and staleness indicator)."
    ),
    "onboarding/ttv-analysis": (
        "G7 (flag any milestone completion data that is stale — include source date and staleness indicator on all TtV figures)."
    ),

    # ── CS-Ops plugin ────────────────────────────────────────────────────────
    "cs-ops/customize": NO_GUARDRAILS,
    "cs-ops/cold-start-interview": NO_GUARDRAILS,
    "cs-ops/process-doc": (
        "G7 (flag any process data or account records that are stale relative to the configured staleness threshold)."
    ),
    "cs-ops/playbook-auditor": (
        "G6 (playbook audit outputs are leads for CS Ops judgment — not prescriptions for immediate play retirement)."
    ),
    "cs-ops/data-quality-check": (
        "G7 (the purpose of this skill is to surface stale data — every stale record flagged must include source date and staleness indicator)."
    ),
    "cs-ops/capacity-planner": (
        "G4 (verify a named capacity alert escalation path is configured before surfacing over/under-allocation flags)."
    ),
    "cs-ops/segment-analyzer": (
        "G7 (flag any account or ARR data that is stale relative to the configured staleness threshold)."
    ),
    "cs-ops/health-model-review": (
        "G1 (health scores are heuristics — calibration findings must not be framed as churn predictions)."
    ),
    "cs-ops/metric-dashboard": (
        "G3 (GRR, NRR, and ARR metrics carry commitment language + Finance/RevOps validation callout), "
        "G5 (confidentiality check before distributing portfolio-level financial data), "
        "G7 (flag any metric data that is stale — include source date and staleness indicator on all figures)."
    ),
}


def build_reasoning_protocol(guardrail_text: str) -> str:
    return f"""
## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match the `Use when` triggers? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — {guardrail_text}
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

"""


def insert_reasoning_protocol(content: str, guardrail_text: str) -> str | None:
    """
    Insert the Reasoning Protocol block after the ## Pre-flight section ends,
    immediately before the next ##-level header.

    For config skills (no ## Pre-flight), falls back to inserting before the
    first ## section in the body.

    Returns the modified content, or None if the insertion point was not found.
    """
    # Primary: find the end of the ## Pre-flight block
    pattern = re.compile(
        r'(## Pre-flight\b.*?\n)(## )',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        insert_pos = match.start(2)  # position of the next ## header
        block = build_reasoning_protocol(guardrail_text)
        return content[:insert_pos] + block + content[insert_pos:]

    # Fallback for config skills: insert before the first ## section in the body
    fallback = re.search(r'\n(## [A-Z])', content)
    if not fallback:
        return None
    insert_pos = fallback.start(1)  # position of the ## header itself
    block = build_reasoning_protocol(guardrail_text)
    return content[:insert_pos] + block + "\n" + content[insert_pos:]


def process_all_skills():
    modified = []
    skipped = []
    errors = []

    plugins = ["csm", "renewals", "onboarding", "cs-ops"]

    for plugin in plugins:
        skills_dir = os.path.join(BASE, plugin, "skills")
        if not os.path.isdir(skills_dir):
            errors.append(f"MISSING skills dir: {skills_dir}")
            continue

        for skill_name in sorted(os.listdir(skills_dir)):
            skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
            if not os.path.isfile(skill_path):
                errors.append(f"MISSING: {skill_path}")
                continue

            key = f"{plugin}/{skill_name}"
            guardrail_text = GUARDRAIL_MAP.get(key)
            if guardrail_text is None:
                errors.append(f"NO GUARDRAIL ENTRY: {key}")
                continue

            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Idempotency check
            if re.search(r'^## Reasoning Protocol', content, re.MULTILINE):
                skipped.append(key)
                continue

            new_content = insert_reasoning_protocol(content, guardrail_text)
            if new_content is None:
                errors.append(f"NO INSERTION POINT (no ## Pre-flight → next ##): {key}")
                continue

            with open(skill_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            modified.append(key)

    # ── Report ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"Task 6 — Reasoning Protocol Insertion Report")
    print(f"{'='*60}")
    print(f"\nModified ({len(modified)}):")
    for s in modified:
        print(f"  ✓ {s}")

    print(f"\nSkipped — already present ({len(skipped)}):")
    for s in skipped:
        print(f"  – {s}")

    print(f"\nErrors ({len(errors)}):")
    for s in errors:
        print(f"  ✗ {s}")

    print(f"\nTotal: {len(modified)} modified, {len(skipped)} skipped, {len(errors)} errors")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    process_all_skills()
