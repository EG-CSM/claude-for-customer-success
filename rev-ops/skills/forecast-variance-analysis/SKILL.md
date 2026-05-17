---
name: forecast-variance-analysis
version: 1.0.0
description: "Compares submitted forecast to actual closed/won outcomes. Classifies variance by root cause: rep-level, deal-size band, stage-entry, seasonal, or product/segment. Surfaces systemic patterns — not one-off explanations. Minimum: 3 deals or 2 consecutive quarters before a pattern is surfaced. Triggers: 'why did we miss', 'forecast variance', 'call accuracy', 'forecast accuracy by rep', 'what caused the miss'."
---

# Forecast Variance Analysis

Traces the gap between what was called and what closed to its root cause.
Patterns require ≥3 deals or ≥2 consecutive quarters before surfacing.
One-off variance is noted but not classified as a pattern.

**Reference:** Variance classification taxonomy → `reference/revops-domain-model.md §4`
**Config reads:** `current_arr`, `primary_segment`, `crm_system`

---

## Reasoning Protocol

1. Confirm activation — user is asking about forecast accuracy, miss analysis, or call quality
2. Check HubSpot connector — multi-quarter history required; declare fallback if unavailable
3. Confirm the period being analyzed (default: most recently closed quarter)
4. Apply G6 — state data-as-of for all historical pipeline pulls
5. Apply G1 — any forward-looking variance projection requires forecast language qualification
6. Confirm output destination before delivering

---

## Inputs

Required:
- Period to analyze (default: most recently closed quarter)
- Submitted forecast at quarter-start (from HubSpot or user-provided)
- Actual closed/won (from HubSpot)

Optional:
- Rep filter, segment filter
- Number of prior quarters for trend analysis (default: 4)

---

## Workflow

**Step 1 — Calculate total variance**
```
Variance Amount = Submitted Forecast − Actual Closed/Won
Variance %      = Variance Amount ÷ Submitted Forecast
```

**Step 2 — Classify variance** `[revops-domain-model.md §4]`

For each deal that was in the submitted forecast but did not close, or closed at
a different amount, classify the contributing factor:

- **Rep-level** — specific rep consistently over/under-calling (≥3 deals, ≥2Q)
- **Deal-size band** — ACV range systematically slipping
- **Stage-entry** — deals entering a stage that historically don't close from there
- **Seasonal** — quarter-end compression patterns
- **Product/segment** — structural close-rate issue in specific product or segment

**Step 3 — Pattern confidence gate**
Only surface a pattern classification when:
- Rep-level: ≥3 deals from same rep, or same rep in ≥2 consecutive quarters
- All other categories: ≥3 deals matching the pattern

If below threshold: "Insufficient data to classify as systemic — noted as isolated."

**Step 4 — Rep call accuracy scorecard** (if rep data available)
```
Rep     Submitted    Actual    Variance    Accuracy
[name]  $XXXk        $XXXk     −$XXk       XX%
```

---

## Output Format

```
FORECAST VARIANCE ANALYSIS — [Quarter/Period]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Total variance: −$XXXk (−XX% of submitted forecast)

Root cause classification:
  Primary:   [Rep-level / Deal-size / Stage-entry / Seasonal / Product]
  Secondary: [if applicable]

Pattern evidence:
  "[Pattern description]" — observed in [N] deals over [N] quarters
  [Confidence: High/Moderate/Low — based on sample size]

Rep accuracy scorecard:
  [table if rep data available]

One-off variances (not classified as patterns):
  [Deal name, amount, what happened — 1 line each]

[DRAFT — RevOps internal] [Confidence: High/Moderate]
```

---

## Guardrails

- G1: Forward-looking projections from variance analysis require qualification
- G5: Rep accuracy scorecard is analytical input — manager owns the coaching response
- G6: State data-as-of for all historical pulls
