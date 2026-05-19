# rev-ops.stage-integrity-audit

Detects CRM hygiene issues that distort forecasts: stage-skipping (multi-stage jumps in one update), backward movement, and stale stage (stuck > 2x historical avg). Produces audit report for human review before any CRM edits. Never updates CRM autonomously.

## Use it for

- Identify deals with retroactive stage-skip entries
- Flag deals that moved backward (may indicate lost deal not yet closed)
- Surface stale-stage deals inflating pipeline with unlikely-to-close opportunities

## Don't use it for

- Executing CRM stage corrections (G9 — all changes are proposals for human review)
- Velocity trend analysis (route to pipeline-velocity-tracking)

## How to trigger it

Say something like:

- "stage integrity"
- "stage skipping"
- "backward movement"
- "CRM stage hygiene"
- "stale stage"

## What you get

- Stage integrity audit report (three pattern sections + recommended actions)

## Prerequisites

- HubSpot stage change history (entry/exit dates per deal)
- avg_sales_cycle_days and historical median by stage from practice profile

## Governance

- G9 (Write Protocol) — no autonomous CRM edits; all corrections are proposals requiring human confirmation
- G5 — stage anomalies are signals for manager and CRM admin review
- G6 — data-as-of required on all stage history reads

## See also

- rev-ops.pipeline-velocity-tracking
- rev-ops.crm-hygiene-audit
- rev-ops.forecast-variance-analysis

---

*Domain: `rev-ops` · Skill ID: `rev-ops.stage-integrity-audit`*
