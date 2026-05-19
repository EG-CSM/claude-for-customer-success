---
name: stage-integrity-audit
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Detects CRM hygiene issues that distort forecasts: stage-skipping (multi-stage jumps in one update), backward movement, and stale stage (stuck >2x historical avg). Produces audit report for human review before any CRM edits. Never updates CRM autonomously. Triggers: 'stage integrity', 'stage skipping', 'backward movement', 'CRM stage hygiene', 'stale stage'."
---

[PROPOSED]

# Stage Integrity Audit

Detects the three stage anomaly patterns that most distort pipeline forecasts.
All findings are proposals for human review — no autonomous CRM edits.

**Reference:** Governance tiers (Write Protocol) → `../../../shared/revops-domain-model.md §9`
**Config reads:** `crm_system`, `avg_sales_cycle_days`

---

## Use when
- CRM stage data needs validation against defined stage entry/exit criteria
- Deals appear to be in wrong stages based on activity signals
- Pipeline hygiene audit requires stage-level integrity check

## Do NOT use for
- Pipeline velocity or conversion analysis (use pipeline-velocity-tracking)
- Full CRM hygiene sweep (use crm-hygiene-audit)
- Deal health scoring (use deal-health-scoring)

## Typical activation
"Stage integrity audit", "are deals in the right stages", "stage hygiene check", "audit stage progression for [rep/team/period]"

---

## Reasoning Protocol

1. Confirm activation — user asking about stage hygiene, CRM accuracy, or forecast distortion
2. Check HubSpot stage change history — required; declare unavailable if missing
3. Apply G6 — data-as-of on all stage history reads
4. Apply governance tier — any CRM correction is Write-tier; requires human confirmation
5. Apply G5 — findings are inputs for manager and CRM admin review

---

## Three Anomaly Patterns

**Pattern 1 — Stage skipping**
Deal advanced 2+ stages in a single update, with no intermediate stage entry recorded.
Signal: retroactive CRM entry rather than real-time progression. Distorts time-in-stage
averages and velocity metrics.

**Pattern 2 — Backward movement**
Deal moved to an earlier stage after being in a later one.
Signal: may indicate a stalled or lost deal not yet marked closed/lost.
Requires investigation before accepting the regression as valid.

**Pattern 3 — Stale stage**
Deal has been in the same stage for >2x the historical median for that stage and segment.
Signal: pipeline may be padded with deals unlikely to close in the stated quarter.

---

## Output Format

```
STAGE INTEGRITY AUDIT — [Quarter/Scope]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

Pattern 1 — Stage skipping ([N] deals)
  [Account A]  Skipped Discovery→Proposal→Negotiation on [date]  Rep: [name]
  [Account B]  Skipped Qualification→Proposal on [date]           Rep: [name]

Pattern 2 — Backward movement ([N] deals)
  [Account C]  Moved Negotiation→Proposal on [date]              Investigate: lost deal?
  [Account D]  Moved Proposal→Discovery on [date]                Investigate: restart?

Pattern 3 — Stale stage ([N] deals)
  [Account E]  In Proposal 41 days (avg 18d, ratio 2.3x)         Rep: [name]
  [Account F]  In Discovery 35 days (avg 12d, ratio 2.9x)        Rep: [name]

Recommended actions (require human confirmation before CRM edits):
  [ ] Review backward movement deals for closed/lost reclassification
  [ ] Validate stage-skip deals for accurate close date
  [ ] Review stale stage deals for pipeline qualification

[DRAFT — RevOps internal] [Confidence: High]
[Write-tier: CRM corrections require human confirmation before execution]
```

---

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

- G9 (Write Protocol): No autonomous CRM edits. All corrections are proposals.
- G5: Stage anomalies are signals for manager and CRM admin review
- G6: Data-as-of required
