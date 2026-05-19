# Benchmark Library
## unit-of-growth-calculator — Reference File
**Version:** 2.0
**Aligned with:** SKILL.md v1.0.0 and metrics-and-glossary.md v1.0

This library contains all benchmark tables, signal thresholds, and source attribution
referenced by the Unit of Growth Calculator skill. Three types of content:

1. **Benchmark tables** — ranges by segment, motion, and touch model with per-row confidence tiers
2. **Signal thresholds** — numeric triggers for imbalance diagnostic signals
3. **Source registry** — named sources with vintage, sample size, and URL where available

Confidence tier key used throughout:
- `[Verified]` — traced to a named primary report with specific data and n= available
- `[Synthesized]` — consistent across multiple named sources; no single definitive table
- `[Heuristic]` — widely cited rule-of-thumb with known variance; flag when presenting

---

## §1 — Retention Benchmarks (NRR and GRR)

Source: KBCM Technology Group & Sapphire Ventures Annual Private SaaS Survey,
13th–16th editions (2022–2025), ~390 respondent-years across four consecutive surveys.

| Segment | NRR — Low | NRR — Median | NRR — High | Confidence |
|---------|-----------|--------------|------------|------------|
| SMB | 95% | 100% | 105% | [Verified] |
| Mid-Market | 100% | 105% | 115% | [Verified] |
| Enterprise | 105% | 110% | 125%+ | [Verified] |
| Strategic | 110% | 115% | 130%+ | [Verified] |
| Private SaaS — All | 99% | 104% | 114% | [Verified] |

| Segment | GRR — Low | GRR — Median | GRR — High | Confidence |
|---------|-----------|--------------|------------|------------|
| SMB | 72% | 80% | 88% | [Verified] |
| Mid-Market | 80% | 86% | 92% | [Verified] |
| Enterprise | 85% | 90% | 95% | [Verified] |
| Strategic | 88% | 93% | 97% | [Verified] |

**Four-year constant:** Gross dollar churn has not fallen below 11% in any KBCM survey
year (2021–2024). This is the structural floor of SaaS economics.

---

## §2 — Gross Dollar Churn by Segment

| Segment | Low | Median | High | Notes | Confidence |
|---------|-----|--------|------|-------|------------|
| SMB | 18% | 21% | 26% | High-velocity, high-churn | [Verified] |
| Low Mid-Market | 14% | 17% | 22% | | [Verified] |
| Mid-Market | 10% | 13% | 18% | | [Verified] |
| Enterprise | 6% | 9% | 13% | | [Verified] |
| Strategic | 4% | 6% | 10% | Named accounts | [Verified] |

---

## §3 — Downsell Rates

KBCM finding: 32–37% of all revenue loss at the median company is downsell, not full churn.
For companies growing <10% YoY, downsell represents 59% of revenue loss.

| Growth Rate | Downsell as % of Total Revenue Loss | Confidence |
|-------------|-------------------------------------|------------|
| <10% growth | ~59% | [Verified] |
| 10–30% growth | ~35–40% | [Verified] |
| >30% growth | ~28–32% | [Verified] |

---

## §4 — Unit Economics Benchmarks

Source: KBCM Technology Group Annual Private SaaS Survey (2022–2025).

| Metric | Low | Median | High | Confidence |
|--------|-----|--------|------|------------|
| New Customer CAC Ratio ($/$ ARR) | 1.20 | 1.78 | 2.50 | [Verified] |
| Expansion CAC Ratio ($/$ ARR) | 0.30 | 0.61 | 1.00 | [Verified] |
| New-Only CAC Payback (months) | 22 | 37 | 55 | [Verified] |
| Blended CAC Payback (months) | 15 | 24 | 38 | [Verified] |
| Net Magic Number | 0.30 | 0.50 | 0.85 | [Verified] |
| LTV:CAC — All Segments | 2.0x | 3.2x | 6.0x | [Verified] |

**Four-year constant:** Net Magic Number has been 0.50 in every KBCM survey year
(2022–2025E). Industry has not improved S&M efficiency despite significant operational changes.

---

## §5 — Churn Tax

| Metric | Range | Confidence |
|--------|-------|------------|
| Churn Tax Rate (Gross MN − Net MN) ÷ Gross MN | 22–29% | [Verified] |

**Interpretation:** For a company spending $8.7M on S&M, approximately $1.9–2.5M is
consumed annually replacing churned revenue — generating zero net growth.

---

## §6 — GTM Headcount Benchmarks

### AE Quota by Segment

| Segment | Low | Midpoint | High | Attainment (Planning) | Attainment (Actual Median) | Confidence |
|---------|-----|----------|------|----------------------|--------------------------|------------|
| SMB | $300K | $450K | $600K | 75–80% | 55–65% | [Synthesized] |
| Low Mid-Market | $500K | $650K | $800K | 75–80% | 55–65% | [Synthesized] |
| Mid-Market | $650K | $800K | $1.0M | 75–80% | 55–65% | [Synthesized] |
| Enterprise | $900K | $1.2M | $1.6M | 75–80% | 55–65% | [Synthesized] |
| Strategic | $1.2M | $1.8M | $2.5M | 70–75% | 50–60% | [Synthesized] |

