---
title: Expansion Onboarding Reasoning Blueprint
type: reasoning-blueprint
skill: expansion-onboarding
version: 1.0.0
---

# Expansion Onboarding — Reasoning Blueprint

## Problem Classification Taxonomy

### Type A — Clean CSQL Win, Immediate Onboarding
- **Characteristics:** CSQL marked won, stakeholders identified, scope clear, no open questions from the sales motion
- **Primary Risk:** Skipping structure — CSM moves straight to execution without a documented plan, leaving no artifact for handoffs or reviews
- **Expert Focus:** Completeness of the milestone scaffold; confirm the success definition is documented before kicking off the first milestone

### Type B — CSQL Win with Scope Ambiguity
- **Characteristics:** CSQL won but expansion scope, stakeholders, or timeline still being finalized
- **Primary Risk:** Creating a plan against a moving target — milestone dates and success definitions need anchoring before the plan is treated as authoritative
- **Expert Focus:** Flag ambiguity in the plan; use placeholder values with explicit "needs confirmation" markers; do not treat as complete until scope is locked

### Type C — Expansion Onboarding Mid-Flight
- **Characteristics:** Plan already active; update or milestone progress operation
- **Primary Risk:** Losing prior state — append-only structure must be preserved; prior milestones should not be overwritten
- **Expert Focus:** Ensure the update is appended correctly; verify timestamp and milestone reference are accurate; do not re-generate the full plan

### Type D — Expansion Onboarding Closure
- **Characteristics:** Close operation; adoption confirmed
- **Primary Risk:** Closing before adoption is actually confirmed — premature closure removes the operational artifact from view
- **Expert Focus:** Adoption confirmation statement must be substantive (what was adopted, by whom); plan becomes read-only after close so the statement must be complete

## Domain Heuristics

### H1 — One Active Plan Per Account
Only one expansion onboarding plan should be active per account at a time. Creating a new plan when one is already active indicates a scope or CSQL tracking error upstream. Flag the conflict before proceeding.

### H2 — Four-Milestone Scaffold Is the Default
Expansion onboarding plans default to four milestones unless the CSM provides a different structure. The scaffold (kickoff, adoption baseline, adoption checkpoint, confirmed adoption) maps to the standard Stage 4 motion.

### H3 — Success Definition Before Milestone Execution
The success definition must be present in the plan before any milestone is marked as in-progress. A plan without a success definition has no objective completion criteria.

### H4 — Plan Closure Is Irreversible
Once closed with an adoption confirmation statement, the plan artifact is read-only. Ensure all progress notes and milestone updates are complete before executing close.

### H5 — AE Handoff Context Travels With the Plan
The plan artifact is the system of record for AE handoffs and CSM manager reviews. Context that exists only in the CSM's head is not captured — push key decisions and blockers into the plan notes.

### H6 — Downstream Dependency on rev-ops:csql-tracking
The won CSQL event from `rev-ops:csql-tracking` is the authoritative input for account name, CSQL scope, and deal context. If that data is incomplete or stale, surface it as a data gap rather than inferring.

## Common Failure Modes

### Type A (Clean Win)
1. **No success definition** — Plan created without a documented success definition. Fix: Require the CSM to supply a success definition before treating the plan as ready for execution.
2. **Stakeholder field left blank** — Plan created with no stakeholders listed. Fix: Flag as a gap; a plan without stakeholders has no accountability chain.

### Type B (Scope Ambiguity)
1. **Treating ambiguous scope as confirmed** — Generating a fully specific plan against unresolved scope. Fix: Use explicit placeholders and add a scope-confirmation note to the plan header.
2. **Milestone dates invented** — CSM hasn't provided dates; plan uses fabricated target dates. Fix: Leave dates as TBD and note that they require CSM input.

### Type C (Mid-Flight Update)
1. **Overwriting prior state** — Update operation replaces earlier progress notes. Fix: Append-only; prior state must be preserved with timestamp separation.
2. **Wrong plan referenced** — Update applied to a closed or different account's plan. Fix: Verify account name and plan creation date before writing the update.

### Type D (Closure)
1. **Adoption confirmation is a formality** — Statement is generic ("adoption confirmed") with no substance. Fix: Require specifics — what was adopted, confirmed by whom, any follow-on actions.
2. **Unclosed milestones at closure** — Milestones still in-progress when plan is closed. Fix: Flag and require resolution or documented explanation before accepting closure.

## Expert Judgment Patterns

### Scope Decisions
- If CSQL context is complete and unambiguous, generate a full plan with all four milestones
- If context is partial, generate a plan with explicit TBD markers and add a pre-flight note listing what the CSM still needs to provide

### Operation Routing
- `create`: new plan artifact, full scaffold, new context file
- `update`: append to existing plan, preserve all prior content, update milestone status only
- `close`: add adoption confirmation block, mark plan read-only, no further updates accepted

### Stakeholder Decisions
- If expansion stakeholders differ from the core account team, note the distinction in the plan — different stakeholders may require different communication cadence
- Route adoption confirmation sign-off to the AE if ARR uplift exceeds org escalation threshold

### Confidence Decisions
- CSQL data from rev-ops integration: high confidence
- Milestone dates estimated by CSM: moderate confidence — treat as targets, not commitments
- Adoption confirmation from CSM verbal report only (no CS platform data): moderate confidence — flag data gap in closure record
