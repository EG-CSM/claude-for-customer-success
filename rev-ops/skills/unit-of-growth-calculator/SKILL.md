---
name: unit-of-growth-calculator
version: 1.0.0
description: "Unit of Growth Calculator -- compute GTM headcount requirements, capacity imbalances, and efficiency diagnostics for B2B SaaS organizations using the AE-anchored or CSM-anchored pod model. Use during revenue planning, board preparation, CRO/CFO reviews, or CS capacity modeling to surface under/over-capacity signals across AE, SDR, CSM, and Support functions with specific remediation guidance. Synthesizes the SuccessCOACHING Unit of Growth research model with 2025 SaaS benchmarks."
deployment_target: plugin
status: PROPOSED
---

[PROPOSED]

# Unit of Growth Calculator

## Overview

Computes GTM headcount requirements and surfaces capacity imbalance signals for B2B SaaS
organizations. Works from either direction: start from revenue targets to derive required
headcount, or start from existing headcount to compute maximum supportable growth and surface
structural constraints.

The model anchors on the AE as the unit of growth and derives SDR, CSM, and Support headcount
from a small set of ratios and benchmarks. It also runs the reverse — starting from CS capacity
to find the maximum ARR growth the post-sales org can absorb before breaking.

## Use when
- Preparing for board, CFO, or CRO headcount planning reviews
- Modeling GTM pod requirements for a revenue target
- Detecting whether CS can absorb the accounts Sales is closing (or will close)
- Diagnosing why quota is being missed despite sufficient headcount
- Checking whether lead volume justifies the current SDR or AE count
- Computing closed-won-to-CS-capacity constraints
- Running a pipeline coverage sanity check against win rate

## Do NOT use for
- Individual rep performance review (this is a structural capacity tool, not a rep coaching tool)
- Pricing or packaging analysis
- Customer health scoring or churn prediction on specific accounts
- Detailed financial modeling with COGS, EBITDA, or equity dilution — route to a CFO model

## Typical Activation
"Model my GTM headcount for a $5M ARR target", "Do I have enough CSMs to support my current AE team?", "How much ARR can my current CS team support?", "Is my pipeline coverage ratio healthy?", "Run the unit of growth calculation for my company", "Show me where my GTM org is over or under capacity"

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `primary_segment`, `crm_system`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of unit of growth calculation is this?
   - AE-anchored calculation (revenue target → derived GTM headcount requirements)
   - CS-anchored reverse (existing CSM headcount → maximum supportable ARR ceiling)
   - Scenario comparison (multi-scenario modeling across segments, growth rates, or headcount assumptions)
   - Imbalance diagnostic only (user has headcount and revenue data and wants signals without running a full model)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting headcount planning, capacity analysis, or GTM structure review
   2. Pull company profile from config; declare segment, CRM system, and any stored benchmark overrides
   3. Apply benchmark source discipline — all defaults traced to `references/benchmark-library.md`; no training-memory benchmarks
   4. Apply G5 — all headcount outputs are analytical inputs for planning review; no output is an approved headcount plan
   5. Flag when user-provided inputs deviate significantly from benchmarks — note the deviation, never override the user's number
   6. Confirm `primary_segment` from config before applying segment-specific benchmark defaults
   7. Confirm output destination before delivering — board deck vs. CFO/CRO planning session vs. internal RevOps analysis

3. **EXPERT CHECK**: What would a veteran RevOps capacity planner verify before surfacing findings?
   - Is the pipeline coverage calculation win-rate-anchored rather than a static 3x rule? Required coverage = 1 ÷ win rate — presenting 3x as universal without checking win rate is a common planning error that can understate or overstate pipeline need by 30–50%.
   - Is the CS hiring timing sequenced correctly? CS must be hired in advance of AE-driven growth, not in arrears — a model that shows CS and AE scaling in lockstep understates the CS hiring lead time required to avoid churn spikes.
   - Is the segment boundary applied to benchmarks? SMB, mid-market, and enterprise benchmarks diverge significantly on AE quota, CSM portfolio size, and attainment rates — applying a blended benchmark to a segment-specific question produces misleading signals.
   - Is the NRR effect on new ARR requirements declared? High NRR reduces the new ARR burden on Sales; low NRR increases it. A model that omits NRR as an input variable will overstate or understate AE headcount need for the same net growth target.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Applying SMB benchmarks to enterprise accounts or vice versa without flagging the mismatch
   - Using 3x pipeline coverage without checking win rate first (produces incorrect coverage targets)
   - Presenting headcount outputs as exact counts rather than ranges (benchmarks are ranges, not point estimates)
   - Skipping the CS capacity reverse check when current CSM count is available — it must always run
   - Omitting NRR from the new ARR requirement calculation when the user provides it

