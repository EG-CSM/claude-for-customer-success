---
name: crm-hygiene-audit
version: 1.0.0
description: "Overall CRM health score plus rep-level hygiene scorecard across three dimensions: completeness, accuracy, and recency. Produces weekly hygiene report for RevOps review before sharing with Sales managers. Never writes to CRM — all corrections are proposals. Triggers: 'CRM hygiene', 'data quality', 'hygiene report', 'field completeness', 'CRM health score'."
---

# CRM Hygiene Audit

Three-dimension health score at portfolio and rep level. All corrections are
proposals — requires Write-tier confirmation before any CRM edits.

**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `crm_system`, `primary_segment`

---

## Reasoning Protocol

1. Confirm activation — user requesting hygiene audit or data quality review
2. Check HubSpot — full field scan required; declare scope limits if data is large
3. Apply G6 — data-as-of on all field reads
4. Apply governance Write-tier — no autonomous CRM edits; all corrections are proposals
5. Confirm scope: full portfolio, current quarter pipeline, or specific rep

---

## Three Dimensions

**Completeness** — Required fields populated at each stage gate
(per `field-completion-monitoring` gate definitions)

**Accuracy** — Field values passing format and logic validation:
- Close dates not in the past on open deals
- Stage inconsistent with activity history
- ACV outside segment range (flag for review, not auto-correct)
- Contact email format invalid

**Recency** — Staleness signals:
- Last activity date >14 days on open deal (G6 threshold)
- Last contact update >90 days
- Last stage change >30 days on non-stale deal

---

## Output Format

```
CRM HYGIENE AUDIT — [Scope] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

Overall health score: [N]/100  (vs. [N] prior week  ↑/↓)

Dimension breakdown:
  Completeness:  [N]/100  [N] deals with missing stage-gate fields
  Accuracy:      [N]/100  [N] deals with logic/format issues
  Recency:       [N]/100  [N] deals with stale activity (>14 days)

Rep scorecard:
Rep       Completeness   Accuracy   Recency   Overall
[Rep A]   92             88         85        88
[Rep B]   71             90         62        74  ⚠
[Rep C]   55             78         70        67  ⚠

Top 5 hygiene issues by revenue impact:
1. [Issue type] — [N] deals, $XXXk ACV — Action: [what to fix]
2. ...

[DRAFT — for RevOps review before sharing with Sales managers]
[Write-tier: CRM corrections require human confirmation before execution]
```

---

## Guardrails

- G6: Data-as-of required
- G9 (Write Protocol): No autonomous CRM edits
- G5: Rep scorecard shared with manager — manager owns the coaching response
