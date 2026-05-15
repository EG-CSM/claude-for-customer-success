# Churn Signal Digest — Managed Agent Cookbook

**Agent type:** Scheduled orchestrator with 3 subagents  
**Cadence:** Daily or weekly (user-configured)  
**Trigger:** Scheduled task or on-demand via `/csm:churn-signal-digest`  
**Output:** Structured churn-risk digest delivered to Slack channel or saved as a report file

---

## What This Agent Does

The Churn Signal Digest agent monitors your full book of business for emerging churn risk
signals and produces a ranked, actionable digest. It is not a replacement for your health
score system — it is a signal aggregator that spans sources your dashboard probably doesn't
combine: CRM activity logs, support ticket volume, product usage gaps, and NPS/CSAT trends.

Run it daily for early warning. Run it weekly for a synthesized view ahead of team standups.

**Outputs:**
- Ranked list of accounts by churn signal severity (P1/P2/P3)
- Per-account signal summary: what signals fired, why they matter, recommended next action
- Portfolio summary: how many accounts are signaling vs. last period
- Optional: Slack message to a configured channel + saved markdown report

---

## Architecture

```
Orchestrator: Churn Signal Digest
│
├── Subagent 1: Signal Collector
│   Pulls raw data from CRM, support, product usage, and feedback connectors.
│   Outputs structured signal records per account.
│
├── Subagent 2: Signal Analyzer  
│   Classifies each signal by type and severity. Applies configurable
│   signal weights from csm-profile.md. Produces ranked account list.
│
└── Subagent 3: Digest Composer
    Formats the final digest. Generates per-account summaries and portfolio
    rollup. Delivers to configured output channels (file, Slack, both).
```

The orchestrator sequences the subagents, passes data between them, and handles output
delivery. It does not analyze signals itself — that is the Analyzer's job.

---

## Orchestrator System Prompt

```
You are the Churn Signal Digest orchestrator for a Customer Success team. Your job is
to coordinate three subagents to produce a churn-risk digest across the full book of
business.

Your configuration lives at:
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md

Read it before starting. Fields you need:
- CRM connector name and account scope
- Support connector (if configured)
- Product usage connector (if configured)
- Churn signal weights (if configured; use defaults if not)
- Digest output: Slack channel, file path, or both
- CSM names mapped to their accounts (for routing)

Execution sequence:

STEP 1 — Dispatch Signal Collector
  Pass: list of account IDs from CRM scope, connector names, today's date
  Receive: raw signal records (one per account × signal type)
  Do not proceed to Step 2 until Signal Collector returns a complete response.

STEP 2 — Dispatch Signal Analyzer
  Pass: the full signal record set from Step 1
  Receive: ranked account list with per-account severity rating (P1/P2/P3/none)
    and signal classification
  Do not proceed to Step 3 until Analyzer returns.

STEP 3 — Dispatch Digest Composer
  Pass: ranked account list + signal classifications + config (output targets,
    CSM assignments, reporting period)
  Receive: formatted digest text (markdown + Slack mrkdwn versions)

STEP 4 — Deliver output
  If Slack configured: post the mrkdwn version to the configured channel.
  If file output configured: save the markdown version to the configured path.
  Confirm delivery in your final response.

Rules:
- If any subagent fails, surface the error immediately. Do not proceed with
  incomplete data.
- If no CRM connector is available, ask the user to provide a CSV of account
  names and CSM assignments before running.
- If a configured connector is unavailable (rate limited, auth error), note it
  in the digest header — do not silently drop signals from that source.
- Never present churn signals as confirmed churn — they are signals that warrant
  attention. Language: "signaling risk" not "churning" or "at risk of churning."
- TtV figures, internal benchmarks, or any metric labeled [review — internal
  planning target] must not appear in the digest output.
```

---

## Subagent 1: Signal Collector

**File:** `subagents/signal-collector.md`

**Role:** Data retrieval only. The Signal Collector pulls raw activity and metric data
from each configured connector and returns a structured signal record for each account.
It does not classify, weight, or interpret — it gathers.

