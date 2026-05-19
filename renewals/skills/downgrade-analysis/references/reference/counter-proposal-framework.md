# Counter-Proposal Framework

**Used by:** `renewals:downgrade-analysis`
**Purpose:** Internal CSM/AM use only — never customer-facing. Defines retention levers, negotiation anchors, concession guidance, and escalation trigger conditions per driver category.

---

## Critical Usage Note

This framework is strictly for CSM/AM internal preparation. The retention levers and negotiation positions defined here are inputs to the CSM/AM's strategy — they are not scripts, customer-facing proposals, or commitments. Do not share this framework or its outputs directly with customers.

---

## Retention Levers by Driver Category

### `budget_pressure`

These levers address the financial constraint without conceding the full value of the contract.

| Lever | Description | When to use |
|-------|-------------|-------------|
| Payment term adjustment | Extend payment schedule (quarterly or monthly instead of annual upfront) to reduce immediate cash burden | Customer has cash flow constraint but budget will normalize |
| Multi-year commitment discount | Offer year-1 price reduction in exchange for 2–3 year commitment | Customer is wavering but not at risk of leaving entirely |
| Phased renewal | Renew at current scope for 6 months at reduced rate, then step back to full rate | Budget constraint is temporary (90-day freeze, fiscal year boundary) |
| Tier restructure (right-size) | Move to a lower tier with a documented re-expansion clause | Tier gap is genuine; downgrade is preferable to churn |
| Re-expansion commitment clause | Accept a downgrade but contractually or verbally anchor a re-expansion at a named milestone (Q3 budget, team growth, project start) | Customer agrees the constraint is temporary |
| Bundle consolidation | If customer uses multiple products, consolidate into a single contract with a package discount | Customer is cutting individual line items; package deal may preserve overall ARR |
| Success milestone credit | Offer a credit against future renewal tied to achievement of named outcomes in the current period | Customer doubts ROI; credit de-risks their commitment |

**What to hold:**
- Do not agree to a downgrade without a re-expansion clause or timeline commitment
- Do not offer a discount without a multi-period commitment or a concrete return condition
- Do not accept verbal re-expansion promises — document them in the renewal agreement or a follow-up email

---

### `reduced_scope`

These levers address legitimate right-sizing while protecting future ARR.

| Lever | Description | When to use |
|-------|-------------|-------------|
| Seat reduction with floor | Accept reduced seat count but set a contract floor above the minimum to preserve ARR baseline | Headcount reduction is genuine; full seat count is no longer defensible |
| Re-expansion trigger clause | Reduce seats with a named trigger for expansion (new hires above X, team growth, new department onboarding) | Org change is likely temporary or bounded |
| Department expansion conversation | Identify other teams or departments that could absorb unused licenses | Current users shrank, but product use case exists in adjacent teams |
| Module right-sizing | Remove unused modules rather than reducing tier — preserve strategic footprint | Customer only uses subset of features; module removal is less damaging than tier change |
| Usage-based pricing exploration | If the product supports it, explore whether a usage-based model better fits reduced scope | Fixed seat pricing is the friction; usage model may retain the relationship |

**What to hold:**
- Do not reduce below a seat count that makes the account unprofitable for CS investment
- Do not remove modules that are on the roadmap for future expansion without documenting the re-introduction path

---

### `feature_underutilization`

These levers address adoption failures and create a path to recognized value before accepting a downgrade.

| Lever | Description | When to use |
|-------|-------------|-------------|
| Adoption sprint commitment | Offer a focused 30-day enablement engagement to drive adoption of the specific unused features | Customer is open to trying; adoption gap is recoverable |
| Usage audit + ROI report | Pull actual usage data and build a value narrative showing what has been achieved with the tool | Customer doesn't see ROI because it hasn't been quantified or surfaced |
| Champion re-engagement | Schedule a working session with the champion and key end users to remove specific adoption blockers | Adoption gap is relationship/communication-driven, not technical |
| Training redesign | Replace generic training with role-specific, workflow-integrated training for the customer's actual use cases | Prior training didn't stick because it wasn't contextualized |
| Feature sunset negotiation | If specific features are genuinely not needed, explore a module removal that right-sizes the contract while preserving the core | Pure right-sizing; unused features have no realistic adoption path |
| Success milestone gate | Propose a 60-day adoption milestone review before any contract change is finalized — "give us 60 days to close the adoption gap" | Customer is willing to defer the decision |

