---
name: annual-planning-workflow
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Orchestrates the six-phase annual (or mid-year) planning cycle: forecast scenarios → UoG three-scenario capacity modeling → quota sensitivity → comp simulation → baseline save → change communication. Each phase gates on human approval before the next begins. Invokes unit-of-growth-calculator for capacity modeling. Triggers: 'annual planning', 'planning cycle', 'run the plan', 'quota comp planning', 'mid-year replan'."
---

[PROPOSED]

# Annual Planning Workflow

Seven-phase gated planning cycle. Each phase produces a human-approved artifact
before the next begins. Phases can be run individually with `--phase N`.

## Use when
- User initiates annual planning cycle, quota setting, or territory design process
- Annual planning workflow orchestration is needed across multiple RevOps domains
- GTM planning for a new fiscal year requires coordinated output across quota, territory, and comp

## Do NOT use for
- Individual quota calculations (use quota-sensitivity-analysis)
- Comp modeling without full planning context (use comp-simulation)
- Mid-year replanning triggered by miss (use mid-year-replan-triggering)

## Typical Activation
"Run annual planning", "start the planning cycle", "annual plan for [year]", "set quotas for next year", "kick off territory design"

**Invokes:** `unit-of-growth-calculator` v1.1.0 for capacity modeling (Phase 2)
**Reference:** UoG formulas → `../../../shared/revops-domain-model.md §5`
**Config reads:** All planning parameters from company profile

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `ae_quota`, `ae_attainment_planning_rate`, `current_ae_count`,
`arr_per_csm`, `nrr_current`, `avg_deal_acv`, `uog_baseline_path`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of planning request is this?
   - Full annual planning cycle (all 7 phases)
   - Mid-year replan (subset of phases)
   - Single-phase execution with `--phase N`
   - Baseline update vs. new plan

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user initiating annual or mid-year planning
   2. Read company profile — all seven planning parameters required; surface any missing ones
   3. Check for existing plan baseline in `uog_baseline_path` — if present, offer update vs. new plan
   4. Apply G2 — capacity model outputs are structural inputs, not hiring mandates
   5. Apply G3 — comp plan outputs require HR + Finance dual review before rep communication
   6. Apply G4 — territory proposals are drafts until dual-confirmed

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Are all seven company profile parameters populated and current?
   - Is the UoG baseline path configured? If absent, Phase 5 has no save target.
   - Has the forecast scenario (P10/P50/P90) been selected before capacity modeling begins?
   - Are CS constraint signals checked before AE headcount decisions? CS ceiling can invalidate an otherwise clean AE growth plan.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Skipping Phase 1 gate and running capacity modeling against an unvetted forecast
   - Distributing comp plan outputs before HR + Finance dual review (G3 violation)
   - Finalizing territory proposals without dual confirmation (G4 violation)
   - Running phases out of order — each phase gates on the prior phase's approved artifact

**After execution**, verify:
- Each phase artifact is labeled [DRAFT] until its gate is cleared
- Baseline save (Phase 5) only runs after the planning scenario is confirmed
- Confidence: High when all company profile parameters are populated and UoG baseline is present; Moderate when any parameter is estimated or baseline is absent
- Confidence: [High] when all planning parameters populated and connectors live / [Medium] when any parameter estimated or connector unavailable / [Low] if all inputs are manual or unverified

---

## Six Phases

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

### Phase 3 — Quota Sensitivity Analysis

Run `/rev-ops:quota-sensitivity-analysis` using UoG-confirmed AE headcount
and New ARR Target from the selected scenario.

**Gate:** RevOps lead confirms. Finance sign-off if quota changes >10%.

---

### Phase 4 — Comp Plan Simulation

Model payout at multiple attainment levels (50% / 65% / 75% / 85% / 100%).
Surface cost-to-company at each level. Flag unintended payout behaviors.

**Gate — Critical Write:** RevOps lead + HR/Finance dual confirmation.
G3 applies: no comp output distributed to reps without dual review.

---

### Phase 5 — Baseline Save

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

### Phase 6 — Change Communication

Invoke `/rev-ops:change-communication-packaging` for any changes from
the quota model (Phase 3) or comp plan (Phase 4).

**Gate:** RevOps lead reviews all packages before distribution.

---

## Output

Phase status tracker plus phase-specific artifacts: three-scenario capacity table (Phase 2), quota sensitivity table (Phase 3), comp simulation (Phase 4), baseline save confirmation (Phase 5), change communication package (Phase 6). Each phase artifact is labeled [DRAFT] until its gate is cleared.

## Phase Status Tracking

```
ANNUAL PLANNING — [FY/Period]
─────────────────────────────────────────────────────────
Phase 1  Forecast Scenarios          [ ] Pending / [✓] Complete / [⏸] Awaiting gate
Phase 2  Capacity Modeling (UoG)     [ ] / [✓] / [⏸]
Phase 3  Quota Sensitivity           [ ] / [✓] / [⏸]
Phase 4  Comp Plan Simulation        [ ] / [✓] / [⏸]
Phase 5  Baseline Save               [ ] / [✓] / [⏸]
Phase 6  Change Communication        [ ] / [✓] / [⏸]
─────────────────────────────────────────────────────────
```

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

- G1: Forecast scenario outputs qualify as range models, not revenue commitments
- G2: Capacity outputs include: "Structural input. Hiring requires budget approval."
- G3: Comp plan output includes: "Requires HR + Finance dual review before rep distribution."
- G4: Territory proposals labeled: "[DRAFT — not final until dual-confirmed]"
