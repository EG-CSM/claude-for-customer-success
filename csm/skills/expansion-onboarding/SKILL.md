---
name: csm:expansion-onboarding
version: "1.0.0"
description: >
  Generate and track structured expansion onboarding plans for accounts where a CSQL
  has been won. Three operations: create (new plan from won CSQL context), update
  (milestone progress and notes), close (adoption confirmation and plan closure).
  Operates at Stage 4 of the CS Journey. Bridges rev-ops:csql-tracking won event
  to CSM-led adoption execution.
deployment_target: plugin
enhancement_level: P1
task_id: expansion-onboarding
duration_minutes: 2
lifecycle_stage: stage-4-expansion
---

# /csm:expansion-onboarding

[VALIDATED]

> **Quality gate:** critical-skill-evaluator run 2026-05-18. Three WARNs resolved:
> W1 ✓ — nested `metadata:` block removed from frontmatter (plugin parser incompatible with nested YAML objects).
> W2 ✓ — `xml_structural_escape()` and `scan_for_injection()` extracted to `reference/injection-defense.md`; inline replaced with stubs. Worked examples 2 and 3 moved to reference file; one canonical example retained inline.
> W3 ✓ — formal two-column field mapping table added to Dependencies section for `rev-ops:csql-tracking` → `csm:expansion-onboarding` inter-skill contract.
> Zero BLOCK findings. Promoted to VALIDATED.

## Overview

Generate and track structured expansion onboarding plans for Customer Success Managers
working post-CSQL-win at Stage 4 of the CS Journey. Three operations cover the full
lifecycle of an expansion onboarding engagement:

- **create**: Generates a new structured onboarding plan from a won CSQL context.
  Produces the primary CSM execution artifact for the post-close expansion adoption
  phase, including a four-milestone scaffold, stakeholder assignments, and success
  definition.
- **update**: Appends milestone progress, revised target dates, and CSM notes to an
  active plan. Append-only; prior state is always preserved.
- **close**: Marks expansion onboarding complete with a mandatory adoption confirmation
  statement. Plan becomes read-only after close.

**Service context:** Expansion & Growth service, Stage 4 CS Journey. This skill is the
operational bridge between a `rev-ops:csql-tracking` won event and CSM-led adoption
execution. Context file output (`context/expansion-onboarding-[safe_account]-[YYYY-MM-DD].md`)
is the system of record for the onboarding engagement. One active plan per account at
a time.

---

## Use When

- A CSQL has transitioned to `won` and the CSM is ready to initiate the expansion
  onboarding motion
- CSM needs a structured milestone scaffold for tracking expansion adoption from close
  to confirmed adoption
- Milestone progress or target dates need to be recorded against an active plan
- Expansion adoption has been confirmed and the onboarding record needs to be closed
- CSM manager or AE handoff requires a documented expansion onboarding artifact

## Do NOT Use For

- CSQL deal management or status transitions (use `rev-ops:csql-tracking`)
- Drafting customer-facing communications (use `csm:customer-comms`)
- Full Success Plan canvas generation (use `csm:success-plan-canvas`)
- Health score calculation (use `csm:health-monitor`)
- Renewal risk analysis (use `csm:renewal-risk-assessment`)
- Multi-account batch onboarding plans
- Initial onboarding for new customers (this skill is expansion-only)
- CRM integration or calendar sync

## Typical Activation

- "Start expansion onboarding for Acme Corp — they just signed the enterprise upgrade"
- "Update M2 to complete for the Globex expansion onboarding"
- "Close the Springfield Industries expansion onboarding — 47 of 50 seats active"
- "Create an onboarding plan for the TechCo seat expansion from the CSQL win today"

---

## Parameters

