---
name: scenario-modeling
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Builds P10/P50/P90 range forecasts from current pipeline state. Models win rate sensitivity, slip scenarios, and enterprise concentration risk. Produces structured scenario output consumed by annual-planning-workflow for three-scenario UoG capacity modeling. Triggers: 'forecast scenarios', 'P10 P50 P90', 'range forecast', 'what if win rate drops', 'downside scenario', 'upside scenario'."
---

[PROPOSED]

# Scenario Modeling

Builds three calibrated forecast scenarios from current pipeline. The P10/P50/P90
output feeds directly into `annual-planning-workflow` for capacity planning.

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `target_growth_pct`, `nrr_current`, `primary_segment`, `ae_quota`, `ae_attainment_planning_rate`

---

## Use when
- User needs to model multiple revenue or growth scenarios with named assumptions
- "What if" analysis across ACV targets, win rates, headcount, or churn rate assumptions
- Planning scenarios require structured comparison before commitment

## Do NOT use for
- Single-point forecasts without scenario comparison (use pipeline-coverage-analysis)
- Historical variance analysis (use forecast-variance-analysis)


## Typical Activation
"Model three scenarios for next year", "what if win rate drops to 20%", "scenario analysis for [target]", "run bull/base/bear cases"

**Reference:** Scenario construction formulas → `../../../shared/revops-domain-model.md §4`
**Config reads:** `target_growth_pct`, `nrr_current`, `primary_segment`, `ae_quota`,
`ae_attainment_planning_rate`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of scenario modeling request is this?
   - Single-period range forecast (P10/P50/P90 for one quarter or year)
   - Win rate sensitivity analysis (impact of win rate shift on ARR outcome)
   - Concentration risk scenario (enterprise account weighting on downside)
   - Annual planning handoff (structured UoG growth pct output for capacity modeling)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting range forecast, what-if analysis, or named scenario comparison
   2. Pull current pipeline state from HubSpot filtered to relevant period; declare connector status
   3. Read company profile for win rate baseline, segment definition, and growth target
   4. Build all three scenarios (P10/P50/P90) — never present only the optimistic case
   5. Apply G1 — scenario outputs for Finance or board require qualification language
   6. Apply G6 — data-as-of timestamp required on all HubSpot pipeline reads
   7. Confirm output destination before delivering — internal RevOps vs. Finance vs. leadership

3. **EXPERT CHECK**: What would a veteran RevOps scenario analyst verify before surfacing outputs?
   - Is the win rate source declared and scoped correctly? Win rates must be stage-and-segment-specific,
     not a single blended rate — applying a blended rate to a pipeline with different stage mix
     than history produces a structurally invalid P50.
   - Is concentration risk assessed before surfacing P10? If the top 3 enterprise accounts
     represent >30% of pipeline, a standard 1-std-dev downside understates the true P10 —
     concentration risk weighting is required, not optional.
   - Is the P90 upside disciplined or aspirational? Best-quarter win rates applied to current
     pipeline is defensible; applying a higher win rate "because the team feels good" is not
     a scenario model — it's a hope. Flag the assumption explicitly.
   - Is the handoff to annual-planning-workflow declared? If this output feeds UoG capacity
     modeling, the growth pct fields must be computed and surfaced explicitly — not implied
     from the ARR numbers.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting only P50 or only the optimistic scenario (hides structural risk from leadership)
   - Applying a blended win rate without stage-and-segment breakdown (produces false precision)
   - Pulling HubSpot pipeline data without data-as-of timestamp (G6 violation)
   - Surfacing scenario outputs to Finance or board without G1 qualification language

**After execution**, verify:
- G1 qualification present on all scenario outputs leaving RevOps
- G6 data-as-of label applied to all HubSpot pipeline reads
- All three scenarios (P10/P50/P90) present — no single-scenario delivery
- Win rate source declared and labeled (company profile or HubSpot trailing actuals)
- Confidence: High when HubSpot is connected and pipeline data is current; Moderate when connector unavailable or win rate is from company profile only
    - Confidence: [High] when HubSpot is connected and pipeline data is current / [Medium] when connector unavailable or win rate is from company profile only / [Low] if all inputs are manual or unverified

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

## Output

```
FORECAST SCENARIOS — [Quarter/Period]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

New ARR Target: $XXXk (NRR-adjusted) [Company profile]

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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

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