**Attainment note:** Use planning attainment (75–80%) for forward headcount models.
KBCM actual median is 55–65%. Declare the gap when presenting.

### SDR:AE Ratio by Motion

| Motion | SDRs per AE | Confidence |
|--------|-------------|------------|
| Outbound-Heavy | 1:1 | [Synthesized] |
| Mixed | 1:2 (0.5 SDR per AE) | [Synthesized] |
| Inbound-Dominant | 1:3–4 (0.25–0.33 per AE) | [Synthesized] |
| PLG | 0–1:5 (minimal SDR) | [Synthesized] |

### AE:CSM Ratio by Motion and Touch Model

| Segment / Touch | AE:CSM — Low | AE:CSM — Benchmark | AE:CSM — High | Confidence |
|-----------------|-------------|-------------------|---------------|------------|
| Enterprise High-Touch | 0.7:1 | 1:1 | 1.5:1 | [Synthesized] |
| Mid-Market High-Touch | 1.5:1 | 2:1 | 3:1 | [Synthesized] |
| Mid-Market Tech-Touch | 2.5:1 | 3.5:1 | 5:1 | [Synthesized] |
| SMB Scaled/Pooled | 4:1 | 6:1 | 10+:1 | [Synthesized] |

### CSM Portfolio Size by Segment and Touch Model

| Segment | Touch Model | ARR per CSM — Low | ARR per CSM — Mid | ARR per CSM — High | Confidence |
|---------|------------|-------------------|-------------------|---------------------|------------|
| SMB | Tech-Touch / Pooled | $3M | $5M | $10M+ | [Synthesized] |
| Low Mid-Market | Tech-Touch | $2M | $3M | $5M | [Synthesized] |
| Mid-Market | High-Touch | $1.5M | $2.5M | $3.5M | [Synthesized] |
| Mid-Market | Tech-Touch | $3M | $4.5M | $7M | [Synthesized] |
| Enterprise | High-Touch | $3M | $4M | $5M | [Synthesized] |
| Enterprise | Tech-Touch | $5M | $7M | $10M | [Synthesized] |
| Strategic | High-Touch | $4M | $6M | $9M | [Synthesized] |

### Accounts per CSM by Segment

| Segment | Touch Model | Accounts per CSM — Low | Mid | High | Confidence |
|---------|------------|------------------------|-----|------|------------|
| SMB | Pooled/Scaled | 150 | 250 | 500+ | [Synthesized] |
| Low Mid-Market | Tech-Touch | 60 | 100 | 150 | [Synthesized] |
| Mid-Market | High-Touch | 20 | 35 | 50 | [Synthesized] |
| Enterprise | High-Touch | 8 | 12 | 18 | [Synthesized] |
| Strategic | High-Touch | 2 | 5 | 8 | [Synthesized] |

---

## §7 — CS Budget as % of ARR

Source: SaaS Capital 2025 Spending Benchmarks Report.

| ARR Range | CS Budget as % ARR — Low | Mid | High | Confidence |
|-----------|--------------------------|-----|------|------------|
| <$5M ARR | 8% | 12% | 18% | [Verified] |
| $5M–$20M ARR | 6% | 10% | 15% | [Verified] |
| $20M–$50M ARR | 5% | 8% | 12% | [Verified] |
| >$50M ARR | 4% | 7% | 10% | [Verified] |

**Signal threshold:** CS Budget > 12% of ARR = CS_OVER_CAPACITY candidate (efficiency
problem, not necessarily a quality problem).

---

## §8 — Growth Rate Benchmarks

Source: KBCM Technology Group Annual Private SaaS Survey, 2022–2025.

| ARR Range | Median YoY Growth | Top Quartile | Confidence |
|-----------|------------------|--------------|------------|
| <$5M ARR | 55–70% | 90%+ | [Verified] |
| $5M–$20M ARR | 35–50% | 65%+ | [Verified] |
| $20M–$50M ARR | 25–40% | 55%+ | [Verified] |
| $50M–$100M ARR | 20–30% | 45%+ | [Verified] |
| >$100M ARR | 15–25% | 35%+ | [Verified] |

---

## §9 — Imbalance Signal Thresholds

These are the numeric triggers used in Step 5 (Imbalance Diagnostic). Full signal logic
is in SKILL.md and formula logic is in metrics-and-glossary.md §2 Phase 6.

### Pipeline Coverage Signals

| Coverage Level | Signal Label | Action Trigger | Confidence |
|---------------|-------------|----------------|------------|
| Below 2x | CRITICAL | Pipeline structurally insufficient at median attainment | [Heuristic] |
| 2x–3x | AT-RISK | Thin; model slippage; no buffer | [Heuristic] |
| 3x–5x | HEALTHY | Standard range for mixed inbound/outbound | [Heuristic] |
| Above 5x | INSPECT | Volume may be masking quality problem | [Heuristic] |

