---
name: pipeline-velocity-tracking
version: 1.0.0
description: "Tracks average sales cycle time by segment, rep, and deal size. Flags deals aging past 1.5x historical average for their current stage. Surfaces velocity trend vs. prior quarter. Triggers: 'pipeline velocity', 'cycle time', 'deals aging', 'stalling pipeline', 'how long are deals taking'."
---

# Pipeline Velocity Tracking

Surfaces where pipeline is slowing before it shows up in a missed quarter.
Aging threshold: 1.5x historical average for stage and segment.

**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `avg_sales_cycle_days`, `primary_segment`

---

## Reasoning Protocol

1. Confirm activation — user asking about deal velocity, aging, or cycle time
2. Check HubSpot stage history — required; declare fallback if unavailable
3. Apply G6 — data-as-of on all stage history reads
4. Apply G5 — velocity signals are inputs; manager owns the coaching response
5. Confirm output destination

---

## Workflow

Pull stage entry/exit dates for all open opportunities from HubSpot.
Calculate:
```
Days in current stage = Today − Stage entry date
Segment avg for stage = Historical median days in this stage for this segment (trailing 4Q)
Stage-age ratio       = Days in current stage ÷ Segment avg
```

Flag when stage-age ratio > 1.5x. Surface deals by aging severity.

Compare overall cycle time trend: current quarter avg vs. prior quarter avg.

---

## Output Format

```
PIPELINE VELOCITY — [Scope] [HubSpot ✓ live — as of YYYY-MM-DD]

Avg cycle time this quarter:  [N] days  (vs. [N] days prior quarter  ↑/↓)

Aging flags (stage-age ratio > 1.5x):
Deal             Stage           Days in stage   Avg    Ratio   Owner
[Account A]      Negotiation     34d             18d    1.9x    [Rep]
[Account B]      Proposal        28d             14d    2.0x    [Rep]

Total aging deals: [N]  ($XXXk ACV)
Velocity trend: [Slowing / Stable / Accelerating]

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G5: Velocity flags are analytical inputs. Manager owns the response.]
```

## Guardrails

- G5, G6 apply. Aging flags require manager as escalation path (G7).
