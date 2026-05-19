# Wave 2 Remediation — Completion Report

**Status:** [VALIDATED]  
**Date:** 2026-05-19  
**Sweep result:** 1701/1701 PASS — 0 FAIL  
**Baseline (Wave 1):** 1701/1701 PASS  
**Delta:** No regression introduced

---

## Summary

Wave 2 addressed the remaining 8 BLOCK findings (B-05 through B-12) from the red team synthesis report. All findings are resolved. The Production-Readiness Rubric v1.7 sweep confirms 81 skills × 21 checks = 1701 checks, all passing.

---

## BLOCK-by-BLOCK Resolution

### B-05 — Bare Filenames in Load-on-Demand Instructions
**File:** `renewals/skills/churn-rca/SKILL.md`  
**Finding:** 3 bare filenames without directory prefix in load-on-demand instruction block  
**Fix:** Prefixed all three with `reference/`:
- `churn-rca-taxonomy.md` → `reference/churn-rca-taxonomy.md`
- `cohort-analysis-framework.md` → `reference/cohort-analysis-framework.md`
- `remediation-playbook.md` → `reference/remediation-playbook.md`

---

### B-06 — Config File Misclassified as Reference
**File:** `renewals/skills/downgrade-analysis/SKILL.md`  
**Finding:** `company-profile.md` listed in Reference Files table; it is a runtime config dependency, not a reference  
**Fix:** Removed row from Reference Files table; added parenthetical in Pre-flight: "(company-profile.md is a runtime config dependency, not a reference file)"

---

### B-07 — Absolute Repo-Root Paths in Reference Table
**File:** `rev-ops/skills/csql-tracking/SKILL.md` [VALIDATED — status preserved]  
**Finding:** 4 Reference Files table entries used full repo-root-relative paths  
**Fix:** Normalized to skill-relative paths:
- `rev-ops/skills/csql-tracking/reference/csql-record-schema.md` → `reference/csql-record-schema.md`
- `rev-ops/skills/csql-tracking/reference/csql-status-transitions.md` → `reference/csql-status-transitions.md`
- `rev-ops/skills/csql-tracking/reference/query-filter-patterns.md` → `reference/query-filter-patterns.md`
- `rev-ops/skills/csql-tracking/references/reasoning-blueprint.md` → `references/reasoning-blueprint.md`

**Note:** [VALIDATED] status signal preserved. Cross-skill reference to `csm/skills/expansion-business-case/reference/csql-package-template.md` was left untouched (outside B-07 scope).

---

### B-08 — Missing injection-defense.md + reference/ vs references/ Standardization
**Files affected:** 6 skills across csm, renewals, rev-ops, onboarding  
**Finding (part 1):** `injection-defense.md` absent from `csm/skills/expansion-business-case/reference/`  
**Fix:** Created `csm/skills/expansion-business-case/reference/injection-defense.md` with full canonical prompt injection defense implementation including: threat model, 4-layer defense specification (input classification, keyword scan protocol, output isolation, cross-skill routing integrity), implementation checklist.

Reference row added to `expansion-business-case/SKILL.md` Reference Files table: `reference/injection-defense.md | Prompt injection defense implementation | Load when processing user-supplied free-text fields`

**Finding (part 2):** 5 of 6 skills had `references/reasoning-blueprint.md` in SKILL.md entries when the actual directory is `reference/` (no trailing 's')  
**Fix:** Corrected in all 5 affected skills:
- `csm/skills/expansion-business-case/SKILL.md` — 4 occurrences fixed
- `csm/skills/expansion-onboarding/SKILL.md` — 2 occurrences fixed (note: actual path is `csm/skills/expansion-onboarding/`, not `onboarding/skills/expansion-onboarding/`)
- `csm/skills/success-plan-canvas/SKILL.md` — 2 occurrences fixed
- `renewals/skills/churn-rca/SKILL.md` — 1 occurrence fixed
- `renewals/skills/downgrade-analysis/SKILL.md` — 1 occurrence fixed

**No mismatch:** `rev-ops/skills/outcome-statement-builder/` uses `references/` on disk; path entries are correct

