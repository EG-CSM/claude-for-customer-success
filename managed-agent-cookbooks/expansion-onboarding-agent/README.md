# Expansion Onboarding Agent

**Agent type:** Event-driven orchestrator with 3 subagents  
**Cadence:** Event-driven (CSQL stage change to `won`) + daily sweep fallback (8:00 AM)  
**Trigger:** CSQL marked `won` in `rev-ops:csql-tracking` OR daily scheduled sweep  
**Cookbook:** [`cookbook.md`](./cookbook.md)

---

## What This Agent Does

The Expansion Onboarding Agent bridges the gap between a won CSQL and a structured expansion onboarding plan. When a Customer Success Qualified Lead reaches the `won` stage in Rev-Ops tracking — meaning the expansion opportunity is committed and the account has agreed to proceed — the CSM needs a kickoff-ready onboarding plan before the first post-win touchpoint.

A CSQL (Customer Success Qualified Lead) progresses through four stages: `qualified → proposed → verbal → won`. This agent triggers at `won` only. Earlier stages represent pipeline activity, not confirmed expansions, and are not processed.

It runs event-driven when possible (immediately on a CSQL stage change) and falls back to a daily morning sweep so that any CSQLs won outside business hours or outside the event window are never missed.

**Outputs:**

- One expansion onboarding plan per qualifying CSQL (via `csm:expansion-onboarding operation=create`) with four-milestone scaffold
- Slack notification (or file notification if Slack not configured) listing all newly created plans: onboarding ID, account name, CSM assignment, committed ARR uplift, M1 kickoff target date
- Logged skip records for accounts excluded due to: existing active plan, missing required CSQL fields, closed plan status, or `create` operation failure

**What it does not do:**

- Does not invoke `force=true` to override an existing active plan — the CSM resolves that directly
- Does not create plans for accounts with a `closed` expansion onboarding plan — CSM re-initiates
- Does not fabricate CSQL fields — accounts with missing `account_name`, `csql_id`, `arr_uplift`, or `close_date` are skipped with a logged warning
- Does not write back to CSQL records — read-only access to `rev-ops:csql-tracking`
- Does not track milestone progress — M1–M4 completion is managed by the CSM in `csm:expansion-onboarding`

---

## Architecture

```
Orchestrator: Expansion Onboarding Agent
│
├── Subagent 1: CSQL Won Scanner
│   Queries rev-ops:csql-tracking for CSQLs in stage=won that do not have an
│   active expansion onboarding plan. Returns qualifying CSQL records with all
│   fields required for plan creation. Also returns skip log for accounts
│   excluded by idempotency or data-quality checks.
│
├── Subagent 2: Onboarding Plan Creator
│   Dispatches csm:expansion-onboarding operation=create for each qualifying
│   CSQL record. Receives onboarding_id, plan status, and M1 kickoff date per
│   account. Enforces idempotency — never passes force=true. Returns created
│   plan records and any creation failures.
│
└── Subagent 3: Notification Composer
    Formats the Slack notification (or file notification) summarising all newly
    created onboarding plans. Lists each plan: onboarding_id, account, CSM,
    arr_uplift, M1 kickoff target. Flags any skip records for CSM awareness.
    Delivers to configured output channel.
```

Subagents execute **sequentially** — this is a correctness requirement, not a performance choice. The Scanner must complete before the Creator is dispatched (qualifying records must exist before plan creation). The Creator must complete before the Notification Composer is dispatched (actual onboarding IDs must exist before the notification references them).

---

## Prerequisites

### Required Connectors

| Connector | MCP Tool | Used For |
|-----------|----------|----------|
| `rev-ops:csql-tracking` | CSQL Won Scanner | Query won CSQLs within look-back window |
| `csm:expansion-onboarding` | CSQL Won Scanner + Onboarding Plan Creator | Idempotency check (`operation=status`) and plan creation (`operation=create`) |

### Optional Connectors

| Connector | MCP Tool | Used For |
|-----------|----------|----------|
| Slack | Notification Composer | Post sweep results to CS team channel |

If Slack is not connected, notifications are written to the configured file path. If neither is configured, the orchestrator surfaces results inline and prompts for output configuration.

