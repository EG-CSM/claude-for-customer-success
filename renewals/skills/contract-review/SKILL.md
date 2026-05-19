---
name: contract-review
description: >
  Extract and flag renewal-relevant contract terms for a specific account —
  auto-renewal mechanics, price protection clauses, termination rights, MFN
  provisions, payment terms, and data portability obligations. Surfaces the
  commercial constraints and legal requirements that must be respected before
  any renewal offer, price increase notification, or negotiation conversation
  is initiated. Output is an internal risk register, not a legal opinion. Any
  non-standard or ambiguous clause routes to Legal before a customer response
  is drafted. Use before negotiation-prep, price-increase-prep, or any renewal
  where contract terms may constrain the commercial motion.
argument-hint: "[<account-name-or-ID>] [--extract | --flag | --summary]"
version: "1.0.0"
deployment_target: plugin
---

# /renewals:contract-review [VALIDATED]

Extract the contract terms that govern this renewal before the negotiation starts.

---

## Use when
- You are preparing for a renewal, price increase, or negotiation conversation and need to know what contract constraints apply before the commercial motion begins
- An account has amendments, order forms, or SOWs beyond the base MSA and you need a consolidated view of which terms govern
- A price protection clause, MFN provision, or rate lock may exist and must be confirmed before any pricing action
- An auto-renewal notice window or quote obligation deadline may be approaching and you need to surface it before it is missed
- The prior contract review is more than 12 months old and the executed agreement should be re-verified before renewal

## Do NOT use for
- Legal interpretation of contract clauses — this skill produces a commercial risk register; ambiguous or red-flagged clauses route to Legal before any CSM action
- Drafting customer-facing contract language or counter-proposals — use `/renewals:negotiation-prep` after contract-review is complete
- Accounts where no executed contract is available — flag outputs `[Low Confidence]` and obtain the document before any commercial decision
- Price increase analysis — always run contract-review first to surface any price cap, then proceed to `/renewals:price-increase-prep`

## Typical Activation
> `/renewals:contract-review Meridian Health` — full extraction of all renewal-relevant terms for a named account
> `/renewals:contract-review Meridian Health --flag` — targeted pass: deviations from standard terms and Legal-routing clauses only
> `/renewals:contract-review Meridian Health --summary` — two-page executive summary of key dates, price constraints, and top 3 risks for a pre-call quick reference

---

## Pre-flight

Read both configuration files before running any contract review:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from config:
- Standard contract terms (the baseline — deviations are flagged)
- Pricing model and standard increase policy (to check against price caps)
- Customer segments (to calibrate what non-standard terms are common for the segment)
- Escalation matrix (for Legal routing on flagged clauses)
- AE partner (co-owner on strategic accounts with complex contract terms)

If config is missing or contains `[PLACEHOLDER]` markers in standard contract term fields:
> "Standard contract terms aren't configured — this review will flag what's present
> in the contract but cannot identify deviations from your standard. Run
> `/renewals:cold-start-interview --section contracts` to configure your baseline."

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of contract review request is this?
   - **Standard Renewal Extraction**: Executed MSA, no amendments, standard terms, adequate notice window. Full eight-category pass — non-standard terms hide in exhibits.
   - **Amended or Multi-Document**: MSA plus amendments, order forms, or SOWs. Amendment language governs where it conflicts — build consolidated term view before extracting.
   - **Price-Constrained Renewal**: Price caps, CPI linkage, MFN, or rate locks present. Extract exact constraint mechanics and validate against any proposed increase before commercial action.
   - **Time-Critical Review**: Auto-renewal notice, quote obligation, or price increase deadline inside 60 days. Surface every date-sensitive obligation first; escalate anything inside 30 days before completing the full extraction.
   - **Unverified Source**: No executed contract — working from notes, summaries, or partial uploads. Flag all outputs `[Low Confidence]` and block commercial decisions until signed document is obtained.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: This output is a commercial risk register, not a legal opinion — never interpret contract language as legal advice or present clause analysis as a legal conclusion.
   - G2: Amendments govern where they conflict with the MSA — never extract terms from the MSA alone when amendments exist; confirm amendment count before starting.
   - G4: All red-flag clauses route through the configured escalation matrix to Legal with named owner, channel, and SLA — no generic "check with Legal."
   - G5: Contract terms, ARR, and risk flags are internal-only — confidentiality check required before any output leaves the CSM's view.
   - G7: Flag stale contract data with source date and staleness indicator — contract system data >7 days, uploaded documents flagged if version currency is unconfirmed.

