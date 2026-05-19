# renewals.negotiation-prep

Prepares the renewals manager for a contract negotiation. Produces an internal brief (anchor, floor, top objections) and optionally a clean customer-facing export proposal. Requires contract-review output as input. Three locked numbers (anchor, first concession, walk-away) must be confirmed before any negotiation call.

## Use it for

- Pre-call negotiation brief preparation
- Objection bank construction
- Multi-scenario offer modeling
- Clean customer-facing proposal export

## Don't use it for

- Contract review (must run contract-review first)
- Executive positioning (use executive-summary)
- Price increase communications (use price-increase-prep)

## How to trigger it

Say something like:

- "negotiation prep for [account]"
- "prep for renewal call"
- "objection handling for [account]"
- "build negotiation brief"
- "--brief"
- "--full"
- "--export"

## What you get

- {'Negotiation brief (internal': 'opening position, walk-away, authority ceiling, top objections, recommended opening, pre-call checklist)'}
- Customer-facing export proposal (--export mode only; fully suppresses internal content)

## Prerequisites

- Domain CLAUDE.md
- contract-review output (required; blocks if not present)
- Account ARR, risk tier, key stakeholders
- Discount authority ceiling from CLAUDE.md

## Governance

- Three locked numbers (anchor, first concession, walk-away) required before any call
- Walk-away floor is not an opening offer — never present it as one
- Non-standard contract terms → Legal review required before committing
- --export mode fully suppresses all internal positioning, floor, and authority data
- No fabricated competitor intelligence — only verified data included
- Discount authority check on every scenario — ceiling from CLAUDE.md
- contract-review must have run first; skill blocks without it

## See also

- renewals.contract-review (prerequisite; must run first)
- renewals.risk-assessment (risk tier context)
- renewals.expansion-signal (if expansion in scope)
- renewals.executive-summary (separate artifact)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.negotiation-prep`*
