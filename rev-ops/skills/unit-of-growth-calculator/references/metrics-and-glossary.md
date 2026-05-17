# Metrics, Formulas, and Glossary
## unit-of-growth-calculator — Reference File
**Version:** 1.0
**Aligned with:** SKILL.md v1.0.0 and benchmark-library.md v2.0

This reference documents every metric, formula, and term used in the skill and its benchmark library. Three sections:

1. **Metrics Catalog** — what each metric measures, how it is calculated, what good looks like
2. **Formula Reference** — all formulas in execution order with annotations
3. **Glossary** — definitions of all terms used across the skill and benchmark library

---

## SECTION 1 — Metrics Catalog

Each entry follows this structure:
- **Definition** — what the metric measures
- **Formula** — how it is calculated
- **Inputs** — what you need to compute it
- **Units** — the output unit
- **Interpretation** — how to read the result
- **Benchmark** — reference range (see benchmark-library.md for full tables with sources)
- **Common errors** — how this metric is misused

---

### Revenue Metrics

---

#### ARR — Annual Recurring Revenue

**Definition:** The annualized value of active subscription contracts at a point in time. The primary size metric for SaaS businesses.

**Formula:**
```
ARR = Sum of all active subscription contract values × (12 ÷ contract months)
```
For a monthly subscription: ARR = MRR × 12

**Inputs:** Active contract values and their billing periods

**Units:** Dollar amount (e.g., $5,000,000)

**Interpretation:** ARR is a snapshot, not a cash flow statement. A company with $5M ARR has $5M of annualized subscription value committed at that moment. It does not mean they collected $5M last year.

**Common errors:**
- Confusing ARR with revenue recognized (ARR is a forward run-rate; revenue is backward-looking)
- Including one-time professional services fees in ARR (they are not recurring)
- Not adjusting for partial-year contracts (a 6-month contract at $50K = $100K ARR, not $50K)

---

#### New ARR Target

**Definition:** The incremental ARR that must be closed in the planning period — net of what existing customers will provide through expansion — to hit the growth target.

**Formula (simple, no NRR):**
```
New ARR Target = Current ARR × Target Growth %
```

**Formula (NRR-adjusted, preferred):**
```
Target ARR     = Current ARR × (1 + Target Growth %)
New ARR Target = Target ARR − (Current ARR × NRR)
```

**Inputs:** Current ARR, Target Growth %, NRR (optional but recommended)

**Units:** Dollar amount

**Interpretation:**
- When NRR > 1.0: Existing customer expansion offsets some of the new-logo requirement. A company with 110% NRR needs less from Sales than the growth rate implies.
- When NRR < 1.0: Churn must be replaced before net growth begins. A company with 90% NRR must first close enough new ARR to cover the $X being lost before counting any growth.
- When NRR = 1.0: No adjustment needed.

**Example:**
- Current ARR $5M, 45% growth target, NRR 110%
- Target ARR = $5M × 1.45 = $7.25M
- New ARR Target = $7.25M − ($5M × 1.10) = $7.25M − $5.5M = **$1.75M**
- The $0.5M in expansion reduces the Sales burden from $2.25M to $1.75M

**Common errors:**
- Using simple growth math when NRR is known — this understates or overstates the Sales target
- Treating the NRR adjustment as theoretical — it is the actual demand signal for pipeline and AE capacity

---

#### NRR — Net Revenue Retention

**Definition:** The percentage of ARR retained from a cohort of existing customers over a period, including expansion, downsell, and churn. Measures the net revenue motion of the installed base.

**Formula:**
```
NRR = (Beginning ARR + Expansion ARR − Churned ARR − Downsell ARR) ÷ Beginning ARR
```
Expressed as a percentage (e.g., 105%).

**Inputs:** Beginning period ARR, expansion ARR added, churned ARR lost, downsell ARR lost — all from the same cohort

**Units:** Percentage

**Interpretation:**
- NRR > 100%: The installed base is growing. Existing customers expand faster than others churn or downgrade.
- NRR = 100%: Perfect retention — expansion exactly offsets churn. No net movement.
- NRR < 100%: The installed base is shrinking. Churn and downsell exceed expansion.
- NRR 101–109% (2024 private SaaS median): Barely positive. Expansion engine barely covers churn.
- NRR 120%+: Expansion-dominant; world-class.

**Critical limitation:** NRR is a single number that hides four independent revenue motions. Two companies can report identical NRR while operating in completely different risk environments (see GRR vs. NRR interaction below). Always decompose.

**Common errors:**
- Treating NRR as a current signal — it is a 12–24 month lagging verdict on decisions already made
- Using NRR as the sole retention metric — it can show 101% while gross churn is 14% and expansion is 15%, masking the fragility
- Confusing NRR with GRR — NRR includes expansion; GRR does not

---

#### GRR — Gross Revenue Retention

**Definition:** The percentage of ARR retained from a cohort of existing customers over a period, counting only retention — not expansion. Measures the pure retention floor before any upsell or cross-sell benefit.

**Formula:**
```
GRR = (Beginning ARR − Churned ARR − Downsell ARR) ÷ Beginning ARR
```
Expressed as a percentage. GRR is always ≤ 100%; it cannot exceed 100% because it excludes expansion.

**Inputs:** Beginning period ARR, churned ARR, downsell ARR

**Units:** Percentage