3. **EXPERT CHECK**: What would a veteran contracts reviewer verify first?
   - Are all amendments pulled and reviewed, or is this an MSA-only extraction that may reflect superseded terms?
   - Is there a price protection clause that must be confirmed before any price-increase-prep or negotiation-prep runs downstream?
   - Are there hard deadlines (auto-renewal notice, quote obligation, price increase notification) inside 60 days that require immediate surfacing before the full extraction completes?

4. **ANTI-PATTERNS**: Common contract review mistakes to avoid:
   - Extracting from the MSA without incorporating amendments — produces a risk register built on superseded terms.
   - Skipping Category 7 (non-standard terms) or Category 8 (governing law) because the contract "looks standard" — buried clauses create renewal liability.
   - Treating an MFN clause as a single-account yellow flag instead of routing immediately to Legal and Head of CS — MFN has book-wide pricing implications.
   - Producing crisp, structured output from unverified sources (notes, verbal accounts) that reads as authoritative — inflates confidence and enables bad commercial decisions.
   - Surfacing a deadline inside 30 days in the body of the report instead of escalating immediately to the configured escalation owner.
   - Running price-increase-prep or negotiation-prep without confirming whether a price protection clause exists — sequence is non-negotiable.

**After execution**, verify:
- Does the risk register cover all eight term categories, or were any skipped?
- Are all red-flag clauses routed to Legal with specific clause references, not generic routing?
- Are all date-sensitive obligations converted to specific calendar dates with days-remaining counts?
- Confidence: [Verified] if pulled from contract system and cross-referenced / [Moderate] if uploaded document, version unconfirmed / [Low Confidence] if working from notes or verbal accounts — state which and why.
    - Confidence: [High] when executed contract confirmed and cross-referenced / [Medium] when uploaded document with unconfirmed version / [Low] if working from notes or verbal accounts

## This Skill vs. Other Renewals Skills

**`/renewals:contract-review`** — Use first, when contract terms may constrain the
commercial motion. Output: internal risk register of clause-level constraints and flags.

**`/renewals:negotiation-prep`** — Use after contract-review when terms are understood.
Contract-review inputs feed directly into the pricing anchor and walk-away sections.

**`/renewals:price-increase-prep`** — Always run contract-review first if any account
has a price protection clause. A price increase issued against a contract with a valid
price cap is a legal and relationship risk.

---

## Mode

`--extract` (default): Full clause-by-clause extraction of all renewal-relevant terms.
Structures each clause with its location, language summary, renewal implication, and
risk flag. Use when reviewing a contract for the first time or when the prior review
is more than 12 months old.

`--flag`: Targeted pass — surfaces only clauses that deviate from your standard terms
or that require Legal review before the renewal motion proceeds. Use when you have an
existing extraction and need a quick check on specific risk areas.

`--summary`: Two-page executive summary of renewal constraints — key dates, price
constraints, termination rights, and the top 3 risks. Use when preparing for a
negotiation call and you need a quick reference rather than the full extraction.

---

## Contract source and data pull

Ask: "Which account's contract are you reviewing? Provide the account name, and attach
the contract or tell me where it's stored."

If a contract management connector is available (DocuSign / Ironclad / Conga / Salesforce
CPQ), pull:
- Executed master agreement and any amendments
- Active order forms or statements of work
- Prior renewal agreements (amendments that changed the original terms)
- Contract effective date and current term end date

