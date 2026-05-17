# churn-signal-scanner
## Managed Agent Cookbook — rev-ops plugin v1.0.0

Scans the active account portfolio for Tier 1, 2, and 3 churn signals on a
configurable schedule. Produces a prioritized at-risk account list for CS
leadership. Tier 3 accounts trigger Linear escalation issues with human
confirmation required before any write operation.

---

## Architecture

```
churn-signal-scanner/
├── agent.yaml                          # Orchestrator manifest
├── agents/
│   └── churn-signal-scanner.md         # Orchestrator behavioral spec
├── subagents/
│   ├── churn-signal-collector.yaml     # Signal evaluation subagent manifest
│   ├── churn-signal-collector.md       # Signal evaluation spec
│   ├── churn-escalation-writer.yaml    # Linear write subagent manifest
│   ├── churn-escalation-writer.md      # Linear write spec
│   ├── churn-alert-poster.yaml         # Slack delivery subagent manifest
│   └── churn-alert-poster.md           # Slack delivery spec
├── steering-examples.json              # 10 test scenarios
└── README.md                           # This file
```

### Subagent tool assignment

| Subagent | Filesystem | HubSpot | CS Platform | Linear | Slack |
|----------|-----------|---------|-------------|--------|-------|
| churn-signal-collector | read only | ✓ | ✓ | — | — |
| churn-escalation-writer | **none** | — | — | ✓ | — |
| churn-alert-poster | **none** | — | — | — | ✓ |
| Orchestrator | read + task | ✓ | ✓ | ✓ | ✓ |

Orchestrator connectors are passed through to subagents via the `callable_agents`
mechanism — each subagent only receives the connectors its `.yaml` manifest
declares.

---

## Prerequisites

