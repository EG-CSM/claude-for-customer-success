# Reasoning Protocol Quality Rubric

**Version:** 1.0
**Date:** 2026-05-15
**Purpose:** Evaluate remediated tier-1 reasoning protocols across 41 SKILL.md files
**Status:** [PROPOSED]

---

## Rubric Structure

Each dimension has 5 components: What it tests / Observable evidence / Measurement method / Pass threshold / Gaming vulnerability.

---

## Dimension 1: Tier-1 Format Compliance

**What it tests:** Does the protocol follow the required CLASSIFY → CONSTRAINTS → EXPERT CHECK → ANTI-PATTERNS + post-execution verification structure?

**Observable evidence:**
- Section heading is `## Reasoning Protocol`
- Opening line is `Before generating output, apply these primers:`
- Exactly 4 numbered primers: CLASSIFY, CONSTRAINTS, EXPERT CHECK, ANTI-PATTERNS (in order)
- Post-execution verification block starting with `**After execution**, verify:`
- Confidence calibration line with High/Medium/Low bands

**Measurement method:** Structural regex + manual check. Grep for heading, opening line, 4 primer labels, post-execution block, confidence line.

**Pass threshold:** All 6 structural elements present. Missing any one = FAIL.

**Gaming vulnerability:** A protocol could copy the structure verbatim while filling it with generic content. Mitigated by Dimension 2 (domain specificity) — format compliance alone is necessary but not sufficient.

---

## Dimension 2: Domain Specificity

**What it tests:** Are the CLASSIFY types, CONSTRAINTS, EXPERT CHECK items, and ANTI-PATTERNS specific to the skill's domain rather than generic CS boilerplate?

**Observable evidence:**
- CLASSIFY types name domain-specific scenarios (not "simple request / complex request / edge case")
- CONSTRAINTS reference specific guardrails (G1-G7) with domain-specific framing (not just listing "G1, G2, G5")
- EXPERT CHECK items reference domain-specific verification steps a veteran in that role would actually perform
- ANTI-PATTERNS describe concrete failure modes unique to the skill's task

**Measurement method:** For each of the 4 primers, score domain specificity on a 3-point scale:
- 3 = Specific to this skill's domain; couldn't be copy-pasted to another skill
- 2 = Partially specific; some items are generic CS patterns rather than skill-specific
- 1 = Generic; could apply to any CS skill with minimal edits

**Pass threshold:** Average score ≥ 2.5 across the 4 primers. No single primer scores 1.

**Gaming vulnerability:** A protocol could use domain keywords superficially while structurally being generic. Mitigated by checking whether the CLASSIFY types partition the skill's actual input space, not just relabel generic categories.

---

## Dimension 3: Blueprint-to-Protocol Alignment

**What it tests:** Does the reasoning protocol draw from and reflect the skill's reasoning blueprint (`references/reasoning-blueprint.md`)?

**Observable evidence:**
- CLASSIFY types correspond to the blueprint's Problem Classification Taxonomy
- ANTI-PATTERNS draw from the blueprint's Common Failure Modes
- EXPERT CHECK items reflect the blueprint's Expert Judgment Patterns
- CONSTRAINTS incorporate the blueprint's Domain Heuristics where applicable

**Measurement method:** Side-by-side comparison. For each primer, count how many items trace to a specific blueprint section vs. appear to be invented independently. Calculate alignment ratio = (blueprint-sourced items) / (total items).

**Pass threshold:** Alignment ratio ≥ 0.60 (at least 60% of protocol items traceable to blueprint content). Perfect 1.0 is not expected — the protocol should compress and adapt, not copy.

**Gaming vulnerability:** A blueprint and protocol could be written together as a pair without the blueprint actually driving the protocol design. Mitigated by checking that the blueprint contains richer content than the protocol (compression occurred) and that the protocol's items are recognizable distillations, not independent inventions.

---

## Dimension 4: Anti-Pattern Concreteness

**What it tests:** Are the anti-patterns specific, actionable failure descriptions that a practitioner could recognize in their own work?

**Observable evidence:**
- Each anti-pattern describes a specific wrong action (not just "avoid mistakes")
- Each anti-pattern implies or states the consequence of the failure
- Anti-patterns are distinguishable from each other (not overlapping restatements)
- Count: 4-6 anti-patterns present (per tier-1 spec)

**Measurement method:** Score each anti-pattern on a 3-point scale:
- 3 = Names a specific action + consequence; immediately recognizable to a practitioner
- 2 = Names a specific action but consequence is vague, or consequence is clear but trigger is vague
- 1 = Vague advisory ("be careful with data quality") that doesn't specify what to do or not do

**Pass threshold:** Average score ≥ 2.5 across all anti-patterns. Count within 4-6 range. No anti-pattern scores 1.

**Gaming vulnerability:** Anti-patterns could be highly specific but irrelevant to common failure modes. Mitigated by Dimension 3 (blueprint alignment) — anti-patterns should trace to documented failure modes.

---

## Dimension 5: Post-Execution Verification Quality

**What it tests:** Does the post-execution block include meaningful verification checks with proper confidence calibration?

**Observable evidence:**
- At least 3 verification questions present
- First question tests whether the output answers the implicit (not just explicit) need
- Data staleness verification per G7 is present
- Mode-matching check is present (output format matched to request type)
- Confidence calibration line uses the standard 3-band format: High (2+ live sources) / Medium (single-source or stale) / Low (user-provided only)
- Confidence criteria are domain-specific (not just restating the generic template)

**Measurement method:** Checklist — count of 6 elements above. Plus qualitative assessment: are the verification questions specific enough to catch real output defects for this skill?

**Pass threshold:** At least 5 of 6 elements present. Confidence criteria must be domain-adapted (not a verbatim copy of the template).

**Gaming vulnerability:** Verification questions could be present but so generic they wouldn't catch real defects. Mitigated by requiring at least one verification question that is unique to the skill's output type (e.g., "Is the root cause assignment based on the earliest signal?" for churn-analysis).

---

## Scoring Summary

| Dimension | Weight | Pass Threshold |
|-----------|--------|----------------|
| D1: Format Compliance | 15% | All 6 structural elements present |
| D2: Domain Specificity | 30% | Avg ≥ 2.5/3, no primer at 1 |
| D3: Blueprint Alignment | 20% | Alignment ratio ≥ 0.60 |
| D4: Anti-Pattern Concreteness | 20% | Avg ≥ 2.5/3, count 4-6, no item at 1 |
| D5: Post-Exec Verification | 15% | ≥ 5/6 elements, domain-adapted confidence |

**Overall pass:** All 5 dimensions pass individually. No dimension can be compensated by another — each tests a distinct quality axis.

---

## Grading Scale

| Rating | Criteria |
|--------|----------|
| **Excellent** | All 5 dimensions pass with headroom (D2 avg ≥ 2.8, D4 avg ≥ 2.8, D3 ratio ≥ 0.75) |
| **Pass** | All 5 dimensions meet threshold |
| **Marginal** | 4 of 5 dimensions pass; 1 dimension within 10% of threshold |
| **Fail** | 2+ dimensions below threshold, or any dimension far below threshold |
