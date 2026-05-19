# rev-ops.forecast-variance-analysis

Analyzes forecast vs. actuals variance across five root cause categories (deal slippage, classification error, competitive loss, timing shift, territory gap). Applies pattern confidence gate before surfacing systemic diagnosis (≥3 deals or ≥2 consecutive quarters). Output feeds revenue-brief generation and GTM metrics pulse.

## Use it for

- Compute forecast vs. actuals delta for a period
- Classify variance by root cause category
- Apply pattern confidence gate before systemic diagnosis
- Produce variance report with prioritized root cause ranking
- Feed variance findings into revenue-brief-generation

## Don't use it for

- Forecast generation (use deal-classification + scenario-modeling)
- CRM edits (G9)
- Pipeline coverage analysis (use pipeline-coverage-analysis)

## How to trigger it

Say something like:

- "forecast variance"
- "why did we miss"
- "forecast accuracy"
- "actuals vs forecast"
- "forecast analysis"

## What you get

- Variance report with root cause ranking (Markdown)
- Systemic pattern memo when confidence gate passes

## Prerequisites

- Forecast figures by period (from CRM or Finance sheets)
- Actuals by period
- Deal-level data for root cause attribution

## Governance

- {'G1': 'all ARR figures flagged [review — not yet a revenue commitment]'}
- {'G6': 'data-as-of timestamp on all reads'}
- {'Pattern confidence gate': '≥3 deals or ≥2 consecutive quarters before systemic diagnosis'}

## See also

- rev-ops.deal-classification
- rev-ops.revenue-brief-generation
- rev-ops.gtm-unified-metrics-pulse
- rev-ops.pipeline-coverage-analysis

---

*Domain: `rev-ops` · Skill ID: `rev-ops.forecast-variance-analysis`*
