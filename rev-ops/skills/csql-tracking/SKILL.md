---
name: rev-ops:csql-tracking
version: 1.0.0
description: "Manages the lifecycle of Customer Success Qualified Leads (CSQLs) — create, update, close, and query operations — with persistent filesystem storage, status state machine enforcement, and inter-skill contract consumption from csm:expansion-business-case."
deployment_target: plugin
status: VALIDATED
eval_pass_rate: "1.00 (12/12) — iteration-4, 2026-05-17"
eval_delta: "+0.500 (with_skill 1.000 vs baseline 0.500)"
eval_workspace: "csql-tracking-workspace/iteration-4"
---

[VALIDATED]

## Overview

`rev-ops:csql-tracking` manages the full lifecycle of Customer Success Qualified Leads (CSQLs) — the handoff artifact produced by `csm:expansion-business-case [mode=csql]` — from CS handoff through closed/won or terminal pipeline states. It provides RevOps with a persistent, queryable portfolio of active and closed CSQLs within the CS plugin's filesystem control plane.

This skill is the downstream consumer in a two-skill inter-skill contract:

```
csm:expansion-business-case [mode=csql]
        ↓  emits CSQL Qualification Package
rev-ops:csql-tracking [operation=create]
        ↓  persists to context/csql-*.md
```

Four operations are supported: `create`, `update`, `close`, `query`.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `cs_platform_connected`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use When

- A CSM has completed a CSQL Qualification Package via `csm:expansion-business-case [mode=csql]` and needs to register it in the CSQL pipeline
- RevOps or an AE needs to update a CSQL status, assign an AE, or append notes to an existing record
- A deal reaches a terminal state (won, lost, or stalled) and needs to be formally closed in the tracker
- RevOps wants a portfolio view of active or closed CSQLs, with filtering by status, CSM, AE, or account, and sorting by creation date or close date

---

## Do NOT Use For

- Generating CSQL Qualification Packages — use `csm:expansion-business-case [mode=csql]` for that
- CRM integration or external data writes of any kind
- Revenue forecasting or pipeline analytics
- Notification or alerting workflows

---

## Typical Activation

- "Register this CSQL for Acme Corp"
- "Update CSQL-ACME-20260516-001 status to qualified"
- "Close CSQL-WIDG-20260510-002 — won at $42,000"
- "Show me all active CSQLs assigned to Jane"
- "Log a CSQL for Thorngate Partners — here's the qualification package"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of CSQL operation is this?
   - Create (ingest a new CSQL Qualification Package and persist a new record)
   - Update (modify mutable fields on an existing CSQL record)
   - Close (set a CSQL to a terminal state — won, lost, or stalled)
   - Query (retrieve, filter, and surface one or more CSQL records)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting CSQL lifecycle management or retrieval
   2. Resolve the target CSQL record(s) from filesystem; declare file path and data-as-of context
   3. Apply G9 — all filesystem write operations (create, update, close) require explicit user confirmation before execution; surface as draft and await approval
   4. Enforce immutable field lock — csql_id, created_at, csm_owner, and source_skill fields cannot be modified after record creation under any circumstance
   5. Enforce terminal state immutability — records in won, lost, or stalled status cannot be reopened, updated, or re-staged; surface the block explicitly if attempted
   6. Validate status transitions against the state machine before proposing any update; reject invalid transitions with a clear explanation
   7. Confirm output destination before delivering — inline summary vs. formatted table vs. full record dump

