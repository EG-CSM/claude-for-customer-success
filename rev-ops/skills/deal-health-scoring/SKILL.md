---
name: deal-health-scoring
version: 1.0.0
description: "Scores each open opportunity on five dimensions (activity recency, stakeholder coverage, stage-age ratio, competitive signal, rep forecast accuracy history). Composite 0–100 score. Deals below 50 flagged for next-best-action. Triggers: 'deal health', 'health score', 'which deals are at risk', 'pipeline health', 'risky deals this quarter'."
---

# Deal Health Scoring

Five-dimension health score per open opportunity. Below 50 triggers
automatic handoff to `next-best-action-recommendation`.

**Reference:** Health score dimensions and confidence bands →
`reference/revops-domain-model.md §2`
**Config reads:** `avg_sales_cycle_days`, `primary_segment`

---

## Reasoning Protocol

1. Confirm activation — user wants deal health view or at-risk identification
2. Check HubSpot connector — activity history required; declare fallback if absent
3. Apply G5 — health score is analytical input; rep and manager own the response
4. Apply G6 — surface data-as-of on all activity reads
5. For any score triggering a risk flag, confirm escalation path exists (G7)
6. Confirm output destination

---

## Scoring Model

| Dimension | Weight | Commit signal (full points) | Degraded |
|-----------|--------|-----------------------------|---------|
| Activity recency | 25% | Contact ≤7 days | −5pts per 7 days beyond |
| Stakeholder coverage | 25% | EB + Champion + TC engaged | −8pts per missing role |
| Stage-age ratio | 20% | At/ahead of historical avg | −4pts per 25% beyond avg |
| Competitive signal | 15% | No competitor / counter-play logged | −8pts if competitor active and no response |
| Rep forecast accuracy | 15% | Trailing commit accuracy ≥70% | Scaled linearly to 0 at <30% |

---

## Output Format

```
DEAL HEALTH SCORES — [Scope]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Deal             ACV      Score   Signal    Top risk factor
[Account A]      $XXXk    82      Healthy   —
[Account B]      $XXXk    64      Watch     Stakeholder: no EB contact in 14d
[Account C]      $XXXk    41      AT-RISK   Stage stalled; competitive active
[Account D]      $XXXk    28      AT-RISK   All three dimensions degraded

At-risk (< 50): [N] deals, $XXXk total ACV
→ Run /rev-ops:next-best-action-recommendation for intervention options

Portfolio health distribution:
  Healthy (≥75):   [N] deals  $XXXk
  Watch (50–74):   [N] deals  $XXXk
  At-risk (<50):   [N] deals  $XXXk

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G5: Health scores are analytical inputs. Rep and manager own the response.]
```

---

## Guardrails

- G5: Health score is not a directive — always include the G5 qualifier
- G6: Activity data-as-of timestamp required
- G7: At-risk flags include escalation path: "Flag to [rep's manager] for review"
