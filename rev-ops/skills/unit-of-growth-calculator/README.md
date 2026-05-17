# unit-of-growth-calculator

**Version:** 1.1.0 | **Status:** [PROPOSED] | **Author:** SuccessCOACHING

Computes GTM headcount requirements and surfaces capacity imbalance signals for B2B SaaS
organizations. Works from either direction: start from a revenue target to derive required
headcount across AE, SDR, CSM, and Support functions, or start from existing CS headcount
to find the maximum ARR growth the post-sales org can absorb before breaking.

Anchors on the AE as the unit of growth. Derives all other headcount from a small set of
ratios and benchmarks, then runs five structural imbalance checks with severity-rated signals
and specific remediation actions.

---

## Folder Structure

```
unit-of-growth-calculator/
│
├── README.md                          ← This file
├── SKILL.md                           ← Skill definition (672 lines)
│
└── references/
    ├── benchmark-library.md           ← All benchmarks with primary source citations (443 lines)
    └── metrics-and-glossary.md        ← Metrics catalog, formula reference, glossary (1,160 lines)
```

---

## File Descriptions

### `SKILL.md`
The executable skill definition. Contains the full 7-step workflow, input/output schemas,
benchmark defaults, calculation instructions for both AE-anchored and CS-anchored paths,
pipeline coverage logic, five imbalance signal checks, output format template, two worked
examples with full benchmark citations, guardrails, and failure mode recovery.

**Key sections:**
- Overview: activation triggers and exclusions
- Specification: calculation modes, benchmark sources, reference file pointers
- Input Schema: all inputs across Tiers 1–3 (core, AE, SDR, CSM, optional)
- Output Schema: full structured output including all check results and imbalance signals
- Core Workflow: Steps 1–7
  - Step 1 — Intake with tiered input collection and benchmark defaults table (with `BL §` citations)
  - Step 2 — AE-Anchored Calculation (revenue → headcount)
  - Step 3 — CS-Anchored Calculation (headcount → max ARR)
  - Step 4 — Pipeline Coverage Check
  - Step 5 — Imbalance Diagnostic (five signals)
  - Step 6 — Structured results output template
  - Step 7 — Scenario comparison mode
- Guardrails: NEVER / ALWAYS / Failure Modes and Recovery
- Worked Examples: two fully annotated examples with benchmark and formula citations
- Trust & Verification: primary sources, confidence tier explanation

---

### `references/benchmark-library.md`
All benchmarks used by the skill, with primary source citations, sample sizes, vintage, and
per-row confidence tiers. Every number the skill uses as a default or comparison point traces
to a row in this file, which traces to a named primary source in the Source Registry.

**Confidence tiers:**
- `[Verified]` — traced to a named primary report with specific data and n= where available
- `[Synthesized]` — consistent across multiple named sources but not a single definitive table
- `[Heuristic]` — widely cited rule-of-thumb; flag when presenting to CFO or board audiences

**Primary data source:** KBCM Technology Group & Sapphire Ventures Annual Private SaaS
Survey, 13th–16th editions (2022–2025), ~390 respondent-years. Supporting sources: SaaS
Capital 2025, Bain & Company 2024, Software Equity Group Q2 2024, McKinsey 2025,
SuccessCOACHING SaaS Market Evolution research.

**Sections:**

| Section | Contents |
|---------|----------|
| Source Registry | 12 named sources with full name, coverage, vintage, sample size, and URL |
| §1 — Core Formulas | All calculation formulas in compact reference form |
| §2 — NRR and GRR | Four-year longitudinal NRR/GRR, by ARR band, by GTM model, valuation sensitivity |
| §3 — Gross Churn | Structural floor, by contract length (highest-leverage lever), by ACV, by PS attach rate |
| §4 — Downsell | Downsell as % of revenue loss, causal direction note |
| §5 — Unit Economics | CAC, CAC payback, LTV:CAC, Magic Number, Churn Tax, expansion composition |
| §6 — GTM Headcount | AE quota, AE attainment, SDR:AE ratio, CSM portfolio (ARR and account-based), AE:CSM ratio |
| §7 — Operating Efficiency | S&M/R&D spend trends, CS budget %, gross margin, Rule of 40, top-quartile vs. median |
| §8 — Growth Rates | By ARR band with median and top-quartile thresholds |
| §9 — Imbalance Signal Thresholds | Fire conditions and evidence basis for all five signals |
| §10 — AI/Pricing Risk | Seat-based pricing prevalence, AI operational changes, structural downsell risk |
| Benchmark Application Rules | Six rules for valid benchmark use (from SC-BDR) |
| Segment Definitions | SMB through Strategic with ACV ranges, motion, and sales cycle |

