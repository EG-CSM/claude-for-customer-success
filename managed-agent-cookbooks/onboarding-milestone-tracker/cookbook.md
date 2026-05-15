# Onboarding Milestone Tracker — Managed Agent Cookbook

**Agent type:** Scheduled orchestrator with 3 subagents  
**Cadence:** Daily  
**Trigger:** Scheduled task or on-demand via `/csm:onboarding-milestone-tracker`  
**Output:** Daily milestone health report delivered to Slack + saved as markdown report

---

## What This Agent Does

The Onboarding Milestone Tracker monitors M1–M5 milestone progress across all active
onboarding accounts and surfaces at-risk and overdue milestones before they become
escalations. It runs each morning, giving the onboarding team a prioritized action list
at the start of every day.

Unlike the `/onboarding:milestone-tracker` skill (which operates on a single account
interactively), this agent sweeps the entire onboarding book of business automatically,
requiring no per-account invocation. It reads from the configured PM connector to get
current milestone status, applies at-risk signal detection from the onboarding profile,
and routes flagged accounts to the output.

**Outputs:**
- Overdue milestone list with escalation recommendations
- At-risk milestone list with proactive action recommendations
- Accounts due for upcoming milestone within 3 days
- Portfolio health summary: count by status across the full onboarding book
- Optional: Slack post + saved markdown report

---

## Architecture

```
Orchestrator: Onboarding Milestone Tracker
│
├── Subagent 1: Milestone Puller
│   Reads all active onboarding accounts from the PM connector.
│   Returns current milestone status, completion dates, and
│   contract start dates for each account in the onboarding book.
│
├── Subagent 2: Risk Assessor
│   Calculates target dates from config milestone framework.
│   Evaluates each account's at-risk signals and days-overdue status.
│   Produces tiered flag list: overdue, at-risk, due soon, on track.
│
└── Subagent 3: Report Composer
    Formats the daily report. Overdue accounts first, then at-risk,
    then due soon. Includes recommended actions from the escalation
    matrix. Delivers to configured output channels.
```

The orchestrator handles configuration loading and passes the complete milestone framework
and escalation thresholds to the Risk Assessor. Subagents do not read config files —
the orchestrator owns config access.

---

## Orchestrator System Prompt

```
You are the Onboarding Milestone Tracker orchestrator for a Customer Success team.
Your job is to produce a daily milestone health report across all active onboarding
accounts.

Your configuration lives at:
~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md

And company profile at:
~/.claude/plugins/config/claude-for-customer-success/company-profile.md

Read both before starting. Fields you need from onboarding config:
- Milestone framework: M1–M5 day targets and at-risk signals per milestone
- Escalation matrix: who to involve at each days-overdue tier
- Onboarding model: affects which milestones are CSM-led vs. partner-led
- PM connector name: the project management tool to pull milestone data from

Execution sequence:

STEP 1 — Dispatch Milestone Puller
  Pass: PM connector name, date (today), onboarding project tag/filter
  Receive: list of all active onboarding accounts with current milestone status
    and contract start dates
  Do not proceed until Milestone Puller returns a complete response.

STEP 2 — Dispatch Risk Assessor
  Pass: full account/milestone list from Step 1 + milestone framework from config
    (M1-M5 day targets, at-risk signals) + escalation thresholds + today's date
  Receive: tiered flag list (overdue, at-risk, due soon, on track) with recommended
    actions and days calculations

STEP 3 — Dispatch Report Composer
  Pass: tiered flag list + portfolio summary + output targets (Slack/file) +
    CSM assignments
  Receive: formatted daily report (markdown + Slack mrkdwn)

STEP 4 — Deliver output
  If Slack configured: post mrkdwn version to the configured channel.
  If file output configured: save markdown to the configured path.
  Confirm delivery in your final response.

Rules:
- If the PM connector is unavailable, surface the error immediately. Do not run
  risk assessment without current milestone data — stale data produces false alarms.
- If contract start date is missing for any account, flag those accounts as
  [unverified dates] in the report rather than estimating.
- TtV projections are internal only. They may appear in the internal reviewer note
  but NEVER in the output delivered to Slack or saved as a shared report.
- Overdue does not equal failed. The report flags overdue milestones for CSM attention;
  it does not characterize the account or the CSM's performance.
- Do not recommend actions the CSM has already taken — the Milestone Puller should
  surface prior escalation history if available from the PM connector.
```

---

## Subagent 1: Milestone Puller

**File:** `subagents/milestone-puller.md`

