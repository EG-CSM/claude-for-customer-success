# renewals.downgrade-analysis

Contract contraction analysis for accounts requesting seat reduction or scope reduction. Diagnoses contraction drivers, quantifies ARR impact, and produces counter-proposal inputs for the negotiation-prep workflow. Scoped to contract contractions only — full cancellations route to renewals.churn-rca.

## Use it for

- Analyze a customer request to reduce seats, tiers, or product scope
- Quantify ARR impact of proposed contraction
- Generate counter-proposal framing for negotiation
- Identify whether contraction reflects temporary budget pressure or structural disengagement

## Don't use it for

- Full cancellations (use renewals.churn-rca)
- Active at-risk accounts not yet requesting contraction (use renewals.risk-assessment)
- Renewal forecasting (use renewals.renewal-forecast)
- Expansion or upsell opportunities

## How to trigger it

Say something like:

- "customer wants to reduce seats"
- "they're asking to downgrade"
- "contraction request"
- "scope reduction"
- "downgrade analysis"
- "they want to cut the contract"

## What you get

- Contraction analysis report (structured markdown)
- ARR impact summary (current vs. proposed)
- Counter-proposal inputs for renewals.negotiation-prep

## Prerequisites

- Domain CLAUDE.md (reads at startup; routes to cold-start-interview if missing)
- Account name or ID
- {'Current contract': 'ARR, seat count, tier, renewal date'}
- {'Requested contraction': 'seats to reduce or scope to remove'}
- {'CRM data or manual input': 'engagement history, usage data, support history'}

## Governance

- Account content is confidential — no cross-account data sharing in outputs
- CRM data older than 7 days triggers freshness warning
- ARR figures flagged as not-yet-a-revenue-commitment until signed amendment

## See also

- renewals.churn-rca
- renewals.risk-assessment
- renewals.negotiation-prep
- renewals.renewal-forecast

---

*Domain: `renewals` · Skill ID: `renewals.downgrade-analysis`*
