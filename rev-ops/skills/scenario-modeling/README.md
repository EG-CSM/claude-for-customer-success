# rev-ops.scenario-modeling

Builds P10/P50/P90 range forecasts from current pipeline state. Models win rate sensitivity, slip scenarios, and enterprise concentration risk. Produces structured scenario output consumed by annual-planning-workflow for three-scenario UoG capacity modeling.

## Use it for

- Build downside/base/upside ARR scenarios from current pipeline
- Model win rate sensitivity (±5pp impact on ARR)
- Surface enterprise concentration risk when top 3 accounts exceed 30% of pipeline
- Produce P10/P50/P90 growth percentages for annual-planning-workflow Phase 1

## Don't use it for

- Individual deal forecasting (route to deal-health-scoring)
- Quota modeling (route to quota-sensitivity-analysis)

## How to trigger it

Say something like:

- "forecast scenarios"
- "P10 P50 P90"
- "range forecast"
- "what if win rate drops"
- "downside scenario"
- "upside scenario"

## What you get

- Three-scenario table (P10/P50/P90) with ARR, vs-plan, and primary driver
- Win rate sensitivity table (±5pp impact)
- Concentration risk flag when top 3 accounts > 30% of pipeline
- p10/p50/p90_growth_pct fields for annual-planning-workflow handoff

## Prerequisites

- HubSpot current pipeline with stage breakdown
- Win rate history (trailing 4Q) by stage and segment
- target_growth_pct, nrr_current, primary_segment, ae_quota, ae_attainment_planning_rate from company profile

## Governance

- {'G1 — all scenario outputs carry': 'This is a range model, not a revenue commitment'}
- G6 — data-as-of timestamp required on all pipeline pulls
- Present all three scenarios; do not surface only the optimistic one
- Confirm output destination before delivering

## See also

- rev-ops.annual-planning-workflow
- rev-ops.pipeline-coverage-analysis
- rev-ops.quota-sensitivity-analysis

---

*Domain: `rev-ops` · Skill ID: `rev-ops.scenario-modeling`*
