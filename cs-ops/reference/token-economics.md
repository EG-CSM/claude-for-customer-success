# CS-Ops Plugin — Token Economics Reference

**Note: All figures are illustrative examples based on typical prompt patterns.
Actual token consumption varies by model, context window, and skill invocation depth.
Use these estimates for architectural planning and cost modeling only — not for billing
or SLA commitments.**

---

## Overview

Every CS-Ops skill invocation incurs a baseline pre-flight cost before any skill-specific
work begins. Skills then add their own prompt assembly and response generation costs.

### Pre-flight Baseline (All Skills)

| Phase | What Loads | Estimated Tokens |
|-------|-----------|-----------------|
| Plugin CLAUDE.md | CS-Ops config (segments, capacity targets, health thresholds, escalation matrix) | 400–600 |
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

### process-doc

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads | 550–850 |
| Prompt assembly | Process name, scope, stakeholders, mode flag | 150–300 |
| Context pull | Existing process documentation (if configured) | 200–600 |
| Response generation | Process document (RACI, SOP, or workflow) | 500–900 |
| **Invocation total** | | **~1,400–2,650** |

Notes: Document storage connector adds 200–600 tokens if configured. `--raci` mode is lighter than `--sop`.

---

### playbook-auditor

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes playbook governance thresholds) | 550–850 |
| Prompt assembly | Audit scope, mode flag (`--full` / `--dead-plays` / `--low-adoption`) | 150–300 |
| Context pull | Playbook execution data from CS Platform; play metadata | 500–1,500 |
| Response generation | Audit report with dead plays, low-adoption flags, governance recommendations | 500–1,000 |
| **Invocation total** | | **~1,700–3,650** |

Notes: G6 guardrail adds ~50 tokens to mark play outputs as leads, not prescriptions. Dead play threshold (default 90 days) and low adoption threshold (default 20%) drive flagging logic; token cost is proportional to playbook count.

---

### data-quality-check

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes required field lists, completeness target) | 550–850 |
| Prompt assembly | Scope flag (account, portfolio, segment), data source targets | 200–400 |
| CRM context | Account record field completeness scan | 400–1,000 |
| CS Platform context | Health score record field completeness scan | 400–1,000 |
| Data warehouse context | Optional additional source scan (if configured) | 0–500 |
| Response generation | Quality report with completeness gaps, staleness flags, Reviewer note | 500–900 |
| **Invocation total** | | **~2,050–4,650** |

Notes: G7 staleness guardrail adds ~50 tokens per stale data flag; CS-Ops default staleness threshold is 14 days (vs CSM's 7-day default). Simultaneous multi-connector reads (CRM + CS Platform + optional data warehouse) make this one of the heavier skills. Completeness target default: 90%.

---

### capacity-planner

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes segment definitions, target accounts per CSM) | 550–850 |
| Prompt assembly | Planning scope, segment filter, mode flag (`--current` / `--forecast`) | 200–400 |
| CRM context | Account distribution by segment, CSM assignments | 400–1,000 |
| CS Platform context | Engagement load, health status distribution | 300–800 |
| Response generation | Capacity analysis with over/under-allocation flags by segment | 500–1,000 |
| **Invocation total** | | **~1,950–4,050** |

Notes: G4 guardrail adds ~50 tokens to verify named escalation path before surfacing capacity alerts. Segment count drives cost — 3-segment analysis is approximately 1.5× a single-segment scope. `--forecast` mode pulls projected account growth from CRM pipeline.

---

### segment-analyzer

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes segment ARR floor definitions) | 550–850 |
| Prompt assembly | Analysis scope, segment filter, mode flag | 200–400 |
| CRM context | Account ARR data, industry/size attributes, CSM assignments by segment | 500–1,500 |
| CS Platform context | Health distribution, engagement patterns by segment | 400–1,200 |
| Data warehouse context | Historical trend data (if configured) | 0–800 |
| Response generation | Segment analysis with distribution summary, trend data, CSM alignment review | 600–1,200 |
| **Invocation total** | | **~2,250–5,950** |

Notes: Portfolio-level analysis scales linearly with account count. Data warehouse connector adds 0–800 tokens for historical trend data when configured. Segment ARR floor overrides in config drive classification boundary validation cost.

