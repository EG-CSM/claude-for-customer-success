---
name: closed-won-to-cs-capacity-modeling
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Converts rolling sales forecast into CS resource demand using UoG formulas. Runs three-scenario capacity check (P10/P50/P90 from scenario-modeling). Compares projected CSM demand to current headcount and UoG annual plan baseline. Surfaces CS capacity gaps with a hiring lead time flag. Updates when SA1 forecast moves >10%. Triggers: 'CS capacity', 'can CS absorb', 'CSM headcount needed', 'CS ceiling', 'will CS be able to handle new logos'."
---

[PROPOSED]

# Closed-Won to CS Capacity Modeling

Translates what Sales is about to close into what CS needs to handle.
The skill that prevents hiring CSMs one quarter after you needed them.

**Reference:** UoG formulas (CS capacity) → `../../../shared/revops-domain-model.md §5`
**Config reads:** `current_csm_count`, `arr_per_csm`, `avg_deal_acv`,
`csm_avg_ramp_days`, `uog_baseline_path`, `open_csm_requisitions`

---

## Use when
- CS team capacity needs to be assessed against incoming closed-won volume
- Onboarding capacity planning requires modeling against pipeline close projections
- CS hiring or resource decisions need to be tied to revenue intake rate

## Do NOT use for
- Individual CS assignment decisions (use handoff workflow)
- CS performance assessment
- Pipeline coverage analysis from a Sales perspective (use pipeline-coverage-analysis)

## Typical Activation
"CS capacity model", "can CS absorb this pipeline", "capacity planning for CS", "closed-won to onboarding capacity", "do we have enough CS capacity"

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `current_csm_count`, `arr_per_csm`, `avg_deal_acv`, `csm_avg_ramp_days`, `uog_baseline_path`, `open_csm_requisitions`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of CS capacity request is this?
   - Current-state headroom check (no forecast context)
   - Three-scenario demand modeling (P10/P50/P90)
   - Plan comparison (vs. UoG annual baseline)
   - Hiring lead time assessment

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about CS capacity, CSM headcount, or CS ability to absorb growth
   2. Read current CSM count and ARR per CSM from company profile
   3. Read P10/P50/P90 forecast from `scenario-modeling` output or ask for current pipeline
   4. Read UoG baseline from `uog_baseline_path` for plan comparison
   5. Apply G2 — capacity outputs are structural inputs, not hiring mandates
   6. Confirm output destination — CS leadership vs. RevOps internal

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Is the UoG baseline present? If absent, declare and run in current-state mode only.
   - Is the ARR-per-CSM target current? Stale targets produce misleading headroom signals.
   - Is hiring lead time factored in? A gap identified today may already be too late for the quarter.
   - Is the CS constraint signal checked before any AE growth discussion? CS ceiling can invalidate an AE plan.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting capacity outputs as hiring mandates (G2 violation)
   - Running plan comparison without checking whether the baseline path is configured
   - Omitting the hiring lead time flag when CS_Gap > 0
   - Ignoring the CS headroom signal when advising on AE headcount growth

**After execution**, verify:
- G2 structural input qualifier present on all capacity outputs
- Data-as-of label applied per G6
- Hiring lead time flag included when CS_Gap > 0
- Confidence: High when baseline is present and all config fields are populated; Moderate when baseline is absent or any field is estimated
- Confidence: [High] when baseline is present and all config fields populated / [Medium] when baseline is absent or any field is estimated / [Low] if all inputs are manual or unverified

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

## Output

```
CS CAPACITY MODELING — [Quarter/Period]
[Company profile] [Confidence: High/Moderate]
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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

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

- G2: Always include the structural input qualifier
- G6: Data-as-of on all connector reads
- When baseline absent: declare before analysis; run in current-state mode only
