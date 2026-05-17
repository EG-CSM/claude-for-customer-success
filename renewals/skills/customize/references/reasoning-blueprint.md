---
title: "Reasoning Blueprint: Renewals Profile Customization"
type: reasoning-blueprint
skill: customize
version: 1.0.0
---

# Reasoning Blueprint: Renewals Profile Customization

Load this blueprint when advanced reasoning is activated for renewals profile
customization work. It provides the domain-specific taxonomy, heuristics, and
expert judgment patterns that shape expert-level config editing.

---

## Problem Classification Taxonomy

### Type A: Single-Field Update
**Characteristics**: One field changed — discount authority ceiling updated, new AE partner, revised GRR target. Rest of profile is accurate.
**Primary Risk**: Writing the update without checking downstream consistency (e.g., new discount ceiling creates illogical walk-away floor).
**Expert Focus**: Trace the changed field to every skill that consumes it; surface downstream implications the user hasn't considered.

### Type B: Section Rebuild
**Characteristics**: Multiple fields within one section need updating — new escalation matrix, revised pricing model with tier restructure, full team turnover.
**Primary Risk**: Partial update — some fields in the section get new values while related fields retain stale values that now contradict.
**Expert Focus**: Treat the section as a unit; validate internal consistency across all fields before writing.

### Type C: Validation Audit
**Characteristics**: User runs `--validate` or asks "what's missing." No edits — diagnostic only.
**Primary Risk**: Surfacing field-level gaps without catching cross-field consistency issues (GRR/NRR inversion, threshold contradictions).
**Expert Focus**: Run structural completeness AND logical consistency checks; prioritize findings by downstream skill impact.

### Type D: Post-Cold-Start Completion
**Characteristics**: Cold-start interview was run but left placeholders or incomplete sections. User returns to fill gaps.
**Primary Risk**: Treating each placeholder independently instead of recognizing they may form a dependency chain (e.g., escalation contacts needed before risk-assessment can route).
**Expert Focus**: Sequence completions by downstream dependency — fill fields that unblock the most skills first.

---

## Domain Heuristics

1. **The Downstream Trace Rule**: Every config field feeds at least one skill. Before confirming a write, name which skills consume the changed field and what changes in their output.

2. **The Consistency Cascade Rule**: Any change to `targets`, `discount-authority`, or `pricing` can create cross-field contradictions. Run the four consistency checks (GRR/NRR inversion, discount floor vs. anchor, escalation SLA vs. renewal window, strategic threshold vs. deal size) after any edit to these sections.

3. **The Placeholder Priority Rule**: When multiple placeholders exist, resolve them in dependency order: `company` → `team` → `targets` → `escalation` → everything else. Skills that reference company name or escalation contacts fail most visibly.

4. **The Three-Section Threshold**: If the user needs to update 3+ sections, route to cold-start-interview. Customize is a scalpel, not a rebuild tool — using it for bulk edits introduces more error surface than a structured interview.

5. **The Show-Before-Edit Rule**: Never collect a new value without displaying the current value first. Config fields drive financial decisions — the user must see what they're replacing.

6. **The Section Isolation Rule**: Writing one section must never alter adjacent sections. If the file-write mechanism can't guarantee isolation, abort rather than risk silent corruption.

---

## Common Failure Modes by Classification Type

### Single-Field Update Failures
- **Silent downstream breakage**: Field updated but downstream skill implications not surfaced.
  Fix: Always run the downstream trace and include affected skills in confirmation output.
- **Consistency violation introduced**: New value contradicts a related field in another section.
  Fix: Run cross-field consistency checks before writing, not just after.

### Section Rebuild Failures
- **Partial section update**: Some fields updated, others left stale within the same section.
  Fix: Walk through every field in the section, even if user only mentioned one — show current value and ask "keep or change?"
- **Format mismatch**: New values entered in a format downstream skills don't expect (e.g., "about 10%" instead of "10%").
  Fix: Reference field definitions and validate format before writing.

### Validation Audit Failures
- **Completeness-only check**: Reports missing fields but skips logical consistency (GRR < NRR, threshold math).
  Fix: Always run both structural and logical checks in validate mode.
- **No prioritization**: Lists all issues with equal weight instead of ordering by downstream impact.
  Fix: Rank findings by number of skills affected and severity of impact.

### Post-Cold-Start Completion Failures
- **Random fill order**: User fills placeholders in the order they appear, not the order that unblocks the most value.
  Fix: Suggest completion sequence based on dependency chain when multiple placeholders exist.

---

## Expert Judgment Patterns

### Scope Decisions
- If user says "update my profile" without specifying a section, ask which section — don't assume.
- If user describes a change that spans 3+ sections, recommend cold-start-interview with explanation.
- If user asks to edit a field that doesn't exist in the schema, clarify whether it maps to an existing field or is genuinely unsupported.

### Sequencing Decisions
- Show current values before collecting new ones — always.
- Collect field-by-field, not all-at-once — reduces error rate on structured values like escalation contacts.
- Confirm before writing — never auto-write, even for single-field changes.

### Confidence Decisions
- [High] when editing a field with a clear schema definition and the user provides an unambiguous value.
- [Medium] when the user's input could map to multiple formats or the field has downstream consistency implications not yet checked.
- [Low] when the user describes a change but the target field is ambiguous or the value seems inconsistent with other configured fields.

---

*Reasoning Blueprint: Renewals Profile Customization v1.0*
*For use with customize when advanced reasoning is activated*
