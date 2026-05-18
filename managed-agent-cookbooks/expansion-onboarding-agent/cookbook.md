# Expansion Onboarding Agent — Managed Agent Cookbook

**Agent type:** Event-driven orchestrator with 3 subagents  
**Cadence:** Event-driven (CSQL stage change to `won`) + daily sweep fallback (8:00 AM)  
**Trigger:** CSQL marked `won` in `rev-ops:csql-tracking` OR daily scheduled sweep  
**Output:** Expansion onboarding plans created in `csm:expansion-onboarding` + Slack notification listing new plans with onboarding IDs and M1 kickoff targets

---

## What This Agent Does

The Expansion Onboarding Agent bridges the gap between a won CSQL and a structured
expansion onboarding plan. When a Customer Success Qualified Lead reaches the `won`
stage in Rev-Ops tracking — meaning the expansion opportunity is committed and the
account has agreed to proceed — the CSM needs a kickoff-ready onboarding plan before
the first post-win touchpoint.

This agent automates that handoff. It scans `rev-ops:csql-tracking` for newly won
CSQLs that do not yet have an active expansion onboarding plan, creates a structured
four-milestone plan for each via `csm:expansion-onboarding operation=create`, and
notifies the CS team with onboarding IDs, account names, CSM assignments, and M1
kickoff target dates.

It runs event-driven when possible (immediately on a CSQL stage change) and falls back
to a daily morning sweep so that any CSQLs won outside business hours or outside the
event window are never missed.

**What it does not do:**
- It does not invoke `force=true` to override an existing active plan. If an active
  plan already exists for an account, it logs a skip and notifies the CSM — the CSM
  makes the call on force.
- It does not bypass the `adoption_confirmation` blocking gate. Plan closure requires
  explicit CSM confirmation; this agent handles plan creation only.
- It does not fabricate CSQL fields. If a CSQL record is missing required fields
  (`account_name`, `csql_id`, `arr_uplift`, `close_date`), the account is skipped with
  a logged warning.
- It does not create plans for accounts with a `closed` expansion onboarding plan. A
  new CSQL for the same account is a separate qualifying event — the CSM handles
  re-initiation explicitly.

**Outputs:**
- One expansion onboarding plan per qualifying CSQL (via `csm:expansion-onboarding
  operation=create`) with four-milestone scaffold
- Slack notification (or file notification if Slack not configured) listing all newly
  created plans: onboarding ID, account name, CSM assignment, arr_uplift, M1 kickoff
  target date
- Logged skip records for accounts excluded due to: existing active plan, missing
  required CSQL fields, closed plan status, or `create` operation failure

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

The orchestrator sequences subagents strictly and does not parallelize. CSQL Won Scanner
must complete before Onboarding Plan Creator is dispatched — plan creation depends on
the qualifying record set. Onboarding Plan Creator must complete before Notification
Composer is dispatched — the notification lists created plan IDs that are only known
after creation succeeds.

---

## Orchestrator System Prompt

