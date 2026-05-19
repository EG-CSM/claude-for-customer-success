# rev-ops.outcome-to-value-tracking

Tracks value realization per account against OCV-defined milestones using L0-L3 rubric. Surfaces systemic patterns when L0 persistence exceeds 40% of accounts. Coordinates with deal-to-outcome-tracing for account-level detail. Only Ratified OCV entries used (G8).

## Use it for

- Assess value realization level (L0-L3) per account per OCV entry
- Track milestone achievement at OCV-defined intervals
- Flag systemic L0 persistence when >40% of accounts show no measurement
- Coordinate with deal-to-outcome-tracing for account-level detail

## Don't use it for

- Building OCV entries (use outcome-statement-builder)
- At-close completeness check (use deal-to-outcome-tracing)
- CRM edits (G9)

## How to trigger it

Say something like:

- "value tracking"
- "outcome to value"
- "are customers realizing value"
- "OCV milestone tracking"
- "L0-L3 value assessment"

## What you get

- Value realization report with L0-L3 scores per account-OCV pair (Markdown)
- Systemic pattern memo when L0 persistence >40%

## Prerequisites

- Ratified OCV entries per account (G8)
- CS platform activity and milestone data

## Governance

- {'G5': 'assessment is analytical input, not performance ruling'}
- {'G6': 'data-as-of timestamp on all reads'}
- {'G8': 'only Ratified OCV entries; provisional OCV flagged with [Low Confidence]'}

## See also

- rev-ops.deal-to-outcome-tracing
- rev-ops.outcome-statement-builder
- rev-ops.growth-model-vs-actuals-tracking

---

*Domain: `rev-ops` · Skill ID: `rev-ops.outcome-to-value-tracking`*