### create

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | `"create"` |
| `account_name` | string | Yes | Account name from won CSQL |
| `csm_name` | string | Yes | CSM who owns the expansion onboarding |
| `expansion_product` | string | Yes | Expansion product, tier, or seat count from won CSQL |
| `csql_id` | string | No | CSQL record ID from `rev-ops:csql-tracking` — stored for traceability |
| `champion` | string | No | Customer champion from CSQL MEDDIC context |
| `ae_owner` | string | No | AE who closed the deal — for handoff documentation |
| `close_date` | string | No | ISO date of deal close. Defaults to today if absent. |
| `onboarding_horizon_days` | integer | No | Expected onboarding duration. One of: `30`, `60`, `90`. Default: `60`. |
| `success_definition` | string | No | CSM-defined statement of what "expansion adopted" means for this account |
| `notes` | string | No | Additional context or CSM notes for the onboarding record |
| `force` | boolean | No | Set `true` to create a new plan when an active plan already exists for the account. Required to bypass duplicate guard. |

### update

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | `"update"` |
| `account_name` | string | Yes | Account name — used to locate existing onboarding file |
| `onboarding_id` | string | No | Onboarding record ID. If absent, defaults to most recent active plan for account. |
| `milestone_updates` | list | No | List of milestone update objects (see schema below) |
| `notes` | string | No | Progress notes appended to record (append-only; prior notes preserved) |

**Milestone Update Object schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `milestone` | string | Yes | One of: `M1`, `M2`, `M3`, `M4` |
| `status` | string | Yes | One of: `pending`, `in_progress`, `complete`, `blocked` |
| `target_date` | string | No | Revised ISO target date for this milestone |
| `completion_date` | string | No | Actual completion date (required when status = `complete`) |
| `notes` | string | No | Milestone-specific notes |

### close

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | `"close"` |
| `account_name` | string | Yes | Account name — used to locate existing onboarding file |
| `onboarding_id` | string | No | Onboarding record ID. Defaults to most recent active plan for account. |
| `adoption_confirmation` | string | **Yes (BLOCKING)** | Statement confirming expansion adoption (e.g., "50 seats provisioned, 38 active users within 14 days of go-live"). Cannot be empty. |
| `closure_date` | string | No | ISO date of closure. Defaults to today. |
| `notes` | string | No | Closing notes appended to record |

---

## Execution Flow

### Phase 1: CLASSIFY

**Step 1 — Operation determination**

Parse `operation` parameter:
- If `operation` is present and equals `create`, `update`, or `close` → proceed
- If `operation` is absent or invalid → AskUserQuestion:
  ```
  question: "Which operation do you want to perform?"
  header: "Expansion Onboarding Operation"
  options:
    - label: "Create"
      description: "Generate a new expansion onboarding plan from a won CSQL"
    - label: "Update"
      description: "Record milestone progress or append notes to an active plan"
    - label: "Close"
      description: "Confirm adoption and close a completed onboarding plan"
  ```

**Step 2 — Display/safe name separation**

Initialize `display_account` and `safe_account` before any filesystem or output operations:

**Implementation:** See `reference/injection-defense.md` — `xml_structural_escape()` section.
Five-step HTML/Unicode injection defense: html.unescape → NFKC normalization → strip raw `<>` → HTML entity regex → Unicode homoglyph iteration (10 chars).

```python
import html, unicodedata, re

display_account = xml_structural_escape(account_name)  # document output only
safe_account = re.sub(r'[^\w\-]', '_', display_account)  # filesystem ops only
safe_csm_name = xml_structural_escape(csm_name) if csm_name else ''
```

**Step 3 — Operation-specific validation**

*For `create`:*
```python
# Required field check
if not account_name or not account_name.strip():
    raise ValueError("account_name is required for create operation.")
if not csm_name or not csm_name.strip():
    raise ValueError("csm_name is required for create operation.")
if not expansion_product or not expansion_product.strip():
    raise ValueError("expansion_product is required for create operation.")

# Horizon validation
valid_horizons = {30, 60, 90}
horizon = onboarding_horizon_days if onboarding_horizon_days is not None else 60
if horizon not in valid_horizons:
    raise ValueError(
        f"onboarding_horizon_days must be 30, 60, or 90. Received: {horizon}."
    )

# Duplicate plan guard
import glob
existing_plans = glob.glob(f"context/expansion-onboarding-{safe_account}-*.md")
active_plans = [p for p in existing_plans if _plan_is_active(p)]
if active_plans and not force:
    # Warn and block — require force=true
    raise ValueError(
        f"An active expansion onboarding plan already exists for "
        f"{display_account}: {active_plans[0]}. "
        f"To create a new plan and supersede it, set force=true. "
        f"To update the existing plan, use operation=update."
    )
```

