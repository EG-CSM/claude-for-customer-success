---
title: "Reasoning Blueprint: Renewal Negotiation Prep"
type: reasoning-blueprint
skill: negotiation-prep
version: 1.0.0
---

# Reasoning Blueprint: Renewal Negotiation Prep

Load this blueprint when Tier 3 reasoning is activated for renewal negotiation
preparation. It provides the domain-specific taxonomy, heuristics, and expert
judgment patterns that shape expert-level negotiation brief construction.

---

## Problem Classification Taxonomy

### Type A: Standard Renewal (No Pressure Signals)
**Characteristics**: Account healthy, no competitor mentions, no price objections in recent calls, champion engaged. Renewal is a formality with a price-increase conversation.
**Primary Risk**: Under-preparing because it looks easy — missing a latent objection that surfaces on the call.
**Expert Focus**: Validate that silence is genuine satisfaction, not disengagement. Pull call data to confirm.

### Type B: Price-Sensitive Renewal
**Characteristics**: Budget freeze signals, price objections in prior calls, declining usage, or customer requesting scope reduction.
**Primary Risk**: Conceding too early — opening below anchor or offering discounts before the customer applies real pressure.
**Expert Focus**: Separate stated price sensitivity from actual willingness to pay. Usage data and switching cost analysis reveal the real floor.

### Type C: Competitive Displacement Threat
**Characteristics**: Competitor named in calls or CRM, RFP issued, procurement engaged early, champion mentions "evaluation."
**Primary Risk**: Panic discounting that signals weakness and sets a precedent without addressing the real evaluation criteria.
**Expert Focus**: Determine evaluation stage (exploring vs. active RFP) and the criteria driving it — price is rarely the only factor.

### Type D: Stakeholder Disruption
**Characteristics**: Champion departure, executive sponsor change, reorg, or new economic buyer unfamiliar with the relationship.
**Primary Risk**: Negotiating with the wrong person or missing that the new stakeholder has different priorities than the predecessor.
**Expert Focus**: Map the new decision-making structure before building the brief. A stakeholder gap invalidates the entire negotiation posture.

### Type E: Expansion-Attached Renewal
**Characteristics**: Renewal coincides with upsell opportunity, multi-product deal, or tier upgrade. Commercial conversation is bigger than retention.
**Primary Risk**: Conflating the renewal hold with the expansion ask — losing leverage on one by bundling with the other.
**Expert Focus**: Separate the renewal anchor from the expansion proposal. Each needs its own walk-away.

---

## Domain Heuristics

1. **The Anchor Integrity Rule**: Never open below your anchor unless you have pre-approved authority to do so. Every dollar below anchor in the opening is a dollar you cannot recover — concessions only move in one direction.

2. **The Three-Number Rule**: Know your anchor, first concession, and walk-away before the call starts. If you're calculating on the call, the customer hears uncertainty.

3. **The Silence Test**: If the customer hasn't raised a price objection, don't solve a problem that doesn't exist. Preemptive discounting trains customers to expect it.

4. **The Switching Cost Multiplier**: Customers underestimate switching costs by 2-3x. When they cite a competitor's price, ask for an apples-to-apples comparison in writing — implementation, migration, retraining, and productivity loss close most gaps.

5. **The 30-Day Escalation Threshold**: Any renewal inside 30 days without a decision signal is a risk flag, not a timeline issue. Escalate to the configured owner — waiting longer compresses options.

6. **The Authority Boundary Rule**: Never present an offer you cannot approve. Below-authority offers presented on-call cannot be retracted without damaging trust. Get approval first; present second.

7. **The Export Separation Rule**: Internal briefs and customer-facing proposals are separate artifacts with zero content overlap on strategy, walk-away, or competitive positioning. Never edit one into the other — generate them independently.

---

## Common Failure Modes by Negotiation Type

### Standard Renewal Failures
- **Complacency Brief**: Producing a thin brief because the account looks healthy.
  Fix: Run the full objection scan anyway — surface the top 3 objections even if signals are weak.
- **Missing Price-Increase Framing**: Presenting the increase as a number without a value anchor.
  Fix: Lead with value delivered this period, then present the increase as continuation of that value.

### Price-Sensitive Renewal Failures
- **Premature Concession**: Offering a discount in the brief's recommended opening before the customer asks.
  Fix: Open at full anchor. First concession should be non-price (multi-year, service credit, phased increase).
- **Floor Confusion**: Treating the walk-away floor as the opening offer.
  Fix: Anchor and floor are different numbers. The brief must present both with the concession path between them.

### Competitive Displacement Failures
- **Fabricated Competitive Intel**: Inventing competitor weaknesses or pricing without configured data.
  Fix: If no competitive intelligence is configured, say so. Offer to run `/renewals:cold-start-interview --section churn-signals`.
- **Defensive Posture**: Framing the entire brief around the competitor instead of the account's value.
  Fix: Lead with value delivered and switching cost. Competitor counter-positioning is secondary.

### Stakeholder Disruption Failures
- **Stale Stakeholder Map**: Using the CRM contact list without verifying current roles and engagement.
  Fix: Cross-reference CRM contacts against recent call attendees. Flag any mismatch before building talking points.

### Expansion-Attached Renewal Failures
- **Bundled Walk-Away**: Using a single floor number for a combined renewal + expansion deal.
  Fix: Separate the renewal floor from the expansion floor. Each has its own authority check.

---

## Expert Judgment Patterns

### Concession Sequencing Decisions
- Offer non-price concessions first (multi-year term, service credits, phased increase) — they preserve ARR while giving the customer a win.
- If the customer rejects non-price concessions and insists on ARR reduction, that's when the discount authority check matters — not before.
- Never offer two concessions simultaneously. Each concession should feel like a deliberate move, not a bundle.

### Mode Selection Decisions
- Default to `--brief` unless the renewal is >$100K ARR, involves multi-stakeholder complexity, or has active competitive threat — then `--full`.
- Use `--export` only after reviewing the internal brief. Never generate export first.
- If the CSM asks for export without having seen the brief, produce the brief first with a note explaining why.

### Escalation Timing Decisions
- Escalate before the call, not during. A mid-call escalation ("let me check with my team") is acceptable once; twice signals disorganization.
- If the customer's ask is within 5% of your authority ceiling, pre-approve with the escalation owner before the call rather than discovering the gap live.
- Route non-standard contract terms (IP, liability, data residency) to Legal immediately — these are not negotiation concessions, they are compliance gates.

---

*Reasoning Blueprint: Renewal Negotiation Prep v1.0*
*For use with negotiation-prep when Tier 3 reasoning is activated*
