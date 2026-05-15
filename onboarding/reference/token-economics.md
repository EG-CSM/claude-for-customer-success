# Onboarding Plugin — Token Economics Reference

**Note: All figures are illustrative examples based on typical prompt patterns.
Actual token consumption varies by model, context window, and skill invocation depth.
Use these estimates for architectural planning and cost modeling only — not for billing
or SLA commitments.**

---

## Overview

Every Onboarding skill invocation incurs a baseline pre-flight cost before any skill-specific
work begins. Skills then add their own prompt assembly and response generation costs.

### Pre-flight Baseline (All Skills)

| Phase | What Loads | Estimated Tokens |
|-------|-----------|-----------------|
| Plugin CLAUDE.md | Onboarding config (milestone definitions, TtV targets, escalation matrix) | 400–600 |
| company-profile.md | Shared company context | 150–250 |
| **Pre-flight subtotal** | | **~550–850** |

---

## Per-Skill Estimates

### customize

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (CLAUDE.md + company-profile.md) | 550–850 |
| Prompt assembly | Section target, current config content | 200–500 |
| Response generation | Updated config section + validation notes | 300–600 |
| **Invocation total** | | **~1,050–1,950** |

---

### success-criteria

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, segment, customer goals | 200–400 |
| Context pull | CRM account data, deal notes, initial goals | 300–900 |
| Response generation | Success criteria document for onboarding scope | 500–900 |
| **Invocation total** | | **~1,550–3,050** |

---

### kickoff-prep

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, kickoff date, segment | 150–300 |
| Context pull | CRM account record, deal context, technical counterpart info (if configured) | 400–1,200 |
| Response generation | Kickoff agenda, attendee prep notes, technical setup checklist | 700–1,200 |
| **Invocation total** | | **~1,800–3,550** |

---

### blocker-review

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes Decision posture + escalation matrix) | 550–850 |
| Prompt assembly | Account name, blocker description, blocker type | 200–400 |
| Context pull | Milestone status, prior blockers, engagement history | 400–1,200 |
| Response generation | Blocker analysis + escalation recommendation per escalation matrix | 500–900 |
| **Invocation total** | | **~1,650–3,350** |

Notes: G4 guardrail adds ~50 tokens to verify named escalation path is present before triage output. Technical vs. stakeholder blocker type routes to configured escalation owner.

---

### handoff-doc

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes Handoff point, M5 label) | 550–850 |
| Prompt assembly | Account name, mode flag (`--draft` / `--finalize`) | 150–300 |
| Context pull | Milestone completion data, success criteria, stakeholder contacts, CS Platform data | 600–1,800 |
| Document storage | Write handoff document to configured storage (if connector present) | 100–300 |
| Response generation | Structured handoff document for CSM team | 700–1,200 |
| **Invocation total** | | **~2,100–4,450** |

Notes: Document storage connector adds 100–300 tokens for write operation. `--finalize` mode runs completeness check against all required M5 criteria.

---

### onboarding-plan

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes milestone definitions + average duration) | 550–850 |
| Prompt assembly | Account name, segment, start date | 150–300 |
| Context pull | Success criteria, technical scope, project management system (if configured) | 400–1,500 |
| Response generation | Full milestone-based onboarding plan with target dates | 800–1,500 |
| **Invocation total** | | **~1,900–4,150** |

Notes: Project management connector (e.g., Asana) adds 200–600 tokens for task creation if configured. Milestone labels pulled from configured M0–M5 definitions.

---

### milestone-tracker

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes milestone definitions + target days) | 550–850 |
| Prompt assembly | Account name or portfolio flag, as-of date, mode flag | 200–400 |
| Context pull | CS Platform milestone status data, actual completion dates | 400–1,500 |
| TtV framing | Pace multiplier calculation + `[review — internal planning target]` tag | 100–200 |
| Response generation | Milestone status summary + pace analysis + at-risk flags | 500–1,000 |
| **Invocation total** | | **~1,750–3,950** |

Notes: TtV framing rule adds ~100–200 tokens for the internal planning target disclaimer on all TtV-related output. Portfolio mode scales linearly with account count.

---

### ttv-analysis

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes Target TtV + milestone target days) | 550–850 |
| Prompt assembly | Account name or portfolio scope, analysis period | 200–400 |
| Context pull | Milestone completion data, actual vs. target TtV across accounts | 500–1,800 |
| TtV framing | Pace multiplier calculations + `[review — internal planning target]` tags | 100–300 |
| Response generation | TtV analysis with segment breakdown and trend data | 700–1,200 |
| **Invocation total** | | **~2,050–4,550** |

Notes: TtV disclaimer adds ~100–300 tokens across all TtV figure outputs. Portfolio mode scales with account count; segment-level analysis is heavier than single-account.

---

### cold-start-interview

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Mode flag, existing CLAUDE.md if `--redo` | 100–600 |
| Interview dialogue | Multi-turn Q&A covering all required Onboarding config sections | 1,500–3,000 |
| Config write | Generated CLAUDE.md content | 400–800 |
| **Invocation total** | | **~2,550–5,250** |

Notes: Full `--full` mode covers all config sections including milestone definitions and TtV targets; `--redo` loads existing config for diff.

---

## Cost Planning Summary

| Skill | Light Mode | Heavy Mode |
|-------|-----------|-----------|
| customize | ~1,050 | ~1,950 |
| success-criteria | ~1,550 | ~3,050 |
| blocker-review | ~1,650 | ~3,350 |
| kickoff-prep | ~1,800 | ~3,550 |
| milestone-tracker | ~1,750 | ~3,950 |
| onboarding-plan | ~1,900 | ~4,150 |
| ttv-analysis | ~2,050 | ~4,550 |
| handoff-doc | ~2,100 | ~4,450 |
| cold-start-interview | ~2,550 | ~5,250 |

**Pre-flight baseline (all skills):** ~550–850 tokens per invocation.

---

## Token Optimization Notes

1. **Config caching** — If the runtime caches CLAUDE.md between invocations in the same
   session, the pre-flight cost drops to near-zero after the first call.

2. **Mode selection** — `--draft` versus `--finalize` modes in `handoff-doc` differ
   by ~30% in output token cost. `--brief` flags on milestone-tracker reduce output
   tokens by 40–50%.

3. **Portfolio-mode costs** — `milestone-tracker` and `ttv-analysis` aggregate data
   across all accounts. For a 50-account portfolio, expect 3–5× the single-account cost.

4. **Connector depth** — Project management (Asana) and document storage (Google Drive)
   connectors each add 100–600 tokens per invocation when configured. Token cost scales
   with task count or document size retrieved.

5. **TtV framing overhead** — The internal planning target disclaimer adds ~100–300 tokens
   per invocation for skills that surface TtV figures (`ttv-analysis`, `milestone-tracker`).
   Across all 7 guardrails, expect ~350–700 tokens of fixed overhead per invocation.
