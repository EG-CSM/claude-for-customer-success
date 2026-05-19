---
name: revenue-brief-generation
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Produces weekly or monthly executive revenue narrative by coordinating outputs from all rev-ops agents. Five sections: forecast + pipeline, pipeline health, CS capacity status, NRR trajectory, top 3 risks with recommended owner and action. One decision required per brief. Delivered as [DRAFT] for RevOps lead review before distribution. Triggers: 'revenue brief', 'weekly summary', 'executive summary', 'what happened this week', 'run the revenue brief'."
---

[PROPOSED]

# Revenue Brief Generation

Executive narrative that synthesizes the full revenue picture into one
coherent story — not a dashboard dump.

**Reference:** All domain model sections, output destination labels →
`../../../shared/revops-domain-model.md §11`
**Config reads:** All company profile fields

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: all company profile fields

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when

This skill produces a **cross-functional revenue narrative** that spans Sales pipeline,
CS-owned ARR vectors, and finance-facing forecast. It is not a CS-function operational
dashboard — it synthesizes across functions for leadership or board consumption.

- Leadership or board review requires a structured revenue performance brief
- Weekly or monthly revenue status needs synthesis across pipeline, forecast, and actuals
- RevOps needs to package revenue narrative for a specific audience

## Do NOT use for
- Raw pipeline analysis (use pipeline-coverage-analysis)
- Detailed forecast variance decomposition (use forecast-variance-analysis)
- Deal-level detail (this is a brief, not a deal review)
- CS-internal operational reporting — weekly triage, CSM performance summaries,
  or GRR/NRR dashboards for the CS team (use `/cs-ops:metric-dashboard`)
- Cross-functional metrics dashboard covering pipeline, handoff quality, and CS capacity signals — use `gtm-unified-metrics-pulse`

## Typical Activation
"Revenue brief", "generate revenue summary", "revenue status for [period]", "brief for leadership", "weekly revenue brief"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of revenue brief request is this?
   - Weekly brief (default — all five sections, period = current week)
   - Monthly brief (all five sections, period = current month)
   - Single-section delivery (one section requested in isolation)
   - Fallback-mode brief (one or more source skills/connectors unavailable — labeled partial output)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting executive summary, weekly brief, or revenue narrative
   2. Determine period: weekly (default) or monthly — confirm with user if ambiguous
   3. For each section, pull from its source skill or connector; label connector status and data-as-of per section
   4. Apply G1 to all forward-looking content (Section 1 forecast language mandatory)
   5. Apply G6 to every section — data-as-of timestamp required on all connector reads
   6. Apply G2 to Section 3 (CS capacity) — structural input, not a hiring mandate
   7. Apply G7 to Section 5 (Top 3 Risks) — each risk requires escalation path and named owner
   8. Confirm output destination before delivering — who sees this brief? Destination label required on final version
   9. Deliver as [DRAFT] — RevOps lead reviews before distribution

3. **EXPERT CHECK**: What would a veteran RevOps leader verify before this brief leaves the room?
   - Is data freshness declared on every section? A section without a data-as-of date misleads leadership
     on whether they're making decisions from live or stale inputs.
   - Are CS-owned ARR vectors (expansion, renewal) in Section 1 labeled as CS accountability — not Sales?
     Misattributing CS-owned pipeline creates conflicting ownership narratives at the leadership level.
   - Does Section 5 name a specific owner and recommended action for each risk — not just a risk label?
     "At-risk deal count is high" without an owner and action is observation, not a brief.
   - Is the "one decision required" item genuinely the single most important decision, and is it specific
     enough for leadership to act on? Vague decisions ("address pipeline risk") produce no action.
   - Is the output destination confirmed before delivery? Section 4 account-level data must never land
     in #revops-alignment — only #cs-leadership.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Producing any section from an unavailable connector without a labeled fallback (creates phantom metrics)
   - Applying G1 forecast qualification only to Section 1 new logo pipeline but not to expansion or renewal forecast
   - Surfacing connector reads without data-as-of timestamp on each section (G6 violation)
   - Section 5 risks without named owner and escalation path (G7 violation)
   - Delivering the brief without confirming output destination — account-level data routed to wrong audience

**After execution**, verify:
- G1 qualification present on all forward-looking content across all sections
- G6 data-as-of label applied to every section with a connector read
- G7 escalation path with named owner on every Section 5 risk
- Output destination confirmed — account-level data labeled for correct audience
- [DRAFT] status applied — RevOps lead review before distribution
- Confidence: High when all source skills and connectors are live; Moderate when any section is in fallback mode
    - Confidence: [High] when all source skills and connectors are live / [Medium] when any section is in fallback mode / [Low] if all inputs are manual or unverified

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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

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
**Distribution:** Outputs contain revenue projections and pipeline data. Confirm receiving audience is authorized before sharing. All forward-looking figures carry `[review — internal planning data]` tags.

## Guardrails

- G1: Section 1 forecast qualification mandatory
- G2: Section 3 structural input qualifier mandatory
- G6: Data-as-of on every section
- G7: Section 5 risks each require escalation path and owner
