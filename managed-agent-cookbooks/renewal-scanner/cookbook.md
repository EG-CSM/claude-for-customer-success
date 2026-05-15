# Renewal Scanner — Managed Agent Cookbook

**Agent type:** Scheduled orchestrator with 3 subagents  
**Cadence:** Weekly (Sunday evening or Monday morning) + on-demand  
**Trigger:** Scheduled task or on-demand via `/csm:renewal-scanner`  
**Output:** Renewal pipeline brief — risk-classified and expansion-flagged accounts delivered to Slack + saved as report

---

## What This Agent Does

The Renewal Scanner reviews all accounts with renewals coming up within the configured
look-ahead window (default: 90 days) and produces a prioritized renewal pipeline brief.
It is distinct from the churn signal digest — the Renewal Scanner is focused specifically
on accounts approaching a contract decision point and asks two separate questions for
each: "how confident are we in this renewal?" and "is there an expansion opportunity to
pursue before or alongside the renewal?"

It pulls renewal pipeline data from the CRM, enriches it with health scores and recent
engagement signals, and classifies each account on two dimensions: renewal risk (red,
yellow, green) and expansion potential (strong, moderate, none). The output gives the
CS leadership team and AEs a structured view of the renewal pipeline before the weekly
pipeline review.

**Outputs:**
- Risk-classified renewal pipeline: all accounts renewing within the look-ahead window,
  sorted by renewal date, flagged by risk tier
- Expansion signal summary: accounts where product signals or stakeholder engagement
  suggest expansion capacity before renewal
- Per-account renewal brief: ARR, renewal date, CSM, risk classification, top risk
  signals, recommended next action
- AE routing: accounts where AE involvement is recommended flagged explicitly
- Optional: Slack post + saved markdown report

---

## Architecture

```
Orchestrator: Renewal Scanner
│
├── Subagent 1: Pipeline Puller
│   Reads all accounts with renewals within the configured look-ahead window
│   from the CRM. Returns renewal dates, ARR, contract history, health score
│   (if in CRM), CSM assignment, and AE assignment.
│
├── Subagent 2: Risk & Expansion Classifier
│   Enriches each account with signals from available connectors (health score,
│   product usage, support history). Classifies renewal risk as red/yellow/green.
│   Classifies expansion potential as strong/moderate/none. Produces a ranked
│   renewal pipeline sorted by risk priority.
│
└── Subagent 3: Renewal Brief Composer
    Formats the renewal pipeline brief. Red-tier accounts lead; expansion
    opportunities are called out in a dedicated section. Delivers to
    configured output channels (Slack, file, or both).
```

The orchestrator sequences subagents and passes the full pipeline record forward.
The Risk & Expansion Classifier does not call connectors — it works on data the
orchestrator passes, which includes raw connector pulls requested from the Pipeline
Puller. The orchestrator is responsible for assembling the enrichment data before
dispatch.

---

## Orchestrator System Prompt

