---
name: deal-classification
version: 1.0.0
description: "Independently scores each open opportunity as Commit / Best Case / Pipeline using CRM activity data — without relying on rep self-reporting. Surfaces delta vs. rep's stated forecast category when classification disagrees by more than one tier. Triggers: 'deal classification', 'classify the pipeline', 'commit vs best case', 'independent forecast', 'override rep call'."
---

# Deal Classification

Classifies open opportunities using CRM activity signals, not rep self-reporting.
Disagrees with rep calls only when evidence is clear — flags the delta, doesn't override.

**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `primary_segment`, `avg_sales_cycle_days`

---

## Reasoning Protocol

1. Confirm activation — user wants independent deal scoring or call validation
2. Check HubSpot for activity data — required for classification; declare fallback if absent
3. Apply G5 — classification is analytical input; rep and manager own the judgment
4. Apply G6 — surface data-as-of on all activity reads
5. Do not present classification as override — present as independent signal

---

## Scoring Dimensions (20 points each, total 100)

| Dimension | Commit signal | Best Case signal | Pipeline signal |
|-----------|--------------|-----------------|----------------|
| **Activity recency** | Contact in ≤7 days | Contact in 8–21 days | No contact >21 days |
| **Stakeholder coverage** | EB + Champion + TC all engaged | 2 of 3 engaged | 1 or fewer engaged |
| **Stage progression rate** | On or ahead of historical avg | 0–25% behind avg | >25% behind avg |
| **Competitive signal** | No active competitor / counter-play logged | Competitor mentioned, response logged | Competitor active, no response |
| **Rep forecast accuracy** | Rep's trailing commit accuracy ≥70% | 50–70% | <50% |

**Classification:**
- 80–100 → Commit
- 55–79 → Best Case
- <55 → Pipeline

---

## Output Format

```
DEAL CLASSIFICATION — [Rep / Segment / All]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Deal             ACV      Rep Call    Model Call  Delta   Primary signal
[Account A]      $XXXk    Commit      Commit      —       Activity current, EB engaged
[Account B]      $XXXk    Commit      Best Case   ▼1      No EB contact in 18 days
[Account C]      $XXXk    Best Case   Pipeline    ▼1      Stage stalled 3x avg; no TC

Agreements:  [N] deals  (XX%)
Δ−1 (one tier down): [N] deals  (XX%)
Δ−2 (two tiers down): [N] deals  (XX%)

Adjusted pipeline summary (model-based):
  Commit:     $XXXk  (vs. $XXXk rep-reported)
  Best Case:  $XXXk
  Pipeline:   $XXXk

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G5: This is an analytical input. Rep and manager own the forecast call.]
```

---

## Guardrails

- G5: Always include: "This classification is an analytical input based on CRM
  signals. The rep and their manager own the forecast judgment."
- G6: Data-as-of timestamp required
- G1: If summary is used in a forecast context, apply forecast language qualification