**After execution**, verify:
- G5 qualifier present — all headcount outputs labeled as planning proposals, not approved decisions
- Benchmark sources cited per `references/benchmark-library.md` — no training-memory benchmarks presented as defaults
- CS capacity check run in both directions (forward and reverse) when CSM headcount is available
- Segment-appropriate benchmarks applied per `primary_segment` config
- Confidence: High for formula calculations; Moderate for GTM headcount benchmarks (sourced from industry synthesis, shifting with AI-assisted CS tooling)
    - Confidence: [High] for formula calculations / [Medium] for GTM headcount benchmarks (sourced from industry synthesis, shifting with AI-assisted CS tooling) / [Low] if all inputs are manual or unverified

---

## Specification

| Attribute | Value |
|-----------|-------|
| Calculation Modes | AE-anchored (revenue → headcount) / CS-anchored (headcount → max ARR) |
| Imbalance Signals | 5 categories: Sales over-capacity, CS under-capacity, CS over-capacity, Sales under-capacity, Lead volume insufficient |
| Benchmark Source | KBCM Technology Group & Sapphire Ventures Annual Private SaaS Survey (13th–16th editions, 2022–2025, ~390 respondent-years) + supporting sources. Full tables with source attribution: `references/benchmark-library.md` |
| Formula Source | All formulas, metric definitions, and term glossary: `references/metrics-and-glossary.md` |
| Output Format | Structured calculation table + imbalance diagnostic + remediation actions |
| Interaction Mode | Intake → Calculate → Diagnose → Recommend |
| Complexity | T2 — Professional |

---

## Input Schema

```
core_inputs:
  current_arr: float                    # Current ARR in dollars
  target_growth_pct: float              # YoY growth target (e.g., 0.45 = 45%)
  nrr: float | None                     # Net Revenue Retention (e.g., 1.10 = 110%); optional
  segment: str                          # SMB | Low Mid-Market | Mid-Market | Enterprise | Strategic
  motion: str                           # Outbound-Heavy | Mixed | Inbound-Dominant | PLG

ae_inputs:
  ae_quota: float                       # Annual new ARR quota per fully-ramped AE
  ae_attainment: float                  # Expected attainment rate (e.g., 0.75 = 75%)
  current_ae_count: int | None          # Existing AEs; if None, derive from targets

sdr_inputs:
  sdr_ae_ratio: str | None              # e.g., "1:2" (1 SDR per 2 AEs); if None, use benchmark
  current_sdr_count: int | None         # Existing SDRs; if None, derive from AE count

csm_inputs:
  csm_model: str                        # "ARR-based" | "Account-based"
  arr_per_csm: float | None             # Target ARR per CSM (if ARR-based)
  accounts_per_csm: int | None          # Target accounts per CSM (if account-based)
  current_csm_count: int | None         # Existing CSMs
  current_customer_count: int | None    # Total current customers/accounts
  touch_model: str                      # "High-Touch" | "Tech-Touch" | "Pooled/Scaled"

optional_inputs:
  avg_deal_acv: float | None            # Average new deal ACV (for pipeline modeling)
  win_rate: float | None                # Win rate on qualified opportunities (e.g., 0.25)
  current_pipeline_value: float | None  # Current pipeline value (for coverage check)
  sales_cycle_months: int | None        # Average months to close
  tickets_per_customer_month: float | None  # For support sizing
  tickets_per_support_fte_month: int | None # For support sizing
  gross_margin_pct: float | None        # For CAC payback and LTV calculations
  sm_spend_last_period: float | None    # Sales & Marketing spend (for magic number)
  net_new_arr_last_period: float | None # For magic number calculation
```

---

## Output Schema

```
calculation_result:
  inputs_confirmed: dict               # Echo of confirmed inputs with segment/benchmark defaults applied
  revenue_model:
    new_arr_target: float
    target_arr: float
    nrr_adjustment: str
  headcount_model:
    ae_required: float
    ae_effective_capacity: float
    sdr_required: float
    csm_required: float
    support_fte_required: float | None
  cs_capacity_check:
    max_supported_arr: float
    max_incremental_arr: float
    cs_headroom_pct: float
    max_ae_cs_can_support: float
    constraint_signal: str            # "CS is the binding constraint" | "CS has headroom" | "CS over-capacity"
  pipeline_check:
    required_coverage: float | None
    current_coverage: float | None
    pipeline_gap: float | None
    lead_sufficiency_signal: str | None
  imbalance_signals: list[ImbalanceSignal]
  remediation_actions: list[str]
  efficiency_metrics: dict | None     # Magic number, CAC payback, LTV:CAC if inputs provided
```

