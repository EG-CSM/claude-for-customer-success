# rev-ops.revenue-leakage-scanning

Identifies deal structures leaving money on the table before close. Detects four leakage patterns: underpriced professional services, missing expansion clauses in multi-year deals, renewal terms misaligned with ARR classification, and missing success milestone gates. Primary detection window is Negotiation stage — before close locks the structure.

## Use it for

- Scan a specific deal for structural revenue leakage before contract signing
- Identify missing expansion clause on multi-year deals
- Flag PS pricing against deal complexity and estimated impact

## Don't use it for

- Post-close contract renegotiation (flagged as lower-value window)
- ARR forecasting or pipeline coverage (route to relevant skills)

## How to trigger it

Say something like:

- "revenue leakage"
- "missing expansion clause"
- "mispriced services"
- "deal structure review"
- "are we leaving money on the table"

## What you get

- Leakage scan report per deal (pattern type, estimated impact, action before close)

## Prerequisites

- HubSpot deal fields, product configuration, and notes for target deal
- avg_deal_acv, primary_segment from company profile

## Governance

- G1 — leakage estimates require qualification language when shared beyond RevOps
- Most valuable at Negotiation stage — flag explicitly when run on closed deals
- Impact estimates are models, not revenue commitments

## See also

- rev-ops.non-standard-terms-detection
- rev-ops.deal-desk-workflow-management
- rev-ops.sales-cs-handoff-quality-scoring

---

*Domain: `rev-ops` · Skill ID: `rev-ops.revenue-leakage-scanning`*
