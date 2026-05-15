# Renewal Scanner — Deployment & Configuration Guide

## What This Agent Does

The Renewal Scanner runs weekly (or on-demand) and produces a prioritized renewal brief
for all accounts renewing within a configurable look-ahead window (default: 90 days). It
classifies each account as red, yellow, green, or insufficient data, surfaces expansion
signals alongside risk, and delivers the brief as a markdown file and/or a Slack message.

The brief is designed for the CS leadership standup or weekly renewal meeting — not for
account-level CSM work. It answers: "Which renewals need attention this week, which are
safe, and where is expansion opportunity?"

**Outputs:**
- Markdown brief: red-tier accounts with full signal detail and recommended actions,
  yellow-tier with signals, green-tier as a compact list, expansion opportunities section,
  and a pipeline summary table
- Optional Slack delivery: mrkdwn version posted to a configured channel
- Data provenance: sources used, unavailable connectors, and unverified dates flagged

---

## Architecture

```
Orchestrator: Renewal Scanner
│
├── Subagent 1: Pipeline Puller
│   Pulls all accounts renewing within the look-ahead window from CRM.
│   Returns a pipeline record per account with ARR, renewal date, CSM/AE
│   assignment, segment, and available health signals.
│
├── Subagent 2: Risk & Expansion Classifier
│   Classifies each account as red/yellow/green/insufficient_data using
│   configured signal weights. Detects expansion signals. Returns a
│   ranked pipeline with recommended actions per account.
│
└── Subagent 3: Renewal Brief Composer
    Formats the classified pipeline into the weekly brief. Delivers
    markdown output and optional Slack message. Calls no data connectors
    except Slack for delivery.
```

---

## Prerequisites

### Required Connectors

| Connector | Role |
|-----------|------|
| CRM (HubSpot, Salesforce, etc.) | Pipeline data, renewal dates, ARR, CSM/AE assignments, health signals |

### Optional Connectors

