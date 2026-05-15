# Health Score Watcher — Managed Agent Cookbook

**Agent type:** Scheduled orchestrator with 3 subagents  
**Cadence:** Daily (change detection) or weekly (trend summary)  
**Trigger:** Scheduled task or on-demand via `/csm:health-watcher`  
**Output:** Health score change alerts delivered to Slack + saved change log

---

## What This Agent Does

The Health Score Watcher tracks health score movements across your book of business
and surfaces meaningful changes before they become visible problems. Unlike a static
dashboard snapshot, this agent detects directional movement — accounts trending down,
accounts recovering, and accounts with sudden drops that warrant same-day attention.

It reads health score data from your health score source (CRM, dedicated health scoring
tool, or data warehouse), compares current values against a stored baseline, and routes
only the accounts with meaningful change to the alert output. Stable accounts are logged
but not surfaced — the output is signal, not noise.

**Outputs:**
- Immediate alert: accounts with significant health score drops (configured threshold)
- Trend summary: accounts improving, declining, or newly entering risk bands
- Change log: all movements recorded for pattern analysis over time
- Optional: Slack channel post + saved markdown report

---

## Architecture

```
Orchestrator: Health Score Watcher
│
├── Subagent 1: Health Reader
│   Pulls current health scores from configured source (CRM, health tool, or warehouse).
│   Compares against the stored baseline from the previous run.
│   Outputs a delta record per account: current score, previous score, change, band movement.
│
├── Subagent 2: Trend Analyzer
│   Classifies each account's movement by type and severity.
│   Groups accounts into alert tier (immediate), watch tier (monitor), and stable tier.
│   Produces ranked alert list and trend summary.
│
└── Subagent 3: Alert Composer
    Formats the alert output. Generates concise per-account summaries for
    immediate-tier accounts. Produces trend narrative for weekly summaries.
    Delivers to configured output channels (Slack, file, or both).
```

The orchestrator manages baseline persistence — reading the prior run's snapshot and
writing the current run's snapshot to the configured baseline file path. Subagents do
not write to disk; only the orchestrator does.

---

## Orchestrator System Prompt

```
You are the Health Score Watcher orchestrator for a Customer Success team. Your job is
to detect meaningful health score changes across the book of business and route alerts
to the CSM team.

Your configuration lives at:
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md

Read it before starting. Fields you need:
- Health score source: connector name and field paths for health score data
- Alert threshold: minimum point drop that triggers an immediate alert (default: 10 points)
- Band definitions: score ranges that define each health band (red/yellow/green or equivalent)
- Baseline file path: where the prior run's snapshot is stored
- Digest output: Slack channel, file path, or both
- CSM assignments: which CSM owns which accounts (for routing)
- Reporting mode: daily (change detection only) or weekly (full trend summary)

Execution sequence:

STEP 1 — Load baseline
  Read the baseline snapshot from the configured baseline file path.
  If no baseline exists (first run), log that this is an initialization run and proceed.
  On initialization runs, the Health Reader will capture the baseline; no alerts will fire.

STEP 2 — Dispatch Health Reader
  Pass: account ID list, connector name, field paths for health scores, prior baseline data
  Receive: delta records (current score, previous score, change amount, band movement per account)
  Do not proceed to Step 3 until Health Reader returns.

STEP 3 — Dispatch Trend Analyzer
  Pass: full delta record set, alert threshold from config, band definitions
  Receive: tiered account list (immediate / watch / stable) with classification per account

STEP 4 — Dispatch Alert Composer
  Pass: tiered account list, reporting mode (daily/weekly), output targets, CSM assignments
  Receive: formatted alert output (markdown + Slack mrkdwn)

STEP 5 — Persist new baseline
  Write the current run's health scores as the new baseline to the configured baseline
  file path. This is required before delivery — if baseline write fails, surface the
  error and do not proceed silently.

STEP 6 — Deliver output
  If Slack configured: post mrkdwn version to configured channel.
  If file output configured: save markdown version to configured path.
  Confirm delivery.

Rules:
- If the health score source is unavailable, do not run with stale data — surface
  the error and ask the user to run again when the source is accessible.
- If the baseline file cannot be read (corrupted or missing), treat as initialization
  run. Do not fabricate prior scores.
- Health scores are observations, not verdicts. Language: "score dropped from X to Y"
  not "account is deteriorating" or "heading toward churn."
- Accounts with no score change (within ±2 points) are logged in the change log but
  do not appear in the alert output.
- Never include TtV figures or metrics labeled [review — internal planning target]
  in any output.
```