```
You are the Expansion Onboarding Agent orchestrator for a Customer Success team. Your
job is to identify CSQLs that have reached the won stage and create a structured
expansion onboarding plan for each qualifying account via csm:expansion-onboarding.

Your configuration lives at:
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md

And company profile at:
~/.claude/plugins/config/claude-for-customer-success/company-profile.md

Read both before starting. Fields you need:
- rev-ops connector name (for csql-tracking queries)
- Default CSM assignment rule (if no CSM field in CSQL record)
- Notification output: Slack channel, file path, or both
- Slack connector name (if configured)
- look_back_hours: how far back to scan for newly won CSQLs (default: 26 hours,
  covers daily sweep overlap; use 2 hours for event-driven triggers)

Execution sequence:

STEP 1 — Dispatch CSQL Won Scanner
  Pass: rev-ops connector name, look_back_hours, today's date and time (UTC)
  The scanner will:
    - Query rev-ops:csql-tracking for records where csql_stage=won AND
      won_at timestamp is within the look_back_hours window
    - For each won CSQL, check whether an active expansion onboarding plan
      already exists (status != closed) for that account
    - Return: qualifying_csqls (records ready for plan creation) and
      skip_log (accounts excluded with reason)
  Do not proceed until CSQL Won Scanner returns a complete response.
  If qualifying_cqsls is empty: proceed to STEP 4 — Notification Composer
    will send a "no new plans" confirmation. Do not skip notification.

STEP 2 — Dispatch Onboarding Plan Creator
  Pass: qualifying_cqsls array from Step 1 (each record must include account_name,
    csql_id, arr_uplift, close_date, and csm — if csm is null, apply the default
    CSM assignment rule from config)
  The creator will:
    - Call csm:expansion-onboarding operation=create for each record
    - Capture the returned onboarding_id, plan_status, and m1_kickoff_date per account
    - If creation returns a duplicate-plan warning: add to skip_log with reason
      "active plan exists — force=true required"; do NOT retry with force=true
    - If creation fails for any other reason: add to fail_log with the error
  Return: created_plans (onboarding_id, account_name, csm, arr_uplift, m1_kickoff_date
    per plan), skip_log (updated), fail_log (any hard failures)
  Do not proceed until Onboarding Plan Creator returns a complete response.

STEP 3 — Validate created plans
  Before dispatching Notification Composer, verify:
    - Every record in created_plans has a non-null onboarding_id
    - onboarding_id format is EXP-ONB-[ACCT]-[YYYYMMDD]
    - m1_kickoff_date is present and is a valid date
  If any record fails validation: move it from created_plans to fail_log with
    reason "invalid plan record — manual review required". Do not include
    unvalidated records in the notification.

STEP 4 — Dispatch Notification Composer
  Pass: created_plans, skip_log, fail_log, output targets (Slack/file),
    today's date, sweep type (event-driven or daily)
  Receive: formatted notification ready for delivery

STEP 5 — Deliver output
  If Slack configured: post mrkdwn notification to the configured channel.
  If file output configured: save markdown version to the configured path.
  Confirm delivery in your final response.

Rules:
- NEVER pass force=true to csm:expansion-onboarding under any circumstances.
  The duplicate-plan guard is intentional. If an active plan exists, the CSM
  decides whether to force. Surface the skip in the notification and stop.
- NEVER fabricate CSQL fields. If account_name, csql_id, arr_uplift, or close_date
  is null in a CSQL record, skip that account with reason "missing required field"
  and include it in the skip_log. Do not substitute estimates or placeholders.
- NEVER create plans for accounts where an existing plan has status=closed.
  A new CSQL for the same account is a new qualifying event — the CSM re-initiates
  explicitly. Skip with reason "closed plan on record — CSM re-initiation required".
- NEVER present arr_uplift as committed ARR. It is the projected uplift from the CSQL.
  Language in notifications: "projected uplift" not "confirmed ARR".
- If rev-ops:csql-tracking connector is unavailable: halt and notify the user with
  a clear error. Do not attempt fallback data sources.
- If zero qualifying CSQLs and zero skips in the look_back_hours window: this is a
  valid outcome. Notify: "No new won CSQLs in the past [N] hours. No plans created."
```

---

## Subagent 1: CSQL Won Scanner

**File:** `subagents/csql-won-scanner.md`

**Role:** Data retrieval and idempotency gate. The CSQL Won Scanner queries
`rev-ops:csql-tracking` for CSQLs that have reached the `won` stage within the
look-back window and filters out any accounts that already have an active expansion
onboarding plan — preventing duplicate plan creation before any `create` call is made.

**Tools required:**
- `rev-ops:csql-tracking` connector — required (CSQL records, stage, timestamps)
- `csm:expansion-onboarding` connector — required (existing plan status lookup)

**Inputs from orchestrator:**
- rev-ops connector name
- look_back_hours (default: 26 for daily sweep, 2 for event-driven)
- today's date and time (UTC)

**Idempotency check sequence:**
1. Query `rev-ops:csql-tracking` for records where `csql_stage=won` AND `won_at` is
   within the look_back_hours window
2. For each won CSQL, query `csm:expansion-onboarding` for any existing plan on the
   account (`operation=status` or equivalent lookup)
3. Classify each account:
   - **Qualifying:** no existing plan found, or only plan has `status=closed`
     → Wait — `closed` plans are NOT qualifying. See filter below.
   - **Skip — active plan:** existing plan with `status` ∈ {`active`, `in_progress`,
     `pending`} → add to skip_log, reason: "active plan exists — force=true required"
   - **Skip — closed plan:** existing plan with `status=closed` → add to skip_log,
     reason: "closed plan on record — CSM re-initiation required"
   - **Skip — missing fields:** `account_name`, `csql_id`, `arr_uplift`, or
     `close_date` is null → add to skip_log, reason: "missing required field: [field]"

**Output format:**
```
qualifying_cqsls:
  - account_name: [name]
    csql_id: [ID]
    csql_stage: won
    arr_uplift: [amount]
    close_date: [date]
    csm: [CSM name or null]
    won_at: [ISO 8601 timestamp]

skip_log:
  - account_name: [name]
    csql_id: [ID or null]
    skip_reason: [reason]
    won_at: [timestamp or null]

scan_summary:
  look_back_hours: [N]
  won_cqsls_found: [N]
  qualifying: [N]
  skipped: [N]
  scan_as_of: [ISO 8601 timestamp]
```

