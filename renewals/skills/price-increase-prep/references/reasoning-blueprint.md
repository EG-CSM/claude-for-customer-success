---
title: "Reasoning Blueprint: Price Increase Prep"
type: reasoning-blueprint
skill: price-increase-prep
version: 1.0.0
---

# Reasoning Blueprint: Price Increase Prep

Load this blueprint when Tier 3 reasoning is activated for price increase planning.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level price increase communication and approval routing.

---

## Problem Classification Taxonomy

### Type A: Standard Policy Increase
**Characteristics**: Increase aligns with configured policy (CPI, flat %, contractual clause). Account is healthy, no contract price protection, within authority threshold.
**Primary Risk**: Treating it as routine and skipping value framing — even contractual increases benefit from proactive communication.
**Expert Focus**: Timing the notification to land before the customer hears about it from procurement or finance internally.

### Type B: Above-Authority Increase
**Characteristics**: Proposed increase exceeds the CSM's configured approval threshold. Requires routing through the approval chain before any customer communication.
**Primary Risk**: Drafting or sending customer communication before approval is confirmed — a walked-back increase is worse than no increase.
**Expert Focus**: Building the internal business case (risk assessment, churn exposure, competitive context) alongside the customer rationale.

### Type C: At-Risk Account Increase
**Characteristics**: Account has active churn signals, declining health, or recent escalation. Price increase is still directed but requires a fundamentally different strategy.
**Primary Risk**: Applying a standard increase playbook to an account that needs stabilization first — the increase becomes the trigger for churn.
**Expert Focus**: Sequencing — run risk assessment before increase planning. The increase conversation may need to be deferred or paired with a value recovery plan.

### Type D: Cohort Rollout
**Characteristics**: Multiple accounts receiving increases simultaneously. Requires segmentation, prioritization, and sequenced communication.
**Primary Risk**: Treating all accounts identically — failing to segment by risk, contract terms, and relationship strength produces avoidable churn.
**Expert Focus**: Identifying which accounts need individual handling versus batch communication, and sequencing high-risk accounts first.

### Type E: Contract-Constrained Increase
**Characteristics**: Account has price caps, MFN clauses, or CPI ceilings in the existing contract that may limit or invalidate the proposed increase.
**Primary Risk**: Issuing an increase notice that violates contract terms — creates legal exposure and severe trust damage.
**Expert Focus**: Confirming contract review is complete before any communication is drafted, not after.

---

## Domain Heuristics

1. **The Approval-Before-Draft Rule**: Never draft customer communication before confirming the increase is within authority or approved. A draft creates momentum toward sending; approval gates must come first.

2. **The 60-Day Floor**: Increases notified with fewer than 60 days before renewal compress negotiation time and escalate churn risk disproportionately. Inside 30 days, treat as a crisis conversation requiring leadership sign-off.

3. **The Value-Evidence Test**: If you cannot substantiate the rationale with account-specific evidence, use plain language ("we're adjusting pricing broadly") rather than fabricated value framing. Customers detect hollow justification.

4. **The Risk-First Sequencing Rule**: Any account with active churn signals requires `/renewals:risk-assessment` before price increase planning begins. The increase plan is downstream of the risk strategy, not parallel.

5. **The Contract-Check Gate**: Accounts with multi-year agreements, enterprise terms, or negotiated pricing always require contract review before increase notification — assume price protection exists until confirmed otherwise.

6. **The Precedent Awareness Rule**: Any concession offered (deferral, phased increase, rate lock) sets a precedent for future renewals. Evaluate the long-term cost before offering, especially on strategic accounts.

7. **The Cohort Isolation Rule**: At-risk accounts must be removed from cohort rollouts and handled individually. A batch increase notification to an at-risk account signals that you aren't paying attention.

---

## Common Failure Modes by Request Type

### Standard Policy Increase Failures
- **Skipped value framing**: Sent the increase notice without rationale, treating contractual language as sufficient.
  → Fix: Always pair the increase with a 2-3 sentence rationale tied to value delivered, even for contractual adjustments.
- **Wrong contact targeted**: Sent to day-to-day user instead of economic buyer or champion.
  → Fix: Verify the primary renewal contact in CRM before drafting; cross-reference with recent call attendees.

### Above-Authority Increase Failures
- **Premature customer communication**: Drafted or discussed the increase with the customer before internal approval was confirmed.
  → Fix: Enforce the approval-before-draft gate. Do not enter `--draft` mode until approval status is confirmed.
- **Weak internal business case**: Approval request lacked risk assessment and competitive context, causing delays.
  → Fix: Include churn probability assessment, competitive landscape, and recommended concession boundaries in every approval request.

### At-Risk Account Failures
- **Applied standard playbook**: Used the same increase framing as a healthy account, ignoring active risk signals.
  → Fix: Run risk assessment first. If risk is High or Critical, the increase conversation must be paired with a retention strategy.
- **Deferred without a plan**: Decided to skip the increase but didn't document why or set a follow-up trigger.
  → Fix: Any deferral must include a documented rationale, a re-evaluation date, and leadership awareness.

### Cohort Rollout Failures
- **Uniform treatment**: Applied the same increase percentage and communication to all accounts regardless of segment, risk, or contract terms.
  → Fix: Segment the cohort by risk level, contract constraints, and relationship strength before generating communications.
- **Missed contract constraints**: Included contract-protected accounts in the cohort without individual review.
  → Fix: Flag all accounts with multi-year or negotiated terms for individual contract review before inclusion.

---

## Expert Judgment Patterns

### Timing Decisions
- When renewal is 90+ days out: standard notification — maximum negotiation runway.
- When renewal is 60-90 days: notify immediately but monitor response closely for escalation signals.
- When renewal is <30 days: this is a leadership decision, not a CSM decision. Escalate before acting.

### Concession Decisions
- Offer multi-year lock-in before offering a rate reduction — it preserves ARR trajectory.
- Phased increases are preferable to deferrals — deferrals create a larger cliff at next renewal.
- Never offer a concession without understanding the actual objection — price resistance often masks a value or relationship problem.

### Communication Decisions
- Lead with what hasn't changed before introducing what has — anchors the conversation in stability.
- If the honest rationale is "broad price adjustment," say so — fabricated value framing is detectable and damages trust.
- For strategic accounts, the CSM should deliver the news in a call, not an email — the email follows as documentation.

### Escalation Decisions
- Price objection + competitive mention = risk assessment trigger, not a negotiation tactic. Escalate.
- Multiple stakeholders asking the same objection question independently = organized resistance. Engage the executive sponsor.
- Silence after increase notification is not acceptance — follow up within 5 business days.

---

*Reasoning Blueprint: Price Increase Prep v1.0*
*For use with price-increase-prep skill*
