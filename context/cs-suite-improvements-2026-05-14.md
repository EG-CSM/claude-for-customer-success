# CS Suite Skill Improvement — Session Context
**Project:** claude-for-customer-success  
**Date:** 2026-05-14  
**Status:** COMPLETED — all 11 tasks from improvement recommendations delivered  
**Session path:** agent-skill-builder / claude-for-customer-success

---

## Current State

All 11 tasks from `cs-suite-skill-improvement-recommendations.md` are **complete**. The repository is in full compliance with CS_SKILL_MD_TEMPLATE_SPECIFICATION v5.3 requirements for the four CS Suite plugins (csm, renewals, onboarding, cs-ops).

An additional unplanned improvement (`add-output-sections.py`) was also written and run, adding `## Output` sections to all skill bodies — this extends beyond the original 11-task scope.

---

## Completed Artifacts

### SKILL.md improvements (41 files across 4 plugins)
| Plugin | Skills | Skills Modified |
|--------|--------|-----------------|
| csm | 13 | 13 |
| renewals | 10 | 10 |
| onboarding | 9 | 9 |
| cs-ops | 9 | 9 |

**Sections added to all 41 SKILL.md files:**
- `## Reasoning Protocol` — 6-step structure per v5.3; guardrail subsets from G1–G7 per skill
- `## Output` — output format declarations (via add-output-sections.py)

**Config skills (NO_GUARDRAILS):** 8 files — `cold-start-interview` and `customize` in each of the 4 plugins. These receive environment-configuration language instead of domain guardrails G1–G7.

### Eval fixtures (41 files)
Location: `[plugin]/evals/fixtures/[skill-name]-eval.md`  
Structure per file: 5 TP tests, 5 TN tests, 3 edge cases, 3 injection tests, eval results log  
Threshold declared: TPR ≥ 0.80, TNR ≥ 0.80

### Scripts (7 files in `scripts/`)
| Script | Purpose | Status |
|--------|---------|--------|
| `add_reasoning_protocol.py` | Inserts `## Reasoning Protocol` into SKILL.md files | Run — idempotent; 41 skipped (all already present) |
| `add-output-sections.py` | Inserts `## Output` sections | Run — all 41 confirmed present |
| `lint-skill-body.py` | B01–B10 body linter (532 lines) | Functional; tested on renewals/renewal-forecast → PASS |
| `generate-eval-fixtures.py` | Generates eval fixture markdown (271 lines) | Syntax OK; dry-run confirmed 41/41 fixtures present |
| `validate-cross-links.py` | Validates cross-skill reference format (430 lines) | Run — 146 checks, 0 FAIL, 0 WARN (after fix-prose-paths.py) |
| `check-config-completeness.py` | Config completeness audit (387 lines) | Run — NOT INSTALLED expected (pre-package state) |
| `fix-reasoning-protocol-step1.py` | Corrects Step 1 "Use when" reference in all SKILL.md files | Run — 41 updated, idempotent (0 updates on re-run) |

---

## Key Decisions

### GUARDRAIL_MAP (canonical)
Full mapping of all 41 skills to their G1–G7 guardrail subsets. Eight config skills mapped to `NO_GUARDRAILS`. Reference: `add_reasoning_protocol.py` contains the authoritative GUARDRAIL_MAP — check that file for the complete mapping rather than reconstructing from memory.

### Deployment target
All plugins: `deployment_target: plugin` — no `security:` block in frontmatter (plugin loader rejects it). Security contract lives in `## Security & Permissions` + `## Trust & Verification` body sections.

### Insertion strategy
`add_reasoning_protocol.py` uses regex `r'(## Pre-flight\b.*?\n)(## )'` with `re.DOTALL` to insert `## Reasoning Protocol` after the Pre-flight block and before the next `##`-level section. Idempotent: skips any file already containing `## Reasoning Protocol`.

### Linter BLOCK checks
B02 (Reasoning Protocol presence), B03 (Pre-flight presence), B10 (no security block in plugin frontmatter). These are non-negotiable; any skill failing B02 or B03 is non-compliant.

---

## Spot-Check Results

