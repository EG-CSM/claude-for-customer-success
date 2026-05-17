---
name: sales-cs-handoff-quality-scoring
version: 1.0.0
description: "Scores each closed/won deal on five handoff dimensions (0–100). Pass threshold: 80. Below-threshold deals trigger a Linear issue assigned to the AE manager with 48-hour SLA. CS onboarding proceeds but CSM is notified of open issue. Dimensions: OCV entry referenced, trigger match, measurement source accessible, stakeholder map, risk flags documented. Triggers: 'handoff quality', 'handoff score', 'what's missing for [deal] handoff', 'CS handoff check', 'handoff completeness'."
---

# Sales-CS Handoff Quality Scoring

Objective catalog alignment check — not subjective prose quality. The pass/fail
is binary per dimension, sourced from structured fields and OCV catalog, not
a judgment call on how good the rep's notes are.

**Reference:** Handoff quality scoring rubric → `reference/revops-domain-model.md §10`
**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `ocv_catalog_path`, `linear_connected`

---

## Reasoning Protocol

1. Confirm activation — user requesting handoff check for a specific deal or recent closes
2. Read deal fields from HubSpot and OCV catalog
3. Apply G8 — only Ratified OCV entries count toward dimension 1
4. Apply G6 — data-as-of on all reads
5. Confirm Linear is connected for issue creation if below threshold
6. Apply G7 — below-threshold flags include named escalation path

---

## Five Dimensions `[revops-domain-model.md §10]`

```
D1: OCV entry referenced (20pts)
    PASS: ≥1 Ratified OCV entry linked to deal in HubSpot
    FAIL: No entry, or only Draft entries

D2: Trigger condition match (20pts)
    PASS: OCV trigger condition confirmed present in account context
    FAIL: Trigger condition not present, or not verifiable from deal data

D3: Measurement source accessible (20pts)
    PASS: The measurement source in the OCV entry is accessible to CS post-close
    FAIL: Source requires system CS doesn't have access to

D4: Stakeholder map transferred (20pts)
    PASS: Economic buyer + champion + technical contact all named and tagged
    FAIL: One or more roles missing

D5: Risk flags documented (20pts)
    PASS: Deal notes include risk flags OR explicit "none identified"
    FAIL: Field empty or not populated
```

---

## Below-Threshold Action (score < 80)

```
1. Create Linear issue:
   Title: "Handoff quality below threshold — [Account Name]"
   Assigned to: [AE manager]
   SLA: 48 hours
   Body:
     Deal: [link]  ACV: $XXXk  Close date: [date]
     Failed dimensions: [list]
     What's needed: [specific fields/actions per dimension]

2. Notify CSM:
   "Handoff for [Account] is below threshold (score: [N]/100).
   Missing: [dimensions]. Linear issue [#N] assigned to [AE manager].
   Onboarding proceeds — please flag if blockers surface."

3. Log in audit trail:
   timestamp, deal ID, score, failed dimensions, issue number, CSM notified
```

---

## Output Format

```
HANDOFF QUALITY SCORING — [Deal / Week]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

[Account A]  $XXXk  Score: 100/100  ✓ PASS
[Account B]  $XXXk  Score: 60/100   ✗ BELOW THRESHOLD
  Failed: D1 (no Ratified OCV entry), D4 (technical contact not tagged)
  Linear issue created: #[N] → [AE manager], 48h SLA
  CSM [name] notified

Weekly digest:
  Deals closed this week: [N]
  Pass (≥80): [N] (XX%)
  Below threshold: [N] (XX%)
  Avg score: [N]/100

[G7: Below-threshold escalation path: AE manager via Linear within 48h]
[G8: Only Ratified OCV entries counted toward D1]
```

---

## Guardrails

- G7: Every below-threshold flag includes named escalation path and owner
- G8: Draft OCV entries do not satisfy D1
- G6: Data-as-of required on all reads
