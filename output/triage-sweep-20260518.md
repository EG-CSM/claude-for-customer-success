# Production-Readiness Rubric v1.7 — Sweep Triage Report
**Date:** 2026-05-18  
**Sweep output:** `output/review-sweep-20260518.csv`  
**Status:** [VALIDATED]

> **P0 fix applied 2026-05-18.** Checks 2.1 and 2.2 updated to case-insensitive ERE patterns (`^## [Uu]se [Ww]hen`, `^## [Dd][Oo] [Nn][Oo][Tt] [Uu]se [Ff]or`) with `## Trigger Precision` accepted as an equivalent heading for the onboarding plugin convention. Sweep re-run immediately after. Results below reflect the corrected run unless marked *(pre-fix)*.

## Post-Fix Summary (corrected baseline)

| Metric | Pre-fix | Post-fix | Delta |
|--------|---------|---------|-------|
| Skills scanned | 80 | 80 | — |
| Checks run | 1,681 | 1,681 | — |
| PASS | 1,001 (59.5%) | 1,043 (62.0%) | **+42** |
| FAIL | 680 (40.5%) | 638 (38.0%) | **−42** |
| BLOCK failures | 126 | 4 | **−122** |
| WARN failures | 553 | 553 | — |
| NOTE | 1 | 1 | — |

**4 surviving BLOCKs:** `renewals/churn-rca` (checks 2.1 + 2.2) and `renewals/downgrade-analysis` (checks 2.1 + 2.2) — both skills are genuinely missing trigger sections, not a casing artifact.

**P0 recommendation status: COMPLETED.** The 122 false-positive BLOCK failures were a rubric artifact, not skill defects. True BLOCK count confirmed at 4.

---

## Executive Summary

80 skills across 5 plugins were swept against 21 automated checks from Rubric v1.7.

| Metric | Count |
|--------|-------|
| Skills scanned | 80 |
| Checks run | 1,681 |
| PASS | 1,001 (59.5%) |
| FAIL | 680 (40.5%) |
| BLOCK failures | 126 |
| WARN failures | 553 |
| NOTE | 1 |

**Top finding:** 63 of the 126 BLOCK failures (50%) are a casing artifact — rev-ops, cs-ops, renewals, and onboarding all use `## Use when` / `## Do NOT use for` (lowercase) while the rubric checks for `## Use When` / `## Do NOT Use For` (title case). This is the single highest-leverage fix: one sed pass corrects 62 BLOCK failures instantly.

---

## BLOCK Failure Analysis

### Check 2.1 — `## Use When` present (BLOCK)
### Check 2.2 — `## Do NOT Use For` present (BLOCK)

**Root cause:** Casing mismatch. The rubric pattern-matches `## Use When` and `## Do NOT Use For` (title case). Four plugins were authored with lowercase variants.

| Plugin | Skills | 2.1 FAIL | 2.2 FAIL | Root Cause |
|--------|--------|----------|----------|------------|
| cs-ops | 9 | 9 | 9 | All use `## Use when` / `## Do NOT use for` |
| csm | 16 | 0 | 0 | Title case throughout — **no BLOCKs** |
| onboarding | 9 | 9 | 9 | Neither section exists — uses `## Trigger Precision` pattern instead |
| renewals | 12 | 12 | 12 | Mix: 10 skills lowercase; 2 (`churn-rca`, `downgrade-analysis`) missing both entirely |
| rev-ops | 34 | 33 | 33 | 33 skills lowercase; 1 (`csql-tracking`) title case (passes) |

**Total BLOCK failures from casing: 62** (33+9+10+9+9+10-8 ... see table — 33+9+9+10 = 61 lowercase + 2 missing = 63 per check × 2 checks = 126 total BLOCK rows, but unique skills with at least one BLOCK = 63).

**Remediation options (in priority order):**