| Skill | Guardrails Confirmed | Status |
|-------|---------------------|--------|
| csm/health-score-review | G1, G4, G5, G7 | ✅ PASS |
| renewals/renewal-forecast | G2, G3, G4, G7 | ✅ PASS |
| csm/cold-start-interview | NO_GUARDRAILS | ✅ PASS |
| renewals/renewal-forecast (lint) | 0 BLOCK, 0 WARN | ✅ PASS |
| csm/risk-flag (## Output) | count=1 | ✅ PASS |
| renewals/renewal-forecast (## Output) | count=1 | ✅ PASS |
| cs-ops/metric-dashboard (## Output) | count=1 | ✅ PASS |

---

## Open Questions

1. **`add-output-sections.py` provenance** — this script was not in the original 11-task plan. It was found in `scripts/` alongside the planned scripts. Unclear whether it was part of a broader improvement pass or added opportunistically. Worth confirming with Todd whether the `## Output` section content is complete and correct across all 41 files (a full run of the linter against all skills would surface any `## Output` format issues if B08 is active).

2. **Scripts 10–11 untested end-to-end** — `generate-eval-fixtures.py` passed syntax check but was not executed against the live repository. `validate-cross-links.py` and `check-config-completeness.py` have both been fully run and validated (see session 2/3 log). `generate-eval-fixtures.py` is ready to run when needed.

3. **Full lint sweep not run** — `lint-skill-body.py` was tested on one skill only (renewals/renewal-forecast). A full sweep across all 41 skills has not been run. Recommended next step if clean bill of health is needed before production use.

---

## Next Steps

1. **Run full lint sweep (recommended before production):**
   ```bash
   cd /sessions/[session]/mnt/claude-for-customer-success
   python3 scripts/lint-skill-body.py --plugin csm
   python3 scripts/lint-skill-body.py --plugin renewals
   python3 scripts/lint-skill-body.py --plugin onboarding
   python3 scripts/lint-skill-body.py --plugin cs-ops
   ```

2. **Run validate-cross-links.py** to confirm all cross-skill references use `/plugin:skill-name` format.

3. **Run check-config-completeness.py** to verify all 8 config skills have required fields.

4. **Package plugins** — when ready to deploy, use `build-plugin.sh` from the agent-skill-builder workspace (not raw `zip -r`). That script validates frontmatter, zips, re-extracts, and re-validates before install.

5. **Confirm `## Output` coverage** — if any doubt about add-output-sections.py completeness, grep for `## Output` count across all 41 SKILL.md files:
   ```bash
   grep -l "^## Output" */skills/*/SKILL.md | wc -l
   # Expected: 41
   ```

---

## Patterns Learned

- **Script idempotency is load-bearing** — the reasoning protocol script running twice (once in the prior session before compaction, once in the recovery verification) caused 0 data corruption because the idempotent check was built in. Always build idempotent insertion scripts for batch SKILL.md modification.

- **Continuation context as safety backup** — embedding the full script in the continuation context document (not just the GUARDRAIL_MAP) was the correct call. The outputs directory clears between sessions; the workspace-mounted project folder persists. Future multi-session scripts should be saved to the project folder, not the outputs directory.

- **Session name changes between compaction cycles** — the bash mount path prefix (`/sessions/[session-name]/mnt/`) changes when a new session is started after compaction. Any script with a hardcoded BASE path must be verified and corrected at session start.

---

## Active Session Log

| Session | Key Actions |
|---------|-------------|
| 2026-05-13 (prior) | Tasks 1–5 executed; Task 6 run (33 modified, 8 skipped confirmed); Tasks 7–11 artifacts written; compaction before logging |
| 2026-05-14 (session 1) | Recovered from compaction; confirmed Task 6 already done (41 skipped); spot-checked 6 skills + linter; updated task list; wrote this context |
| 2026-05-14 (session 2) | Full lint sweep: 41/41 PASS, 0 BLOCK, 0 WARN across all 4 plugins. Cross-link validation: 0 FAIL, 25 WARN (all intentional root-relative refs in docs/cookbooks — targets exist). Config completeness: NOT INSTALLED (expected, plugins not yet packaged) — 0 placeholder fields, 0 blocked skills. Fixed stale `build-plugin.sh` reference in this context file. |
| 2026-05-14 (session 3) | Converted all 25 WARN prose paths to explicit document-relative paths. Wrote scripts/fix-prose-paths.py (idempotent, 30 replacements across 18 files). Re-ran validate-cross-links.py: 146 checks, 0 FAIL, 0 WARN. Repository is now fully clean across all validation scripts. |