| Connector | Role |
|-----------|------|
| Slack | Delivery of the mrkdwn brief to a channel |
| Health score platform | Gainsight, Totango, ChurnZero, or similar — if health scores are not in CRM |

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`

Run `/csm:cold-start-interview --section renewals` to configure this file if it
contains `[PLACEHOLDER]` values.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `crm_connector` | CRM MCP connector name | `hubspot-mcp` |
| `look_ahead_window_days` | Days forward to include renewals | `90` |
| `output_path` | Where to save the markdown brief | `~/renewal-briefs/` |
| `digest_output` | `file` \| `slack` \| `both` | `both` |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `slack_channel` | Slack channel for delivery (required if digest_output includes `slack`) | — |
| `health_score_source` | Connector name for health scores, or `crm` to use CRM custom fields | `crm` |
| `risk_signal_weights` | Override default signal weights per signal type | built-in defaults |
| `expansion_signals` | Configure which signals trigger expansion flagging | built-in defaults |
| `csm_filter` | Restrict scan to accounts owned by a specific CSM | all CSMs |
| `segment_filter` | Restrict scan to a segment (Enterprise, Mid-Market, SMB) | all segments |

### Default Signal Weights

If `risk_signal_weights` is not configured, the classifier uses these defaults:

| Signal Type | Default Weight |
|-------------|---------------|
| Health score drop ≥ 15 points | High |
| Support P1 ticket open | High |
| Contract value change flagged in CRM | High |
| CRM note tagged as escalation | High |
| Executive contact gap > 45 days | Medium |
| Login volume decline > 30% over 30 days | Medium |
| NPS score ≤ 5 (most recent response) | Medium |
| No CRM activity logged in 30 days | Low |

---

## Scheduling

### Recommended: Weekly Monday Morning

```
cronExpression: "0 7 * * 1"
prompt: "Run the renewal scanner for this week."
```

Delivers the brief before the Monday renewal standup.

### Alternative: Friday End of Day

```
cronExpression: "0 16 * * 5"
prompt: "Run the renewal scanner for the upcoming week."
```

Prepares the brief before the weekend for Monday review.

### On-Demand Invocation

Trigger at any time with natural language. See `steering-examples.json` for the full
prompting pattern library. Common invocations:

- "Run the renewal scanner."
- "Give me this week's renewal brief."
- "Scan renewals for the next 90 days."
- "Which accounts renewing soon need attention?"

---

## Output Reference

### Brief Section Order (fixed — never reordered)

| Section | Contents | Format |
|---------|----------|--------|
| Header | Date, account counts, generation note | Header block |
| 🔴 Immediate Attention | Red-tier accounts: all signals, recommended action, AE involvement | Full per-account block |
| 🟡 Monitor Closely | Yellow-tier accounts: signals, recommended action, AE involvement | Full per-account block |
| 🟢 On Track | Green-tier accounts: name, segment, CSM, ARR, days to renewal | One line per account |
| ⚪ Insufficient Data | Accounts with no classifiable health data | One line per account; omitted if count = 0 |
| ⚡ Expansion Opportunities | Accounts with strong or moderate expansion signals | Per-account block with evidence |
| Pipeline Summary | Counts and ARR by tier; data provenance footnotes | Table |

Sections with zero accounts are omitted from the body. The Pipeline Summary always
renders, including zero-count tiers.

### Inline Data Flags

The brief uses two inline flags for unverified data:

- `[date unverified]` — renewal date could not be confirmed from CRM
- `[ARR unverified]` — ARR value flagged as unverified; omitted from ARR totals

### Slack Delivery Details

When `digest_output: slack` or `both`:
- Posts mrkdwn version to `slack_channel`
- If the brief exceeds 3,000 characters, splits into two sequential messages
  (message 1: red + yellow + header; message 2: green + expansion + summary)
- Slack delivery failure does not halt markdown output; failure is noted in delivery status

---

## Data Gap Behavior

| Situation | Behavior |
|-----------|----------|
| CRM unavailable | Halt immediately — no brief produced; error surfaced to orchestrator |
| Health score connector unavailable | Continue; affected accounts classified as `insufficient_data` |
| Slack connector unavailable | Complete markdown; note Slack failure in delivery status |
| Renewal date not found in CRM | Flag `[date unverified]`; include account in brief |
| ARR not found in CRM | Flag `[ARR unverified]`; omit from ARR totals |
| No accounts in look-ahead window | Brief renders with a "no accounts renewing within [N] days" note; pipeline summary shows all zeros |

---

## Customization

### Adjusting the Look-Ahead Window

Change `look_ahead_window_days` in config. 90 days is standard for most CS teams.
Enterprise-heavy books with longer renewal cycles may prefer 120 days.

### Tuning Signal Weights

Modify `risk_signal_weights` in config. Valid weights: `high`, `medium`, `low`, `ignore`.
Setting a signal to `ignore` excludes it from classification entirely. Changes take effect
on the next run — no restart required.

### Restricting the Scan

Use `csm_filter` or `segment_filter` to run the agent for a subset of the portfolio.
Useful when CSMs operate independently or for segment-specific leadership reviews.
These can also be passed as one-off overrides in the invocation prompt without
changing config.

### CSM and AE Assignment Overrides

If CRM assignments are stale or missing for specific accounts, add `csm_assignments`
and `ae_assignments` maps to the orchestrator config. These override null values from
CRM for display in the brief without modifying CRM records.

---

## Subagent Reference

| Subagent | File | Role |
|----------|------|------|
| Pipeline Puller | `subagents/pipeline-puller.md` | CRM data retrieval |
| Risk & Expansion Classifier | `subagents/risk-expansion-classifier.md` | Classification and scoring |
| Renewal Brief Composer | `subagents/renewal-brief-composer.md` | Output formatting and delivery |