**Interpretation:**
- GRR measures the stability of the base. It is what remains if the expansion engine stops entirely.
- GRR 90–95%: Healthy for enterprise SaaS
- GRR 86–90%: Median private SaaS (KBCM 2024–2025)
- GRR < 85%: High structural risk; revenue base is eroding even before churn is visible in NRR
- GRR floor insight: At 14% gross churn, GRR is approximately 86% — a $30M ARR company destroys $4.2M annually before expansion is counted

**Common errors:**
- Combining downsell and churn into a single "loss" figure — this makes it impossible to diagnose the cause
- Reporting only NRR to the board — GRR tells the structural health story NRR obscures

---

#### Gross Dollar Churn

**Definition:** The ARR lost in a period from customers who fully canceled their subscriptions, expressed as a percentage of beginning ARR.

**Formula:**
```
Gross Dollar Churn Rate = Churned ARR ÷ Beginning ARR
```

**Inputs:** ARR from accounts that fully canceled, beginning period ARR

**Units:** Percentage (e.g., 14%)

**Interpretation:**
- The KBCM four-year floor: gross dollar churn has never fallen below 11% in any private SaaS survey year (2021–2024). This is the structural constant of SaaS economics.
- 14% gross churn at $30M ARR = $4.2M destroyed annually before any growth is attempted
- At 37-month CAC payback, 14% annual churn means approximately 31–37% of new customers churn before the company recovers acquisition cost

