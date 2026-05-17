---
name: revenue-brief-generation
version: 1.0.0
description: "Produces weekly or monthly executive revenue narrative by coordinating outputs from all rev-ops agents. Five sections: forecast + pipeline, pipeline health, CS capacity status, NRR trajectory, top 3 risks with recommended owner and action. One decision required per brief. Delivered as [DRAFT] for RevOps lead review before distribution. Triggers: 'revenue brief', 'weekly summary', 'executive summary', 'what happened this week', 'run the revenue brief'."
---

# Revenue Brief Generation

Executive narrative that synthesizes the full revenue picture into one
coherent story — not a dashboard dump.

**Reference:** All domain model sections, output destination labels →
`reference/revops-domain-model.md §11`
**Config reads:** All practice profile fields

---

## Reasoning Protocol

1. Confirm activation — user requesting executive summary or weekly brief
2. Determine period: weekly (default) or monthly
3. Pull each section from its source skill or connector
4. Apply G1 to all forward-looking content
5. Apply G6 to every section — data-as-of per section
6. Confirm output destination before delivering — who sees this brief?
7. Deliver as [DRAFT] — RevOps lead reviews before distribution

---

## Five Sections + Decision

```
Section 1 — Forecast + Pipeline
  Commit: $XXXk | Best Case: $XXXk | Pipeline: $XXXk
  Coverage: [signal] | WoW: [delta with "why it changed" if >threshold]
  Source: /rev-ops:pipeline-coverage-analysis + /rev-ops:scenario-modeling
  [CRM ✓ live — as of YYYY-MM-DD]

Section 2 — Pipeline Health
  Overall health: [N]/100 | At-risk deals: [N] ($XXXk ACV)
  Top 3 at-risk: [deal name, signal, owner] — each 1 line
  Source: /rev-ops:deal-health-scoring
  [CRM ✓ live — as of YYYY-MM-DD]

Section 3 — CS Capacity
  Headroom: XX% [HEALTHY/AT-RISK/CRITICAL]
  At P50: [N] CSMs needed, [N] in seat, gap [+N/-N]
  Hiring action required by: [date or "none"]
  Source: /rev-ops:closed-won-to-cs-capacity-modeling
  [G2: Structural input — hiring requires budget approval]

Section 4 — NRR Trajectory
  Current NRR: XXX% | Plan: XXX% | Delta: [Xpp]
  Expansion: [trend] | Contraction: [trend] | Churn: [trend]
  Source: /rev-ops:growth-model-vs-actuals-tracking
  [CS Platform ✓ live — as of YYYY-MM-DD]

Section 5 — Top 3 Risks (cross-functional)
  1. [Risk name] | Owner: [role] | Recommended action: [specific]
  2. [Risk name] | Owner: [role] | Recommended action: [specific]
  3. [Risk name] | Owner: [role] | Recommended action: [specific]

One decision required this week:
  [The single most important decision leadership needs to make — specific, named]
```

---

## Fallback Behavior

When any source skill is unavailable, that section is labeled:
`[Section N: unavailable — [Connector]: Unavailable]`

Brief is still produced; available sections are delivered. Degraded sections
do not block the brief.

---

## Output

Delivered as `[DRAFT — for RevOps lead review before distribution]`
Output destination label required on final version before distribution.

## Guardrails

- G1: Section 1 forecast qualification mandatory
- G2: Section 3 structural input qualifier mandatory
- G6: Data-as-of on every section
- G7: Section 5 risks each require escalation path and owner
