# rev-ops.pipeline-velocity-tracking

Tracks average sales cycle time by segment, rep, and deal size. Flags deals aging past 1.5x the historical average for their current stage. Surfaces velocity trend vs. prior quarter to surface where pipeline is slowing before it shows up in a missed quarter.

## Use it for

- Identify deals stalling in a specific stage before the quarter ends
- Compare current-quarter velocity trend vs. prior quarter
- Surface aging flags by rep and segment for manager coaching

## Don't use it for

- Prescribing manager coaching actions (G5 — analytical input only)
- Closing or updating deal stage records (G9 — no autonomous CRM edits)

## How to trigger it

Say something like:

- "pipeline velocity"
- "cycle time"
- "deals aging"
- "stalling pipeline"
- "how long are deals taking"

## What you get

- Pipeline velocity report with aging flags (stage-age ratio > 1.5x)

## Prerequisites

- HubSpot stage entry/exit date history
- Historical median days-in-stage by segment (trailing 4Q)

## Governance

- G5 — velocity flags are analytical inputs; manager owns coaching response
- G6 — data-as-of required on all stage history reads
- G7 — aging flags require manager escalation path

## See also

- rev-ops.stage-integrity-audit
- rev-ops.deal-health-scoring
- rev-ops.pipeline-coverage-analysis

---

*Domain: `rev-ops` · Skill ID: `rev-ops.pipeline-velocity-tracking`*
