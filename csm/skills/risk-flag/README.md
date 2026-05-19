# csm.risk-flag

Generates a risk memo for at-risk accounts, including signal summary, risk tier, and escalation routing per the configured escalation matrix. Optionally produces a full escalation memo.

## Use it for

- Quick risk memo for an at-risk account
- Escalation memo triggered by risk signal

## Don't use it for

- Portfolio-level risk analysis (use renewals.risk-assessment)
- Full escalation lifecycle (use csm.escalation-memo)

## How to trigger it

Say something like:

- "risk flag"
- "flag this account as at-risk"
- "risk memo"
- "account is at risk"

## What you get

- Risk memo
- Escalation memo (optional)

## Prerequisites

- csm CLAUDE.md
- Account and signal context

## Governance

**Approval required** — output must be reviewed before distribution.
- Escalation routing follows configured matrix

## See also

- csm.escalation-memo
- renewals.risk-assessment
- csm.health-score-review

---

*Domain: `csm` · Skill ID: `csm.risk-flag`*