---

## Subagent 1: Health Reader

**File:** `subagents/health-reader.md`

**Role:** Data retrieval and comparison. The Health Reader fetches current health scores
from the configured source, compares each account's score against the baseline, and
returns a delta record for every account in scope.

**Tools required:**
- Health score source connector (CRM custom field, health scoring tool API, or data
  warehouse query) — required
- CRM connector (account list, segment, CSM assignment) — recommended for enrichment

**Inputs from orchestrator:**
- Account ID list
- Connector name and field paths
- Prior baseline data (map of account ID → prior score)

**Output format:**
```
account_id: [ID]
account_name: [name]
csm: [assigned CSM]
segment: [segment]
current_score: [0-100 or tool-native scale]
previous_score: [0-100 or null if first run]
change: [+N / -N / 0 or null if first run]
band_current: [red|yellow|green or tool-native label]
band_previous: [band or null if first run]
band_movement: [none|improved|declined|entered-red|exited-red or null if first run]
data_as_of: [timestamp]
score_source: [connector name]
```

Return one record per account. If the health score source is unavailable for a specific
account (data gap), return a record with `current_score: null` and a note in a
`data_gap_reason` field — do not omit the account.

**Full subagent spec:** See `subagents/health-reader.md`

---

## Subagent 2: Trend Analyzer

**File:** `subagents/trend-analyzer.md`

**Role:** Classification and tiering. The Trend Analyzer takes the delta records from
the Health Reader and classifies each account into an alert tier based on the magnitude
and direction of score change.

**Tools required:** None — works on data passed from orchestrator.

**Tiering logic:**

| Tier | Condition |
|------|-----------|
| **Immediate** | Score dropped ≥ alert threshold (default: 10 points) in one period |
| **Immediate** | Band movement: entered-red (any drop into red band) |
| **Watch** | Score dropped < alert threshold (3–9 points) over 2+ consecutive periods |
| **Watch** | Band movement: declined (yellow → green reversal, or red holding) |
| **Watch** | Score improving: exited-red or consistent positive movement 3+ periods |
| **Stable** | Change within ±2 points; no band movement |

For **weekly mode**, trend is calculated across the full period snapshot-over-snapshot,
not intraday. Accounts improving for 2+ consecutive weekly periods are surfaced in a
"recovering" group.

**Output format:**
```
immediate_tier:
  - account_id: [ID]
    account_name: [name]
    csm: [name]
    segment: [segment]
    score_change: [−N or +N]
    current_score: [score]
    previous_score: [score]
    band_movement: [description]
    recommended_action: [1-sentence specific action]

watch_tier:
  - [same fields, no recommended_action — watch tier requires CSM judgment]

stable_tier_count: [N]
recovering_count: [N — weekly mode only]

portfolio_summary:
  total_accounts: [N]
  immediate_count: [N]
  watch_count: [N]
  stable_count: [N]
  avg_score_this_period: [X.X]
  avg_score_prior_period: [X.X]
  net_portfolio_movement: [+N / -N]
```

**Full subagent spec:** See `subagents/trend-analyzer.md`

---

## Subagent 3: Alert Composer

**File:** `subagents/alert-composer.md`

**Role:** Output formatting and delivery preparation. The Alert Composer takes the
Trend Analyzer's tiered account list and formats it for delivery.

**Tools required:**
- Slack connector (if Slack output configured)

**Output format (markdown version):**

```markdown
## Health Score Alert — [date]
*[N] accounts monitored · [reporting mode] · Generated by Claude Health Watcher*

---

### 🔴 Immediate Attention ([N] accounts)

**[Account Name]** · [Segment] · CSM: [Name]
- Score: [previous] → [current] ([change])
- [Band movement if applicable: "entered red band"]
**Recommended action:** [Specific next step]

---

### 🟡 Watch ([N] accounts)

**[Account Name]** · [Segment] · CSM: [Name]
- Score: [previous] → [current] ([change])
- [Trend note: "3rd consecutive weekly decline" or "recovering — 2nd straight week up"]

---

### Portfolio Movement
| | This period | Prior period | Change |
|---|---|---|---|
| Avg portfolio score | [X.X] | [X.X] | [±N] |
| Immediate alerts | [N] | [N] | [↑/↓/=] |
| Watch accounts | [N] | [N] | [↑/↓/=] |
| Stable | [N] | [N] | [↑/↓/=] |

*Source: [health score connector] · Data as of [timestamp]*
*Baseline: [prior run timestamp]*
```

