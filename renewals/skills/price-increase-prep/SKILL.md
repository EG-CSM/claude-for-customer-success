---
name: price-increase-prep
description: >
  Plan and execute a price increase for a single account or a cohort of accounts
  — rationale framing, customer communication, approval routing, and objection
  handling. Validates the increase against your configured policy and escalation
  thresholds before any customer communication is drafted. Use 60–90 days before
  a renewal where a price increase applies, or when finance/leadership has directed
  a broad price adjustment. Never presents a price increase to the customer without
  a completed value narrative and confirmed approval routing.
argument-hint: "[<account-name-or-ID> | --cohort] [--plan | --draft | --objections]"
version: "1.0.0"
---

# /renewals:price-increase-prep

Plan, approve, and communicate a price increase — in the right order.

---

## Pre-flight

Read both configuration files before preparing any price increase work:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If price increase policy fields are missing or contain `[PLACEHOLDER]` markers:

> "Your price increase policy isn't configured — standard increase %, approval
> thresholds, and approval chain are required before this skill can validate
> whether a proposed increase is within your authority. Run
> `/renewals:cold-start-interview --section pricing` to configure these fields."

Fields read from config:
- Standard price increase policy (CPI / flat % / market-rate review)
- Increase approval thresholds (e.g., increases >X% require approval)
- Approval chain (who approves increases above threshold)
- Customer segments (for segment-appropriate framing)
- Negotiation posture (affects communication tone)
- AE partner (for strategic account increases requiring co-ownership)

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of price increase request is this?
   - **Standard Policy Increase**: Increase aligns with configured policy (CPI, flat %, contractual clause). Account is healthy, no contract constraints, within authority. Optimize for clear value framing and timely notification.
   - **Above-Authority Increase**: Proposed increase exceeds configured approval threshold. Must route through approval chain before any customer communication is drafted — the approval gate is non-negotiable.
   - **At-Risk Account Increase**: Account has active churn signals, declining health, or recent escalation. Requires risk assessment before increase planning — standard playbook will accelerate churn.
   - **Cohort Rollout**: Multiple accounts receiving increases simultaneously. Requires segmentation by risk, contract terms, and relationship strength — uniform treatment produces avoidable churn.
   - **Contract-Constrained Increase**: Account has price caps, MFN clauses, or CPI ceilings. Requires contract review before any communication — issuing an invalid increase is a legal and trust risk.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: Revenue figures in increase plans are targets, not closed-won commitments — tag with `[review — not yet a revenue commitment]` if shared with leadership before the renewal is signed.
   - G2: Approval routing must complete before any customer-facing communication is drafted or sent. Walking back a communicated increase damages trust and sets a negotiation precedent.
   - G4: At-risk accounts require `/renewals:risk-assessment` before inclusion in any price increase plan — do not apply standard increase logic to an account with active churn signals.
   - G5: Accounts with multi-year agreements, enterprise terms, or negotiated pricing require `/renewals:contract-review` before increase notification — assume price protection exists until confirmed otherwise.
   - G7: Value claims in customer communication must be substantiated with account-specific evidence — generic value language that doesn't match the customer's experience undermines credibility at the worst moment.

3. **EXPERT CHECK**: What would a veteran renewals leader verify first?
   - Is the increase within authority, or does it need approval? Check the threshold before anything else — drafting before approval creates momentum toward a message you may not be authorized to send.
   - Does the contract contain price protection clauses? A price cap or MFN clause makes the proposed increase partially or fully invalid — verify before calculating impact.
   - What's the account's risk posture right now? A price increase on a healthy account is a conversation; on an at-risk account it's a potential churn trigger. Check health signals before planning.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Drafting customer communication before approval is confirmed — the `--draft` mode should only run after `--plan` confirms the approval gate is clear.
   - Applying the same increase framing to at-risk and healthy accounts — at-risk accounts need a fundamentally different strategy, not a softer version of the standard email.
   - Using value rationale that isn't substantiated by account-specific evidence — customers detect hollow justification and it damages trust at a moment that demands credibility.
   - Including contract-protected accounts in a cohort rollout without individual contract review — one invalid increase notice undermines the entire rollout's credibility.
   - Notifying inside 30 days without leadership sign-off — compressed timelines remove negotiation room and accelerate churn decisions.
   - Offering concessions (deferrals, rate locks, phased increases) without understanding the actual objection — price resistance often masks a value or relationship problem that a discount won't solve.

