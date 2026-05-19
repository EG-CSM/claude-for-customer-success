# renewals.price-increase-prep

Prepares a price increase plan for one account or a multi-account cohort. Produces internal plan, optional customer-facing draft notice, and objection handling prep. Approval must precede customer communication (non-negotiable). Five increase types supported; at-risk accounts require risk-assessment first.

## Use it for

- Price increase plan for a single account
- Cohort rollout table for multi-account price increase
- Customer-facing notice draft (after plan approval)
- Objection handling prep for price increase conversations

## Don't use it for

- Negotiation strategy (use negotiation-prep)
- Contract review for price-protected terms (run contract-review first)
- Discount modeling (separate from price increase logic)

## How to trigger it

Say something like:

- "price increase for [account]"
- "plan a rate increase"
- "cohort price increase"
- "draft price increase notice"
- "--plan"
- "--draft"
- "--objections"
- "--cohort"

## What you get

- Price increase plan (internal; approval status, rationale, timing, objection prep)
- Customer-facing draft email (--draft mode; after plan approval only)
- Cohort rollout table (--cohort mode)

## Prerequisites

- Domain CLAUDE.md
- Account ARR, contract end date, current rate
- Risk-assessment output if at-risk signals present
- contract-review output if price-protected account
- Approval status (required before --draft)

## Governance

**Approval required** — output must be reviewed before distribution.
- Approval required before any customer communication — non-negotiable
- No value claims without account-specific evidence
- Inside 30 days of renewal = high-risk; consult Head of CS before proceeding
- Revenue commitment language on all ARR figures
- --draft only available after --plan confirms approval
- {'At-risk accounts': 'risk-assessment required first'}
- {'Price-protected accounts': 'contract-review required first'}

## See also

- renewals.contract-review (prerequisite for price-protected accounts)
- renewals.risk-assessment (prerequisite for at-risk accounts)
- renewals.negotiation-prep (downstream if increase triggers negotiation)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.price-increase-prep`*
