# CSM Plugin — Config Schema Reference

Documents every configurable field in the CSM plugin's `CLAUDE.md` template.
Skills read this schema to locate configuration values. `../../scripts/check-config-completeness.py`
validates that a deployed `CLAUDE.md` satisfies all required fields.

---

## Schema Overview

Config file location: `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`
Shared config: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

---

## Section: Who we are

Describes the CS motion and team context. Skills read this section for portfolio sizing,
segment targeting, and engagement model calibration.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `CS model` | Required | string | Engagement model label (e.g., "High-touch named CSM") | account-research, health-score-review, call-prep |
| `Primary segments` | Required | string | Comma-separated segment labels from domain model (Enterprise, Mid-Market, SMB) | health-score-review, taro-play-runner, value-statement |
| `Accounts per CSM` | Required | integer | Typical account load per CSM; used for capacity context | health-score-review, risk-flag |
| `CS methodology` | Optional | string | Named methodology in use (e.g., "TARO, Customer Journey") | taro-play-runner, success-plan-builder, call-prep |
| `Primary value metric` | Optional | string | Top outcome metric tracked (e.g., "Outcome achievement rate") | value-statement, qbr-builder, health-score-review |

---

## Section: Who's using this

Identifies the user role and escalation path. Skills use this for output tone calibration
and escalation routing.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Role` | Required | string | Job title of the primary user (e.g., "Customer Success Manager") | all skills (tone/authority calibration) |
| `Team` | Required | string | Team name (e.g., "Customer Success") | escalation-memo, risk-flag |
| `Manager / escalation contact` | Required | string | Name or role to escalate to; used in G4 escalation path | escalation-memo, risk-flag, health-score-review |

---

## Section: Available integrations

Declares which data connectors are live. Skills check this section to determine whether
to attempt live data retrieval or prompt user to provide data manually.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `CRM` | Required | string\|"none" | Connector name (e.g., "HubSpot") or "none" | account-research, health-score-review, stakeholder-map, all skills |
| `CS Platform` | Required | string\|"none" | Connector name (e.g., "Gainsight") or "none" | health-score-review, renewal-readiness, risk-flag |
| `Call recording` | Optional | string\|"none" | Connector name (e.g., "Gong") or "none" | call-prep, account-research |
| `Document storage` | Optional | string\|"none" | Connector name (e.g., "Google Drive") or "none" | qbr-builder, success-plan-builder, value-statement |

---

## Section: Outputs

Controls the structure of the Reviewer note appended to every skill output.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Reviewer note format` | Required | string | Template string for the Reviewer note block; must include data sources, confidence, and next-step fields | all skills (output generation) |

---

## Section: Decision posture

Sets the default risk tolerance for recommendations. Skills use this to calibrate
whether to flag borderline cases.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Default posture` | Required | string | "Conservative", "Balanced", or "Aggressive" | risk-flag, health-score-review, renewal-readiness, taro-play-runner |

---

## Section: Health score thresholds

Overrides the domain model default band cutoffs. If absent, skills fall back to
`../../shared/cs-domain-model.md` § Health Model defaults (Green ≥75, Yellow ≥50, Red ≥25).

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Green threshold` | Optional | integer (0–100) | Minimum score for Green band | health-score-review, risk-flag, stakeholder-map |
| `Yellow threshold` | Optional | integer (0–100) | Minimum score for Yellow band | health-score-review, risk-flag |
| `Red threshold` | Optional | integer (0–100) | Minimum score for Red band | health-score-review, risk-flag, escalation-memo |

---

## Section: Health score components

Configures the weighted components of the health model. Weights must sum to 100.
If this section is absent, skills use the domain model default weight ranges.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `product_usage_weight` | Optional | integer | Weight % for product usage component | health-score-review |
| `engagement_weight` | Optional | integer | Weight % for engagement component | health-score-review |
| `support_load_weight` | Optional | integer | Weight % for support load component | health-score-review |
| `nps_sentiment_weight` | Optional | integer | Weight % for NPS/sentiment component | health-score-review |
| `outcome_achievement_weight` | Optional | integer | Weight % for outcome achievement component | health-score-review |

Validation: all configured weights must sum to 100. Missing weights default to domain model ranges.

---

## Section: Data freshness

Sets the staleness threshold. Skills flag data older than this value with
`[stale — N days since last update]` and downgrade confidence.

| Field | Required | Type | Default | Skills that read |
|-------|----------|------|---------|-----------------|
| `Staleness threshold (days)` | Optional | integer | 14 (from domain model) | health-score-review, account-research, risk-flag, renewal-readiness |

CSM plugin note: the CSM CLAUDE.md template uses a 7-day threshold by default —
stricter than the domain model baseline of 14 days. Configure explicitly to override.

---

## Section: Account portfolio

Optional list of named accounts for quick-reference loading. Skills use this for
default account context when none is specified in the prompt.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Accounts` | Optional | list | Named accounts with ARR, segment, health, and renewal date | all skills (account context) |

Each entry format:
```
- Account: [name]
  ARR: [amount]
  Segment: [Enterprise|Mid-Market|SMB]
  Health: [score or band]
  Renewal: [date]
  CSM: [name]
```

---

## Section: Escalation matrix

Maps health bands and situation types to escalation owners. Required for G4 compliance
(no triage without escalation path).

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Red account escalation` | Required | string | Name or role of Red account escalation owner | risk-flag, escalation-memo, health-score-review |
| `Critical account escalation` | Required | string | Name or role for Critical (0–24) accounts | escalation-memo, health-score-review |
| `Executive escalation` | Optional | string | Executive sponsor or VP contact for executive escalation type | escalation-memo |
| `Technical escalation` | Optional | string | Engineering or Support lead for technical escalation type | escalation-memo |

---

## Shared Guardrails Reference

All skills in this plugin enforce the 7 shared guardrails from
`../../shared/cs-domain-model.md` § 7. These cannot be overridden by config.

| Guardrail | Governed behavior |
|-----------|------------------|
| G1 | Health scores are heuristics — never predict churn |
| G2 | Expansion requires economic buyer qualification |
| G3 | Revenue projections carry `[review — could be read as a revenue commitment]` |
| G4 | No triage without named escalation path |
| G5 | Confidentiality check before distributing account-level data |
| G6 | TARO plays are leads, not prescriptions |
| G7 | No silent stale data — always flag with date |

---

## Validation Rules for check-config-completeness.py

```
REQUIRED fields (plugin will not function correctly if absent):
  - Who we are: CS model, Primary segments, Accounts per CSM
  - Who's using this: Role, Team, Manager / escalation contact
  - Available integrations: CRM, CS Platform
  - Outputs: Reviewer note format
  - Decision posture: Default posture
  - Escalation matrix: Red account escalation, Critical account escalation

OPTIONAL fields (skills degrade gracefully when absent):
  - CS methodology, Primary value metric
  - Call recording, Document storage
  - Health score thresholds (falls back to domain model defaults)
  - Health score components (falls back to domain model weight ranges)
  - Staleness threshold (falls back to 14 days)
  - Account portfolio
  - Executive escalation, Technical escalation

CROSS-FIELD VALIDATIONS:
  - If health score components are configured, weights must sum to 100
  - Segment labels must match: Enterprise, Mid-Market, or SMB
  - Decision posture must be one of: Conservative, Balanced, Aggressive
```
