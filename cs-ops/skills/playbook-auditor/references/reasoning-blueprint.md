---
title: "Reasoning Blueprint: Playbook Audit"
type: reasoning-blueprint
skill: playbook-auditor
version: 1.0.0
---

# Reasoning Blueprint: Playbook Audit

Load this blueprint when Tier 3 reasoning is activated for playbook audit work.
It provides the domain-specific taxonomy, heuristics, and expert judgment
patterns that shape expert-level CS playbook assessment.

---

## Problem Classification Taxonomy

### Type A: Coverage Gap Analysis
**Characteristics**: Request focuses on whether the right plays exist — mapping configured plays against baseline CS scenarios to find holes.
**Primary Risk**: Treating all gaps as equal severity — a missing churn-prevention play in a segment with 60% ARR concentration is not the same as a missing relationship play in tech-touch.
**Expert Focus**: Weight gaps by ARR exposure and scenario frequency, not just count.

### Type B: Play Quality Audit
**Characteristics**: Plays exist but may have vague triggers, unmeasurable outcomes, or incomplete TARO structure. Request targets whether plays are well-defined enough to execute consistently.
**Primary Risk**: Accepting "looks reasonable" triggers that two CSMs would interpret differently — the inter-rater reliability test.
**Expert Focus**: Apply the "two CSMs, same account, same moment" test to every trigger.

### Type C: Adoption & Effectiveness Review
**Characteristics**: Request centers on whether plays are actually being used and producing results. Requires activation history data.
**Primary Risk**: Conflating low activation with CSM non-compliance — low activation may reflect segment fit, trigger narrowness, or platform logging gaps.
**Expert Focus**: Separate signal (play doesn't fit) from noise (play isn't logged) before drawing conclusions.

### Type D: Dead Play / Bloat Cleanup
**Characteristics**: Request targets plays that exist but are never triggered — candidates for archival, trigger revision, or retraining.
**Primary Risk**: Archiving a play for an infrequent-but-critical scenario (e.g., acquisition) and losing the structured response when it next occurs.
**Expert Focus**: Check scenario frequency before recommending archival — dead is not the same as dormant.

### Type E: Single-Play Deep Dive
**Characteristics**: Focused audit of one named play — trigger, steps, outcome, activation history, TARO completeness.
**Primary Risk**: Auditing the play in isolation without checking whether its scenario is actually covered by a different play (overlap) or whether it conflicts with adjacent plays.
**Expert Focus**: Check for trigger overlap and handoff gaps with adjacent plays.

---

## Domain Heuristics

1. **The Two-CSM Rule**: A trigger is specific enough only if two CSMs reading it independently would activate the play at the same moment for the same account. If not, the trigger needs a threshold.

2. **The ARR Gravity Rule**: Coverage gaps should be weighted by ARR concentration in affected segments. A gap affecting 5% of ARR is a backlog item; a gap affecting 40% is a P1.

3. **The Outcome Closure Test**: If a play's outcome cannot be confirmed by checking a single observable state in the CS platform or CRM, the play will accumulate as perpetually open. Vague outcomes are operational debt.

4. **The 90-Day Frequency Check**: Before recommending a dead play for archival, check whether the scenario it covers has occurred in the last 12 months. Infrequent scenarios still need structured responses.

5. **The Adoption Floor Rule**: If fewer than 50% of eligible CSMs have activated a play in a quarter, the issue is systemic (trigger, training, or platform) — not individual performance.

6. **The Motion Match Rule**: Not every play applies to every CS motion. A play designed for high-touch executive engagement is noise in a tech-touch segment. Check motion scope before flagging adoption gaps.

7. **The Trigger Cascade Check**: When a play trigger overlaps with another play's trigger, check which fires first and whether handoff is defined. Undefined cascade = inconsistent execution.

---

## Common Failure Modes by Audit Type

### Coverage Gap Failures
- **Equal-weight gap listing**: Listing all gaps without severity weighting by ARR or frequency.
  → Fix: Rank gaps by ARR concentration in affected segment and estimated scenario frequency.
- **Segment-blind baseline**: Applying the full 24-scenario baseline to a tech-touch segment where half the scenarios don't apply.
  → Fix: Filter baseline by configured CS motion before scoring coverage.

### Play Quality Failures
- **Surface-pass trigger review**: Marking a trigger as "specific" because it names a metric without checking for a threshold or time window.
  → Fix: Apply the two-CSM rule — if the trigger lacks a threshold, it's vague regardless of metric naming.
- **Outcome conflation**: Accepting "improve health" or "resolve issue" as measurable outcomes.
  → Fix: Require the format: "[observable state] by [timeframe], confirmed by [evidence source]."

### Adoption Failures
- **Blaming CSMs for low activation**: Interpreting zero activations as non-compliance without checking segment fit, trigger design, or logging behavior.
  → Fix: Check three causes before attribution — trigger too narrow, segment mismatch, platform logging gap.
- **Ignoring outcome achievement rates**: Reporting activation counts without checking whether activated plays actually achieved their documented outcome.
  → Fix: Always pair activation rate with outcome achievement rate.

### Dead Play Failures
- **Premature archival**: Recommending archival for a play covering a rare but high-impact scenario (acquisition, regulatory event).
  → Fix: Apply the 90-day frequency check and confirm with CS lead before any archival recommendation.

---

## Expert Judgment Patterns

### Scope Decisions
- Full audit is the default; narrow to coverage-only when the playbook is new and adoption data doesn't exist yet.
- Single-play deep dive when a specific play is underperforming and the team needs root cause, not a portfolio view.

### Severity Decisions
- Coverage gap in churn-prevention with ARR >30% exposure = High. Expansion or relationship gap = Medium unless segment-specific ARR says otherwise.
- Trigger vagueness is always higher priority than coverage additions — vague triggers undermine plays that already exist.

### Data Sufficiency Decisions
- Adoption analysis without activation history is speculation — state this and skip the section rather than guessing.
- When only a play list (no activation data) is available, run coverage + quality only and flag adoption as "requires data."

### Recommendation Sequencing
- Fix vague triggers before adding new plays — new plays with vague triggers compound the problem.
- Archive dead plays before building replacements — confirm the gap still exists after cleanup.

---

*Reasoning Blueprint: Playbook Audit v1.0*
*For use with playbook-auditor when Tier 3 reasoning is activated*
