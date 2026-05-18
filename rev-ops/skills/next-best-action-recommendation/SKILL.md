---
name: next-best-action-recommendation
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Produces specific, rationale-backed interventions for deals flagged at-risk by deal-health-scoring or pipeline-velocity-tracking. Intervention types: executive sponsor escalation, competitive response, procurement/legal acceleration, CS pre-close engagement, closed/lost reclassification. Not generic nudges — every recommendation names what to do, who does it, and why. Triggers: 'next action for [deal]', 'intervention for [account]', 'what should we do with [deal]', 'stuck deal'."
---

# Next Best Action Recommendation

Specific interventions for at-risk deals. Every recommendation has a what,
a who, and a why grounded in the specific signal that triggered it.

**Reference:** Cross-skill registry → `reference/cross-skill-registry.md`
**Config reads:** `primary_segment`, `renewal_conversation_window_days`

---

## Use when
- Rep or CS manager needs a prioritized action recommendation for a specific deal or account
- Deal signals indicate risk or opportunity that warrants a specific next step
- Weekly planning requires prioritized action list across pipeline or book of business

## Do NOT use for
- Automated action execution (all recommendations require human confirmation)
- Deal approval routing (use deal-desk-workflow-management)
- Portfolio-level strategy (this is account/deal-level)

## Typical activation
"Next best action for [account/deal]", "what should I do with this deal", "prioritize my actions", "NBA for [rep]", "recommended actions for [account]"

---

## Reasoning Protocol

1. Confirm activation — user is asking about a specific at-risk deal or set of flagged deals
2. Read deal health score and triggering signal from `deal-health-scoring` output or HubSpot
3. Apply G5 — recommendations are inputs; rep and manager own the decision
4. Apply G7 — any risk flag includes an escalation path and named owner
5. Confirm whether this deal has CS implications (high ACV, implementation complexity)

---

## Intervention Types

Match recommendation to the primary signal from `deal-health-scoring`:

| Primary signal | Intervention type | Who acts |
|----------------|------------------|---------|
| No EB contact >14 days | Executive sponsor escalation | AE + AE manager |
| Competitive signal active, no counter | Competitive response play | AE + Sales Enablement |
| Late stage, legal review not started | Procurement/legal acceleration | AE + Legal/Deal Desk |
| High ACV + technical complexity | CS pre-close engagement | AE + CS leader |
| All signals degraded, 3x avg cycle time | Closed/lost reclassification review | AE manager |
| Stage stalled but activity current | Stakeholder expansion | AE |

---

## Output Format (per deal)

```
NEXT BEST ACTION — [Account Name]
[HubSpot ✓ live — as of YYYY-MM-DD]

Health score: [N]/100  ([Watch/At-risk])
ACV: $XXXk  Stage: [Stage]  Rep: [Name]

Triggering signals:
  • [Signal 1 — specific, e.g., "No economic buyer contact in 18 days"]
  • [Signal 2 — e.g., "Competitor [name] mentioned in notes on [date], no counter logged"]

Recommended action:
  WHAT: [Specific action — not generic]
  WHO:  [Rep / AE manager / CS leader / Legal]
  WHY:  [The specific signal this addresses]
  BY:   [Suggested timeframe]

If action taken, expected signal change: [What should improve and in how long]

Secondary recommendation (if applicable):
  [Same format]

[G5: Recommendation is an analytical input. [Rep] and [Manager] own the decision.]
[G7: Escalation path: [Manager name/role] via [channel] within [timeframe]]
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

- G5: Every output includes the G5 qualifier naming the rep and manager
- G7: Every at-risk flag names an escalation path and owner
- Cross-plugin: If deal has CS handoff implications, suggest `/csm:risk-flag`