---

### health-model-review

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes health score component weights, distribution targets) | 550–850 |
| Prompt assembly | Review scope, component filter, mode flag (`--calibration` / `--distribution` / `--full`) | 200–400 |
| CS Platform context | Health component scores, distribution across portfolio | 600–1,800 |
| CRM context | Renewal outcomes, churn history (for calibration validation) | 400–1,200 |
| Survey tool context | NPS/CSAT data for sentiment component (if configured) | 0–500 |
| Response generation | Health model review with calibration findings, distribution analysis, recommended adjustments | 600–1,200 |
| **Invocation total** | | **~2,350–5,950** |

Notes: G1 guardrail adds ~50 tokens to verify health scores are framed as heuristics, not churn predictions. `--full` mode pulls from all configured connectors; `--distribution` mode is CS Platform only and approximately 40% lighter. Survey tool connector adds 0–500 tokens for NPS/CSAT sentiment component validation.

---

### metric-dashboard

| Phase | Description | Estimated Tokens |
|-------|-------------|-----------------|
| Pre-flight | Config reads (includes all metric targets: GRR, NRR, TtV, CSAT, health distribution) | 550–850 |
| Prompt assembly | Reporting period, audience flag, metric scope | 200–400 |
| CRM context | ARR data, renewal outcomes, pipeline | 500–1,500 |
| CS Platform context | Health scores, engagement, TtV actuals, onboarding completion | 600–1,800 |
| Data warehouse context | Historical trend data (if configured) | 0–1,200 |
| BI tool context | Pre-built metric queries (if configured) | 0–600 |
| Survey tool context | NPS/CSAT data (if configured) | 0–500 |
| Response generation | Portfolio metric dashboard with target comparisons, trend lines, Reviewer note | 800–1,500 |
| **Invocation total** | | **~2,650–8,350** |

Notes: G3 guardrail adds ~100 tokens for revenue commitment language on ARR/NRR metric outputs. G5 guardrail adds ~50–100 tokens for confidentiality check before distributing portfolio-level financial data. This skill has the highest potential token cost of any CS-Ops skill — simultaneous reads across up to 5 connectors (CRM, CS Platform, data warehouse, BI tool, survey tool). Heavy mode reflects all 5 connectors configured and active. Each metric target configured in CLAUDE.md adds a comparison calculation to output.

---

## Cost Planning Summary

| Skill | Light Mode | Heavy Mode |
|-------|-----------|-----------|
| customize | ~1,050 | ~1,950 |
| process-doc | ~1,400 | ~2,650 |
| playbook-auditor | ~1,700 | ~3,650 |
| data-quality-check | ~2,050 | ~4,650 |
| capacity-planner | ~1,950 | ~4,050 |
| segment-analyzer | ~2,250 | ~5,950 |
| health-model-review | ~2,350 | ~5,950 |
| cold-start-interview | ~2,550 | ~5,250 |
| metric-dashboard | ~2,650 | ~8,350 |

**Pre-flight baseline (all skills):** ~550–850 tokens per invocation.

---

## Token Optimization Notes

1. **Config caching** — If the runtime caches CLAUDE.md between invocations in the same
   session, the pre-flight cost drops to near-zero after the first call.

2. **Mode selection** — `--distribution` mode on `health-model-review` is ~40% lighter
   than `--full`. `--dead-plays` on `playbook-auditor` is lighter than `--full`. `--current`
   on `capacity-planner` avoids pipeline data pull. Choose modes intentionally.

3. **Connector depth** — `metric-dashboard` can pull from up to 5 connectors simultaneously.
   Skills that read from data warehouse or BI tool add 200–1,200 tokens per connector.
   Token cost scales with content retrieved, not connector count alone.

4. **Portfolio-mode costs** — `segment-analyzer`, `health-model-review`, and `metric-dashboard`
   aggregate data across all accounts. For a 50-account portfolio, expect 3–5× the
   single-account cost for these skills.

5. **Staleness threshold** — CS-Ops uses a 14-day staleness threshold (vs CSM's 7-day
   default). Skills that surface stale data flags add ~50 tokens per flag via the G7
   guardrail. Across all 7 guardrails, expect ~350–700 tokens of fixed overhead per invocation.