---

## Configuration

The agent reads from:
```
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md
```

If required fields are `[PLACEHOLDER]`, run:
```
/csm:cold-start-interview --section expansion-onboarding
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `revops_connector` | string | Name of the `rev-ops:csql-tracking` MCP connector |
| `expansion_onboarding_connector` | string | Name of the `csm:expansion-onboarding` MCP connector |
| `onboarding_output` | `file` \| `slack` \| `both` | Output delivery method for sweep notifications |

### Conditionally Required Fields

These fields are required based on the value of `onboarding_output`. The agent halts at startup if a conditionally required field is missing.

| Field | Required When | Description |
|-------|---------------|-------------|
| `slack_connector` | `onboarding_output` is `slack` or `both` | Name of the Slack MCP connector |
| `onboarding_file_path` | `onboarding_output` is `file` or `both` | File path for notification output |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `look_back_hours_daily` | `26` | Hours to scan during daily sweep (overlap buffer ensures no gaps between sweeps) |
| `look_back_hours_event` | `2` | Hours to scan on event-driven trigger |
| `slack_channel` | `#cs-expansions` | Slack channel for plan notifications |
| `default_csm` | _(none)_ | CSM name to assign when CSQL record has no CSM field. Without this, accounts missing the CSM field are skipped. |
| `exclude_accounts` | _(none)_ | Comma-separated account names to exclude from every sweep |
| `account_id_format` | `EXP-ONB-[ACCT]-[YYYYMMDD]` | Format string for onboarding ID generation. **Note:** Custom formats require a corresponding update to the STEP 3 validation logic — the default format is hardcoded in validation. |
| `dry_run` | `false` | If `true`, runs the full scan but skips all `operation=create` calls. Notification shows `[DRY RUN]` prefix. Run with `dry_run: true` to validate scan results before enabling live scheduling. |

---

## Scheduling

### Daily Sweep — Monday through Friday, 8:00 AM UTC

```
cronExpression: "0 8 * * 1-5"
timezone: UTC
prompt: "Run the Expansion Onboarding Agent daily sweep."
```

The `look_back_hours: 26` overlap buffer ensures no CSQLs are missed between sweeps.

**Weekend coverage:** The Monday 8:00 AM sweep with 26-hour look-back reaches back to Saturday 6:00 AM — it does NOT cover Friday 8:00 AM through Saturday 6:00 AM. For full weekend coverage, add a Saturday sweep:

```
cronExpression: "0 8 * * 6"
timezone: UTC
prompt: "Run the Expansion Onboarding Agent weekend sweep."
```

> **Timezone note:** These cron expressions are in UTC. Convert to local time if your scheduling platform uses local time by default.

### Event-Driven Trigger (Preferred)

Configure your CRM or Rev-Ops workflow to invoke the agent when a CSQL stage changes to `won`:

```json
{
  "prompt": "Run the Expansion Onboarding Agent event-driven trigger.",
  "config_override": { "look_back_hours_event": 2 }
}
```

**`config_override` allowlist** — only these fields may be overridden via webhook:

| Field | Type | Notes |
|-------|------|-------|
| `look_back_hours_event` | number (1–168) | Hours for this event invocation |
| `look_back_hours_daily` | number (1–168) | Override daily sweep look-back |
| `dry_run` | boolean | Override dry_run for this invocation only |
| `slack_channel` | string | Override notification channel |

All other config fields (`revops_connector`, `expansion_onboarding_connector`, `onboarding_output`, `slack_connector`, `onboarding_file_path`, `exclude_accounts`, `account_id_format`, `default_csm`) cannot be overridden via webhook.

### On-Demand Invocation

Phrase any of these to the agent:

- "Run the expansion onboarding agent"
- "Check for new won CSQLs and create onboarding plans"
- "Any new CSQLs that need onboarding plans?"

Default scan window for on-demand invocations: `look_back_hours: 24`. For recovery invocations following an outage or missed sweep, supply an explicit `look_back_hours` value matching the outage window.

### Concurrent Sweep Protection

