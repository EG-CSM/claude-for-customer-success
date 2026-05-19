# renewals.executive-summary

Produces a structured executive-facing account summary for renewal conversations with senior stakeholders. Three modes: brief (1-page CRO/weekly), full (extended with competitive context and exec engagement plan), board (board/investor format, strips relationship detail). ARR figures always flagged as not-yet-a-revenue-commitment.

## Use it for

- Pre-call brief for CRO or VP CS on a renewal account
- Board or investor update on strategic accounts
- Full account narrative for QBR executive prep

## Don't use it for

- Detailed negotiation positioning (use negotiation-prep)
- Risk tier calculation (import from risk-assessment; never re-derive here)
- Customer-facing documents (this is internal)

## How to trigger it

Say something like:

- "executive summary for [account]"
- "CRO brief on [account]"
- "board update for [account]"
- "prep exec for renewal call"
- "--brief"
- "--full"
- "--board"

## What you get

- Executive summary document (mode-appropriate length and format)
- Bottom line (2 sentences)
- Commercial status table
- Relationship health summary
- Risk summary (imported tier)
- Recommended executive action with named ask (person/action/date)

## Prerequisites

- Domain CLAUDE.md
- Risk tier from risk-assessment (must be pre-run; not re-derived here)
- Account ARR, contract end date, key stakeholders
- Recent engagement notes or CRM activity

## Governance

**Approval required** — output must be reviewed before distribution.
- All ARR figures flagged "[review — not yet a revenue commitment]"
- Risk tier imported from risk-assessment; never re-derived in this skill
- Executive asks must name specific person, specific action, specific date — no vague asks
- Board format requires explicit user authorization before generating
- Value claims require account-specific evidence — no generic benefit statements

## See also

- renewals.risk-assessment (tier import — must run first)
- renewals.negotiation-prep (separate artifact; not combined here)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.executive-summary`*
