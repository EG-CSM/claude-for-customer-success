# CS-Ops Plugin — Config Schema Reference

Documents every configurable field in the CS-Ops plugin's `CLAUDE.md` template.
Skills read this schema to locate configuration values. `../../scripts/check-config-completeness.py`
validates that a deployed `CLAUDE.md` satisfies all required fields.

---

## Schema Overview

Config file location: `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
Shared config: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

---

## Section: Who we are

Describes the CS Ops scope, portfolio, and organizational context. Skills read this
section for portfolio sizing, segment distribution, and ops model calibration.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `CS Ops scope` | Required | string | Description of CS Ops function (e.g., "Health model, capacity planning, playbook governance, data quality") | all skills |
| `Portfolio size` | Required | string | Total accounts under CS management (e.g., "320 accounts") | capacity-planner, segment-analyzer, metric-dashboard |
| `Segments managed` | Required | string | Comma-separated segment labels with headcount (e.g., "Enterprise: 80 accts, Mid-Market: 140, SMB: 100") | segment-analyzer, capacity-planner, health-model-review |
| `Total CSM headcount` | Required | integer | Number of CSMs in the team | capacity-planner |
| `Target accounts per CSM` | Required | string | Accounts-per-CSM target by segment (e.g., "Enterprise: 10, Mid-Market: 25, SMB: 50") | capacity-planner |

---

## Section: Who's using this

Identifies the user role and primary stakeholder contacts.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Role` | Required | string | Job title of the primary user (e.g., "Head of CS Operations") | all skills |
| `Team` | Required | string | Team name (e.g., "CS Operations") | escalation routing |
| `Primary stakeholders` | Required | string | Stakeholders who consume CS Ops outputs (e.g., "VP of Customer Success, Finance, RevOps") | metric-dashboard, executive outputs |
| `CS leadership contact` | Optional | string | VP or Director of CS for escalations | capacity-planner, health-model-review |
| `RevOps contact` | Optional | string | RevOps counterpart for data and systems alignment | data-quality-check, health-model-review |

---

## Section: Available integrations

Declares which data connectors are live. CS-Ops skills query multiple sources simultaneously;
all three primary sources should be configured.

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `CRM` | Required | string\|"none" | Connector name (e.g., "Salesforce") or "none" | all skills |
| `CS Platform` | Required | string\|"none" | Connector name (e.g., "Gainsight") or "none" | health-model-review, data-quality-check, metric-dashboard |
| `Data warehouse` | Optional | string\|"none" | Connector name (e.g., "Snowflake") or "none" | metric-dashboard, health-model-review, segment-analyzer |
| `BI tool` | Optional | string\|"none" | Connector name (e.g., "Looker") or "none" | metric-dashboard |
| `Survey tool` | Optional | string\|"none" | Connector name (e.g., "Delighted") or "none" | health-model-review, metric-dashboard |

---

## Section: Outputs

Controls the structure of the Reviewer note appended to every skill output.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Reviewer note format` | Required | string | Template string for the Reviewer note block; must reference data warehouse, CS Platform, and CRM sources when applicable | all skills |

---

## Section: Data freshness

CS-Ops uses a 14-day staleness threshold by default — longer than other plugins because
ops data is typically batch-processed. Skills flag data older than this value.

| Field | Required | Type | Default | Skills that read |
|-------|----------|------|---------|-----------------|
| `Staleness threshold (days)` | Optional | integer | 14 | all skills |

CS-Ops plugin note: this default matches the domain model baseline. Other plugins
(CSM: 7 days) are stricter. Do not lower below 7 days without validating data pipeline
refresh frequency.

---

## Section: Decision posture

Sets the default risk tolerance for ops recommendations (capacity flags, data quality
thresholds, health model calibration triggers).

| Field | Required | Type | Valid values | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Default posture` | Required | string | "Conservative", "Balanced", or "Aggressive" | capacity-planner, health-model-review, data-quality-check |

---

## Section: Metric targets

Configures the performance benchmarks used by `metric-dashboard` and `health-model-review`.
If absent, skills surface raw metrics without target comparison.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `GRR target` | Optional | float (0–1) | e.g., 0.88 for 88% GRR target | metric-dashboard |
| `NRR target` | Optional | float (0–1) | e.g., 1.10 for 110% NRR target | metric-dashboard |
| `TtV target (days)` | Optional | integer | Portfolio-level TtV target | metric-dashboard |
| `CSAT target` | Optional | float (0–5 or 0–10) | Customer satisfaction score target | metric-dashboard |
| `Onboarding completion rate target` | Optional | float (0–1) | Target % of accounts completing onboarding within plan | metric-dashboard |
| `Health score distribution target` | Optional | string | Target distribution by band (e.g., "Green: 70%, Yellow: 20%, Red: 10%") | health-model-review, metric-dashboard |

