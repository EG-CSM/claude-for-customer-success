---
title: "Reasoning Blueprint: Renewal Risk Assessment"
type: reasoning-blueprint
skill: risk-assessment
version: 1.0.0
---

# Reasoning Blueprint: Renewal Risk Assessment

Load this blueprint when Tier 3 reasoning is activated for renewal risk assessment work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns that
shape expert-level churn risk triage and escalation routing.

---

## Problem Classification Taxonomy

### Type A: Signal-Rich Triage
**Characteristics**: Multiple live data sources available (CRM, CS Platform, call recording). Signals span all five domains with quantitative backing.
**Primary Risk**: Over-weighting one domain's signals while under-counting cross-domain compound risk.
**Expert Focus**: Look for signal combinations that individually read Medium but compound to High or Critical.

### Type B: Signal-Sparse Manual Assessment
**Characteristics**: Limited or no live connectors. CSM provides context verbally or from memory. Data freshness is unknown.
**Primary Risk**: Anchoring on the signals the CSM remembers (usually the most recent or dramatic) while missing quiet degradation in unmeasured domains.
**Expert Focus**: Probe for absence of data as a signal itself -- especially product adoption and support domains where silence often means disengagement, not health.

### Type C: Auto-Escalate Trigger Present
**Characteristics**: A non-negotiable trigger is active (non-renewal notice, executive escalation from customer, NPS below configured threshold). Tier is Critical regardless of aggregation.
**Primary Risk**: Spending time on full signal collection when the escalation clock is already running.
**Expert Focus**: Route immediately, then backfill the signal picture for the escalation owner.

### Type D: Multi-Account Triage (--triage mode)
**Characteristics**: Batch of accounts for pipeline review prep. Minimal signal input per account; purpose is ranked prioritization, not deep assessment.
**Primary Risk**: Applying deep-mode rigor to each account and burning the CSM's time, or conversely missing a Critical buried in the batch.
**Expert Focus**: Screen for auto-escalate triggers first across the entire batch before ranking the rest.

---

## Domain Heuristics

1. **The Compound Signal Rule**: Two Medium-tier signals in different domains are worse than one High-tier signal in a single domain. Cross-domain risk compounds non-linearly.

2. **The Silence-Is-Not-Health Rule**: Absence of engagement data (no logins, no calls, no tickets) in a renewal window is a red flag, not a neutral signal. Healthy accounts generate activity.

3. **The 30-Day Decay Rule**: Any signal older than 30 days inside a 90-day renewal window should be treated as stale. Re-verify before using it to assign tier.

4. **The Champion Departure Multiplier**: When a champion or executive sponsor departs, multiply the severity of every other signal by one tier. Relationship loss amplifies all existing risk.

5. **The Competitor + Price Rule**: A price objection alone is commercial negotiation. A price objection combined with a confirmed competitor evaluation is a save-or-lose scenario -- always Critical.

6. **The First-Signal Anchor Trap**: The signal the CSM mentions first is usually not the most important one -- it's the most recent or most emotionally salient. Probe all five domains before weighting.

7. **The Save-Offer Ceiling Rule**: Never surface a discount above configured authority without flagging it. A save offer the CSM can't actually approve damages credibility with both the customer and the escalation owner.

---

## Common Failure Modes by Assessment Type

### Signal-Rich Triage Failures
- **Domain tunnel vision**: Analyst fixates on the domain with the most data (usually product usage) and under-weights engagement or commercial signals.
  -> Fix: Force a signal-per-domain minimum before tier assignment. No domain gets "N/A" when a connector returned data.
- **Health score shortcut**: Using the composite health score as the tier instead of decomposing signals.
  -> Fix: Cite the health score as one input; assign tier from signal aggregation across all five domains.

### Signal-Sparse Manual Failures
- **Recency bias acceptance**: CSM provides only recent signals; analyst doesn't probe for longer trends.
  -> Fix: Ask explicitly about 30/60/90-day trends even when CSM offers only point-in-time data.
- **Missing-data optimism**: Treating absent signals as neutral rather than flagging them.
  -> Fix: Mark every domain without data as "[no data -- not assessed]" and note it reduces confidence.

### Auto-Escalate Trigger Failures
- **Aggregation delay**: Running full five-domain collection before routing the escalation.
  -> Fix: Route escalation immediately on trigger detection; backfill signal picture afterward.

### Multi-Account Triage Failures
- **Uniform depth**: Applying deep-mode rigor to every account in a batch.
  -> Fix: First pass screens for auto-escalate triggers only; second pass assigns preliminary tiers; deep mode reserved for Critical/High.
- **ARR-blind ranking**: Ranking by signal severity without weighting by ARR at stake.
  -> Fix: Include ARR in triage table and flag any High-ARR account regardless of preliminary tier.

---

## Expert Judgment Patterns

### Tier Assignment Decisions
- When signals split evenly between two tiers, assign the higher tier and note the ambiguity -- under-escalation costs more than over-escalation.
- When the health score says Green but individual signals say otherwise, trust the signals. Composite scores mask domain-level degradation.

### Escalation Routing Decisions
- Match the situation to the configured matrix first. If no exact match, name the closest scenario and recommend confirming with Head of CS.
- For Critical tier: prepare the escalation package (ARR, signals, save options) before routing -- the escalation owner needs context to act, not just an alert.

### Save Option Decisions
- Lead with non-commercial saves (executive engagement, product roadmap, dedicated support) before discount offers. Discounts compress margin permanently; relationship interventions don't.
- If the customer's primary signal is product adoption failure, a discount doesn't solve the problem. Match save type to signal type.

### Confidence Decisions
- State [High] only when 3+ domains have live-sourced, <7-day-old data that corroborates the tier.
- State [Low] when relying on user-provided context without cross-reference. Make the confidence gap visible.

---

*Reasoning Blueprint: Renewal Risk Assessment v1.0*
*For use with risk-assessment when Tier 3 reasoning is activated*