*For `update`:*
```python
# Locate active plan
plan_file = _locate_active_plan(safe_account)
if not plan_file:
    raise ValueError(
        f"No active expansion onboarding plan found for {display_account}. "
        f"Run create first."
    )

# Check plan is not closed
if _plan_is_closed(plan_file):
    onboarding_id = _read_field(plan_file, 'onboarding_id')
    raise ValueError(
        f"Onboarding record {onboarding_id} is closed. "
        f"Open a new expansion onboarding plan for a subsequent expansion on this account."
    )

# Immutable field guard
IMMUTABLE_FIELDS = {'onboarding_id', 'created_at', 'created_by', 'account_name', 'expansion_product'}
attempted_updates = set(kwargs.keys()) & IMMUTABLE_FIELDS
if attempted_updates:
    raise ValueError(
        f"Cannot update immutable field(s): {', '.join(sorted(attempted_updates))}. "
        f"These fields are set at create and cannot be changed."
    )
```

*For `close`:*
```python
# Locate active plan
plan_file = _locate_active_plan(safe_account)
if not plan_file:
    raise ValueError(
        f"No active expansion onboarding plan found for {display_account}. "
        f"Run create first."
    )

# BLOCKING gate: adoption_confirmation must be non-empty
if not adoption_confirmation or not adoption_confirmation.strip():
    raise ValueError(
        "adoption_confirmation is required to close an expansion onboarding plan. "
        "Provide a statement confirming expansion adoption before closing "
        "(e.g., '50 seats provisioned, 38 active users within 14 days of go-live')."
    )
```

---

### Phase 2: PRE-FLIGHT

**Step 1 — Apply `xml_structural_escape()` to all user-provided string inputs**

Apply to every string parameter before any use:
```python
safe_expansion_product = xml_structural_escape(expansion_product) if expansion_product else ''
safe_champion = xml_structural_escape(champion) if champion else ''
safe_ae_owner = xml_structural_escape(ae_owner) if ae_owner else ''
safe_csql_id = xml_structural_escape(csql_id) if csql_id else ''
safe_success_definition = xml_structural_escape(success_definition) if success_definition else ''
safe_notes = xml_structural_escape(notes) if notes else ''
safe_close_date = xml_structural_escape(close_date) if close_date else ''
safe_closure_date = xml_structural_escape(closure_date) if closure_date else ''
safe_adoption_confirmation = xml_structural_escape(adoption_confirmation) if adoption_confirmation else ''

# For update: escape all milestone update string fields
safe_milestone_updates = []
if milestone_updates:
    for mu in milestone_updates:
        safe_mu = {
            'milestone': xml_structural_escape(str(mu.get('milestone', ''))),
            'status': xml_structural_escape(str(mu.get('status', ''))),
            'target_date': xml_structural_escape(str(mu.get('target_date', ''))) if mu.get('target_date') else '',
            'completion_date': xml_structural_escape(str(mu.get('completion_date', ''))) if mu.get('completion_date') else '',
            'notes': xml_structural_escape(str(mu.get('notes', ''))) if mu.get('notes') else '',
        }
        safe_milestone_updates.append(safe_mu)
```

**Step 2 — Layer 2 semantic injection scan**

**Implementation:** See `reference/injection-defense.md` — `scan_for_injection()` section.
13-pattern semantic injection scan across all user-supplied string inputs.

