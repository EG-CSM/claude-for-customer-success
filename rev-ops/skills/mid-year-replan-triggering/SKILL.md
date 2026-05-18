---
name: mid-year-replan-triggering
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Monitors plan-vs-actual drift against the UoG baseline. Fires a replan recommendation when actuals diverge >15% from P50 plan, CS headroom crosses 10%, AE attainment runs >20pp below plan for 2+ months, or a material territory event occurs. Produces a replan recommendation memo with supporting data. Triggers: 'replan', 'plan vs actual drift', 'mid-year adjustment', 'are we off plan', 'should we replan'."
---

# Mid-Year Replan Triggering

Monitors four drift signals against the annual plan baseline. Produces a replan
recommendation memo when a trigger fires — not a replan itself.

**Reference:** UoG formulas → `../../../shared/revops-domain-model.md §5`
**Config reads:** `uog_baseline_path`, `target_growth_pct`, `current_csm_count`

---

## Use when
- Actuals have deviated materially from annual plan and replanning criteria need evaluation
- Mid-year variance triggers need to be assessed against configured thresholds
- Leadership needs structured recommendation on whether to initiate a replan

## Do NOT use for
- Annual planning execution (use annual-planning-workflow)
- Forecast variance analysis in isolation (use forecast-variance-analysis)
- Scenario modeling for a replan (use scenario-modeling after trigger fires)

## Typical activation
"Should we replan?", "mid-year replan", "replan trigger assessment", "are we off plan enough to replan", "evaluate replan criteria"

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

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal, customer, and revenue data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G1, G2 apply to all forward-looking outputs
- When baseline absent: always declare before analysis; never fabricate a comparison
