# Reasoning Protocol Remediation — Evaluation Report

**Date:** 2026-05-15
**Rubric Version:** 1.0
**Sample Size:** 10 skills (2-3 per agent)
**Status:** [VALIDATED]

---

## Overall Results

| Rating | Count | Skills |
|--------|-------|--------|
| Excellent | 7 | stakeholder-map, kickoff-prep, success-criteria, churn-analysis, negotiation-prep, expansion-signal, health-model-review |
| Pass | 3 | risk-flag, qbr-builder, blocker-review |
| Marginal | 0 | — |
| Fail | 0 | — |

**70% Excellent / 30% Pass / 0% Fail.** The remediation effort produced consistently high-quality reasoning protocols. No skill scored Marginal or Fail — every protocol meets the minimum quality bar, and most exceed it.

---

## Per-Dimension Analysis

| Dimension | Weight | Pass Rate | Pattern |
|-----------|--------|-----------|---------|
| D1: Format Compliance | 15% | 8/10 (80%) | Two CSM skills share identical structural defect |
| D2: Domain Specificity | 30% | 10/10 (100%) | Universal 3.0/3.0 — strongest dimension |
| D3: Blueprint Alignment | 20% | 10/10 (100%) | Range 0.79–0.95; well above 0.60 threshold |
| D4: Anti-Pattern Concreteness | 20% | 10/10 (100%) | Range 2.67–3.0; all above 2.5 threshold |
| D5: Post-Exec Verification | 15% | 7/10 (70%) | G7 staleness check is the most commonly missing element |

### D2: Domain Specificity — Perfect Score

Every protocol scored 3.0/3.0 across all four primers (CLASSIFY, CONSTRAINTS, EXPERT CHECK, ANTI-PATTERNS). The reasoning blueprints drove genuine domain adaptation — no protocol could be copy-pasted to another skill. This validates the two-step remediation approach: blueprint first, then protocol derived from blueprint.

### D3: Blueprint Alignment — Strong

Alignment ratios ranged from 0.79 (blocker-review) to 0.95 (churn-analysis). The blueprint-to-protocol traceability confirms that protocols are distillations of their blueprints rather than independent inventions. Even the lowest ratio (0.79) is well above the 0.60 threshold.

### D4: Anti-Pattern Concreteness — Solid

Two skills scored slightly below 3.0 (negotiation-prep at 2.67, risk-flag and qbr-builder at 2.8) but all passed. The lower-scoring anti-patterns had clear triggers but slightly vague consequences — worth noting but not blocking.

### D1: Format Compliance — Two Failures

Both failures share the same root cause — the subagent that remediated risk-flag and qbr-builder used bold labels instead of numbered primers and omitted the canonical opening line.

**Missing in both:**
- `Before generating output, apply these primers:` opening line
- Numbered primer format (used `**CLASSIFY**:` instead of `1. **CLASSIFY**:`)

### D5: Post-Execution Verification — Three Failures

The most common gap is the G7 staleness check. Four skills rated Excellent also had this as their single missing element but still passed (5/6 threshold).

| Skill | Missing Elements |
|-------|-----------------|
| risk-flag | G7 staleness check, mode-matching check, 3-band confidence format |
| qbr-builder | Implicit-need question, G7 staleness check, 3-band confidence format |
| blocker-review | G7 staleness check, mode-matching check |

---

## Skills Needing Remediation

Three skills need targeted fixes to reach Excellent. All fixes are mechanical — add specific missing structural elements without changing the domain content.

### 1. `csm/skills/risk-flag/SKILL.md`

**Current rating:** Pass
**Target:** Excellent

Fixes:
- **D1:** Add opening line `Before generating output, apply these primers:` and convert bold labels to numbered format (`1. **CLASSIFY**:`, `2. **CONSTRAINTS**:`, etc.)
- **D5:** Add G7 staleness check to post-execution verification, add mode-matching check, add 3-band confidence calibration line

### 2. `csm/skills/qbr-builder/SKILL.md`

**Current rating:** Pass
**Target:** Excellent

Fixes:
- **D1:** Add opening line `Before generating output, apply these primers:` and convert bold labels to numbered format
- **D5:** Add implicit-need question as first verification check, add G7 staleness check, add 3-band confidence calibration line

### 3. `onboarding/skills/blocker-review/SKILL.md`

**Current rating:** Pass
**Target:** Excellent

Fixes:
- **D5:** Add G7 staleness check to post-execution verification, add mode-matching check

---

## Systemic Observations

The G7 staleness check appeared as a gap in 7 of 10 skills (missing in 3 failures + noted as the single absent element in 4 Excellent-rated skills). The remaining 31 un-sampled skills likely share this pattern. A targeted sweep for G7 staleness check presence across all 41 skills would be low-effort and high-value.

The D1 format defect in risk-flag and qbr-builder suggests those two skills were processed by the same subagent in Batch 1, which interpreted the format slightly differently. The fix is trivial, but a grep across all 41 for the canonical opening line would confirm no other skills share this defect.

---

## Conclusion

The remediation effort succeeded. Domain specificity — the hardest dimension to get right and the one with the highest weight (30%) — scored perfectly across all 10 samples. The blueprint-first approach produced protocols that are genuinely tailored to each skill's problem space rather than generic CS boilerplate.

The three Pass-rated skills need only structural fixes (formatting and missing verification elements). No skill requires content rework. Estimated effort to bring all three to Excellent: under 15 minutes of mechanical edits.