```python
# Scan all escaped string inputs
inputs_to_scan = [
    safe_csm_name, safe_expansion_product, safe_champion, safe_ae_owner,
    safe_csql_id, safe_success_definition, safe_notes, safe_close_date,
    safe_closure_date, safe_adoption_confirmation,
]
# Also scan milestone update strings
for mu in safe_milestone_updates:
    inputs_to_scan.extend([mu['milestone'], mu['status'], mu.get('notes', '')])

for val in inputs_to_scan:
    if val and scan_for_injection(val):
        raise ValueError(
            "Input rejected: potential prompt injection detected. "
            "Please review your inputs and remove any instruction-like content."
        )
```

---

### Phase 3: OPERATE

**Step 1 — Mode-conditional execution**

*create operation:*

```python
from datetime import datetime, date, timedelta

# Generate onboarding_id
def _make_onboarding_id(account_name: str, create_date: date) -> str:
    """
    EXP-ONB-[ACCT]-[YYYYMMDD]
    ACCT = first 4 alpha chars of account_name, uppercased, padded with X if fewer than 4.
    """
    alpha_chars = [c for c in account_name if c.isalpha()]
    acct = ''.join(alpha_chars[:4]).upper()
    acct = acct.ljust(4, 'X')  # pad with X if fewer than 4 alpha chars
    return f"EXP-ONB-{acct}-{create_date.strftime('%Y%m%d')}"

create_date = date.today()
onboarding_id = _make_onboarding_id(display_account, create_date)
created_at = datetime.now().isoformat()
plan_status = 'active'

# Parse close_date
if safe_close_date:
    close_dt = date.fromisoformat(safe_close_date)
else:
    close_dt = date.today()

# Calculate milestone target dates (calendar days)
m1_target = close_dt + timedelta(days=3)
m2_target = close_dt + timedelta(days=round(horizon * 0.20))
m3_target = close_dt + timedelta(days=round(horizon * 0.70))
m4_target = close_dt + timedelta(days=horizon)

# Build context file content
file_date = create_date.strftime('%Y-%m-%d')
file_path = f"context/expansion-onboarding-{safe_account}-{file_date}.md"

context_content = f"""# Expansion Onboarding Plan: {display_account}

**Onboarding ID:** {onboarding_id}
**Account:** {display_account}
**CSM:** {safe_csm_name}
**AE:** {safe_ae_owner or "[Unassigned]"}
**Champion:** {safe_champion or "[Identify — confirm with AE]"}
**Expansion product:** {safe_expansion_product}
**CSQL reference:** {safe_csql_id or "[Not provided]"}
**Status:** {plan_status}
**Created:** {created_at}
**Horizon:** {horizon} days

---

## Success Definition

{safe_success_definition or "[CSM to define — what does adoption look like for this expansion?]"}

---

## Milestone Schedule

| Milestone | Description | Target Date | Status | Completed |
|-----------|-------------|-------------|--------|-----------|
| M1 | Kickoff | {m1_target.isoformat()} | pending | — |
| M2 | Configuration complete | {m2_target.isoformat()} | pending | — |
| M3 | Adoption gate | {m3_target.isoformat()} | pending | — |
| M4 | Onboarding confirmed | {m4_target.isoformat()} | pending | — |

*Note: M1 target date is a suggested date based on calendar days from close date.*

---

## Progress Log

*(No updates recorded yet.)*

---

## Notes

{safe_notes or "*(No initial notes provided.)*"}

---

## Closure Record

**Adoption confirmation:** —
**Closure date:** —
**Closing notes:** —
"""

# Write file (create context/ if it does not exist)
import os
os.makedirs('context', exist_ok=True)
with open(file_path, 'w') as f:
    f.write(context_content)

# Return console summary
return {
    'onboarding_id': onboarding_id,
    'file_path': file_path,
    'account': display_account,
    'expansion_product': safe_expansion_product,
    'status': plan_status,
    'milestone_scaffold': {
        'M1_kickoff': m1_target.isoformat(),
        'M2_configuration_complete': m2_target.isoformat(),
        'M3_adoption_gate': m3_target.isoformat(),
        'M4_onboarding_confirmed': m4_target.isoformat(),
    }
}
```

*update operation:*