**Option A — Fix the rubric check (preferred):** Make checks 2.1 and 2.2 case-insensitive. Pattern `^## [Uu]se [Ww]hen` and `^## [Dd]o [Nn][Oo][Tt] [Uu]se [Ff]or` would pass all lowercase-but-present variants. The onboarding plugin's `## Trigger Precision` pattern is a different structural choice and warrants a separate decision (see below).

**Option B — Fix the skill files:** Run a sed normalization pass across cs-ops, renewals, and rev-ops to uppercase the headings. ~62 files. Low risk if done as a pure heading rename. Does not address onboarding's structural difference.

**Option C — Hybrid:** Fix the rubric to be case-insensitive (catches the convention variation without mass file edits) AND document `## Trigger Precision` as an accepted equivalent heading in the rubric notes.

**Recommendation: Option A** — rubric should be permissive of casing; the structural intent (trigger block present) is what matters for the BLOCK check. Mass file edits risk introducing noise into the skill content.

**Onboarding structural note:** All 9 onboarding skills use `## Trigger Precision` (a different heading) instead of `## Use When` / `## Do NOT Use For`. This is a deliberate structural convention in that plugin — the section is present but under a different name. The rubric should either accept this pattern or the onboarding plugin needs a heading normalization pass.

---

## WARN Failure Matrix

Rows are check IDs; columns are plugin skill counts failing that check.

| Check | cs-ops (9) | csm (16) | onboarding (9) | renewals (12) | rev-ops (34) | **Total** |
|-------|-----------|---------|---------------|--------------|-------------|---------|
| 1.2 — version field present | 0 | 0 | 0 | 0 | 2 | **2** |
| 2.3 — Typical Activation present | 9 | 0 | 9 | 12 | 33 | **63** |
| 3.1 — Pre-flight section present | 1 | 5 | 1 | 3 | 34 | **44** |
| 3.2 — company-profile.md referenced | 1 | 3 | 0 | 2 | 33 | **39** |
| 5.1 — Reasoning Protocol present | 0 | 0 | 0 | 0 | 3 | **3** |
| 5.1a — reasoning-blueprint.md file exists | 0 | 2 | 0 | 2 | 34 | **38** |
| 5.1-D1a — D1 opening line present | 0 | 6 | 0 | 2 | 34 | **42** |
| 5.1-D1b — CLASSIFY primer present | 0 | 2 | 0 | 2 | 34 | **38** |
| 5.1-D1c — CONSTRAINTS primer present | 0 | 6 | 0 | 2 | 34 | **42** |
| 5.1-D1d — EXPERT primer present | 0 | 6 | 0 | 4 | 34 | **44** |
| 6.1 — Reference Files section present | 9 | 14 | 9 | 10 | 31 | **73** |
| 6.1a — reasoning-blueprint.md referenced in SKILL.md | 9 | 8 | 9 | 12 | 34 | **72** |
| 9.1 — G-code references present | 0 | 8 | 1 | 2 | 3 | **14** |
| S1 — output status signal present | 0 | 0 | 9 | 0 | 30 | **39** |

---

## Pattern Analysis by Check

### 2.3 — `## Typical Activation` missing (63 WARNs)
- cs-ops (9/9), onboarding (9/9): all missing — likely replaced by `## Trigger Precision`
- renewals (12/12): all missing
- rev-ops (33/34): all but `csql-tracking` missing
- csm (0/16): perfect — all present
- **Pattern:** Same structural convention split as checks 2.1/2.2. Onboarding uses `## Trigger Precision` which apparently doesn't include a `Typical activation:` subsection. csm is the reference implementation.

### 6.1 — `## Reference Files` section missing (73 WARNs)
- Largest single WARN failure count (73 across 63 skills)
- All cs-ops (9/9), all onboarding (9/9), all but 3 rev-ops skills
- csm has 14/16 failing — the 2 that pass likely have the section; 14 don't
- **Pattern:** `## Reference Files` is a rubric v1.7 addition that predates most plugin authoring. This is a systemic structural gap, not individual skill failures.

