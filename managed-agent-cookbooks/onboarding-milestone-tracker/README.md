# Onboarding Milestone Tracker — Deployment & Configuration Guide

## What This Agent Does

The Onboarding Milestone Tracker runs each weekday morning and monitors milestone
progress across all active onboarding accounts. It compares current milestone status
against expected timelines, surfaces accounts where milestones are overdue or at risk
of slipping, and delivers a digest designed for daily CS team review during onboarding
standups.

An account is considered active if it has not yet completed M5 (handoff_ready).
Accounts that have graduated — where M5 is complete — are excluded from the scan
automatically.

The digest answers: "Which accounts have onboarding milestones that are overdue or
trending late, and what does each one need?"

**Outputs:**
- Alert digest: overdue milestone accounts with full status blocks and recommended
  actions; at-risk accounts with status blocks and recommended actions; due-soon
  accounts in brief list format only
- Portfolio Summary table: counts of active accounts by milestone status category
- Optional Slack delivery: mrkdwn version posted to a configured channel
- On-track accounts: counted in the portfolio summary but not surfaced in the body

---

## Architecture

```
Orchestrator: Onboarding Milestone Tracker
│
├── Subagent 1: Milestone Puller
│   Pulls current milestone status for all active onboarding accounts from
│   the configured project management connector. Returns one milestone record
│   per account including milestone completion dates, current milestone, and
│   contract start date if available from CRM.
│
├── Subagent 2: Risk Assessor
│   Compares actual milestone progress against the expected timeline in the
│   configured milestone framework. Classifies each account as Overdue,
│   At Risk, Due Soon, or On Track. Returns a ranked alert list.
│
└── Subagent 3: Report Composer
    Formats the classified account list into the digest. Delivers the
    markdown output and optional Slack message. Does not call project
    management or CRM connectors — receives all data from the orchestrator.
```

---

## Prerequisites

### Required Connectors

| Connector | Role |
|-----------|------|
| Project management platform | Milestone status and completion dates for all active onboarding projects |

The project management connector is the primary data source. This can be Asana,
Linear, Jira, Monday.com, or any platform with project tracking capability. Configure
`pm_connector` to point to the appropriate connector.

### Optional Connectors

| Connector | Role |
|-----------|------|
| CRM (HubSpot, Salesforce, etc.) | Contract start date for timeline anchor; CSM assignment for display |
| Slack | Delivery of the mrkdwn digest to a configured channel |