**Role:** Data retrieval. The Milestone Puller reads all active onboarding projects from
the PM connector and returns current milestone status for every account in the onboarding
book.

**Tools required:**
- PM connector (Asana, Linear, Jira, or Monday.com) — required
- CRM connector — recommended for contract start date and CSM assignment

**Inputs from orchestrator:**
- PM connector name
- Project tag or filter (how onboarding accounts are identified in the PM tool)
- Today's date

**Output format:**
```
account_id: [ID or project key]
account_name: [name]
csm: [assigned CSM]
segment: [segment]
onboarding_model: [white-glove|guided-self-serve|implementation-plus-handoff|partner-led]
contract_start_date: [date or null]
milestones:
  m1_kickoff:
    status: [complete|in_progress|not_started]
    target_date: [date or null — from PM tool if set]
    actual_date: [date or null]
  m2_tech_setup:
    status: [complete|in_progress|not_started]
    target_date: [date or null]
    actual_date: [date or null]
  m3_first_use:
    status: [complete|in_progress|not_started]
    target_date: [date or null]
    actual_date: [date or null]
  m4_first_value:
    status: [complete|in_progress|not_started]
    target_date: [date or null]
    actual_date: [date or null]
  m5_handoff_ready:
    status: [complete|in_progress|not_started]
    target_date: [date or null]
    actual_date: [date or null]
open_blockers: [count or null]
prior_escalations: [count or null]
data_as_of: [timestamp]
```

Return all active onboarding accounts. An account is "active" if M5 is not yet marked
complete. Graduated accounts (M5 complete) are excluded.

**Full subagent spec:** See `subagents/milestone-puller.md`

---

## Subagent 2: Risk Assessor

**File:** `subagents/risk-assessor.md`

**Role:** Risk calculation and tiering. The Risk Assessor applies the milestone framework
from config to calculate each account's risk status and produces a prioritized flag list.

**Tools required:** None — works on data passed from orchestrator.

**Milestone date calculation:**

For each account:
- If a target date exists in the PM tool, use it
- If not, calculate: `contract_start_date + milestone_day_target_from_config`
- If contract start date is null, flag as `[unverified]` — do not estimate

**Status determination per active milestone:**

| Status | Condition |
|--------|-----------|
| `Overdue` | Target date is in the past; milestone not complete |
| `At risk` | At-risk signal present (per config) OR target date ≤ 5 days and signal present |
| `Due soon` | Target date is 1–3 days away; no signals; not yet at risk |
| `On track` | Target date ≥ 4 days away; no signals |
| `Complete` | Milestone marked complete in PM tool |

**Default at-risk signals** (overridden by config values):

| Milestone | Signal |
|-----------|--------|
| M1 | Required attendees not confirmed 48h before kickoff date |
| M2 | Integration credentials not received within 7 days of M1 |
| M3 | No product login activity logged in first 14 days |
| M4 | No use case completion documented by 25 days post-kickoff |
| M5 | Success criteria not confirmed by 45 days post-kickoff |

**Output format:**
```
overdue:
  - account_id: [ID]
    account_name: [name]
    csm: [name]
    segment: [segment]
    milestone: [M# label]
    days_overdue: [N]
    at_risk_signals: [list or empty]
    escalation_recommended: [AE | manager | exec sponsor | none]
    recommended_action: [specific action from escalation matrix]

at_risk:
  - account_id: [ID]
    account_name: [name]
    csm: [name]
    segment: [segment]
    milestone: [M# label]
    days_to_target: [N]
    at_risk_signals: [list]
    recommended_action: [proactive step]

due_soon:
  - [account_id, account_name, csm, milestone, days_to_target]

on_track_count: [N]
unverified_dates_count: [N]

portfolio_summary:
  total_active_accounts: [N]
  overdue_count: [N]
  at_risk_count: [N]
  due_soon_count: [N]
  on_track_count: [N]
```

**Full subagent spec:** See `subagents/risk-assessor.md`

---

## Subagent 3: Report Composer

**File:** `subagents/report-composer.md`

**Role:** Output formatting. The Report Composer formats the risk assessment into the
daily report. Overdue accounts lead; at-risk follow; due soon is a brief list; on-track
accounts are not included in the body (count only in portfolio summary).

**Tools required:**
- Slack connector (if Slack output configured)

**Output format (markdown version):**

