---
name: quota-sensitivity-analysis
version: 1.0.0
description: "Builds quota models from UoG-confirmed AE headcount and revenue target. Models structural achievability at five attainment levels (50/65/75/85/100%). Flags when hitting plan requires attainment above the 75th percentile of historical actuals. Used inside annual-planning-workflow Phase 4 or standalone. Triggers: 'quota model', 'is quota achievable', 'quota sensitivity', 'quota attainment model', 'what does quota need to be'."
---

# Quota Sensitivity Analysis

Quota achievability modeling from UoG inputs. Flags structurally challenging
quotas — not as a rejection, but as a risk disclosure for leadership.

**Reference:** UoG formulas → `reference/revops-domain-model.md §5`
**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `ae_quota`, `ae_attainment_planning_rate`, `current_ae_count`

---

## Reasoning Protocol

1. Confirm activation — quota modeling requested
2. Read UoG-confirmed inputs from practice profile or `annual-planning-workflow` Phase 2
3. Apply G2 — output is structural input; quota decisions require leadership approval
4. Apply G3 — if output changes OTE/comp structure, HR + Finance dual review required
5. Apply G1 — revenue projections require forecast language qualification

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

## Output Format

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

## Guardrails

- G1, G2, G3 all apply
- Structural achievability flag is risk disclosure, not a quota rejection
