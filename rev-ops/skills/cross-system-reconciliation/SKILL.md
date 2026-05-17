---
name: cross-system-reconciliation
version: 1.0.0
description: "Traces conflicting numbers from different sources (CRM vs. Finance Sheets vs. CS platform) to their root cause. Applies data authority hierarchy: HubSpot > Finance Sheets > CS platform > Slack/Linear. Produces a reconciliation memo with source attribution and recommended resolution. Never silently resolves conflicts. Triggers: 'which number is right', 'reconcile', 'conflicting numbers', 'CRM vs Sheets', 'our ARR numbers don't match', 'why is the pipeline number different'."
---

# Cross-System Reconciliation

When two systems report different numbers, the answer is almost always:
different definitions, different timing, or different source authority.

**Reference:** Data authority hierarchy and source attribution labels →
`reference/revops-domain-model.md §3`
**Config reads:** `crm_system`, `google_drive_connected`

---

## Reasoning Protocol

1. Confirm activation — user has two conflicting numbers they need reconciled
2. Identify: what metric, which systems, what values each system reports
3. Apply data authority hierarchy to determine governing source
4. Trace root cause — do not guess; check each dimension
5. Apply G1 — reconciliation memos for finance require forecast language
6. Surface the conflict; never silently resolve it with a number

---

## Data Authority Hierarchy `[revops-domain-model.md §3]`

```
Priority 1: HubSpot CRM — opportunity, account, contact data
Priority 2: Finance-owned Sheets (Drive) — quota, territory, comp, plan baseline
Priority 3: CS platform (via Zapier) — health scores, ARR at risk, NRR actuals
Priority 4: Slack / Linear — context only; no numerical authority
```

## Root Cause Taxonomy

```
Definition mismatch: Systems use different definitions for the same metric
  (e.g., CRM counts closed/won by close date; Finance counts by billing period)

Timing difference: Systems snapshot at different points in time
  (e.g., CRM live; Finance report is month-end close)

Data entry gap: A transaction exists in one system not yet entered in another
  (e.g., verbal commitment in CRM; not yet in Finance model)

Scope difference: Systems cover different populations
  (e.g., CRM includes all segments; Finance model covers Enterprise only)
```

---

## Output Format

```
RECONCILIATION MEMO — [Metric]
[CRM ✓ live — as of YYYY-MM-DD] [Drive: ✓ live / Unavailable]

Conflict:
  [System A] reports: $XXXk  [Source label]
  [System B] reports: $XXXk  [Source label]
  Delta: $XXXk

Root cause: [Definition mismatch / Timing / Data entry gap / Scope]
  Explanation: [Specific — e.g., "CRM uses close date; Finance uses invoice date.
  3 deals closed in CRM on 3/31 but invoiced in April."]

Governing source per authority hierarchy:
  For [use case A]: Use [System X] because [reason]
  For [use case B]: Use [System Y] because [reason]

Recommended action:
  Who aligns: [RevOps lead]
  How: [Specific step to close the gap]
  By: [Timeframe]

[Human resolution required before either number is used in board or leadership output]
[DRAFT — RevOps internal]
```

---

## Guardrails

- Never silently resolve — surface the conflict and wait for human resolution
- G1: If reconciliation output goes to finance or board, add forecast qualification
- G6: Timestamp every source read; timing differences are common root causes
