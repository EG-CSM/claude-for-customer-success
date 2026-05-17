---
name: scenario-modeling
version: 1.0.0
description: "Builds P10/P50/P90 range forecasts from current pipeline state. Models win rate sensitivity, slip scenarios, and enterprise concentration risk. Produces structured scenario output consumed by annual-planning-workflow for three-scenario UoG capacity modeling. Triggers: 'forecast scenarios', 'P10 P50 P90', 'range forecast', 'what if win rate drops', 'downside scenario', 'upside scenario'."
---

# Scenario Modeling

Builds three calibrated forecast scenarios from current pipeline. The P10/P50/P90
output feeds directly into `annual-planning-workflow` for capacity planning.

**Reference:** Scenario construction formulas → `reference/revops-domain-model.md §4`
**Config reads:** `target_growth_pct`, `nrr_current`, `primary_segment`, `ae_quota`,
`ae_attainment_planning_rate`

---

## Reasoning Protocol

1. Confirm activation — user wants range forecast or scenario analysis
2. Check HubSpot for current pipeline state; declare confidence if unavailable
3. Read practice profile for win rate baseline and segment
4. Build all three scenarios; do not present only the optimistic one
5. Apply G1 — scenario outputs for finance or board require qualification language
6. Confirm destination before delivering

---

## Scenario Construction `[revops-domain-model.md §4]`

**P50 — Base case**
Current pipeline at historical win rates by stage and segment.
Win rates sourced from: HubSpot closed/won history trailing 4 quarters.

**P10 — Downside**
Win rates at 1 std dev below trailing 4Q average.
Enterprise accounts: apply concentration risk weighting if top 3 accounts
represent >30% of pipeline.

**P90 — Upside**
Win rates at trailing best quarter.
Late-stage deals (Negotiation+): assume close on current close date, not slipped.

---

## Output Format

```
FORECAST SCENARIOS — [Quarter/Period]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

New ARR Target: $XXXk (NRR-adjusted) [Practice profile]

Scenario    ARR        vs. Plan    Primary driver
P10         $XXXk      −XX%        [Win rate compression / slip / concentration]
P50         $XXXk      ±XX%        Base case — historical win rates
P90         $XXXk      +XX%        [Best-quarter win rates / on-time close]

P50–P10 spread: $XXXk  Primary driver: [factor]
P90–P50 spread: $XXXk  Primary driver: [factor]

Concentration risk: [Top 3 accounts = XX% of pipeline — HIGH/MODERATE/LOW]

Win rate sensitivity:
  −5pp win rate → −$XXXk ARR (P50 moves to $XXXk)
  +5pp win rate → +$XXXk ARR (P50 moves to $XXXk)

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G1: This is a range model, not a revenue commitment.]
```

---

## Handoff to Annual Planning

When used inside `annual-planning-workflow`, output these fields for UoG input:
```
p10_growth_pct: (P10_ARR − Current_ARR) ÷ Current_ARR
p50_growth_pct: (P50_ARR − Current_ARR) ÷ Current_ARR
p90_growth_pct: (P90_ARR − Current_ARR) ÷ Current_ARR
```
See: `/rev-ops:annual-planning-workflow --phase 1`

---

## Guardrails

- G1: All scenario outputs carry: "This is a range model based on current pipeline as
  of [date]. It is not a revenue commitment."
- G6: Data-as-of timestamp required on all pipeline pulls
