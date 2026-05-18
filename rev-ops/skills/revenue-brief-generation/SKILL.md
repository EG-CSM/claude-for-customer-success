---
name: revenue-brief-generation
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Produces weekly or monthly executive revenue narrative by coordinating outputs from all rev-ops agents. Five sections: forecast + pipeline, pipeline health, CS capacity status, NRR trajectory, top 3 risks with recommended owner and action. One decision required per brief. Delivered as [DRAFT] for RevOps lead review before distribution. Triggers: 'revenue brief', 'weekly summary', 'executive summary', 'what happened this week', 'run the revenue brief'."
---

# Revenue Brief Generation

Executive narrative that synthesizes the full revenue picture into one
coherent story — not a dashboard dump.

**Reference:** All domain model sections, output destination labels →
`../../../shared/revops-domain-model.md §11`
**Config reads:** All practice profile fields

---

## Use when
- Leadership or board review requires a structured revenue performance brief
- Weekly or monthly revenue status needs synthesis across pipeline, forecast, and actuals
- RevOps needs to package revenue narrative for a specific audience

## Do NOT use for
- Raw pipeline analysis (use pipeline-coverage-analysis)
- Detailed forecast variance decomposition (use forecast-variance-analysis)
- Deal-level detail (this is a brief, not a deal review)

## Typical activation
"Revenue brief", "generate revenue summary", "revenue status for [period]", "brief for leadership", "weekly revenue brief"

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

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal, customer, and revenue data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G1: Section 1 forecast qualification mandatory
- G2: Section 3 structural input qualifier mandatory
- G6: Data-as-of on every section
- G7: Section 5 risks each require escalation path and owner