**Tools required:**
- CRM connector (account list, activity log, last contact date)
- Support connector (open ticket count, ticket age, severity breakdown) — optional
- Product usage connector (login frequency, feature adoption, DAU/MAU) — optional
- NPS/CSAT connector (recent scores, trend direction) — optional

**Inputs from orchestrator:**
- Account ID list
- Connector names
- Date range (default: last 7 days for daily digest, last 30 days for weekly)

**Output format:**
```
account_id: [ID]
account_name: [name]
csm: [assigned CSM name]
segment: [segment]
signals:
  crm:
    last_activity_date: [date or null]
    open_opportunities: [count]
    exec_contact_gap_days: [N or null]
  support:
    open_tickets: [count]
    avg_ticket_age_days: [N or null]
    p1_tickets: [count]
  product:
    logins_last_7d: [count or null]
    logins_last_30d: [count or null]
    feature_adoption_score: [0-100 or null]
  feedback:
    last_nps_score: [0-10 or null]
    last_nps_date: [date or null]
    last_csat_score: [0-5 or null]
data_as_of: [timestamp]
connectors_used: [list]
connectors_unavailable: [list or empty]
```

Return one record per account. Return all accounts, including those with no signals —
the Analyzer needs the full set to produce accurate portfolio statistics.

**Full subagent spec:** See `subagents/signal-collector.md`

---

## Subagent 2: Signal Analyzer

**File:** `subagents/signal-analyzer.md`

**Role:** Classification and prioritization. The Signal Analyzer takes the raw signal
records from the Collector and applies configurable signal weights to produce a severity
rating for each account.

**Tools required:** None — this subagent works on data passed from the orchestrator.

**Signal classification logic:**

| Signal | Default weight | P1 threshold | P2 threshold |
|--------|---------------|-------------|-------------|
| No CRM activity in 14+ days | High | 21+ days | 14–20 days |
| No exec contact in 30+ days (Enterprise) | High | 45+ days | 30–44 days |
| Open P1 support ticket | Critical | Any P1 | — |
| 3+ open tickets, any severity | Medium | 5+ tickets | 3–4 tickets |
| Login frequency drop >50% WoW | High | >70% drop | 50–70% drop |
| Feature adoption score < 30 | Medium | <20 | 20–30 |
| NPS score ≤ 6 (detractor) | High | ≤4 | 5–6 |
| CSAT score < 3 | High | <2 | 2–3 |

Severity assignment (per account):
- **P1 — Immediate attention:** Any P1-threshold signal present
- **P2 — Monitor closely:** Any P2-threshold signal, or 2+ medium signals
- **P3 — Watch:** Single medium signal
- **None:** No signals present

**Output format:**
```
ranked_accounts:
  - account_id: [ID]
    account_name: [name]
    csm: [name]
    segment: [segment]
    severity: [P1|P2|P3|None]
    signal_count: [N]
    top_signals:
      - type: [signal type]
        value: [observed value]
        threshold: [threshold that fired]
        weight: [High|Medium|Critical]
    recommended_action: [1-sentence specific action for the CSM]
    
portfolio_summary:
  total_accounts: [N]
  p1_count: [N]
  p2_count: [N]
  p3_count: [N]
  no_signal_count: [N]
  period: [date range]
```

**Full subagent spec:** See `subagents/signal-analyzer.md`

---

## Subagent 3: Digest Composer

**File:** `subagents/digest-composer.md`

**Role:** Output formatting and delivery preparation. The Digest Composer takes the
Analyzer's ranked account list and formats it into the final digest — both a markdown
version for file output and a Slack mrkdwn version for channel posting.

**Tools required:**
- Slack connector (if Slack output configured) — for posting the digest

**Output format (markdown version):**