```markdown
## Onboarding Milestone Report — [date]
*[N] accounts in active onboarding · Generated by Claude Milestone Tracker*

---

### 🔴 Overdue Milestones ([N] accounts)

**[Account Name]** · M[#]: [label] · [Segment] · CSM: [Name]
- [N] days overdue (target: [date])
- [At-risk signals if any]
**Escalation:** [contact] — [recommended action]

---

### ⚠ At Risk ([N] accounts)

**[Account Name]** · M[#]: [label] · [Segment] · CSM: [Name]
- [N] days to target
- Signal: [at-risk signal description]
**Recommended action:** [proactive step]

---

### 🟡 Due Soon ([N] accounts)
[Account Name] · M[#] · [N] days · CSM: [Name]
[Account Name] · M[#] · [N] days · CSM: [Name]

---

### Portfolio Summary
| Status | Count |
|--------|-------|
| Overdue | [N] |
| At risk | [N] |
| Due soon | [N] |
| On track | [N] |
| Total active | [N] |

*Sources: [PM connector], [CRM connector if used] · Data as of [timestamp]*
*[N] accounts with unverified dates (contract start missing) — dates excluded from calculation*
```

**Guardrails for Composer:**
- Lead with overdue accounts — these need same-day action
- Due soon accounts are a brief list only — no narrative, no recommended action
  (they aren't in trouble yet)
- If zero overdue and zero at-risk: open with "No overdue or at-risk milestones
  today." before the Due Soon section
- TtV projections must not appear in this output — internal only
- Never characterize an overdue milestone as the CSM's failure — state facts only

**Full subagent spec:** See `subagents/report-composer.md`

---

## Connector Requirements

| Connector | Required | Purpose |
|-----------|----------|---------|
| PM (Asana, Linear, Jira, Monday.com) | Yes | Milestone status and dates |
| CRM (HubSpot, Salesforce, etc.) | Recommended | Contract start date, CSM assignment, segment |
| Slack | Optional | Report channel delivery |

The PM connector is the authoritative source for milestone status. If the CRM connector
provides conflicting milestone information (e.g., custom fields), the PM connector
takes precedence. Surface the discrepancy in the reviewer note.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`

Required config fields:
- `pm_connector`: Name of the PM MCP connector
- `onboarding_project_tag`: How onboarding accounts are tagged/filtered in the PM tool
- `milestone_framework`: M1–M5 day targets (used when PM tool has no target date)
- `digest_output`: `file` | `slack` | `both`

Optional config fields:
- `at_risk_signals`: Override default at-risk signals per milestone
- `escalation_matrix`: Days-overdue thresholds and escalation contacts
- `slack_channel`: Required if output = slack or both
- `digest_file_path`: Required if output = file or both
- `csm_filter`: Run for specific CSM's accounts only

If required fields are `[PLACEHOLDER]`, prompt:
> "Run `/onboarding:cold-start-interview --section milestones` to configure the
> Onboarding Milestone Tracker before running this agent."

---

## Scheduling

```
Daily morning report at 7:00 AM:
  cronExpression: "0 7 * * 1-5"
  prompt: "Run the Onboarding Milestone Tracker for today."
```

Weekday-only scheduling (`1-5`) is typical for onboarding teams — adjust to `* * *`
if weekend coverage is needed.

---

## Sample Output (abbreviated)

```
## Onboarding Milestone Report — May 13, 2026
*14 accounts in active onboarding · Generated by Claude Milestone Tracker*

### 🔴 Overdue Milestones (1 account)

**Cascade Health** · M3: First use · Enterprise · CSM: Priya Sharma
- 6 days overdue (target: May 7)
- Signal: No product login activity in first 14 days
**Escalation:** AE (Marcus Lee) — confirm executive sponsor priority before week end

### ⚠ At Risk (2 accounts)

**Finwave Corp** · M2: Tech setup · Mid-Market · CSM: Daniel Flores
- 4 days to target
- Signal: Integration credentials not received (Day 7 threshold exceeded)
**Recommended action:** Escalate to customer IT lead today; confirm firewall
approval timeline.

**GrowPath** · M4: First value · SMB · CSM: Sarah Chen
- 3 days to target
- Signal: No use case completion documented by Day 25
**Recommended action:** Schedule same-week call to confirm first use case completion
criteria met or agree on extension.

### 🟡 Due Soon (2 accounts)
Lumify AI · M1 Kickoff · 2 days · CSM: James Park
Northgate Corp · M3 First use · 1 day · CSM: Priya Sharma

### Portfolio Summary
| Status | Count |
|--------|-------|
| Overdue | 1 |
| At risk | 2 |
| Due soon | 2 |
| On track | 9 |
| Total active | 14 |

*Sources: Asana MCP, Salesforce · Data as of 2026-05-13 07:01 UTC*
```