3. **EXPERT CHECK**: What would a veteran RevOps CSQL lifecycle analyst verify before executing?
   - Is the CSQL ID being referenced one that actually exists in the filesystem? Fabricating or inferring a CSQL ID from partial context before confirming the record exists produces phantom operations. Read the record first, then act.
   - Is the requested status transition valid per the state machine? The lifecycle is create → qualified → in_negotiation → won/lost/stalled. Skipping stages (create → won) or reversing direction (won → in_negotiation) are not supported — the analyst flags and blocks, not silently accepts.
   - Is the close operation being performed with sufficient terminal-state data? A won close requires ACV; a lost close requires lost_reason. Attempting to close without required fields is a partial write — surface the missing data requirement before writing anything.
   - Is the query filter producing the intended scope? Filters default to active records (exclude_closed=true); a query that silently omits closed records when the user asked "all CSQLs" is a silent data gap. Confirm include_closed intent before executing.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Attempting to modify csql_id, created_at, csm_owner, or source_skill after record creation — these are immutable and the operation must be blocked, not silently ignored
   - Attempting to update or close a record already in won, lost, or stalled status — terminal states are locked; surface the block with the current terminal state and explain why the operation cannot proceed
   - Executing filesystem writes (create, update, close) without surfacing the draft for G9 confirmation first — this is a write-tier protocol violation
   - Silently rejecting an invalid status transition without explaining what transitions are valid from the current state — the user needs the valid path forward, not just a block
   - Returning query results that omit closed records when the user's intent was a full-portfolio view — always confirm include_closed scope for broad queries

**After execution**, verify:
- G9 confirmation surfaced for all filesystem write operations — no writes executed autonomously
- Immutable field lock enforced — no csql_id, created_at, csm_owner, or source_skill mutations accepted
- Terminal state immutability enforced — no won/lost/stalled record updates or reopens executed
- Status transition validated against state machine before any update was proposed
- Confidence: High when CSQL record retrieved directly from filesystem and field values confirmed; Moderate when record inferred from context or CSQL ID not yet confirmed in filesystem
    - Confidence: [High] when CSQL record retrieved directly from filesystem and field values confirmed / [Medium] when record inferred from context or CSQL ID not yet confirmed in filesystem / [Low] if all inputs are manual or unverified

---

## Operations

### create

**Purpose:** Ingest a completed CSQL Qualification Package and persist a new CSQL record to the filesystem.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"create"` |
| `account_name` | string | Yes | Account name — matches the `Account` field in the CSQL package. Locked at creation (immutable). |
| `csql_package` | string | Yes | Full CSQL Qualification Package content from `csm:expansion-business-case [mode=csql]`. Stored verbatim. |
| `csm_name` | string | Yes | CSM who owns this CSQL. |
| `expansion_product` | string | Yes | Product, tier, or capability being proposed. |
| `expansion_amount` | string | No | Estimated expansion ARR (e.g., "~$42,000 ARR"). |
| `ae_owner` | string | No | Assigned AE. Defaults to `[Unassigned]` if not provided. |
| `target_close_date` | string | No | ISO date — expected decision date. |

**Auto-generated fields (immutable after creation):**

| Field | Generation rule |
|-------|----------------|
| `csql_id` | `CSQL-[ACCT]-[YYYYMMDD]-[SEQ]` — see Filesystem Architecture |
| `created_at` | ISO 8601 datetime at time of `create` call |
| `created_by` | Session user identity |
| `account_name` | Captured from input; locked — cannot be modified via `update` |

**Behavior:**

1. Sanitize `account_name` via `safe_account()` for filesystem path derivation.
2. Derive `csql_id` using Auto-ID generation rules (see Filesystem Architecture).
3. Write context file: `context/csql-[safe_account]-[YYYY-MM-DD]-v1.md`
4. Append initial transition log entry: `[created]`
5. Set initial `status` to `new`.

**Output:** Returns `csql_id` and the path of the created context file.

**Error conditions:**
- `account_name` empty or missing → rejected with field validation error
- `csql_package` empty or missing → rejected with field validation error
- `csm_name` empty or missing → rejected with field validation error
- `expansion_product` empty or missing → rejected with field validation error

---

### update

**Purpose:** Partially modify a non-terminal CSQL record — status progression, AE assignment, close date update, or note append.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"update"` |
| `csql_id` | string | Yes | Target CSQL ID (e.g., `CSQL-ACME-20260516-001`) |
| `status` | string | No | New status — must pass transition guard (see Status State Machine) |
| `ae_owner` | string | No | Assign or reassign AE |
| `target_close_date` | string | No | Update expected close date (ISO date) |
| `notes` | string | No | Append-only — new note is appended to the Notes section, not replaced |
| `meddic_updates` | object | No | Updated MEDDIC field values |
| `override` | boolean | No | `true` permits backward status transitions on non-terminal records (admin correction only) |

