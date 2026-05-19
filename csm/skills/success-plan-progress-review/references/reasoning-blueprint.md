---
title: Success Plan Progress Review Reasoning Blueprint
type: reasoning-blueprint
skill: success-plan-progress-review
version: 1.0.0
---

# Success Plan Progress Review — Reasoning Blueprint

## Problem Classification Taxonomy

### Type A — Routine Progress Review, Green Trajectory
- **Characteristics:** Milestones On Track; OCV outcomes In Progress or Delivered; success criteria trending toward met
- **Primary Risk:** Shallow review — a Green trajectory doesn't mean no action items; milestones running on schedule but without substance still fail at the success criteria check
- **Expert Focus:** Even On Track reviews need a value story; confirm success criteria progress, not just milestone cadence

### Type B — At-Risk Milestone Review
- **Characteristics:** One or more milestones At Risk; OCV outcomes Blocked or Not Started; success criteria status uncertain
- **Primary Risk:** Treating each risk independently — multiple At Risk milestones may share a root cause; addressing symptoms individually misses the systemic issue
- **Expert Focus:** Identify whether risks are independent or connected; the action list should address root causes, not just milestone-level symptoms

### Type C — QBR Pre-Work Review
- **Characteristics:** Review generated in preparation for a Quarterly Business Review; customer-facing summary and QBR pre-work note required
- **Primary Risk:** Customer-facing summary is too internal — CSM action items, risk flags, and internal-only context should not appear in the customer summary
- **Expert Focus:** Hard separation between internal scorecard and customer-facing summary; QBR pre-work note should be executive-ready, not operational

### Type D — Post-Missed-Milestone Review
- **Characteristics:** One or more milestones marked Missed; account may be at risk
- **Primary Risk:** Documenting the miss without actioning it — a Missed milestone note that only records what didn't happen provides no path forward
- **Expert Focus:** Every Missed milestone requires a clear action item: recovery plan, timeline adjustment, or escalation routing

## Domain Heuristics

### H1 — Canvas Is the Authoritative Source
The upstream success plan canvas from `csm:success-plan-canvas` is the authoritative source for plan structure, success criteria, and milestone definitions. If the canvas is incomplete or outdated, the progress review inherits those gaps. Flag canvas quality issues before generating the review.

### H2 — Milestone Scorecard Is Not the Final Product
The milestone scorecard is a component of the review, not the deliverable. The deliverable is the action list — what the CSM will do next based on the scorecard state.

### H3 — OCV Outcome Ratings Drive the Value Narrative
OCV outcome ratings (Delivered / In Progress / Not Started / Blocked) are the primary evidence for the value story at renewal. A review without OCV ratings is missing its strongest retention argument.

### H4 — Customer-Facing Summary Has a Different Audience
The customer-facing summary is for executive stakeholders, not operational reviewers. It should lead with value delivered, not with process status. CSM internal notes and action items never appear in the customer-facing summary.

### H5 — Point-in-Time Snapshot
The progress review is a snapshot artifact. It captures state at the time of generation and is not updated retroactively. If milestones change after generation, a new review must be generated.

### H6 — Milestone Rating Guide Is Authoritative
Consult `reference/milestone-rating-guide.md` for On Track / At Risk / Missed definitions and rating criteria. Do not apply subjective or informal rating criteria.

## Common Failure Modes

### Type A (Green Trajectory)
1. **No action items for Green accounts** — Review completed with no actions because "everything is fine." Fix: Even Green reviews should confirm executive sponsor engagement and surface the next value touchpoint.
2. **Milestone status without substance** — Scorecard shows On Track but no evidence of what's been accomplished. Fix: Each On Track milestone should have a progress note, not just a status.

### Type B (At-Risk)
1. **Independent treatment of connected risks** — Three At Risk milestones attributed to three different causes when the root cause is one shared dependency gap. Fix: Assess risks for shared root causes before assigning action items.
2. **Action items without owners** — Risk action list has tasks but no assigned owner or timeline. Fix: Each action item requires a clear owner (CSM, AE, customer, CS Lead) and a target date.

### Type C (QBR Pre-Work)
1. **Internal content in customer summary** — CSM notes, escalation flags, or internal ARR discussions appear in the customer-facing output. Fix: Generate the internal scorecard first; strip all internal content before producing the customer summary.
2. **QBR pre-work note is operational, not executive** — Pre-work note lists tactical milestones rather than strategic value. Fix: QBR pre-work note leads with business impact and outcome delivery, not process status.

### Type D (Missed Milestone)
1. **Documentation without action** — Missed milestone recorded with no recovery plan. Fix: Every Missed milestone requires an action item: recovery timeline, adjusted target, or escalation.
2. **Missed milestone understated** — Framed as a minor delay rather than a review signal. Fix: Missed milestones trigger a review of whether the success criteria timeline is still achievable; document that assessment.

## Expert Judgment Patterns

### Scope Decisions
- If the upstream canvas is incomplete (missing milestones, absent success criteria), flag and request an updated canvas before generating the review
- If all milestones are On Track but OCV outcomes are Not Started, flag the disconnect — schedule performance and outcome delivery are not the same thing

### Output Component Decisions
- Customer-facing summary: generate only when explicitly requested or for QBR pre-work
- QBR pre-work note: generate only for Type C reviews; lead with strategic value narrative
- Internal scorecard and action list: always generated

### Risk Escalation Routing
- At Risk + executive sponsor disengaged: route to CSM Lead
- Missed milestone + ARR above threshold: route to AE
- Multiple Missed milestones: trigger renewal readiness assessment

### Confidence Decisions
- Milestone status from CSM-provided updates: moderate confidence — CSM self-report; verify against CS platform data where available
- OCV outcome ratings from live catalog: high confidence
- Success criteria met/not-met assessment from CSM judgment only: moderate confidence — document basis for the assessment
