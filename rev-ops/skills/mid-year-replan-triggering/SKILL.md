---
name: mid-year-replan-triggering
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Monitors plan-vs-actual drift against the UoG baseline. Fires a replan recommendation when actuals diverge >15% from P50 plan, CS headroom crosses 10%, AE attainment runs >20pp below plan for 2+ months, or a material territory event occurs. Produces a replan recommendation memo with supporting data. Triggers: 'replan', 'plan vs actual drift', 'mid-year adjustment', 'are we off plan', 'should we replan'."
---

[PROPOSED]

# Mid-Year Replan Triggering

Monitors four drift signals against the annual plan baseline. Produces a replan
recommendation memo when a trigger fires — not a replan itself.

**Reference:** UoG formulas → `../../../shared/revops-domain-model.md §5`
**Config reads:** `uog_baseline_path`, `target_growth_pct`, `current_csm_count`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `uog_baseline_path`, `target_growth_pct`, `current_csm_count`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- Actuals have deviated materially from annual plan and replanning criteria need evaluation
- Mid-year variance triggers need to be assessed against configured thresholds
- Leadership needs structured recommendation on whether to initiate a replan

## Do NOT use for
- Annual planning execution (use annual-planning-workflow)
- Forecast variance analysis in isolation (use forecast-variance-analysis)
- Scenario modeling for a replan (use scenario-modeling after trigger fires)

## Typical Activation
"Should we replan?", "mid-year replan", "replan trigger assessment", "are we off plan enough to replan", "evaluate replan criteria"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of replan triggering request is this?
   - Single-trigger assessment (one dimension — evaluate whether one signal is firing)
   - Full four-trigger assessment (all dimensions — produce replan recommendation memo)
   - Reporting mode (UoG baseline absent — actuals only, no variance analysis)
   - Post-trigger routing (trigger has fired — recommend replan scope and urgency)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about plan drift or replan criteria
   2. Read UoG baseline from `uog_baseline_path` — if absent, run in reporting mode; label output accordingly
   3. Check HubSpot connector for actuals; declare fallback if unavailable
   4. Apply G1 — replan projections require forecast language qualification
   5. Apply G2 — headcount signals in replan are structural inputs, not hiring mandates
   6. Apply G6 — data-as-of on all connector reads
   7. Evaluate all four trigger dimensions before surfacing recommendation
   8. Replan recommendation requires at least one trigger firing — do not recommend replan without evidence

3. **EXPERT CHECK**: What would a veteran RevOps planning analyst verify first?
   - Is the UoG baseline confirmed present before running variance analysis? Comparing actuals
     to an absent baseline produces phantom variance — declare reporting mode explicitly.
   - Are all four trigger dimensions evaluated independently? A CS headroom breach and an ARR
     drift may require different replan scopes — conflating them obscures the recommendation.
   - Is G1 qualification applied to all year-end projections? "Projected year-end ARR without
     replan" is a model output, not a commitment — it must be labeled as such.
   - Is the replan recommendation tied to specific firing triggers, not general concern? A
     recommendation without evidence is noise — name which trigger(s) fired and the delta.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Running variance analysis without confirming UoG baseline is accessible (produces phantom variance)
   - Recommending a replan when no trigger has crossed threshold (produces false urgency)
   - Applying forward-looking year-end projections without G1 qualification
   - Surfacing connector reads without data-as-of timestamp (G6 violation)

**After execution**, verify:
- G1 qualification present on all year-end projections and forward-looking outputs
- G2 qualifier present if headcount signal appears in output
- G6 data-as-of label applied to all HubSpot and company profile reads
- Replan recommendation tied to named firing trigger(s) with supporting delta
- Confidence: High when HubSpot connected and baseline present; Moderate when data stale or baseline absent (reporting mode)
    - Confidence: [High] when HubSpot connected and baseline present / [Medium] when data stale or baseline absent (reporting mode) / [Low] if all inputs are manual or unverified

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

## Output

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

- G1, G2 apply to all forward-looking outputs
- When baseline absent: always declare before analysis; never fabricate a comparison