**VALIDATED status:** `csm/skills/expansion-onboarding/SKILL.md` line 19 confirmed [VALIDATED] — not downgraded.

---

### B-09 — Trigger Collision: success-plan-builder vs success-plan-canvas
**Files:** `csm/skills/success-plan-builder/SKILL.md`, `csm/skills/success-plan-canvas/SKILL.md`  
**Finding:** Both skills activated on identical inputs; no discriminator prevented collision  
**Fix:** OCV (Outcome-to-Customer Value) system as the routing discriminator:
- `success-plan-builder` Use When: first bullet extended with "without requiring the OCV canvas structure"; new bullet added for orgs not using OCV system
- `success-plan-canvas` Use When: new prepended bullet requiring OCV system explicitly; fallback route to `success-plan-builder` stated
- Both Typical Activation blocks annotated with OCV context markers

---

### B-10 — cs-ops Skills Missing Security Body Sections
**Files:** All 9 `cs-ops/skills/*/SKILL.md`  
**Finding:** No `## Security & Permissions` or `## Trust & Verification` sections in any cs-ops skill  
**Fix:** Added both sections to all 9 skills  

**CRITICAL deployment constraint honored:** All cs-ops skills are `deployment_target: plugin`. Security contract placed in body sections ONLY — no `security:` block added to frontmatter. Confirmed: zero frontmatter `security:` blocks introduced.

**Template applied:**

| Skill | Template | Rationale |
|-------|----------|-----------|
| customize | config-write | Writes to config file path; carries sanitization contract + path sanitization clause |
| cold-start-interview | config-write | Writes to config file path; same as customize |
| process-doc | standard (read-only) | Analysis/reporting; no writes |
| capacity-planner | standard (read-only) | Analysis/reporting; no writes |
| data-quality-check | standard (read-only) | Analysis/reporting; no writes |
| health-model-review | standard (read-only) | Analysis/reporting; no writes |
| metric-dashboard | standard (read-only) | Analysis/reporting; no writes |
| playbook-auditor | standard (read-only) | Analysis/reporting; no writes |
| segment-analyzer | standard (read-only) | Analysis/reporting; no writes |

---

### B-11 — Config Poisoning Vector in cold-start-interview
**File:** `csm/skills/cold-start-interview/SKILL.md`  
**Finding:** User-supplied free-text written to config without sanitization contract  
**Fix:** Appended to existing `## Trust & Verification` section: display-string-only handling for user-supplied free-text; `[review]` marker protocol for strings containing instruction-like keywords (ignore, override, system prompt, route to)

---

### B-12 — Stray `---` Separator Accumulation
**Finding description:** 6–37 stacked separator lines per skill across all 83 skills  
**Audit result:** No stacked consecutive `---` lines found in any of the 81 SKILL.md files. Files contain 6–37 `---` horizontal rules (min=6, max=37, median=17), all separated by meaningful content. No two `---` lines appear within a blank-line window of each other. Finding not applicable in current file state.

---

## VALIDATED Skills — Status Preserved

Both [VALIDATED] skills that were in scope for Wave 2 edits retain their status:

| Skill | Status | Edits made |
|-------|--------|------------|
| `rev-ops/skills/csql-tracking/SKILL.md` | [VALIDATED] ✓ | B-07 path normalization |
| `csm/skills/expansion-onboarding/SKILL.md` | [VALIDATED] ✓ | B-08 reasoning-blueprint path fix |

---

## Wave-Level Summary

| Wave | BLOCKs addressed | Sweep result |
|------|-----------------|--------------|
| Wave 1 | B-01–B-04, NEW-1–NEW-3 | 1701/1701 PASS |
| Wave 2 | B-05–B-12 | 1701/1701 PASS |
| **Combined** | **All 15 original BLOCK findings** | **1701/1701 PASS** |

**Production-Readiness Rubric v1.7:** 81 skills × 21 checks = 1701 check runs. Zero failures across both waves.

---

## Sweep Artifact

Output CSV: `output/review-sweep-20260519.csv`  
Command: `bash scripts/review-sweep.sh`  
Run from: `claude-for-customer-success/` project root