**After execution**, verify:
- Does the plan address the right type (standard / above-authority / at-risk / cohort / contract-constrained)?
- Is the approval gate resolved before any customer-facing output was produced?
- Are all ARR figures flagged as targets, not commitments, if shared beyond the CSM?
- Confidence: [High] if CRM data + contract terms confirmed and within 7 days / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

## Mode

`--plan` (default): Build the increase plan — rationale, approval routing, timing,
and account-specific impact. Does not draft customer communication. Use first to
confirm the increase is approvable before drafting anything.

`--draft`: Produce the customer-facing communication for the price increase.
Runs after `--plan` confirms approval routing. Requires the account context and
value narrative to be available before drafting.

`--objections`: Surface the top objections to this price increase with tailored
response frameworks. Use in preparation for the customer conversation after the
increase notification is sent.

`--cohort`: Apply to a list of accounts instead of a single account. Collects
cohort data, groups by segment and increase tier, and produces a rollout plan
with prioritized communication sequencing.

---

## Account identification and impact calculation

Ask: "Which account (or accounts for `--cohort`) is this price increase for?
Provide the account name, current ARR, renewal date, and proposed increase."

If a CRM connector is available, pull:
- Current ARR and product tier
- Renewal date and days remaining
- Expansion history (prior increases accepted — signals price tolerance)
- Risk signals (any active churn indicators — a price increase on an at-risk account
  requires a different strategy)
- Contract terms (price caps or MFN clauses in the existing agreement)

Confirm the pull:
> "[CRM]: [account name] · $[current ARR] ARR · renewal [date] · [N] days out ·
> [expansion history summary] · data as of [timestamp]"

### Impact calculation

| | Current | Proposed |
|--|---------|---------|
| ARR | $[current] | $[proposed] |
| Increase amount | — | $[delta] |
| Increase % | — | [%] |
| Approval required? | — | [Yes — route to [owner] / No — within authority] |

> Flag immediately if a price cap or MFN clause exists in the contract:
> "⚠️ Contract review required: this account's contract may contain a price
> protection clause. Confirm with Legal before issuing the increase notification.
> Run `/renewals:contract-review` to extract relevant contract terms."

---

## Approval routing

Before any customer communication is drafted, validate the increase against
the configured approval thresholds.

| Increase % | Threshold | Status | Action |
|-----------|----------|--------|--------|
| [proposed %] | [configured approval threshold] | ✅ Within authority / ⚠️ Requires approval | [proceed / route to [owner]] |

If approval is required:
> "This increase exceeds your configured authority threshold of [threshold].
> Submit for approval to [configured owner] via [method] before drafting
> customer communication. Do not send an increase notice without approval —
> if the increase is later walked back, it damages credibility."

If within authority:
> "This increase is within your configured authority. No approval required
> before proceeding to customer communication."

### What to include in the approval request (if needed)

- Account name and current ARR
- Proposed increase % and new ARR
- Renewal date
- Rationale (see below)
- Risk assessment: is the account at risk? Is this increase likely to trigger
  a churn conversation?
- Recommended communication timing and approach

---

## Rationale framing

Build the rationale before the customer communication. The rationale must be
honest, specific, and tied to value — not to internal cost pressures that the
customer has no visibility into.

### Rationale options (select those that apply honestly)

**Product investment rationale:** "We've made significant investments in [feature
area / infrastructure / security / support capacity] since your last renewal.
The updated pricing reflects the expanded capabilities and value you're receiving."

**Market adjustment rationale:** "Our pricing has been held flat for [N] years.
The adjustment aligns with market rates for [product category] and ensures we
can continue investing in the product roadmap."

**Usage and growth rationale:** "Your team's usage has grown [X]% over the past
year [if data supports this]. The new pricing reflects the expanded footprint and
value being delivered."

**CPI / contractual adjustment rationale:** "This adjustment applies the standard
[CPI / contractual escalation clause] defined in your agreement."

> Do not use a rationale you cannot substantiate with evidence. If the honest
> answer is "we're raising prices broadly," say so plainly — customers respond
> better to directness than to value framing that doesn't match their experience.