```python
# Locate most recent active plan
plan_file = _locate_active_plan(safe_account)
update_timestamp = datetime.now().isoformat()

# Update Milestone Schedule table in place (overwrite milestone status/dates)
if safe_milestone_updates:
    _apply_milestone_updates(plan_file, safe_milestone_updates)

# Append timestamped update block to Progress Log (append-only)
if safe_notes or safe_milestone_updates:
    update_block = f"""
---

### Update — {update_timestamp}

"""
    if safe_milestone_updates:
        update_block += "**Milestone updates:**\n"
        for mu in safe_milestone_updates:
            update_block += (
                f"- {mu['milestone']}: status → {mu['status']}"
            )
            if mu.get('target_date'):
                update_block += f", target date → {mu['target_date']}"
            if mu.get('completion_date'):
                update_block += f", completed → {mu['completion_date']}"
            if mu.get('notes'):
                update_block += f" | {mu['notes']}"
            update_block += "\n"
        update_block += "\n"

    if safe_notes:
        update_block += f"**Notes:** {safe_notes}\n"

    _append_to_progress_log(plan_file, update_block)

# Return console summary
current_milestones = _read_milestone_summary(plan_file)
return {
    'onboarding_id': _read_field(plan_file, 'onboarding_id'),
    'account': display_account,
    'updated_at': update_timestamp,
    'milestone_status': current_milestones,
}
```

*close operation:*

```python
# Locate active plan
plan_file = _locate_active_plan(safe_account)
closure_dt = date.fromisoformat(safe_closure_date) if safe_closure_date else date.today()
closure_timestamp = datetime.now().isoformat()

# Set plan status to closed
_update_plan_field(plan_file, 'Status', 'closed')

# Set M4 to complete if not already
m4_status = _read_milestone_status(plan_file, 'M4')
if m4_status != 'complete':
    _update_milestone_status(plan_file, 'M4', 'complete', completion_date=closure_dt.isoformat())

# Append closure block to Closure Record section
closure_block = f"""**Adoption confirmation:** {safe_adoption_confirmation}
**Closure date:** {closure_dt.isoformat()}
**Closing notes:** {safe_notes or "*(None provided.)*"}
"""
_populate_closure_record(plan_file, closure_block)

# Plan is read-only after this point
# Subsequent update calls will detect closed status and return explicit error

onboarding_id = _read_field(plan_file, 'onboarding_id')
return {
    'onboarding_id': onboarding_id,
    'account': display_account,
    'status': 'closed',
    'closure_date': closure_dt.isoformat(),
    'adoption_confirmation': safe_adoption_confirmation,
    'message': (
        f"Expansion onboarding plan {onboarding_id} closed successfully. "
        f"Adoption confirmed: {safe_adoption_confirmation}"
    )
}
```

---

### Phase 4: POST-EXECUTION

**Step 1 — Console summary output**

Return the operation result object from OPERATE. All string values in the returned
object are sourced from escaped variables (`display_account`, `safe_*` fields) only.

**Step 2 — Output quality validation (pre-delivery)**

Before returning result, verify:
- For `create`: file exists at `file_path`; all four milestone target dates are present;
  `onboarding_id` matches `EXP-ONB-[ACCT]-[YYYYMMDD]` pattern
- For `update`: Progress Log contains the new timestamped update block; milestone
  table reflects updated values
- For `close`: plan `Status` field shows `closed`; Closure Record populated with
  `adoption_confirmation` and `closure_date`; M4 status is `complete`

---

## Defaults

1. `onboarding_horizon_days` defaults to `60` if absent
2. `close_date` defaults to today (ISO date) if absent — milestone target dates
   calculated from today
3. `closure_date` defaults to today if absent on `close` operation
4. If `champion` is absent, insert `[Identify — confirm with AE]` in plan output
5. If `ae_owner` is absent, insert `[Unassigned]` in plan output
6. If `success_definition` is absent, insert the placeholder prompt in the plan output
7. For `update`: if `onboarding_id` is absent, default to the most recent active plan
   for the account (by file modification date)
