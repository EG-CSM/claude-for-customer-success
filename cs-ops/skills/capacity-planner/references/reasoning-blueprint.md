---
title: "Reasoning Blueprint: CSM Capacity Planning"
type: reasoning-blueprint
skill: capacity-planner
version: 1.0.0
---

# Reasoning Blueprint: CSM Capacity Planning

Load this blueprint when Tier 3 reasoning is activated for capacity planning work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level CSM capacity assessment and workforce planning.

---

## Problem Classification Taxonomy

### Type A: Current-State Audit
**Characteristics**: Request asks for a snapshot of existing capacity — actual vs. target ratios, load distribution, who is over/under.
**Primary Risk**: Presenting ratios without decomposing by segment and motion, masking pockets of severe overload behind acceptable averages.
**Expert Focus**: Segment-level ratio variance matters more than portfolio-wide averages — a balanced average can hide one segment at 2x target.

### Type B: Headcount Justification
**Characteristics**: Building a hiring case — required FTEs at current or projected ARR against target ratios.
**Primary Risk**: Producing a coverage-only number without cost context or growth assumptions, making the recommendation unactionable for finance.
**Expert Focus**: Distinguish current-ARR need from growth-adjusted need; present both so leadership sees the gap trajectory, not just today's snapshot.

### Type C: Redistribution / Rebalancing
**Characteristics**: Balancing load across existing CSMs without adding headcount — account moves, segment reassignment.
**Primary Risk**: Recommending moves that look numerically clean but ignore relationship continuity, renewal proximity, or active escalations.
**Expert Focus**: Red accounts and accounts within 60 days of renewal are not movable without a warm handoff plan — redistribution math must respect relationship constraints.

### Type D: Departure / Coverage Crisis
**Characteristics**: A CSM is leaving or on extended leave; their portfolio must be absorbed immediately.
**Primary Risk**: Distributing accounts evenly without triaging by urgency — Red accounts and imminent renewals need assignment within 24 hours, not "when convenient."
**Expert Focus**: Separate immediate-priority (Red + renewal < 60 days) from standard-priority; verify receiving CSMs won't exceed capacity limits that create a second crisis.

---

## Domain Heuristics

1. **The Averages Lie Rule**: Portfolio-wide account-per-CSM averages mask segment imbalance. Always decompose ratios by segment and motion before declaring capacity healthy.

2. **The 110% Threshold**: A CSM at 110% of target ratio is a yellow flag, not a crisis. Above 130%, Red account concentration rises non-linearly. Use 130% as the hard intervention trigger.

3. **The Renewal Proximity Lock**: Never redistribute an account within 60 days of renewal unless the current CSM is literally unavailable. Handoff friction near renewal accelerates churn risk more than overload does.

4. **The Red Account Freeze**: Red accounts stay with their current CSM unless that CSM is departing or above 130% capacity. Moving a Red account without a warm handoff and continuity plan worsens the situation.

5. **The Headcount Lag Rule**: Hiring takes 3-6 months from approval to productive CSM. If the gap is urgent, always pair headcount recommendations with an interim redistribution plan.

6. **The Unassigned Account Alarm**: Any account without a CSM owner is a coverage gap by definition. Surface the full list, total ARR, and health distribution — do not fold unassigned accounts into per-CSM averages.

7. **The Departure Triage Split**: In departure scenarios, split the portfolio into immediate-priority (Red + renewal < 60 days + active escalation) and standard-priority. Assign immediate accounts within 24 hours; standard within one week.

---

## Common Failure Modes by Request Type

### Current-State Audit Failures
- **Average masking**: Reporting portfolio-wide ratio as healthy when one segment is 2x target.
  --> Fix: Always show segment-level breakdown; flag any segment where actual exceeds target by >20%.
- **Missing unassigned accounts**: Excluding accounts with no CSM owner from the analysis entirely.
  --> Fix: Include unassigned accounts as a separate row; total their ARR and health distribution.

### Headcount Justification Failures
- **Coverage-only math**: Presenting FTE need without cost context or growth scenarios.
  --> Fix: Include cost estimate if fully-loaded CSM cost is configured; present current-ARR and growth-adjusted scenarios side by side.
- **Static snapshot**: Using today's account count without acknowledging pipeline or expected growth.
  --> Fix: Ask for growth assumption; if not provided, state the analysis uses current ARR only and flag the limitation.

### Redistribution Failures
- **Relationship-blind moves**: Recommending account transfers purely by count without checking renewal proximity, health status, or active escalations.
  --> Fix: Apply the Renewal Proximity Lock and Red Account Freeze heuristics before finalizing any move.
- **Silent handoff assumption**: Listing moves without specifying handoff requirements for high-ARR or at-risk accounts.
  --> Fix: Include a handoff requirements section for every moved account above configured ARR threshold.

### Departure/Coverage Failures
- **Flat distribution**: Spreading departing CSM's accounts evenly without urgency triage.
  --> Fix: Apply the Departure Triage Split — immediate vs. standard priority with different assignment SLAs.
- **Overloading receivers**: Assigning accounts to CSMs who are already at or near capacity, creating a cascade.
  --> Fix: Show post-assignment capacity for every receiving CSM; flag any who would exceed target after absorption.

---

## Expert Judgment Patterns

### Scope Decisions
- If the request mentions "planning" or "next quarter," treat as headcount justification (Type B) even if phrased as a current-state question.
- If a CSM name is mentioned with departure language, activate Type D regardless of other flags.

### Prioritization Decisions
- ARR concentration > account count when prioritizing which overloaded CSM to relieve first — a CSM with 8 accounts at $500K each is higher risk than one with 15 accounts at $20K each.
- Red account count relative to portfolio size matters more than absolute Red count — 3 Red out of 8 is worse than 5 Red out of 30.

### Confidence Decisions
- [High] when CRM + CS Platform data are live and ratios are configured in cs-ops profile.
- [Medium] when working from user-provided roster or partially stale data.
- [Low] when ratios are assumed (not configured) or account data is conversation-context only.

---

*Reasoning Blueprint: CSM Capacity Planning v1.0*
*For use with capacity-planner when Tier 3 reasoning is activated*