Return `qualifying_cqsls` as an empty array if no accounts qualify — do not omit the
key. Return `skip_log` as an empty array if no accounts were skipped.

**Full subagent spec:** See `subagents/csql-won-scanner.md`

---

## Subagent 2: Onboarding Plan Creator

**File:** `subagents/onboarding-plan-creator.md`

**Role:** Plan creation. The Onboarding Plan Creator calls
`csm:expansion-onboarding operation=create` for each qualifying CSQL record and
captures the returned onboarding ID, plan status, and M1 kickoff date. This subagent
enforces the no-force constraint: it never retries a duplicate-plan warning with
`force=true`. Any duplicate warning is treated as a skip event and passed back to
the orchestrator.

**Tools required:**
- `csm:expansion-onboarding` connector — required (plan creation)

**Inputs from orchestrator:**
- `qualifying_cqsls` array from CSQL Won Scanner (each record: `account_name`,
  `csql_id`, `arr_uplift`, `close_date`, `csm`)

**Creation call per qualifying CSQL:**
```
csm:expansion-onboarding
  operation: create
  account_name: [from qualifying record]
  csql_id: [from qualifying record]
  arr_uplift: [from qualifying record]
  close_date: [from qualifying record]
  csm_name: [from qualifying record, or default CSM from config if null]
```

**Handling creation outcomes:**

| Outcome | Action |
|---------|--------|
| Success — returns `onboarding_id`, `plan_status`, `m1_kickoff_date` | Add to `created_plans` |
| Duplicate plan warning (no `force=true` in call) | Add to `skip_log`, reason: "active plan exists — force=true required" |
| Hard failure (any non-duplicate error) | Add to `fail_log` with error detail |

**Output format:**
```
created_plans:
  - account_name: [name]
    csql_id: [ID]
    onboarding_id: [EXP-ONB-[ACCT]-[YYYYMMDD]]
    csm: [CSM name]
    arr_uplift: [amount]
    m1_kickoff_date: [date]
    plan_status: active

skip_log:
  - account_name: [name]
    csql_id: [ID]
    skip_reason: [reason]

fail_log:
  - account_name: [name]
    csql_id: [ID]
    error: [error message from skill]
```

Return all three keys even if empty. Do not omit `created_plans`, `skip_log`, or
`fail_log` from the response — the orchestrator validates against all three.

**Full subagent spec:** See `subagents/onboarding-plan-creator.md`

---

## Subagent 3: Notification Composer

**File:** `subagents/notification-composer.md`

**Role:** Output formatting and delivery preparation. The Notification Composer formats
the sweep results into a Slack notification (mrkdwn) and/or a markdown file. Plans lead
the notification; skips and failures are surfaced with enough detail for the CSM to
take action without requiring them to dig into logs.

**Tools required:**
- Slack connector (if Slack output configured)

**Output format (markdown version):**

```markdown
## Expansion Onboarding — New Plans Created — [date]
*[N] plan(s) created · [N] skipped · [N] failed*
*[event-driven | daily sweep] · Generated by Claude Expansion Onboarding Agent*

---

### ✅ New Onboarding Plans ([N])

**[Account Name]**
- Onboarding ID: `EXP-ONB-[ACCT]-[YYYYMMDD]`
- CSM: [Name]
- Projected uplift: $[arr_uplift]
- M1 Kickoff target: [date]

---

### ⏭️ Skipped ([N])
*These accounts were not processed. CSM action may be required.*

| Account | CSQL ID | Reason |
|---------|---------|--------|
| [name] | [ID] | [skip reason] |

---

### ❌ Failed ([N])
*Plan creation failed for these accounts. Manual review required.*

| Account | CSQL ID | Error |
|---------|---------|-------|
| [name] | [ID] | [error detail] |

---

*Sweep type: [event-driven | daily sweep] · Look-back: [N] hours*
*[N] won CSQLs found in window · [N] qualified · [N] skipped · [N] failed*
*Generated [ISO 8601 timestamp]*
```

**Guardrails for Composer:**
- If `created_plans` is empty and `skip_log` is empty and `fail_log` is empty:
  output exactly: "No new won CSQLs in the past [N] hours. No plans created."
  Do not add sections or tables — there is nothing to report.
- If `created_plans` is empty but skips or failures exist: include the Skipped and/or
  Failed sections with no Plans Created section. Do not suppress skips when no plans
  were created — skips often require CSM attention.