Confirm the pull:
> "[Contract system]: [account name] · MSA executed [date] · [N] amendments ·
> term end: [date] · data as of [timestamp]"

If no connector is available:
> "No contract connector is configured. Attach the executed contract or paste the
> relevant clauses. If you don't have the contract, request it from Legal or
> RevOps before continuing — proceeding without the actual contract creates legal risk."

> ⚠️ Working from memory or summary notes rather than the executed contract:
> "This review is based on [notes / prior summary / verbal account] — not the
> executed contract. Flag all outputs `[Low Confidence]` until verified against
> the signed document. Do not use this review to make any commercial decision
> without Legal confirming the actual contract language."

---

## Clause extraction — eight term categories

Extract terms across eight categories. For each clause found, record:

| Field | Content |
|-------|---------|
| Clause type | [Category from list below] |
| Contract section | [Section number or exhibit] |
| Language summary | [Plain-English summary — not verbatim; verbatim excerpt for critical clauses] |
| Renewal implication | [What this means for the renewal motion] |
| Risk flag | [🟢 Standard / 🟡 Requires attention / 🔴 Legal review required] |
| Action required | [Specific action before renewal proceeds] |

---

### Category 1 — Auto-renewal mechanics

The auto-renewal clause defines whether the contract renews automatically, on what
terms, and what's required to prevent renewal.

Extract:
- **Renewal trigger:** Does the contract auto-renew, require affirmative renewal, or
  expire without action?
- **Notice period:** How many days before term end must a non-renewal notice be delivered?
- **Renewal term:** Does it renew for the same term (e.g., 1 year) or a different period?
- **Pricing on auto-renewal:** Does it renew at the same price, at a defined increase,
  or at then-current list price?
- **Notice method:** Written notice only? Email? Specific recipient required?

Risk flags:
- 🔴 Notice period inside 60 days and renewal is approaching: "Auto-renewal notice
  deadline is [date] — [N] days from now. Miss this window and the contract renews
  under current terms with no commercial opportunity."
- 🟡 Auto-renews at then-current list price: "If rates have changed since this
  contract was signed, auto-renewal may trigger a price change the customer isn't
  expecting. Confirm pricing before the renewal notice window closes."
- 🟢 Standard auto-renewal with >90-day notice window: routine management.

---

### Category 2 — Price protection clauses

Price caps, CPI links, and rate locks that constrain what the company can charge at renewal.

Extract:
- **Rate lock:** Is the price fixed for the term? For multiple terms?
- **Price cap:** Is there a maximum % increase the company can apply at renewal?
- **CPI linkage:** Is the increase tied to a specific CPI index? Which one? Which period?
- **MFN (Most Favored Nation):** Does the customer have a right to the lowest price
  offered to any similarly-situated customer?
- **Expansion pricing:** Are expanded seats or usage covered by the same protections?

Risk flags:
- 🔴 MFN clause present: "Route to Legal before issuing any price increase or
  discount to other accounts. An MFN clause may require matching the lowest price
  offered to any comparable customer."
- 🔴 Price cap constrains proposed increase: "Proposed [X]% increase exceeds the
  contractual cap of [Y]%. The increase cannot exceed [Y]% without a contract amendment.
  Run `/renewals:price-increase-prep` after confirming the legal ceiling."
- 🟡 CPI linkage: "Confirm the applicable CPI index and the measurement period before
  issuing any increase notification. Incorrect CPI application is a contract breach."
- 🟢 No price protection; standard renewal pricing applies.

---

### Category 3 — Termination rights

The conditions under which either party can end the contract before or at renewal.

Extract:
- **Termination for cause:** What constitutes cause? What's the cure period?
- **Termination for convenience:** Can either party terminate without cause? What's
  the notice period? Is there a penalty or obligation?
- **Termination for non-renewal:** What happens if the customer sends a non-renewal
  notice? Is there a wind-down period? Data export rights?
- **Survival clauses:** What obligations survive termination (confidentiality, payment,
  data deletion timelines)?

