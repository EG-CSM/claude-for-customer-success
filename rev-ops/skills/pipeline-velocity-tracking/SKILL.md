---
name: pipeline-velocity-tracking
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Tracks average sales cycle time by segment, rep, and deal size. Flags deals aging past 1.5x historical average for their current stage. Surfaces velocity trend vs. prior quarter. Triggers: 'pipeline velocity', 'cycle time', 'deals aging', 'stalling pipeline', 'how long are deals taking'."
---

# Pipeline Velocity Tracking

Surfaces where pipeline is slowing before it shows up in a missed quarter.
Aging threshold: 1.5x historical average for stage and segment.

**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `avg_sales_cycle_days`, `primary_segment`

---

## Use when
- User needs to understand how fast deals move through pipeline stages
- Velocity degradation analysis needed (deals slowing, stage duration increasing)
- Cohort comparison of pipeline velocity across segments, reps, or time periods

## Do NOT use for
- Coverage ratio analysis (use pipeline-coverage-analysis)
- Individual deal health (use deal-health-scoring)
- Stage integrity verification (use stage-integrity-audit)

## Typical activation
"Pipeline velocity", "how fast are deals moving", "velocity by stage", "where are deals getting stuck", "track pipeline velocity for [segment/period]"

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

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal and pipeline data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G5, G6 apply. Aging flags require manager as escalation path (G7).