### Rationale to avoid

- "Our costs have increased" — rarely resonates; shifts focus to your margins
- "All our customers are getting this increase" — removes any sense of
  individual consideration
- "Our product is worth more" — true but not a customer-facing argument without
  substantiation
- Competitor pricing comparisons — opens a comparison conversation you may not
  want

---

## Customer communication — `--draft` mode

Produce the customer-facing notice. This communication must be:
- Clear about the new amount and effective date
- Honest about the rationale (no fabricated value claims)
- Forward-looking — focused on what they're getting, not what's changing
- Action-oriented — what the customer needs to do and by when

---

**[Subject line options — pick one]:**
- "Your [Product] renewal — updated investment for [Year]"
- "Upcoming renewal: a note from your Customer Success team"
- "Renewing with [Company] — what's changing and why"

---

**[Email body]**

Hi [Champion name],

I wanted to reach out ahead of your [Month Year] renewal to give you visibility
into what to expect.

Starting with your [date] renewal, the annual investment for your [tier /
seat count] will be **$[new ARR]/year** — an increase of [X]% from your current
rate of $[current ARR]/year.

**Why this change:**
[2–3 sentences of honest, substantiated rationale from the options above.
Do not fabricate. If no strong rationale applies, the plain-language version
is: "We've held pricing flat for [N] years, and this adjustment reflects where
the market has moved."]

**What hasn't changed:**
Your [current tier / seat count / feature access] remains the same. Your [CSM
name] and support contact remain the same. [If applicable: your contract terms
remain the same.]

**What you need to do:**
Nothing immediately — your CSM will reach out to walk through the renewal and
answer any questions. If you'd prefer to discuss this ahead of that conversation,
reply here and we'll set up time.

[Your name]
[Title]

---

> ⚠️ Before sending this draft:
> - [ ] Confirm approval routing is complete (if increase exceeded authority)
> - [ ] Confirm the new ARR figure is correct
> - [ ] Confirm the effective date
> - [ ] Confirm no contract price protection clause exists for this account
> - [ ] Confirm the customer's primary contact is current (no recent
>       stakeholder changes that haven't been updated in CRM)

---

## Timing guidance

| Renewal date proximity | Recommended notification window |
|----------------------|-------------------------------|
| 90+ days out | Notify now — gives maximum runway for objections and negotiation |
| 60–90 days out | Notify immediately — standard window |
| 30–60 days out | Notify now — compress the timeline; escalate if churn risk is present |
| <30 days out | Consult with AE partner and Head of CS before notifying — late notifications on price increases are high-risk |

If the notification is inside 30 days:
> "⚠️ Price increase notification inside 30 days of renewal is high-risk. The
> customer has limited time to process the change, and it can trigger an
> escalation or churn conversation that's avoidable with earlier timing. Consult
> [configured Head of CS / AE partner] before proceeding."

---

## Objection handling — `--objections` mode

Surface the most common objections to price increases and the responses calibrated
to this account.

### Objection — "We weren't expecting a price increase"

**Most likely if:** Increase isn't contractually defined; customer hasn't seen
an increase before; notification came late.

**Response:** "I understand this may have caught you off guard — I apologize
for not getting ahead of this sooner. [If applicable: This is in line with
[CPI clause / our standard adjustment policy].] I'd like to walk you through
what's behind it and make sure you feel good about the value you're getting."

Do not backpedal on the increase at the first objection. Acknowledge the
surprise; do not immediately offer to waive or reduce without understanding
the actual concern.

---

### Objection — "We can't absorb the increase this year"

**Most likely if:** Budget freeze mentioned previously; no expansion history;
account flagged as cost-sensitive.

**Response options (in order of preference):**
1. Multi-year lock-in: Offer to hold the current rate for a 2-year term.
   "If budget certainty is the concern, we can lock in your current rate through
   [date] in exchange for a 2-year commitment."
2. Phased increase: "We could apply half the increase this year and the remainder
   at next renewal — would that work for your budget cycle?"
3. Defer to next cycle: For strategic accounts, consult with AE partner before
   offering a deferral. A deferral sets a precedent.

> Any rate lock or deferral beyond your configured authority requires approval
> before presenting to the customer.

---

### Objection — "We'll need to evaluate our options"

**Most likely if:** Competitor evaluation was already in progress; relationship
is strained; economic buyer is newly engaged and hasn't built trust.

**Response:**
1. Don't panic. "I'd want you to feel confident in your decision. What would
   make this an easy yes?"
2. Ask what's driving the evaluation: Is it the price, or something else that
   the price increase surfaced?
3. Escalate to `/renewals:risk-assessment` — a price objection combined with
   a competitive mention is a High or Critical risk signal, not a negotiation tactic.

---

### Objection — "Can you justify this increase?"

**Most likely if:** Economic buyer is newly engaged; account has had support issues;
usage has been flat.

**Response:** Come with evidence, not confidence. "Let me pull together [usage
trends / outcomes achieved / ROI data] for your team. Can we set up 30 minutes
to walk through what the product has delivered for you this year? That conversation
will give us both a better foundation for the renewal."

