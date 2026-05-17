---
title: "Reasoning Blueprint: CS-Ops Cold-Start Interview"
type: reasoning-blueprint
skill: cold-start-interview
version: 1.0.0
---

# Reasoning Blueprint: CS-Ops Cold-Start Interview

Load this blueprint when advanced reasoning is activated for CS-Ops
configuration interview work. It provides the domain-specific taxonomy,
heuristics, and expert judgment patterns that shape expert-level practice
configuration capture.

---

## Problem Classification Taxonomy

### Type A: First-Install Full Configuration
**Characteristics**: No config file exists. User is running the interview for the first time across all seven sections.
**Primary Risk**: Interview fatigue — user abandons mid-interview, leaving partial config with silent gaps.
**Expert Focus**: Pace the interview, confirm after each section, and ensure every unanswered field gets `[PLACEHOLDER]` not silence.

### Type B: Section Reconfiguration
**Characteristics**: Config exists but user wants to update one section (e.g., `--section metrics` after a reorg or platform migration).
**Primary Risk**: Overwriting downstream dependencies — changing segment definitions without surfacing impact on capacity planning or reporting sections.
**Expert Focus**: Cross-reference the changed section against dependent sections and surface conflicts before writing.

### Type C: Conflict Resolution
**Characteristics**: Interview answers contradict existing `company-profile.md` or cross-plugin config values (e.g., segment ARR thresholds differ between CSM and CS-Ops configs).
**Primary Risk**: Silent overwrite — writing config that disagrees with the shared profile without surfacing the conflict.
**Expert Focus**: Detect and surface every cross-file conflict before writing; let the user decide which source of truth wins.

### Type D: Incomplete-Data Configuration
**Characteristics**: User cannot answer multiple questions — early-stage CS org, no formal health model, no documented segments.
**Primary Risk**: Inventing plausible defaults that masquerade as real configuration — downstream skills treat placeholders as real data.
**Expert Focus**: Use `[PLACEHOLDER]` markers liberally and explain which downstream skills will be limited until real values are provided.

---

## Domain Heuristics

1. **The Confirmation Gate Rule**: Never write config to disk without displaying the full file and receiving explicit "yes." Partial confirmations ("looks fine") on individual sections do not count.

2. **The Dependency Chain Rule**: Segments drive capacity planning, capacity drives reporting, reporting drives tooling priority. When reconfiguring one section, trace forward through the chain and flag downstream sections that may need updates.

3. **The Placeholder Honesty Rule**: A `[PLACEHOLDER]` that triggers a downstream skill to ask for input is better than a plausible guess that passes silently. When in doubt, placeholder.

4. **The Single Source of Truth Rule**: If `company-profile.md` already defines segments or metrics, the CS-Ops config must either reference or explicitly override — never silently diverge.

5. **The Fatigue Checkpoint Rule**: After section 4 of a full interview, check whether the user wants to continue or finish remaining sections later. Seven sections is a long interview.

6. **The "No Formal X" Rule**: When the user says they don't have a formal process (health model review, data quality audit, capacity tracking), record "No formal process" — do not invent one or suggest they should have one during the interview.

---

## Common Failure Modes by Classification Type

### First-Install Failures
- **Silent gap**: Skipping a question the user didn't answer and leaving no `[PLACEHOLDER]`
  -> Fix: After each section, enumerate unanswered questions and confirm they should be placeholders.
- **Premature write**: Writing config before all sections are complete or confirmed
  -> Fix: Full-file display + explicit confirmation gate is mandatory, no shortcuts.

### Section Reconfiguration Failures
- **Orphaned dependency**: Updating segments without flagging that capacity planning ratios reference the old segment names
  -> Fix: After any section edit, scan the existing config for references to changed values.
- **Version clobber**: Overwriting the entire config file when only one section changed
  -> Fix: Read existing config, merge the changed section, display the diff, confirm.

### Conflict Resolution Failures
- **Silent override**: Writing CS-Ops config that contradicts `company-profile.md` without surfacing the conflict
  -> Fix: Always diff new answers against `company-profile.md` before writing.

### Incomplete-Data Failures
- **Invented defaults**: Filling in "industry standard" values when the user said they don't track a metric
  -> Fix: Record exactly what the user said; use `[PLACEHOLDER]` or "Not tracked" — never synthesize.
- **Scope creep into consulting**: Turning the configuration interview into a maturity assessment or recommendations session
  -> Fix: Capture current state only; recommendations belong in downstream skills.

---

## Expert Judgment Patterns

### Pacing Decisions
- Full interview with an engaged user: run all seven sections sequentially with per-section confirmation.
- Full interview with a time-pressed user: prioritize sections 1 (metrics), 3 (segments), and 6 (tooling) — these gate the most downstream skills. Offer to complete remaining sections in a follow-up.
- Section reconfiguration: complete the target section, then scan for cross-section impacts before writing.

### Conflict Decisions
- When CS-Ops config and `company-profile.md` disagree on a factual value (ARR thresholds, segment names): surface the conflict, ask which is current, update both or note the intentional divergence.
- When the user gives an answer that contradicts a previous answer in the same interview: surface it immediately ("In section 1 you said X, but here you're saying Y — which is correct?").

### Completeness Decisions
- A config with `[PLACEHOLDER]` markers in non-critical sections is shippable — downstream skills will prompt for the missing data.
- A config with `[PLACEHOLDER]` in metrics or segments is functional but limited — flag which skills will produce generic output until these are filled.

---

*Reasoning Blueprint: CS-Ops Cold-Start Interview v1.0*
*For use with cold-start-interview skill*