8. For `close`: if `onboarding_id` is absent, default to the most recent active plan
   for the account
9. M1 target date is calculated using calendar days, not business days; the output
   notes this is a suggested date

---

## Guardrails

### ALWAYS

1. Initialize `display_account` and `safe_account` from `account_name` via
   `xml_structural_escape()` and `re.sub(r'[^\w\-]', '_', ...)` at CLASSIFY Step 2 —
   before any filesystem or output operations
2. Apply `xml_structural_escape()` to every user-provided string input at PRE-FLIGHT
   Step 1 before any use in output generation, file writes, or parameter evaluation
3. Apply `scan_for_injection()` to all escaped inputs at PRE-FLIGHT Step 2 before
   proceeding to OPERATE — raise ValueError on detection
4. Use `display_account` exclusively for document output (plan file content, console
   summaries, error messages referring to the account by name); use `safe_account`
   exclusively for filesystem path construction — never cross-use
5. Block `close` if `adoption_confirmation` is empty or whitespace-only — raise
   ValueError with explicit instruction; no exceptions to this gate
6. Block immutable field updates in `update` — raise ValueError naming the specific
   immutable field(s) attempted
7. Warn and raise ValueError on duplicate `create` when an active plan exists —
   require explicit `force=true` to proceed; never silently overwrite
8. Return explicit error when `update` or `close` is called and no active plan exists
   for the account
9. Set M4 to `complete` during `close` if not already complete — never close a plan
   with an incomplete M4 milestone record

### NEVER

1. Never generate `dynamic_code_execution: true` or `requires_elevated: true` in
   any frontmatter or configuration output
2. Never use `safe_account` (filesystem-safe string) in document output — use
   `display_account` for all human-readable account name references
3. Never use `display_account` for filesystem path construction — use `safe_account`
   for all file path operations
4. Never close a plan without a non-empty `adoption_confirmation` — this gate exists
   to prevent premature closure and loss of adoption evidence
5. Never silently overwrite an existing active plan on `create` — always raise ValueError
   and require `force=true`
6. Never allow `update` on a `closed` plan — return explicit error identifying the
   `onboarding_id` and directing the CSM to create a new plan for subsequent expansion
7. Never pass unescaped user input to plan file content, file path construction, or
   console output — escape first, scan second, write third
8. Never accept `onboarding_horizon_days` values other than 30, 60, or 90 — reject
   with ValueError naming the received value and the valid options

---

## Failure Modes

1. **Missing required fields (create)**: Raise `ValueError` identifying the missing
   field (`account_name`, `csm_name`, or `expansion_product`) before any file operation.
   Do not create a partial plan file.

2. **Invalid horizon (create)**: Raise `ValueError` stating the received value and the
   valid options (30, 60, 90). Do not default silently — an invalid value indicates
   a likely input error.

3. **Duplicate active plan (create, force absent)**: Raise `ValueError` identifying
   the existing plan file path and instructing the CSM to set `force=true` or use
   `update` on the existing plan.

4. **No active plan found (update or close)**: Raise `ValueError` identifying the
   account and directing the CSM to run `create` first.

5. **Closed plan update attempt**: Raise `ValueError` identifying the `onboarding_id`
   and stating the plan is closed. Direct CSM to create a new plan for subsequent
   expansion on this account.

6. **Immutable field update attempt**: Raise `ValueError` naming each immutable field
   that was in the update request. Do not apply any updates in the same call — reject
   the entire update if any immutable field is targeted.

7. **Empty adoption_confirmation (close)**: Raise `ValueError` with explicit instruction
   to provide an adoption confirmation statement before closing. Do not proceed with
   partial close.

8. **Injection detected (Layer 2)**: Raise `ValueError` with generic message. Do not
   reveal which pattern matched — pattern enumeration enables evasion.

---

## Reasoning Protocol

### CLASSIFY

When entering CLASSIFY, resolve in order:
1. Is `operation` present and valid (`create`, `update`, or `close`)? If absent or
   invalid → AskUserQuestion before proceeding.