**Immutable fields — rejected if included in `update` payload:**

| Field | Error response |
|-------|---------------|
| `csql_id` | `Immutable field error: csql_id cannot be modified after creation.` |
| `created_at` | `Immutable field error: created_at cannot be modified after creation.` |
| `created_by` | `Immutable field error: created_by cannot be modified after creation.` |
| `account_name` | `Immutable field error: account_name cannot be modified after creation.` |

**Behavior:**

1. Locate the latest version file for the target `csql_id`.
2. Verify record is not in a terminal state (`won`, `lost`, `stalled`). If terminal → reject with: `Update rejected: CSQL-[ID] is in terminal state [status] and cannot be modified.`
3. If `status` is provided, validate against the transition guard. Reject invalid transitions.
4. Write new version file (`v[N+1]`). Prior version is preserved — never overwritten.
5. Append transition log entry if `status` changed.
6. Append note if `notes` provided.

**Output:** Returns updated `csql_id`, new version path, and transition log entry (if status changed).

**Error conditions:**
- `csql_id` not found → not-found error
- Record in terminal state → terminal-lock error
- Invalid status transition (no `override`) → transition guard rejection with valid next states listed
- Override on terminal state → rejected: `Override rejected: terminal state [status] is immutable and cannot be overridden. Create a new CSQL to re-pursue this opportunity.`

---

### close

**Purpose:** Set a CSQL to a terminal state and lock the record.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"close"` |
| `csql_id` | string | Yes | Target CSQL ID |
| `terminal_status` | string | Yes | One of: `won`, `lost`, `stalled` |
| `close_reason` | string | Yes | Free-text reason for closure |
| `close_date` | string | No | ISO date — defaults to today if not provided |
| `won_amount` | string | Conditional | Required when `terminal_status == won` |

**Behavior:**

1. Locate the latest version file for the target `csql_id`.
2. Verify record is not already in a terminal state. If already terminal → reject.
3. Validate `terminal_status` is one of `won`, `lost`, `stalled`.
4. If `terminal_status == won` and `won_amount` is absent → reject with: `won_amount is required when terminal_status is won.`
5. Set status to terminal state. Write final version file (`v[N+1]`). Prior version preserved.
6. Append terminal transition log entry.
7. Record is now locked — no further `update` operations will be accepted.

**Output:** Returns closed record summary with `csql_id`, `terminal_status`, `close_date`, and `close_reason`.

**Error conditions:**
- `csql_id` not found → not-found error
- Record already in terminal state → already-closed error
- `terminal_status` not one of `won`, `lost`, `stalled` → invalid terminal status error
- `terminal_status == won` without `won_amount` → field required error

---

### query

**Purpose:** Read-only portfolio view of CSQL records with filtering and sorting. No filesystem writes.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation` | string | Yes | Must be `"query"` |
| `filter_status` | string or list | No | Filter by status(es). Accepts single value or list. |
| `filter_csm` | string | No | Filter by CSM name (exact or substring match) |
| `filter_ae` | string | No | Filter by AE name (exact or substring match) |
| `filter_account` | string | No | Substring match on `account_name` |
| `created_after` | string | No | ISO date — include only CSQLs created on or after this date |
| `created_before` | string | No | ISO date — include only CSQLs created on or before this date |
| `sort_by` | string | No | Sort field: `created_at` (default), `target_close_date`, `status`, `account_name` |
| `sort_order` | string | No | `asc` (default) or `desc` |
| `include_closed` | boolean | No | Include `won`, `lost`, `stalled` records. Default: `false` |
| `limit` | integer | No | Max records returned. Default: 20. Max: 100. |
| `offset` | integer | No | Skip first N matching records (for pagination). Default: 0. |

**Behavior:** Scan `context/csql-*` files (latest version per account-date only). Apply filters using AND logic across all provided parameters. Sort. Return formatted table or structured list.

**Output:** Formatted table of matching CSQL records. Includes `csql_id`, `account_name`, `status`, `csm_name`, `ae_owner`, `expansion_amount`, `target_close_date`, `created_at`. Read-only — no filesystem writes occur.