If usage is genuinely flat and value evidence is thin:
> Internal note: a price increase on a low-adoption account with thin value evidence
> is high-risk. Consider whether the increase is worth the churn exposure. Consult
> with AE partner or Head of CS before proceeding.

---

## Cohort mode (`--cohort`)

For multi-account price increase rollouts:

1. Collect account list: name, ARR, renewal date, segment, current price tier
2. Group by segment and increase tier
3. Prioritize notification sequence: accounts with the earliest renewal dates first;
   at-risk accounts require a separate strategy (consult Head of CS before increasing)
4. Identify accounts requiring approval (increase % above authority threshold)
5. Flag contract review needs (accounts with known price protection clauses)

### Cohort rollout plan format

| Account | ARR | Increase % | New ARR | Renewal date | Priority | Approval needed? | Contract check? |
|---------|-----|-----------|---------|-------------|---------|-----------------|----------------|
| [Name] | $[ARR] | [%] | $[new] | [date] | [1-N] | [Y/N] | [Y/N] |

> Segment at-risk accounts separately — a price increase on an account with
> active churn signals requires `/renewals:risk-assessment` before notification.
> Do not include at-risk accounts in a broad cohort rollout without individual
> review.

---

## Output format

---

**Price Increase Plan — [Account Name / Cohort]**
*Current ARR: $[amount] · Proposed ARR: $[amount] · [+X%]*
*Renewal: [date] · Notification target: [date]*
*Prepared: [date] · Sources: [list]*

**Approval status:** [Within authority — proceed / ⚠️ Requires [owner] approval]

**Rationale selected:** [Summary of chosen rationale]

**Communication timing:** [Recommended notification date and rationale]

**Objections to prepare for:** [Top 2–3 for this account based on signals]

**Next actions:**
1. [Obtain approval if required]
2. [Send notification by target date]
3. [Schedule follow-up call with champion]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | manual input]
> - **Data as of:** [timestamp | N/A]
> - **Read:** [account record | contract terms | expansion history]
> - **Flagged for your judgment:** [contract price protection check needed |
>   at-risk account — recommend risk assessment before proceeding | none]
> - **Before sending:** Confirm approval is in place and contract permits the
>   increase — this check is non-negotiable

---

## Guardrails

**Approval before communication.** Do not draft or send a price increase notice
without confirming the increase is within authority or has been approved.
The approval check is not a formality — walking back a communicated increase
damages trust and sets a negotiation precedent.

**Contract review for price-protected accounts.** Any account that may have a
price cap, CPI cap, or MFN clause in its contract requires `/renewals:contract-review`
before the increase notification is issued. Issuing an invalid increase notice
is a legal and relationship risk.

**No value claims without evidence.** Do not include value assertions in the
customer communication that aren't supported by account-specific data. Generic
value language that doesn't match the customer's experience undermines credibility
at a moment that requires it most.

**At-risk accounts need separate strategy.** A price increase on an account
with active churn signals is a different conversation from a standard renewal
increase. Always check risk signals before including an account in a price
increase plan. If churn risk is present, run `/renewals:risk-assessment` first.

**Late notifications are high-risk.** Inside 30 days, consult Head of CS before
notifying. The compressed timeline removes room for negotiation and can accelerate
a churn decision.

**Revenue commitment language.** Any ARR figure in this plan is a target, not
a closed-won revenue commitment. Flag with `[review — not yet a revenue commitment]`
if shared with leadership before the renewal is signed.
