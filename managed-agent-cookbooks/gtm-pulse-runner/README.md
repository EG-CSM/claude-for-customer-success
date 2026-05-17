# GTM Pulse Runner
## Managed Agent Cookbook — rev-ops plugin v1.0.0

Runs the weekly GTM unified metrics pulse. Collects pipeline, revenue, velocity,
and churn signals from HubSpot and your CS platform; formats five Slack-ready
sections with full data freshness labels; routes sections to the correct channels
with a human-in-the-loop gate on first run and for Tier 3 high-ACV churn flags.

---

## What This Agent Does

The GTM Pulse Runner executes a three-subagent ETL pipeline on demand or on a
weekly cron schedule:

1. **data-collector** — Pulls raw metrics from HubSpot (pipeline, closed-won,
   stage velocity) and your CS platform (churn signals Tier 2 and Tier 3). Returns
   a structured JSON payload. Applies confidence band assignment based on connector
   availability and data freshness.

2. **pulse-composer** — Transforms the raw payload into five Slack-formatted
   sections with data freshness headers, emoji status indicators, G1-compliant
   forecast language, and G7 escalation paths on churn flags. Pure transformation —
   no connector access.

3. **delivery-router** — Gates delivery on first-run operator confirmation and
   Tier 3 high-ACV review (>$250K ACV). Routes sections to the correct channels.
   Maintains a state file and appends to an audit log on every execution.

**Default routing:**

| Section | Content | Channel |
|---------|---------|---------|
| 1 — Pipeline Status | Coverage ratio, stage breakdown | `#revops-alignment` |
| 2 — Revenue Run-Rate | Closed-won pacing vs target | `#revops-alignment` |
| 3 — GTM Velocity | Stage velocity, deal creation rate | `#revops-alignment` |
| 4 — Churn Signals | Account names, ACV, Tier 2/3 signals | `#cs-leadership` |
| 5 — Cross-Function Summary | Aggregate counts only (no names) | `#revops-alignment` + `#cs-leadership` |

---

## Architecture

```
gtm-pulse-runner/
├── agent.yaml                        # Orchestrator definition
├── agents/
│   └── gtm-pulse-runner.md           # Orchestrator system prompt
├── subagents/
│   ├── data-collector.yaml           # HubSpot + CS platform; no filesystem
│   ├── data-collector.md
│   ├── pulse-composer.yaml           # Pure transform; zero MCP access
│   ├── pulse-composer.md
│   ├── delivery-router.yaml          # Filesystem + Slack only
│   └── delivery-router.md
├── steering-examples.json            # 8 test scenarios
└── README.md                         # This file
```

**Tool assignment by subagent (principle of least privilege):**

| Subagent | Filesystem | HubSpot MCP | CS Platform MCP | Slack MCP |
|----------|-----------|------------|----------------|----------|
| data-collector | — | ✓ | ✓ | — |
| pulse-composer | — | — | — | — |
| delivery-router | read + write | — | — | ✓ |

---

## State and Audit Persistence

The delivery-router writes to two files under `~/.cs-agent/`:

### `~/.cs-agent/gtm-pulse-state.json`

Created on first confirmed run. Controls the first-run gate on subsequent
executions. Write-once after confirmation; updated only if schedule changes.

```json
{
  "first_run_confirmed": true,
  "confirmed_by": "Sarah Chen",
  "confirmed_at": "2026-01-06T09:12:00Z",
  "weekly_schedule_confirmed": true,
  "schedule_cron": "0 8 * * 1"
}
```

If this file is absent or `first_run_confirmed = false`, the agent pauses
delivery, presents the routing confirmation prompt, and waits for operator
approval before writing the state and proceeding.

### `~/.cs-agent/gtm-pulse-audit.jsonl`

Appended on every execution (including failed runs). Each line is a JSON record:

```json
{
  "timestamp": "2026-01-06T09:15:43Z",
  "run_type": "scheduled",
  "delivery_status": "posted",
  "sections_posted": ["section_1", "section_2", "section_3", "section_4", "section_5"],
  "tier3_flags_count": 1,
  "tier3_gate_triggered": true,
  "slack_available": true,
  "connectors": { "hubspot": "live", "cs_platform": "live" }
}
```

---

## Deployment Prerequisites