---

## Core Workflow

### STEP 1 — Intake

When the user invokes the skill, collect the minimum required inputs. If any are missing, ask
for them one at a time in this priority order.

**Term definition lookups:** If the user asks "what does X mean?" or "how is X calculated?"
at any point — during intake or mid-calculation — look up the term in
`references/metrics-and-glossary.md`:
- Section 3 (Glossary) for the plain-language definition
- Section 1 (Metrics Catalog) for the full formula, inputs, units, and interpretation
Answer from those definitions. Do not paraphrase from training memory.

**Tier 1 (required for any calculation):**
1. Current ARR
2. Target growth % (or specific New ARR target)
3. Customer segment (SMB / Mid-Market / Enterprise / Strategic)
4. Sales motion (Outbound-Heavy / Mixed / Inbound-Dominant / PLG)

**Tier 2 (required for headcount model):**
5. AE quota and attainment (offer benchmark defaults if not provided — see below)
6. CSM model preference: ARR-based or account-based
7. ARR per CSM or accounts per CSM target (offer benchmark defaults)

**Tier 3 (enriches imbalance diagnostics — ask after Tier 1-2):**
8. Current AE, SDR, CSM counts (if modeling against existing org)
9. Win rate and current pipeline value (for pipeline coverage check)
10. Average deal ACV and sales cycle length (for lead sufficiency modeling)

**Benchmark defaults to offer when user doesn't have a number:**
All defaults are sourced from `references/benchmark-library.md` Section 6 (GTM Headcount
Benchmarks). Offer the midpoint. Confidence tiers are noted per row — state them when the
user asks about the source.

| Input | Default Offer | Confidence | BL Section |
|-------|--------------|------------|------------|
| AE Quota — Mid-Market | $800K ("typical for mid-market; adjust up for higher ACV") | [Synthesized] | BL §6 |
| AE Quota — Enterprise | $1.2M | [Synthesized] | BL §6 |
| AE Attainment | 75% ("planning rate; KBCM actuals median 55–65%") | [Verified] | BL §6 |
| ARR per CSM — Mid-Market High-Touch | $2M–$3.5M | [Synthesized] | BL §6 |
| ARR per CSM — Enterprise High-Touch | $3M–$5M | [Synthesized] | BL §6 |
| SDR:AE — Mixed motion | 1:2 | [Synthesized] | BL §6 |
| Win Rate | 25% ("typical B2B SaaS; verify against your CRM actuals") | [Heuristic] | BL §9 |
| Pipeline Coverage | 4x ("= 1 ÷ 25% win rate — derive from win rate, not a universal 3x rule") | [Heuristic] | BL §9 |

State any defaults applied explicitly: "I'm using a 75% attainment rate as the planning
default (sourced from `references/benchmark-library.md` §6; KBCM median actuals are
55–65%) — let me know if you want to change this."

---

### STEP 2 — AE-Anchored Calculation (Revenue → Headcount)

All formulas below are fully defined with inputs, units, and interpretation examples in
`references/metrics-and-glossary.md` Section 2 (Formula Reference, Phase 1–2). Metric
definitions are in Section 1 (Metrics Catalog).

**2a. Revenue Model**
```
If NRR provided:
  Target ARR     = Current ARR × (1 + Target Growth %)
  New ARR Target = Target ARR − (Current ARR × NRR)
Else:
  New ARR Target = Current ARR × Target Growth %

NRR > 1 reduces the new ARR required from Sales (existing customers expand).
NRR < 1 increases it (churn must be offset before net growth begins).
NRR = 1.0 → no adjustment.
```
See: M&G §1 — "New ARR Target" metric entry for the full NRR conditional logic and examples.

**2b. AE Headcount**
```
Effective AE Capacity = AE Quota × AE Attainment Rate
AEs Required          = CEILING(New ARR Target ÷ Effective AE Capacity)
```
Benchmarks: AE Quota and Attainment by segment in `references/benchmark-library.md` §6.
See: M&G §1 — "Effective AE Capacity" and "AEs Required" metric entries.

**2c. SDR Headcount**
```
SDRs Required = CEILING(AEs Required × SDRs per AE)
             or CEILING(AEs Required ÷ AEs per SDR)
```
Benchmark defaults by motion: `references/benchmark-library.md` §6 — SDR:AE Ratio table.

**2d. CSM Headcount (forward from AE output)**
```
ARR-based:
  Total Managed ARR = Current ARR + New ARR Target
  CSMs Required     = CEILING(Total Managed ARR ÷ ARR per CSM)

Account-based:
  New Customers ≈ New ARR Target ÷ Average Deal ACV  (if ACV provided)
  Total Accounts    = Current Customer Count + New Customers
  CSMs Required     = CEILING(Total Accounts ÷ Accounts per CSM)
```
Benchmark defaults by segment and touch model: `references/benchmark-library.md` §6.
See: M&G §1 — "CSMs Required" metric entry.