---

### `references/metrics-and-glossary.md`
The skill's complete reference for metric definitions, formulas, and terminology. Three
sections covering everything used across the skill and benchmark library.

**Section 1 — Metrics Catalog (30 metrics)**

Full entries for every metric used in the skill. Each entry includes: definition, formula,
inputs, units, interpretation (with threshold guidance), benchmark reference, and common
errors. Organized in four groups:

| Group | Metrics |
|-------|---------|
| Revenue | ARR, New ARR Target, NRR, GRR, Gross Dollar Churn, Downsell ARR, Expansion ARR |
| Unit Economics | CAC, CAC Payback Period, LTV, LTV:CAC, Net Magic Number, Gross Magic Number, Churn Tax, Burn Multiple, Rule of 40 |
| GTM Capacity | Effective AE Capacity, AEs Required, SDRs Required, CSMs Required, Max Supported ARR, Max Incremental ARR, CS Headroom %, Max AEs CS Can Support, AE:CSM Ratio |
| Pipeline | Pipeline Coverage Ratio, Required Coverage Ratio, Pipeline Gap, Pipeline Coverage Signals, Win Rate, Lead Sufficiency, Support FTE Required |

**Section 2 — Formula Reference (6 phases)**

All formulas in execution order, exactly matching the skill's 7-step workflow:

| Phase | Contents |
|-------|---------|
| Phase 1 | Revenue Model — Target ARR, New ARR Target (simple and NRR-adjusted) |
| Phase 2 | AE-Anchored Headcount — Effective AE Capacity, AEs Required, SDRs Required, CSMs Required (ARR-based and account-based), Support FTE |
| Phase 3 | CS-Anchored Reverse — Max Supported ARR, Max Incremental ARR, CS Headroom %, Max AEs CS Can Support, constraint check logic |
| Phase 4 | Pipeline Coverage — Required Coverage, Pipeline Target, Current Coverage, Pipeline Gap, coverage signal thresholds |
| Phase 5 | Efficiency Metrics — Magic Numbers, Churn Tax, LTV, CAC Payback, Pre-Payback Churn probability, LTV:CAC |
| Phase 6 | Imbalance Signals — all five signal fire conditions, severity rules, and the rule that every signal requires a remediation action |

**Section 3 — Glossary (60+ terms)**

Plain-language definitions for every term used across the skill and benchmark library.
Covers all acronyms (AE, SDR, CSM, NRR, GRR, LTV, CAC, etc.), all segment labels, all
motion types, all imbalance signal labels, and all calculation terms. Includes critical
distinctions — e.g., why Required Coverage ≠ 3x, why blended CAC payback misleads, why
planning attainment ≠ market median attainment.

---

## How the Files Work Together

```
User Invokes Skill
       ↓
STEP 1 — Intake
  Benchmark defaults   →  references/benchmark-library.md §6 (GTM Headcount)
  Term definitions     →  references/metrics-and-glossary.md §3 (Glossary)
       ↓
STEPS 2–4 — Calculations
  Formula execution    →  references/metrics-and-glossary.md §2 (Formula Reference)
  Metric interpretation→  references/metrics-and-glossary.md §1 (Metrics Catalog)
  Benchmark comparisons→  references/benchmark-library.md (cited by section per check)
       ↓
STEP 5 — Imbalance Diagnostic
  Signal thresholds    →  references/benchmark-library.md §9
  Benchmark evidence   →  references/benchmark-library.md §6 (GTM Headcount)
       ↓
STEP 6 — Present Results
  All cited values include BL §X source tags and confidence tiers
```

**When the skill cites a reference, the format is:**
- `BL §X` — benchmark-library.md section X (e.g., `BL §6` for GTM headcount benchmarks)
- `M&G §1` — metrics-and-glossary.md Section 1, Metrics Catalog
- `M&G §2` — metrics-and-glossary.md Section 2, Formula Reference

---

## Imbalance Signals

Five structural checks run after every calculation. Each fires independently; multiple
can fire in the same run.

| Signal | Description | Max Severity |
|--------|------------|--------------|
| `CS_UNDER_CAPACITY` | Too few CSMs to absorb AE closed-won output | HIGH |
| `CS_OVER_CAPACITY` | Too many CSMs for current ARR base | MEDIUM |
| `SALES_OVER_CAPACITY` | Too many AEs for available pipeline or CS ceiling | HIGH |
| `SALES_UNDER_CAPACITY` | Too few AEs to hit revenue target | HIGH |
| `LEAD_VOLUME_INSUFFICIENT` | Pipeline generation is the binding constraint, not headcount | HIGH |

