# rev-ops.deal-desk-workflow-management

Routes non-standard deal elements through the deal desk approval workflow. Assembles context brief from CRM and sub-agent signals, applies 5-stage approval routing (standard/elevated/executive/legal/finance), and enforces SLAs (24h standard, 4h final-2-weeks). Coordinates discount-threshold-monitoring, non-standard-terms-detection, revenue-leakage-scanning, and early-churn-downgrade-signal-detection.

## Use it for

- Identify non-standard deal elements requiring deal desk review
- Assemble deal context brief for approvers
- Route deal to correct approval tier based on discount, terms, and risk signals
- Track SLA adherence and escalate on breach
- Create Linear issues for approvals requiring written record

## Don't use it for

- Approving deals autonomously
- CRM record edits (G9)
- Final pricing decisions

## How to trigger it

Say something like:

- "deal desk"
- "approval routing"
- "non-standard deal"
- "deal needs approval"
- "route this deal for approval"

## What you get

- Deal context brief (Markdown)
- Approval routing recommendation with tier and rationale
- Linear issue for written approval record (Write-tier)

## Prerequisites

- Opportunity record from CRM
- Discount thresholds and approval tier configuration
- SLA configuration

## Governance

**Approval required** — output must be reviewed before distribution.
- {'G1': 'all ARR/revenue figures flagged [review — not yet a revenue commitment]'}
- Never approves deals autonomously
- {'G9': 'no CRM edits'}
- SLA breach triggers escalation; skill does not silently let SLAs slip

## See also

- rev-ops.discount-threshold-monitoring
- rev-ops.non-standard-terms-detection
- rev-ops.revenue-leakage-scanning
- rev-ops.sales-cs-handoff-quality-scoring

---

*Domain: `rev-ops` · Skill ID: `rev-ops.deal-desk-workflow-management`*