- [ ] `rev-ops` plugin cold-start complete (practice profile populated)
- [ ] HubSpot MCP server running — `HUBSPOT_MCP_URL` env var set
- [ ] CS platform MCP server running — `CS_PLATFORM_MCP_URL` env var set
  *(Section 4 degrades gracefully if unavailable — see Data Gap Behavior)*
- [ ] Slack MCP server running — `SLACK_MCP_URL` env var set
- [ ] `#revops-alignment` channel exists and bot has `chat:write` scope
- [ ] `#cs-leadership` channel exists and bot has `chat:write` scope
- [ ] RevOps lead available to confirm routing on first run

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HUBSPOT_MCP_URL` | Required | HubSpot MCP server endpoint |
| `CS_PLATFORM_MCP_URL` | Required | CS platform MCP server endpoint |
| `SLACK_MCP_URL` | Required | Slack MCP server endpoint |

---

## Running the Agent

### On-demand

```
Run the weekly GTM pulse and post to the configured channels.
```

### Preview mode (no Slack posts)

```
Run the GTM pulse in preview mode — show me the output but don't post to Slack.
```

### Scoped sections

```
Run the weekly pulse but only Sections 1 and 3 this week — skip the churn section.
```

### Churn-only for CS leadership

```
Run just the churn signals section this week and send it to CS leadership.
```

### Scheduled (weekly cron)

To schedule automatic weekly runs, confirm the cron during first-run setup or
update `~/.cs-agent/gtm-pulse-state.json` directly:

| Schedule | Cron expression |
|----------|----------------|
| Monday 8am UTC | `0 8 * * 1` |
| Monday 9am EST (UTC-5) | `0 14 * * 1` |
| Friday 4pm UTC (end-of-week) | `0 16 * * 5` |
| Monday 7am PST (UTC-8) | `0 15 * * 1` |

The `schedule_cron` field in the state file is recorded for audit purposes.
Actual scheduling must be configured separately in your Claude Code task
scheduler or cron infrastructure.

---

## First-Run Flow

On the first execution (state file absent or `first_run_confirmed = false`),
delivery-router pauses before posting and displays:

```
GTM Pulse Runner — First Run Setup
───────────────────────────────────
This is the first time the GTM pulse has been run for [company_name].

Before posting to Slack, I need your confirmation on two things:

1. Routing confirmation:
   Sections 1, 2, 3, 5 (aggregates) → #revops-alignment
   Sections 4, 5 (account detail)   → #cs-leadership

2. Weekly schedule (optional — leave blank to run manually):
   Enter a cron expression (e.g., "0 8 * * 1" = Monday 8am UTC)
   or press Enter to run on-demand only.

Please confirm: [YES / NO] and provide your name for the audit log.
```

On YES, the state file is written and delivery proceeds. On NO or no response,
delivery is paused with:
`GTM Pulse — delivery paused. First-run confirmation required before posting.`

---

## Tier 3 High-ACV Gate

When Section 4 contains accounts with ACV > $250,000, delivery-router pauses
before posting Section 4 and displays the flagged accounts for individual review.

Sections 1, 2, 3, and 5 (aggregate) are posted immediately. Section 4 is held
until explicit confirmation. If HOLD is selected, the hold is noted in the
delivery receipt and audit log, and Section 4 is not posted until manually
re-triggered.

---

## Output Reference

### Section 1 — Pipeline Status and Coverage

Coverage ratio classified against domain model thresholds:

| Ratio | Status | Emoji |
|-------|--------|-------|
| < 2x | CRITICAL | 🔴 |
| 2x – 3x | AT-RISK | 🟡 |
| 3x – 5x | HEALTHY | 🟢 |
| > 5x | INSPECT | 🔵 |

Win rate: live trailing-4Q average from HubSpot, or 25% fallback (labeled).

### Section 2 — Revenue Run-Rate vs Target

Pacing computed from NRR-adjusted new ARR target formula (see
`reference/revops-domain-model.md`). Qualified with G1 forecast language:
"current model indicates," "P50 estimate," "based on pipeline as of [date]."

### Section 3 — GTM Velocity Indicators

Velocity flags when stage velocity >25% slower than 4Q average. Creation flags
when deal creation <50% of weekly average. Clean week renders:
`No velocity anomalies detected this week.`

### Section 4 — Account-Level Churn Signals

Routed to `#cs-leadership` only. Contains Tier 2 (behavioral risk) and
Tier 3 (pre-renewal risk) accounts with ACV, days to renewal, and primary signal.
Every entry carries a G7 escalation path. If the escalation owner is not in the
CS platform data, renders: `Escalation: RevOps lead to assign owner — SLA: 48h`

