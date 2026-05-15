# Renewals Plugin — Config Schema Reference

Documents every configurable field in the Renewals plugin's `CLAUDE.md` template.
Skills read this schema to locate configuration values. `../../scripts/check-config-completeness.py`
validates that a deployed `CLAUDE.md` satisfies all required fields.

---

## Schema Overview

Config file location: `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
Shared config: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

---

## Section: Who we are

Describes the renewals motion and book of business. Skills read this section for
portfolio context, deal sizing, and renewal model calibration.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Renewals motion` | Required | string | Description of renewal model (e.g., "Named renewals manager, co-owned with CSM") | renewal-forecast, negotiation-prep, executive-summary |
| `Primary segments` | Required | string | Comma-separated segment labels (Enterprise, Mid-Market, SMB) | renewal-forecast, churn-analysis, risk-assessment |
| `ARR under management` | Required | string | Total ARR in the renewals book (e.g., "$12M") | renewal-forecast, executive-summary |
| `Average deal size` | Required | string | Typical renewal deal size (e.g., "$85K") | negotiation-prep, renewal-forecast |
| `Renewal cycle` | Optional | string | Standard renewal term (e.g., "Annual") | renewal-forecast, contract-review |
| `Notice period` | Optional | integer (days) | Days of notice required for non-renewal | contract-review, renewal-forecast |

---

## Section: Who's using this

Identifies the user role, team, and key cross-functional contacts.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Role` | Required | string | Job title of the primary user (e.g., "Renewal Manager") | all skills (tone/authority calibration) |
| `Team` | Required | string | Team name (e.g., "Renewals") | escalation routing |
| `AE partner` | Required | string | Account Executive counterpart for expansion coordination | expansion-signal, negotiation-prep, executive-summary |
| `Finance / RevOps contact` | Required | string | Contact for G3 revenue commitment validation | renewal-forecast, executive-summary |

---

## Section: Available integrations

Declares which data connectors are live. Skills check this section to determine whether
to attempt live data retrieval or prompt the user to provide data manually.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `CRM` | Required | string\|"none" | Connector name (e.g., "Salesforce") or "none" | all skills |
| `CS Platform` | Required | string\|"none" | Connector name (e.g., "Gainsight") or "none" | churn-analysis, risk-assessment, expansion-signal |
| `Contract management` | Optional | string\|"none" | Connector name (e.g., "DocuSign") or "none" | contract-review |
| `CPQ / quoting` | Optional | string\|"none" | Connector name (e.g., "Salesforce CPQ") or "none" | expansion-signal, renewal-forecast |

---

## Section: Outputs

Controls the structure of the Reviewer note appended to every skill output.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Reviewer note format` | Required | string | Template string for the Reviewer note block | all skills |

---

## Section: Revenue commitment language

Configures the revenue commitment warning that G3 requires on all forecast outputs.
If absent, skills use the domain model default language.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Commitment disclaimer` | Optional | string | Override text for the `[review — could be read as a revenue commitment]` tag | renewal-forecast, executive-summary |
| `Finance validation required` | Optional | boolean | When true, add explicit Finance/RevOps review callout to every forecast output | renewal-forecast, executive-summary |

---

## Section: Decision posture

Sets the default risk tolerance for renewal recommendations.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Default posture` | Required | string | "Conservative", "Balanced", or "Aggressive" | risk-assessment, churn-analysis, negotiation-prep |

---

## Section: Pipeline stage weights

Overrides the domain model default renewal pipeline weights. If absent, skills use
`../../shared/cs-domain-model.md` § Renewal Forecast defaults.

| Field | Required | Type | Range | Description | Skills that read |
|-------|----------|------|-------|-------------|-----------------|
| `open_weight` | Optional | float (0–1) | default: 0.70 | Probability weight for Open stage | renewal-forecast |
| `verbal_commitment_weight` | Optional | float (0–1) | default: 0.90 | Probability weight for Verbal commitment | renewal-forecast |
| `at_risk_weight` | Optional | float (0–1) | default: 0.25 | Probability weight for At risk | renewal-forecast |
| `won_weight` | Optional | float (0–1) | default: 1.00 | Probability weight for Won | renewal-forecast |
| `lost_weight` | Optional | float (0–1) | default: 0.00 | Probability weight for Lost/Churn | renewal-forecast |

---

## Section: Scenario modeling parameters

Overrides scenario modeling percentages. If absent, skills use domain model defaults.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `best_case_open` | Optional | float (0–1) | Best case probability for Open accounts | renewal-forecast |
| `best_case_at_risk_save` | Optional | float (0–1) | Best case save rate for At-risk accounts | renewal-forecast |
| `worst_case_open` | Optional | float (0–1) | Worst case probability for Open accounts | renewal-forecast |
| `worst_case_verbal` | Optional | float (0–1) | Worst case probability for Verbal commitment | renewal-forecast |

---

## Section: Escalation matrix

Maps renewal risk levels to escalation owners.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `At-risk escalation` | Required | string | Name or role for At-risk account escalation | risk-assessment, churn-analysis |
| `Executive escalation` | Optional | string | Executive contact for strategic account renewals | negotiation-prep, executive-summary |

---

## Shared Guardrails Reference

All skills in this plugin enforce the 7 shared guardrails from
`../../shared/cs-domain-model.md` § 7.

| Guardrail | Governed behavior |
|-----------|------------------|
| G1 | Health scores are heuristics — never predict churn |
| G2 | Expansion requires economic buyer qualification before inclusion in NRR |
| G3 | Revenue projections carry commitment language + Finance validation callout |
| G4 | No triage without named escalation path |
| G5 | Confidentiality check before distributing account-level financial data |
| G6 | TARO plays are leads, not prescriptions |
| G7 | No silent stale data |

---

## Validation Rules for check-config-completeness.py

```
REQUIRED fields:
  - Who we are: Renewals motion, Primary segments, ARR under management, Average deal size
  - Who's using this: Role, Team, AE partner, Finance / RevOps contact
  - Available integrations: CRM, CS Platform
  - Outputs: Reviewer note format
  - Decision posture: Default posture
  - Escalation matrix: At-risk escalation

OPTIONAL fields (graceful degradation when absent):
  - Renewal cycle, Notice period
  - Contract management, CPQ / quoting
  - Commitment disclaimer, Finance validation required
  - All pipeline stage weight overrides (fall back to domain model)
  - All scenario modeling parameter overrides (fall back to domain model)
  - Executive escalation

CROSS-FIELD VALIDATIONS:
  - Segment labels must be: Enterprise, Mid-Market, or SMB
  - Pipeline stage weights must each be in range [0.0, 1.0]
  - Decision posture must be: Conservative, Balanced, or Aggressive
  - ARR under management must be parseable as a currency value
```
