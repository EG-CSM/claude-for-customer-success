---
name: closed-won-to-cs-capacity-modeling
version: 1.0.0
description: "Converts rolling sales forecast into CS resource demand using UoG formulas. Runs three-scenario capacity check (P10/P50/P90 from scenario-modeling). Compares projected CSM demand to current headcount and UoG annual plan baseline. Surfaces CS capacity gaps with a hiring lead time flag. Updates when SA1 forecast moves >10%. Triggers: 'CS capacity', 'can CS absorb', 'CSM headcount needed', 'CS ceiling', 'will CS be able to handle new logos'."
---

# Closed-Won to CS Capacity Modeling

Translates what Sales is about to close into what CS needs to handle.
The skill that prevents hiring CSMs one quarter after you needed them.

**Reference:** UoG formulas (CS capacity) → `reference/revops-domain-model.md §5`
**Config reads:** `current_csm_count`, `arr_per_csm`, `avg_deal_acv`,
`csm_avg_ramp_days`, `uog_baseline_path`, `open_csm_requisitions`

---

## Reasoning Protocol

1. Confirm activation — user asking about CS capacity, CSM headcount, or CS ability to absorb growth
2. Read current CSM count and ARR per CSM from practice profile
3. Read P10/P50/P90 forecast from `scenario-modeling` output or ask for current pipeline
4. Read UoG baseline from `uog_baseline_path` for plan comparison
5. Apply G2 — capacity outputs are structural inputs, not hiring mandates
6. Confirm output destination — CS leadership vs. RevOps internal

---

## Three-Scenario Capacity Check `[revops-domain-model.md §5]`

```
For each scenario (P10 / P50 / P90):
  New_Customers     = Scenario_New_ARR ÷ avg_deal_acv  (if available)
  Total_Future_ARR  = current_arr + Scenario_New_ARR
  CSMs_Required     = CEILING(Total_Future_ARR ÷ arr_per_csm)
  CS_Gap            = CSMs_Required − current_csm_count
  Constraint_Signal = derived from CS Headroom % thresholds [domain-model §5]
```

**CS headroom signal thresholds** `[revops-domain-model.md §5]`:
- < 0% → CS already over capacity — churn risk live NOW
- 0–10% → Near ceiling — CS hiring is primary constraint
- 10–25% → Limited headroom — model next quarter before hiring AEs
- > 25% → Healthy headroom

**Plan comparison:**
If UoG baseline present: compare CSMs_Required to baseline `csm_required`.
Surfaces: are we ahead of, on, or behind the plan's CS hiring assumptions?

**Hiring lead time flag:**
```
If CS_Gap > 0:
  Hire_By = quarter_close_date − csm_avg_ramp_days
  If Hire_By < today:
    → "CS ramp period means any hire today won't be productive before Q[N] close."
```

---

## Output Format

```
CS CAPACITY MODELING — [Quarter/Period]
[Practice profile] [Confidence: High/Moderate]
[UoG baseline: present / absent]

Current state:
  CSMs in seat: [N]  Open reqs: [N]
  ARR per CSM target: $XXXk
  CS headroom today: XX%  ([Signal])

Three-scenario demand:
Scenario  New ARR    CSMs needed  CS gap  Headroom  Signal
P10       $XXXk      N            [+N/-N] XX%       [HEALTHY/AT-RISK/CRITICAL]
P50       $XXXk      N            [+N/-N] XX%       [signal]
P90       $XXXk      N            [+N/-N] XX%       [signal]

vs. annual plan baseline: [N CSMs planned → N required at P50 — on/ahead/behind plan]

Hiring lead time:
  At P50: hire [N] CSMs by [date] to be productive by [quarter close]
  Current ramp: [csm_avg_ramp_days] days

[DRAFT — RevOps and CS leadership]
[G2: Structural input. Hiring requires budget approval and HR process.]
```

---

## Guardrails

- G2: Always include the structural input qualifier
- G6: Data-as-of on all connector reads
- When baseline absent: declare before analysis; run in current-state mode only
