---
name: mid-year-replan-triggering
version: 1.0.0
description: "Monitors plan-vs-actual drift against the UoG baseline. Fires a replan recommendation when actuals diverge >15% from P50 plan, CS headroom crosses 10%, AE attainment runs >20pp below plan for 2+ months, or a material territory event occurs. Produces a replan recommendation memo with supporting data. Triggers: 'replan', 'plan vs actual drift', 'mid-year adjustment', 'are we off plan', 'should we replan'."
---

# Mid-Year Replan Triggering

Monitors four drift signals against the annual plan baseline. Produces a replan
recommendation memo when a trigger fires — not a replan itself.

**Reference:** UoG formulas → `reference/revops-domain-model.md §5`
**Config reads:** `uog_baseline_path`, `target_growth_pct`, `current_csm_count`

---

## Reasoning Protocol

1. Confirm activation — user asking about plan drift or replan need
2. Read UoG baseline from `uog_baseline_path` — if absent, declare and run in reporting mode
3. Read current actuals from HubSpot and practice profile
4. Compare actuals vs. baseline on all four trigger dimensions
5. Apply G1 — replan recommendation for finance requires forecast language qualification
6. Apply G2 — headcount signals in replan are structural inputs, not hiring mandates

---

## Four Trigger Dimensions

```
Trigger 1 — ARR drift
  Signal: Actuals tracking >15% below or above P50 plan at mid-quarter
  Compare: Closed/won YTD vs. (new_arr_target × quarters_elapsed ÷ 4)

Trigger 2 — CS headroom breach
  Signal: CS headroom % has dropped below 10%
  Compare: Current (csm_count × arr_per_csm − current_arr) ÷ current_arr

Trigger 3 — AE attainment shortfall
  Signal: AE attainment running >20pp below planning rate for ≥2 consecutive months
  Compare: Monthly closed/won ÷ monthly quota target

Trigger 4 — Territory event
  Signal: Rep departure, major account loss, or segment shift materially changes inputs
  Source: User-reported or CRM departure detection
```

**When no UoG baseline exists:**
Run in reporting mode only. Report actuals without variance analysis.
Label: `[Variance analysis unavailable — UoG baseline not configured. Reporting actuals only.]`

---

## Output Format

```
MID-YEAR REPLAN ASSESSMENT — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Low]

Trigger check:
  ARR drift:         [FIRING / Clear]  Actuals $XXXk vs. plan $XXXk (−XX%)
  CS headroom:       [FIRING / Clear]  Headroom XX% (threshold: 10%)
  AE attainment:     [FIRING / Clear]  Trailing 2mo avg: XX% vs. XX% planned
  Territory event:   [FIRING / Clear]  [Event description if applicable]

Recommendation: [REPLAN RECOMMENDED / No replan needed]

If replan recommended:
  Primary trigger: [which fired]
  Projected year-end ARR without replan: $XXXk (vs. $XXXk plan)
  Recommended replan scope: [Full / Targeted — Phase [N] only]
  Urgency: [Immediate / Next planning cycle]

To initiate replan: /rev-ops:annual-planning-workflow --phase [1 or relevant phase]

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G1: Projections are models, not revenue commitments]
[G2: Headcount signals are structural inputs. Hiring requires budget approval.]
```

---

## Guardrails

- G1, G2 apply to all forward-looking outputs
- When baseline absent: always declare before analysis; never fabricate a comparison
