---
name: annual-planning-workflow
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Orchestrates the seven-phase annual (or mid-year) planning cycle: forecast scenarios → UoG three-scenario capacity modeling → territory optimization → quota sensitivity → comp simulation → baseline save → change communication. Each phase gates on human approval before the next begins. Invokes unit-of-growth-calculator for capacity modeling. Triggers: 'annual planning', 'planning cycle', 'run the plan', 'territory quota comp', 'mid-year replan'."
---

# Annual Planning Workflow

Seven-phase gated planning cycle. Each phase produces a human-approved artifact
before the next begins. Phases can be run individually with `--phase N`.

## Use when
- User initiates annual planning cycle, quota setting, or territory design process
- Annual planning workflow orchestration is needed across multiple RevOps domains
- GTM planning for a new fiscal year requires coordinated output across quota, territory, and comp

## Do NOT use for
- Individual quota calculations (use quota-sensitivity-analysis)
- Territory optimization in isolation (use territory-optimization)
- Comp modeling without full planning context (use comp-simulation)
- Mid-year replanning triggered by miss (use mid-year-replan-triggering)

## Typical activation
"Run annual planning", "start the planning cycle", "annual plan for [year]", "set quotas for next year", "kick off territory design"

**Invokes:** `unit-of-growth-calculator` v1.1.0 for capacity modeling (Phase 2)
**Reference:** UoG formulas → `../../../shared/revops-domain-model.md §5`
**Config reads:** All planning parameters from practice profile

---

## Reasoning Protocol

1. Confirm activation — user initiating annual or mid-year planning
2. Read practice profile — all seven planning parameters required; surface any missing ones
3. Check for existing plan baseline in `uog_baseline_path` — if present, offer update vs. new plan
4. Apply G2 — capacity model outputs are structural inputs, not hiring mandates
5. Apply G3 — comp plan outputs require HR + Finance dual review before rep communication
6. Apply G4 — territory proposals are drafts until dual-confirmed

---

## Seven Phases

### Phase 1 — Forecast Scenarios
Run `/rev-ops:scenario-modeling` to produce P10/P50/P90.

**Output:** Three-scenario table with ARR and growth % for each scenario.
**Gate:** RevOps lead confirms scenarios are reasonable before Phase 2.

---

### Phase 2 — UoG Three-Scenario Capacity Modeling

Invoke `unit-of-growth-calculator` once per scenario using Phase 1 output:

```
For each scenario (P10 / P50 / P90):
  target_growth_pct = (Scenario_ARR − Current_ARR) ÷ Current_ARR
  inputs: current_arr, target_growth_pct, nrr_current, segment, motion,
          ae_quota, ae_attainment_planning_rate, arr_per_csm, touch_model
```

Present as comparison table:

```
Metric              P10 Plan   P50 Plan   P90 Plan
New ARR target      $XXXk      $XXXk      $XXXk
AEs required        N          N          N
CSMs required       N          N          N
CS headroom %       XX%        XX%        XX%
Constraint signal   [signal]   [signal]   [signal]
```

**Gate — Critical Write:** RevOps lead selects planning scenario.
Default: P50 if no selection within 48 hours (logged).
CS constraint signal surfaced for all three — if CS is the binding constraint
even at P10, that is the primary action item regardless of scenario selected.

---

### Phase 3 — Territory Optimization

Run `/rev-ops:territory-optimization --draft`

**Gate — Critical Write:** RevOps lead + Sales lead dual confirmation before
any territory proposal is finalized.

---

### Phase 4 — Quota Sensitivity Analysis

Run `/rev-ops:quota-sensitivity-analysis` using UoG-confirmed AE headcount
and New ARR Target from the selected scenario.

**Gate:** RevOps lead confirms. Finance sign-off if quota changes >10%.

---

### Phase 5 — Comp Plan Simulation

Model payout at multiple attainment levels (50% / 65% / 75% / 85% / 100%).
Surface cost-to-company at each level. Flag unintended payout behaviors.

**Gate — Critical Write:** RevOps lead + HR/Finance dual confirmation.
G3 applies: no comp output distributed to reps without dual review.

---

### Phase 6 — Baseline Save

Write confirmed UoG output to the path specified in `uog_baseline_path`
(or prompt to set path if absent). This becomes the annual plan baseline
that `growth-model-vs-actuals-tracking` compares against all year.

**Gate — Critical Write:** RevOps lead only.

```
Saves: full UoG calculation_result for the selected scenario
       + confirmed planning decisions log
       + OCV catalog version reference
       + date, confirmed by [name]
```

---

### Phase 7 — Change Communication

Invoke `/rev-ops:change-communication-packaging` for any changes from
territory optimization (Phase 3), quota model (Phase 4), or comp plan (Phase 5).

**Gate:** RevOps lead reviews all packages before distribution.

---

## Phase Status Tracking

```
ANNUAL PLANNING — [FY/Period]
─────────────────────────────────────────────────────────
Phase 1  Forecast Scenarios          [ ] Pending / [✓] Complete / [⏸] Awaiting gate
Phase 2  Capacity Modeling (UoG)     [ ] / [✓] / [⏸]
Phase 3  Territory Optimization      [ ] / [✓] / [⏸]
Phase 4  Quota Sensitivity           [ ] / [✓] / [⏸]
Phase 5  Comp Plan Simulation        [ ] / [✓] / [⏸]
Phase 6  Baseline Save               [ ] / [✓] / [⏸]
Phase 7  Change Communication        [ ] / [✓] / [⏸]
─────────────────────────────────────────────────────────
```

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

- G1: Forecast scenario outputs qualify as range models, not revenue commitments
- G2: Capacity outputs include: "Structural input. Hiring requires budget approval."
- G3: Comp plan output includes: "Requires HR + Finance dual review before rep distribution."
- G4: Territory proposals labeled: "[DRAFT — not final until dual-confirmed]"