---

## Section: Segment definitions

Overrides domain model default segment boundaries. If absent, skills use the domain model
labels (Enterprise, Mid-Market, SMB) without ARR range enforcement.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Enterprise ARR floor` | Optional | string | Minimum ARR for Enterprise classification (e.g., "$100K") | segment-analyzer |
| `Mid-Market ARR floor` | Optional | string | Minimum ARR for Mid-Market classification (e.g., "$20K") | segment-analyzer |
| `SMB ARR floor` | Optional | string | Minimum ARR for SMB classification (e.g., "$1K") | segment-analyzer |
| `Enterprise accounts per CSM` | Optional | integer | Target account load for Enterprise CSMs | capacity-planner |
| `Mid-Market accounts per CSM` | Optional | integer | Target account load for Mid-Market CSMs | capacity-planner |
| `SMB accounts per CSM` | Optional | integer | Target account load for SMB CSMs (or pooled CSM ratio) | capacity-planner |

---

## Section: Playbook governance

Configures the playbook audit and governance parameters for `playbook-auditor`.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Playbook review cadence` | Optional | string | How often playbooks are formally reviewed (e.g., "Quarterly") | playbook-auditor |
| `Dead play threshold (days)` | Optional | integer | Days since last execution before a play is flagged as dead (default: 90) | playbook-auditor |
| `Low adoption threshold (%)` | Optional | integer | Execution rate below which a play is flagged for review (default: 20%) | playbook-auditor |

---

## Section: Data quality thresholds

Configures `data-quality-check` completeness and staleness flags.

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Required CRM fields` | Optional | list | Fields that must be populated on every account record | data-quality-check |
| `Required CS Platform fields` | Optional | list | Fields that must be populated on every health score record | data-quality-check |
| `Completeness target (%)` | Optional | integer | Target field completeness rate (default: 90%) | data-quality-check |

---

## Section: Escalation matrix

| Field | Required | Type | Description | Skills that read |
|-------|----------|------|-------------|-----------------|
| `Capacity alert escalation` | Required | string | Name or role for capacity over/under-allocation alerts | capacity-planner |
| `Data quality escalation` | Optional | string | Name or role for data quality failures | data-quality-check |
| `Health model escalation` | Optional | string | Name or role for health model calibration issues | health-model-review |

---

## Shared Guardrails Reference

All skills in this plugin enforce the 7 shared guardrails from
`../../shared/cs-domain-model.md` § 7.

| Guardrail | Governed behavior |
|-----------|------------------|
| G1 | Health scores are heuristics — never predict churn |
| G2 | Expansion ARR not counted until qualified |
| G3 | Revenue projections carry commitment language + Finance validation callout |
| G4 | No triage without named escalation path |
| G5 | Confidentiality check before distributing portfolio-level financial data |
| G6 | TARO plays are leads, not prescriptions |
| G7 | No silent stale data — always flag with date and staleness indicator |

---

## Validation Rules for check-config-completeness.py

```
REQUIRED fields:
  - Who we are: CS Ops scope, Portfolio size, Segments managed,
                Total CSM headcount, Target accounts per CSM
  - Who's using this: Role, Team, Primary stakeholders
  - Available integrations: CRM, CS Platform
  - Outputs: Reviewer note format
  - Decision posture: Default posture
  - Escalation matrix: Capacity alert escalation

OPTIONAL fields (graceful degradation when absent):
  - CS leadership contact, RevOps contact
  - Data warehouse, BI tool, Survey tool
  - Staleness threshold (falls back to 14 days)
  - All metric targets (metric-dashboard surfaces raw metrics without comparison)
  - All segment definition overrides (fall back to domain model labels)
  - Playbook governance fields (playbook-auditor uses defaults)
  - Data quality threshold overrides (data-quality-check uses defaults)
  - Data quality escalation, Health model escalation

CROSS-FIELD VALIDATIONS:
  - Decision posture must be: Conservative, Balanced, or Aggressive
  - GRR target must be in range [0.0, 1.0]
  - NRR target may exceed 1.0 (expansion)
  - Segment ARR floors must be in ascending order: SMB < Mid-Market < Enterprise
  - If per-segment accounts-per-CSM configured, must match segments in Segments managed
  - Dead play threshold must be a positive integer
  - Completeness target must be in range [0, 100]
```
