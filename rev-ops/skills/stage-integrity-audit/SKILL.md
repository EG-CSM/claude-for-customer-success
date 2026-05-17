---
name: stage-integrity-audit
version: 1.0.0
description: "Detects CRM hygiene issues that distort forecasts: stage-skipping (multi-stage jumps in one update), backward movement, and stale stage (stuck >2x historical avg). Produces audit report for human review before any CRM edits. Never updates CRM autonomously. Triggers: 'stage integrity', 'stage skipping', 'backward movement', 'CRM stage hygiene', 'stale stage'."
---

# Stage Integrity Audit

Detects the three stage anomaly patterns that most distort pipeline forecasts.
All findings are proposals for human review — no autonomous CRM edits.

**Reference:** Governance tiers (Write Protocol) → `reference/revops-domain-model.md §9`
**Config reads:** `crm_system`, `avg_sales_cycle_days`

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

## Guardrails

- G9 (Write Protocol): No autonomous CRM edits. All corrections are proposals.
- G5: Stage anomalies are signals for manager and CRM admin review
- G6: Data-as-of required
