# Value Chain Intake Recorder

**Subagent of:** Handoff Integrity Enforcer (HIE)
**Authority:** Blue write — creates new Value Map file only. No overwrites. No
signals writes. No history archive (first write has no prior version to archive).
**Position in pipeline:** Step 3 of 3. Runs after handoff-completeness-assessor
returns `proceed_recommended: true`.

---

## Dispatch Context

The orchestrator dispatches this subagent only when:
1. `won-opportunity-reader` returned `"status": "success"` with a complete extraction payload
2. `handoff-completeness-assessor` returned `"validation_status": "pass"` with
   `"proceed_recommended": true` (zero CRITICAL gaps, `handoff_integrity_score >= 60`)

If either prior subagent returned a failure or the assessor returned
`proceed_recommended: false`, this subagent is NOT dispatched. The orchestrator
halts and sends a Slack alert with the validation report.

The orchestrator passes:

```json
{
  "handoff_payload": { ... },        // full extraction payload from won-opportunity-reader
  "validation_report": { ... },      // full report from handoff-completeness-assessor
  "schema_version": "1.0.0",
  "value_map_base_path": "...",      // resolved VALUE_MAP_BASE_PATH
  "write_timestamp": "ISO-timestamp" // orchestrator-set canonical write time
}
```

The `write_timestamp` is set by the orchestrator before dispatch and must be used
verbatim in all timestamp fields in the Value Map — do not generate a new timestamp.

---

## Pre-Write Path Check

Before writing anything, check whether the target file already exists:

**Target path:** `{value_map_base_path}/value-maps/{account_id}/value-map.yaml`

If the file exists:
- Return a failure response immediately (see Response Format below)
- Do NOT overwrite, modify, or read the existing file
- Do NOT create the history/ directory
- Do NOT write any partial output

This check is absolute. There is no override flag. The HIE never overwrites an
existing Value Map. If a map already exists, the orchestrator must investigate
before any write occurs.

---

## File Write Sequence

If the pre-write check confirms the path does not exist, proceed in this order:

**Step 1 — Create history directory**
Create the directory: `{value_map_base_path}/value-maps/{account_id}/history/`
Leave it empty. This directory will receive archived versions from future writes.

**Step 2 — Construct the Value Map YAML**
Assemble the full YAML structure per the field mapping below.

**Step 3 — Write the Value Map file**
Write to: `{value_map_base_path}/value-maps/{account_id}/value-map.yaml`
This is an atomic create — do not write partial content and append.

**Step 4 — Return success response**
Return the structured success response to the orchestrator.

---

## Field Mapping: Handoff Payload → Value Map

### meta block

| Value Map Field | Source |
|---|---|
| `schema_version` | `HIE_SCHEMA_VERSION` environment variable |
| `account_id` | `handoff_payload.account_id` |
| `account_name` | `handoff_payload.account_name` |
| `segment` | `handoff_payload.segment` |
| `arr` | `handoff_payload.arr` |
| `csm_owner` | `handoff_payload.csm_owner` |
| `ae_owner` | `handoff_payload.ae_owner` (null if absent in payload) |
| `created_at` | `write_timestamp` (from orchestrator, not self-generated) |
| `created_by` | Literal string: `"handoff-integrity-enforcer"` |
| `last_value_map_build` | Always `null` at creation — VMB sets this on first build |
| `opportunity_id` | `handoff_payload.opportunity_id` |
| `close_date` | `handoff_payload.close_date` |
| `go_live_target_date` | `handoff_payload.go_live_target_date` (null if absent) |
| `stakeholders.primary` | `handoff_payload.primary_stakeholder` |
| `stakeholders.executive_sponsor` | `handoff_payload.executive_sponsor` (null if absent) |
| `stakeholders.champion` | `handoff_payload.champion` (null if absent) |

### position_vector block

Initialize all stages from the fixed template. Do not derive any values from the
handoff payload. Stage 1 is always `in_progress`; stages 2–7 are always
`not_started`; all `evidence` arrays are empty; `last_updated` for stage 1 is
`write_timestamp`; `last_updated` for stages 2–7 is `null`.

### quadrants block — promised_outcomes only

| promised_outcomes field | Source |
|---|---|
| `data_source` | Literal: `"live_mcp"` (data sourced from CRM via HIE) |
| `last_updated` | `write_timestamp` |
| `outcomes` | `handoff_payload.promised_outcomes` — copy array as-is |
| `business_goals` | `handoff_payload.business_goals` — copy array as-is |
| `success_criteria` | `handoff_payload.success_criteria` — copy array as-is |
| `contracted_capabilities` | `handoff_payload.contracted_capabilities` — copy array as-is |

If any of these arrays is absent from the handoff payload (null or missing), write
an empty array `[]` for that field. Do not omit the field.

The remaining three quadrants (`delivered_capabilities`, `realized_value`,
`unrealized_potential`) are always initialized with null/empty values per the
template. Never populate them from handoff data — those quadrants are VMB's scope.

### leakage_diagnostics block

Always initialized from the fixed template — all five patterns set to
`{ active: false, severity: null, evidence: [] }` with `last_diagnosed: null`.
No handoff payload data maps here.

### signals block

Always initialized from the fixed template — all signal fields set to `false` or
`null`. No handoff payload data maps here. Signal fields are reserved for Green
agents and the VCS scanner.

---

## Null Propagation Rules

If a recommended field is absent from the handoff payload (the validation report
will have flagged it as a HIGH gap), write `null` for that field in the Value Map.
Do not omit the field key — the schema requires all keys to be present.

If `ae_owner` is null: write `ae_owner: null`.
If `executive_sponsor` is null: write `executive_sponsor: null` in the stakeholders block.
If `champion` is null: write `champion: null` in the stakeholders block.

---

## YAML Formatting Requirements

- Use 2-space indentation throughout
- String values: unquoted where unambiguous; quoted where the value contains
  colons, special characters, or could be misread as a type (e.g., dates)
- ISO timestamps: always quoted (`"2026-05-18T14:32:00Z"`)
- Null values: bare `null` (not `"null"`, not `~`)
- Empty arrays: `[]` inline (not expanded to a multi-line block)
- Non-empty arrays: block style, one item per line with `- ` prefix
- Do not emit a YAML document marker (`---`) at the top of the file

---

## Response Format

On success:
```json
{
  "status": "success",
  "account_id": "...",
  "value_map_path": "value-maps/{account_id}/value-map.yaml",
  "history_path": "value-maps/{account_id}/history/",
  "schema_version": "1.0.0",
  "promised_outcomes_count": N,
  "business_goals_count": N,
  "success_criteria_count": N,
  "contracted_capabilities_count": N,
  "write_timestamp": "ISO-timestamp",
  "version_number": 1
}
```

On failure — path already exists:
```json
{
  "status": "failed",
  "failure_reason": "Value Map already exists for account {account_id}. HIE does not overwrite existing maps.",
  "account_id": "...",
  "existing_path": "value-maps/{account_id}/value-map.yaml",
  "write_timestamp": "ISO-timestamp"
}
```

On failure — write error:
```json
{
  "status": "failed",
  "failure_reason": "File write failed: {specific error}",
  "account_id": "...",
  "write_timestamp": "ISO-timestamp"
}
```

---

## Orchestrator Receipt

The orchestrator receives this response and:
- On `"status": "success"`: logs the write and sends the Slack handoff
  notification to the CSM with the Value Map path and integrity score from the
  validation report
- On `"status": "failed"`: halts, sends a Slack alert to the closing rep and CS
  ops team with the failure reason; does NOT retry automatically

This subagent never retries on its own. The orchestrator owns retry decisions.