**What to hold:**
- Do not accept the downgrade before attempting an adoption sprint — feature_underutilization is often recoverable
- Do not promise adoption outcomes (usage %) as contract conditions unless the CSM has direct influence over those metrics

---

### `competitive_pressure`

These levers address competitive threats. Note: this is the highest-churn-risk category.

| Lever | Description | When to use |
|-------|-------------|-------------|
| Competitive displacement analysis | Build an internal brief on the named competitor: feature gaps, total cost of ownership (including switching costs), implementation timeline | Customer has not done a full TCO analysis |
| Switching cost framing | Surface the real cost of migration: data migration, retraining, integration rebuild, productivity loss during transition | Customer is focused on license price only |
| Strategic roadmap briefing | Request access to product leadership to brief the customer on upcoming features that address their stated gap | Customer has a feature gap that is on the product roadmap |
| Price match (limited) | If the competitive threat is purely price-based and the customer has strong retention indicators, explore a targeted price adjustment | Customer is price-sensitive and satisfied with the product; price match removes the reason to switch |
| Executive sponsor engagement | Bring in CS/Sales leadership for an executive relationship conversation | Economic buyer is driving the competitive evaluation; CSM/AM cannot access that level |
| Proof of value data package | Build a comprehensive value summary: ROI achieved, outcomes delivered, time saved — contextualized for the economic buyer | Customer (or their CFO) has not seen a formal ROI case |

**What to hold:**
- Do not offer a price match without VP-level approval and a multi-year commitment in return
- Do not dismiss the competitive threat without getting specific about the competitor and the evaluation stage
- If the customer is already in a formal RFP or evaluation process, escalate immediately — CSM/AM-level retention tactics may be insufficient

---

### `dissatisfaction`

These levers address trust and relationship failures. Dissatisfaction requires acknowledgment before any commercial lever is effective.

| Lever | Description | When to use |
|-------|-------------|-------------|
| Formal acknowledgment and apology | CSM/AM explicitly acknowledges the failure, names what went wrong, and apologizes without defensiveness | Always — no other lever is effective until this step is complete |
| Executive escalation to resolution | Bring in CS leadership to own the remediation commitment | Customer has lost confidence in the CSM or the standard support channel |
| SLA commitment with penalties | Offer a formal SLA for the remediation period with defined remedies if milestones are missed | Customer needs contractual protection to re-engage |
| Dedicated support assignment | Assign a named senior resource (TAM, senior CSM, support engineer) to the account for a defined recovery period | Customer's trust in the standard support model is broken |
| Credit or fee waiver | Offer a credit or partial fee waiver for the period of degraded service — tied to the remediation plan | Customer has measurable financial impact from the delivery failure |
| Root cause briefing | Provide the customer with a written root cause analysis of what went wrong and what has been done to prevent recurrence | Customer needs assurance this won't happen again |
| Re-contracting at reduced scope | If remediation is not sufficient to retain full scope, negotiate a reduced contract at a price that reflects the reduced delivery — with a defined re-expansion path | Customer cannot return to full scope until trust is rebuilt |

**What to hold:**
- Do not jump to commercial concessions before completing formal acknowledgment — offering a discount without acknowledging the failure reads as dismissive
- Do not assign blame (internally or externally) in any customer-facing communication
- Do not promise a remediation timeline the delivery team cannot commit to

---

## Negotiation Anchors

Negotiation anchors are facts and positions that the CSM/AM can reference to maintain a strong negotiating stance. These are internal reference points — not scripts.