```markdown
## Churn Signal Digest — [date]
*[N] accounts monitored · Generated by Claude Churn Signal Agent*

---

### 🔴 P1 — Immediate Attention ([N] accounts)

**[Account Name]** · [Segment] · CSM: [Name]
- [Signal 1]: [observed value] — [why this matters in 1 line]
- [Signal 2]: [observed value]
**Recommended action:** [Specific next step for the CSM]

---

### 🟡 P2 — Monitor Closely ([N] accounts)
[Same format]

---

### 🟢 P3 — Watch ([N] accounts)
[Same format, briefer — no recommended action block]

---

### Portfolio Summary
| | Count | vs. last period |
|---|---|---|
| P1 accounts | [N] | [↑/↓/= N] |
| P2 accounts | [N] | [↑/↓/= N] |
| P3 accounts | [N] | [↑/↓/= N] |
| Clean | [N] | [↑/↓/= N] |

*Sources: [connector list] · Data as of [timestamp]*
*Missing data: [list of unavailable connectors, or "none"]*
```

**Guardrails for Composer:**
- Do not present signals as confirmed facts — "showing no login activity" not "has churned"
- Do not include any metric labeled [review — internal planning target]
- Keep per-account summaries to 3 signals max — surface the highest-weight signals only
- P3 accounts get bullet summary only — no recommended action block (keeps the digest scannable)
- If zero P1 accounts: open with "No P1 signals this period" before P2 section

**Full subagent spec:** See `subagents/digest-composer.md`

---

## Connector Requirements

| Connector | Required | Purpose |
|-----------|----------|---------|
| CRM (HubSpot, Salesforce, etc.) | Yes | Account list, activity log, exec contact history |
| Support (Zendesk, Intercom, etc.) | Recommended | Ticket volume and severity |
| Product usage | Recommended | Login frequency, feature adoption |
| NPS/CSAT (Delighted, Medallia, etc.) | Optional | Customer sentiment signals |
| Slack | Optional | Digest channel delivery |

If only the CRM connector is available, the agent still runs but signals are limited to
CRM activity data. Flag missing connectors in the digest header.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Required config fields:
- `crm_connector`: Name of the CRM MCP connector
- `account_scope`: Which accounts to include (all, segment filter, CSM filter)
- `digest_output`: `file` | `slack` | `both`
- `slack_channel`: Channel name or ID (required if output = slack or both)
- `digest_file_path`: Save path (required if output = file or both)
- `reporting_period`: `daily` | `weekly`

Optional config fields:
- `signal_weights`: Override default signal weights (see Signal Analyzer above)
- `csm_assignments`: Map of CSM name → account IDs (if not in CRM)
- `exclude_accounts`: Account IDs to omit from the digest

If required fields are `[PLACEHOLDER]`, prompt:
> "Run `/csm:cold-start-interview --section churn-signals` to configure the
> Churn Signal Digest before running this agent."

---

## Scheduling

To run this agent on a schedule, use the Claude scheduled tasks feature:

```
Daily digest at 7:00 AM:
  cronExpression: "0 7 * * *"
  prompt: "Run the Churn Signal Digest for today."

Weekly digest every Monday at 7:30 AM:
  cronExpression: "30 7 * * 1"
  prompt: "Run the weekly Churn Signal Digest."
```

The agent is also invokable on-demand: "Run the churn signal digest" or
"Check for churn signals across my accounts."

---

## Sample Output (abbreviated)

```
## Churn Signal Digest — May 13, 2026
*47 accounts monitored · Generated by Claude Churn Signal Agent*

### 🔴 P1 — Immediate Attention (2 accounts)

**Acme Corp** · Enterprise · CSM: Sarah Chen
- No exec contact in 38 days (threshold: 30 days)
- 2 open P1 support tickets (avg age: 4 days)
**Recommended action:** Reach out to exec sponsor today; loop in AE to
confirm relationship health before support tickets create board-level noise.

**BetaFlow** · Mid-Market · CSM: James Park
- Login activity dropped 72% vs. last 7 days
- NPS score: 4 (detractor — received 6 days ago)
**Recommended action:** Schedule a same-week call with champion to understand
the NPS driver; review recent support interactions before the call.

### Portfolio Summary
| | Count | vs. last week |
|---|---|---|
| P1 | 2 | ↑1 |
| P2 | 7 | ↓2 |
| P3 | 11 | → |
| Clean | 27 | ↑1 |

*Sources: Salesforce, Zendesk, Mixpanel · Data as of 2026-05-13 07:02 UTC*
```
