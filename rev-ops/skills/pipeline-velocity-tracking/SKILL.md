---
name: pipeline-velocity-tracking
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Tracks average sales cycle time by segment, rep, and deal size. Flags deals aging past 1.5x historical average for their current stage. Surfaces velocity trend vs. prior quarter. Triggers: 'pipeline velocity', 'cycle time', 'deals aging', 'stalling pipeline', 'how long are deals taking'."
---

[PROPOSED]

# Pipeline Velocity Tracking

Surfaces where pipeline is slowing before it shows up in a missed quarter.
Aging threshold: 1.5x historical average for stage and segment.

**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `avg_sales_cycle_days`, `primary_segment`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `avg_sales_cycle_days`, `primary_segment`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- User needs to understand how fast deals move through pipeline stages
- Velocity degradation analysis needed (deals slowing, stage duration increasing)
- Cohort comparison of pipeline velocity across segments, reps, or time periods

## Do NOT use for
- Coverage ratio analysis (use pipeline-coverage-analysis)
- Individual deal health (use deal-health-scoring)
- Stage integrity verification (use stage-integrity-audit)

## Typical Activation
"Pipeline velocity", "how fast are deals moving", "velocity by stage", "where are deals getting stuck", "track pipeline velocity for [segment/period]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of pipeline velocity request is this?
   - Single-rep velocity review (one rep's deals — stage-age ratios across active pipeline)
   - Segment-level velocity analysis (Enterprise vs. SMB cycle time comparison)
   - Quarter-over-quarter trend (velocity acceleration or deceleration vs. prior period)
   - Aging flag sweep (all open deals exceeding 1.5x stage-avg threshold)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about deal velocity, aging, or cycle time
   2. Pull HubSpot stage entry/exit history for scope; declare connector status and data-as-of timestamp per G6
   3. Apply G5 — velocity signals are analytical inputs; manager owns the coaching response
   4. Apply G7 — aging flags must include a named escalation path (manager) per at-risk signal protocol
   5. Confirm `avg_sales_cycle_days` from config before computing stage-age ratios
   6. Apply `primary_segment` from config to scope segment-level comparisons correctly
   7. Confirm output destination before delivering — internal RevOps vs. manager coaching vs. leadership

3. **EXPERT CHECK**: What would a veteran RevOps pipeline analyst verify before surfacing findings?
   - Is the stage-age ratio segment-aware? Enterprise deals have longer median stage duration than SMB —
     applying a single `avg_sales_cycle_days` baseline to a mixed-segment pipeline produces false positives
     on enterprise deals and misses SMB stalls. Confirm segment before applying the 1.5x flag.
   - Is the HubSpot stage history scoped to the current active cycle? Pulling all-time stage history
     surfaces legitimate re-stages (deals reopened after closed/lost) alongside current velocity data —
     filter to current active deal cycle, not full deal lifetime.
   - Is the velocity trend directionally consistent with pipeline composition changes? A cycle-time
     increase that coincides with an enterprise mix shift is not the same as a coaching problem —
     distinguish composition effects from rep performance signals before surfacing to management.
   - Is the escalation path named before surfacing aging flags? G7 requires a named owner and channel,
     not a generic "review with manager" instruction.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Applying `avg_sales_cycle_days` without segment-level breakdown (produces noise in mixed pipelines)
   - Surfacing aging flags without a named escalation path (G7 violation)
   - Pulling HubSpot stage history without data-as-of timestamp (G6 violation)
   - Presenting velocity as a rep performance signal without accounting for pipeline composition changes
   - Routing aging flag findings directly to reps — escalation path is manager, not rep

**After execution**, verify:
- G5 qualifier present — velocity signals named as analytical inputs; manager named as decision owner
- G6 data-as-of label applied to all HubSpot stage history reads
- G7 escalation path present on every aging flag (named manager + channel)
- Stage-age ratio computed against segment-appropriate baseline, not blended `avg_sales_cycle_days`
- Confidence: High when HubSpot connected and stage history current; Moderate when connector unavailable or `avg_sales_cycle_days` is estimated
- Confidence: [High] when HubSpot connected and stage history current / [Medium] when connector unavailable or cycle data estimated / [Low] if all inputs are manual or unverified

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

## Output

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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

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
