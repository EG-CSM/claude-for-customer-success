---
title: "Reasoning Blueprint: Onboarding Graduation Handoff"
type: reasoning-blueprint
skill: handoff-doc
version: 1.0.0
---

# Reasoning Blueprint: Onboarding Graduation Handoff

Load this blueprint when Tier 3 reasoning is activated for onboarding handoff work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level account context transfer from onboarding to post-onboarding teams.

---

## Problem Classification Taxonomy

### Type A: Clean Graduation
**Characteristics**: All graduation criteria met, milestone dates on track, stakeholders engaged, no open blockers.
**Primary Risk**: Complacency — skipping the readiness check because everything looks fine, missing subtle gaps in stakeholder handoff or unverified success criteria.
**Expert Focus**: Verify success criteria were confirmed by the customer, not assumed by the CSM. Check that the receiving team has been introduced, not just named.

### Type B: Conditional Graduation
**Characteristics**: Most criteria met but 1-2 items pending — typically adoption gaps, incomplete integrations, or one unconfirmed success criterion.
**Primary Risk**: Transferring an account with unresolved items that have no owner on the receiving side — orphaned problems that erode trust in the first 30 days.
**Expert Focus**: Every open item must have a named owner and a target date before the handoff document is generated. The override justification must be specific, not boilerplate.

### Type C: Model-Variant Handoff
**Characteristics**: Onboarding model (white-glove, implementation-plus-handoff, partner-led) requires model-specific sections and relationship context that standard handoffs omit.
**Primary Risk**: Generating a generic handoff that drops the executive relationship section (white-glove), technical implementation context (impl+handoff), or partner alignment notes (partner-led).
**Expert Focus**: Confirm onboarding model from config and include the correct model-specific section. Missing model context leaves the receiving team blind to the account's service structure.

### Type D: Summary / Async Handoff
**Characteristics**: Full handoff document exists; CSM needs an abbreviated brief for a verbal or async transfer.
**Primary Risk**: The summary replaces the full document instead of supplementing it. Critical context (open items, risk flags, stakeholder nuances) gets lost in compression.
**Expert Focus**: Verify the full --draft document exists and is accessible before generating the summary. The summary is a pointer, not a standalone record.

---

## Domain Heuristics

1. **The Readiness-First Rule**: Always run --readiness before --draft. A handoff doc generated without a graduation check may transfer an account that isn't ready. No exceptions without documented override.

2. **The Owner-or-Orphan Rule**: Every open item in Section 6 must have a named owner. If the onboarding CSM is listed as owner on a transferring item, it's orphaned — the receiving team won't pick it up without explicit assignment.

3. **The Customer-Confirmed Rule**: Success criteria marked "Achieved" must have evidence of customer confirmation — call notes, email, or written acknowledgment. CSM assumption alone is not confirmation.

4. **The Staleness Gate**: CRM data older than 7 days and PM data older than 3 days must be flagged with timestamp and staleness indicator. Contact information is the most commonly stale — always ask the CSM to verify.

5. **The 30-Day Lens**: Every section of the handoff should answer: "What does the receiving team need to know or do in their first 30 days?" Context without actionability is noise.

6. **The Expansion-Is-Observation Rule**: Expansion signals are observations for the AE and receiving CSM to evaluate. Converting observations to pipeline commitments in a handoff document is not the onboarding CSM's job.

---

## Common Failure Modes by Classification Type

### Clean Graduation Failures
- **Assumed success criteria**: CSM marks criteria achieved without customer confirmation.
  -> Fix: Cross-reference each criterion against call notes, emails, or CRM activity for customer acknowledgment.
- **Stale stakeholder contacts**: People changed roles during onboarding; CRM contacts are outdated.
  -> Fix: Ask CSM to verify all contacts before generating the document. Flag unverified in reviewer note.

### Conditional Graduation Failures
- **Ownerless open items**: Items transferred without a named owner on the receiving side.
  -> Fix: Refuse to finalize Section 6 until every item has a named owner and target date.
- **Boilerplate override justification**: CSM overrides HOLD with "business decision" instead of specific reasoning.
  -> Fix: Require the justification to name the unmet criterion, the risk, and the mitigation plan.

### Model-Variant Failures
- **Missing model-specific section**: Generic handoff generated for a white-glove account, omitting executive relationship context.
  -> Fix: Check onboarding model from config before generating. Include the correct Section 8 variant.
- **Wrong escalation path**: Post-onboarding escalation doesn't match the model's service structure.
  -> Fix: Pull escalation matrix from config and validate it matches the onboarding model.

### Summary Failures
- **Summary as replacement**: No full --draft exists; summary becomes the authoritative record.
  -> Fix: Check for existing full document before generating summary. Warn if none exists.
- **Critical context dropped**: Open items or risk flags omitted from the summary.
  -> Fix: "What to watch" section must always include open items and risk flags, even in compressed form.

---

## Expert Judgment Patterns

### Scope Decisions
- If graduation criteria are placeholders, warn and offer cold-start-interview before proceeding with generic criteria.
- If CRM and PM connectors are both unavailable, shift to interview mode — ask the CSM for structured input rather than generating empty templates.

### Sequencing Decisions
- Always run readiness check first, even when the CSM is confident the account is ready — the check catches what confidence misses.
- Pull CRM data before PM data — account identity and contract context frames the milestone interpretation.

### Depth Decisions
- Match output mode to the actual need: a CSM with 10 minutes before a handoff call needs --summary, not --draft. Ask if mode wasn't specified.
- Model-specific sections only appear when the config declares that model — never include all three "just in case."

### Stakeholder Decisions
- The receiving team is the primary audience for --draft. Write for someone who has never spoken to this customer.
- The onboarding CSM is the primary reviewer — they verify accuracy before the document reaches the receiving team.

---

*Reasoning Blueprint: Onboarding Graduation Handoff v1.0*
*For use with handoff-doc when Tier 3 reasoning is activated*