Risk flags:
- 🔴 Termination for convenience with short notice: "Customer can terminate with
  [N]-day notice. If they're at-risk, this clause removes the typical renewal runway.
  Flag for `/renewals:risk-assessment` immediately."
- 🟡 Cure period on cause-based termination: "If a support issue or SLA miss is
  unresolved, confirm no cure period has been triggered before the renewal call."
- 🟢 Standard termination clauses with ≥30-day notice.

---

### Category 4 — Renewal notice obligations (company side)

Obligations the company must fulfill before or at renewal — not just notice the customer
sends, but obligations that fall on the company.

Extract:
- **Renewal quote delivery:** Is the company obligated to deliver a renewal quote N
  days before expiration?
- **Price increase notification:** Is there a required notice period before a price
  increase takes effect?
- **Change of terms notification:** Must the company notify the customer if renewal
  terms differ from the prior term?
- **Contact requirement:** Must the renewal notice go to a specific contact or title?

Risk flags:
- 🔴 Renewal quote obligation not yet fulfilled: "Contract requires renewal quote
  delivery by [date] — [N] days out. If this deadline passes without delivery,
  the auto-renewal or expiration terms may govern."
- 🟡 Price increase notice period in contract: "The contract requires [N]-day
  advance notice for price increases — which differs from your standard [N]-day
  window. Use the contract's requirement, not the standard."
- 🟢 No company-side notice obligations beyond standard practice.

---

### Category 5 — Payment terms and financial obligations

The financial mechanics that govern the renewal transaction.

Extract:
- **Payment terms:** Net 30, Net 60, or other? Does this differ from company standard?
- **Invoice timing:** When must the invoice be issued relative to the renewal term start?
- **Late payment:** Are there late fees? Interest on overdue amounts?
- **Prepayment or multi-year structure:** If the account is on a multi-year deal, how
  are future-year payments structured? Are they obligated or optional?
- **Taxes:** Who is responsible for taxes on the renewal? Any tax exemption certificates?
- **Refund or credit terms:** Under what conditions does the company owe a refund or credit?

Risk flags:
- 🟡 Payment terms longer than company standard: "Net [60/90] payment terms — confirm
  RevOps has accounted for this in the renewal pipeline timing. Revenue recognition
  may differ from the contract start date."
- 🟡 Late payment clause with penalty: "Outstanding invoice from [date] may be
  accruing interest. Resolve before issuing the renewal — an open balance dispute
  during negotiation is a risk."
- 🟢 Standard payment terms.

---

### Category 6 — Data portability and transition obligations

What the company must provide if the customer does not renew — this affects the churn
conversation and the walk-away posture.

Extract:
- **Data export:** Must the company provide the customer's data in a portable format?
  In what format? Within what timeframe?
- **Transition assistance:** Is there an obligation to assist with data migration or
  transition to a successor vendor?
- **Data deletion:** When must the company delete or destroy customer data post-termination?
  What certification is required?
- **Data access during transition:** Does the customer retain read access to the product
  after term end for any period?

Risk flags:
- 🔴 Transition assistance obligation: "Contract requires [N days / months] of
  transition support post-termination. This is a cost obligation if the account
  churns — flag for Head of CS and Finance if this account is at-risk."
- 🟡 Data export obligation with specific format requirement: "Customer has a right
  to data export in [format] within [N] days of termination. Confirm the technical
  team can fulfill this before the churn conversation occurs."
- 🟢 Standard data deletion with no transition assistance obligations.

---

### Category 7 — Non-standard or custom terms

Terms that deviate from the company's standard agreement — these often represent
past concessions that constrain the renewal motion.

Extract any clauses that differ from configured standard terms:
- Custom SLA commitments (uptime guarantees, response time SLAs)
- Dedicated support or CSM commitments
- Feature development commitments or roadmap commitments
- Custom data residency or security requirements
- Liability caps that differ from standard
- Intellectual property terms that differ from standard
- Non-solicitation or non-compete provisions

