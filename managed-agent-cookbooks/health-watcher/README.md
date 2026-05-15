# Health Watcher — Deployment & Configuration Guide

## What This Agent Does

The Health Watcher runs daily or weekly and monitors health score movement across the
configured account portfolio. It compares each account's current health score against a
persisted baseline from the prior run and fires alerts when scores drop beyond configured
thresholds or when accounts shift health bands. It does not produce a portfolio report —
it produces an alert digest. Accounts that are stable are logged but not surfaced.

The digest is designed for CS team monitoring between scheduled reviews — it answers:
"Which accounts had meaningful health score changes since we last looked?"

**Outputs:**
- Alert digest: accounts with immediate or watch-level movement, with score deltas and
  one contextual note per account
- Portfolio Movement table: counts of accounts by movement direction and band
- Optional Slack delivery: mrkdwn version posted to a configured channel
- Baseline update: the current run's scores are persisted as the next run's baseline

---

## Architecture

```
Orchestrator: Health Watcher
│
├── Subagent 1: Health Reader
│   Pulls current health scores for all accounts in scope from the configured
│   health score source. Returns one score record per account with band
│   classification. Also loads the prior baseline from the filesystem.
│
├── Subagent 2: Trend Analyzer
│   Compares current scores against the baseline. Classifies each account as
│   Immediate, Watch, Recovering, or Stable based on configured alert thresholds
│   and band movement rules. Returns a ranked alert list.
│
└── Subagent 3: Alert Composer
    Formats the alert list into the digest. Persists the updated baseline.
    Delivers the markdown output and optional Slack message. Calls no data
    connectors except Slack for delivery.
```

---

## Baseline Persistence

The Health Watcher is a stateful agent. It stores health scores from each run in a JSON
baseline file at `baseline_file_path`. The next run reads this file to calculate score
movement.

**Baseline format:**
```json
{
  "run_timestamp": "[ISO timestamp]",
  "accounts": {
    "[account-id]": { "score": 72, "band": "yellow" },
    "[account-id]": { "score": 88, "band": "green" }
  }
}
```

**Baseline write timing:** The Alert Composer writes the updated baseline at Step 5
(before delivery). A write failure halts the run — the agent will not deliver an alert
digest without persisting the baseline, because the next run would not have accurate
prior data.

**First run behavior:** When no baseline file exists, the agent runs in initialization
mode. It pulls current scores, logs that this is a baseline capture run, and writes the
baseline. No alerts are fired. The digest notes that this was the initialization run.

**Corrupted or missing baseline mid-run:** If the baseline file exists but cannot be
parsed, the agent treats the run as an initialization run — no alerts fired, baseline
written fresh. This is logged in the digest.

---

## Prerequisites

### Required Connectors

| Connector | Role |
|-----------|------|
| Health score platform | Current health scores for all accounts in scope |

The health score source can be a dedicated health platform (Gainsight, Totango,
ChurnZero) or a CRM with health score custom fields. Configure `health_score_source`
to point to the appropriate connector.

### Optional Connectors

| Connector | Role |
|-----------|------|
| Slack | Delivery of the mrkdwn alert digest to a channel |
| CRM | CSM assignment lookup for display in the digest |

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Run `/csm:cold-start-interview --section health` to configure this file if it contains
`[PLACEHOLDER]` values.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `health_score_source` | Connector name for health scores | `gainsight-mcp` |
| `health_score_scale` | Score range the platform uses | `0-100` |
| `alert_threshold` | Minimum drop (in points) to trigger an Immediate alert | `15` |
| `baseline_file_path` | Absolute path for baseline JSON storage | `~/.cs-agent/health-baseline.json` |
| `digest_output` | `file` \| `slack` \| `both` | `both` |
| `reporting_mode` | Determines date window and output format | `daily` \| `weekly` |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `slack_channel` | Slack channel for delivery (required if digest_output includes `slack`) | — |
| `digest_file_path` | Where to save the markdown digest | — |
| `exclude_accounts` | Account IDs to skip during scoring | — |
| `csm_filter` | Restrict alerts to accounts owned by a specific CSM | all CSMs |

### Alert Tier Definitions

| Tier | Trigger Condition |
|------|-----------------|
| 🔴 Immediate Attention | Score drop ≥ `alert_threshold` in one period, OR band movement = entered red |
| 🟡 Watch | Score drop below threshold over 2+ consecutive periods, OR band-declining trend, OR recovering from red |
| ✅ Stable | Score movement ≤ ±2 points — logged but NOT in alert output |

Recovering accounts (moved out of red since last run) appear in the Watch section in
weekly mode. In daily mode, recovering accounts are included in the Watch section with
a "recovering" note.

---

## Scheduling

