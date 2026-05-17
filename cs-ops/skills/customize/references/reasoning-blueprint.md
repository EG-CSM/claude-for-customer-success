---
title: "Reasoning Blueprint: CS-Ops Configuration Management"
type: reasoning-blueprint
skill: customize
version: 1.0.0
---

# Reasoning Blueprint: CS-Ops Configuration Management

Load this blueprint when complex configuration scenarios require deeper reasoning.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level CS-Ops plugin configuration updates.

---

## Problem Classification Taxonomy

### Type A: Single-Section Update
**Characteristics**: User knows exactly which section to change and has the new values ready. Straightforward write with confirmation.
**Primary Risk**: Writing a valid value that is internally inconsistent with other sections (e.g., new segment without a matching ratio entry).
**Expert Focus**: Cross-section consistency check before confirming the write.

### Type B: Multi-Section Cascade
**Characteristics**: A structural change (territory restructure, headcount shift, segment redefinition) that requires coordinated updates across 2+ sections.
**Primary Risk**: Updating one section and forgetting downstream sections, leaving configuration internally contradictory.
**Expert Focus**: Map the full cascade before starting any writes — segments touch ratios, team, health thresholds, and possibly playbook triggers.

### Type C: Audit-Triggered Remediation
**Characteristics**: User arrives from an audit skill output (capacity-planner, health-model-review, data-quality-check) that flagged a configuration mismatch.
**Primary Risk**: Fixing the symptom the audit flagged without addressing the root configuration drift.
**Expert Focus**: Trace the audit finding back to the specific config value that caused it before proposing a change.

### Type D: Cold-Start Completion
**Characteristics**: Configuration exists but has multiple placeholder sections. User wants to fill gaps without re-running full cold-start-interview.
**Primary Risk**: Filling placeholders with generic defaults instead of values calibrated to the user's actual CS practice.
**Expert Focus**: Each placeholder section needs the same quality of guided interview that cold-start-interview would provide — shortcuts produce bad defaults.

### Type E: Configuration Review (--show)
**Characteristics**: Read-only inspection. User wants to see current state, not change it.
**Primary Risk**: Surfacing raw config without highlighting staleness, inconsistencies, or placeholder gaps.
**Expert Focus**: Configuration health assessment — are values internally consistent, current, and complete?

---

## Domain Heuristics

1. **The Cascade Rule**: Any change to segments, team, or health model affects at least one other section. Before writing, list affected sections and confirm the user wants to update them too.

2. **The Placeholder Gravity Rule**: Configurations with 3+ placeholder sections should be redirected to cold-start-interview. Section-by-section update is slower and produces less coherent results than a guided interview for bulk completion.

3. **The Confirmation Gate Rule**: Never batch confirmations. Show one proposed change, get one yes. Multiple changes in a single confirmation invite mistakes the user catches only later.

4. **The Staleness Signal Rule**: If the user hasn't run `--show` in 90+ days, the configuration has likely drifted from actual practice. Suggest a full review before targeted updates.

5. **The Threshold Continuity Rule**: Health tier thresholds must cover 0-100 with no gaps or overlaps. Validate arithmetic before confirming — a gap causes silent health assignment failures downstream.

6. **The SOP Sync Rule**: Escalation matrix and playbook changes create documentation debt. If a published SOP exists, flag that it needs updating in the same session — don't let config and docs diverge.

---

## Common Failure Modes by Classification Type

### Single-Section Update Failures
- **Cross-section orphan**: Adding a segment without creating its ratio entry or team assignment.
  -> Fix: After any segment add/modify, prompt for ratio and team updates before closing.
- **Silent threshold gap**: Modifying health tiers to values that don't cover the full range.
  -> Fix: Validate contiguity (sum check) before confirming the write.

### Multi-Section Cascade Failures
- **Partial cascade**: Updating segments and ratios but missing playbook trigger conditions that reference the old segment names.
  -> Fix: Map all sections that reference the changed entity before the first write.
- **Order-dependent corruption**: Writing team changes before segment changes, creating temporary inconsistency.
  -> Fix: Write in dependency order: segments -> ratios -> health -> team -> playbook -> escalation.

### Audit-Triggered Remediation Failures
- **Symptom fix**: Changing a ratio to satisfy a capacity audit without addressing the headcount change that caused the mismatch.
  -> Fix: Ask "what changed in your org that caused this?" before proposing a config fix.

### Cold-Start Completion Failures
- **Default stuffing**: Filling placeholder sections with industry averages instead of user-specific values.
  -> Fix: Run the same interview questions cold-start-interview uses for each section.

---

## Expert Judgment Patterns

### Scope Decisions
- If the user says "update my config" without specifying a section, run `--show` first to ground the conversation in current state.
- If a change touches segments, always ask about cascade impact before writing.

### Sequencing Decisions
- Write dependency order: segments -> ratios -> health -> team -> playbook -> escalation -> data-quality -> reporting.
- Show current values before asking for new values — users often don't remember what's configured.

### Depth Decisions
- Single-value change (e.g., one ratio number): confirm and write, minimal ceremony.
- Structural change (new segment, team restructure): full cascade mapping before any writes.
- Audit remediation: trace root cause before proposing fix.

### Safety Decisions
- Reset operations get two confirmation gates — the stakes justify the friction.
- Playbook archival requires CS lead approval confirmation — governance matters.
- Never write without showing the before/after diff — even for "obvious" changes.

---

*Reasoning Blueprint: CS-Ops Configuration Management v1.0*
*For use with customize when complex configuration scenarios are activated*
