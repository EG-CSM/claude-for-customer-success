---
name: territory-optimization
version: 1.0.0
description: "Evaluates territory fairness across reps on four dimensions: TAM coverage, historical attainment, account density, and whitespace. Proposes recarving when imbalances exceed threshold. All proposals are [DRAFT] until dual-confirmed by RevOps lead and Sales lead. Never finalizes territory changes autonomously. Triggers: 'territory balance', 'recarve territories', 'territory fairness', 'territory analysis', 'rep territory review'."
---

# Territory Optimization

Territory fairness analysis and recarving proposals. All outputs are [DRAFT]
until RevOps lead + Sales lead dual confirmation (Critical Write).

**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `current_ae_count`, `primary_segment`, `avg_deal_acv`

---

## Reasoning Protocol

1. Confirm activation — user requesting territory analysis or recarving
2. Check HubSpot for account distribution data; declare fallback if unavailable
3. Apply G4 — all territory outputs are drafts until dual-confirmed
4. Apply G5 — territory analysis is structural input; Sales leadership owns decisions
5. Confirm this is being run inside `annual-planning-workflow` or standalone

---

## Four Fairness Dimensions

| Dimension | What it measures | Imbalance signal |
|-----------|-----------------|-----------------|
| TAM coverage | Total addressable accounts per rep territory | >2x spread between highest and lowest rep |
| Historical attainment | Is attainment variance explained by territory quality or rep performance? | Attainment variance >30pp where territory TAM is similar |
| Account density | Travel/call coverage burden | Outlier rep >1.5x avg accounts per geographic area |
| Whitespace | Expansion potential in existing accounts | Significant whitespace concentrated in <20% of reps |

---

## Output Format

```
TERRITORY OPTIMIZATION [DRAFT]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: Moderate]

Fairness scorecard:
Rep       TAM     Attainment   Density   Whitespace   Fairness
[Rep A]   High    High         Medium    Low          Favorable
[Rep B]   Low     Medium       High      Medium       Unfavorable
[Rep C]   Medium  Low          Low       High         Neutral

Recarving proposals:
1. [Specific account or territory segment] from [Rep B] to [Rep A/new rep]
   Rationale: [TAM gap / density relief / whitespace rebalancing]
   Impact: Attainment variance reduction: estimated XX pp

[DRAFT — not final until dual-confirmed by RevOps and Sales leadership]
[G4 applies]
```

---

## Guardrails

- G4: Every territory output is labeled [DRAFT] until dual-confirmed
- G5: Structural analysis — Sales leadership owns decisions
- G2: Territory proposals do not constitute headcount decisions