**2e. Support Headcount (if ticket data provided)**
```
Monthly Ticket Load = (Current Customers + New Customers) × Tickets per Customer per Month
Support FTE         = CEILING(Monthly Ticket Load ÷ Tickets per Support FTE per Month)
```
See: M&G §1 — "Support FTE Required" metric entry.

---

### STEP 3 — CS-Anchored Calculation (Headcount → Max ARR)

Run this when the user provides current CSM count and wants to know the CS capacity ceiling.
Full formula sequence with metric definitions in `references/metrics-and-glossary.md`
Section 2, Phase 3 (CS-Anchored Reverse).

```
Max Supported ARR   = Current CSM Count × ARR per CSM (benchmark or user-provided)
Max Incremental ARR = Max Supported ARR − Current ARR
CS Headroom %       = (Max Supported ARR − Current ARR) ÷ Current ARR × 100
Max AEs CS Can Support = Max Incremental ARR ÷ Effective AE Capacity
```

ARR per CSM benchmarks by segment and touch model: `references/benchmark-library.md` §6.
Metric interpretations (Max Supported ARR, Max Incremental ARR, CS Headroom %, Max AEs CS
Can Support): `references/metrics-and-glossary.md` §1.

If Max AEs CS Can Support < AEs Required (from Step 2):
→ CS is the binding constraint. Flag as primary imbalance signal.

If Max AEs CS Can Support > AEs Required:
→ CS has headroom. Note how many additional AEs can be added before hitting the CS ceiling.

---

### STEP 4 — Pipeline Coverage Check

Run if win rate and/or current pipeline value are provided. Run if ACV and sales cycle are
provided (derive pipeline target from AE headcount). Full formula sequence in
`references/metrics-and-glossary.md` Section 2, Phase 4 (Pipeline Coverage Check).

```
Required Coverage Ratio = 1 ÷ Win Rate
  (NOT a universal 3x — always derive from win rate; see M&G §1 "Required Coverage Ratio")

Pipeline Target    = New ARR Target × Required Coverage Ratio
Pipeline Gap       = Pipeline Target − Current Pipeline Value
  (negative = shortfall; positive = surplus)

Lead Volume Required = Pipeline Target ÷ Average Deal ACV
  (# of qualified opportunities needed to fill the pipeline)
```

Coverage signal thresholds (full table with rationale in `references/benchmark-library.md` §9):

| Current Coverage | Signal | Action |
|-----------------|--------|--------|
| Below 2x | CRITICAL | Pipeline is structurally insufficient; AE count is secondary problem |
| 2x–3x | AT-RISK | Thin buffer; model slippage scenarios |
| 3x–5x | HEALTHY | Standard range |
| Above 5x | INSPECT | Check opportunity quality; high volume may mask low-quality pipeline |

---

### STEP 5 — Imbalance Diagnostic

After calculating, run all five imbalance checks. Surface every signal that fires, ranked by
severity. Full signal threshold tables with evidence basis in
`references/benchmark-library.md` §9 (Imbalance Signal Thresholds). Full formula logic in
`references/metrics-and-glossary.md` Section 2, Phase 6.

**Check 1 — CS Under-Capacity (Too Few CSMs for AE Output)**

Benchmark thresholds from `references/benchmark-library.md` §6 (CSM Portfolio) and §9.

Fire if any of:
- ARR per CSM (implied by current counts) > High benchmark for segment (`BL §6`)
- AE:CSM Ratio > 2x the benchmark for the stated motion (`BL §6 — AE:CSM Ratio table`)
- CSMs Required (Step 2) > Current CSM Count by more than 1 FTE
- CS Headroom % < 10% (CS is nearly at ceiling)

Signal label: `CS_UNDER_CAPACITY`
Severity: HIGH when AE:CSM ratio exceeds 3x benchmark; MEDIUM otherwise

**Check 2 — CS Over-Capacity (Too Many CSMs for Current ARR)**

Fire if any of:
- ARR per CSM (implied by current counts) < Low benchmark for segment by >25% (`BL §6`)
- CS Budget % of ARR > 12% (if spend data provided; `BL §7 — CS Budget as % ARR`)
- AE:CSM Ratio < 0.5x the benchmark (`BL §6`)

Signal label: `CS_OVER_CAPACITY`
Severity: MEDIUM (inefficiency, not churn risk)

**Check 3 — Sales Over-Capacity (Too Many AEs for Lead/Pipeline Volume)**