### Universal anchors (applicable to all driver categories)

1. **Total cost of ownership:** The customer's all-in cost for switching includes migration, retraining, integration rebuild, and productivity loss — not just license price differential.
2. **Relationship investment:** Reference the time already invested in onboarding, configuration, and customization. Switching resets this investment.
3. **Outcome delivery record:** Use OCV data to quantify what has been delivered. Frame the downgrade in terms of outcomes at risk, not features.
4. **Future roadmap relevance:** If the product roadmap addresses a stated gap, brief the customer on the timeline. A near-term release may change the calculus.
5. **Account team continuity:** The CSM/AM relationship has organizational memory. A new vendor starts from zero.

### Category-specific anchors

| Driver Category | Key anchor |
|---|---|
| budget_pressure | Payment flexibility doesn't require losing the capability — frame as a cashflow solution, not a product decision |
| reduced_scope | Right-sizing to current need is reasonable, but future re-expansion will cost more than maintaining the current floor |
| feature_underutilization | The capability exists and is configured — the cost to achieve value is lower now than at any other point in the relationship |
| competitive_pressure | Competitor's published price excludes implementation, migration, and integration costs — build the true TCO comparison |
| dissatisfaction | A downgrade doesn't resolve the service failure — remediation with current vendor is faster than rebuilding with a new one |

---

## Escalation Trigger Conditions

These conditions require leadership involvement beyond CSM/AM. When any trigger is met, escalate before continuing negotiation.

| Condition | Escalation target | Rationale |
|-----------|-------------------|-----------|
| CSM/AM cannot access economic buyer within 5 business days | CS Manager / VP Customer Success | Decision is being made above the CSM's relationship level |
| Customer is in an active RFP or competitive evaluation with a named vendor | CS leadership + Sales leadership | Formal eval requires formal response at leadership level |
| Dissatisfaction involves a product failure, legal complaint, or data issue | CS leadership + Product/Engineering | Technical or legal exposure requires immediate escalation |
| Downgrade would reduce ARR below the account's strategic threshold | CS leadership | Business case for retention investment must be approved at leadership level |
| Customer explicitly requests executive conversation | CS leadership / Executive sponsor | Honor the request — declining signals the problem isn't being taken seriously |
| Remediation plan requires resources not within CSM's control (PS hours, engineering time, product commitment) | CS leadership + delivery owner | CSM cannot commit to resources they don't control |
| Missing link failure was caused by a product deficiency, not CSM execution | Product leadership | Product-caused delivery failures require a product-level response |
| Champion is no longer the decision-maker (new economic buyer, reorg) | CS leadership + Sales | New buyer requires exec-level introductions; CSM-level relationship is insufficient |

---

## Concession Guidance

Concessions should be structured, conditional, and documented. Unstructured concessions signal willingness to accept any terms and weaken future negotiating positions.

### Concession structuring principles

1. **Every concession requires a condition.** "We can adjust payment terms [concession] if you commit to a 2-year renewal [condition]." Never offer a concession without attaching a return ask.
2. **Concede scope before price.** Right-sizing the contract (fewer seats, fewer modules) preserves the per-unit value of the product. Discounting reduces the per-unit value and sets a new price anchor for future renewals.
3. **One concession at a time.** Do not offer multiple concessions simultaneously — it signals desperation and invites further negotiation.
4. **Document all concessions.** Every verbal concession should be followed by a written confirmation email. Undocumented concessions are unenforceable and create future ambiguity.
5. **Escalate before exceeding standard authority.** Most CSMs/AMs have a defined concession authority (% discount, payment term flexibility). Any concession outside that authority requires manager approval before being offered.

### What never to concede without leadership approval
- Permanent price reductions with no term commitment
- SLA guarantees with financial penalties
- Feature development commitments (product roadmap items)
- Credits that exceed one month of ARR
- Re-contracting at below-cost pricing
