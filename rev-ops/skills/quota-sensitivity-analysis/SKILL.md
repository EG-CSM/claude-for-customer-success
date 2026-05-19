---
name: quota-sensitivity-analysis
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Builds quota models from UoG-confirmed AE headcount and revenue target. Models structural achievability at five attainment levels (50/65/75/85/100%). Flags when hitting plan requires attainment above the 75th percentile of historical actuals. Used inside annual-planning-workflow Phase 4 or standalone. Triggers: 'quota model', 'is quota achievable', 'quota sensitivity', 'quota attainment model', 'what does quota need to be'."
---

[PROPOSED]

# Quota Sensitivity Analysis

Quota achievability modeling from UoG inputs. Flags structurally challenging
quotas — not as a rejection, but as a risk disclosure for leadership.

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `ae_quota`, `ae_attainment_planning_rate`, `current_ae_count`

---

## Use when
- User needs to understand how quota attainment changes under different input assumptions
- Sensitivity testing of quota model before annual plan is finalized
- Rep or segment quota review requires range analysis rather than point estimate

## Do NOT use for
- Full annual planning orchestration (use annual-planning-workflow)
- Comp plan modeling (use comp-simulation)

## Typical activation
"How sensitive is quota to win rate?", "quota sensitivity analysis", "what happens to attainment if ACV drops 10%", "sensitivity test the plan"

**Reference:** UoG formulas → `../../../shared/revops-domain-model.md §5`
**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `ae_quota`, `ae_attainment_planning_rate`, `current_ae_count`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of quota sensitivity request is this?
   - Per-rep quota derivation (AEs required + target → implied quota)
   - Attainment scenario table (five-level structural achievability model)
   - Structural achievability flag (plan requires above-75th-percentile performance?)
   - Integrated quota review (all three — full sensitivity analysis output)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about quota modeling, achievability, or attainment scenarios
   2. Read UoG-confirmed inputs from practice profile or `annual-planning-workflow` Phase 2 output
   3. Apply G2 — quota model output is a structural input; quota decisions require leadership approval before finalization
   4. Apply G3 — if quota model output changes OTE or comp structure, HR + Finance dual review required
   5. Apply G1 — revenue projections in scenario table require forecast language qualification
   6. Confirm all three inputs confirmed before running: `ae_required`, `new_arr_target`, `ae_quota`
   7. If any input is estimated rather than UoG-confirmed, label it `[Estimated]` and apply Moderate confidence

3. **EXPERT CHECK**: What would a veteran RevOps quota analyst verify first?
   - Are the AE count and ARR target from the same UoG scenario? Mixing scenario inputs produces
     a structurally invalid quota model — confirm they reference the same selected scenario.
   - Is the planning rate (75%) declared as an assumption, not a universal benchmark? The 75th
     percentile is the KBCM actuals context — it must be surfaced explicitly, not implied.
   - Does the structural achievability flag surface evidence, not just a conclusion? "Requires
     top-quartile performance" without naming the KBCM actuals median (55–65%) is unactionable
     for leadership.
   - Is G3 evaluated — not just noted? If per-rep quota derived here differs from the practice
     profile `ae_quota`, this is a comp structure change requiring HR + Finance dual review.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Using unconfirmed or estimated AE count without labeling it (produces phantom precision in the quota model)
   - Applying the structural achievability flag without declaring the KBCM actuals benchmark
   - Presenting quota as a final decision rather than a structural input requiring leadership approval (G2 violation)
   - Applying G1 qualification only to the top-line projection but not to individual attainment scenario lines

**After execution**, verify:
- G1 qualification present on all revenue projection lines in attainment scenario table
- G2 qualifier present — quota decisions require leadership approval
- G3 evaluated — if derived quota differs from profile `ae_quota`, dual review flag surfaced
- All inputs labeled as `[UoG confirmed]` or `[Estimated]` as appropriate
- Confidence: High when all inputs are UoG-confirmed from Phase 2; Moderate when any input is estimated or practice profile only

---

## Workflow

```
From UoG (practice profile or Phase 2 output):
  ae_required      = confirmed from selected scenario
  new_arr_target   = confirmed from selected scenario
  ae_quota         = from practice profile

Per-rep quota = new_arr_target ÷ ae_required

Attainment scenario table:
  At 50%:  Revenue = ae_required × ae_quota × 0.50
  At 65%:  Revenue = ae_required × ae_quota × 0.65
  At 75%:  Revenue = ae_required × ae_quota × 0.75  ← planning rate
  At 85%:  Revenue = ae_required × ae_quota × 0.85
  At 100%: Revenue = ae_required × ae_quota × 1.00

Structural achievability flag:
  If hitting plan requires attainment > 75th percentile of trailing actuals:
  → Flag as [Structurally Challenging] with evidence
  KBCM actuals median: 55–65%. Planning rate: 75%.
```

---

## Output

```
QUOTA SENSITIVITY ANALYSIS [DRAFT]
[Practice profile] [Confidence: High if UoG confirmed / Moderate if estimated]

Confirmed inputs:
  AEs required (selected scenario): N
  New ARR target: $XXXk
  Per-rep quota:  $XXXk

Attainment scenario:
  Attainment   ARR outcome    vs. Plan
  50%          $XXXk          −XX%
  65%          $XXXk          −XX%
  75%          $XXXk          ±XX%  ← planning rate
  85%          $XXXk          +XX%
  100%         $XXXk          +XX%

Structural achievability: [Achievable / Structurally Challenging]
  [If challenging]: Hitting plan requires XX% attainment.
  KBCM actuals median is 55–65%. This quota requires top-quartile performance.
  Risk disclosure: share with leadership before finalizing.

[DRAFT — for RevOps and Finance review]
[G2: Structural input — quota decisions require leadership approval]
[G1: Revenue projections are range models, not commitments]
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

- G1, G2, G3 all apply
- Structural achievability flag is risk disclosure, not a quota rejection
