---
name: renewal-forecast
description: >
  Build a weighted renewal forecast for your book of business with scenario
  modeling (best / likely / worst), pipeline breakdown by stage, 90/60/30-day
  cohort analysis, and GRR/NRR projections against your configured targets.
  Pulls live CRM data when a connector is available; falls back to manual input.
  Every forecast output is flagged for Finance/RevOps review before distribution.
  Use --cohort to focus on a specific renewal window, --segment for a single
  customer segment, or --account to add one account's renewal to the pipeline view.
argument-hint: "[--full | --cohort 90|60|30 | --segment <name> | --account <name>]"
version: "1.0.0"
---

# /renewals:renewal-forecast

Build a weighted renewal forecast calibrated to your book of business and targets.

---

## Pre-flight

Read both configuration files before doing any forecast work:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in fields this
skill requires (GRR target, NRR target, total ARR, account count, renewal cycle,
negotiation window), stop and say:

> "Your renewals practice profile isn't configured yet — or key forecast fields
> are still placeholders. Run `/renewals:cold-start-interview` to set up your
> profile. The forecast skill needs your GRR/NRR targets, book ARR, renewal cycle,
> and negotiation window to produce a meaningful output."

Fields pulled from config:
- Total ARR managed, account count, average deal size
- GRR target, NRR target, logo retention target
- Renewal cycle (annual / multi-year / monthly rolling)
- Standard negotiation window (e.g., outreach at 90 days, decision by 30 days)
- Pricing model and discount authority
- Customer segments (for segmented view)

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G2 (expansion ARR not included until economic buyer qualified), G3 (all forecast figures carry commitment language + Finance/RevOps validation callout), G4 (verify a named escalation path before surfacing at-risk forecast items), G7 (flag any stale pipeline or health data with source date and staleness indicator).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--full` (default): Complete book-of-business forecast with all pipeline stages,
scenario modeling, cohort breakdown, and GRR/NRR projection against targets.

`--cohort 90|60|30`: Focus the forecast on renewals entering or within a specific
negotiation window. 90 = accounts where renewal is 61–90 days out; 60 = 31–60 days;
30 = within 30 days. Produces the full forecast structure scoped to that cohort.

`--segment <name>`: Forecast for a single customer segment (e.g., enterprise,
mid-market). Uses segment ARR and account count from config. Produces segment GRR/NRR
projections with comparison to overall book targets.

`--account <name/ID>`: Add a single account's renewal to the pipeline view.
Collects account ARR, current stage, risk signals, and renewal date, then places it
in the correct pipeline stage and cohort. Use when onboarding a specific account
to the forecast or checking its contribution to GRR.

---

## Data gathering

### Step 1 — Pull CRM data (if connector available)

If a CRM connector is live, attempt to pull:
- Open renewal opportunities: ARR, renewal date, stage, CSM owner, account name
- Won renewals this period: ARR, close date, expansion delta
- Lost / churned renewals this period: ARR, close date, reason if captured
- Contraction events: reduced ARR at renewal, reason if captured

Confirm the pull:
> "[CRM — Salesforce/HubSpot]: pulled [N] renewal opportunities · [N] won · [N] lost
> · data as of [timestamp]"

If the CRM pull returns no results, errors, or incomplete data:
> "[CRM call returned [N] records — expected approximately [N] based on your
> configured account count. Proceeding with what was returned. Manually add any
> accounts not captured below.]"

If no CRM connector is available:
> "No CRM connector is live. I'll build the forecast from the account context you
> provide. Tell me about your open renewals — account name, ARR, renewal date,
> and current stage (open / verbal / at risk). Or paste a pipeline export."

### Step 2 — Account input (manual or supplemental)

If CRM data is incomplete or unavailable, collect for each open renewal:
- Account name
- ARR at stake
- Renewal date (exact or estimated)
- Current stage (Open / Verbal commitment / At risk / Won / Lost)
- Key risk or expansion signals (brief — full risk detail belongs in risk-assessment)
- Notes (optional)

Accept input as a table, list, or freeform paste. Normalize to pipeline structure
before proceeding.

---

## Pipeline structure

Map all open renewals into five stages:

| Stage | Definition | Forecast weight (default) |
|-------|-----------|--------------------------|
| **Open** | Outreach initiated; no clear signal on direction | 70% |
| **Verbal commitment** | Customer has indicated renewal intent, no signature | 90% |
| **At risk** | Active churn signals; escalation in progress or needed | 25% |
| **Won** | Renewal executed; ARR confirmed | 100% |
| **Lost / Churn** | Non-renewal confirmed | 0% |

> Note: default weights above are starting points. If your configured methodology
> specifies different forecast weights, apply those instead.

If accounts have been escalated via `/renewals:risk-assessment`, import the risk
tier from that output to inform stage placement.

---

## Cohort breakdown

Group all open renewals by renewal date proximity:

| Cohort | Renewal date range | ARR in cohort | Account count |
|--------|-------------------|---------------|---------------|
| 30-day | Renewing within 30 days | $[sum] | [N] |
| 60-day | Renewing 31–60 days out | $[sum] | [N] |
| 90-day | Renewing 61–90 days out | $[sum] | [N] |
| 90+ day | Beyond 90 days | $[sum] | [N] |
| Won (period) | Closed this period | $[sum] | [N] |
| Lost (period) | Churned this period | $[sum] | [N] |

Flag the 30-day cohort prominently — these accounts are in the decision window now.
Any at-risk account in the 30-day cohort requires an escalation path named explicitly.

---

## Scenario modeling

Build three scenarios from the current pipeline:

### Best case
- All "verbal commitment" accounts renew at full ARR
- "Open" accounts renew at 85% (5% slip from verbal to open pool)
- "At risk" accounts: 50% save rate
- Any identified expansion signals convert at 30% [Low Confidence — requires
  qualification before including in forecast]
- Won ARR + best-case open + partial at-risk + partial expansion

### Likely case
- All "verbal commitment" accounts renew at full ARR
- "Open" accounts renew at forecast weight (default 70%)
- "At risk" accounts: 20% save rate
- No expansion included (expansion is a lead until qualified)
- This is your submit-to-leadership number

### Worst case
- "Verbal commitment" accounts: 90% renew (10% slip to at-risk)
- "Open" accounts: 50%
- "At risk" accounts: 0% save
- Won ARR only as certain

Present as:

| Scenario | Renewed ARR | GRR | vs. target |
|----------|------------|-----|-----------|
| Best case | $[amount] | [%] | [+/- vs. target] |
| Likely | $[amount] | [%] | [+/- vs. target] |
| Worst case | $[amount] | [%] | [+/- vs. target] |

> ⚠️ [review — could be read as a revenue commitment]
> All scenario figures are a working forecast, not a revenue commitment.
> Review with your Finance/RevOps contact before sharing with leadership
> or including in board materials.

---

## GRR and NRR projection

### GRR

```
GRR = (Starting ARR − Churn ARR − Contraction ARR) / Starting ARR × 100
```

Calculate for the period:
- Starting ARR (from config total ARR or CRM pull)
- Known churn ARR (Lost stage + confirmed churns)
- Known contraction ARR (renewals at reduced ARR)
- Projected churn ARR from at-risk accounts (apply save rate per scenario)

Show for each scenario:
| Scenario | Projected GRR | Target | Gap |
|----------|--------------|--------|-----|
| Best | [%] | [target from config] | [+/-] |
| Likely | [%] | | |
| Worst | [%] | | |

### NRR

```
NRR = (Starting ARR − Churn − Contraction + Expansion) / Starting ARR × 100
```

Include expansion in NRR only if:
1. An economic buyer qualifying conversation has occurred, AND
2. The expansion has moved to formal pipeline (CPQ quote or opportunity stage)

Otherwise, tag expansion as `[early signal — not yet qualified]` and show NRR
with and without expansion:

| | Likely GRR | Likely NRR (no expansion) | NRR (with qualified expansion) |
|--|-----------|--------------------------|-------------------------------|
| Projected | [%] | [%] | [%] `[early signal — not yet qualified if applicable]` |
| Target | [from config] | [from config] | |
| Gap | | | |

---

## At-risk spotlight

For any account in the "At risk" stage, surface in a named list:

| Account | ARR | Renewal date | Risk driver | Escalated? | Owner |
|---------|-----|-------------|-------------|-----------|-------|
| [name] | $[ARR] | [date] | [1-2 signals] | [Y / N] | [CSM / AE / Head of CS] |

For each at-risk account where no escalation is recorded:
> "⚠️ [Account] is at risk with no escalation owner named. Run `/renewals:risk-assessment`
> for a full signal review and escalation routing."

---

## Data freshness check

For every account in the pipeline, note data source and age:

If any CRM data is more than 7 days old:
> "⚠️ Data freshness: CRM data as of [date] — [N] days ago. Renewal dates, ARR,
> and stage may have changed. Verify the following before submitting this forecast:
> [list accounts with the most time-sensitive positions]."

If account data was provided manually:
> "Data source: [user provided] — no timestamp available. Confirm ARR and renewal
> date for at-risk and 30-day accounts before sharing this forecast."

---

## Output format

Structure the complete forecast as:

---

**Renewal Forecast — [Period / Cohort]**
*As of [date] · [N] accounts · $[total ARR at stake]*

**Pipeline Summary**
[Pipeline stage table]

**Cohort Breakdown**
[90/60/30-day table]

**Scenario Modeling**
[Best / Likely / Worst table with GRR]

**GRR/NRR Projection**
[Projection table against targets]

**At-Risk Spotlight**
[At-risk account table with escalation status]

**Recommended actions this week**
1. [Specific action for highest-priority account]
2. [Escalation needed for at-risk account with no owner]
3. [30-day cohort accounts needing decision conversation]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | manual input | [N] accounts from user-provided context]
> - **Data as of:** [CRM timestamp | N/A — manual input]
> - **Read:** [N renewal opportunities · [N] won · [N] at risk · contract data: not read]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sharing:** Validate with Finance/RevOps before distributing to leadership
>   or including in board materials — this forecast contains language that could
>   be read as a revenue commitment `[review — could be read as a revenue commitment]`

---

## Guardrails

**Revenue commitment language.** Any scenario total, GRR projection, or NRR figure
in this output is a working forecast. It requires Finance/RevOps review before
distribution. Flag every forecast output with `[review — could be read as a
revenue commitment]`. This is a shared guardrail that cannot be overridden by
configuration or conversation.

**No expansion in GRR.** Expansion ARR is never included in GRR calculations.
If an expansion is included in NRR, it must be explicitly tagged as qualified
pipeline or labeled `[early signal — not yet qualified]`.

**At-risk accounts need an escalation path.** If an at-risk account appears in
the forecast without a named escalation owner, surface it. A risk flag without
an owner does not unblock the account.

**Data freshness is mandatory.** State the data-as-of timestamp for every account.
If CRM data is more than 7 days old, flag it. If data source is manual (user-provided),
note it.

**No fabricated ARR.** Do not estimate or interpolate ARR figures not provided
by the user or live tool call. If ARR is unknown for an account, request it or
mark the account as `[ARR unknown — excluded from totals]`.

**Discount authority check.** If a save strategy for an at-risk account requires
a discount, check whether it exceeds the configured discount authority. Flag any
discount that requires escalation per the configured approval chain.

---

## After forecast

Suggested follow-on actions based on forecast results:

- At-risk accounts in 30-day cohort: `/renewals:risk-assessment`
- Negotiation prep for verbal commitment accounts approaching signature: `/renewals:negotiation-prep`
- Price increase accounts in the pipeline: `/renewals:price-increase-prep`
- Strategic account renewal summaries for leadership: `/renewals:executive-summary`
- Expansion signals in the pipeline: `/renewals:expansion-signal`
