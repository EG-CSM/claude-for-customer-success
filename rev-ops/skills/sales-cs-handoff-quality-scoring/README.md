# rev-ops.sales-cs-handoff-quality-scoring

Scores each closed/won deal on five handoff dimensions (0–100). Pass threshold: 80. Below-threshold deals trigger a Linear issue assigned to the AE manager with 48-hour SLA. CS onboarding proceeds but CSM is notified of open issue. Dimensions: OCV entry referenced, trigger match, measurement source accessible, stakeholder map, risk flags documented.

## Use it for

- Score a specific deal or all recent closes on handoff quality
- Create Linear issue for below-threshold deals with named escalation path
- Notify CSM of handoff gaps without blocking onboarding

## Don't use it for

- Subjective prose quality assessment (scoring is binary per structured dimension)
- Handoff completion steps beyond scoring and escalation

## How to trigger it

Say something like:

- "handoff quality"
- "handoff score"
- "what's missing for [deal] handoff"
- "CS handoff check"
- "handoff completeness"

## What you get

- Handoff quality score per deal (N/100, pass/fail, failed dimensions)
- Linear issue for below-threshold deals (assigned to AE manager, 48h SLA)
- CSM notification for below-threshold deals
- Audit trail entry (timestamp, deal ID, score, failed dimensions, issue number)
- Weekly digest when run across all recent closes

## Prerequisites

- HubSpot deal fields for target deal(s)
- OCV catalog (ocv_catalog_path from practice profile) — Ratified entries only
- linear_connected flag from practice profile

## Governance

- G6 — data-as-of required on all reads
- G7 — every below-threshold flag includes named escalation path (AE manager, 48h SLA)
- G8 — only Ratified OCV entries count toward D1; Draft entries do not satisfy dimension
- G9 — no autonomous CRM edits; scoring is read-only

## See also

- rev-ops.revenue-leakage-scanning
- rev-ops.outcome-catalog-entry-builder
- onboarding domain skills

---

*Domain: `rev-ops` · Skill ID: `rev-ops.sales-cs-handoff-quality-scoring`*