2. Is `account_name` non-empty? If not → ValueError immediately (applies to all operations).
3. Operation-specific validation (create: required fields + horizon + duplicate guard;
   update: locate active plan + closed check + immutable field check;
   close: locate active plan + adoption_confirmation blocking gate).

CLASSIFY is complete when: operation confirmed, `display_account`/`safe_account`
initialized, operation-specific validation passes.

### PRE-FLIGHT

Escape-before-scan contract applies to all inputs without exception:
1. `xml_structural_escape()` runs on all string inputs (Layer 1)
2. `scan_for_injection()` runs on all escaped inputs (Layer 2)
3. Any detection raises ValueError before OPERATE phase begins

### OPERATE

Mode-conditional execution — only the logic branch for the active operation runs.
File writes occur after all validation passes. Console summary is built from escaped
variables only.

### POST-EXECUTION

Output quality validation runs before result is returned. Verify file state matches
expected post-operation state (file exists for create; file updated for update;
file shows closed status for close).

---

## Security & Permissions

**Network access:** none — skill operates on provided parameters only; no external API calls

**Filesystem access:** read/write to `context/` directory within CS plugin filesystem

**Subprocess execution:** none

**Dynamic code execution:** none — Python pseudocode represents logic contract, not runtime execution

**Data sensitivity:** inputs may contain account names, deal data, stakeholder names, and
adoption metrics. All user-provided strings are escaped via `xml_structural_escape()` before
any processing, file write, or output use.

**Injection defense — Layer 1 (xml_structural_escape):**
- Step 0: `html.unescape()` — single-pass; resolves double-encoded entities
- Step 1: NFKC normalization — collapses width variants
- Step 2: Strip raw `<` and `>` individually (no separator; adjacent tag residues concatenate directly)
- Step 3: HTML entity regex `#[xX]0*3[cCeE]` (with `0*` for leading zeros)
- Step 4: Explicit iteration over 10 Unicode homoglyphs: `<>‹›⟨⟩〈〉﹤﹥`

**Injection defense — Layer 2 (scan_for_injection):**
- 13 word-boundary-anchored regex patterns covering instruction suppression, role override,
  system prompt extraction, concatenation bypass forms, and structural LLM-format injection
- Patterns 11–13 compiled with `re.IGNORECASE` (index >= 10 in INJECTION_PATTERNS list)
- Pattern 9: `\boverride\w*\b` (catches concatenation forms like `overrideignore`)
- Pattern 13: `\s+` not `\s` (prevents double-space bypass)

---

## Trust & Verification

**Input trust model:** All user-provided string parameters are treated as untrusted until
escaped and scanned. No parameter is trusted by virtue of parameter name or position.

**Escape-before-scan contract:** `xml_structural_escape()` (Layer 1) runs before
`scan_for_injection()` (Layer 2) on all inputs. Scanning unescaped input would create
a bypass surface.

**Scan failure handling:** On Layer 2 detection, raise `ValueError` with a generic
message. Do not reveal which pattern matched — pattern enumeration enables evasion.

**Output trust:** Plan file content and console summaries are constructed from escaped
inputs only. Raw user input never appears directly in file output.

**Adoption confirmation gate:** The `adoption_confirmation` blocking gate is enforced
in CLASSIFY before PRE-FLIGHT runs. An empty or whitespace-only value raises immediately.
The gate cannot be bypassed by passing an escaped empty string — the check is applied
to the raw parameter value before escaping.

**Closed plan enforcement:** `update` detects closed plan status by reading the `Status`
field from the existing plan file. This is a file-state check, not a session-state check —
the guard survives across sessions and agent restarts.

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `reference/injection-defense.md` | Prompt injection defense guidelines and input sanitization patterns for this skill |
| `reference/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Worked Examples

### Example 1: create — Happy Path (won CSQL context)

**Input:**
```
operation: create
account_name: Meridian Logistics
csm_name: Jordan Park
expansion_product: Advanced Analytics Suite — 50 additional Enterprise seats
csql_id: CSQL-2026-0441
champion: Marco Vitelli, VP Operations
ae_owner: Priya Nair
close_date: 2026-05-18
onboarding_horizon_days: 60
success_definition: >
  50 seats provisioned and at least 40 active users (80% seat utilization)
  within 60 days of go-live, with at least one dashboard shared to executive
  stakeholder.
