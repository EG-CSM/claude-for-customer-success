# Value Chain Failure Map

**Used by:** `renewals:downgrade-analysis`
**Purpose:** Defines the three failure classifications, detection patterns, remediation pathways, and escalation guidance for value chain analysis in downgrade scenarios.

---

## Overview

The value chain failure map answers a single diagnostic question: **Is this downgrade happening because we failed to deliver value, or because of factors outside the value chain?**

The answer determines the response strategy. A CSM cannot negotiate their way out of a delivery failure — they must remediate it. Conversely, applying a remediation approach to a budget cut wastes time and may damage the relationship.

---

## The Three Failure Classifications

### Missing Link

**Definition:** An outcome was committed during the sales or onboarding process, but has not been delivered. The gap between promised and actual outcomes is the root cause of the downgrade.

**Accountability:** CSM/delivery failure. The product capability may exist, but the customer has not been enabled to achieve the outcome they were sold.

**Indicators:**
- OCV shows outcomes at "not started" or "below target" for one or more committed areas
- Customer references what they were "promised" or "sold on" vs. what actually happened
- Implementation milestones were missed or are significantly delayed
- QBR outcomes reviewed show consistent delivery gap over 2+ quarters
- Customer expresses that they are "not getting what they paid for"
- Usage data is low not because of disinterest but because setup/enablement was not completed

**OCV detection pattern:**
If `ocv_snapshot` shows committed outcome count > delivered outcome count, with delivery gaps of 30% or more, and the `downgrade_request` references dissatisfaction with outcomes or delivery, classify as Missing link.

**Example signals in downgrade_request:**
- "We were supposed to have X set up by now and it hasn't happened"
- "The reporting we were promised never got built"
- "Our CSM said we'd be able to do Y by Q2 and we still can't"
- "We're not getting the value we expected from this"

---

### Broken Link

**Definition:** The outcome was delivered — the capability is live, the configuration is complete — but the customer has not recognized, adopted, or internalized the value. The breakdown is in change management, not delivery.

**Accountability:** Adoption/change management failure. The product works; the customer is not using it.

**Indicators:**
- OCV shows outcomes marked "delivered" but usage metrics are below threshold (e.g., seat utilization under 40%, feature adoption under 30%)
- Customer references complexity, not getting around to it, or team resistance
- Champion is aware the features are live but end-user adoption has not materialized
- Customer does not associate the delivered capability with outcomes they care about
- Training was completed but behavior change did not follow

**OCV detection pattern:**
If `ocv_snapshot` shows high delivery rate (outcomes marked complete) but low usage/adoption metrics alongside the downgrade request, classify as Broken link.

**Example signals in downgrade_request:**
- "We have it set up but honestly the team just isn't using it"
- "Too complicated — people went back to their old way of doing things"
- "We pay for 500 seats but only 150 people ever log in"
- "The features are there but no one adopted them"
- "It's not part of our workflow"

---

### Non-Value-Chain Driver

**Definition:** The downgrade is driven by factors external to value delivery. Budget constraints, organizational restructuring, headcount reductions, market conditions, competitive pricing pressure, or executive mandates are causing the contraction. Value delivery quality is not the root cause — the downgrade would occur even if all outcomes were fully delivered and adopted.

**Accountability:** External factors. This is not a CSM failure (though unaddressed delivery gaps can give customers a justification to act on external pressure).

**Indicators:**
- Customer explicitly references CFO mandate, budget freeze, cost reduction initiative, or headcount cuts
- Org change events: merger, acquisition, reorg, department elimination
- Competitive pressure from a lower-cost alternative (not driven by dissatisfaction)
- Seasonal or project-based scope reduction ("the project ended," "we only need it for Q1")
- Customer acknowledges they like the product but the spend cannot be justified in the current environment

**OCV detection pattern:**
If `ocv_snapshot` shows strong outcome delivery and reasonable adoption, but the `downgrade_request` references budget, org change, or competitive price, classify as Non-value-chain driver.

**Example signals in downgrade_request:**
- "It's not about the product — the CFO needs us to cut SaaS spend by 20%"
- "Our team was restructured and we went from 400 to 180 people"
- "We found a cheaper tool that does most of what we need"
- "The project this was for wrapped up last quarter"

---

## Detection Patterns by Driver Category

| Driver Category | Most likely failure classification | Key detection signal |
|---|---|---|
| `budget_pressure` | Non-value-chain driver | Explicit budget/CFO reference; no delivery complaint |
| `budget_pressure` + OCV gap | Missing link contributing | Budget is forcing function; delivery gap gives internal justification |
| `reduced_scope` | Non-value-chain driver | Headcount or org change; no product complaint |
| `feature_underutilization` (features never adopted) | Broken link | Features live but unused; training completed without behavior change |
| `feature_underutilization` (features never configured) | Missing link | Features never set up; onboarding incomplete |
| `competitive_pressure` | Non-value-chain driver | Competitor named; primary driver is price |
| `competitive_pressure` + `dissatisfaction` | Missing link escalation risk | Competitor is filling a delivery gap — treat as Missing link + high churn risk |
| `dissatisfaction` | Missing link | Explicit delivery failure; outcome promises not met |