Fire if any of:
- Pipeline Coverage < 3x (when win rate implies ≥3x needed; `BL §9`)
- AE Count > Max AEs CS Can Support (CS is the hard ceiling; Step 3 output)
- AE Quota Attainment stated as <55% for 2+ quarters (KBCM actual median: `BL §6`)

Signal label: `SALES_OVER_CAPACITY`
Severity: HIGH when pipeline coverage below 2x; MEDIUM when 2x–3x

**Check 4 — Sales Under-Capacity (Too Few AEs for Target)**

Fire if any of:
- AEs Required > Current AE Count + 1
- New ARR Capacity (from current AEs) < New ARR Target × 85%
- Pipeline Coverage >5x with stated high deal quality (demand exceeds closing capacity)

Signal label: `SALES_UNDER_CAPACITY`
Severity: HIGH when capacity gap >20% of target; MEDIUM otherwise

**Check 5 — Lead Volume Insufficient for SDR/AE Count**

Fire if SDR or pipeline data indicates:
- Pipeline per SDR × SDR Count < Pipeline Target
- MQL volume (if provided) < Required Opportunities ÷ MQL→Opportunity conversion rate
- Coverage ratio below required AND SDR count is at or above benchmark (`BL §6 — SDR:AE`)

Signal label: `LEAD_VOLUME_INSUFFICIENT`
Severity: HIGH when pipeline coverage below 2x due to lead volume

---

### STEP 6 — Present Results

Present the full output in this structure:

```
═══════════════════════════════════════════════════════
UNIT OF GROWTH ANALYSIS — [Company / Segment]
═══════════════════════════════════════════════════════

INPUTS CONFIRMED
  Current ARR:          $[X]
  Target Growth:        [X]% → New ARR Target: $[X]
  NRR Adjustment:       [X]% → [effect on new ARR target]
  Segment:              [segment]
  Motion:               [motion]
  AE Quota:             $[X] at [X]% attainment → $[X] effective capacity
  CSM Model:            [ARR-based / Account-based] at $[X]/CSM or [X] accounts/CSM
  [any defaults applied — stated explicitly]

───────────────────────────────────────────────────────
HEADCOUNT MODEL
  AE Required:          [X] AEs        (currently: [X] | gap: [+/-X])
  SDR Required:         [X] SDRs       (currently: [X] | gap: [+/-X])
  CSM Required:         [X] CSMs       (currently: [X] | gap: [+/-X])
  Support FTE:          [X] FTE        (if modeled)

───────────────────────────────────────────────────────
CS CAPACITY CHECK
  Current CSMs:         [X] CSMs
  Max Supported ARR:    $[X]     (at $[X]/CSM benchmark)
  Max Incremental ARR:  $[X]     ([X]% headroom above current ARR)
  Max AEs CS Supports:  [X] AEs
  
  Signal: [CS is the binding constraint | CS has headroom for X more AEs | CS over-capacity]

───────────────────────────────────────────────────────
PIPELINE COVERAGE CHECK   [if data available]
  Win Rate:             [X]%
  Required Coverage:    [X]x   (= 1 ÷ win rate)
  Current Pipeline:     $[X]   → [X]x coverage
  Coverage Signal:      [CRITICAL below 2x | AT-RISK 2–3x | HEALTHY 3–5x | INSPECT >5x]
  Pipeline Gap:         $[X] short  (or  $[X] surplus)

───────────────────────────────────────────────────────
IMBALANCE SIGNALS

  [For each signal fired:]
  ⚠️  [SIGNAL_LABEL] — [Severity: HIGH / MEDIUM]
      What's happening: [one sentence description]
      Evidence: [the specific numbers that triggered it]
      Risk: [what breaks if this isn't addressed]

───────────────────────────────────────────────────────
REMEDIATION ACTIONS

  Priority 1: [most urgent action]
  Priority 2: [second action]
  Priority 3: [third action — may be conditional]

  [If CS is the binding constraint on AE hiring:]
  CS Hiring Sequence: Hire CSMs before (or simultaneous with) AEs.
  Target: [X] CSMs needed to clear the ceiling for [X] AEs.
  Sequence: [specific hire order recommendation]

═══════════════════════════════════════════════════════
```

After presenting, offer:
- Run the reverse: "Want me to run the CS-anchored path to see what ARR your current CSMs can support?"
- Scenario comparison: "Want to model what happens at 30% vs 50% growth rate?"
- Pipeline deep-dive: "Want me to model the lead volume required to support this AE count?"

---

### STEP 7 — Scenario Mode (Optional)

If the user asks for scenario comparison, run two or three variants side-by-side:

