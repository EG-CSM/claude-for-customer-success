# renewals.contract-review

Extracts and risk-flags key contract terms across eight categories. Applies a 🟢/🟡/🔴 risk system; MFN clauses always trigger 🔴 + Legal escalation. Must run before negotiation-prep and price-increase-prep for any account.

## Use it for

- Pre-renewal contract term extraction
- Risk flagging of non-standard terms
- Pre-negotiation brief preparation
- Price protection and MFN clause identification

## Don't use it for

- Legal advice or binding legal interpretation
- Contract redlining or drafting (Legal team function)
- New logo contract review (sales domain)

## How to trigger it

Say something like:

- "review the contract for [account]"
- "what are the renewal terms"
- "check for MFN clause"
- "price protection check"
- "--extract"
- "--flag"
- "--summary"

## What you get

- Contract term extraction table (8 categories)
- Risk flag summary (🟢/🟡/🔴 by term)
- Escalation notice (if 🔴 findings present)

## Prerequisites

- Domain CLAUDE.md
- Contract document (PDF, text, or pasted content)
- Account name or ID

## Governance

- MFN clause detection → always 🔴 + immediate Legal + Head of CS routing (non-negotiable)
- Output is informational only — not legal advice
- Non-standard terms require Legal review before negotiation commitment

## See also

- renewals.negotiation-prep (runs after this; requires output)
- renewals.price-increase-prep (runs after this for price-protected accounts)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.contract-review`*
