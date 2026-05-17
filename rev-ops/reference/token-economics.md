# Rev-Ops Plugin Token Economics
## claude-for-customer-success / rev-ops — v1.0.0

Per-skill token cost estimates for operators making deployment decisions.
Three usage patterns per skill: minimal (no connectors), typical (standard config),
heavy (large dataset, full connector stack).

Token counts are estimates. Actual usage varies with data volume and connector latency.
Skills with heavy connector usage should be evaluated before scheduling as autonomous agents.

---

## Summary Table

| Skill | Minimal | Typical | Heavy | Connector sensitivity |
|-------|---------|---------|-------|----------------------|
| cold-start-interview | 2K | 4K | 6K | Low — user input only |
| pipeline-coverage-analysis | 1K | 8K | 20K | High — HubSpot pipeline pull |
| forecast-variance-analysis | 1K | 10K | 25K | High — HubSpot multi-quarter history |
| scenario-modeling | 2K | 6K | 12K | Medium — current pipeline state |
| deal-classification | 1K | 12K | 30K | High — per-deal activity history |
| deal-health-scoring | 1K | 15K | 35K | High — per-deal multi-signal |
| pipeline-velocity-tracking | 1K | 8K | 18K | High — stage history across deals |
| stage-integrity-audit | 1K | 6K | 15K | Medium — stage change log |
| next-best-action-recommendation | 1K | 5K | 10K | Low — derived from health scores |
| annual-planning-workflow | 3K | 15K | 30K | High — UoG + territory + quota |
| territory-optimization | 2K | 10K | 20K | Medium — account distribution data |
| quota-sensitivity-analysis | 2K | 5K | 8K | Low — calculation from inputs |
| mid-year-replan-triggering | 1K | 6K | 12K | Medium — actuals vs. baseline |
| crm-hygiene-audit | 1K | 12K | 28K | High — full CRM field scan |
| duplicate-detection | 1K | 8K | 20K | High — account/contact matching |
| field-completion-monitoring | 1K | 6K | 14K | Medium — field completion scan |
| data-decay-tracking | 1K | 6K | 14K | Medium — contact/account freshness |
| deal-to-outcome-tracing | 2K | 10K | 22K | High — HubSpot + CS platform |
| sales-cs-handoff-quality-scoring | 1K | 5K | 10K | Medium — deal fields + OCV lookup |
| closed-won-to-cs-capacity-modeling | 2K | 6K | 10K | Low — forecast + UoG formulas |
| growth-model-vs-actuals-tracking | 2K | 8K | 15K | Medium — actuals vs. Drive baseline |
| outcome-to-value-tracking | 2K | 12K | 25K | High — CS platform + OCV rubrics |
| early-churn-downgrade-signal-detection | 2K | 10K | 20K | High — multi-signal scan |
| gtm-unified-metrics-pulse | 3K | 18K | 35K | Very High — all connectors |
| discount-threshold-monitoring | 1K | 4K | 8K | Low — deal field scan |
| non-standard-terms-detection | 1K | 5K | 10K | Low — deal notes scan |
| revenue-leakage-scanning | 1K | 5K | 10K | Low — deal structure analysis |
| deal-desk-workflow-management | 2K | 6K | 12K | Medium — Linear + HubSpot |
| revenue-brief-generation | 3K | 20K | 40K | Very High — all subagent synthesis |
| cross-system-reconciliation | 2K | 8K | 15K | High — multi-connector comparison |
| change-communication-packaging | 2K | 5K | 8K | Low — text generation from inputs |

---

## High-Cost Skills — Operator Guidance

### revenue-brief-generation (20K–40K typical–heavy)
Pulls from all connected systems. Run interactively or on a schedule with explicit
scope limits. For autonomous deployment, scope to specific agents (SA1 + SA5 only)
rather than full synthesis.

### gtm-unified-metrics-pulse (18K–35K typical–heavy)
Five-section output pulling pipeline, forecast, handoff, capacity, and churn signals.
Token cost scales with pipeline size and CS platform data volume. For large orgs
(>500 open opportunities), limit pipeline pull to current quarter only.

### deal-health-scoring (15K–35K typical–heavy)
Per-deal scoring across five dimensions. Cost scales linearly with open opportunity count.
For portfolios >200 open deals, run on a filtered set (e.g., current quarter close date,
deals >$X ACV) rather than full portfolio.

### deal-classification (12K–30K typical–heavy)
Reads full activity history per deal. Most expensive per-deal skill. Schedule daily for
deals in Proposal+ stages only; weekly for earlier stages.

### crm-hygiene-audit (12K–28K typical–heavy)
Full CRM field scan. Run weekly, not daily. Scope to current quarter's pipeline for
lighter runs; full portfolio for monthly hygiene reports.

---

## Autonomous Agent Token Budgets

Managed agent cookbooks in `managed-agent-cookbooks/` use these default budgets:

| Agent | Default token budget | Rationale |
|-------|---------------------|-----------|
| gtm-pulse-runner | 40K | Full weekly pulse — all connectors |
| capacity-monitor | 12K | SA1 forecast + UoG formulas only |
| churn-signal-scanner | 25K | SA5 multi-signal scan, filtered pipeline |
| deal-desk-watcher | 10K | Deal field scan — low data volume |
| planning-cycle-orchestrator | 35K | Multi-phase planning — runs quarterly |
