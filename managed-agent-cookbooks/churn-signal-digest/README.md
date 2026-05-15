# Churn Signal Digest — Deployment & Configuration Guide

## What This Agent Does

The Churn Signal Digest runs daily or weekly and produces a prioritized digest of churn
risk signals across the configured account portfolio. It pulls raw activity, usage, and
sentiment data from connected platforms, classifies each account by signal severity, and
delivers a digest that surfaces the accounts most likely to need attention before the
next check-in.

The digest is designed for daily or weekly CS team scanning — not for account-level
strategy work. It answers: "Which accounts had signals fire since the last run, and
how urgent are they?"

**Outputs:**
- Ranked digest: P1 accounts (immediate attention) with full signal blocks and
  recommended actions, P2 accounts (monitor closely) with signals and actions,
  P3 accounts (watch) with a brief bullet summary only
- Portfolio Summary table: account counts by severity with period-over-period change
- Optional Slack delivery: mrkdwn version posted to a configured channel
- Data provenance: sources used, unavailable connectors noted

---

## Architecture

```
Orchestrator: Churn Signal Digest
│
├── Subagent 1: Signal Collector
│   Pulls raw activity and metric data from each configured connector for
│   every account in scope. Returns one signal record per account. Does not
│   classify or score — returns raw values only.
│
├── Subagent 2: Signal Analyzer
│   Receives the full signal record set and classifies each account as P1,
│   P2, P3, or no signal using configured signal weights. Returns a ranked
│   list with signal details and recommended actions per account.
│
└── Subagent 3: Digest Composer
    Formats the classified signal list into the digest. Delivers the
    markdown output and optional Slack message. Calls no data connectors
    except Slack for delivery.
```

---

## Prerequisites

### Required Connectors

| Connector | Role |
|-----------|------|
| CRM (HubSpot, Salesforce, etc.) | Account list, CSM assignments, activity history, exec contact dates |

### Optional Connectors

| Connector | Role |
|-----------|------|
| Support platform | Open tickets, P1 count, ticket age |
| Product usage platform | Login counts, feature adoption score |
| NPS / CSAT platform | Most recent sentiment scores |

A CRM-only configuration is valid. Adding optional connectors expands the signal set
and reduces the number of accounts classified as insufficient data.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Run `/csm:cold-start-interview --section churn-signals` to configure this file if it
contains `[PLACEHOLDER]` values.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `crm_connector` | CRM MCP connector name | `hubspot-mcp` |
| `account_scope` | Which accounts to include | `all` \| `csm_owned` \| `segment:Enterprise` |
| `digest_output` | `file` \| `slack` \| `both` | `both` |
| `slack_channel` | Slack channel for delivery (required if digest_output includes `slack`) | `#cs-signals` |
| `digest_file_path` | Where to save the markdown digest | `~/cs-digests/churn/` |
| `reporting_period` | How frequently the agent runs | `daily` \| `weekly` |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `signal_weights` | Override default severity thresholds per signal type | built-in defaults |
| `csm_assignments` | Override null CRM assignments for specific accounts | — |
| `exclude_accounts` | Account IDs to exclude from the scan | — |

### Default Signal Weights

If `signal_weights` is not configured, the classifier uses these defaults:

| Signal Type | P1 Threshold | P2 Threshold |
|-------------|-------------|-------------|
| Health score drop | ≥ 15 points | 8–14 points |
| P1 support ticket open | Any | — |
| No CRM activity | > 30 days | 21–30 days |
| Exec contact gap | > 45 days | 31–44 days |
| Login volume decline | > 50% over 30 days | 25–50% |
| NPS score | ≤ 4 | 5–6 |
| Feature adoption drop | > 25 points | 10–24 points |

Signal severity classification:
- **P1** — Any signal at or above P1 threshold
- **P2** — Any signal at P2 threshold, or two or more medium signals co-occurring
- **P3** — A single medium signal below P2 threshold

---

## Scheduling

### Recommended: Daily Morning

```
cronExpression: "0 7 * * *"
prompt: "Run the churn signal digest."
```

Delivers the digest before the CS team's daily standup.

