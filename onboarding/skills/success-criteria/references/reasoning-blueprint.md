---
title: "Reasoning Blueprint: Onboarding Success Criteria"
type: reasoning-blueprint
skill: success-criteria
version: 1.0.0
---

# Reasoning Blueprint: Onboarding Success Criteria

Load this blueprint when advanced reasoning is activated for success criteria work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level criteria definition, refinement, and review.

---

## Problem Classification Taxonomy

### Type A: Greenfield Definition
**Characteristics**: No existing criteria; CSM is starting from scratch with sales context and customer goals.
**Primary Risk**: Criteria are CSM hypotheses disconnected from what the customer actually said they wanted.
**Expert Focus**: Anchor every criterion to a named customer statement or sales artifact before drafting.

### Type B: Scope-Triggered Refinement
**Characteristics**: Existing criteria need revision due to a scope change, stakeholder shift, product capability adjustment, or date shift.
**Primary Risk**: Revising criteria without re-confirming with the customer — the CSM adjusts internally and treats revised criteria as agreed.
**Expert Focus**: Distinguish which criteria are genuinely affected vs. reflexively rewritten; preserve confirmed criteria that still hold.

### Type C: Progress Review
**Characteristics**: Criteria are confirmed; CSM needs a progress assessment against a milestone checkpoint.
**Primary Risk**: Review becomes a status report instead of a diagnostic — at-risk criteria get reported but not root-caused.
**Expert Focus**: For every at-risk criterion, classify the block type (customer / technical / CSM) before recommending action.

### Type D: Customer-Facing Export
**Characteristics**: Criteria are confirmed and need to be formatted for customer consumption.
**Primary Risk**: Internal labels, confidence signals, or unconfirmed flags leak into the customer-facing document.
**Expert Focus**: Verify every criterion is confirmed with the customer before exporting — unconfirmed criteria must not appear.

---

## Domain Heuristics

1. **The Sales Echo Rule**: The strongest criteria come from echoing what the customer said during sales, not from what the CSM thinks the product can do. If no sales context exists, the first discovery question must surface the customer's own words.

2. **The 3-5 Ceiling**: More than 5 criteria always indicates a prioritization failure, not a complex customer. Force-rank and cut. Three sharp criteria outperform seven vague ones.

3. **The Confirmation Gap**: A criterion defined in a CSM-only session is a hypothesis until the customer confirms it. Track the gap explicitly — unconfirmed criteria cannot drive milestone tracking.

4. **The M4 Anchor Test**: If the single most important Day 30 outcome is not named as a criterion, the set is misaligned. The M4 anchor criterion is the one the customer would notice is missing.

5. **The Measurability Gate**: If the CSM cannot name how they will know a criterion is met, the criterion is not ready. "The team is comfortable" fails; "zero manual exports in the last two weeks" passes.

6. **The Milestone Orphan Check**: A criterion that does not map to M2, M3, M4, or M5 belongs in the post-onboarding relationship, not the onboarding plan. Orphaned criteria dilute focus.

7. **The Graduation Alignment Rule**: The M5 criterion must align with the configured graduation criteria. If they diverge, either the criterion or the config is wrong — surface the gap.

---

## Common Failure Modes by Type

### Greenfield Definition Failures
- **CSM Projection**: CSM drafts criteria from product knowledge rather than customer input.
  Fix: Start with Step 1 (sales echo) and draft only from customer-stated goals before adding CSM perspective.
- **Scope Creep Past 5**: CSM lists 7-8 candidate criteria and expects all to be included.
  Fix: Facilitate prioritization explicitly — present the 3-5 ceiling as a design constraint, not a suggestion.
- **Vague Anchor Criterion**: M4 criterion is aspirational rather than observable ("customer sees value").
  Fix: Apply the measurability gate — ask "how will you know?" and rewrite until the answer is concrete.

### Scope-Triggered Refinement Failures
- **Silent Re-Confirmation Skip**: CSM revises criteria internally without flagging re-confirmation need.
  Fix: Every revised criterion gets `[Requires re-confirmation with customer]` — no exceptions.
- **Wholesale Rewrite**: A single scope change triggers rewriting all criteria instead of isolating the affected ones.
  Fix: Ask which specific criteria are affected before revising; preserve unaffected confirmed criteria.

### Progress Review Failures
- **Status Without Diagnosis**: At-risk criteria are reported but not root-caused — "at risk" with no block type or action.
  Fix: For every at-risk criterion, require block classification (customer / technical / CSM) and one recommended action.
- **Anchor Deprioritization**: M4 or M5 anchor criterion is at risk but treated with the same urgency as intermediate criteria.
  Fix: Flag anchor criteria at risk with explicit priority escalation.

### Customer-Facing Export Failures
- **Internal Label Leak**: Confidence signals, pending-confirmation flags, or reviewer notes appear in export.
  Fix: Run export only after confirming all criteria; strip all internal markers before output.

---

## Expert Judgment Patterns

### Scope Decisions
- When a scope change affects more than 2 criteria, treat it as a re-definition session (Type A), not a refinement.
- When a stakeholder change affects the owner of the M4 anchor criterion, escalate to a confirmation call before revising.

### Prioritization Decisions
- When the CSM has 6+ candidate criteria, ask: "If the customer could only achieve three of these, which three would they pick?" The customer's priority order, not the CSM's, drives the cut.
- When criteria span multiple product areas, verify each area is achievable within the onboarding window before including it.

### Confidence Decisions
- High confidence when criteria are confirmed with the customer and map to observable measures with milestone anchors.
- Medium confidence when criteria are CSM-confirmed but pending customer validation.
- Low confidence when criteria are inferred from sales notes without direct customer input.

### Timing Decisions
- Run --review at each milestone checkpoint, not only when problems surface — proactive review catches drift before it becomes risk.
- Run --refine immediately after a scope change is identified, not at the next scheduled review — delayed refinement creates phantom criteria the customer has already abandoned.

---

*Reasoning Blueprint: Onboarding Success Criteria v1.0*
*For use with success-criteria skill*
