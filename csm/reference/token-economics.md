# CSM Plugin — Token Economics Reference

**Note: All figures are illustrative examples based on typical prompt patterns.
Actual token consumption varies by model, context window, and skill invocation depth.
Use these estimates for architectural planning and cost modeling only — not for billing
or SLA commitments.**

---

## Overview

Every CSM skill invocation incurs a baseline pre-flight cost before any skill-specific
work begins. Skills then add their own prompt assembly and response generation costs.

### Pre-flight Baseline (All Skills)

| Phase | What Loads | Estimated Tokens |
|-------|-----------|-----------------|
| Plugin CLAUDE.md | CSM config (segments, escalation matrix, health thresholds) | 400–600 |
| company-profile.md | Shared company context | 150–250 |
| **Pre-flight subtotal** | | **~550–850** |

---

## Per-Skill Estimates

### account-research

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (CLAUDE.md + company-profile.md) | 550–850 |
| Prompt assembly | Account name, CRM query instructions, mode flag (`--brief` / `--deep` / `--stakeholders`) | 200–400 |
| CRM context | Account record, contacts, activity history (varies by depth) | 500–2,500 |
| Response generation | Brief: account summary ~600 tokens; Deep: full profile ~1,500 tokens | 600–1,500 |
| **Invocation total** | | **~1,850–5,250** |

Notes: `--deep` mode triggers stakeholder org-chart assembly; token cost scales with contact count in CRM.

---

### call-prep

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, call type (kickoff/qbr/health/renewal/check-in/custom), date | 150–250 |
| Context pull | Account record + recent interactions + health data | 600–1,800 |
| Response generation | Agenda, talking points, context summary | 800–1,200 |
| **Invocation total** | | **~2,100–4,100** |

Notes: `kickoff` and `qbr` modes pull more context; `check-in` is the lightest invocation.

---

### cold-start-interview

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Mode flag, existing CLAUDE.md if `--redo` | 100–600 |
| Interview dialogue | Multi-turn Q&A to populate all required config fields | 1,500–3,000 |
| Config write | Generated CLAUDE.md content | 400–800 |
| **Invocation total** | | **~2,550–5,250** |

Notes: Full `--full` mode covers all 10 config sections; `--redo` loads existing config for diff.

---

### customize

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Section target, current config content | 200–500 |
| Response generation | Updated config section + validation notes | 300–600 |
| **Invocation total** | | **~1,050–1,950** |

---

### escalation-memo

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account context, escalation type, existing memo (if `--update`) | 300–800 |
| Response generation | Formal escalation memo draft | 600–1,000 |
| **Invocation total** | | **~1,450–2,650** |

Notes: G4 guardrail enforcement adds ~50–100 tokens to verify named escalation path in config.

---

### health-score-review

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes health thresholds + component weights) | 550–850 |
| Prompt assembly | Account name, mode flag, health data payload | 200–400 |
| Health data context | CS Platform health record + component scores | 400–1,200 |
| Response generation | Triage: ~500 tokens; Deep: ~1,200 tokens; Portfolio: ~2,000 tokens | 500–2,000 |
| **Invocation total** | | **~1,650–4,450** |

Notes: `--portfolio` mode aggregates across all accounts — token cost scales linearly with portfolio size.

---

### qbr-builder

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, QBR date, mode flag | 150–250 |
| Context pull | Value metrics, health history, outcomes, success plan | 800–2,500 |
| Response generation | Draft: full QBR slide content; Exec-brief: condensed narrative | 1,200–2,500 |
| **Invocation total** | | **~2,700–6,100** |

Notes: `--exec-brief` mode is ~40% lighter than `--draft`. Document storage connector (if configured) adds one additional context read.

---

### renewal-readiness

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, renewal date, mode flag | 150–250 |
| Context pull | Health data, engagement history, stakeholder map | 600–1,800 |
| Response generation | Readiness assessment + recommended actions | 600–1,000 |
| **Invocation total** | | **~1,900–3,900** |

---

### risk-flag

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account context, risk signal description, mode flag | 200–400 |
| Response generation | Risk summary (`--brief`) or escalation memo (`--escalation-memo`) | 400–900 |
| **Invocation total** | | **~1,150–2,150** |

Notes: `--escalation-memo` triggers the full escalation-memo generation path; see that skill for cost breakdown.

---

### stakeholder-map

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, mode flag | 100–200 |
| CRM context | Contact list with roles, engagement history | 400–1,200 |
| Response generation | Stakeholder map / gap analysis / sponsor risk | 500–900 |
| **Invocation total** | | **~1,550–3,150** |

---

### success-plan-builder

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, mode flag, existing plan (if `--review`) | 200–800 |
| Context pull | Health data, goals, outcomes, engagement history | 600–1,800 |
| Response generation | Success plan document | 800–1,500 |
| **Invocation total** | | **~2,150–4,950** |

---

### taro-play-runner

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes CS methodology field) | 550–850 |
| Play selection | Situation description → play matching | 200–400 |
| Play content | TARO play steps and guidance | 400–800 |
| Response generation | Customized play execution for account | 500–900 |
| **Invocation total** | | **~1,650–2,950** |

Notes: G6 guardrail adds ~50 tokens to mark TARO output as leads, not prescriptions.

---

### value-statement

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes Primary value metric if configured) | 550–850 |
| Prompt assembly | Account name, statement type (internal/customer/exec-brief/ae-handoff) | 150–300 |
| Context pull | Outcome data, usage metrics, success milestones | 400–1,200 |
| Response generation | Value narrative formatted for target audience | 500–1,000 |
| **Invocation total** | | **~1,600–3,350** |

Notes: `--customer` and `--exec-brief` modes require G5 confidentiality check (internal data must be scrubbed).

---

## Cost Planning Summary

| Skill | Light Mode | Heavy Mode |
|-------|-----------|-----------|
| account-research | ~1,850 | ~5,250 |
| call-prep | ~2,100 | ~4,100 |
| cold-start-interview | ~2,550 | ~5,250 |
| customize | ~1,050 | ~1,950 |
| escalation-memo | ~1,450 | ~2,650 |
| health-score-review | ~1,650 | ~4,450 |
| qbr-builder | ~2,700 | ~6,100 |
| renewal-readiness | ~1,900 | ~3,900 |
| risk-flag | ~1,150 | ~2,150 |
| stakeholder-map | ~1,550 | ~3,150 |
| success-plan-builder | ~2,150 | ~4,950 |
| taro-play-runner | ~1,650 | ~2,950 |
| value-statement | ~1,600 | ~3,350 |

**Pre-flight baseline (all skills):** ~550–850 tokens per invocation.

---

## Token Optimization Notes

1. **Config caching** — If the runtime caches CLAUDE.md between invocations in the same
   session, the pre-flight cost drops to near-zero after the first call.

2. **Mode selection** — `--brief` and `--quick` flags typically reduce output tokens by
   40–60% versus deep/full modes. Choose modes intentionally.

3. **Portfolio-mode costs** — Skills with `--portfolio` mode aggregate data across all
   accounts. For a 50-account portfolio, expect 3–5× the single-account cost.

4. **Connector depth** — Skills that pull from call recordings (Gong) or document
   storage add 500–2,000 tokens per connector read. Token cost scales with content
   retrieved, not with the connector count.

5. **Guardrail overhead** — Each active guardrail (G1–G7) adds ~50–100 tokens to
   verify compliance and label outputs. Across 7 guardrails, this is ~350–700 tokens
   of fixed overhead per invocation.
