---
name: revenue-leakage-scanning
version: 1.0.0
description: "Identifies deal structures leaving money on the table before close: underpriced professional services, missing expansion clauses in multi-year deals, renewal terms misaligned with ARR classification, missing success milestone gates for expansion. Fires at Negotiation stage — before close locks the structure. Triggers: 'revenue leakage', 'missing expansion clause', 'mispriced services', 'deal structure review', 'are we leaving money on the table'."
---

# Revenue Leakage Scanning

Structural leakage is easier to fix before the contract is signed.
Primary detection window: Negotiation stage — before close.

**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `avg_deal_acv`, `primary_segment`

---

## Reasoning Protocol

1. Confirm activation — user reviewing deal structure for a specific deal or cohort
2. Read deal structure fields, notes, and product configuration from HubSpot
3. Identify leakage patterns — quantify estimated ARR impact where possible
4. Apply G1 — leakage analysis for finance requires qualification language
5. Surface findings before close; note if deal is already closed (post-close is lower value)

---

## Four Leakage Patterns

```
Pattern 1 — Professional services underpriced
  Signal: implementation_complexity notes suggest high effort;
          PS line item ≤25% of ACV (typical PS ratio for complexity level)
  Impact estimate: [estimated PS underprice amount]

Pattern 2 — Expansion clause missing
  Signal: multi-year contract (≥2 years) without usage-based expansion clause
          or seat-based expansion rights
  Impact: No contractual mechanism to grow ARR within the contract term

Pattern 3 — Renewal terms / ARR classification mismatch
  Signal: deal counted as New ARR but renewal terms allow flat renewal
          with no price increase clause
  Impact: ARR classification may overstate true growth quality

Pattern 4 — Success milestone gate missing
  Signal: no EBR/QBR or milestone-based check-in tied to expansion conversation
  Impact: CS has no contractual trigger for expansion motion
```

---

## Output Format

```
REVENUE LEAKAGE SCAN — [Account Name] — [Stage]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: Moderate]

Deal: [link]  ACV: $XXXk  Stage: [stage]  Close: [date]

Leakage findings:
  [Pattern type]  Estimated impact: $XXXk  Action: [specific fix before close]
  [Pattern type]  Impact: [structural]      Action: [specific fix]

No leakage patterns detected: [if clean]

Window: [deal is at Negotiation — action window is open / deal is closed — lower leverage]

[DRAFT — RevOps internal]
[G1: Leakage estimates are models. Not revenue commitments.]
```

## Guardrails

- G1: Leakage estimates require qualification when shared beyond RevOps
- Most valuable when run at Negotiation stage — flag this explicitly on closed deals