```
You are the Renewal Scanner orchestrator for a Customer Success team. Your job is to
produce a weekly renewal pipeline brief covering all accounts renewing within the
configured look-ahead window.

Your configuration lives at:
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md

And company profile at:
~/.claude/plugins/config/claude-for-customer-success/company-profile.md

Read both before starting. Fields you need:
- CRM connector name
- Renewal look-ahead window in days (default: 90 days)
- Health score source (connector name and field path — may be CRM custom field)
- Health score scale and band definitions (for risk classification)
- Product usage connector (if configured)
- Support connector (if configured)
- Renewal risk thresholds (if configured; use defaults if not)
- Digest output: Slack channel, file path, or both
- CSM names and AE names (for routing and attribution)

Execution sequence:

STEP 1 — Dispatch Pipeline Puller
  Pass: CRM connector name, today's date, look-ahead window (days), field paths
    for ARR, renewal date, CSM assignment, AE assignment, health score (if in CRM)
  Receive: all accounts renewing within the look-ahead window — one record per
    account with contract and relationship data
  Do not proceed until Pipeline Puller returns a complete response.

STEP 2 — Enrich with connector data
  Before dispatching the Risk & Expansion Classifier, enrich the pipeline record
  yourself using available connectors:
  - Health score connector (if separate from CRM): pull current scores for all accounts
    in the pipeline
  - Product usage connector (if configured): pull login frequency and feature adoption
    for the past 30 days
  - Support connector (if configured): pull open ticket count and P1 ticket history
    for the past 30 days
  If a connector call fails, note the failure and proceed with available data —
  log unavailable sources explicitly. Do not fabricate enrichment data.

STEP 3 — Dispatch Risk & Expansion Classifier
  Pass: full pipeline record from Step 1 + enrichment data from Step 2 +
    risk thresholds from config + health score band definitions
  Receive: classified and ranked renewal pipeline (risk tier + expansion signal
    per account) with recommended actions

STEP 4 — Dispatch Renewal Brief Composer
  Pass: ranked pipeline from Step 3 + output targets (Slack/file) +
    CSM and AE assignments + look-ahead window + today's date
  Receive: formatted renewal brief (markdown + Slack mrkdwn)

STEP 5 — Deliver output
  If Slack configured: post mrkdwn version to the configured channel.
  If file output configured: save markdown version to the configured path.
  Confirm delivery in your final response.

Rules:
- ARR must come from CRM. Never estimate ARR. If CRM does not return an ARR value
  for an account, mark it [ARR unverified] and do not fabricate a figure.
- Renewal dates must come from CRM. If renewal date is missing, flag the account
  as [renewal date unverified] and include it with a note — do not exclude it.
- Health scores must come from the configured source. If the source is unavailable
  for a specific account, the classifier must note [health data unavailable] —
  do not infer a score from other signals.
- Never characterize an account as "churning" or "lost." Language: "renewal signals
  suggest risk" or "flagged for immediate attention." The CSM makes the judgment.
- Never present expansion signals as committed pipeline. These are observations to
  raise in the renewal conversation — revenue recognition is the AE's and CSM's call.
- TtV figures, [review — internal planning target] metrics, or any internal benchmark
  must not appear in the renewal brief output.
- If the look-ahead window returns zero accounts (no renewals in window): confirm
  this to the user and skip subagent dispatch.
```

---

## Subagent 1: Pipeline Puller

**File:** `subagents/pipeline-puller.md`

**Role:** Data retrieval. The Pipeline Puller queries the CRM for all accounts with
renewal dates within the configured look-ahead window and returns a structured pipeline
record for each.

**Tools required:**
- CRM connector — required (renewal dates, ARR, contract history, CSM/AE assignments)

**Inputs from orchestrator:**
- CRM connector name
- Today's date
- Look-ahead window (days)
- Field paths for: renewal date, ARR, contract start, CSM, AE, health score (if in CRM)

**Output format:**
```
account_id: [CRM ID]
account_name: [name]
segment: [segment]
arr: [ARR or null if not found — flag if null]
product_tier: [tier]
csm: [assigned CSM]
ae: [assigned AE or null]
contract_start: [date]
renewal_date: [date or null — flag if null]
days_to_renewal: [N or null]
prior_renewal_count: [N — how many times this account has renewed]
prior_renewal_outcome: [renewed|expanded|contracted|at-risk-renewed|null]
health_score_crm: [score or null — from CRM field if configured]
health_band_crm: [band or null]
last_crm_activity_date: [date or null]
exec_sponsor: [name or null]
champion: [name or null]
data_as_of: [timestamp]
```

Return all accounts with a renewal date within the look-ahead window, inclusive.
Sort by days_to_renewal ascending (soonest renewals first). Accounts with null
renewal dates must be included — flag them; do not omit them.

**Full subagent spec:** See `subagents/pipeline-puller.md`

---

## Subagent 2: Risk & Expansion Classifier

**File:** `subagents/risk-expansion-classifier.md`

**Role:** Classification and prioritization. The Risk & Expansion Classifier takes the
enriched pipeline record from the orchestrator and assigns each account a renewal risk
tier and an expansion signal level. This subagent does not call connectors — it works
on data passed from the orchestrator.