notes: AE confirmed champion is highly motivated. Budget pre-approved in Q1 cycle.
```

**CLASSIFY:**
- operation = create ✓
- display_account = "Meridian Logistics", safe_account = "Meridian_Logistics"
- account_name ✓, csm_name ✓, expansion_product ✓
- horizon = 60 ✓ (valid)
- No existing active plan → duplicate guard passes

**PRE-FLIGHT:**
- All inputs escaped via `xml_structural_escape()` — no angle brackets or entities present
- Layer 2 scan: no injection patterns detected ✓

**OPERATE (create):**
- `onboarding_id` = `EXP-ONB-MERI-20260518`
  (alpha chars from "Meridian Logistics": M, e, r, i → "MERI")
- `close_dt` = 2026-05-18
- M1 target: 2026-05-21 (close + 3 days)
- M2 target: 2026-05-30 (close + round(60 × 0.20) = +12 days)
- M3 target: 2026-06-27 (close + round(60 × 0.70) = +42 days)
- M4 target: 2026-07-17 (close + 60 days)
- File written: `context/expansion-onboarding-Meridian_Logistics-2026-05-18.md`

**Result:**
```
onboarding_id: EXP-ONB-MERI-20260518
file_path: context/expansion-onboarding-Meridian_Logistics-2026-05-18.md
account: Meridian Logistics
expansion_product: Advanced Analytics Suite — 50 additional Enterprise seats
status: active
milestone_scaffold:
  M1_kickoff: 2026-05-21
  M2_configuration_complete: 2026-05-30
  M3_adoption_gate: 2026-06-27
  M4_onboarding_confirmed: 2026-07-17
```

*Additional examples: see `reference/injection-defense.md` — Examples section (Example 2: update — M1 Completion; Example 3: close — Adoption Confirmation).*

---

## Dependencies

**Upstream skills (source of create inputs):**
- `rev-ops:csql-tracking` — CSQL win event provides `account_name`, `csm_name`,
  `expansion_product`, `csql_id`, `ae_owner`; CSM-triggered, not automated at MVP

**Inter-skill field mapping — `rev-ops:csql-tracking` → `csm:expansion-onboarding`:**

| `rev-ops:csql-tracking` source field | `csm:expansion-onboarding` parameter |
|--------------------------------------|---------------------------------------|
| `account_name` | `account_name` |
| `csql_id` | `csql_id` |
| `csql_stage` (must be `won`) | `operation=create` trigger condition |
| `arr_uplift` | `arr_uplift` |
| `close_date` | `close_date` (milestone horizon anchor) |

Consuming skill reads these fields from the won CSQL record to populate the expansion onboarding plan. No transformation applied except date parsing for milestone calculation.

**Downstream skills (optional consumers):**
- `csm:success-plan-canvas [plan_type=expansion]` — strategic canvas layer;
  complementary to onboarding plan, not redundant; no formal inter-skill data contract
- `csm:communication-planner` — milestone dates and stakeholder fields are relevant
  inputs for expansion communication planning; advisory use only

**Reference files (on-demand):**
- No reference files required at MVP; if milestone date calculation is extended to
  support business day logic, extract calculator to `reference/milestone-schedule-calculator.md`

**Open questions (carry forward from DS-20260518):**
- OQ-1: Should `close` require all 4 milestones complete before allowing closure?
  MVP resolution: `adoption_confirmation` only; milestone states are scaffold, not gate
- OQ-2: Should `update` allow replacing `success_definition`?
  MVP resolution: allow; not immutable
- OQ-3: Should `rev-ops:csql-tracking` emit a machine-readable CSQL Win Event object?
  Post-MVP: out of scope for this version
- OQ-4: Business day calculation for M1 — MVP uses calendar days with output note
