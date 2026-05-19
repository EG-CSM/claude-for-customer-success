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

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `crm_system`, `avg_sales_cycle_days`

---

## Use when
- CRM stage data needs validation against defined stage entry/exit criteria
- Deals appear to be in wrong stages based on activity signals
- Pipeline hygiene audit requires stage-level integrity check

## Do NOT use for
- Pipeline velocity or conversion analysis (use pipeline-velocity-tracking)
- Full CRM hygiene sweep (use crm-hygiene-audit)
- Deal health scoring (use deal-health-scoring)

## Typical Activation
"Stage integrity audit", "are deals in the right stages", "stage hygiene check", "audit stage progression for [rep/team/period]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of stage integrity request is this?
   - Single-deal audit (one account — all three pattern checks against its history)
   - Cohort audit (all open pipeline or a rep/team subset — pattern frequency summary)
   - Rep-period analysis (stage hygiene across a rep's deals for a specific period)
   - Below-threshold remediation (specific deal already flagged — what needs correction)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about stage hygiene, CRM accuracy, or forecast distortion
   2. Pull HubSpot stage change history for scope; declare connector status and unavailability if missing
   3. Apply G6 — data-as-of timestamp required on all stage history reads
   4. Apply G9 — no autonomous CRM edits; all corrections are proposals for human confirmation
   5. Apply G5 — findings are inputs for manager and CRM admin review, not auto-executed corrections
   6. Confirm `avg_sales_cycle_days` from config before running Pattern 3 (stale stage ratio requires baseline)
   7. If `crm_system` is not HubSpot, declare connector assumptions explicitly before proceeding

3. **EXPERT CHECK**: What would a veteran RevOps CRM analyst verify before surfacing findings?
   - Is the stage change history scoped correctly? Pulling all-time history for a deal will surface
     legitimate re-stages (e.g., after a lost reopen) alongside hygiene problems — the analyst
     filters to the current active deal cycle, not the full deal lifetime.
   - Is the stale-stage ratio segment-aware? Enterprise deals have longer median stage duration than
     SMB — applying a single `avg_sales_cycle_days` baseline to a mixed-segment pipeline produces
     false positives on enterprise and misses SMB stalls. Confirm segment before applying the 2x flag.
   - Is write-tier confirmation surfaced before any CRM action is queued? Any proposed stage
     correction is Write-tier under G9 — the analyst confirms the escalation path (CRM admin or
     manager) before the finding is delivered, not after.
   - Is the escalation path specific? "Review with manager" is not actionable — the finding must
     name the rep's manager and the recommended resolution step per pattern type.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Proposing autonomous CRM stage corrections without human confirmation (G9 violation)
   - Applying stale-stage ratio without segment-level baseline (produces noise in mixed-segment pipelines)
   - Pulling HubSpot stage history without data-as-of timestamp (G6 violation)
   - Routing stage anomaly findings directly to reps — escalation path is manager and CRM admin, not rep

**After execution**, verify:
- G6 data-as-of label applied to all HubSpot stage history reads
- G9 compliance confirmed — no CRM corrections queued without explicit human confirmation
- G5 framing applied — findings are analytical inputs, not correction mandates
- Escalation path named per finding (manager + CRM admin where applicable)
- Confidence: High when HubSpot connected and stage history current; Moderate when connector unavailable or `avg_sales_cycle_days` is estimated
    - Confidence: [High] when HubSpot connected and stage history current / [Medium] when connector unavailable or `avg_sales_cycle_days` is estimated / [Low] if all inputs are manual or unverified

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

## Output

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

- G9 (Write Protocol): No autonomous CRM edits. All corrections are proposals.
- G5: Stage anomalies are signals for manager and CRM admin review
- G6: Data-as-of required