- rev-ops plugin installed (`../../rev-ops`)
- Practice profile at `~/.cs-agent/practice-profile.json` (see § Practice Profile)
- Four MCP connectors configured:
  - `HUBSPOT_MCP_URL` — CRM account data
  - `CS_PLATFORM_MCP_URL` — Health scores and usage data
  - `LINEAR_MCP_URL` — Issue creation for Tier 3 escalation
  - `SLACK_MCP_URL` — Alert delivery

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HUBSPOT_MCP_URL` | HubSpot MCP server URL |
| `CS_PLATFORM_MCP_URL` | CS platform MCP server URL (Gainsight, ChurnZero, etc.) |
| `LINEAR_MCP_URL` | Linear MCP server URL |
| `SLACK_MCP_URL` | Slack MCP server URL |

---

## Practice Profile

The orchestrator reads `~/.cs-agent/practice-profile.json` before invoking
any subagent. The following fields govern churn scan behavior:

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `company_name` | **yes** | — | Displayed in scan header; scan stops if missing |
| `primary_segment` | no | `"general"` | Used for cohort mode context |
| `tier1_mode` | no | `"rule"` | `"rule"` or `"cohort"` |
| `discount_elevated_threshold` | no | `0.20` | Discount % that triggers Tier 1 flag |
| `segment_avg_sales_cycle_days` | no | `90` | Baseline for sales cycle Tier 1 rule |
| `renewal_window_days` | no | `180` | How far ahead to pull renewal dates |
| `onboarding_window_days` | no | `90` | How far back to pull onboarding starts |
| `tier3_acv_threshold` | no | `0` | Minimum ACV for Tier 3 evaluation; 0 = all accounts |
| `alert_channel` | no | `"#revops-alignment"` | Primary Slack channel |
| `tier3_channel` | no | `"#cs-leadership"` | Channel for Tier 3-only summary |

If `company_name` is missing, the orchestrator stops before invoking any
subagent and reports the configuration error.

---

## Churn Signal Tiers

### Tier 1 — Structural Risk (fires at deal close)

Evaluated for all accounts. Mode declared on every output.

**Rule mode** — flag account if ANY of:

| Signal | Condition |
|--------|-----------|
| Elevated discount | `discount_pct > discount_elevated_threshold` |
| Extended sales cycle | `sales_cycle_days > segment_avg_sales_cycle_days × 2` |
| Single-threaded | `stakeholder_count = 1` |
| No OCV at close | `ocv_trigger_present = false` |

**Cohort mode** — applies cohort-based risk scoring from CS platform. Falls
back to rule mode if cohort data is absent.

Mode declaration appended to every output:
- `[Tier 1: Rule mode — upgrade to cohort mode when 6+ months of churn data available]`
- `[Tier 1: Cohort mode — based on closed/won-to-churn cohort analysis]`

### Tier 2 — Behavioral Risk (30–90 days post-onboarding)

Flag account if ANY of:

| Signal | Condition |
|--------|-----------|
| Low adoption | `usage_pct_of_expected < 0.70` |
| OCV not started | `ocv_rubric_stage = "L0"` past first checkpoint |
| Champion departure | `champion_departure_flag = true` |
| Missed EBR/QBR | `ebr_qbr_missed_count >= 2` |

### Tier 3 — Late-Stage Risk (90–120 days pre-renewal)

ACV threshold filter applied first (`tier3_acv_threshold`). Flag account if ANY of:

| Signal | Condition |
|--------|-----------|
| Declining health trend | `health_score_trend` declining for ≥ 3 consecutive weeks |
| Renewal not started | `renewal_conversation_not_initiated = true` |
| Support ticket spike | `support_ticket_count_30d >= 2× account avg` |
| Sponsor gone dark | `executive_sponsor_last_activity_days >= 30` |

**Tier 3 accounts trigger Linear issue creation** (see § Governance Protocol).

---

## Governance Protocol — Section 9 Write Tier

Linear issue creation is a **Write** operation. The churn-escalation-writer
enforces a mandatory human confirmation gate before any Linear API call.

**Confirmation flow:**

1. Subagent renders a proposed issue table:
   ```
   | # | Account | ACV | Days to Renewal | Signals Fired | Proposed Owner |
   ```
2. Operator responds:
   - `"confirm all"` — create all proposed issues
   - `"confirm N, M"` — create issues N and M only
   - `"skip all"` — do not create any issues

3. Issues are created only for confirmed accounts.

4. A write-audit log entry is produced for each account:
   ```json
   {
     "timestamp": "ISO timestamp",
     "skill_name": "churn-signal-scanner/churn-escalation-writer",
     "operation_type": "linear_issue_create",
     "account_id": "...",
     "human_approval_status": "approved | skipped",
     "approver_response": "confirm all | confirm N,M | skip all",
     "outcome": "created | skipped | failed"
   }
   ```

This gate is **not skippable** — not even when only one Tier 3 account is
present. The `require_confirmation: true` flag is always sent by the
orchestrator.

---

## Linear Issue Format

**Title:** `[Churn Risk — Tier 3] {account_name} — {days_to_renewal} days to renewal`

**Labels:** `churn-risk`, `tier-3`, `cs-escalation`

**Priority:** Urgent

**Assignee:** `cs_manager` from the account record, if present. If absent,
issue is created unassigned and the write log flags `manual_assignment_required: true`.

**Description body** includes:
- Account name, ACV, renewal date and days
- Bulleted list of signals fired
- Required actions checklist (3 items)
- Escalation path and expected response time (48 hours)
- G5 disclaimer: *"This flag is an analytical input. The CSM and manager own the decision."*
- Timestamp and attribution footer

---

## Slack Alert Format

### Section structure

| Section | Always shown | Condition |
|---------|-------------|-----------|
| Header (company, accounts evaluated, confidence, timestamp) | ✓ | — |
| Tier 3 at-risk table | — | tier3_accounts non-empty |
| Tier 2 watch list | — | tier2_accounts non-empty |
| Tier 1 summary | ✓ | — |
| Data freshness (G6) | ✓ | — |
| G5 disclaimer | ✓ | — |

### Sample Tier 3 section

```
⚠️ Tier 3 — Late-Stage Risk (2 accounts)
90–120 days pre-renewal · Escalation required

| Account           | ACV    | Days to Renewal | Signals                                          | Owner        | Linear   |
|-------------------|--------|-----------------|--------------------------------------------------|--------------|----------|
| Acme Corp         | $220K  | 103 days        | health_score_declining, renewal_not_started      | Jane Smith   | LIN-4421 |
| Globex Industries | $185K  | 97 days         | support_ticket_spike, sponsor_gone_dark          | Tom Kaplan   | LIN-4422 |

Expected response: 48 hours · Escalation channel: #cs-leadership
```

### Sample Tier 2 section

```
🟡 Tier 2 — Early Warning (4 accounts)
30–90 days post-onboarding · CSM action recommended