**Reference:** See `reference/query-filter-patterns.md` for filter combination examples, sort behavior, and output format specification. Load on demand when query behavior details are needed.

**Error conditions:**
- Invalid `sort_by` value → error listing valid options
- `limit` exceeds 100 → capped at 100 with warning
- `created_after` after `created_before` → date range error

---

## Status State Machine

**Reference:** See `reference/csql-status-transitions.md` for the full state diagram, transition table, override rules, and log format examples. Load on demand.

### Valid States

| State | Type | Description |
|-------|------|-------------|
| `new` | Active | CSQL created; not yet reviewed by AE |
| `qualified` | Active | AE has reviewed and confirmed qualification |
| `in_negotiation` | Active | Active deal in negotiation |
| `won` | **TERMINAL** | Deal closed won — record locked |
| `lost` | **TERMINAL** | Deal closed lost — record locked |
| `stalled` | **TERMINAL** | Deal stalled; no near-term path — record locked |

### Valid Transitions

| From | To | Override required? |
|------|----|--------------------|
| `new` | `qualified` | No |
| `new` | `stalled` | No (early disqualification) |
| `qualified` | `in_negotiation` | No |
| `qualified` | `stalled` | No (disqualified post-AE review) |
| `in_negotiation` | `won` | No |
| `in_negotiation` | `lost` | No |
| `in_negotiation` | `stalled` | No |
| `in_negotiation` | `qualified` | Yes (admin correction, backward) |
| `qualified` | `new` | Yes (admin correction, backward) |

### Terminal State Rules (IMMUTABLE)

`won`, `lost`, and `stalled` are **terminal and immutable**. Once set:

- No further `update` operations are accepted on the record
- No `override` flag can reactivate a terminal record
- A stalled opportunity that is later re-pursued requires **creating a new CSQL record** — the stalled record is preserved as-is in the filesystem as historical record

This is a design decision, not a limitation. Stalled records must never be mutated. To re-pursue: invoke `rev-ops:csql-tracking [operation=create]` with the same account and a fresh CSQL package.

### Override Flag Rules

- `override: true` permits **backward transitions on non-terminal records only** (e.g., `in_negotiation → qualified` for admin correction)
- Override on a terminal state (`won`, `lost`, `stalled`) is always rejected regardless of flag value
- All override transitions are logged with timestamp and note
- Override is intended for admin correction only — not standard workflow

### Transition Log Format

Every status change appends a log entry to the CSQL record's Transition Log section:

```
[YYYY-MM-DDTHH:MM:SSZ] [from_status] → [to_status] | [notes or "no note"] | [override: true/false]
```

**Examples:**
```
[2026-05-16T14:23:00Z] created | status: new | no note | override: false
[2026-05-17T09:11:00Z] new → qualified | AE confirmed after discovery call | override: false
[2026-05-20T15:44:00Z] in_negotiation → qualified | Reverting — deal not yet in negotiation | override: true
[2026-05-28T10:00:00Z] in_negotiation → won | Closed at $42,000 ARR | override: false
```

---

## Filesystem Architecture

### Context File Naming

```
context/csql-[sanitized_account]-[YYYY-MM-DD]-v[N].md
```

- `sanitized_account`: derived from `account_name` via `safe_account()` — see below
- `YYYY-MM-DD`: creation date, set at `create`, never updated on `update` or `close`
- `v[N]`: integer version, starts at 1, increments on each `update` or `close`
- Prior versions are preserved — never overwritten

**Examples:**
```
context/csql-acme-corp-2026-05-16-v1.md     ← created
context/csql-acme-corp-2026-05-16-v2.md     ← after update
context/csql-acme-corp-2026-05-16-v3.md     ← after close
```

### safe_account() Sanitization Algorithm

