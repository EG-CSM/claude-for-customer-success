# CSM Plugin — PROPOSED → VALIDATED Promotion Tracker

**Finding:** N-15 from redteam synthesis report  
**Created:** 2026-05-19  
**Status:** [REQUIRES FOLLOW-UP]

---

## Purpose

15 of 16 csm skills currently carry `[PROPOSED]` status. Before the csm plugin
is marked production-ready at the ecosystem level, each PROPOSED skill must pass
a validation gate and be promoted to `[VALIDATED]`.

## Validation Gate Criteria

A skill is promoted from PROPOSED to VALIDATED when ALL of the following are met:

1. **Trigger precision test** — TP activation confirmed, TN exclusion confirmed, edge cases documented
2. **Output correctness** — at least 2 representative scenarios produce expected output structure
3. **G-code compliance** — all referenced G-codes (G1–G9) behave correctly when config is loaded
4. **Connector error handling** — rate-limit vs unavailability distinction tested (N-14 fix)
5. **Pre-flight dependency** — config load failure halts execution, does not produce partial output

## Current Status

| Skill | Status | Validated Date | Validator |
|-------|--------|----------------|-----------|
| account-research | PROPOSED | — | — |
| call-prep | PROPOSED | — | — |
| cold-start-interview | PROPOSED | — | — |
| customize | PROPOSED | — | — |
| escalation-memo | PROPOSED | — | — |
| expansion-business-case | PROPOSED | — | — |
| expansion-onboarding | **VALIDATED** | prior | — |
| health-score-review | PROPOSED | — | — |
| qbr-builder | PROPOSED | — | — |
| renewal-readiness | PROPOSED | — | — |
| risk-flag | PROPOSED | — | — |
| stakeholder-map | PROPOSED | — | — |
| success-plan-builder | PROPOSED | — | — |
| success-plan-canvas | PROPOSED | — | — |
| success-plan-progress-review | PROPOSED | — | — |
| taro-play-runner | PROPOSED | — | — |
| value-statement | PROPOSED | — | — |

## Process

1. Pick a skill from the table above
2. Run it through the 5-point validation gate criteria
3. If it passes, update the status to `[VALIDATED]` in the SKILL.md frontmatter and this tracker
4. If it fails, document the failure and fix before re-running
5. Ecosystem production-readiness requires all 16 skills at VALIDATED

---

*This tracker was created as part of the N-15 remediation from the redteam synthesis report.*