```
SCENARIO COMPARISON
                        Conservative    Base Case    Aggressive
Growth Target:          [X]%            [X]%         [X]%
New ARR Target:         $[X]            $[X]         $[X]
AEs Required:           [X]             [X]          [X]
CSMs Required:          [X]             [X]          [X]
CS Ceiling Hit at:      $[X] ARR        $[X] ARR     $[X] ARR
Primary Constraint:     [AE / CS / Pipeline / Lead volume]
Imbalance Signals:      [list]          [list]       [list]
```

---

## Guardrails

### NEVER
- State headcount requirements as exact counts without flagging that benchmarks are ranges — always present as "approximately X–Y" or "X FTE (±1 given benchmark range)"
- Apply SMB benchmarks to Enterprise accounts or vice versa without flagging the mismatch
- Skip the CS capacity check when current CSM count is provided — it is always run
- Present the AE-derived headcount without checking whether CS can absorb the closed-won output
- Use the 3x pipeline coverage rule without checking win rate first — required coverage = 1 ÷ win rate, not a universal 3x
- Claim that adding more SDRs or AEs solves a pipeline quality problem — always distinguish volume from quality signals
- Present imbalance signals without remediation actions — every signal must have at least one concrete action
- Use the $1M/CSM rule as the only benchmark — it is a rough proxy and increasingly inaccurate with AI-assisted CS tooling

### ALWAYS
- State which benchmarks are being applied and where they come from — cite `references/benchmark-library.md` section and confidence tier when presenting any default or benchmark comparison
- Answer definition and formula questions from `references/metrics-and-glossary.md`, not from training memory
- Flag when user-provided inputs deviate significantly from benchmarks — note the deviation with the benchmark source, don't override the user's number
- Run the CS capacity check in both directions: forward (how many CSMs does AE output require?) and reverse (what ARR ceiling does current CSM count imply?)
- Distinguish between planning attainment rates (70–80%) and actual median attainment (55–65%, KBCM — `BL §6`) — use planning rates for forward models, note the gap
- Acknowledge NRR's effect on new ARR requirements: high NRR reduces the Sales burden; low NRR increases it
- Surface the CS hiring sequence when CS is the binding constraint — "hire in advance, not arrears" is the operational implication
- Present pipeline coverage as a function of win rate, not a static 3x rule — cite the formula from `references/metrics-and-glossary.md` §1 if the user pushes back on this
- Distinguish imbalance severity: HIGH signals indicate near-term revenue or retention risk; MEDIUM signals indicate efficiency or cost structure issues

### Failure Modes and Recovery

| Failure | Signal | Recovery |
|---------|--------|----------|
| User provides only ARR and growth % with no headcount data | Can run revenue model and benchmark-derived headcount only | Present derived headcount; note these are target states, not gap analysis; invite current counts |
| User provides current headcount but no ARR or growth target | Can run CS-anchored reverse only | Present max supportable ARR and CS ceiling; invite growth target for full model |
| Win rate not provided | Cannot compute accurate pipeline coverage | Use 25% default with explicit flag; recommend user verify with their CRM data |
| User asks about a specific individual (rep performance) | This is a structural tool | Redirect: "This model is for org-level capacity; rep performance is a coaching conversation" |
| Segment is ambiguous (e.g., "mid-market and enterprise mix") | Benchmarks diverge across segments | Run both and present the range; ask which segment represents the majority of the ARR target |
| NRR not known | User unsure of NRR | Default to 100% (neutral) with note; ask for churn rate as proxy if available |

### Guardrail Codes

- G5: All headcount model outputs are analytical inputs — planning proposals for board, CFO, or CRO review. No output constitutes an approved headcount plan.

---

## Worked Examples

These examples demonstrate full execution including explicit benchmark sourcing. When running
real calculations, present the same benchmark citations so the user can trace any number to
its source. Full formula definitions for every metric used below are in
`references/metrics-and-glossary.md` §1 and §2.

---

### Example A — Mid-Market AE-Anchored Model

**Inputs:**
- Current ARR: $5M | Target Growth: 45% | NRR: 110% | Segment: Mid-Market | Motion: Mixed
- AE Quota: $800K (benchmark midpoint, `BL §6` [Synthesized]) | Attainment: 75% (planning rate, `BL §6` [Verified]) | Current AEs: 3 | Current CSMs: 2
- CSM Model: ARR-based at $2M/CSM (low end of Mid-Market High-Touch benchmark, `BL §6` [Synthesized])
- Win Rate: 25% (default, `BL §9` [Heuristic]) | Current Pipeline: $2.5M

**Calculations:**
*(All formulas from `references/metrics-and-glossary.md` §2, Phases 1–4)*

