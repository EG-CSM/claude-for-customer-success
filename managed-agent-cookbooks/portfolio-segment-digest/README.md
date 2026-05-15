# Portfolio Segment Digest — Deployment & Configuration Guide

## What This Agent Does

`portfolio-segment-digest` runs on a weekly Monday schedule and produces a
segment-level health roll-up for CS Ops, Head of CS, and CRO audiences. It
pulls current health distributions across all configured segments, compares
them against last week's baseline, and surfaces meaningful distribution
shifts, ARR at risk by segment, capacity coverage gaps, and top at-risk
accounts per segment.

This agent operates at the portfolio layer — it tells you whether segments
are shifting, not which individual accounts to call. Account-level alerting
lives in `health-watcher` and `churn-signal-digest`.

---

## Architecture

```
portfolio-segment-digest (orchestrator)
│
├── Step 1: Read cs-ops/CLAUDE.md + company-profile.md
│           (stops if [PLACEHOLDER] markers found)
│
├── Step 2: Load baseline snapshot from baseline_file_path
│           (first-run initialization if no baseline exists)
│
├── Step 3: Segment Data Puller
│           Pulls all accounts from CRM + CS Platform
│           → per-account records (ID, segment, ARR, health tier, CSM)
│           → grouped into segment-level collections
│           [empty-set guard — stops if zero accounts returned]
│
├── Step 4a: Distribution Analyzer
│            Computes per-segment distributions
│            → band counts and ARR totals (Red / Yellow / Green)
│            → WoW band shifts, at-risk account lists
│            → capacity coverage flags per segment
│
├── Step 4b: Portfolio Summarizer
│            Computes cross-segment roll-ups
│            → cross-segment comparison table (ranked by Red ARR)
│            → portfolio-level totals (all segments combined)
│
├── Step 5: Report Composer
│           Formats markdown + Slack mrkdwn output
│           → applies first-run or standard format based on baseline flag
│
├── Step 6: Write updated baseline to baseline_file_path
│           (required before delivery — stops if write fails)
│
└── Step 7: Deliver
            → Slack: CS Ops channel (if configured)
            → File: portfolio-segment-digest-YYYY-MM-DD.md
```

---

## Baseline Persistence

**Format:** JSON file at `baseline_file_path` from cs-ops config.

```json
{
  "run_timestamp": "2025-10-21T07:02:14Z",
  "segments": {
    "enterprise": {
      "account_count": 84,
      "red_pct": 14.3,
      "yellow_pct": 22.6,
      "green_pct": 63.1,
      "arr_at_risk": 4200000
    },
    "mid_market": { ... },
    "smb": { ... }
  }
}
```

**Write timing:** Baseline is written after all subagents complete (Step 6),
before delivery (Step 7). If the write fails, the agent surfaces the error
and does not proceed silently.

**First run:** If no baseline file exists, the agent initializes — no
week-over-week columns or shift flags are included; current distributions
are written as the new baseline; a first-run summary is posted instead of
the standard digest format.

**Corrupted baseline:** If the baseline file is present but cannot be parsed
(corrupted, truncated, or schema mismatch), the agent treats this as a first
run and logs: "Baseline file could not be read — initializing fresh. Prior
week-over-week data unavailable."

---

## Prerequisites

### Required connectors

| Connector | Use |
|-----------|-----|
| CRM (e.g., HubSpot, Salesforce) | Account records: account ID, segment, ARR, CSM assignment |
| CS Platform (e.g., Gainsight, Totango, ChurnZero) | Health score or health tier by account ID |

### Optional connectors

| Connector | Use |
|-----------|-----|
| Slack | Post mrkdwn digest to CS Ops channel |

If the CRM or CS Platform connector is unavailable at run time, the agent
stops and surfaces the error — it does not run on stale or partial data.

---

## Configuration

All configuration lives in `../../cs-ops/CLAUDE.md`. Run `/cs-ops:cold-start-interview`
to complete setup if the file contains `[PLACEHOLDER]` markers.

### Required fields

| Field | Description |
|-------|-------------|
| `segment_definitions` | Named segments with membership criteria (e.g., ARR range, industry) |
| `health_band_definitions` | Red / Yellow / Green boundaries and score scale |
| `capacity_targets` | Accounts-per-CSM target by segment |
| `crm_connector` | Connector name and field paths (account ID, segment, ARR, CSM) |
| `cs_platform_connector` | Connector name and field paths (health score or tier by account ID) |
| `baseline_file_path` | Full path to the baseline JSON file |
| `slack_output_channel` | CS Ops Slack channel ID or name |
| `file_output_path` | Directory for markdown file output |