Without the CRM connector, the agent uses the onboarding project creation date as the
timeline anchor. This may produce less accurate at-risk classifications for accounts
where the contract predates project creation.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`

Note: This agent uses the `onboarding/` config namespace, not `csm/`. Run
`/onboarding:cold-start-interview --section milestones` to configure this file if it
contains `[PLACEHOLDER]` values.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `pm_connector` | Project management MCP connector name | `asana-mcp` |
| `onboarding_project_tag` | Tag or label that identifies onboarding projects in the PM platform | `customer-onboarding` |
| `milestone_framework` | Which milestone set the agent tracks | `m1-m5-standard` |
| `digest_output` | `file` \| `slack` \| `both` | `both` |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `at_risk_signals` | Override default at-risk detection rules | built-in defaults |
| `escalation_matrix` | CSM and manager assignments for escalation blocks | — |
| `slack_channel` | Slack channel for delivery (required if digest_output includes `slack`) | — |
| `digest_file_path` | Where to save the markdown digest | — |
| `csm_filter` | Restrict output to accounts owned by a specific CSM | all CSMs |

### Milestone Framework: M1–M5 Standard

| Milestone | Label | Description |
|-----------|-------|-------------|
| M1 | kickoff | Kickoff call completed |
| M2 | tech_setup | Technical configuration and integration complete |
| M3 | first_use | First meaningful product use by the customer |
| M4 | first_value | First customer-confirmed value moment |
| M5 | handoff_ready | Onboarding complete; account graduated to ongoing CS motion |

Accounts that have completed M5 are excluded from all scans. Accounts with M1 not yet
started are included if their onboarding project exists in the PM platform.

### Status Classification

| Status | Trigger Condition |
|--------|------------------|
| 🔴 Overdue | Current milestone is past its expected completion date |
| ⚠ At Risk | Current milestone is within 3 days of its expected completion date with no completion signal, OR two or more configured at-risk signals are present |
| 🟡 Due Soon | Current milestone is due within the next 7 days; no at-risk signals present |
| ✅ On Track | Milestone timeline is healthy; no signals present |

At-risk signals (defaults, configurable):
- No PM task activity in the last 5 business days
- No CRM contact logged in the last 10 days
- Technical milestone (M2) has open blocking issues
- Customer has not responded to last CSM outreach

---

## Scheduling

### Standard: Weekday Mornings

```
cronExpression: "0 7 * * 1-5"
prompt: "Run the onboarding milestone tracker."
```

Delivers the digest Monday through Friday before the CS team's morning standup.
Weekday-only scheduling prevents false alerts on weekends when no action is possible.

### On-Demand Invocation

Trigger at any time with natural language. See `steering-examples.json` for the full
prompting pattern library. Common invocations:

- "Run the onboarding milestone tracker."
- "Which onboarding accounts are overdue?"
- "Check milestone status for Marcus Webb's accounts."

---

## Output Reference

### Digest Section Order (fixed — never reordered)

| Section | Contents | Format |
|---------|----------|--------|
| Header | Date, active account count, alert counts by category | Header block |
| 🔴 Overdue | All accounts with overdue milestones | Per-account block |
| ⚠ At Risk | All accounts trending late | Per-account block |
| 🟡 Due Soon | Accounts with milestones due within 7 days | Brief list only |
| Portfolio Summary | Counts by status category | Table |

Sections with zero accounts are omitted from the body. The Portfolio Summary table
always renders.

When there are zero Overdue accounts AND zero At Risk accounts, the digest opens with:

> No overdue or at-risk milestones today.

immediately before the Due Soon section (or Portfolio Summary if Due Soon is also empty).

### Per-Account Format

**Overdue and At Risk accounts — full block:**

```
**[Account Name]** · CSM: [Name or —] · Started: [contract start date or project date]
Current milestone: [M label] — [milestone name] · Expected: [date] · [N days overdue / N days until due]
Signals: [at-risk signals if any, or none]
**Recommended action:** [One sentence]
```

**Due Soon accounts — brief list (no recommended action, no narrative):**

```
[Account Name] · CSM: [Name or —] · [Milestone name] due [date]
```

### Portfolio Summary

The summary table shows account counts across all five status categories:

| Status | Count |
|--------|-------|
| 🔴 Overdue | N |
| ⚠ At Risk | N |
| 🟡 Due Soon | N |
| ✅ On Track | N |
| Total Active | N |

Graduated accounts (M5 complete) are excluded from all counts.

---

## Data Gap Behavior

| Situation | Behavior |
|-----------|----------|
| PM connector unavailable | Halt immediately — no digest produced; error surfaced to orchestrator |
| CRM unavailable | Continue; use PM project creation date as timeline anchor; render CSM as `—` |
| Account not found in PM | Skip account; note in digest footer |
| Milestone dates missing for an account | Include account in portfolio count; flag as `[milestone dates unavailable]` in body if Overdue or At Risk |
| No active onboarding accounts | Digest renders with "No active onboarding accounts in scope." and an empty portfolio summary |
| Slack connector unavailable | Complete markdown digest; note Slack failure in delivery status; do not halt |
| At-risk signal data unavailable | Classify using available signals only; note connector gap inline |
| `logins_last_7d: 0` vs null | Zero is a confirmed zero login count; null means the connector did not return data — these are not equivalent and must not be treated as such |

---

## Customization

### Adjusting At-Risk Signals

Override `at_risk_signals` in config to change the signals the Timeline Analyzer uses
for at-risk classification. Valid signal types include: `no_pm_activity_days`,
`no_crm_contact_days`, `open_blocking_issues`, `no_csm_response`. Setting a signal
to `ignore` removes it from classification.

### Restricting the Scope

Use `csm_filter` to run alerts for a specific CSM's onboarding accounts only. This can
also be passed as a one-off override in the invocation prompt: "Run the onboarding
milestone tracker for Priya Sharma's accounts."

### Escalation Matrix

When `escalation_matrix` is configured, the Digest Composer includes the assigned
escalation contact (CSM manager or implementation lead) in the recommended action block
for Overdue accounts. This field maps CSM names to escalation contacts and is optional.

### Output Scope Note

This agent surfaces onboarding velocity and milestone status. Time-to-value projections
and internal planning targets are not included in any digest output — those are internal
planning tools and are never surfaced to external audiences or logged in customer-facing
systems.

---

## Subagent Reference

| Subagent | File | Role |
|----------|------|------|
| Milestone Puller | `subagents/milestone-puller.md` | Milestone status retrieval and timeline anchor resolution |
| Risk Assessor | `subagents/risk-assessor.md` | Status classification and at-risk signal detection |
| Report Composer | `subagents/report-composer.md` | Output formatting, delivery, and portfolio summary |