**Guardrails for Composer:**
- Do not characterize score movements as "declining health" or "deteriorating" —
  state the numerical movement and let the CSM interpret
- Do not include accounts in the alert output that changed < 3 points (log only)
- Weekly mode: include a "recovering" section between Watch and Portfolio if any
  accounts are on a 2+ period improvement trend — this is positive signal
- If zero immediate-tier accounts: open with "No immediate alerts this period"
  before the Watch section
- Keep per-account summaries to the score movement and one contextual note max —
  the Alert Composer is not a diagnostic tool

**Full subagent spec:** See `subagents/alert-composer.md`

---

## Connector Requirements

| Connector | Required | Purpose |
|-----------|----------|---------|
| Health score source (CRM, Gainsight, Totango, ChurnZero, etc.) | Yes | Current health scores |
| CRM (HubSpot, Salesforce, etc.) | Recommended | Account list, segment, CSM assignment |
| Slack | Optional | Alert channel delivery |

This agent is designed to work with any health score system that is accessible via MCP
connector. The health score field path and scale (0–100, letter grade, red/yellow/green)
are configured in `../../csm/CLAUDE.md` rather than hardcoded.

If no health score connector is available but the CSM maintains a manual score in the
CRM as a custom field, configure that field path and the agent will read from it.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Required config fields:
- `health_score_source`: Connector name and field path to health score data
- `health_score_scale`: Score range (e.g., `0-100`) and band boundaries
- `alert_threshold`: Minimum drop (in points or percent) that triggers immediate alert
- `baseline_file_path`: Where to persist the prior-run snapshot
- `digest_output`: `file` | `slack` | `both`
- `reporting_mode`: `daily` | `weekly`

Optional config fields:
- `slack_channel`: Required if output includes Slack
- `digest_file_path`: Required if output includes file
- `exclude_accounts`: Account IDs to omit from monitoring
- `csm_filter`: Run only for accounts assigned to a specific CSM

If required fields are `[PLACEHOLDER]`, prompt:
> "Run `/csm:cold-start-interview --section health` to configure the Health Score
> Watcher before running this agent."

---

## Baseline Persistence

The Health Watcher maintains a baseline snapshot file between runs. This is a JSON
file at `baseline_file_path` that stores:

```json
{
  "run_timestamp": "2026-05-13T07:02:00Z",
  "accounts": {
    "account-id-001": { "score": 72, "band": "yellow" },
    "account-id-002": { "score": 88, "band": "green" }
  }
}
```

On first run (no baseline file exists):
- Log that this is an initialization run
- Capture current scores as the baseline
- Do not fire any alerts
- Notify: "Health Watcher initialized. [N] accounts baselined. Alerts will fire
  on the next run."

---

## Scheduling

```
Daily alerts at 8:00 AM (change detection):
  cronExpression: "0 8 * * *"
  prompt: "Run the Health Score Watcher for today."

Weekly trend summary every Monday at 8:30 AM:
  cronExpression: "30 8 * * 1"
  prompt: "Run the weekly Health Score Watcher."
```

---

## Sample Output (abbreviated)

```
## Health Score Alert — May 13, 2026
*52 accounts monitored · daily · Generated by Claude Health Watcher*

### 🔴 Immediate Attention (1 account)

**Meridian Labs** · Enterprise · CSM: Priya Sharma
- Score: 71 → 54 (−17)
- Entered yellow band
**Recommended action:** Review account activity log before EOD; check for open support
tickets or recent executive changes that may explain the drop.

### 🟡 Watch (3 accounts)

**Crestwood Analytics** · Mid-Market · CSM: Daniel Flores
- Score: 68 → 63 (−5)
- 2nd consecutive weekly decline

**LoopStack Inc.** · SMB · CSM: Sarah Chen
- Score: 41 → 48 (+7)
- Recovering — 2nd straight week up

**Nora Systems** · Mid-Market · CSM: James Park
- Score: 74 → 70 (−4)

### Portfolio Movement
| | This period | Prior period | Change |
|---|---|---|---|
| Avg portfolio score | 72.4 | 73.8 | −1.4 |
| Immediate alerts | 1 | 0 | ↑1 |
| Watch accounts | 3 | 2 | ↑1 |
| Stable | 48 | 50 | ↓2 |

*Source: Gainsight MCP · Data as of 2026-05-13 08:01 UTC*
*Baseline: 2026-05-12 08:01 UTC*
```
