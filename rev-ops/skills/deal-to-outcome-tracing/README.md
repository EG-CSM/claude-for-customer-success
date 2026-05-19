# rev-ops.deal-to-outcome-tracing

Traces closed-won deals through post-close outcome milestones using the L0-L3 rubric (L0 no measurement, L1 tracking started, L2 milestone hit, L3 outcome validated). Runs at-close completeness checks (OCV entry, trigger match, measurement source) and milestone assessments at 30/60/90/180d. Coordinates with outcome-to-value-tracking for systemic pattern analysis.

## Use it for

- Run at-close completeness check for closed-won deals
- Assess outcome milestone achievement at 30/60/90/180d checkpoints
- Score each account-OCV pair on L0-L3 rubric
- Flag systemic L0 persistence when >40% of accounts show no measurement
- Structural fallback when OCV entry is absent

## Don't use it for

- Building OCV entries (use outcome-statement-builder)
- Full value tracking pattern analysis (use outcome-to-value-tracking)
- CRM edits (G9)

## How to trigger it

Say something like:

- "outcome tracing"
- "deal to outcome"
- "post-close milestone check"
- "how are outcomes tracking"
- "L0-L3 rubric assessment"

## What you get

- At-close completeness check report (Markdown)
- L0-L3 milestone assessment per account-OCV pair
- Systemic pattern flags when L0 persistence >40%

## Prerequisites

- Closed-won deal data with OCV entries (where available)
- Milestone definitions per checkpoint interval
- CS platform activity data

## Governance

- {'G5': 'assessment is analytical input, not performance ruling'}
- {'G6': 'data-as-of timestamp on all reads'}
- {'G8': 'only Ratified OCV entries used; provisional OCV flagged'}
- Structural fallback when OCV absent; Low confidence on inferred outcomes

## See also

- rev-ops.outcome-to-value-tracking
- rev-ops.outcome-statement-builder
- rev-ops.sales-cs-handoff-quality-scoring

---

*Domain: `rev-ops` · Skill ID: `rev-ops.deal-to-outcome-tracing`*
