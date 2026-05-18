---
name: deal-desk-workflow-management
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Manages the complete deal desk approval routing workflow: submit → review → route → decide → log. Assembles context brief (discount rationale, competitive context, Tier 1 churn risk signal) before routing to approver. Enforces SLA (24h standard, 4h final 2 weeks of quarter). SLA breach escalates to #revops-ops. Triggers: 'deal desk', 'approval workflow', 'route for approval', 'deal approval status', 'process a deal desk request'."
---

# Deal Desk Workflow Management

The approval routing workflow — not the approval itself. Deal Desk assembles
context, routes to the right person, and tracks to resolution.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
`linear_connected`, `slack_connected`

---

## Use when
- Deal requires formal approval routing through the deal desk
- Discount level crosses standard or elevated threshold requiring approver assignment
- User needs to check status of an active deal desk submission
- Deal desk submission requires context brief assembly before routing

## Do NOT use for
- Approving deals (this skill routes only — never approves)
- Discount threshold calculation in isolation (use discount-threshold-monitoring)
- Non-standard terms detection without approval routing context (use non-standard-terms-detection)

## Typical activation
"Submit to deal desk", "route for approval", "deal desk for [account]", "deal approval status", "process a deal desk request"

---

## Reasoning Protocol

1. Confirm activation — user submitting a deal for desk review or checking status
2. Read deal fields from HubSpot
3. Run sub-skills: discount-threshold-monitoring, non-standard-terms-detection,
   revenue-leakage-scanning to assemble context brief
4. Route to correct approval authority
5. Apply G1 — desk review does not constitute deal approval or revenue commitment
6. Track SLA — flag breach to #revops-ops

---

## Workflow Stages

```
Stage 1 — Submission (automatic on threshold crossing or manual)
  Confirm: deal link, ACV, discount %, close date, rep

Stage 2 — Context brief assembly
  Run: discount-threshold-monitoring → tier and approver
  Run: non-standard-terms-detection → any legal/finance flags
  Run: early-churn-downgrade-signal-detection (Tier 1) → structural risk signal
  Run: revenue-leakage-scanning → any structural leakage

Stage 3 — Routing
  Create Linear issue with context brief attached
  Assign to: [determined by discount tier from practice profile]
  Set SLA: 24h standard / 4h final 2 weeks of quarter

Stage 4 — Decision
  Approver resolves Linear issue: Approved / Approved with conditions / Rejected
  Decision and rationale logged in CRM (Write-tier — confirm before writing)

Stage 5 — Outcome log
  Log: timestamp, deal ID, discount %, approver, decision, rationale
  Update CRM deal record (Write-tier — confirm before writing)
  Flag pattern: discount frequency report updated
```

---

## Context Brief Format

```
DEAL DESK BRIEF — [Account Name]
Submitted: [timestamp]  SLA: [deadline]

Deal: [link]  ACV: $XXXk  Discount: XX%  Close: [date]  Rep: [name]

Approval tier: [Elevated / Executive]  Required: [Role(s)]

Discount rationale: [from deal notes / rep-stated]
Competitive context: [from deal notes]
Tier 1 churn signal: [FIRING: reason / Clear]
Non-standard terms: [list or None]
Revenue leakage: [list or None detected]

Recommended decision: [Approve / Approve with conditions / Investigate]
  Basis: [structured rationale — not opinion]
```

---

## SLA Monitoring

```
If SLA approaching (4h remaining): Slack ping to approver
If SLA breached: Post to #revops-ops with deal link and approver name
```

---

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

- Never approve deals — route only
- G1: Context brief does not constitute revenue commitment
- G9: CRM updates are Write-tier — confirm before execution
- G3: If comp implications exist in deal structure → flag for HR + Finance