### Recommended: Daily Morning

```
cronExpression: "0 8 * * *"
prompt: "Run the health watcher."
```

Delivers the digest before the CS team's morning standup. Best for portfolios with
volatile health scores or frequent at-risk accounts.

### Alternative: Weekly Monday Morning

```
cronExpression: "30 8 * * 1"
prompt: "Run the weekly health watcher."
```

Delivers a trend summary with movement over the prior week. Includes a recovering
accounts section in the digest. Best for stable portfolios where daily granularity
is more noise than signal.

### On-Demand Invocation

Trigger at any time with natural language. See `steering-examples.json` for the full
prompting pattern library. Common invocations:

- "Run the health watcher."
- "Check for health score drops since this morning."
- "What moved in health scores this week?"

---

## Output Reference

### Alert Digest Section Order (fixed — never reordered)

| Section | Contents | Format |
|---------|----------|--------|
| Header | Date, run timestamp, accounts assessed, alert counts | Header block |
| 🔴 Immediate Attention | All accounts triggering immediate alert | Per-account block |
| 🟡 Watch | All accounts with watch-level movement | Per-account block |
| 🟢 Recovering (weekly only) | Accounts that moved out of red since last run | Per-account block |
| Portfolio Movement | Count of accounts by direction and band | Table |

Sections with zero accounts are omitted from the body. The Portfolio Movement table
always renders, including zero-count categories.

When there are zero Immediate Attention accounts, the digest opens with:

> No immediate health alerts this period.

immediately before the Watch section (or Portfolio Movement if Watch is also empty).

### Per-Account Format

Each alerted account uses this block:

```
**[Account Name]** · [Segment or —] · CSM: [Name or —]
Score: [prior] → [current] ([+/-N] points) · Band: [prior band] → [current band or unchanged]
Note: [One contextual observation — not a diagnosis]
```

One note maximum per account. The note describes the observed movement, not the cause.
Examples: "Entered red band for the first time this period" / "Third consecutive week of
declining scores" / "Recovered from red — now yellow for two periods."

### Weekly Mode Additions

In weekly mode, the digest adds:
- Recovering accounts section between Watch and Portfolio Movement
- A trend summary line in the header: "[N] accounts declining · [N] recovering · [N] stable"
- Period comparison in the Portfolio Movement table

---

## Data Gap Behavior

| Situation | Behavior |
|-----------|----------|
| Health score source unavailable | Halt immediately — no digest produced; do not run on stale data |
| Baseline file missing on first run | Initialization mode — capture baseline; no alerts fired |
| Baseline file corrupted or unparseable | Treat as initialization run; log the condition; write fresh baseline |
| Baseline write fails | Halt before delivery — alert digest not delivered without persisted baseline |
| Account not in baseline (new account) | No comparison available; include in portfolio count; no alert fired |
| Account removed from health platform | Flag in digest footer; remove from baseline on next write |
| Slack connector unavailable | Complete markdown digest; note Slack failure in delivery status; do not halt |
| CRM unavailable (CSM lookup) | Render CSM as `—` in digest; continue |
| Score returned as null for an account | Skip account in alert processing; note in Portfolio Movement footnotes |

---

## Customization

### Adjusting the Alert Threshold

Change `alert_threshold` in config. The default of 15 points is appropriate for a 0–100
scale. For platforms with a 0–10 scale, consider 2–3 points as the threshold. The Watch
tier is always defined as drops smaller than the Immediate threshold that persist across
2+ periods.

### Restricting the Scope

Use `csm_filter` to run alerts for a specific CSM's accounts only. Use `exclude_accounts`
to skip accounts where health score volatility is expected (e.g., new implementations,
accounts in churn management where score may fluctuate intentionally). These can also
be passed as one-off overrides in the invocation prompt.

### Daily vs. Weekly Mode

Daily mode tracks changes between the current run and the prior run's baseline. The
look-back is one period. Weekly mode compares the current run against a baseline from
7 days prior and adds a recovering accounts section. Choose daily for real-time
monitoring; choose weekly for trend visibility and reduced alert fatigue.

### Baseline File Location

The `baseline_file_path` should be on a path that persists between sessions and is
writable by the agent. A hidden directory under the home folder (e.g., `~/.cs-agent/`)
works well. Do not point to a temp directory — baseline loss on the next run will
trigger a silent re-initialization that misses genuine score movements.

---

## Subagent Reference

| Subagent | File | Role |
|----------|------|------|
| Health Reader | `subagents/health-reader.md` | Score retrieval and baseline loading |
| Trend Analyzer | `subagents/trend-analyzer.md` | Movement classification and alert ranking |
| Alert Composer | `subagents/alert-composer.md` | Output formatting, baseline write, and delivery |