Two simultaneous sweeps can both pass the idempotency check before either creates a plan — resulting in duplicate plan creation. For production deployments, configure an external locking mechanism:

- **Preferred:** Enforce single-flight execution at the webhook gateway (reject or queue concurrent invocations for the same agent)
- **Alternative:** Distributed lock (e.g., Redis SETNX) keyed on agent identity + sweep date
- **Minimum viable:** 429 response from the webhook endpoint if a sweep is already in progress

The cookbook's `operation=status` idempotency check reduces but does not eliminate the race window.

---

## Output Reference

### Empty Sweep

```
No new won CSQLs in the past [N] hours. No plans created.
```

### Standard Notification

```
## Expansion Onboarding — New Plans Created — [date]
*[N] plan(s) created · [N] skipped · [N] failed*
*[event-driven | daily sweep] · Generated by Claude Expansion Onboarding Agent*

---

### ✅ New Onboarding Plans ([N])

**[Account Name]**
- Onboarding ID: `EXP-ONB-[ACCT]-[YYYYMMDD]`
- CSM: [Name]
- Committed ARR uplift: $[amount]
- M1 Kickoff target: [date]

---

### ⏭️ Skipped ([N])
*These accounts were not processed. CSM action may be required.*

| Account | CSQL ID | Reason |
|---------|---------|--------|

---

### ❌ Failed ([N])
*Plan creation failed for these accounts. Manual review required.*

| Account | CSQL ID | Error |
|---------|---------|-------|
```

**Section inclusion:** Sections are included only when non-empty. If `created_plans` is empty but skips or failures exist, only the relevant sections appear — skips and failures are never suppressed.

**Dry run:** The header reads `[DRY RUN] Expansion Onboarding — Plans That Would Be Created — [date]`. No plans are created and no Slack messages are sent.

**ARR uplift language:** Always "committed ARR uplift" — never "projected uplift", "estimated uplift", or "expansion revenue". At the `won` stage, the expansion is committed.

---

## Data Gap Behavior

| Gap | Behavior |
|-----|----------|
| Missing `account_name`, `csql_id`, `arr_uplift`, or `close_date` | Skip with specific reason logged; account excluded from qualifying set |
| `csm` field null, `default_csm` not configured | Skip with reason "missing required field: csm — no default_csm configured" |
| `csm` field null, `default_csm` configured | Assign `default_csm`; proceed to qualifying set |
| Active plan exists for CSQL (`active`, `in_progress`, `pending`, `pending_activation`, `initializing`) | Skip with reason "active plan exists — force=true required" |
| Closed plan on record | Skip with reason "closed plan on record — CSM re-initiation required" |
| `csm:expansion-onboarding` unavailable mid-loop | All remaining unprocessed accounts added to fail_log; notification sent listing created + failed accounts |
| `m1_kickoff_date` not returned by connector | Derived as `close_date + 5 business days` |
| `m1_kickoff_date` not returned and `close_date` missing | Account added to fail_log with reason "m1_kickoff_date unavailable and close_date missing — cannot derive M1 target" |
| Slack delivery fails | Attempt file output; if file also fails, notification surfaced inline in orchestrator response |

---

## Subagent Reference

| Subagent | Spec | YAML | Connectors | Writes |
|----------|------|------|-----------|--------|
| CSQL Won Scanner | [`subagents/csql-won-scanner.md`](./subagents/csql-won-scanner.md) | [`subagents/csql-won-scanner.yaml`](./subagents/csql-won-scanner.yaml) | `rev-ops:csql-tracking` (read only), `csm:expansion-onboarding` (`operation=status` only) | None |
| Onboarding Plan Creator | [`subagents/onboarding-plan-creator.md`](./subagents/onboarding-plan-creator.md) | [`subagents/onboarding-plan-creator.yaml`](./subagents/onboarding-plan-creator.yaml) | `csm:expansion-onboarding` (`operation=create` only; never `force=true`) | None |
| Notification Composer | [`subagents/notification-composer.md`](./subagents/notification-composer.md) | [`subagents/notification-composer.yaml`](./subagents/notification-composer.yaml) | Slack (post message) | File (optional) |
