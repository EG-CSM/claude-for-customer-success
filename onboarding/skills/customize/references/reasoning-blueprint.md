---
title: "Reasoning Blueprint: Onboarding Configuration Management"
type: reasoning-blueprint
skill: customize
version: 1.0.0
---

# Reasoning Blueprint: Onboarding Configuration Management

Load this blueprint when complex configuration scenarios arise for onboarding
profile management. It provides the domain-specific taxonomy, heuristics, and
expert judgment patterns that shape expert-level configuration guidance.

---

## Problem Classification Taxonomy

### Type A: Configuration Viewing
**Characteristics**: Read-only request — CSM wants to see current state, completeness, or specific section values. No writes involved.
**Primary Risk**: Displaying raw placeholder values without actionable guidance on what to fix first.
**Expert Focus**: Surface cross-section dependencies (e.g., incomplete graduation blocks handoff-doc) rather than just per-section status.

### Type B: Section Update
**Characteristics**: CSM wants to change one or more configuration values within a named section. Requires before/after confirmation and consistency checks.
**Primary Risk**: Writing a value that creates an internal consistency conflict with another section (e.g., TtV target < M4 day target).
**Expert Focus**: Anticipate downstream impacts — a milestone day change ripples into TtV targets, graduation timing, and at-risk signal windows.

### Type C: Section Reset
**Characteristics**: Destructive operation — CSM wants to restore template defaults for a section, erasing custom values.
**Primary Risk**: CSM resets without understanding that custom escalation contacts, graduation criteria, or model assignments are lost and must be manually re-entered.
**Expert Focus**: Verify the CSM's intent — often they want to fix one value, not wipe the section. Offer `--update` as the less destructive alternative.

### Type D: Configuration Validation
**Characteristics**: Health check across all sections — placeholder scan, required field presence, and internal consistency audit.
**Primary Risk**: Reporting PASS on sections that are technically complete but logically inconsistent (e.g., all milestones at Day 30 — valid format, nonsensical timing).
**Expert Focus**: Distinguish between structural completeness and operational readiness — a config can pass all field checks but still produce poor skill output.

### Type E: Scope Confusion
**Characteristics**: CSM requests a change that belongs to company-profile.md (company name, products, segments) rather than the onboarding config.
**Primary Risk**: Writing company-level settings into the onboarding config, creating a split-brain state between the two files.
**Expert Focus**: Redirect cleanly to `/cs-ops:customize` without making the CSM feel corrected.

---

## Domain Heuristics

1. **The Ripple Rule**: Any change to M4 day target must trigger a TtV consistency check — TtV cannot be shorter than the milestone that defines first value. Always cross-validate.

2. **The Placeholder Gravity Rule**: Sections with `[PLACEHOLDER]` values block downstream skills silently. Treat placeholder count as a priority signal — each one is a future skill failure.

3. **The Reset Regret Rule**: 80%+ of reset requests are actually update requests. Before executing a reset, ask whether the CSM wants to fix a specific value or truly start the section over.

4. **The Escalation Staleness Rule**: Named escalation contacts go stale faster than any other config value (role changes, departures, reorgs). After any escalation update, remind the CSM to verify contacts are current and aware.

5. **The Model-Escalation Coupling Rule**: When white-glove or partner-led models are active, the escalation section must include the corresponding executive sponsor or partner contact path. Model changes require escalation review.

6. **The Consistency Cascade Rule**: After updating milestones, always offer `--validate` — day-target changes create consistency risks that per-section checks cannot catch in isolation.

7. **The Immediate Effect Rule**: Config changes take effect on the next skill invocation with no staging environment. Warn explicitly when a change could alter in-progress account workflows.

---

## Common Failure Modes by Classification Type

### Configuration Viewing Failures
- **Status-only display**: Showing completeness indicators without explaining what each gap blocks.
  → Fix: Pair each incomplete section with the specific skills it blocks and a recommended fix command.
- **Missing cross-section context**: Showing each section in isolation without surfacing inter-section conflicts.
  → Fix: Include a summary footer noting any cross-section consistency issues detected.

### Section Update Failures
- **Silent consistency violation**: Writing a valid value that conflicts with another section (M5 < M4, TtV < M4).
  → Fix: Run consistency checks before confirming the write; present violations as blocking warnings.
- **Adjacent section overwrite**: Reformatting or rewriting sections not targeted by the update.
  → Fix: Read-before-write discipline — load full file, modify only the named section, preserve everything else byte-for-byte.

### Section Reset Failures
- **Unintended data loss**: CSM resets escalation contacts thinking they can undo it.
  → Fix: Show full current values before reset and offer to let CSM copy them; require typed confirmation.
- **Reset when update was intended**: CSM says "reset" but means "fix one value."
  → Fix: Before executing, ask: "Do you want to restore all defaults for this section, or update a specific value?"

### Configuration Validation Failures
- **False PASS on logical nonsense**: Sections pass structural checks but contain operationally meaningless values (all milestones same day, TtV of 1 day).
  → Fix: Add sanity-range checks beyond strict field presence (M1 < 7 days, M5 > 30 days for enterprise).
- **Missing skill-blocking analysis**: Reporting FAIL without mapping which downstream skills are affected.
  → Fix: Include a "Skills blocked by current config" section mapping failures to specific skill impacts.

---

## Expert Judgment Patterns

### Scope Decisions
- When a CSM asks to change company name, products, or segments: always redirect to `/cs-ops:customize` — never write company-level values into the onboarding config.
- When a CSM asks to update "everything": break into section-by-section updates rather than attempting a bulk write — each section has its own validation rules.

### Sequencing Decisions
- Fix graduation and escalation sections first — these block the most downstream skills.
- After any milestone update, run validation before proceeding to other sections.
- Update models before escalation — model selection determines which escalation paths are required.

### Safety Decisions
- When in doubt between reset and update, default to update — it preserves existing values.
- Always show before/after for writes; never write without explicit confirmation.
- After writing, remind the CSM that changes are live immediately — no staging buffer.

### Confidence Decisions
- [High] when reading existing config values or performing structural validation.
- [Medium] when advising on appropriate milestone day targets or TtV benchmarks — these are company-specific.
- [Low] when suggesting escalation contacts or graduation criteria content — only the CSM knows their org.

---

*Reasoning Blueprint: Onboarding Configuration Management v1.0*
*For use with customize when complex configuration scenarios arise*