**Tools required:** None — works on data passed from orchestrator.

**Renewal risk classification:**

| Risk tier | Conditions |
|-----------|-----------|
| 🔴 Red — Immediate attention | Any of: health score in red band; health score dropped ≥10 points in 30 days; open P1 support ticket; no exec contact in 45+ days (Enterprise); no product login in 14+ days |
| 🟡 Yellow — Monitor closely | Any of: health score in yellow band; health score declining trend; NPS ≤ 6; 3+ open tickets; login frequency declined >30% vs. prior period; no exec contact in 30–44 days (Enterprise) |
| 🟢 Green — On track | No red or yellow signals present; health score stable or improving |
| ⚪ Insufficient data | Required enrichment data unavailable for classification |

**Default risk thresholds** (overridden by config):
- Red health band: score < 40 on 0–100 scale
- Yellow health band: 40–69
- Green: ≥ 70

**Expansion signal classification:**

| Signal level | Conditions |
|-------------|-----------|
| Strong | Feature adoption score > 80; active users at or near seat limit (≥90% utilization); new use case mentioned in CRM notes in last 60 days; champion promoted or expanded role |
| Moderate | Feature adoption score 60–80; 2+ departments using the product (where started with 1); positive NPS trend (improving over 2+ periods) |
| None | No positive signals present; or data insufficient to assess |

**Output format:**
```
ranked_pipeline:
  - account_id: [CRM ID]
    account_name: [name]
    segment: [segment]
    arr: [ARR or null]
    days_to_renewal: [N or null]
    renewal_date: [date]
    csm: [name]
    ae: [name or null]
    risk_tier: [red|yellow|green|insufficient_data]
    risk_signals:
      - type: [signal type]
        value: [observed value]
        threshold: [threshold that fired]
    expansion_signal: [strong|moderate|none]
    expansion_evidence:
      - [observation supporting expansion signal — factual, not speculative]
    ae_involvement_recommended: [true|false]
    ae_involvement_reason: [1-sentence reason if true]
    recommended_action: [1-sentence specific next step for the CSM]

portfolio_summary:
  total_in_window: [N]
  red_count: [N]
  yellow_count: [N]
  green_count: [N]
  insufficient_data_count: [N]
  arr_at_risk: [sum of ARR for red-tier accounts or null if any ARR is null]
  arr_in_window_total: [total ARR in window or null if any ARR is null]
  strong_expansion_count: [N]
  moderate_expansion_count: [N]
  look_ahead_window_days: [N]
```

Sort `ranked_pipeline` by risk tier first (red, yellow, green, insufficient_data),
then by days_to_renewal ascending within each tier.

**Full subagent spec:** See `subagents/risk-expansion-classifier.md`

---

## Subagent 3: Renewal Brief Composer

**File:** `subagents/renewal-brief-composer.md`

**Role:** Output formatting and delivery preparation. The Renewal Brief Composer formats
the classified pipeline into the weekly renewal brief. Red-tier accounts lead with
recommended actions; expansion opportunities are surfaced in a dedicated section for
the AE and CS leadership team.

**Tools required:**
- Slack connector (if Slack output configured)

**Output format (markdown version):**

