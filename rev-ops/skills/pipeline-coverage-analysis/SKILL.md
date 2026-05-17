---
name: pipeline-coverage-analysis
version: 1.0.0
description: "Calculates pipeline coverage ratio by segment, rep, and quarter. Flags when coverage falls below the threshold derived from win rate (not a universal 3x). Produces an exposure ranking and week-over-week trend. Use when assessing pipeline health before a forecast call, board review, or quarter-close. Triggers: 'pipeline coverage', 'coverage ratio', 'are we covered for Q[N]', 'pipeline risk by segment'."
---

# Pipeline Coverage Analysis

Calculates pipeline coverage ratio and surfaces exposure risk before it becomes
a missed quarter. Coverage threshold is always derived from win rate — never a
universal 3x rule.

**Reference:** Coverage thresholds → `reference/revops-domain-model.md §7`
**Config reads:** `win_rate` (user-provided or practice profile), `current_arr`,
`target_growth_pct`, `nrr_current`

---

## Reasoning Protocol

1. Confirm activation — user is asking about coverage, pipeline sufficiency, or quarter risk
2. Check HubSpot connector — if unavailable, declare and shift to user-provided inputs
3. Read practice profile for segment, target growth, NRR, win rate if not provided
4. Apply G6 — surface data-as-of timestamp on all pipeline figures
5. Apply G1 — coverage output destined for leadership or board requires forecast language qualification
6. Confirm output destination before delivering — internal RevOps vs. leadership vs. finance

---

## Inputs

Required (from practice profile or user):
- Current pipeline value by stage (from HubSpot or user-provided)
- Win rate (practice profile or user-stated)
- New ARR target (derived from practice profile or user-provided)

Optional:
- Segment filter, rep filter, quarter filter

---

## Workflow

**Step 1 — Derive required coverage**
```
Required Coverage = 1 ÷ Win Rate  [revops-domain-model.md §4]
Pipeline Target   = New ARR Target × Required Coverage
```
State the win rate used and its source `[Practice profile]` or `[User provided]`.

**Step 2 — Calculate current coverage by segment**
Pull open pipeline from HubSpot filtered to current quarter close dates.
For each segment:
```
Current Coverage = Current Pipeline Value ÷ New ARR Target
Pipeline Gap     = Pipeline Target − Current Pipeline Value
```

**Step 3 — Apply coverage signal thresholds** `[revops-domain-model.md §7]`
- Below 2x → CRITICAL
- 2x–3x → AT-RISK
- 3x–5x → HEALTHY
- Above 5x → INSPECT

**Step 4 — Produce exposure ranking**
Sort segments and reps by gap magnitude. Name the top 3 most exposed.

**Step 5 — Week-over-week trend**
Compare to prior week's pipeline pull if available in session history.
If not available, note: "Prior week data unavailable — trend not calculated."

---

## Output Format

```
PIPELINE COVERAGE ANALYSIS
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Required coverage: [N]x (1 ÷ [win_rate]% win rate)
─────────────────────────────────────────────────────
Segment          Coverage   Signal      Gap
Enterprise       2.8x       AT-RISK     $420K short
Mid-Market       4.1x       HEALTHY     —
SMB              1.6x       CRITICAL    $280K short
─────────────────────────────────────────────────────
Overall          3.1x       HEALTHY     $700K short in 2 segments

Top exposures:
1. SMB — $280K gap; pipeline at 1.6x vs 4.0x required
2. Enterprise — $420K gap; thin buffer against plan

Week-over-week: [+$X / −$X / unavailable]

[DRAFT — RevOps internal] [Confidence: High]
```

## Guardrails

- G1: If output is for leadership or board, add: "Coverage as of [date]. Subject to
  pipeline movement before quarter close."
- G6: Always surface data-as-of timestamp
- G5: "Coverage ratio is a structural signal. Sales leadership owns the response."