```
— Phase 1: Revenue Model —
Target ARR          = $5M × 1.45 = $7.25M
New ARR Target      = $7.25M − ($5M × 1.10) = $7.25M − $5.5M = $1.75M
  NRR=110% means $0.5M of expansion reduces the new-logo burden from $2.25M to $1.75M
  (M&G §1 "New ARR Target" — NRR-adjusted formula)

— Phase 2: AE-Anchored Headcount —
Effective AE Capacity = $800K × 0.75 = $600K
AEs Required          = CEILING($1.75M ÷ $600K) = CEILING(2.92) = 3 AEs
SDRs Required         = CEILING(3 ÷ 2) = 2 SDRs  (1:2 ratio, mixed motion, BL §6)
CSMs Required         = CEILING($7.25M ÷ $2M) = CEILING(3.63) = 4 CSMs
  Currently 2 CSMs → gap of 2

— Phase 3: CS-Anchored Reverse —
Max Supported ARR    = 2 CSMs × $2M = $4M
Max Incremental ARR  = $4M − $5M = −$1M
  NEGATIVE: CS is already over capacity before any growth is modeled
  CS Headroom % = −$1M ÷ $5M = −20% (already breached)
Max AEs CS Supports  = −$1M ÷ $600K = −1.67 (constraint firing NOW)

— Phase 4: Pipeline Coverage Check —
Required Coverage    = 1 ÷ 0.25 = 4x  (M&G §1 "Required Coverage Ratio")
Pipeline Target      = $1.75M × 4 = $7M
Current Coverage     = $2.5M ÷ $1.75M = 1.43x → CRITICAL (BL §9 threshold: below 2x)
Pipeline Gap         = $7M − $2.5M = $4.5M short
```

**Imbalance Signals:**
*(Signal thresholds from `references/benchmark-library.md` §9)*

- ⚠️ `CS_UNDER_CAPACITY` — **HIGH**
  What's happening: 2 CSMs supporting $5M ARR = $2.5M/CSM, above the $2M mid-benchmark for Mid-Market High-Touch (`BL §6`). CS ceiling at $4M is already below current ARR.
  Evidence: Max Supported ARR $4M < Current ARR $5M; Max Incremental ARR = −$1M
  Risk: Every account closed by current AEs is landing in an over-capacity CS team. Churn risk is live now, not future.

- ⚠️ `SALES_OVER_CAPACITY` (relative to CS ceiling) — **MEDIUM**
  What's happening: CS cannot absorb additional closed-won accounts. Any AE hire before CS is fixed adds to the CS debt.
  Evidence: Max AEs CS Can Support = 0 (CS already over capacity)
  Risk: Hiring AEs before CSMs compounds the churn exposure without adding real growth capacity.

- ⚠️ `LEAD_VOLUME_INSUFFICIENT` — **HIGH**
  What's happening: Pipeline at 1.43x vs. 4x required (1 ÷ 25% win rate, `BL §9`).
  Evidence: Current pipeline $2.5M; Pipeline Target $7M; Gap $4.5M
  Risk: Even at 100% attainment, current pipeline closes $625K. The AE headcount question is moot until pipeline is built.

**Remediation Actions:**
1. **Hire 2 CSMs immediately.** CS is the binding constraint on current ARR — not future growth. Target: 4 CSMs → Max Supported ARR $8M → opens $3M headroom above current ARR.
2. **Invest in pipeline generation before adding AEs.** $4.5M pipeline gap must be closed before the AE count question matters. Focus SDR output and inbound on filling the gap.
3. **Once pipeline ≥3x ($5.25M+) and CS headcount = 4, model AE expansion** against the new CS ceiling.

---

### Example B — CS-Anchored Reverse Model

**Inputs:**
- Current ARR: $8M | Current CSMs: 3 | Segment: Enterprise | Touch: High-Touch
- ARR per CSM target: $3M (mid-range for Enterprise High-Touch, `BL §6` [Synthesized])
- Current AE Count: 4 | AE Quota: $1.2M (Enterprise midpoint, `BL §6` [Synthesized]) | Attainment: 75%

**Calculations:**
*(Formulas from `references/metrics-and-glossary.md` §2, Phase 3)*

```
— Phase 3: CS-Anchored Reverse —
Max Supported ARR    = 3 CSMs × $3M = $9M
Max Incremental ARR  = $9M − $8M = $1M
CS Headroom %        = $1M ÷ $8M × 100 = 12.5%
  (M&G §1 "CS Headroom %" — interpretation: <10% = near ceiling; 12.5% = limited headroom)

Effective AE Capacity = $1.2M × 0.75 = $900K
Max AEs CS Supports  = $1M ÷ $900K = 1.1 AEs of capacity

Current AE Output Potential = 4 AEs × $900K = $3.6M
CS ceiling absorbs $1M → 4 AEs could theoretically close 3.6× more than CS can absorb
```

