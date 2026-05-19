# rev-ops.deal-classification

Classifies pipeline opportunities as Commit, Best Case, or Pipeline using independent CRM-signal scoring across five dimensions (activity recency, stakeholder coverage, stage-age, competitive signal, rep forecast accuracy). Classification is an analytical input (G5); it never overrides rep judgment or edits CRM records (G9).

## Use it for

- Score pipeline deals across five classification dimensions
- Assign Commit / Best Case / Pipeline category per deal
- Produce classification summary for forecast roll-up
- Flag deals where rep classification and signal-based classification diverge

## Don't use it for

- Overriding rep forecast category in CRM (G5 + G9)
- Deal health scoring (use deal-health-scoring for composite health)
- Approval routing (use deal-desk-workflow-management)

## How to trigger it

Say something like:

- "classify the pipeline"
- "commit vs best case vs pipeline"
- "deal classification"
- "forecast category scoring"
- "which deals are commits"

## What you get

- Deal classification table with dimension scores and category (Markdown)
- Divergence flags where rep vs. signal classification conflict

## Prerequisites

- Pipeline opportunity data from CRM (HubSpot preferred)
- Rep forecast category entries
- Historical win rate by segment (for stage-age benchmarks)

## Governance

- {'G1': 'all ARR figures flagged [review — not yet a revenue commitment]'}
- {'G5': 'classification is analytical input only; does not override rep judgment'}
- {'G6': 'data-as-of timestamp on all CRM reads'}
- {'G9': 'no CRM edits; classification output is read-only'}

## See also

- rev-ops.deal-health-scoring
- rev-ops.forecast-variance-analysis
- rev-ops.pipeline-coverage-analysis
- rev-ops.revenue-brief-generation

---

*Domain: `rev-ops` · Skill ID: `rev-ops.deal-classification`*
