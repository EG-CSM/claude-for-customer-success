---
name: outcome-to-value-tracking
version: 1.0.0
description: "Maps each customer to their L0–L3 rubric level on their referenced OCV entries at OCV-defined verification milestones (e.g., 90-day, 180-day). Portfolio view: % at each rubric level per OCV entry. Surfaces systemic L0 persistence (>40% of accounts stuck at L0 past 90-day milestone) as a delivery pattern signal. Triggers: 'outcome tracking', 'rubric level', 'L0 L1 L2 L3', 'value realization', 'are customers achieving outcomes', 'outcome portfolio health'."
---

# Outcome-to-Value Tracking

Are customers achieving what they bought the product to do?
L0–L3 rubric level tracking per account and per OCV entry.

**Reference:** OCV catalog conventions → `reference/revops-domain-model.md §6`
**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `ocv_catalog_path`, `cs_platform_connected`

---

## Reasoning Protocol

1. Confirm activation — user asking about outcome attainment, value realization, or rubric levels
2. Check OCV catalog — required; declare fallback if absent
3. Check CS platform connector for health scores, usage trend, outcome progress notes
4. Apply G8 — only Ratified OCV entries used
5. Apply G5 — rubric level is analytical input; CS owns the response
6. Apply G6 — data-as-of on all reads

---

## Rubric Level Assessment

For each account, at each OCV-defined verification milestone:

```
Read from OCV entry:
  - Observable evidence for L0, L1, L2, L3
  - business_metric and measurement_source
  - verification_milestone schedule

Read from connectors:
  - CS health score and trend [CS Platform ✓ live]
  - Product usage trend [CS Platform ✓ live]
  - CS-documented outcome progress notes [CS Platform ✓ live]
  - CRM: EBR/QBR logged, executive sponsor activity [CRM ✓ live]

Map to rubric level using OCV evidence criteria — not inference.
```

**Portfolio analysis scope boundary:**
Analysis uses CS health scores, product usage summaries, and CS-documented
outcome progress. Feature-level product analytics are out of scope unless a
product analytics connector is configured. When deeper investigation is warranted:
"Root cause may require product usage analytics. Recommend CS + Product review."

---

## Output Formats

**Account-level:**
```
OUTCOME TRACKING — [Account Name]
[CS Platform ✓ live — as of YYYY-MM-DD] [CRM ✓ live]
[OCV catalog v[version] — Confidence: High/Moderate]

OCV-001 [Name]:
  Current rubric level: L[N] — [Label]
  Evidence: [Specific observable signals from OCV rubric — not generic]
  Milestone: [which checkpoint] | Next: [date]
  Recommended action: [if L0 or L1 and approaching next milestone]
  [G5: CS [name] owns the response plan]

[G8: Only Ratified entries assessed]
```

**Portfolio-level:**
```
OUTCOME PORTFOLIO HEALTH — [Period]
[CS Platform ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

OCV-001 [Name] — [N] accounts:
  L3: N (XX%)  L2: N (XX%)  L1: N (XX%)  L0: N (XX%)
  [⚠ L0 PATTERN if >40% at L0 past 90-day checkpoint]
    Common attributes: [segment / product tier / onboarding path]
    Signal: Delivery pattern — not account-specific. Escalate to CS + Product.

OCV-002 [Name] — [N] accounts: [same format]

Portfolio summary:
  Overall L2+ attainment: XX%
  Accounts at L0 past 90-day checkpoint: [N] — [HIGH/MODERATE concern]
```

---

## Guardrails

- G5: Rubric level assessments are analytical inputs — CS owns the response
- G8: Draft OCV entries excluded from assessment
- G6: All connector reads timestamped
- Portfolio analysis scope boundary: declare when product analytics would improve depth