Risk flags:
- 🔴 Roadmap or feature commitment in contract: "Contract includes a commitment to
  deliver [feature/capability] by [date]. Confirm with Product whether this commitment
  has been met before the renewal conversation — an unmet commitment in an active
  contract is a material negotiation liability."
- 🔴 Custom SLA with penalty: "SLA includes financial penalties for [metric] breaches.
  Pull SLA performance data before the renewal call."
- 🟡 Custom term requiring Legal review: "Non-standard [term type] — route to Legal
  before making any renewal commitment that touches this clause."
- 🟢 No material deviations from standard.

---

### Category 8 — Governing law and dispute resolution

Not a primary negotiation factor, but relevant if the renewal becomes adversarial.

Extract:
- **Governing law:** Which jurisdiction's law applies?
- **Dispute resolution:** Arbitration? Litigation? Where?
- **Notice requirements for disputes:** Formal notice required before legal action?

Risk flags:
- 🟡 Governing law differs from company headquarters jurisdiction: "Flag to Legal
  if renewal negotiations become adversarial — the applicable law affects dispute
  resolution options."
- 🟢 Standard governing law and dispute resolution.

---

## Legal routing decision

After extraction, assess whether the renewal can proceed without Legal review.

**Legal review required (🔴 flags) — stop and route before proceeding:**
- MFN clause present
- Price cap constrains proposed increase
- Contractual feature or roadmap commitment unverified
- Termination for convenience notice active or imminent
- Custom SLA with financial penalties — pull performance data first
- Transition assistance obligation on an at-risk account
- Any clause the CSM cannot confidently interpret

**Proceed with caution (🟡 flags) — document and monitor:**
- CPI linkage — verify before increase notification
- Non-standard payment terms — flag to RevOps
- Custom SLA without penalties — verify performance
- Notice window approaching within 30 days

**Proceed normally (🟢 flags):**
- Standard terms across all categories — proceed with standard renewal motion

> "This output is an internal commercial risk register — it is not a legal opinion.
> Any 🔴 flag requires Legal review before the CSM responds to the customer on that
> term. Do not interpret contract language to a customer without Legal sign-off."

---

## Output format

---

**Contract Review — [Account Name]**
*Contract date: [MSA execution date] · Amendment [N]: [date] · Term end: [date]*
*Reviewed: [date] · Sources: [contract system ✓ verified | uploaded document | manual input]*

**Renewal constraints summary:**

| Constraint | Detail | Risk | Action |
|-----------|--------|------|--------|
| Auto-renewal | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Price protection | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Termination rights | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Notice obligations | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Payment terms | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Data portability | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Non-standard terms | [Summary] | 🟢/🟡/🔴 | [Action or none] |
| Governing law | [Summary] | 🟢/🟡/🔴 | [Action or none] |

**Legal routing:** [Proceed normally / Proceed with caution — [flags listed] /
⚠️ Legal review required before proceeding — [specific clauses]]

**Critical dates:**
- Auto-renewal notice deadline: [date] — [N] days out
- Renewal quote obligation (if any): [date] — [N] days out
- Price increase notice deadline (if any): [date] — [N] days out

**Full clause extraction:**
[Table per category above, for any non-green flags]

**Recommended next steps:**
1. [Legal routing action, if required]
2. [Date-sensitive action first]
3. [Commercial motion action — proceed to negotiation-prep / price-increase-prep]

---

> ⚠️ Reviewer note
> - **Sources:** [Contract system ✓ verified | uploaded document — unverified extract |
>   manual input — [Low Confidence]]
> - **Data as of:** [timestamp | N/A — static contract]
> - **Contract version reviewed:** [MSA date] + [Amendment N, date]
> - **Flagged for your judgment:** [🔴 flags requiring Legal routing | 🟡 flags
>   requiring monitoring | none]
> - **Before proceeding:** This is a commercial risk register, not a legal opinion.
>   All 🔴 flags require Legal review. Do not respond to a customer about a flagged
>   clause without Legal sign-off.
> - **Confidence:** [Verified — pulled from contract system / Moderate — uploaded
>   document, not cross-referenced / Low Confidence — working from notes, not
>   executed contract]

