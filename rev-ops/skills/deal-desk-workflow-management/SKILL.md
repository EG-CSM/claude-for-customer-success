---
name: deal-desk-workflow-management
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Manages the complete deal desk approval routing workflow: submit → review → route → decide → log. Assembles context brief (discount rationale, competitive context, Tier 1 churn risk signal) before routing to approver. Enforces SLA (24h standard, 4h final 2 weeks of quarter). SLA breach escalates to #revops-ops. Triggers: 'deal desk', 'approval workflow', 'route for approval', 'deal approval status', 'process a deal desk request'."
---

[PROPOSED]

# Deal Desk Workflow Management

The approval routing workflow — not the approval itself. Deal Desk assembles
context, routes to the right person, and tracks to resolution.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
`linear_connected`, `slack_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
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

## Typical Activation
"Submit to deal desk", "route for approval", "deal desk for [account]", "deal approval status", "process a deal desk request"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of deal desk request is this?
   - New submission (threshold crossed or manual request — assemble context brief + route)
   - Status check (active submission — report current stage, SLA remaining, approver)
   - Re-route (approver unavailable or SLA approaching — identify backup authority)
   - Outcome log (decision received — record in CRM and update discount frequency report)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user submitting a deal for desk review or checking status
   2. Read deal fields from HubSpot — deal link, ACV, discount %, close date, rep required
   3. Run sub-skills: discount-threshold-monitoring, non-standard-terms-detection,
      revenue-leakage-scanning to assemble context brief
   4. Route to correct approval authority per discount tier from company profile
   5. Apply G1 — desk review does not constitute deal approval or revenue commitment
   6. Track SLA — flag breach to #revops-ops; 24h standard / 4h final 2 weeks of quarter

3. **EXPERT CHECK**: What would a veteran RevOps deal desk analyst verify first?
   - Is the discount tier confirmed from the company profile thresholds — not estimated?
     Routing to the wrong approver tier wastes SLA time and creates audit gaps.
   - Is the context brief complete before routing? An incomplete brief (missing competitive
     context or churn signal) sends the approver back to the rep — extending SLA.
   - Is the SLA deadline calculated from submission timestamp, not discovery timestamp?
     Quarter-end 4h window starts from when the desk submission is logged.
   - Are any non-standard terms or leakage flags from sub-skills surfaced before routing?
     Approvers need the full picture in the brief — not post-routing addenda.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Approving a deal through the brief (G1 violation — desk review ≠ revenue commitment)
   - Routing without running all three sub-skills — incomplete context brief reaches approver
   - Logging a CRM update without Write-tier confirmation (G9 violation)
   - Missing the quarter-end SLA window by using wrong timestamp as SLA start
   - Omitting comp flag when deal structure has comp implications (G3 violation)

**After execution**, verify:
- G1 qualifier present: context brief does not constitute approval or revenue commitment
- G9 Write-tier confirmation gate applied to all CRM and Linear writes
- SLA deadline calculated from submission timestamp; quarter-end window identified if applicable
- Confidence: High when HubSpot is connected and all sub-skills return data; Moderate when
  any sub-skill is unavailable or deal fields are partially populated
    - Confidence: [High] when HubSpot is connected and all sub-skills return data / [Medium] when any sub-skill is unavailable or deal fields are partially populated / [Low] if all inputs are manual or unverified

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
  Assign to: [determined by discount tier from company profile]
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

## Guardrails

- Never approve deals — route only
- G1: Context brief does not constitute revenue commitment
- G9: CRM updates are Write-tier — confirm before execution
- G3: If comp implications exist in deal structure → flag for HR + Finance