```python
def safe_account(account_name: str) -> str:
    """
    Derive filesystem-safe account slug from raw account_name.
    Used for path construction only — NEVER for display output.
    """
    result = account_name.lower()
    result = re.sub(r'[^a-z0-9]', '-', result)   # replace non-alphanumeric with hyphen
    result = re.sub(r'-{2,}', '-', result)         # collapse consecutive hyphens
    result = result.strip('-')                      # trim leading/trailing hyphens
    return result[:30]                              # trim to 30 chars
```

**Examples:**
- `"Acme Corp"` → `acme-corp`
- `"Widget & Co., Inc."` → `widget-co-inc`
- `"TechCo International Solutions Group"` → `techco-international-solut`

### Auto-ID Generation

**Format:** `CSQL-[ACCT]-[YYYYMMDD]-[SEQ]`

| Component | Rule |
|-----------|------|
| `ACCT` | First 4 alphabetic characters of `account_name`, uppercased, non-alpha stripped. If fewer than 4 alpha characters exist, pad with `X` to reach 4. |
| `YYYYMMDD` | Creation date |
| `SEQ` | 3-digit sequence: scan `context/csql-[safe_account]-[YYYY-MM-DD]-*.md` for existing files with same account + same date; take highest SEQ found and increment by 1. Default to `001` if no prior files exist. |

**ACCT derivation examples:**

| account_name | Alpha chars extracted | ACCT |
|---|---|---|
| `"Acme Corp"` | A, c, m, e → ACME | `ACME` |
| `"123 Widgets"` | W, i, d, g → WIDG | `WIDG` |
| `"TechCo"` | T, e, c, h → TECH | `TECH` |
| `"IT Services"` | I, T, S, e → ITSE | `ITSE` |
| `"IT"` | I, T → only 2 alpha chars | `ITXX` (padded) |
| `"A1"` | A → only 1 alpha char | `AXXX` (padded) |
| `"123"` | no alpha chars | `XXXX` (all padded) |

**X-padding rule:** When `account_name` yields fewer than 4 alphabetic characters after stripping non-alpha, pad the `ACCT` component with `X` characters on the right until 4 characters are reached.

**Auto-ID examples:**
```
CSQL-ACME-20260516-001   ← first Acme Corp CSQL on 2026-05-16
CSQL-ACME-20260516-002   ← second Acme Corp CSQL same day
CSQL-WIDG-20260510-001   ← first 123 Widgets CSQL on 2026-05-10
CSQL-ITXX-20260517-001   ← first "IT" account CSQL (padded)
```

### Versioning Rules

- Version `1` is set at `create`
- Each `update` or `close` operation creates a new version: `v[N+1]`
- The prior version file is preserved at `v[N]` — never deleted or overwritten
- The latest version is always the highest `v[N]` for a given `[sanitized_account]-[YYYY-MM-DD]` stem

---

## Immutable Fields

The following fields are locked at `create` and cannot be modified by any subsequent operation:

| Field | Reason |
|-------|--------|
| `csql_id` | Identity key — must remain stable for cross-skill reference |
| `created_at` | Audit timestamp |
| `created_by` | Audit identity |
| `account_name` | Account identity — changes would corrupt `query` filter behavior |

Any `update` request that includes an immutable field in its payload must return an explicit error. Rejection is **not silent**:

```
Immutable field error: [field_name] cannot be modified after creation.
```

Examples:
```
Immutable field error: account_name cannot be modified after creation.
Immutable field error: csql_id cannot be modified after creation.
```

---

## Inter-Skill Contract

### Upstream Producer

**Skill:** `csm:expansion-business-case [mode=csql]`

The CSQL Qualification Package emitted by the upstream skill serves as the primary input to `rev-ops:csql-tracking [operation=create]`.

**Field mapping:**

| Producer field | Consumer parameter | Notes |
|----------------|-------------------|-------|
| `Account` header field | `account_name` | Non-empty string required |
| `Prepared by` CSM name | `csm_name` | Non-empty string required |
| Full package document | `csql_package` | Stored verbatim; content integrity not validated at MVP |
| `Proposed expansion` line | `expansion_product` | Non-empty string required |
| `Estimated expansion value` | `expansion_amount` | Optional |
| `Handoff to` AE field | `ae_owner` | Optional; defaults to `[Unassigned]` |

