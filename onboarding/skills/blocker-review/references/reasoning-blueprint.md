---
title: "Reasoning Blueprint: Onboarding Blocker Review"
type: reasoning-blueprint
skill: blocker-review
version: 1.0.0
---

# Reasoning Blueprint: Onboarding Blocker Review

Load this blueprint when Tier 3 reasoning is activated for blocker diagnosis,
escalation, and resolution tracking. It provides the domain-specific taxonomy,
heuristics, and expert judgment patterns that shape expert-level blocker triage.

---

## Problem Classification Taxonomy

### Type A: Active Technical Impediment
**Characteristics**: Something is broken or blocked in the product/environment — integration failure, provisioning gap, data quality issue, or product bug. The customer wants to proceed but cannot.
**Primary Risk**: Misclassifying an adoption problem as technical — the CSM chases engineering when the real issue is engagement.
**Expert Focus**: Verify the customer has actually attempted the blocked step. No attempt + "technical blocker" = likely adoption or bandwidth issue.

### Type B: Customer Engagement Stall
**Characteristics**: The customer has stopped progressing — low activity, missed meetings, champion unavailable, or internal reprioritization. No technical impediment exists.
**Primary Risk**: Treating silence as low priority when it signals stakeholder misalignment or champion loss.
**Expert Focus**: Distinguish temporary bandwidth constraints (recoverable with a nudge) from structural disengagement (requires escalation or champion replacement).

### Type C: CSM Execution Gap
**Characteristics**: The blocker traces back to something the CSM or vendor team failed to deliver — unclear instructions, missing resources, dropped follow-through.
**Primary Risk**: Defensive misclassification — labeling a CSM-side gap as customer-side to avoid accountability.
**Expert Focus**: Ask "did we deliver everything we committed to?" before classifying customer-side.

### Type D: Vendor/Product Constraint
**Characteristics**: A bug, feature gap, or support queue delay outside the CSM's direct control. Resolution depends on internal product or engineering teams.
**Primary Risk**: Using "waiting on product" as a holding pattern without an escalation deadline or workaround plan.
**Expert Focus**: Every vendor blocker needs a workaround assessment and an escalation trigger date — not just a ticket number.

### Type E: Multi-Party Coordination Failure
**Characteristics**: Partner-led or multi-stakeholder blocker where ownership is ambiguous. The partner, customer, and CSM each believe another party owns the next step.
**Primary Risk**: Routing directly to the customer when the partner-led model requires partner-first engagement.
**Expert Focus**: Map the ownership chain before acting. In partner-led models, always confirm partner awareness first.

---

## Domain Heuristics

1. **The Symptom-vs-Cause Rule**: The first blocker the CSM describes is almost always a symptom. Ask "what is preventing the customer from completing the next milestone step?" to surface the root cause. One probing question saves a misclassified action plan.

2. **The 7-Day Silence Rule**: If a customer has had zero engagement (no logins, no replies, no meeting attendance) for 7+ days during active onboarding, the blocker is engagement-related until proven otherwise — regardless of what the CSM labels it.

3. **The Milestone Math Rule**: Severity is determined by math, not feeling. Days remaining to milestone target minus estimated resolution time equals the risk window. Negative = P1. Under 3 days = P2. Everything else is P3/P4.

4. **The Already-Tried Filter**: Never recommend an action the CSM has already attempted. Repeating failed outreach destroys credibility. Always ask what's been tried before generating the action plan.

5. **The Partner-First Gate**: In partner-led models, every blocker routes through the partner before reaching the customer. Skipping this step undermines the partner relationship and creates confusion about ownership.

6. **The Escalation Specificity Rule**: An escalation without a specific ask, a named owner, and a deadline is not an escalation — it's a complaint. Every escalation brief must answer: who does what by when.

7. **The Single-Thread Danger Rule**: If the blocker resolution depends on exactly one person (customer champion, partner contact, support engineer), flag it as fragile. Identify a backup contact or parallel path before committing the action plan.

---

## Common Failure Modes by Blocker Type

### Active Technical Impediment Failures
- **Phantom technical blocker**: CSM reports "integration is broken" but customer hasn't attempted the integration step yet.
  Fix: Ask "has the customer attempted this step?" before classifying as technical.
- **Missing reproduction context**: Escalation to engineering without specific error details or environment context.
  Fix: Collect error messages, timestamps, and environment details before generating the escalation brief.

### Customer Engagement Stall Failures
- **Bandwidth excuse accepted at face value**: CSM accepts "we're too busy" without probing for underlying disengagement.
  Fix: Ask about competing priorities, stakeholder changes, and whether the customer's internal sponsor still supports the initiative.
- **Single-channel follow-up**: CSM sends repeated emails to an unresponsive champion without trying alternative contacts or channels.
  Fix: After 2 unanswered outreach attempts, escalate to a different stakeholder or engage the AE for a warm introduction.

### CSM Execution Gap Failures
- **Defensive misclassification**: Blocker is labeled customer-side when the root cause is a missed CSM deliverable.
  Fix: The diagnostic sequence explicitly asks "did we deliver everything we committed to?" — do not skip this step.

### Vendor/Product Constraint Failures
- **Passive waiting**: CSM logs a support ticket and waits indefinitely without setting an escalation deadline.
  Fix: Every vendor blocker gets a "if not resolved by [date], escalate to [contact]" trigger in the action plan.

### Multi-Party Coordination Failures
- **Partner bypass**: CSM routes directly to the customer in a partner-led model, creating ownership confusion.
  Fix: Apply the Partner-First Gate heuristic. Confirm partner awareness before any direct customer action.

---

## Expert Judgment Patterns

### Severity Calibration Decisions
- When the CSM's emotional urgency exceeds the milestone math, trust the math — present the calculated severity and let the CSM override with stated reasoning.
- When multiple blockers exist simultaneously, severity is driven by the highest-impact single blocker, not aggregated — but note compound risk in the reviewer note.

### Scope Decisions
- If diagnosis reveals the blocker is actually two distinct blockers (e.g., technical + engagement), split into separate entries with independent action plans rather than conflating into one.
- If the blocker affects multiple milestones, anchor the action plan to the nearest milestone at risk — don't try to solve everything at once.

### Escalation Timing Decisions
- Escalate early on P1 blockers even if the CSM wants to "try one more thing" — the cost of late escalation on a critical blocker exceeds the cost of a premature one.
- For P2 blockers, the CSM's judgment on timing is respected — the config threshold is the floor, not the mandate.

### Classification Confidence Decisions
- When the blocker sits between two types (e.g., technical vs. adoption), present both classifications with the distinguishing question that would confirm one over the other.
- When the CSM disagrees with the suggested classification, accept their override — they have context you don't. Note the override in the reviewer note.

---

*Reasoning Blueprint: Onboarding Blocker Review v1.0*
*For use with blocker-review skill*