**Imbalance Signal:**
*(Signal thresholds from `references/benchmark-library.md` §9)*

- ⚠️ `CS_UNDER_CAPACITY` — **HIGH**
  What's happening: 3 Enterprise CSMs at $3M/CSM = $9M ceiling. With $8M current ARR, there is only $1M of headroom — enough for approximately 1 new enterprise account. 4 AEs at full capacity could close $3.6M in new ARR that CS cannot support.
  Evidence: CS Headroom % = 12.5%; Max AEs CS Can Support = 1.1 vs. 4 AEs in seat
  Risk: Every enterprise account closed beyond the first adds churn risk — enterprise churn is 4–8% at median (`BL §3`) but concentrates in accounts where CS coverage is thin.

**Remediation Sequence:**
1. **Hire 2 Enterprise CSMs** → new ceiling: 5 CSMs × $3M = $15M → $7M headroom → Max AEs CS Can Support = 7.8 AEs. Clears the constraint well ahead of current AE count.
2. **Model AE expansion against the $15M ceiling** — there is now capacity to grow before the next CS hire.
3. **Hiring sequence: CSM → AE, not AE → CSM.** With a 3–6 month enterprise CSM ramp, hire CSMs 1 quarter before AE hiring accelerates.

---

## Session Memory

On repeat use within a session:
- Retain confirmed inputs across calculations — do not re-request ARR, segment, or headcount counts already confirmed
- If the user runs scenario comparisons, carry the base-case inputs and vary only the parameter being tested
- If the user references "the model we built" or "our current headcount," use the inputs confirmed earlier in the session

---

## Security & Permissions

This skill performs calculations on user-provided inputs only. No external API calls, file access, or data persistence. All inputs are session-scoped.

- Network access: none
- Filesystem access: none
- Tool calls: none
- Data retention: session scope only

---

## Trust & Verification

**Primary benchmark source:** KBCM Technology Group & Sapphire Ventures Annual Private SaaS
Survey, 13th–16th editions (2022–2025), approximately 390 respondent-years across four
consecutive annual surveys. This is the authoritative source for all retention benchmarks
(NRR, GRR, gross churn, expansion ratios, Net Magic Number, CAC payback, contract length
effects, PS attach effects).

**Supporting sources:** SaaS Capital 2025 Spending Benchmarks (CS budget as % ARR); Bain &
Company 2024 (CS investment → NRR relationship); Software Equity Group Q2 2024, n=112 public
companies (NRR → valuation relationship); McKinsey November 2025 (NRR ownership and
accountability structure); SuccessCOACHING SaaS Market Evolution research (GTM headcount
ratios, SDR:AE, AE:CSM).

Full source registry with URLs, sample sizes, vintage, and per-row confidence tiers:
`references/benchmark-library.md` — Source Registry table.

**Confidence tiers used throughout:**
- `[Verified]` — traced to a named primary report with specific data and n= where available
- `[Synthesized]` — consistent across multiple named sources but not a single definitive table
- `[Heuristic]` — widely cited rule-of-thumb with known variance; flag when presenting

Benchmarks are ranges, not targets. Every output is a starting point for conversation, not
a definitive headcount plan. Actual optimal ratios depend on product complexity, sales motion
maturity, CS tooling, and geographic distribution — factors this model cannot fully account
for from inputs alone.

[Confidence: High for formula calculations. Moderate for GTM headcount benchmarks
(SDR:AE, AE:CSM, quota ranges) — sourced from industry synthesis rather than a single
primary survey, and shifting as AI-assisted CS tooling compresses CSM headcount requirements.]

---

## Reference Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `references/benchmark-library.md` | Full benchmark tables for NRR/GRR, gross churn, downsell, unit economics, GTM headcount (AE quota, attainment, SDR:AE, CSM portfolio sizes), operating efficiency, growth rates, imbalance signal thresholds, and AI/pricing risk signals. Source Registry with URLs, vintage, and sample sizes. Per-row confidence tiers [Verified / Synthesized / Heuristic]. | When applying benchmark defaults, citing sources in output, or checking imbalance signal thresholds |
| `references/metrics-and-glossary.md` | Section 1: Metrics Catalog — definition, formula, inputs, units, interpretation, benchmarks, and common errors for every metric used in the skill. Section 2: Formula Reference — all formulas in execution order (Phases 1–6). Section 3: Glossary — plain-language definitions for all terms. | When answering "what does X mean?", verifying a formula, or explaining a metric to the user |
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill | |

---