Signal thresholds and evidence basis for each: `references/benchmark-library.md §9`.

---

## Worked Examples (in SKILL.md)

Two fully annotated examples showing complete execution with benchmark citations.

**Example A — Mid-Market AE-Anchored Model**
- $5M ARR, 45% growth target, 110% NRR, Mixed motion
- AE Quota $800K (`BL §6` [Synthesized]), 75% attainment, 3 AEs, 2 CSMs
- Signals fired: `CS_UNDER_CAPACITY` HIGH, `SALES_OVER_CAPACITY` MEDIUM, `LEAD_VOLUME_INSUFFICIENT` HIGH
- Key finding: CS already over capacity at current ARR ($4M ceiling vs. $5M ARR) before any growth is modeled

**Example B — CS-Anchored Reverse Model**
- $8M ARR, 3 Enterprise CSMs at $3M/CSM (`BL §6` [Synthesized])
- 4 AEs at $1.2M quota (`BL §6` [Synthesized]), 75% attainment
- Signal fired: `CS_UNDER_CAPACITY` HIGH — only 1 AE's worth of capacity before hitting $9M CS ceiling
- Key finding: 4 AEs could theoretically close $3.6M; CS can absorb $1M. Hire 2 CSMs before adding AEs.

---

## Calculation Modes

| Mode | Starting Point | Output |
|------|---------------|--------|
| AE-Anchored | Revenue target → derives AE, SDR, CSM, Support headcount required | Headcount model + CS capacity check + pipeline check |
| CS-Anchored | Current CSM count → derives max supportable ARR and AE ceiling | CS capacity ceiling + constraint signal + hiring sequence |
| Scenario | Run either mode across 2–3 growth scenarios side-by-side | Comparative output showing primary constraint per scenario |

Both modes always run the CS capacity check — forward and reverse — when CSM count is provided.

---

## Segment Defaults

All benchmark defaults are segment-specific. Applying the wrong segment's benchmarks is
flagged as a NEVER in the skill's guardrails.

| Segment | ACV Range | Motion | AE Quota Midpoint | ARR per CSM (High-Touch) |
|---------|-----------|--------|------------------|--------------------------|
| SMB | <$10K | PLG / high-velocity inbound | $500K | $5–8M (scaled) |
| Low Mid-Market | $10–25K | Inside sales, inbound-dominant | $600K | $2–3.5M |
| Mid-Market | $25–100K | Inside + field, mixed | $800K | $2–3.5M |
| Enterprise | $100–500K | Field sales, multi-stakeholder | $1.2M | $3–5M |
| Strategic | >$500K | Named accounts, executive selling | $2.5M | $1–3M |

Source: `references/benchmark-library.md §6` [Synthesized]. For CFO-grade presentations,
replace [Synthesized] benchmarks with Bridge Group 2024 AE Metrics data or company actuals.

---

## Key Benchmarks at a Glance

Selected [Verified] data points from `references/benchmark-library.md` (KBCM primary source):

| Metric | Value | Source |
|--------|-------|--------|
| Median private SaaS NRR (2024) | 101% | KBCM-25 [Verified] |
| Median gross dollar churn floor | Never below 11% (2021–2024) | KBCM 4-year [Verified] |
| Churn on 3+ year contracts | 3–5% (vs. 13–14% annual) | KBCM 2022–2025 [Verified] |
| Net Magic Number (2022–2025E) | 0.50 — unchanged 4 years | KBCM [Verified] |
| New-only CAC payback (2024) | 37 months | KBCM-25 [Verified] |
| AE median quota attainment (actual) | 55–65% | KBCM [Verified] |
| NRR >120% valuation premium | +63% (9.3x vs. 5.7x EV/Revenue) | SEG Q2 2024 (n=112) [Verified] |

Full tables, all benchmarks, and complete source registry: `references/benchmark-library.md`.

---

*unit-of-growth-calculator v1.1.0 | SuccessCOACHING Skills Ecosystem*
*Research foundation: KBCM Technology Group & Sapphire Ventures Annual Private SaaS Survey
13th–16th editions (2022–2025); SaaS Capital 2025; Bain & Company 2024; Software Equity
Group Q2 2024; McKinsey 2025; SuccessCOACHING SaaS Market Evolution research*