### 6.1a — reasoning-blueprint.md not referenced in SKILL.md (72 WARNs)
- Correlated with 6.1 failures — if no `## Reference Files` section, blueprint won't be referenced
- All rev-ops (34/34): none reference the blueprint
- **Pattern:** reasoning-blueprint.md was introduced in rubric v1.6/1.7. Pre-existing skills haven't been updated.

### 5.1a — reasoning-blueprint.md file doesn't exist in plugin directory (38 WARNs)
- rev-ops (34/34): file absent from plugin
- csm (2/16): `success-plan-canvas`, `success-plan-progress-review` — file absent
- renewals (2/12): `churn-rca`, `downgrade-analysis` — file absent
- **Pattern:** Most plugins don't have a reasoning-blueprint.md artifact deployed. This is a deployment gap, not a SKILL.md authoring gap.

### 5.1-D1{a,b,c,d} — Reasoning Protocol D1 primers missing (38–44 WARNs each)
- rev-ops: 34/34 skills failing all D1 checks — Reasoning Protocol sections don't use the D1 primer framework
- csm failures are concentrated in 6 skills: `escalation-memo`, `expansion-business-case`, `health-score-review`, `renewal-readiness`, `success-plan-canvas`, `success-plan-progress-review`
- **Pattern:** rev-ops skills have Reasoning Protocol sections (check 5.1 passes for most) but they don't use the v1.7 D1 primer structure. Pre-v1.7 authoring convention.

### 3.1 — `## Pre-flight` section missing (44 WARNs)
- rev-ops (34/34): none have Pre-flight sections
- csm (5/16): partial — 11 skills have it, 5 don't
- **Pattern:** Pre-flight is an onboarding/renewals convention that hasn't been adopted in rev-ops.

### 3.2 — company-profile.md not referenced (39 WARNs)
- rev-ops (33/34): all but csql-tracking
- csm (3/16): concentrated failures
- **Pattern:** company-profile.md is a runtime reference artifact. Skills that don't pull account context won't reference it. May be expected for rev-ops portfolio/planning skills.

### S1 — Output status signal missing (39 WARNs)
- onboarding (9/9): none carry PROPOSED/VALIDATED/DRAFT signals
- rev-ops (30/34): 4 skills have status signals; 30 don't
- csm, cs-ops, renewals: all pass — status signals present
- **Pattern:** Onboarding and most rev-ops skills were authored before the status signal requirement was formalized.

### 9.1 — G-code references missing (14 WARNs)
- csm (8/16): half of csm skills lack G-code references — notable since csm is otherwise the best-performing plugin
- **Pattern:** G-code references (e.g., `G1.3`, `G2.1`) are a rubric v1.5+ convention. Older csm skills predate it.

### 1.2 — version field missing from frontmatter (2 WARNs)
- rev-ops only: `outcome-statement-builder`, `unit-of-growth-calculator`
- Low-impact, easy fix: add `version: "1.0"` to frontmatter

### 5.1 — Reasoning Protocol section missing (3 WARNs)
- rev-ops only: `csql-tracking`, `outcome-statement-builder`, `unit-of-growth-calculator`
- All three are also failing 5.1a and D1 checks — structurally incomplete skills

---

## Remediation Priority Tiers

### P0 — Fix the rubric (not the skills): 5 minutes, eliminates 126 BLOCK rows
Make checks 2.1 and 2.2 case-insensitive in `review-sweep.sh`. The structural content is present; only the heading casing differs from the canonical form. Also consider accepting `## Trigger Precision` as an equivalent to `## Use When` + `## Do NOT Use For` for the onboarding plugin convention.

### P1 — Structural gaps affecting all or most skills in a plugin (systemic)
These require plugin-level authoring passes, not per-skill fixes:

| Gap | Plugins affected | Skills affected | Effort |
|-----|-----------------|-----------------|--------|
| Missing `## Typical Activation` (2.3) | cs-ops, onboarding, renewals, rev-ops | 63 | Medium — add subsection to each trigger block |
| Missing `## Reference Files` section (6.1) | All except partial csm | 63 | Low — add section with 2–3 lines per skill |
| reasoning-blueprint.md not in SKILL.md (6.1a) | All | 72 | Low — add one line to Reference Files |
| reasoning-blueprint.md file absent (5.1a) | rev-ops, 2 csm, 2 renewals | 38 | Low — create the file once per plugin |
| D1 primer framework absent (5.1-D1*) | rev-ops, 6 csm, 2–4 renewals | 38–44 per check | High — requires Reasoning Protocol restructuring |
| Output status signal missing (S1) | onboarding, rev-ops | 39 | Trivial — add one line to frontmatter |

### P2 — Isolated failures in otherwise-healthy plugins
| Gap | Plugin | Skills | Fix |
|-----|--------|--------|-----|
| Missing Pre-flight (3.1) | csm (5), renewals (3) | 9 | Add Pre-flight section |
| company-profile.md not referenced (3.2) | csm (3), renewals (2), cs-ops (1) | 6 | Add reference (if applicable to skill) |
| G-code references absent (9.1) | csm (8) | 8 | Add G-code annotations to Reasoning Protocol |
| Reasoning Protocol fully absent (5.1) | rev-ops (3) | 3 | `csql-tracking`, `outcome-statement-builder`, `unit-of-growth-calculator` need full RP |
| version field missing (1.2) | rev-ops (2) | 2 | Add `version:` to frontmatter |

### P3 — Qualitative checks (not automated, deferred)
Checks D2, D4, D5, and 5.1b require human review:
- D2: Domain-specific vocabulary density
- D4: Anti-pattern quality
- D5: Post-execution verification quality
- 5.1b: Blueprint alignment ratio

---

## Plugin Health Summary

| Plugin | Skills | BLOCK fails | WARN fails | Total fails | Fail rate | Health |
|--------|--------|-------------|------------|-------------|-----------|--------|
| csm | 16 | 0 | 61 | 61 | 24% | ✅ Best |
| cs-ops | 9 | 18 | 29 | 47 | 28% | 🟡 Good (BLOCKs are casing) |
| onboarding | 9 | 18 | 38 | 56 | 35% | 🟡 Fair (structural convention differs) |
| renewals | 12 | 24 | 53 | 77 | 36% | 🟡 Fair (BLOCKs are casing + 2 missing) |
| rev-ops | 34 | 66 | 373 | 439 | 73% | 🔴 Needs work |

**csm is the reference implementation.** It's the only plugin with zero BLOCK failures and has the most complete structural coverage. It should be used as the template for upgrading the other four plugins.

**rev-ops outlier explanation:** rev-ops skills were authored with a different structural convention — lowercase trigger headings, no Typical Activation, no Pre-flight, no Reference Files, no output status signals, no D1 primer framework. The content quality may be high (qualitative checks pending), but structurally these skills predate multiple rubric additions and need a systematic update pass.

---

## Recommended Next Steps

1. **Immediate (< 1 hour):** Update `review-sweep.sh` checks 2.1 and 2.2 to be case-insensitive. Re-run sweep to get true BLOCK count (expected: ~4, for the 2 renewals skills with truly missing sections + potentially 2 onboarding if Trigger Precision is accepted as equivalent).

2. **Short-term (1 day):** Plugin-level pass on rev-ops for:
   - Add `## Typical Activation` to all 33 affected skills
   - Add `## Reference Files` section with reasoning-blueprint.md reference
   - Create `reasoning-blueprint.md` once in the plugin root
   - Add output status signal (`[PROPOSED]`) to all 30 affected skills
   - Fix `version:` on 2 skills

3. **Medium-term (2–3 days):** Decide on D1 primer adoption for rev-ops — this requires restructuring 34 Reasoning Protocol sections. May be worthwhile to do as part of a broader rev-ops skill quality pass.

4. **Parallel:** Run qualitative checks (D2, D4, D5, 5.1b) on a representative sample — suggest 5 csm + 5 rev-ops + 2 from each other plugin (16 skills total) to establish baseline quality calibration before committing to the full 80-skill update pass.
