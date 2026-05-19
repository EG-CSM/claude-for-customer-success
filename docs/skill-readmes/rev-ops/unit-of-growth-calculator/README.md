# rev-ops.unit-of-growth-calculator

Computes GTM headcount requirements, capacity imbalances, and efficiency diagnostics for B2B SaaS organizations using the AE-anchored or CSM-anchored pod model. Synthesizes SuccessCOACHING Unit of Growth research with 2025 SaaS benchmarks. Works forward (revenue targets → headcount) or reverse (current headcount → max supportable ARR). Surfaces five imbalance signals across AE, SDR, CSM, and Support functions.

## Use it for

- Model GTM headcount requirements from ARR target and segment
- Run CS-anchored reverse to find max ARR current CSM count can support
- Detect CS under/over-capacity, Sales under/over-capacity, and lead volume insufficiency
- Produce pipeline coverage check from win rate and current pipeline value
- Generate AE:CSM:SDR headcount table with benchmark citations for board/CRO/CFO reviews

## Don't use it for

- Individual rep performance review (structural capacity tool, not rep coaching)
- Pricing or packaging analysis
- Customer health scoring or churn prediction on specific accounts
- Detailed financial modeling with COGS, EBITDA, or equity dilution

## How to trigger it

Say something like:

- "model my GTM headcount"
- "do I have enough CSMs"
- "how much ARR can my CS team support"
- "is my pipeline coverage healthy"
- "run the unit of growth calculation"
- "show me where my GTM org is over or under capacity"

## What you get

- {'UoG analysis': 'headcount model (AE/SDR/CSM/Support required vs. current)'}
- CS capacity check (max supported ARR, headroom %, max AEs CS can support)
- Pipeline coverage check (required coverage ratio, gap, coverage signal)
- Imbalance signals (up to 5 categories, severity HIGH/MEDIUM)
- Remediation actions (priority-ranked, concrete)
- {'Optional': 'scenario comparison (conservative/base/aggressive)'}

## Prerequisites

- current_arr, target_growth_pct or new_arr_target
- segment (SMB / Mid-Market / Enterprise / Strategic)
- motion (Outbound-Heavy / Mixed / Inbound-Dominant / PLG)
- ae_quota, ae_attainment (or accept benchmark defaults)
- csm_model preference (ARR-based or account-based)
- {'Optional': 'current AE/SDR/CSM counts, win rate, pipeline value, ACV, sales cycle'}

## Governance

- Benchmark defaults applied explicitly with source citation (benchmark-library.md section and confidence tier)
- All metrics and formulas answered from references/metrics-and-glossary.md — not training memory
- Pipeline coverage = 1 ÷ win rate; never hardcode 3x rule
- CS capacity check always runs when current CSM count is provided (non-optional)
- Headcount outputs presented as ranges (±1 FTE) given benchmark variability
- Distinguish planning attainment rate (75%) from KBCM actual median (55–65%)
- {'CS is the binding constraint check': 'if Max AEs CS Can Support < AEs Required → flag immediately'}

## See also

- rev-ops.annual-planning-workflow
- rev-ops.closed-won-to-cs-capacity-modeling
- rev-ops.quota-sensitivity-analysis
- rev-ops.scenario-modeling
- rev-ops.pipeline-coverage-analysis

---

*Domain: `rev-ops` · Skill ID: `rev-ops.unit-of-growth-calculator`*
