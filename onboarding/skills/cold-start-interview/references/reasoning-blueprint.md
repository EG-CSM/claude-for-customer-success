---
title: "Reasoning Blueprint: Cold-Start Interview"
type: reasoning-blueprint
skill: cold-start-interview
version: 1.0.0
---

# Reasoning Blueprint: Cold-Start Interview

Load this blueprint when Tier 3 reasoning is activated for onboarding
cold-start configuration work. It provides the domain-specific taxonomy,
heuristics, and expert judgment patterns that shape expert-level practice
profile collection and configuration writing.

---

## Problem Classification Taxonomy

### Type A: First-Time Full Setup
**Characteristics**: No existing config file. User is configuring the onboarding plugin from scratch with `--full` or default invocation.
**Primary Risk**: Collecting answers without validating internal consistency — e.g., TtV target that contradicts milestone day targets, or graduation criteria that reference fields not yet collected.
**Expert Focus**: Sequencing questions so earlier answers constrain later defaults. Detecting when a user's answers signal a model mismatch (says "white-glove" but describes guided-self-serve behaviors).

### Type B: Quick-Start Minimum Viable Config
**Characteristics**: `--quick` flag. User wants the fastest path to unlocking skills, accepting placeholders for non-critical fields.
**Primary Risk**: Writing a config that silently blocks downstream skills because the "minimum" missed a field a specific skill requires.
**Expert Focus**: Knowing exactly which fields gate which skills — the unlock/blocked report must be accurate, not approximate.

### Type C: Reconfiguration / Redo
**Characteristics**: `--redo` or `--section` against an existing config. Onboarding model, segments, or targets have changed.
**Primary Risk**: Overwriting still-valid sections, or updating one section without propagating implications to dependent sections (e.g., changing model from white-glove to guided-self-serve without revisiting milestone day targets).
**Expert Focus**: Displaying current values before asking, and flagging cross-section dependencies the user may not realize exist.

### Type D: Integration Health Check
**Characteristics**: `--check-integrations` only. No interview fields touched.
**Primary Risk**: Reporting a tool as "connected" when the auth token is valid but the data scope is insufficient (e.g., CRM connected but missing account-level read permissions).
**Expert Focus**: Testing data accessibility, not just connectivity. Updating status fields without touching any other config content.

---

## Domain Heuristics

1. **The Model-Behavior Mismatch Rule**: If a user selects an onboarding model but their answers to duration, kickoff format, and team structure contradict it, surface the mismatch before writing. A misconfigured model cascades into every downstream skill.

2. **The Placeholder Cascade Rule**: Every `[PLACEHOLDER]` field should be traceable to the specific skills it blocks. If you cannot name the blocked skill, the placeholder tracking is incomplete.

3. **The Defaults-Are-Dangerous Rule**: When a user accepts all defaults in a section (especially escalation matrix), flag that default role labels lack named contacts. Skills that route escalations will produce unusable output.

4. **The Cross-Section Dependency Rule**: Changing model, segments, or TtV targets in one section may invalidate milestone day targets, graduation criteria, or success criteria in another. After any `--section` update, scan adjacent sections for stale assumptions.

5. **The One-Question Discipline Rule**: Never batch questions. Each answer may change what to ask next — e.g., if the user says "partner-led" model, the kickoff format question changes entirely. Batching prevents adaptive sequencing.

6. **The Company Profile Boundary Rule**: `company-profile.md` is shared across all practice areas. Never overwrite it during a standard `--redo` — only `--redo-company-profile` touches it. Violations corrupt renewals and other practice configs.

---

## Common Failure Modes by Classification Type

### First-Time Full Setup Failures
- **Silent inconsistency**: TtV target says "21 days" but M3 (First use) is set to Day 21 and M4 (First value) to Day 30 — the user may not realize TtV and M4 are misaligned.
  → Fix: After collecting both, display TtV target alongside M4 target and ask user to confirm alignment or adjust.
- **Model mismatch accepted without challenge**: User picks "white-glove" but describes solo CSM with 50+ accounts.
  → Fix: Surface the tension explicitly: "White-glove typically implies low account ratios — does that match your portfolio size?"

### Quick-Start Failures
- **Inaccurate unlock report**: Reporting a skill as "unlocked" when it actually requires a field not collected in quick mode.
  → Fix: Maintain an explicit field-to-skill dependency map; generate the unlock report from the map, not from heuristics.
- **Placeholder amnesia**: User forgets which fields are still placeholder after quick setup, never completes them.
  → Fix: End with a concrete next-step: "Run `--redo` to complete, or `--section success-criteria` to unblock ttv-analysis."

### Reconfiguration Failures
- **Orphaned dependencies**: User changes onboarding model but milestone targets and graduation criteria still reflect the old model.
  → Fix: After writing the updated section, list sections that may need review given the change.
- **Overwrite without display**: Updating a section without showing current values first — user loses context on what they're replacing.
  → Fix: Always display current value before asking for update; accept Enter to keep unchanged.

### Integration Health Check Failures
- **Auth-only testing**: Reporting "connected" when the API token is valid but read scopes are insufficient.
  → Fix: Test a sample data retrieval (e.g., pull one account record), not just auth handshake.

---

## Expert Judgment Patterns

### Sequencing Decisions
- Collect model and segments before duration/milestones — the model constrains sensible defaults for everything downstream.
- Collect success criteria model before graduation criteria — graduation criteria reference success criteria state.
- Always check for existing company profile before starting Section 1.

### Scope Decisions
- If user provides partial context ("just update my milestones"), use `--section milestones` behavior even if invoked without the flag — confirm the implied scope before proceeding.
- If more than half the config is `[PLACEHOLDER]`, recommend `--full` over repeated `--section` calls.

### Validation Decisions
- Validate internal consistency at the section boundary (after each section completes), not only at the final review. Catching a mismatch in Section 3 is cheaper than catching it in the final summary.
- When displaying the final summary, group related fields so cross-section dependencies are visually adjacent.

---

*Reasoning Blueprint: Cold-Start Interview v1.0*
*For use with cold-start-interview when Tier 3 reasoning is activated*
