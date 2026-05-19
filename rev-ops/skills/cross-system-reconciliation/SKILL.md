---
name: cross-system-reconciliation
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Traces conflicting numbers from different sources (CRM vs. Finance Sheets vs. CS platform) to their root cause. Applies data authority hierarchy: HubSpot > Finance Sheets > CS platform > Slack/Linear. Produces a reconciliation memo with source attribution and recommended resolution. Never silently resolves conflicts. Triggers: 'which number is right', 'reconcile', 'conflicting numbers', 'CRM vs Sheets', 'our ARR numbers don't match', 'why is the pipeline number different'."
---

[PROPOSED]

# Cross-System Reconciliation

When two systems report different numbers, the answer is almost always:
different definitions, different timing, or different source authority.

**Reference:** Data authority hierarchy and source attribution labels →
`../../../shared/revops-domain-model.md §3`
**Config reads:** `crm_system`, `google_drive_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `crm_system`, `google_drive_connected`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- Data discrepancies across CRM, CS platform, and billing/finance systems need reconciliation
- ARR recognized in one system does not match another and root cause is needed
- Pre-board or pre-audit data reconciliation is required

## Do NOT use for
- Single-system CRM hygiene (use crm-hygiene-audit)
- Forecast variance analysis (use forecast-variance-analysis)
- Revenue recognition decisions (analytical input only — G1 applies)

## Typical Activation
"Cross-system reconciliation", "data doesn't match between [system A] and [system B]", "reconcile ARR across systems", "why is CRM different from finance", "system reconciliation report"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of reconciliation request is this?
   - Two-system number conflict (CRM vs. Finance Sheets)
   - Multi-system discrepancy (CRM + CS platform + Finance)
   - Pre-board or pre-audit reconciliation sweep
   - Single-metric root cause trace (definition, timing, data entry, scope)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user has two conflicting numbers they need reconciled
   2. Identify: what metric, which systems, what values each system reports
   3. Apply data authority hierarchy to determine governing source
   4. Trace root cause — do not guess; check each dimension
   5. Apply G1 — reconciliation memos for finance require forecast language
   6. Surface the conflict; never silently resolve it with a number

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Are both source values timestamped? Timing differences are the most common root cause — a snapshot date mismatch explains more conflicts than definition errors.
   - Is the data authority hierarchy applied before drawing any conclusion? The governing source determines which number is right for each use case.
   - Is the root cause specific enough to act on? "Definition mismatch" without naming the definitions is not a root cause.
   - Is the recommended action owned? A reconciliation memo without a named resolver and timeframe will not close the gap.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Silently picking one number without surfacing the conflict (G1 violation)
   - Presenting a reconciliation memo without data-as-of timestamps on both sources (G6 violation)
   - Applying the data authority hierarchy without checking whether the higher-authority system is current
   - Recommending resolution without naming the owner and timeframe

**After execution**, verify:
- G1 forecast qualification present if output goes to finance or board
- G6 data-as-of timestamp on every source read
- Root cause is specific (not just category-labeled)
- Recommended action has a named owner and timeframe
- Confidence: High when both systems are connected and timestamps are confirmed; Moderate when either system is unavailable or timing cannot be verified
    - Confidence: [High] when both systems are connected and timestamps are confirmed / [Medium] when either system is unavailable or timing cannot be verified / [Low] if all inputs are manual or unverified

---

## Data Authority Hierarchy `[revops-domain-model.md §3]`

**Connector error categorization:** When a connector call fails, distinguish the error type before proceeding:
- **Rate-limited (transient):** Connector returns HTTP 429 or equivalent throttle signal. Note the rate limit explicitly in output ("data source temporarily rate-limited — retry in 60 seconds recommended") and offer to retry rather than proceeding with degraded output.
- **Unavailable (permanent for this session):** Connector is not configured, authentication has expired, or service is down. Fall back to user-provided data and label all affected sections as "connector unavailable — manual input used."
Do not conflate these — a rate-limited connector will return data shortly; an unavailable connector will not.

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

## Output

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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential customer, deal, and operational data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- Never silently resolve — surface the conflict and wait for human resolution
- G1: If reconciliation output goes to finance or board, add forecast qualification
- G6: Timestamp every source read; timing differences are common root causes