| Account        | ACV   | Days Since Onboarding | Signals                   | CSM          |
|----------------|-------|-----------------------|---------------------------|--------------|
| Initech LLC    | $95K  | 67 days               | usage_below_adoption_curve | Maria Lopez  |
| Umbrella Co    | $72K  | 45 days               | champion_departure         | Carlos Vega  |
```

### Sample Tier 1 summary

```
📊 Tier 1 — Structural Risk Summary
8 accounts flagged at deal close
Top signals: discount_elevated, single_threaded
[Tier 1: Rule mode — upgrade to cohort mode when 6+ months of churn data available]
```

### Sample data freshness (G6)

```
Data freshness
HubSpot — 2026-05-15 09:14
CS Platform — 2026-05-15 08:58
```

---

## Channel Routing

| Condition | Primary channel | Tier 3 channel |
|-----------|----------------|----------------|
| Tier 3 accounts present | `alert_channel` (full report) | `tier3_channel` (Tier 3-only summary) |
| Tier 3 accounts absent | `alert_channel` (full report) | (no post) |

The Tier 3-only summary posted to `tier3_channel` contains the Tier 3 table
plus a reference back to the full report channel. It does not repeat the full alert.

---

## Data Gap Behavior

| Condition | Behavior | Confidence |
|-----------|----------|-----------|
| Both connectors live, data < 7 days | Full evaluation | High |
| CS platform unavailable | Tier 1 evaluates; Tier 2/3 health/usage signals marked unevaluable; `partial_evaluation=true` on affected accounts | Moderate |
| HubSpot unavailable | **Hard stop** — scan cannot run; orchestrator reports error and stops | — (scan aborted) |
| HubSpot data 7–30 days stale | Full evaluation with staleness warning | Moderate |
| HubSpot data > 30 days stale | Full evaluation with staleness warning | Low |
| Both connectors unavailable | Hard stop | — (scan aborted) |

When CS platform is unavailable, signals that require it are marked
`unevaluable` — not fabricated. The account is still surfaced with
`partial_evaluation: true` so the CSM can investigate manually.

---

## Confidence Bands

| Band | Condition |
|------|-----------|
| High | Both connectors live, data < 7 days old |
| Moderate | CS platform unavailable OR HubSpot data 7–30 days stale |
| Low | HubSpot data > 30 days stale |
| — (aborted) | HubSpot unavailable |

---

## Run Modes

| Mode | Command | Behavior |
|------|---------|----------|
| Standard run | `run churn scan` | Full evaluation, Linear confirmation gate, Slack delivery |
| Preview | `preview churn scan` | Full evaluation + Linear confirmation (if Tier 3 present), no Slack delivery |
| Scheduled | cron `0 8 * * 1` | Standard run at 08:00 every Monday |

For scheduled runs, set cron expression in your rev-ops plugin scheduler:
```
0 8 * * 1   # Every Monday at 08:00
0 8 1 * *   # First of every month at 08:00
```

---

## Completion Summary Format

```
Churn Signal Scanner — Run Complete
─────────────────────────────────────
Company:         Acme Corp
Tier 3 accounts: 2 — completed
Tier 2 accounts: 4
Tier 1 summary:  8 accounts flagged (rule mode)
Linear issues:   2 created
Posted to:       #revops-alignment, #cs-leadership
Confidence:      High
Run at:          2026-05-15T08:02:14Z
```

When Tier 3 accounts are present:
```
[Internal — CS leadership] — G7: escalation path assigned for all Tier 3 flags.
```

---

## Token Budget

| Stage | Estimated tokens |
|-------|-----------------|
| Orchestrator overhead + practice profile read | ~1,200 |
| churn-signal-collector (HubSpot + CS platform + evaluation) | ~4,000–8,000 (scales with portfolio size) |
| churn-escalation-writer (confirmation gate + Linear writes) | ~1,500–2,500 |
| churn-alert-poster (format + Slack delivery) | ~1,500–2,000 |
| **Total (typical mid-market portfolio, 50–150 accounts)** | **~8,000–14,000** |

---

## Guardrails

**G5** — All churn risk outputs include:
*"Health scores, deal classifications, and risk flags are analytical inputs.
The CSM or manager owns the decision."*

**G6** — Every alert surfaces data-as-of timestamps for both HubSpot and the
CS platform. Neither freshness line is ever omitted, even in degraded mode.

**G7** — Every Tier 3 flag in the alert must name: owner (cs_manager),
escalation channel (#cs-leadership), and expected response time (48 hours).
A risk flag without an owner is noise. The alert-poster enforces this on every
Tier 3 row.

---

## Subagent Reference

| Subagent | Spec file | Purpose |
|----------|-----------|---------|
| churn-signal-collector | `subagents/churn-signal-collector.md` | Pulls HubSpot + CS platform data; evaluates Tier 1/2/3 signals |
| churn-escalation-writer | `subagents/churn-escalation-writer.md` | Human-confirmed Linear issue creation for Tier 3 |
| churn-alert-poster | `subagents/churn-alert-poster.md` | Formats and delivers Slack alert |

---

## Related Files

| File | Description |
|------|-------------|
| `../../rev-ops/skills/` | Rev-ops skill library loaded by orchestrator |
| `~/.cs-agent/practice-profile.json` | Practice configuration (renewal windows, thresholds) |
| `steering-examples.json` | 10 behavioral test scenarios |
| `../capacity-monitor/` | Companion cookbook — CS headroom monitoring |
| `../gtm-pulse-runner/` | Companion cookbook — GTM KPI briefing |