### Alternative: Weekly Monday Morning

```
cronExpression: "30 7 * * 1"
prompt: "Run the weekly churn signal digest."
```

Delivers a weekly summary with trend comparison against the prior period.

### On-Demand Invocation

Trigger at any time with natural language. See `steering-examples.json` for the full
prompting pattern library. Common invocations:

- "Run the churn signal digest."
- "What signals fired since yesterday?"
- "Show me this week's churn signals for Enterprise accounts."

---

## Output Reference

### Digest Section Order (fixed — never reordered)

| Section | Contents | Format |
|---------|----------|--------|
| Header | Date, run period, account counts, generation note | Header block |
| 🔴 P1 — Immediate Attention | All P1 accounts: full signal block, recommended action | Per-account block |
| 🟡 P2 — Monitor Closely | All P2 accounts: signal block, recommended action | Per-account block |
| 🟢 P3 — Watch | All P3 accounts: bullet summary only, no recommended action | Brief list |
| Portfolio Summary | Counts by tier with period-over-period change column | Table |

Sections with zero accounts are omitted from the body (except Portfolio Summary, which
always renders). When there are zero P1 accounts, the digest opens with:

> No P1 signals this period.

immediately before the P2 section.

### Per-Account Format

**P1 and P2 accounts — full block:**
```
**[Account Name]** · [Segment or —] · CSM: [Name or —]
- [Signal type]: [observed value]
- [Additional signals if any]
**Recommended action:** [One sentence]
```

**P3 accounts — brief list (no recommended action):**
```
[Account Name] · CSM: [Name or —] · [Signal type]: [observed value]
```

At most three signals are shown per account (highest-weight first). Additional signals
are noted as "+ N more" if present.

### Period-Over-Period Change

The Portfolio Summary includes a "vs. last period" column showing whether each tier's
count increased, decreased, or held steady since the prior run. When the prior run's
data is unavailable (e.g., first run after setup), this column renders as `—`.

### Inline Data Flags

- `[data unavailable]` — one or more connectors failed; the account may have additional
  signals not captured in this run

---

## Data Gap Behavior

| Situation | Behavior |
|-----------|----------|
| CRM unavailable | Halt immediately — no digest produced; error surfaced to orchestrator |
| Support connector unavailable | Continue; support signals omitted; affected accounts flagged |
| Product connector unavailable | Continue; usage signals omitted; affected accounts flagged |
| NPS connector unavailable | Continue; sentiment signals omitted; affected accounts flagged |
| Account not found in CRM | Include with `crm_data_available: false` note; omit from signal analysis |
| No signals for an account | Account is not included in the digest body; counted in portfolio total |
| Zero P1 accounts | Digest renders with "No P1 signals this period" header; P2 section follows |
| All accounts show no signals | Digest renders with all-clear note; portfolio summary shows counts |

---

## Customization

### Adjusting Signal Weights

Modify `signal_weights` in config. Valid severity values: `p1_threshold`, `p2_threshold`,
`medium`, `low`, `ignore`. Setting a signal to `ignore` excludes it from classification.
Changes take effect on the next run.

### Restricting the Scan

Use `account_scope` to restrict the population: `all`, `csm_owned`, `segment:Enterprise`,
`segment:Mid-Market`, `segment:SMB`. Use `exclude_accounts` to skip specific accounts
(e.g., accounts in implementation where early signals are expected). These can also be
passed as one-off overrides in the invocation prompt.

### Daily vs. Weekly Mode

The `reporting_period` setting controls the date window used for signal collection
(7 days for daily, 30 days for weekly) and the Portfolio Summary format. Weekly mode
includes period-over-period trend comparison. Daily mode is suitable for real-time
signal monitoring; weekly mode is better for trend analysis and team reporting.

---

## Subagent Reference

| Subagent | File | Role |
|----------|------|------|
| Signal Collector | `subagents/signal-collector.md` | Raw data retrieval from all connectors |
| Signal Analyzer | `subagents/signal-analyzer.md` | Signal classification and ranking |
| Digest Composer | `subagents/digest-composer.md` | Output formatting and delivery |