### Section 5 — Cross-Function Summary

Aggregate counts only — no account names. Routes to both channels. Flags any
dimension that is CRITICAL or has >3 Tier 3 accounts as requiring leadership
attention.

---

## Data Gap Behavior

| Connector unavailable | Sections affected | Behavior |
|-----------------------|-------------------|----------|
| HubSpot | 1, 2, 3 | Sections render as "⚠ Data Unavailable." Section 4 and 5 (partial) post if CS platform is live. |
| CS platform | 4 | Section 4 renders as "⚠ Data Unavailable." Sections 1–3 and 5 (partial) post normally. |
| Both connectors | 1, 2, 3, 4 | Confidence = Insufficient. Delivery-router reports and stops — no sections posted. |
| HubSpot partial (no closed-won) | 2 | Section 2 marked `degraded`; available data included with gap label. |
| Win rate not configured | 1 | 25% fallback used, labeled `[Win rate: fallback 25%]`. |
| Slack unavailable | All | All sections rendered in session for manual distribution. No retry. |

When one connector is unavailable, delivery-router prepends a data availability
note to the first section posted to each channel.

---

## Confidence Bands

Assigned by data-collector and carried through to each formatted section:

| Condition | Band |
|-----------|------|
| Both connectors live, data < 14 days old | `[Confidence: High]` |
| One connector unavailable | `[Confidence: Moderate]` |
| CRM data > 14 days stale | `[Confidence: Moderate]` minimum |
| Both connectors unavailable | `[Data: Insufficient]` — no analysis produced |

---

## Customization

**Change routing channels:** Update the routing table in `delivery-router.md`.
The `sections_requested` input supports any subset of `[1, 2, 3, 4, 5]`.

**Adjust Tier 3 ACV threshold:** The $250,000 threshold is hardcoded in
`delivery-router.md` (Step 3) and `data-collector.md` (Section 4 notes). Update
both to change the gate threshold.

**Add sections:** Extend the data-collector output schema, add a format template
to pulse-composer, and add routing rules to delivery-router.

**Change schedule:** Update `schedule_cron` in `~/.cs-agent/gtm-pulse-state.json`
and reconfigure your task scheduler. The state file entry is for audit logging
only — it does not drive execution timing.

---

## Token Budget

| Run type | Typical | Heavy |
|----------|---------|-------|
| All 5 sections, both connectors live | ~18K tokens | ~35K tokens |
| Sections 1–3 only (HubSpot only) | ~10K tokens | ~18K tokens |
| Section 4 only (churn-only pulse) | ~8K tokens | ~15K tokens |
| Preview mode | Same as above | — |

Heavy runs occur when pipeline is large (>50 open deals) or CS platform returns
many flagged accounts. See `reference/token-economics.md` for detail.

---

## Subagent Reference

| Subagent | Responsibility | Connectors | State |
|----------|---------------|-----------|-------|
| `data-collector` | Pull raw metrics from HubSpot and CS platform; assign confidence band | HubSpot, CS platform | None |
| `pulse-composer` | Transform raw payload into 5 Slack-formatted sections; apply G1/G6/G7 guardrails | None | None |
| `delivery-router` | Gate on first-run + Tier 3; route and post; write state and audit log | Slack + filesystem | `~/.cs-agent/gtm-pulse-state.json`, `~/.cs-agent/gtm-pulse-audit.jsonl` |

---

## Related Files

| File | Purpose |
|------|---------|
| `reference/revops-domain-model.md` | Guardrails G1–G8, confidence bands, churn tier definitions, pipeline thresholds |
| `reference/config-schema.md` | Practice profile fields — `company_name`, `primary_segment`, `current_arr`, etc. |
| `reference/token-economics.md` | Token budget guidance for all rev-ops agents |
| `skills/gtm-unified-metrics-pulse/SKILL.md` | Interactive skill version of this pulse (single-session, no Slack posting) |
| `skills/unit-of-growth-calculator/SKILL.md` | NRR-adjusted target calculations used in Section 2 |
