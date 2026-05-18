---
name: scenario-modeling
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Builds P10/P50/P90 range forecasts from current pipeline state. Models win rate sensitivity, slip scenarios, and enterprise concentration risk. Produces structured scenario output consumed by annual-planning-workflow for three-scenario UoG capacity modeling. Triggers: 'forecast scenarios', 'P10 P50 P90', 'range forecast', 'what if win rate drops', 'downside scenario', 'upside scenario'."
---

# Scenario Modeling

Builds three calibrated forecast scenarios from current pipeline. The P10/P50/P90
output feeds directly into `annual-planning-workflow` for capacity planning.

## Use when
- User needs to model multiple revenue or growth scenarios with named assumptions
- "What if" analysis across ACV targets, win rates, headcount, or churn rate assumptions
- Planning scenarios require structured comparison before commitment

## Do NOT use for
- Single-point forecasts without scenario comparison (use pipeline-coverage-analysis)
- Historical variance analysis (use forecast-variance-analysis)
- Territory optimization calculations (use territory-optimization)

## Typical activation
"Model three scenarios for next year", "what if win rate drops to 20%", "scenario analysis for [target]", "run bull/base/bear cases"

**Reference:** Scenario construction formulas → `../../../shared/revops-domain-model.md §4`
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

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential revenue planning and compensation data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G1: All scenario outputs carry: "This is a range model based on current pipeline as
  of [date]. It is not a revenue commitment."
- G6: Data-as-of timestamp required on all pipeline pulls
