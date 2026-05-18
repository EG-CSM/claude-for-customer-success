---
name: forecast-variance-analysis
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Compares submitted forecast to actual closed/won outcomes. Classifies variance by root cause: rep-level, deal-size band, stage-entry, seasonal, or product/segment. Surfaces systemic patterns — not one-off explanations. Minimum: 3 deals or 2 consecutive quarters before a pattern is surfaced. Triggers: 'why did we miss', 'forecast variance', 'call accuracy', 'forecast accuracy by rep', 'what caused the miss'."
---

# Forecast Variance Analysis

Traces the gap between what was called and what closed to its root cause.
Patterns require ≥3 deals or ≥2 consecutive quarters before surfacing.
One-off variance is noted but not classified as a pattern.

**Reference:** Variance classification taxonomy → `../../../shared/revops-domain-model.md §4`
**Config reads:** `current_arr`, `primary_segment`, `crm_system`

---

## Use when
- Actual results deviate from forecast and root cause analysis is needed
- Post-quarter variance review requires structured decomposition
- Forecast accuracy trending needs to be assessed across periods

## Do NOT use for
- Forward-looking scenario modeling (use scenario-modeling)
- Pipeline coverage adequacy (use pipeline-coverage-analysis)
- Individual deal health (use deal-health-scoring)

## Typical activation
"Forecast variance analysis", "why did we miss forecast", "actuals vs forecast for Q[N]", "variance decomposition", "forecast accuracy review"

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

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal and pipeline data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G1: Forward-looking projections from variance analysis require qualification
- G5: Rep accuracy scorecard is analytical input — manager owns the coaching response
- G6: State data-as-of for all historical pulls
