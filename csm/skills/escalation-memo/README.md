# csm.escalation-memo

Manages the full escalation lifecycle — opening, updating, and closing escalation memos for technical, complaint, executive, and internal escalation types. Routes to the correct escalation path per the configured escalation matrix.

## Use it for

- Open a new escalation memo
- Update an in-progress escalation with new information
- Close an escalation with resolution summary

## Don't use it for

- Churn risk assessment (use renewals.risk-assessment)
- Escalation routing decisions (governed by company profile matrix)

## How to trigger it

Say something like:

- "escalation memo"
- "open an escalation"
- "escalate this account"
- "update escalation"
- "close escalation"

## What you get

- Escalation memo (structured markdown)
- Routing recommendation per escalation matrix

## Prerequisites

- csm CLAUDE.md
- Account context and escalation details

## Governance

**Approval required** — output must be reviewed before distribution.
- Escalation routing follows configured matrix — not overridden by user instruction
- Executive escalations require CS leadership acknowledgment

## See also

- csm.risk-flag
- renewals.risk-assessment

---

*Domain: `csm` · Skill ID: `csm.escalation-memo`*