```markdown
## Renewal Pipeline Brief — [date]
*[N] accounts renewing within [N] days · [N] red · [N] yellow · [N] green*
*Generated by Claude Renewal Scanner*

---

### 🔴 Immediate Attention ([N] accounts)
*These renewals have signals that warrant same-week action.*

**[Account Name]** · [Segment] · CSM: [Name] · AE: [Name or —]
- ARR: [value] · Renewal: [date] ([N] days)
- [Risk signal 1]: [observed value]
- [Risk signal 2]: [observed value if any]
**Recommended action:** [Specific next step for CSM]
*AE involvement: [recommended — reason | not recommended]*

---

### 🟡 Monitor Closely ([N] accounts)

**[Account Name]** · [Segment] · CSM: [Name] · AE: [Name or —]
- ARR: [value] · Renewal: [date] ([N] days)
- [Risk signal]: [observed value]
**Recommended action:** [Next step]

---

### 🟢 On Track ([N] accounts)
[Account Name] · [Segment] · CSM: [Name] · ARR: [value] · [N] days
[Account Name] · [Segment] · CSM: [Name] · ARR: [value] · [N] days

---

### ⚡ Expansion Opportunities ([N] accounts)
*Accounts with signals suggesting capacity to expand before or alongside renewal.*

**[Account Name]** · [Segment] · CSM: [Name] · AE: [Name]
- Signal level: [Strong|Moderate]
- Evidence: [observation 1] · [observation 2 if any]
*Raise with AE — do not commit in the renewal brief.*

---

### Pipeline Summary

| | Count | ARR |
|---|---|---|
| 🔴 Red — immediate attention | [N] | [value or —] |
| 🟡 Yellow — monitor | [N] | [value or —] |
| 🟢 Green — on track | [N] | [value or —] |
| ⚪ Insufficient data | [N] | [value or —] |
| **Total in window** | **[N]** | **[value or —]** |

*Look-ahead window: [N] days ([today] through [end date])*
*Sources: [connector list] · Data as of [timestamp]*
*[N] accounts with unverified renewal dates — included above with [date unverified] flag*
*Unavailable sources: [list or "none"]*
```

**Guardrails for Composer:**
- Red accounts always lead — even if there is only one, it comes before yellow
- Expansion section appears after green accounts — it is not the primary signal;
  renewals lead
- On-track accounts are a brief list only — no per-account narrative
- Expansion evidence must be stated as observations, not projections:
  "90% seat utilization" not "ready to add seats" — the CSM and AE draw the inference
- AE involvement recommendation must include a reason — "true" alone is not useful
- If zero red and zero yellow accounts: open with "No renewal risk signals this period.
  All [N] upcoming renewals are on track." before the On Track list
- ARR figures marked [unverified] must appear as [ARR unverified] in the brief —
  do not substitute an estimate

**Full subagent spec:** See `subagents/renewal-brief-composer.md`

---

## Connector Requirements

| Connector | Required | Purpose |
|-----------|----------|---------|
| CRM (HubSpot, Salesforce, etc.) | Yes | Renewal dates, ARR, contract history, stakeholders |
| Health score source (CRM field, Gainsight, Totango, etc.) | Recommended | Primary risk classification input |
| Product usage | Recommended | Adoption signals for risk and expansion classification |
| Support (Zendesk, Intercom, etc.) | Recommended | Open ticket signals for risk classification |
| NPS/CSAT | Optional | Sentiment signals for risk and expansion |
| Slack | Optional | Pipeline brief channel delivery |

The agent still runs with only the CRM connector. Risk classification will default to
[insufficient data] for any account where health score data is unavailable. Missing
connectors are listed in the brief header — they are never silently dropped.

If the CRM tracks health scores as a custom field, configure that field path in
`../../csm/CLAUDE.md` under `health_score_source`. The Pipeline Puller will retrieve it
and the orchestrator will pass it to the classifier.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Required config fields:
- `crm_connector`: Name of the CRM MCP connector
- `renewal_window_days`: How far ahead to scan (default: `90`)
- `renewal_output`: `file` | `slack` | `both`

Optional config fields:
- `health_score_source`: Connector name and field path to health score data
- `health_score_scale`: Score range and band boundaries (default: `0-100`, red <40, yellow 40-69)
- `usage_connector`: Product usage MCP connector
- `support_connector`: Support MCP connector
- `nps_connector`: NPS/CSAT connector
- `renewal_risk_thresholds`: Override default red/yellow trigger conditions
- `slack_channel`: Required if output includes Slack
- `renewal_file_path`: Required if output includes file
- `csm_filter`: Run only for accounts assigned to a specific CSM
- `exclude_accounts`: Account IDs to exclude from the scan

If required fields are `[PLACEHOLDER]`, prompt:
> "Run `/csm:cold-start-interview --section renewal` to configure the Renewal Scanner
> before running this agent."

---

## Scheduling

```
Weekly renewal brief every Monday at 7:00 AM:
  cronExpression: "0 7 * * 1"
  prompt: "Run the Renewal Scanner for this week."
```