---

## Remediation Pathways by Failure Classification

### Missing Link — Remediation pathway

**Objective:** Acknowledge the delivery gap, commit to a remediation plan, and use the plan as the basis for retaining the current contract scope.

1. **Acknowledge explicitly** — CSM/AM must validate the customer's experience, not defend it. Avoid rationalizations. "You're right that X hasn't been delivered, and that's on us."
2. **Gap quantification** — Enumerate the specific outstanding outcomes (use OCV data if available). Make the remediation concrete and time-bounded.
3. **Remediation plan proposal** — Offer a written 30/60/90-day remediation plan with named milestones. This is the primary counter-proposal lever.
4. **Contract protection ask** — Request that the customer hold the downgrade decision pending the first 30-day milestone review. Frame as "give us the chance to deliver what was promised."
5. **Escalation to delivery resources** — If the delivery gap requires resources beyond the CSM (e.g., PS hours, technical configuration, product involvement), escalate internally before presenting to the customer.

**Does not resolve without:** A concrete, milestone-driven remediation plan and internal commitment to resourcing it.

---

### Broken Link — Remediation pathway

**Objective:** Demonstrate that the value is already there, remove adoption barriers, and create a concrete path to recognized ROI.

1. **Usage audit** — Pull actual usage data vs. licensed capacity. Identify the specific adoption gap (which features, which users, what patterns).
2. **Root cause of non-adoption** — Was it training quality? Workflow integration? Management buy-in? Competing tools? Identify the specific blocker.
3. **Adoption sprint proposal** — Offer a focused 30-day adoption engagement: targeted training, workflow integration session, or manager enablement program.
4. **ROI reframe** — If outcomes were delivered but not recognized, build a value narrative: "Here is what has been accomplished with the tool over the last 6 months." Connect delivered capabilities to business metrics the customer cares about.
5. **Quick win identification** — Find one or two high-visibility use cases the customer can activate within 2 weeks to rebuild momentum.

**Does not resolve without:** Identifying the specific adoption blocker and a targeted action to remove it.

---

### Non-Value-Chain Driver — Remediation pathway

**Objective:** Remove or reduce the financial/organizational friction without conceding value. Preserve ARR or minimize contraction through commercial flexibility.

1. **Validate the driver** — Confirm this is genuinely external (budget, org change) and not a surface-level explanation for deeper dissatisfaction. Ask directly: "If budget weren't an issue, would you stay at the current tier?"
2. **Commercial lever exploration** — Explore alternatives to a tier change: payment terms adjustment, phased renewal, multi-year commitment with year-1 discount, or temporary seat reduction with re-expansion clause.
3. **Scope right-sizing** — If reduced_scope is genuine (headcount actually shrank), work with the customer to identify the right contract size. A collaborative right-sizing conversation is more retention-positive than a contested downgrade negotiation.
4. **Value reinforcement** — Even if the driver is external, surface delivered outcomes and ROI data to strengthen the customer's internal case for retention. The champion may need ammunition to push back on the CFO mandate.
5. **Future commitment anchor** — For budget_pressure with a temporary horizon, negotiate a re-expansion commitment (contractual or verbal) that protects future ARR even while accepting short-term contraction.

**Does not resolve without:** A commercial alternative that gives the customer a path to staying that meets their constraints.

---

## Escalation Guidance

### CSM-addressable (no escalation required)

- Broken link where adoption gap is addressable through CSM-led enablement
- Non-value-chain budget pressure at CSM-sponsor level (champion has budget autonomy)
- Reduced scope where right-sizing conversation is straightforward
- Missing link where the delivery gap is CSM-owned and resourceable within existing capacity

### Escalate to Customer Success leadership

- Missing link where delivery failure requires PS resources, product involvement, or additional headcount
- Competitive pressure with a named competitor and active evaluation underway
- Dissatisfaction where a formal complaint has been filed or executive sponsor is involved
- Any scenario where CSM/AM cannot reach economic buyer within 5 business days

### Escalate to Product/Engineering

- Missing link where the delivery gap is caused by a product limitation, bug, or missing feature
- Feature_underutilization where adoption barrier is product complexity or UX (not training/enablement)
- Scenarios where customer has documented product failures that contributed to the downgrade request

### Escalate to Executive sponsor (exec-to-exec)

- CFO-mandate budget_pressure where only exec-level conversation can protect the contract
- Competitive_pressure + dissatisfaction combination (high churn risk)
- Any downgrade that, if it proceeds, brings ARR below a retention threshold defined by CS leadership
- Customer has escalated to VP or C-level on their side
