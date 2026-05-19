# rev-ops.gtm-unified-metrics-pulse

Produces the weekly 5-section GTM metrics pulse report: pipeline coverage, deal health summary, forecast variance, CS headroom, and churn/contraction flags. Section 4 churn flags are distributed to #cs-leadership only. All Slack posts require RevOps lead approval before distribution (Write-tier).

## Use it for

- Compile 5-section weekly GTM metrics pulse
- Aggregate pipeline coverage, deal health, forecast variance, CS headroom, churn flags
- Route Section 4 churn flags to
- Draft Slack post for RevOps lead approval before distribution

## Don't use it for

- Deep drill-down on individual metrics (use domain-specific sub-skills)
- Revenue brief (more detailed, use revenue-brief-generation)
- Distributing Slack posts without RevOps lead approval

## How to trigger it

Say something like:

- "weekly metrics pulse"
- "GTM pulse"
- "weekly report"
- "metrics pulse"
- "weekly GTM update"

## What you get

- 5-section weekly GTM metrics pulse (Markdown, [DRAFT])
- Slack post draft pending RevOps lead approval

## Prerequisites

- Current pipeline data from CRM
- CS headroom data from CS platform
- Prior week actuals for variance comparison

## Governance

**Approval required** — output must be reviewed before distribution.
- {'G1': 'all ARR figures flagged [review — not yet a revenue commitment]'}
- {'G6': 'data-as-of timestamp on all reads'}
- {'G7': 'escalation path on all churn/risk flags in Section 4'}
- Slack posts require RevOps lead approval; never distribute autonomously

## See also

- rev-ops.pipeline-coverage-analysis
- rev-ops.deal-health-scoring
- rev-ops.forecast-variance-analysis
- rev-ops.revenue-brief-generation

---

*Domain: `rev-ops` · Skill ID: `rev-ops.gtm-unified-metrics-pulse`*
