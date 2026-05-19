# rev-ops.crm-hygiene-audit

Audits CRM data quality across four hygiene dimensions: field completion, stage integrity, duplicate presence, and data decay. Produces a scored hygiene report with prioritized remediation recommendations. All findings are read-only proposals; skill never edits CRM records autonomously (G9).

## Use it for

- Score overall CRM hygiene across four dimensions
- Identify field completion gaps by stage gate
- Flag stage-skipping, backward movement, or stale stage anomalies
- Surface duplicate account/contact/opportunity candidates
- Report data decay signals for accounts not updated within decay threshold

## Don't use it for

- Executing CRM edits (G9 — output is proposals only)
- Deep duplicate merging (use duplicate-detection for confidence scoring)
- Forecast variance analysis (use forecast-variance-analysis)

## How to trigger it

Say something like:

- "CRM audit"
- "hygiene audit"
- "data quality review"
- "clean up the CRM"
- "how healthy is our CRM data"

## What you get

- Hygiene scorecard with dimension scores (Markdown)
- Prioritized remediation recommendation list

## Prerequisites

- CRM data access (HubSpot preferred per data authority hierarchy)
- Stage definitions and field completion requirements per stage

## Governance

- {'G6': 'all data reads must surface data-as-of timestamp'}
- {'G9': 'no autonomous CRM edits; all findings are proposals'}
- {'G7': 'escalation path present for critical hygiene failures'}

## See also

- rev-ops.field-completion-monitoring
- rev-ops.stage-integrity-audit
- rev-ops.duplicate-detection
- rev-ops.data-decay-tracking

---

*Domain: `rev-ops` · Skill ID: `rev-ops.crm-hygiene-audit`*
