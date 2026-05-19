# rev-ops.deal-health-scoring

Produces a 0-100 composite health score for pipeline deals across five weighted dimensions: activity recency (25%), stakeholder coverage (25%), stage-age ratio (20%), competitive signal (15%), rep forecast accuracy (15%). Scores below 50 trigger next-best-action recommendation. Output is analytical input only (G5); never edits CRM (G9).

## Use it for

- Score individual deals or full pipeline on five health dimensions
- Produce composite 0-100 health score per opportunity
- Flag deals below 50 for next-best-action routing
- Surface dimension-level detail for deal diagnosis

## Don't use it for

- Deal classification (Commit/Best Case/Pipeline) — use deal-classification
- Approval routing — use deal-desk-workflow-management
- CRM edits (G9)

## How to trigger it

Say something like:

- "deal health"
- "health score"
- "how healthy is this deal"
- "deal scoring"
- "at-risk deals"

## What you get

- Deal health scorecard with dimension scores and composite (Markdown)
- Sub-50 deal list with next-best-action routing flag

## Prerequisites

- Opportunity data from CRM (activity log, stage, stakeholder contacts)
- Rep forecast category entries
- Segment stage-age benchmarks

## Governance

- {'G5': 'output is analytical input; never overrides rep judgment'}
- {'G6': 'data-as-of timestamp on all CRM reads'}
- {'G7': 'escalation path present when sub-50 deals identified'}
- {'G9': 'no CRM edits'}

## See also

- rev-ops.deal-classification
- rev-ops.next-best-action-recommendation
- rev-ops.pipeline-velocity-tracking
- rev-ops.revenue-brief-generation

---

*Domain: `rev-ops` · Skill ID: `rev-ops.deal-health-scoring`*