- Use "projected uplift" consistently for `arr_uplift` — never "committed ARR" or
  "expansion revenue."
- Skip reasons must be verbatim from the `skip_log` — do not rephrase or soften them.
  "active plan exists — force=true required" must appear exactly as stated so CSMs
  know the required resolution action.
- Failed accounts must show the raw error from `fail_log` — do not summarize as
  "an error occurred."
- The notification is for the CS team channel — it must not include internal config
  values, connector names, or file paths.

**Full subagent spec:** See `subagents/notification-composer.md`

---

## Connector Requirements

| Connector | Required | Purpose |
|-----------|----------|---------|
| `rev-ops:csql-tracking` | Yes | CSQL records, stage status, won timestamp, arr_uplift |
| `csm:expansion-onboarding` | Yes | Active plan status lookup (idempotency check) + plan creation |
| Slack | Optional | CS team channel notification delivery |

The agent requires both `rev-ops:csql-tracking` and `csm:expansion-onboarding` to run.
If either connector is unavailable, the orchestrator halts and notifies the user —
there is no graceful degradation path because CSQL data is the sole input and plan
creation is the sole output.

If Slack is not configured, notifications are written to the configured file path.
If neither Slack nor file output is configured, the orchestrator surfaces the sweep
results inline and prompts the user to configure an output channel.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

**Required config fields:**
- `revops_connector`: Name of the `rev-ops:csql-tracking` MCP connector
- `expansion_onboarding_connector`: Name of the `csm:expansion-onboarding` MCP connector
- `onboarding_output`: `file` | `slack` | `both`

**Optional config fields:**
- `look_back_hours_daily`: Hours to scan during daily sweep (default: `26`)
- `look_back_hours_event`: Hours to scan on event-driven trigger (default: `2`)
- `default_csm`: CSM name to assign when CSQL record has no CSM field
- `slack_connector`: Required if output includes Slack
- `slack_channel`: Slack channel for plan notifications (default: `#cs-expansions`)
- `onboarding_file_path`: Required if output includes file
- `exclude_accounts`: Account names to exclude from sweep (comma-separated)

If required fields are `[PLACEHOLDER]`, prompt:
> "Run `/csm:cold-start-interview --section expansion-onboarding` to configure the
> Expansion Onboarding Agent before running this agent."

---

## Scheduling

**Daily sweep — 8:00 AM Monday through Friday:**
```
cronExpression: "0 8 * * 1-5"
prompt: "Run the Expansion Onboarding Agent daily sweep."
```

The daily sweep uses `look_back_hours: 26` to ensure overlap with the prior day's
sweep and catch any CSQLs marked won outside business hours or over the weekend.

**Weekend coverage — Friday 8:00 AM through Monday 8:00 AM** is handled by the Monday
sweep with an extended look-back. If weekend coverage is critical, add a Saturday
sweep:

```
cronExpression: "0 8 * * 6"
prompt: "Run the Expansion Onboarding Agent weekend sweep."
```

**Event-driven trigger** (preferred when available): Configure your CRM or Rev-Ops
workflow to invoke the agent when a CSQL stage changes to `won`. Use
`look_back_hours: 2` for event-driven invocations to avoid reprocessing prior sweeps.

On-demand invocation: "Run the expansion onboarding agent" or "Check for new won
CSQLs and create onboarding plans" or "Any new CSQLs that need onboarding plans?"

---

## Sample Output (abbreviated)

```
## Expansion Onboarding — New Plans Created — May 18, 2026
*2 plan(s) created · 1 skipped · 0 failed*
*daily sweep · Generated by Claude Expansion Onboarding Agent*

---

### ✅ New Onboarding Plans (2)

**Meridian Labs**
- Onboarding ID: `EXP-ONB-MERIDIAN-20260518`
- CSM: Priya Sharma
- Projected uplift: $48,000
- M1 Kickoff target: May 25, 2026

**Nora Systems**
- Onboarding ID: `EXP-ONB-NORA-20260518`
- CSM: James Park
- Projected uplift: $22,500
- M1 Kickoff target: May 26, 2026

---

### ⏭️ Skipped (1)

| Account | CSQL ID | Reason |
|---------|---------|--------|
| BlueField Tech | CSQL-2026-0041 | active plan exists — force=true required |

---

### ❌ Failed (0)

---

*Sweep type: daily sweep · Look-back: 26 hours*
*3 won CSQLs found in window · 2 qualified · 1 skipped · 0 failed*
*Generated 2026-05-18T08:01:14Z*
```
