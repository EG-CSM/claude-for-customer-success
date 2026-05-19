---
name: growth-model-vs-actuals-tracking
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Monitors unit economics of growth against the UoG annual plan baseline on three vectors: new logo/Sales-owned (CAC, time-to-first-value, ARR-at-12-months), expansion NRR/CS-owned (NRR by cohort vs. modeled), retention GRR/CS-owned (GRR vs. modeled). Vectors 2–3 are CS accountability signals routed to CS leadership. Fires a variance memo when any vector diverges >15% (NRR: >5pp, GRR: >3pp). Routes to mid-year-replan-triggering when threshold is crossed. Triggers: 'plan vs actual', 'growth model drift', 'are we on plan', 'unit economics', 'NRR vs plan', 'GRR vs plan', 'expansion attainment'."
---

[PROPOSED]

# Growth Model vs Actuals Tracking

Unit economics of growth — measured against the plan, not reported in isolation.
The skill that turns "here are the numbers" into "here's what's drifting and why."

**Reference:** UoG formulas → `../../../shared/revops-domain-model.md §5`
**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `uog_baseline_path`, `nrr_current`, `cs_platform_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `uog_baseline_path`, `nrr_current`, `cs_platform_connected`

---

## Use when
- Actual growth metrics need to be compared against the committed growth model
- Period-over-period tracking of growth model attainment is required — covers all three revenue vectors (Sales new logo, CS expansion, CS retention)
- Deviation from growth model needs to be surfaced with signal clarity
- CS leadership needs to see expansion NRR or retention GRR accountability signal against plan

## Do NOT use for
- Forward scenario modeling (use scenario-modeling)
- Forecast variance root cause (use forecast-variance-analysis)
- Annual plan replanning trigger (use mid-year-replan-triggering)

## Typical Activation
"Growth model vs actuals", "how are we tracking against the model", "growth model attainment", "actuals vs growth plan for [period]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of growth model tracking request is this?
   - Single-vector report (one of: new logo, expansion NRR, or retention GRR vs. plan)
   - Full-model summary (all three vectors — cross-vector attainment snapshot)
   - Variance memo trigger (threshold crossed on one or more vectors — memo generation + replan routing)
   - Reporting mode (UoG baseline absent — actuals only, no variance analysis)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about plan vs. actual, unit economics, or NRR/GRR trend
   2. Read UoG baseline from `uog_baseline_path` — if absent, run in reporting mode only; label output accordingly
   3. Check CS platform connector for NRR/GRR actuals; check HubSpot for new logo actuals; declare fallback if unavailable
   4. Apply G1 — variance projections require forecast language qualification
   5. Apply G6 — data-as-of on all reads
   6. Confirm accountability routing: Vectors 2–3 are CS-owned signals → route to CS leadership, not Sales

3. **EXPERT CHECK**: What would a veteran RevOps growth analyst verify first?
   - Is the UoG baseline confirmed present before running variance analysis? Comparing actuals
     to an absent or stale baseline produces phantom variance — declare reporting mode and label
     explicitly before surfacing any number.
   - Are Vectors 2 and 3 routed to CS leadership, not Sales? Expansion NRR and GRR are CS
     accountability signals — misrouting to Sales creates conflicting ownership and delays response.
   - Is the variance threshold correctly applied per vector? >15% for new logo ARR, >5pp for NRR,
     >3pp for GRR — applying a single threshold across vectors misses GRR signals and
     over-triggers on normal NRR fluctuation.
   - Is the replan trigger evaluated and declared? A crossed threshold requires an explicit
     routing decision to mid-year-replan-triggering — not implicit in the variance memo.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Running variance analysis without confirming UoG baseline path is accessible (produces phantom variance)
   - Routing CS-owned vectors (Expansion NRR, Retention GRR) to Sales leadership instead of CS leadership
   - Applying forward-looking year-end projections without G1 qualification
   - Surfacing CS platform or HubSpot reads without data-as-of timestamp (G6 violation)

**After execution**, verify:
- G1 qualification present on all year-end projections derived from variance analysis
- G6 data-as-of label applied to all CRM and CS platform reads
- CS-owned vector accountability correctly routed to CS leadership + RevOps
- Confidence: High when both CRM and CS platform are connected and baseline is present; Moderate when data is stale or baseline is absent (reporting mode)
    - Confidence: [High] when both CRM and CS platform are connected and baseline is present / [Medium] when data is stale or baseline is absent (reporting mode) / [Low] if all inputs are manual or unverified

---

## Three Growth Vectors

**Vector 1 — New logo** _(Sales-owned)_
```
Baseline fields: new_arr_target, ae_required (from UoG output)
Actuals: closed_won_ytd [CRM ✓ live]
Variance threshold: >15% behind or ahead of pro-rata plan
Accountability: Sales leadership
```

**Vector 2 — Expansion** _(CS-owned)_
```
Baseline fields: nrr assumption (from UoG inputs)
Actuals: current NRR by cohort [CS Platform ✓ live]
Variance threshold: >5 NRR points
Accountability: CS leadership — expansion NRR is a CS accountability signal,
not a RevOps-owned metric. CS leaders carry expansion attainment the same
way Sales leaders carry new logo attainment.
```

**Vector 3 — Retention** _(CS-owned)_
```
Baseline fields: GRR assumption (from UoG inputs if provided)
Actuals: current GRR [CS Platform ✓ live]
Variance threshold: >3 GRR points
Accountability: CS leadership — GRR is a CS accountability signal. A GRR
variance memo routes to CS leadership and RevOps jointly.
```

**When baseline absent:**
```
Run in reporting mode: surface actuals only, no variance analysis.
Label: [Variance analysis unavailable — UoG baseline not configured.
Reporting actuals only — Confidence: Low]
```

---

## Variance Memo (fires when threshold crossed)

```
Variance memo for [vector]:
  What diverged: [Vector] — actual [X] vs. plan [Y] (delta: [Z], threshold: [T])
  Impact: At this rate, year-end ARR = $XXXk vs. $XXXk plan (−$XXXk)
  Most likely factor: [Named evidence — not speculation]
    Source: [CRM ✓ live / CS Platform ✓ live / Inferred]
  Accountability routing:
    Vector 1 (New logo) → Sales leadership + RevOps
    Vector 2 (Expansion NRR) → CS leadership + RevOps
    Vector 3 (Retention GRR) → CS leadership + RevOps
  Replan trigger: [Yes — route to mid-year-replan-triggering / No]
```

---

## Output

```
GROWTH MODEL VS ACTUALS — [Period]
[CRM ✓ live — as of YYYY-MM-DD] [CS Platform: ✓ live / Unavailable]
[UoG baseline: present [path] / absent — reporting mode only]
[Confidence: High/Moderate/Low]

Vector                        Owner   Plan      Actual    Delta    Signal
New logo ARR                  Sales   $XXXk     $XXXk     −XX%     [ON PLAN / ⚠ DRIFTING]
Expansion NRR (CS-owned)      CS      XXX%      XXX%      −Xpp     [ON PLAN / ⚠ DRIFTING]
Retention GRR (CS-owned)      CS      XXX%      XXX%      −Xpp     [ON PLAN / ⚠ DRIFTING]

[Variance memo if threshold crossed]

[DRAFT — RevOps and CS leadership]
[G1: Projections are models. Not revenue commitments.]
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

- G1: All forward-looking variance projections require qualification
- G6: Data-as-of required on all reads
- When baseline absent: declare explicitly before any number is shown
