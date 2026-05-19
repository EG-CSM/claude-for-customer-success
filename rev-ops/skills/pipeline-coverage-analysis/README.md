# rev-ops.pipeline-coverage-analysis

Computes pipeline coverage ratio (pipeline / quota) using segment-specific win rates rather than a universal 3x assumption. Signal thresholds: <2x CRITICAL, 2-3x AT-RISK, 3-5x HEALTHY, >5x INSPECT for concentration. Ranks top-3 pipeline exposure risks. Feeds GTM metrics pulse and revenue brief.

## Use it for

- Compute coverage ratio using segment-specific win rates
- Apply signal thresholds and categorize coverage health
- Rank top-3 exposure risks by segment or team
- Feed coverage data into gtm-unified-metrics-pulse and revenue-brief-generation

## Don't use it for

- Pipeline velocity (stage-age tracking) — use pipeline-velocity-tracking
- Deal health scoring — use deal-health-scoring
- Forecast variance — use forecast-variance-analysis

## How to trigger it

Say something like:

- "pipeline coverage"
- "do we have enough pipeline"
- "coverage ratio"
- "pipeline health"
- "coverage analysis"

## What you get

- Coverage analysis report with signal classification by segment (Markdown)
- Top-3 exposure risk ranking

## Prerequisites

- Pipeline data from CRM (HubSpot preferred)
- Quota by segment/team for the period
- Win rate by segment (required; no universal 3x assumption)

## Governance

- {'G1': 'all ARR figures flagged [review — not yet a revenue commitment]'}
- {'G6': 'data-as-of timestamp on all reads'}
- Coverage = pipeline ÷ (quota ÷ win rate); never use universal 3x

## See also

- rev-ops.gtm-unified-metrics-pulse
- rev-ops.revenue-brief-generation
- rev-ops.pipeline-velocity-tracking
- rev-ops.scenario-modeling

---

*Domain: `rev-ops` · Skill ID: `rev-ops.pipeline-coverage-analysis`*