**Differs from:** Logo churn (counts of customers, not dollar value); downsell (customers who reduce but don't cancel)

---

#### Downsell ARR

**Definition:** ARR lost in a period from customers who reduced their subscription value but did not cancel entirely.

**Formula:**
```
Downsell Rate = Downsell ARR ÷ Beginning ARR
```

**Inputs:** ARR delta from accounts that decreased spend without canceling

**Units:** Dollar amount or percentage

**Interpretation:**
- 32–37% of all revenue loss in the median private SaaS company is downsell, not churn (KBCM 2024–2025)
- For low-growth companies (<10% growth), downsell is 59% of revenue loss — the majority cause
- Causal direction: downsell causes low growth, not the reverse (KBCM commentary)
- Downsell is invisible in combined GRR/NRR reporting — must be separated

---

#### Expansion ARR

**Definition:** ARR added in a period from existing customers through upsell, cross-sell, or seat/usage expansion.

**Formula:**
```
Expansion Rate = Expansion ARR ÷ Beginning ARR
Expansion % of New ARR = Expansion ARR ÷ Total New ARR (expansion + new logo)
```

**Units:** Dollar amount or percentage

**Interpretation:**
- 2022 peak: 59% of new ARR came from expansion (expansion-dominant growth)
- 2024 reversal: 48% from expansion, 52% from new logo (back to new-logo-dominant)
- Expansion-to-churn ratio: how much expansion coverage exists over gross churn
  - 2021: 1.6x (expansion overwhelmed churn)
  - 2024: 1.07x (barely covers churn — fragile)

---

### Unit Economics Metrics

---

#### CAC — Customer Acquisition Cost

**Definition:** The fully-loaded sales and marketing cost to acquire one new customer.

**Formula:**
```
CAC = (Sales + Marketing Spend in Period) ÷ New Customers Acquired in Period
```

Also expressed as a **CAC Ratio** ($S&M per $1 of new ARR):
```
New Customer CAC Ratio = S&M Spend ÷ New ARR from New Customers
Expansion CAC Ratio    = S&M Spend ÷ Expansion ARR
```

**Inputs:** Sales spend, marketing spend, new customer count

**Units:** Dollar per customer (CAC) or dollar per dollar of ARR (CAC ratio)

**Benchmarks:**
- New customer CAC ratio: $1.78 median (KBCM 2022)
- Expansion CAC ratio: $0.61 median (KBCM 2022) — 2.9x more efficient than new logo
- Blended CAC payback: 24 months median
- New-only CAC payback: 37 months median (worsened from 31 months in 2022)

**Common errors:**
- Using blended CAC payback in growth models — it includes cheap expansion that subsidizes expensive new logos; use new-only for acquisition planning
- Not separating new logo from expansion CAC — the 2.9x efficiency gap is decisive for capital allocation

---

#### CAC Payback Period

**Definition:** The number of months required to recover the cost of acquiring a customer from their recurring revenue contribution.

**Formula:**
```
CAC Payback (months) = CAC ÷ (ACV × Gross Margin %)
```

Or using the CAC ratio:
```
CAC Payback (months) = New Customer CAC Ratio × 12
```
(Because if CAC ratio = $1.78 per $1 ARR, payback = 1.78 years = ~21 months at 100% GM; adjust for GM)

**Inputs:** CAC (or CAC ratio), ACV, Gross Margin %

**Units:** Months

**Interpretation:**
- Industry best practice: ≤18 months
- KBCM median 2024: 37 months new-only; 24 months blended
- At 37-month payback + 14% annual churn: P(churn before payback) = 1 − (1 − 0.14)^3 ≈ 36% — approximately 1 in 3 new customers churns before CAC payback

**Probability of pre-payback churn formula:**
```
P(churn before payback) = 1 − (1 − Annual Churn Rate)^(Payback Period in Years)
```

---

#### LTV — Customer Lifetime Value

**Definition:** The expected total revenue (or contribution margin) from a customer over their lifetime with the company.

**Formula:**
```
Customer Lifetime = 1 ÷ Annual Gross Churn Rate
LTV (revenue)    = ACV × Customer Lifetime
LTV (margin)     = (ACV × Gross Margin %) ÷ Annual Gross Churn Rate
```

The margin form is more useful for investment decisions:
```
LTV = (ACV × Gross Margin %) ÷ Gross Churn Rate
```

**Inputs:** ACV, Gross Margin %, Annual Gross Churn Rate

**Units:** Dollar amount

**Sensitivity:** Churn is in the denominator — a multiplicative effect.
- LTV at 14% churn, $40K ACV, 75% GM: ($40K × 0.75) ÷ 0.14 = **$214,286**
- LTV at 7% churn, same: ($40K × 0.75) ÷ 0.07 = **$428,571** — doubled by halving churn

---

#### LTV:CAC Ratio

**Definition:** The ratio of customer lifetime value to acquisition cost. The primary unit economics health metric for SaaS.

**Formula:**
```
LTV:CAC = LTV ÷ CAC
```

**Units:** Multiple (e.g., 3.1x)

**Interpretation:**
- >3x: Healthy — generating strong return on customer acquisition
- 1–3x: Marginal — acceptable early-stage but unsustainable at scale
- <1x: Value-destructive — costs more to acquire customers than they generate

**Benchmarks:**
- Overall private SaaS median: 3.0–4.0x
- Enterprise: 5.0–10.0x
- SMB: 1.5–2.5x (high churn compresses LTV)

---

#### Net Magic Number

**Definition:** The efficiency of S&M investment in generating net new recurring revenue. Measures how much net ARR is produced per dollar of S&M spend.

**Formula:**
```
Net Magic Number = (Net New ARR in Period × 4) ÷ S&M Spend Prior Period
```
(The ×4 annualizes a quarterly net new ARR figure.)

**Inputs:** Net new ARR (new logo + expansion − churn − downsell), prior-period S&M spend

**Units:** Ratio (e.g., 0.50 = $0.50 net ARR per $1 S&M)

**Interpretation:**
- >1.0: Excellent — generating more ARR than S&M costs
- 0.75–1.0: Good
- 0.5–0.75: Acceptable
- <0.5: Concerning — capital efficiency is low
- KBCM median: **0.50 — unchanged for four consecutive survey years (2022–2025E)**

**Gross Magic Number:**
```
Gross Magic Number = (Gross New ARR in Period × 4) ÷ S&M Spend Prior Period
```
The difference between gross and net magic number = the churn tax.

---

#### Churn Tax

**Definition:** The fraction of S&M investment consumed by replacing churned revenue rather than generating net growth.

**Formula:**
```
Churn Tax Rate = (Gross Magic Number − Net Magic Number) ÷ Gross Magic Number
```

**Alternative expression:**
```
Churn Tax (%) = (Gross MN − Net MN) ÷ Gross MN × 100
```

**Inputs:** Gross Magic Number, Net Magic Number

**Units:** Percentage

**Interpretation:**
- KBCM 2022–2025: Churn Tax = 22–29% of S&M spend
- For a company spending $8.7M on S&M: approximately $1.9–2.5M is consumed replacing churn annually — generating zero net growth
- Reducing churn from 14% to 7%: Churn Tax drops from ~22% to ~11%, effectively freeing $1.9M in S&M budget for net growth without increasing spend

---

#### Burn Multiple

**Definition:** The ratio of cash burned to net new ARR generated. Measures capital efficiency of growth.

**Formula:**
```
Burn Multiple = Net Burn ÷ Net New ARR
```

**Inputs:** Net burn (operating cash outflow minus inflow), net new ARR added in same period

**Units:** Multiple

**Interpretation:**
- <1.0x: Excellent — more ARR created than cash burned
- 1.0–1.5x: Good
- 1.5–2.0x: Acceptable for growth stage
- 2.0–3.0x: Concerning
- >3.0x: Unsustainable

---

#### Rule of 40

**Definition:** The sum of revenue growth rate and EBITDA margin. A combined profitability-and-growth health indicator for SaaS.

**Formula:**
```
Rule of 40 = Revenue Growth Rate (%) + EBITDA Margin (%)
```

**Inputs:** YoY revenue growth rate, EBITDA as % of revenue

**Units:** Percentage sum (target: ≥40)

**Interpretation:**
- ≥40: Healthy balance of growth and profitability
- <40: Underperforming on the combined metric
- KBCM median 2024: +6% (improved from −14% in 2022 through cost-cutting)
- But: % of companies achieving ≥40 declined from 11% (2022) to 5% (2024) — improvement is concentrated in a small elite

---

### GTM Capacity Metrics

---

#### Effective AE Capacity

**Definition:** The realistic annual new ARR a single AE is expected to close, accounting for typical quota attainment.

**Formula:**
```
Effective AE Capacity = AE Quota × AE Attainment Rate
```

**Inputs:** Annual new ARR quota, expected attainment rate (as decimal, e.g., 0.75)

**Units:** Dollar amount per AE per year

**Example:** $800K quota × 75% attainment = **$600K effective capacity**

**Note:** Use planning attainment (75%) for forward headcount models. Actual median attainment is 55–65% (KBCM). The gap between planning and actual attainment is structural.

---

#### AEs Required

**Definition:** The number of fully-ramped AEs needed to close the New ARR Target.

**Formula:**
```
AEs Required = New ARR Target ÷ Effective AE Capacity
(Round up to next whole number)
```

**Inputs:** New ARR Target, Effective AE Capacity

**Units:** Count (AEs)

---

#### SDRs Required

**Definition:** The number of SDRs needed to support the AE count based on the stated motion and SDR:AE ratio.

**Formula:**
```
SDRs Required = AEs Required × SDRs per AE
             = AEs Required ÷ AEs per SDR
```

**Inputs:** AEs Required, SDR:AE ratio (or AE:SDR ratio)

**Units:** Count (SDRs)

---

#### CSMs Required

**Definition:** The number of Customer Success Managers needed to cover the post-sale customer base at the stated service model.

**Formula (ARR-based):**
```
CSMs Required = Total Managed ARR ÷ ARR per CSM Target
```
Where Total Managed ARR = Current ARR + New ARR Target (the full ARR at end of period)

**Formula (account-based):**
```
CSMs Required = Total Accounts ÷ Accounts per CSM Target
```
Where Total Accounts = Current Customers + New Customers from AEs
New Customers from AEs ≈ New ARR Target ÷ Average Deal ACV (if ACV known)

**Inputs:** Target ARR or total accounts, ARR per CSM or accounts per CSM target

**Units:** Count (CSMs)

---

#### Max Supported ARR

**Definition:** The maximum ARR the current CS team can support without breaching the stated service model.

**Formula:**
```
Max Supported ARR = Current CSM Count × ARR per CSM Target
```

**Inputs:** Current CSM count, ARR per CSM target (benchmark or user-defined)

**Units:** Dollar amount

**Interpretation:** If Max Supported ARR < Current ARR, CS is already over capacity — the constraint fires before any new growth is modeled.

---

#### Max Incremental ARR

**Definition:** The additional ARR that can be added before the CS team reaches its capacity ceiling.

**Formula:**
```
Max Incremental ARR = Max Supported ARR − Current ARR
```

**Inputs:** Max Supported ARR, Current ARR

**Units:** Dollar amount (positive = headroom; negative = already over capacity)

---

#### CS Headroom %

**Definition:** The percentage of current ARR that can be added before CS hits its capacity ceiling.

**Formula:**
```
CS Headroom % = (Max Supported ARR − Current ARR) ÷ Current ARR × 100
```

**Inputs:** Max Supported ARR, Current ARR

**Units:** Percentage

**Interpretation:**
- >30%: Strong headroom — CS can absorb meaningful growth without new hires
- 10–30%: Limited headroom — monitor closely; hire timeline depends on sales cycle length
- <10%: Near ceiling — hire CSMs now; AE hiring will breach capacity imminently
- Negative: Already over capacity — CS constraint is live

---

#### Max AEs CS Can Support

**Definition:** The maximum number of AEs the CS team can support given its current capacity ceiling.

**Formula:**
```
Max AEs CS Can Support = Max Incremental ARR ÷ Effective AE Capacity
```

**Inputs:** Max Incremental ARR, Effective AE Capacity

**Units:** Count (AEs)

**Interpretation:** If Max AEs CS Can Support < AEs Required (from revenue model), CS is the binding constraint on AE hiring. Adding AEs beyond this number generates closed-won accounts CS cannot properly serve.

---

#### AE:CSM Ratio

**Definition:** The ratio of Account Executives to Customer Success Managers. A structural proxy for whether Sales and CS headcount are balanced.

**Formula:**
```
AE:CSM Ratio = AE Count ÷ CSM Count
```

**Inputs:** AE count, CSM count

**Units:** Ratio (e.g., 2:1 = 2 AEs per CSM)

**Benchmarks (as guide only — motion-dependent):**
- Enterprise high-touch: 1:1
- Mid-market high-touch: 2:1
- Mid-market tech-touch: 3–4:1
- SMB scaled: 5–8+:1

---

### Pipeline Metrics

---

#### Pipeline Coverage Ratio

**Definition:** The ratio of total pipeline value to the new ARR target (or quota). Measures whether enough opportunity exists to close the required revenue.

**Formula:**
```
Pipeline Coverage Ratio = Total Pipeline Value ÷ New ARR Target
```

**Inputs:** Total pipeline value (all qualified opportunities), New ARR Target

**Units:** Multiple (e.g., 3.2x)

---

#### Required Coverage Ratio

**Definition:** The pipeline coverage multiple needed to reliably close the New ARR Target, given the win rate.

**Formula:**
```
Required Coverage Ratio = 1 ÷ Win Rate
```

**Examples:**
- 25% win rate → Required Coverage = 1 ÷ 0.25 = **4x**
- 33% win rate → Required Coverage = 1 ÷ 0.33 = **3x**
- 20% win rate → Required Coverage = 1 ÷ 0.20 = **5x**

**Important:** The 3x "rule" is a legacy heuristic. Required coverage is a function of win rate. At 20% win rate, 3x coverage means the team is structurally short by 2x.

---

#### Pipeline Gap

**Definition:** The difference between the pipeline needed (Pipeline Target) and current pipeline.

**Formula:**
```
Pipeline Target  = New ARR Target × Required Coverage Ratio
Pipeline Gap     = Pipeline Target − Current Pipeline Value
```

**Units:** Dollar amount (negative = gap/shortfall; positive = surplus)

---

#### Pipeline Coverage Signals

| Coverage Level | Signal Label | Interpretation |
|---------------|-------------|----------------|
| Below 2x | CRITICAL | Insufficient pipeline to close quota even at median attainment |
| 2x–3x | AT-RISK | Dependent on everything closing; no buffer for slippage |
| 3x–5x | HEALTHY | Standard range for a mixed inbound/outbound motion |
| Above 5x | INSPECT | Possible quality issue — high volume of low-quality opportunities masking real coverage |

---

#### Win Rate

**Definition:** The percentage of qualified sales opportunities that close as won. Denominator for required pipeline coverage.

**Formula:**
```
Win Rate = Closed-Won ARR ÷ Total Qualified Pipeline Entering the Period
```

**Inputs:** Closed-won deals, qualified pipeline entering the period

**Units:** Percentage

**Default:** 25% (typical B2B SaaS; validate against CRM actuals before using in planning)

---

#### Lead Sufficiency

**Definition:** Whether the SDR team and marketing are generating sufficient pipeline to support the AE count.

**Derived from:**
```
Required Opportunities = Pipeline Target ÷ Average Deal ACV
SDR Capacity (opps generated) = SDR Count × Monthly Opps per SDR × Sales Cycle Months
Lead Volume Signal: fire when SDR capacity < Required Opportunities
```

**Not a direct formula input** — inferred from comparing pipeline coverage to SDR headcount ratios.

---

### Support Sizing Metric

---

#### Support FTE Required

**Definition:** The number of support staff needed to handle the ticket load from the current and projected customer base.

**Formula:**
```
Monthly Ticket Load = Total Customers × Tickets per Customer per Month
Support FTE = Monthly Ticket Load ÷ Tickets per Support FTE per Month
```

**Inputs:** Customer count, tickets per customer per month, tickets per FTE per month

**Units:** FTE count

**Note:** This is modeled only when the user provides ticket volume data. Not a default output.

---

## SECTION 2 — Formula Reference (Execution Order)

Full calculation sequence in the order the skill executes them.

### Phase 1: Revenue Model

```
Step 1.1 — Target ARR
  If NRR provided:
    Target ARR = Current ARR × (1 + Target Growth %)
    New ARR Target = Target ARR − (Current ARR × NRR)
  Else:
    New ARR Target = Current ARR × Target Growth %

  Note: NRR > 1.0 reduces new-logo demand
        NRR < 1.0 increases new-logo demand
        NRR = 1.0 has no effect
```

### Phase 2: AE-Anchored Headcount (Revenue → Headcount)

```
Step 2.1 — Effective AE Capacity
  Effective AE Capacity = AE Quota × AE Attainment Rate

Step 2.2 — AEs Required
  AEs Required = CEILING(New ARR Target ÷ Effective AE Capacity)

Step 2.3 — SDRs Required
  SDRs Required = CEILING(AEs Required × SDRs per AE)
               or CEILING(AEs Required ÷ AEs per SDR)

Step 2.4 — CSMs Required (forward from AE output)
  If ARR-based:
    Total Managed ARR = Current ARR + New ARR Target
    CSMs Required = CEILING(Total Managed ARR ÷ ARR per CSM)
  If Account-based:
    New Customers = New ARR Target ÷ Avg Deal ACV   (if ACV known)
    Total Accounts = Current Customers + New Customers
    CSMs Required = CEILING(Total Accounts ÷ Accounts per CSM)

Step 2.5 — Support FTE Required (if ticket data provided)
  Monthly Ticket Load = Total Customers × Tickets per Customer per Month
  Support FTE = CEILING(Monthly Ticket Load ÷ Tickets per Support FTE per Month)
```

### Phase 3: CS-Anchored Reverse (Headcount → Max ARR)

```
Step 3.1 — CS Capacity Ceiling
  Max Supported ARR = Current CSM Count × ARR per CSM

Step 3.2 — CS Headroom
  Max Incremental ARR = Max Supported ARR − Current ARR
  CS Headroom % = Max Incremental ARR ÷ Current ARR × 100

Step 3.3 — CS Constraint on AE Hiring
  Max AEs CS Can Support = Max Incremental ARR ÷ Effective AE Capacity
  (Negative Max Incremental ARR → CS already over capacity → signal fires immediately)

Step 3.4 — Constraint Check
  If Max AEs CS Can Support < AEs Required (from Phase 2):
    → CS is the binding constraint
    → CS_UNDER_CAPACITY signal HIGH severity
  Else:
    → CS has headroom
    → Note number of additional AEs supportable before ceiling
```

### Phase 4: Pipeline Coverage Check

```
Step 4.1 — Required Coverage
  Required Coverage = 1 ÷ Win Rate
  (Not a universal 3x — always derive from win rate)

Step 4.2 — Pipeline Target
  Pipeline Target = New ARR Target × Required Coverage

Step 4.3 — Current Coverage
  Current Coverage Ratio = Current Pipeline Value ÷ New ARR Target

Step 4.4 — Pipeline Gap
  Pipeline Gap = Pipeline Target − Current Pipeline Value
  (Negative = shortfall; positive = surplus)

Step 4.5 — Coverage Signal
  < 2x → CRITICAL
  2x–3x → AT-RISK
  3x–5x → HEALTHY
  > 5x → INSPECT
```

### Phase 5: Efficiency Metrics (if inputs provided)

```
Step 5.1 — Magic Numbers
  Gross Magic Number = (Gross New ARR × 4) ÷ Prior-Period S&M Spend
  Net Magic Number   = (Net New ARR × 4) ÷ Prior-Period S&M Spend
  Churn Tax Rate     = (Gross MN − Net MN) ÷ Gross MN × 100

Step 5.2 — LTV
  Customer Lifetime  = 1 ÷ Annual Gross Churn Rate
  LTV                = (ACV × Gross Margin %) ÷ Annual Gross Churn Rate

Step 5.3 — CAC Payback
  CAC Payback (mo)   = CAC ÷ (ACV × Gross Margin %)
  Pre-Payback Churn  = 1 − (1 − Annual Churn Rate)^(Payback Years)

Step 5.4 — LTV:CAC
  LTV:CAC = LTV ÷ CAC
```

### Phase 6: Imbalance Signals (All Run After Each Other)

```
Signal 1 — CS_UNDER_CAPACITY
  Fire if:
    ARR per implied CSM > High benchmark for segment   OR
    AE:CSM ratio > 2× segment benchmark               OR
    CSMs Required > Current CSM Count + 1             OR
    CS Headroom % < 10%
  Severity: HIGH if AE:CSM > 3× benchmark; MEDIUM otherwise

Signal 2 — CS_OVER_CAPACITY
  Fire if:
    Implied ARR per CSM < Low benchmark by >25%   OR
    AE:CSM < 0.5× benchmark
  Severity: MEDIUM

Signal 3 — SALES_OVER_CAPACITY
  Fire if:
    Pipeline Coverage < 3× (when Required Coverage ≥ 3×)  OR
    AE Count > Max AEs CS Can Support
  Severity: HIGH if coverage < 2×; MEDIUM if 2×–3×

Signal 4 — SALES_UNDER_CAPACITY
  Fire if:
    AEs Required > Current AE Count + 1                   OR
    New ARR Capacity (current AEs) < New ARR Target × 85% OR
    Pipeline Coverage > 5× with high deal quality stated
  Severity: HIGH if capacity gap >20%; MEDIUM otherwise

Signal 5 — LEAD_VOLUME_INSUFFICIENT
  Fire if:
    Pipeline per SDR × SDR Count < Pipeline Target         OR
    Coverage below required AND SDR count is at benchmark
  Severity: HIGH if coverage < 2×

Rule: Every signal that fires must have at least one remediation action.
Rule: Signals are ranked by severity — HIGH before MEDIUM in the output.
```

---

## SECTION 3 — Glossary

Terms are defined as used in this skill and benchmark library. Where terms have different meanings in other contexts, the skill-specific meaning is noted.

---

**ACV — Annual Contract Value**
The annualized value of a single customer contract. For multi-year deals, ACV is the per-year value, not the total contract value (TCV). Used for pipeline modeling (Pipeline Target ÷ ACV = required opportunities) and CSM account-load calculations.

---

**Accounts per CSM**
The number of customer accounts assigned to a single CSM. Used in account-based CSM sizing. Varies by ACV band: enterprise CSMs typically hold 10–15 accounts; SMB CSMs may hold 100–200+.

---

**AE — Account Executive**
A quota-carrying sales representative responsible for closing new logo or expansion deals. In this skill, AE refers primarily to new-logo closing roles. Excludes SDRs (who set meetings) and CSMs (who manage post-sale relationships).

---

**AE-Anchored Model**
The primary calculation path: start from revenue targets, derive AE headcount, then derive SDR, CSM, and support headcount. Runs from the revenue target down to headcount requirements.

---

**AE:CSM Ratio**
The ratio of Account Executives to Customer Success Managers in a GTM organization. Used to detect structural imbalance between the sales rate (AEs closing new accounts) and the CS absorption rate (CSMs servicing those accounts). A high ratio signals CS under-capacity.

---

**Attainment Rate**
The percentage of quota actually achieved by AEs in a period. Differs from planning rate (75–80%, used in forward models) and actual market median (55–65%, KBCM). Using planning rate for models; noting the gap.

---

**Binding Constraint**
The function or resource that limits revenue growth before any other. In this skill, CS capacity is frequently the binding constraint — CS cannot absorb the accounts Sales is closing, creating a sequential bottleneck. Identify the binding constraint before recommending headcount changes.

---

**Blended CAC Payback**
CAC payback calculated using total S&M spend divided across all new and expansion ARR. Lower than new-only payback because cheap expansion subsidizes expensive new logo acquisition. Can be misleading — use new-only payback for acquisition planning.

---

**Burn Multiple**
Net cash burned ÷ net new ARR. Measures capital efficiency of growth. Different from CAC payback (which is customer-level) — burn multiple is company-level.

---

**CAC Ratio**
S&M dollars spent per $1 of ARR generated. A rate, not an absolute cost. New customer CAC ratio median: $1.78. Expansion CAC ratio median: $0.61 (2.9× more efficient).

---

**Churn Floor**
The minimum gross churn rate observed in private SaaS benchmarks. KBCM four-year finding: gross dollar churn has never fallen below 11% in any survey year (2021–2024). Represents a structural baseline that CS, product, and pricing interventions have not broken below at the industry median.

---

**Churn Tax**
The fraction of S&M investment consumed by replacing churned revenue rather than generating net growth. (Gross Magic Number − Net Magic Number) ÷ Gross Magic Number. KBCM median: 22–29% of S&M consumed by churn replacement annually.

---

**Closed-Won**
A sales opportunity that resulted in a signed contract and new ARR. The event that triggers the need for CS onboarding capacity.

---

**CS Capacity Ceiling**
The maximum ARR a CS team can support given current headcount and the target ARR-per-CSM or accounts-per-CSM ratio. When Current ARR exceeds this ceiling, CS_UNDER_CAPACITY fires immediately.

---

**CS-Anchored Model**
The reverse calculation path: start from current CSM count, derive maximum supportable ARR, surface the CS ceiling as a constraint on AE hiring and growth plans.

---

**CSM — Customer Success Manager**
A post-sale role responsible for ensuring customers achieve their desired outcomes, driving renewal, and identifying expansion opportunities. This skill uses "CSM" for all CS delivery roles regardless of exact title. Distinct from support (reactive ticket handling), professional services (project-based delivery), and renewals specialists.

---

**Downsell**
Revenue lost when a customer reduces their subscription value without canceling. Distinct from churn (full cancellation). Frequently combined with churn in GRR reporting, making it invisible as a separate signal. KBCM: 32–37% of all revenue loss at median companies is downsell, not churn.

---

**Effective AE Capacity**
AE Quota × AE Attainment Rate. The realistic new ARR a single AE is expected to close per year accounting for typical quota achievement gaps.

---

**Enterprise**
Segment definition used in this skill: ACV range $100K–$500K, field sales motion, multi-stakeholder buying process, typical sales cycle 3–9 months. Benchmarks (ARR per CSM, NRR targets, churn rates) differ materially from mid-market and SMB — never apply enterprise benchmarks to SMB or vice versa.

---

**Expansion ARR**
Additional ARR generated from existing customers through upsell (customers buying more of the same), cross-sell (buying additional products), or usage/seat growth. Does not include new logos.

---

**Expansion-to-Churn Ratio**
Expansion ARR ÷ Gross Churned ARR. Measures how much expansion coverage exists over gross churn. At >1.0, expansion is absorbing churn; at 1.07x (2024 median), expansion barely covers churn — the engine is fragile.

---

**GRR — Gross Revenue Retention**
Retention rate excluding expansion. The floor — what remains if the expansion engine stops. GRR ≤ 100% always. Measures the structural health of the installed base. See full definition in Metrics Catalog.

---

**Gross Magic Number**
(Gross New ARR × 4) ÷ Prior-Period S&M Spend. Like Net Magic Number but using gross new ARR before subtracting churn. The difference between gross and net magic number = the churn tax.

---

**GTM Motion**
The primary go-to-market approach: Outbound-Heavy (SDR-led prospecting), Mixed (inbound + outbound), Inbound-Dominant (marketing-led), or PLG (product-led growth). Determines SDR:AE ratio defaults and affects churn benchmarks (field vs. inside sales).

---

**High-Touch**
A CS delivery model where CSMs engage proactively and regularly with each customer. Typical for enterprise and strategic accounts. Requires lower ARR per CSM (more CSM time per customer) and lower accounts per CSM.

---

**Imbalance Signal**
A diagnostic flag indicating a structural mismatch in the GTM organization — too many or too few of a specific role relative to demand, capacity, or volume. Five signal types: CS_UNDER_CAPACITY, CS_OVER_CAPACITY, SALES_OVER_CAPACITY, SALES_UNDER_CAPACITY, LEAD_VOLUME_INSUFFICIENT.

---

**Inbound-Dominant**
A sales motion where the majority of pipeline originates from marketing-generated leads rather than SDR outbound prospecting. Associated with higher AE:SDR ratio (fewer SDRs needed per AE) and typically lower ACV.

---

**Lead Volume**
The number of marketing-qualified or sales-qualified leads entering the top of the funnel. Distinct from pipeline (leads that have been converted to qualified opportunities). Insufficient lead volume drives LEAD_VOLUME_INSUFFICIENT signal even when SDR/AE headcount is correct.

---

**Logo Churn**
Customer count attrition — the number of customers who canceled, regardless of their ARR value. Different from gross dollar churn (which weights by ARR value). A $200K customer churning and a $5K customer churning are equal in logo churn but very different in dollar churn.

---

**LTV — Customer Lifetime Value**
(ACV × Gross Margin %) ÷ Annual Gross Churn Rate. The margin-adjusted revenue expected over a customer's lifetime. The numerator in the LTV:CAC ratio. Highly sensitive to churn rate (churn is in the denominator — multiplicative effect).

---

**Magic Number**
GTM efficiency metric. Net new ARR per dollar of S&M spend (annualized). Stuck at 0.50 for four consecutive KBCM survey years — meaning $0.50 in net ARR per $1 of S&M. Industry has not improved this ratio despite significant operational changes.

---

**Max AEs CS Can Support**
The AE count whose closed-won output can be absorbed by the current CS team without exceeding the CS capacity ceiling. Used to identify when CS is the binding constraint on AE hiring.

---

**Max Incremental ARR**
Max Supported ARR − Current ARR. The additional ARR that can be added before CS hits its capacity ceiling. Negative when CS is already over capacity.

---

**Max Supported ARR**
Current CSM Count × ARR per CSM. The maximum ARR the CS team can carry at the current headcount and target service ratio.

---

**Mid-Market**
Segment definition used in this skill: ACV range $25K–$100K, mixed inside + field sales motion, typical sales cycle 45–90 days. The "sweet spot" segment for most private SaaS companies.

---

**Net Magic Number**
(Net New ARR × 4) ÷ Prior-Period S&M Spend. Measures return on S&M investment after churn. See Metrics Catalog for full definition.

---

**New ARR**
ARR generated from customers who had no prior relationship with the company (new logos). Distinct from expansion ARR. The primary Sales contribution metric.

---

**New-Only CAC Payback**
CAC payback calculated using only S&M spend allocated to new logo acquisition and only new customer ARR. More conservative than blended; represents the true economics of acquiring a new customer. KBCM 2025 median: 37 months.

---

**NRR — Net Revenue Retention**
The net ARR motion of the installed base. Includes expansion, churn, and downsell. Can exceed 100%. See full definition in Metrics Catalog.

---

**Outbound-Heavy**
A sales motion driven primarily by SDR prospecting and direct outreach. Higher SDR investment relative to AEs. Typically associated with higher ACV enterprise deals.

---

**Pipeline**
The total value of qualified sales opportunities at a given point in time. Measured against the New ARR Target to compute pipeline coverage. "Qualified" means the opportunity has been validated by some sales qualification process — not all inquiries count.

---

**Pipeline Coverage Ratio**
Total Pipeline Value ÷ New ARR Target. Measures sufficiency of pipeline relative to targets. Required coverage = 1 ÷ win rate (not a universal 3x).

---

**PLG — Product-Led Growth**
A growth motion where the product itself drives user acquisition, expansion, and retention — typically through free tiers, freemium, or viral mechanics. Associated with different SDR:AE ratios and CS models (often digital-first rather than high-touch).

---

**Pod Model**
A GTM team structure where AE, SDR, and CSM are grouped together as a recurring revenue unit. This skill's architecture derives SDR and CSM headcount from AE count, implicitly following pod logic.

---

**Pre-Payback Churn**
The probability that a customer churns before the company recovers the CAC spent to acquire them. Formula: 1 − (1 − Annual Churn Rate)^(Payback Period in Years). At 37-month payback + 14% churn: ~36%.

---

**Professional Services (PS) Attach Rate**
PS revenue as a percentage of the initial ACV at close. Used in churn analysis — PS investment above 26% of ACV produces a documented 46% churn reduction (KBCM, non-linear threshold effect).

---

**Quota**
The annual new ARR target assigned to a fully-ramped AE. The skill uses quota as the planning input, adjusted by attainment rate to derive effective capacity.

---

**Ramp Period**
The time required for a new AE to reach full quota productivity. Typically 4–6 months for SMB/mid-market, 6–9 months for enterprise. Not modeled explicitly in this skill's calculations but affects timing of capacity additions.

---

**Required Coverage Ratio**
1 ÷ Win Rate. The pipeline multiple needed to statistically close the New ARR Target. At 25% win rate, 4x pipeline is required — not 3x.

---

**Rule of 40**
Revenue Growth % + EBITDA Margin %. Aggregate health metric. ≥40 is the target. KBCM 2024: only 5% of private SaaS companies achieve it, despite median score improvement through cost-cutting.

---

**SDR — Sales Development Representative**
A prospecting and pipeline-generation role. Qualifies leads and books meetings for AEs. This skill derives SDR count from AE count using the SDR:AE ratio.

---

**Segment**
The market tier being served: SMB, Low Mid-Market, Mid-Market, Enterprise, or Strategic. Segment determines ACV range, motion, benchmarks for AE quota, CSM ratios, NRR targets, and churn profiles. Critical to match benchmarks to segment.

---

**SMB — Small and Medium Business**
Segment definition used in this skill: ACV < $10K, typically PLG or high-velocity inbound, short sales cycle (<30 days). Highest churn (18–22%), lowest CSM account loads by cost, highest accounts per CSM.

---

**Strategic**
Segment definition used in this skill: ACV >$500K, named account coverage, executive selling, long sales cycles (6–18 months). Lowest churn (4–8%), highest service investment per customer, very low accounts per CSM (2–8).

---

**Support FTE**
Full-time equivalent support staff required to handle the reactive ticket load from the customer base. Sized from ticket volume data (customers × tickets per customer per month ÷ tickets per FTE per month). Only modeled when ticket data is provided.

---

**Tech-Touch**
A CS delivery model that uses automation, in-app messaging, and digital programs rather than dedicated human CSM time for each account. Enables higher ARR per CSM and more accounts per CSM than high-touch. Typically for SMB or long-tail accounts.

---

**TCV — Total Contract Value**
The total value of a multi-year contract. TCV = ACV × Contract Years. Do not use TCV where ACV is required.

---

**Win Rate**
The percentage of qualified sales opportunities that close as won. The denominator for Required Pipeline Coverage. KBCM/industry default: 25%; actual rates vary widely by segment, motion, and competition. Always verify against CRM actuals.

---

*unit-of-growth-calculator v1.0.0 | Metrics, Formulas, and Glossary v1.0*
*Aligned with: SKILL.md v1.0.0 | benchmark-library.md v2.0*
