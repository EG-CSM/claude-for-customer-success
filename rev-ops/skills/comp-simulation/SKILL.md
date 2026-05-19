---
name: comp-simulation
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Models comp plan payout scenarios before plan is finalized. Stress-tests OTE, accelerators, and threshold structures against attainment distributions (50/65/75/85/100%). Surfaces cost-to-company and unintended payout behaviors. G3 applies — all outputs require HR + Finance dual review before rep distribution. Triggers: 'comp simulation', 'model comp payouts', 'comp plan cost', 'stress test comp plan', 'what does the plan cost at 80/100/120%'."
---

[PROPOSED]

# Comp Simulation

Comp plan payout modeling. Surfaces cost-to-company at multiple attainment levels
and flags unintended payout behaviors before the plan is finalized.

G3 applies: all comp outputs require HR + Finance dual review before rep distribution.

## Use when
- User needs to model comp plan payout scenarios before plan is finalized
- Comp plan design requires stress-testing against attainment distributions
- Sensitivity analysis on OTE, accelerators, or threshold structures needed

## Do NOT use for
- Approved comp decisions (outputs are models only — G3 applies)
- Quota setting without comp context (use quota-sensitivity-analysis)
- Full annual planning orchestration (use annual-planning-workflow)

## Typical Activation
"Simulate comp plan payouts", "comp modeling for [role]", "what does the plan cost at 80/100/120% attainment", "stress test the comp plan"

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `ae_quota`, `ae_attainment_planning_rate`, `current_ae_count`, OTE inputs from company profile

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `ae_quota`, `ae_attainment_planning_rate`, `current_ae_count`, OTE inputs from company profile

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of comp simulation request is this?
   - Full plan payout modeling (all attainment levels)
   - Stress-test of specific structure (threshold, accelerator, cliff)
   - Cost-to-company analysis at a single scenario
   - Comparison of two or more plan structures

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user modeling comp plan payouts or stress-testing comp structure
   2. Read OTE, quota, and accelerator inputs from company profile or user-provided parameters
   3. Apply G3 — all outputs labeled with HR + Finance dual-review requirement before any rep distribution
   4. Model at all five attainment levels; flag any cliff effects, kink points, or unintended payout concentrations
   5. Surface cost-to-company at each level alongside per-rep payout
   6. Confirm this is being run inside `annual-planning-workflow` (Phase 5) or standalone

3. **EXPERT CHECK**: What would a veteran RevOps comp designer verify first?
   - Are OTE inputs current and confirmed by HR — not estimated from memory?
   - Is the threshold structure explicit? A missing threshold means variable pays at any attainment.
   - Does the accelerator math produce an unintended cliff at 100% crossing?
   - Is the AE count confirmed — not a headcount plan assumption?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting comp simulation output as a finalized plan (G3 violation)
   - Omitting threshold cliff flags when the payout jump exceeds 25%
   - Running cost-to-company without confirming current headcount
   - Distributing outputs before HR + Finance dual review

**After execution**, verify:
- G3 label present on all outputs: "Requires HR + Finance dual review before rep distribution."
- Unintended behavior flags section populated (or "NONE DETECTED" explicitly stated)
- Confidence: High when OTE and quota are confirmed from company profile; Moderate when any input is estimated
    - Confidence: [High] when OTE and quota are confirmed from company profile / [Medium] when any input is estimated / [Low] if all inputs are manual or unverified

---

## Workflow

```
Inputs (from company profile or user-provided):
  ote_base         = base salary component
  ote_variable     = variable / at-risk component
  ae_quota         = per-rep quota for the plan period
  accelerator_rate = multiplier applied above 100% attainment (if applicable)
  threshold_pct    = minimum attainment required before variable pays out
  current_ae_count = number of AEs in model

Per-rep payout at each attainment level:
  At 50%:  payout = ote_variable × 0.50  (if above threshold; else $0)
  At 65%:  payout = ote_variable × 0.65
  At 75%:  payout = ote_variable × 0.75  ← planning rate
  At 85%:  payout = ote_variable × 0.85
  At 100%: payout = ote_variable × 1.00
  At 120%: payout = ote_variable × 1.00 + (quota × 0.20 × accelerator_rate)

Cost-to-company at each level:
  ctc = (ote_base + per_rep_payout) × current_ae_count

Unintended behavior flags:
  - Threshold cliff: if payout jumps >25% at threshold crossing → flag
  - Accelerator concentration: if >30% of total plan cost comes from accelerator zone → flag
  - Underwater OTE: if at P50 attainment, per-rep payout < 50% of ote_variable → flag as retention risk
```

---

## Output

```
COMP SIMULATION [DRAFT]
[Company profile] [Confidence: High if OTE confirmed / Moderate if estimated]
[G3: Requires HR + Finance dual review before rep distribution]

Inputs:
  OTE (base / variable): $XXXk / $XXXk
  Per-rep quota: $XXXk
  Accelerator rate: Xx above 100%
  Threshold: XX%
  AE count: N

Payout model:
  Attainment   Per-rep payout   Cost-to-company   vs. OTE
  50%          $XXXk            $XXXk              −XX%
  65%          $XXXk            $XXXk              −XX%
  75%          $XXXk            $XXXk              ±XX%   ← planning rate
  85%          $XXXk            $XXXk              +XX%
  100%         $XXXk            $XXXk              OTE
  120%         $XXXk            $XXXk              +XX%   ← accelerator zone

Unintended behavior flags:
  [Threshold cliff / Accelerator concentration / Underwater OTE — or NONE DETECTED]

[DRAFT — for RevOps, HR, and Finance review only]
[G3: Comp implications require HR + Finance dual review before any rep communication]
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

- G3: All comp simulation outputs carry: "Requires HR + Finance dual review before rep distribution." — comp implications require HR + Finance dual review; no exceptions
- G1: Revenue projections used as inputs qualify as range models, not commitments
- G2: Comp outputs are structural inputs; final comp decisions require leadership approval
- Unintended behavior flags are risk disclosures, not plan rejections