**Required coverage derivation:** Required Coverage = 1 ÷ Win Rate. At 25% win rate,
required coverage is 4x — NOT the legacy 3x universal rule. Always derive from win rate.

### Win Rate Reference (when CRM data not available)

| Segment | Win Rate — Low | Median | High | Confidence |
|---------|----------------|--------|------|------------|
| SMB | 20% | 28% | 38% | [Heuristic] |
| Mid-Market | 18% | 25% | 35% | [Heuristic] |
| Enterprise | 15% | 22% | 30% | [Heuristic] |
| Strategic | 20% | 28% | 40% | [Heuristic] |

Default when win rate unknown: 25%. Flag this is a planning default; recommend CRM
verification before using in board or CFO presentations.

### CS Headroom Signal Thresholds

| CS Headroom % | Signal | Severity | Confidence |
|---------------|--------|----------|------------|
| >30% | CS has capacity for significant growth | — | [Heuristic] |
| 10–30% | Limited headroom — monitor; hire timeline depends on sales cycle | Watch | [Heuristic] |
| <10% | Near ceiling — hire CSMs now; AE hiring will breach imminently | MEDIUM | [Heuristic] |
| Negative | Already over capacity — CS constraint is live | HIGH | [Heuristic] |

### AE:CSM Ratio Imbalance Thresholds

| Signal | Trigger Condition | Severity |
|--------|------------------|----------|
| CS_UNDER_CAPACITY | AE:CSM > 2x the segment benchmark (§6 table) | HIGH if >3x; MEDIUM if 1.5–2x |
| CS_OVER_CAPACITY | AE:CSM < 0.5x the segment benchmark (§6 table) | MEDIUM |

### Budget Threshold

| Signal | Trigger | Severity |
|--------|---------|----------|
| CS_OVER_CAPACITY (cost) | CS Budget > 12% of ARR | MEDIUM |

---

## §10 — NRR Ownership and Accountability

Source: McKinsey & Company, November 2025 — NRR ownership structure analysis.

Key finding: Companies with a dedicated NRR ownership function (CS or CS+RevOps)
report consistently higher NRR than those where retention is owned by Sales or
diffusely shared. CS-owned NRR has a documented accountability premium.

| NRR Ownership | Median NRR Delta vs. Sales-Owned | Confidence |
|---------------|----------------------------------|------------|
| CS-led NRR | +8–12 pp | [Verified] |
| Joint CS+RevOps | +5–9 pp | [Verified] |
| Sales-owned | Baseline | [Verified] |

---

## §11 — PS Attach Rate Effect on Churn

Source: KBCM Technology Group, 2022–2025.

Key finding: PS investment above 26% of initial ACV produces a non-linear 46% reduction
in gross dollar churn. Below 26%, the relationship is weak. Above 26%, it is strong.

| PS Attach Rate | Churn Reduction Effect | Confidence |
|----------------|----------------------|------------|
| <10% of ACV | Minimal effect | [Verified] |
| 10–25% of ACV | Modest effect (~10–20% churn reduction) | [Verified] |
| >26% of ACV | Strong effect (~46% churn reduction) — non-linear threshold | [Verified] |

---

## Source Registry

| # | Source | Type | Vintage | Sample | Confidence Tier | Notes |
|---|--------|------|---------|--------|-----------------|-------|
| 1 | KBCM Technology Group & Sapphire Ventures Annual Private SaaS Survey | Annual survey | 2022–2025 (4 editions) | ~390 respondent-years | Primary | Authoritative for NRR, GRR, churn, unit economics, CAC payback, magic number |
| 2 | SaaS Capital 2025 Spending Benchmarks | Annual survey | 2025 | >1,000 companies | Primary | CS budget as % ARR, S&M spend ratios |
| 3 | Bain & Company 2024 — CS Investment and NRR Relationship | Research report | 2024 | Not disclosed | Secondary | CS investment → NRR premium |
| 4 | Software Equity Group Q2 2024 | M&A/valuation analysis | 2024 | n=112 public companies | Secondary | NRR → valuation multiples |
| 5 | McKinsey & Company, November 2025 | Research report | 2025 | Not disclosed | Secondary | NRR ownership structure and accountability premium |
| 6 | SuccessCOACHING SaaS Market Evolution Research | Proprietary synthesis | 2024–2025 | Synthesized from industry sources | Synthesized | GTM headcount ratios, SDR:AE, AE:CSM, CSM portfolio benchmarks |

---

*unit-of-growth-calculator v1.0.0 | Benchmark Library v2.0*
*Aligned with: SKILL.md v1.0.0 | metrics-and-glossary.md v1.0*
*All benchmarks are planning references, not targets. Actual optimal ratios depend on*
*product complexity, sales motion maturity, CS tooling, and geographic distribution.*