Sunday evening is an alternative cadence for teams that review the pipeline in their
Monday morning standup:

```
Sunday evening at 6:00 PM:
  cronExpression: "0 18 * * 0"
  prompt: "Run the Renewal Scanner for the coming week."
```

On-demand invocation: "Run the renewal scanner" or "Show me the renewal pipeline
for the next 90 days" or "Which accounts renewing this quarter need attention?"

---

## Sample Output (abbreviated)

```
## Renewal Pipeline Brief — May 13, 2026
*11 accounts renewing within 90 days · 2 red · 3 yellow · 5 green · 1 insufficient data*
*Generated by Claude Renewal Scanner*

### 🔴 Immediate Attention (2 accounts)

**Meridian Labs** · Enterprise · CSM: Priya Sharma · AE: Kevin Walsh
- ARR: $124,000 · Renewal: June 9, 2026 (27 days)
- Health score: 54 (entered yellow band — dropped 17 points in last 30 days)
- Open P1 ticket: #4821 (3 days unresolved)
**Recommended action:** Schedule exec sponsor call before end of week; loop in
AE to confirm relationship health before ticket becomes renewal blocker.
*AE involvement: recommended — health score drop + P1 ticket within 30 days of renewal*

**Cascade Health** · Enterprise · CSM: Priya Sharma · AE: Jessica Tran
- ARR: $89,500 · Renewal: June 22, 2026 (40 days)
- No exec contact in 51 days (threshold: 45 days)
- Login activity: 22% decline vs. prior 30 days
**Recommended action:** Book executive check-in this week; prepare a brief
usage summary to anchor the conversation before the renewal conversation begins.
*AE involvement: recommended — no exec contact at 51 days with renewal in 40 days*

### 🟡 Monitor Closely (3 accounts)

**Finwave Corp** · Mid-Market · CSM: Daniel Flores · AE: —
- ARR: $42,000 · Renewal: July 1, 2026 (49 days)
- NPS: 6 (received May 2 — at detractor threshold)
**Recommended action:** Follow up on NPS score with champion before renewal
conversation; understand what drove the 6 before it becomes the renewal narrative.

### 🟢 On Track (5 accounts)
BlueField Tech · Enterprise · CSM: James Park · ARR: $210,000 · 61 days
Lumify AI · Mid-Market · CSM: Sarah Chen · ARR: $38,500 · 66 days
GrowPath · SMB · CSM: Sarah Chen · ARR: $18,200 · 71 days
Nora Systems · Mid-Market · CSM: James Park · ARR: $55,000 · 78 days
Apex Digital · SMB · CSM: Daniel Flores · ARR: $14,800 · 88 days

### ⚡ Expansion Opportunities (2 accounts)

**BlueField Tech** · Enterprise · CSM: James Park · AE: Kevin Walsh
- Signal level: Strong
- Evidence: 96% seat utilization (48 of 50 provisioned) · Feature adoption score: 84 ·
  New data science use case mentioned in CRM notes (April 28)
*Raise with AE — do not commit in the renewal brief.*

**Lumify AI** · Mid-Market · CSM: Sarah Chen · AE: Jessica Tran
- Signal level: Moderate
- Evidence: Feature adoption score: 71 (up from 52 at kickoff) · 2 departments now
  using product (started with 1)
*Raise with AE — do not commit in the renewal brief.*

### Pipeline Summary

| | Count | ARR |
|---|---|---|
| 🔴 Red — immediate attention | 2 | $213,500 |
| 🟡 Yellow — monitor | 3 | $104,700 |
| 🟢 Green — on track | 5 | $336,500 |
| ⚪ Insufficient data | 1 | [ARR unverified] |
| **Total in window** | **11** | **$654,700+** |

*Look-ahead window: 90 days (May 13 through Aug 11, 2026)*
*Sources: Salesforce, Gainsight MCP, Mixpanel · Data as of 2026-05-13 07:01 UTC*
*0 accounts with unverified renewal dates*
*Unavailable sources: none*
```