### Optional fields

| Field | Default | Description |
|-------|---------|-------------|
| `at_risk_account_limit` | 5 | Max at-risk accounts listed per segment |
| `red_shift_threshold_pp` | 5 | Minimum Red % increase (percentage points) to flag as meaningful shift |
| `health_refresh_cadence` | weekly | Used to warn if current data may not reflect the latest refresh |
| `health_data_owner` | — | Name or role shown in data freshness warnings |
| `reporting_cadence` | `0 7 * * 1` | Cron schedule for this agent |

### Escalation matrix

Each segment should have an escalation path in the cs-ops config. Capacity
flags in the digest will reference this matrix. If no escalation path is
configured for a segment, the capacity flag will read "escalation path not
configured — update cs-ops/CLAUDE.md".

---

## Scheduling

**Default:** Weekly on Monday at 7:00 AM — ahead of CS leadership standup.

```json
{
  "cronExpression": "0 7 * * 1",
  "prompt": "Run the portfolio segment digest.",
  "agentPath": "cs-ops/agents/portfolio-segment-digest.md"
}
```

**On-demand triggers:** Use any of these phrases to trigger manually:
- "Run portfolio digest"
- "Segment health report"
- "Weekly segment rollup"
- "Run portfolio segment digest"

---

## Output Reference

### Standard output (with prior baseline)

| Section | Content |
|---------|---------|
| Header | Date, segment count, account count |
| Reviewer note | Sources, data timestamp, account count, flags |
| Portfolio Summary | WoW table: accounts in Red, ARR at risk, entered/exited Red |
| Segment Breakdown (×N) | Per-segment band table, ARR at risk, capacity status, shift flag if triggered, top at-risk accounts |
| Cross-Segment Comparison | All segments ranked by Red ARR at risk descending |
| Footer | Connector sources, baseline timestamp, managed-by line |

### First-run output (no prior baseline)

Omits Portfolio Summary table, WoW columns, and distribution shift flags.
Lists each segment with current band percentages. States that WoW
comparisons begin on next run.

### Output files

| Output | Location |
|--------|----------|
| Slack post | Configured CS Ops channel (mrkdwn) |
| Markdown file | `{file_output_path}/portfolio-segment-digest-YYYY-MM-DD.md` |

---

## Data Gap Behavior

| Situation | Behavior |
|-----------|----------|
| CRM connector unavailable | Stop — surface error; do not run with partial data |
| CS Platform connector unavailable | Stop — surface error; do not run with stale health data |
| Zero accounts returned | Stop — log empty-set message; do not dispatch downstream subagents |
| Account with null/zero ARR | Exclude from ARR calculations; log count of excluded accounts |
| Baseline missing | Initialize (first-run mode) |
| Baseline corrupted | Initialize (first-run mode); log warning |
| Health data not refreshed | Warn prominently with last refresh date and data owner |
| Internal planning target metric | Include in file output only (not Slack) |

---

## Customization

**Custom segment definitions:** Update `segment_definitions` in cs-ops/CLAUDE.md.
The Distribution Analyzer will apply the configured band thresholds to each segment
independently.

**Shift threshold:** Increase or decrease `red_shift_threshold_pp` to tune
sensitivity. Default 5pp catches meaningful movement without over-alerting on
normal weekly variance.

**At-risk account limit:** Increase `at_risk_account_limit` for larger segments.
Default 5 keeps the digest scannable in Slack.

**Schedule:** Update `reporting_cadence` in cs-ops/CLAUDE.md. Use cron syntax.

---

## Subagent Reference

| File | Role |
|------|------|
| `subagents/segment-data-puller.md` | Pulls all accounts from CRM + CS Platform and groups them by segment |
| `subagents/distribution-analyzer.md` | Computes per-segment band distributions, WoW shifts, capacity flags, and at-risk account lists |
| `subagents/portfolio-summarizer.md` | Computes cross-segment comparison table and portfolio-level totals |
| `subagents/report-composer.md` | Formats output in markdown and Slack mrkdwn; applies first-run or standard template |

---

## What This Agent Does NOT Do

- Alert on individual accounts — use `health-watcher` or `churn-signal-digest`
- Diagnose why a segment's distribution shifted — it surfaces movement; investigation is a human task
- Modify health scores, account records, CSM assignments, or any system data
- Execute TARO plays or send customer-facing communications
- Run without current connector data — stops and surfaces the error
- Replace capacity planning — capacity notes are flags, not analyses; use `/cs-ops:capacity-planner`
