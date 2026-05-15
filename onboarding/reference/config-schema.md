# Onboarding Plugin — Config Schema Reference

Documents every configurable field in the Onboarding plugin's `CLAUDE.md` template.
Skills read this schema to locate configuration values. `../../scripts/check-config-completeness.py`
validates that a deployed `CLAUDE.md` satisfies all required fields.

---

## Schema Overview

Config file location: `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
Shared config: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

---

## Section: Who we are

Describes the onboarding model and team structure. Skills read this section for
milestone planning, TtV calibration, and handoff point targeting.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Onboarding model` | Required | string | Description of model (e.g., "Dedicated Onboarding Manager per account through M5") | onboarding-plan, kickoff-prep, handoff-doc |
| `Primary segments` | Required | string | Comma-separated segment labels (Enterprise, Mid-Market, SMB) | milestone-tracker, ttv-analysis, blocker-review |
| `Average onboarding duration` | Required | string | Typical onboarding length by segment (e.g., "Enterprise: 90 days, Mid-Market: 60 days") | ttv-analysis, onboarding-plan, milestone-tracker |
| `Target TtV` | Required | string | Target Time-to-Value in days by segment (e.g., "Enterprise: 75 days, Mid-Market: 45 days") | ttv-analysis, milestone-tracker |
| `Handoff point` | Required | string | Milestone at which account transfers to CSM (e.g., "M5 completion") | handoff-doc, milestone-tracker |

---

## Section: Who's using this

Identifies the user role and key cross-functional contacts.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Role` | Required | string | Job title of the primary user (e.g., "Onboarding Manager") | all skills |
| `Team` | Required | string | Team name (e.g., "Customer Onboarding") | escalation routing |
| `Handoff point contact` | Required | string | CSM team contact who receives the handoff (e.g., "CS team lead") | handoff-doc, milestone-tracker |
| `Technical counterpart` | Optional | string | Solutions Engineer or Implementation contact | blocker-review, kickoff-prep, onboarding-plan |

---

## Section: Available integrations

Declares which data connectors are live.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `CRM` | Required | string\|"none" | Connector name or "none" | all skills |
| `CS Platform` | Required | string\|"none" | Connector name (e.g., "Gainsight") or "none" | milestone-tracker, ttv-analysis, blocker-review |
| `Project management` | Optional | string\|"none" | Connector name (e.g., "Asana") or "none" | onboarding-plan, milestone-tracker, kickoff-prep |
| `Document storage` | Optional | string\|"none" | Connector name (e.g., "Google Drive") or "none" | handoff-doc, success-criteria |

---

## Section: Outputs

Controls the structure of the Reviewer note appended to every skill output.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Reviewer note format` | Required | string | Template string for the Reviewer note block | all skills |

---

## Section: TtV accuracy framing

Controls how TtV outputs are labeled to enforce the internal-use-only constraint
(domain model § TtV framing rule).

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `TtV disclaimer` | Optional | string | Override text for the `[review — internal planning target]` tag on TtV outputs | ttv-analysis, milestone-tracker |

If absent, skills use the default domain model framing: `[review — internal planning target]`.

---

## Section: Milestone definitions

Configures the milestone ladder used across all onboarding skills. Default milestone
set is M0–M5; customizable labels and target days per milestone.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `M0_label` | Optional | string | Milestone 0 label (default: "Contract signed / kickoff scheduled") | milestone-tracker, onboarding-plan, ttv-analysis |
| `M1_label` | Optional | string | Milestone 1 label (default: "Technical setup complete") | milestone-tracker, onboarding-plan |
| `M2_label` | Optional | string | Milestone 2 label (default: "User onboarding complete") | milestone-tracker, onboarding-plan |
| `M3_label` | Optional | string | Milestone 3 label (default: "Initial workflow live") | milestone-tracker, onboarding-plan |
| `M4_label` | Optional | string | Milestone 4 — First Value (required label; marks TtV endpoint) | ttv-analysis, milestone-tracker, handoff-doc |
| `M5_label` | Optional | string | Milestone 5 — Graduation/handoff (required label; marks onboarding close) | handoff-doc, milestone-tracker |
| `M1_target_days` | Optional | integer | Target days from M0 to M1 completion | ttv-analysis, milestone-tracker |
| `M2_target_days` | Optional | integer | Target days from M0 to M2 completion | ttv-analysis, milestone-tracker |
| `M3_target_days` | Optional | integer | Target days from M0 to M3 completion | ttv-analysis, milestone-tracker |
| `M4_target_days` | Optional | integer | Target days from M0 to M4 completion; defines TtV target | ttv-analysis, milestone-tracker |
| `M5_target_days` | Optional | integer | Target days from M0 to M5 completion; defines full onboarding duration target | milestone-tracker, handoff-doc |

Note: M4 and M5 labels are structurally significant even if the text is customized —
these positions always map to First Value and Graduation respectively.

---

## Section: Decision posture

Sets the default risk tolerance for blocker escalation and milestone flagging.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Default posture` | Required | string | "Conservative", "Balanced", or "Aggressive" | blocker-review, milestone-tracker |

---

## Section: Escalation matrix

Maps blocker types and stalled onboarding scenarios to escalation owners.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Technical blocker escalation` | Required | string | Name or role for technical onboarding blockers | blocker-review |
| `Stakeholder blocker escalation` | Required | string | Name or role for customer-side stakeholder blockers | blocker-review |
| `Executive escalation` | Optional | string | Executive contact for strategic account onboarding issues | blocker-review |

---

## Shared Guardrails Reference

All skills in this plugin enforce the 7 shared guardrails from
`../../shared/cs-domain-model.md` § 7.

| Guardrail | Governed behavior |
|-----------|------------------|
| G1 | Health scores are heuristics — never predict churn |
| G2 | Expansion requires economic buyer qualification |
| G3 | Revenue projections carry commitment language |
| G4 | No triage without named escalation path |
| G5 | Confidentiality check before distributing account-level data |
| G6 | TARO plays are leads, not prescriptions |
| G7 | No silent stale data |

Onboarding-specific guardrail: TtV figures are **internal planning targets only** —
never include in customer-facing communications. All TtV outputs carry
`[review — internal planning target]`.

---

## Validation Rules for check-config-completeness.py

```
REQUIRED fields:
  - Who we are: Onboarding model, Primary segments, Average onboarding duration,
                Target TtV, Handoff point
  - Who's using this: Role, Team, Handoff point contact
  - Available integrations: CRM, CS Platform
  - Outputs: Reviewer note format
  - Decision posture: Default posture
  - Escalation matrix: Technical blocker escalation, Stakeholder blocker escalation

OPTIONAL fields (graceful degradation when absent):
  - Technical counterpart
  - Project management, Document storage
  - TtV disclaimer (falls back to domain model default)
  - All milestone label overrides (fall back to M0–M5 defaults)
  - All milestone target day overrides
  - Executive escalation

CROSS-FIELD VALIDATIONS:
  - Segment labels must be: Enterprise, Mid-Market, or SMB
  - Decision posture must be: Conservative, Balanced, or Aggressive
  - M4_target_days must be less than M5_target_days if both are configured
  - TtV target values must be parseable as integers (days)
  - Milestone target days must be in ascending order M1 < M2 < M3 < M4 < M5
```
