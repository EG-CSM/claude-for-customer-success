# Renewals Plugin — Token Economics Reference

**Note: All figures are illustrative examples based on typical prompt patterns.
Actual token consumption varies by model, context window, and skill invocation depth.
Use these estimates for architectural planning and cost modeling only — not for billing
or SLA commitments.**

---

## Overview

Every Renewals skill invocation incurs a baseline pre-flight cost before any skill-specific
work begins. Skills then add their own prompt assembly and response generation costs.

### Pre-flight Baseline (All Skills)

| Phase | What Loads | Estimated Tokens |
|-------|-----------|-----------------|
| Plugin CLAUDE.md | Renewals config (segments, pipeline weights, scenario parameters, escalation matrix) | 400–600 |
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

### risk-assessment

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, risk signal, mode flag (`--brief` / `--deep`) | 200–400 |
| Context pull | Health data, engagement history, renewal timeline | 400–1,000 |
| Response generation | Risk summary and recommended actions | 400–700 |
| **Invocation total** | | **~1,550–2,950** |

Notes: G1 guardrail enforcement adds ~50 tokens to verify health scores are not framed as churn predictions.

---

### churn-analysis

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name or portfolio flag, time range | 200–400 |
| Context pull | CS Platform churn signals, engagement history, health trends | 500–1,500 |
| Response generation | Churn driver analysis + pattern summary | 500–900 |
| **Invocation total** | | **~1,750–3,650** |

Notes: G1 guardrail adds ~50 tokens; portfolio mode scales linearly with account count.

---

### cold-start-interview

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Mode flag, existing CLAUDE.md if `--redo` | 100–600 |
| Interview dialogue | Multi-turn Q&A covering all required Renewals config sections | 1,500–3,000 |
| Config write | Generated CLAUDE.md content | 400–800 |
| **Invocation total** | | **~2,550–5,250** |

Notes: Full `--full` mode covers all config sections including pipeline weights and scenario parameters; `--redo` loads existing config for diff.

---

### contract-review

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, contract type, notice period context | 200–400 |
| Contract context | Contract management system retrieval (if configured) | 300–1,200 |
| Response generation | Contract summary, notice period flags, renewal risk items | 500–900 |
| **Invocation total** | | **~1,550–3,350** |

Notes: Contract management connector adds 300–1,200 tokens depending on contract length retrieved.

---

### expansion-signal

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, mode flag | 150–300 |
| Context pull | Product usage, feature adoption, CRM + CS Platform signals | 500–1,500 |
| Response generation | Expansion signal summary with qualification status | 400–800 |
| **Invocation total** | | **~1,600–3,450** |

Notes: G2 guardrail adds ~50–100 tokens to verify expansion requires economic buyer qualification before inclusion in NRR.

---

### negotiation-prep

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes Decision posture) | 550–850 |
| Prompt assembly | Account name, renewal date, deal size, negotiation context | 200–400 |
| Context pull | Account health, engagement history, stakeholder map, prior renewal outcomes | 600–1,800 |
| Response generation | Negotiation brief with posture-calibrated talking points | 700–1,200 |
| **Invocation total** | | **~2,050–4,250** |

Notes: `Aggressive` posture mode generates more expansion-focused content; `Conservative` mode generates more risk-mitigation framing. Executive escalation path adds ~50 tokens if configured.

---

### price-increase-prep

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Account name, price increase amount, timing | 200–400 |
| Context pull | Account health, engagement, relationship context, prior contract data | 500–1,500 |
| Response generation | Price increase brief with objection handling and value defense | 700–1,200 |
| **Invocation total** | | **~1,950–3,950** |

Notes: G3 guardrail adds ~50–100 tokens for revenue commitment language on any price impact projections.

---

### renewal-forecast

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes pipeline stage weights + scenario parameters) | 550–850 |
| Prompt assembly | Portfolio flag or named accounts, forecast period, mode flag (`--base` / `--scenarios`) | 200–400 |
| Context pull | CRM pipeline stage data, health scores, ARR data; CPQ data if configured | 700–2,500 |
| Scenario modeling | 3-scenario calculation (best/base/worst) using configured weights | 200–400 |
| Response generation | Weighted forecast + scenario table + G3 commitment language | 700–1,500 |
| **Invocation total** | | **~2,350–5,650** |

Notes: G3 guardrail adds ~100 tokens for the revenue commitment language + Finance validation callout on all forecast outputs. Portfolio mode scales with account count. CPQ connector adds 200–500 tokens if configured.

---

### executive-summary

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Portfolio or account scope, reporting period, audience flag | 200–400 |
| Context pull | Forecast data, health distribution, at-risk accounts, expansion signals | 800–2,500 |
| Response generation | Executive narrative with portfolio health, forecast, and risk flags | 800–1,500 |
| **Invocation total** | | **~2,350–5,250** |

Notes: G3 adds ~100 tokens for revenue commitment language; G5 adds ~50–100 tokens for confidentiality check before portfolio-level financial data distribution.

---

## Cost Planning Summary

| Skill | Light Mode | Heavy Mode |
|-------|-----------|-----------|
| customize | ~1,050 | ~1,950 |
| risk-assessment | ~1,550 | ~2,950 |
| contract-review | ~1,550 | ~3,350 |
| expansion-signal | ~1,600 | ~3,450 |
| churn-analysis | ~1,750 | ~3,650 |
| price-increase-prep | ~1,950 | ~3,950 |
| negotiation-prep | ~2,050 | ~4,250 |
| cold-start-interview | ~2,550 | ~5,250 |
| renewal-forecast | ~2,350 | ~5,650 |
| executive-summary | ~2,350 | ~5,250 |

**Pre-flight baseline (all skills):** ~550–850 tokens per invocation.

---

## Token Optimization Notes

1. **Config caching** — If the runtime caches CLAUDE.md between invocations in the same
   session, the pre-flight cost drops to near-zero after the first call.

2. **Mode selection** — `--brief` and `--base` flags typically reduce output tokens by
   40–60% versus deep/scenarios modes. Choose modes intentionally.

3. **Portfolio-mode costs** — `renewal-forecast` and `executive-summary` aggregate across
   all accounts. For a 50-account portfolio, expect 3–5× the single-account cost.

4. **Connector depth** — Skills that pull from contract management (DocuSign) or CPQ
   (Salesforce CPQ) add 200–1,200 tokens per connector read depending on content retrieved.

5. **G3 overhead** — The revenue commitment guardrail adds ~100 tokens per forecast output
   for the commitment language block + Finance/RevOps validation callout. Across
   all 7 guardrails, expect ~350–700 tokens of fixed overhead per invocation.