**Contract validation at `create`:**
- `account_name` must be non-empty string
- `csql_package` must be non-empty string (verbatim storage; structural validation is post-MVP — see OQ-3)
- `csm_name` must be non-empty string
- `expansion_product` must be non-empty string

**Reference template:** `csm/skills/expansion-business-case/reference/csql-package-template.md`

---

## Output

Each operation surfaces a structured confirmation or result. Output formats are documented inline within each `## Operations` subsection. Summary:

- **create** — CSQL record confirmation with assigned csql_id, filesystem path, and record summary table
- **update** — Changed fields summary with before/after values and updated record confirmation
- **close** — Terminal state confirmation with close reason, ACV (if won), and immutability notice
- **query** — Filtered CSQL table (id, account, status, ACV, assigned CSM, days since last update) with result count and active/total scope note

All write operation outputs are presented as drafts requiring G9 confirmation before filesystem execution.

---

## Reference Files

Load these files on demand — do not load at skill invocation start.

| File | Path | Load when |
|------|------|-----------|
| `csql-record-schema.md` | `reference/csql-record-schema.md` | Viewing or validating the canonical CSQL record format, field definitions, validation rules, or Auto-ID/sanitization algorithms |
| `csql-status-transitions.md` | `reference/csql-status-transitions.md` | Reviewing the full state machine diagram, valid transition table, override rules, or transition log format |
| `query-filter-patterns.md` | `reference/query-filter-patterns.md` | Reviewing query filter syntax, sort options, output format, include_closed behavior, or limit/offset patterns |
| `reasoning-blueprint.md` | `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions

**Network access:** None — skill operates on provided parameters and local filesystem only. No external API calls.

**Filesystem scope:** Read and write limited to `context/csql-*` only. No reads or writes outside this path prefix are permitted.

**Subprocess execution:** None.

**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.

**Data sensitivity:** Inputs may contain account names, deal data, MEDDIC qualification details, and customer outcome metrics. All user-provided string inputs are sanitized before filesystem path use.

---

## Trust & Verification

**Input trust model:** All user-provided string parameters are treated as untrusted at intake. No parameter is trusted by virtue of its name or position.

**safe_account() contract:** `account_name` and all values interpolated into filesystem paths are sanitized via `safe_account()` before any path construction. Raw `account_name` (display value) is used only in document content — never in path construction.

**display_account / safe_account separation:**
- `display_account` = raw `account_name` as provided — used only for document display and record content
- `safe_account` = sanitized slug — used only for filesystem path construction
- These must never be cross-used

**csql_package handling:** The CSQL Qualification Package is stored verbatim in the context file body. It is never executed, evaluated, or interpolated into skill logic paths.

**Free-text inputs:** `notes`, `close_reason`, `meddic_updates` values — sanitized for filesystem path use when they appear in filenames or log entries. Raw values are written to document body only.

**Immutability enforcement:** Immutable field violations return an explicit error message — rejection is never silent. Terminal state lock is enforced at runtime before any write operation.

**SEQ collision note:** Auto-ID sequence generation uses a scan-and-increment pattern assuming single-writer access. Parallel create calls for the same account on the same date may produce SEQ collisions. This is a known limitation; single-writer assumption is documented. Post-MVP resolution is OQ-4.

---

## Open Questions (Post-MVP)

- **OQ-1:** Query export to CSV or markdown file write — deferred; `query` is read-only at MVP
- **OQ-2:** stalled recoverability — **RESOLVED**: `stalled` is terminal and immutable. Re-pursuing a stalled opportunity requires creating a new CSQL record. This is the design decision.
- **OQ-3:** Structural validation of `csql_package` (header field detection) — deferred; verbatim storage is the MVP approach
- **OQ-4:** SEQ collision under parallel `create` calls — deferred; single-writer assumption documented in Security & Permissions
- **OQ-5 (from WARN-6):** `qualification_status` field (from the CSQL package header: `COMPLETE / INCOMPLETE`) as a queryable filter field — deferred post-MVP enhancement candidate. The field is stored within `csql_package` verbatim but is not surfaced as a structured, filterable field in the CSQL record schema at MVP.