---

> [review before sending]

---

## Security & Permissions

```
network:        none — no direct HTTP calls; contract management connector (DocuSign/Ironclad/
                Conga/Salesforce CPQ) operates via MCP, not filesystem reads by this skill
read_scope:     ~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md and
                ~/.claude/plugins/config/claude-for-customer-success/company-profile.md only
write_scope:    none — all output to conversation; no file writes
subprocess:     none
dynamic_code:   none — no eval, no exec, no runtime code execution
```

This skill reads two plugin config files at session start (Pre-flight) and produces all output directly in the conversation. Contract documents are provided by the operator via an attached file or contract management MCP connector — this skill does not read contracts from the filesystem independently. It does not write any files, make direct network calls, or persist data between sessions.

---

## Trust & Verification

**Contract source handling:**
Contract documents and extracted terms are provided through operator-controlled MCP connectors or direct file attachment. This skill does not access contract management systems independently of the session context. Source provenance (contract system vs. uploaded document vs. notes) is declared explicitly in the Reviewer note and governs the confidence signal applied to all extracted terms.

**Legal boundary enforcement:**
This skill produces a commercial risk register — clause extraction and risk flagging, not legal interpretation. All outputs carry an explicit disclaimer that they do not constitute legal advice. Red-flag clauses are routed to Legal via the configured escalation matrix; the skill does not provide legal conclusions to the CSM or to the customer.

**Free-text field handling:**
`account_name`, contract text, and all manual inputs are treated as display data. They are not executed, evaluated, or used to derive file paths or system behavior.

**Confidence signal discipline:**
All term extractions carry explicit confidence signals tied to source quality. `[Low Confidence]` is applied to any extraction from notes, verbal accounts, or unverified documents. The skill will not suppress confidence signals to produce cleaner-looking output.

**Confidentiality boundary:**
Contract terms, ARR, and risk flags are internal-only. The Reviewer note requires a confidentiality confirmation before any output leaves the CSM's view. This skill never formats output for direct customer sharing.

---

## Guardrails

**Not a legal opinion.** This output identifies commercial risk areas — it does not
constitute legal advice. Any clause that is ambiguous, non-standard, or flagged 🔴
routes to Legal before the CSM takes action. The CSM does not interpret contract
language to the customer without Legal sign-off.

**Executed contract only.** Contract review must be based on the signed, executed
agreement — not term sheets, proposals, emails, or verbal accounts of the terms.
If the executed contract is unavailable, flag all outputs `[Low Confidence]` and
obtain the document before making any commercial decision.

**Amendments govern.** If the account has amendments, the amendment language controls
where it conflicts with the MSA. Always pull and review all amendments before extracting
terms — an MSA-only review of an amended contract produces unreliable output.

**Price cap before price increase.** Any account where a price protection clause exists
requires contract-review output before `/renewals:price-increase-prep` is run. Issuing
a price increase that exceeds a contractual cap is a breach — this check is non-negotiable.

**MFN clauses require immediate Legal routing.** An MFN clause affects pricing
decisions across the entire book, not just this account. Flag immediately to Legal
and Head of CS — do not proceed with any discount or pricing decision on any account
until the MFN implications are understood.

**Auto-renewal deadlines are hard deadlines.** A missed auto-renewal notice window
removes the commercial opportunity for that renewal cycle. If the notice deadline is
inside 30 days, escalate immediately to the configured escalation owner — do not
let this slip in the queue.

**Feature and roadmap commitments in contracts are material liabilities.** A renewal
conversation that proceeds without surfacing an unmet contractual feature commitment
creates legal exposure. Always pull and verify roadmap commitments before the renewal
call.

**Route non-standard terms to Legal, not to the customer.** If the customer asks
about a non-standard clause during the renewal, the response is: "Let me confirm
the details with our team and come back to you." Do not improvise contract
interpretation on a live call.

---

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill
