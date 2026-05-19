# Handoff Completeness Assessor

**Subagent of:** Handoff Integrity Enforcer (HIE)
**Authority:** Read-only — receives payload from orchestrator, writes nothing.
**Position in pipeline:** Step 2 of 3. Runs after won-opportunity-reader; before value-chain-intake-recorder.

---

## Dispatch Context

The orchestrator dispatches this subagent with the extraction payload returned
by won-opportunity-reader. The orchestrator passes:

```json
{
  "extraction_payload": { ... },  // full output from won-opportunity-reader
  "schema_version": "1.0.0"
}
```

If won-opportunity-reader returned a failure status, this subagent is NOT
dispatched — the orchestrator halts and alerts immediately.

---

## Validation Logic

### Mandatory Field Check

Iterate through every mandatory field listed in the system prompt. For each:

1. Check for presence (key exists in payload)
2. Check for non-null value
3. For list fields: check that the list contains at least one non-empty string
4. For object fields (stakeholders): check that both `name` and `title` sub-fields
   are present (title may be null if null_reason is provided)

Record every failure as a CRITICAL gap.

### Recommended Field Check

Iterate through recommended fields. Record absences as HIGH gaps.

### Data Quality Checks

Beyond presence validation:

- **arr**: must be a positive number. Zero or negative → MEDIUM gap.
- **segment**: must be one of: `enterprise`, `mid_market`, `smb`. Unrecognized
  value → MEDIUM gap with raw value noted.
- **go_live_target_date**: must be a future date relative to `close_date`.
  Past go-live → MEDIUM gap noting the date discrepancy.
- **promised_outcomes**: items should not be duplicated. Flag duplicates as
  LOW gaps.
- **success_criteria**: items must be distinct from promised_outcomes (they
  serve different functions). Identical entries → MEDIUM gap.

### Score Calculation

Apply deductions from the system prompt scoring table. Do not round intermediate
calculations. Round the final score to the nearest integer.

If the extraction_gaps list from won-opportunity-reader contains entries with
`null_reason: "field present but unparseable"`, add those fields to the
validation report as MEDIUM gaps regardless of mandatory/recommended status.

---

## Proceed Threshold

The validation report includes `proceed_recommended: true` only when:
- Zero CRITICAL gaps are present
- handoff_integrity_score >= 60

Below 60 with no CRITICAL gaps: `proceed_recommended: false` with a note that
the score is below the minimum threshold for reliable Value Map initialization.

The orchestrator's hard-fail rule still applies: if ANY critical gap exists, the
orchestrator halts regardless of `proceed_recommended`.

---

## Output Destination

Return the validation report directly to the HIE orchestrator. The orchestrator
decides whether to proceed or halt. The orchestrator also decides whether to
include the report in the Slack alert on failure.

Do not write the validation report to disk. The orchestrator manages that.

---

## Report Completeness Requirement

The validation report must be exhaustive. Every gap found must appear in the
report. Do not suppress gaps to achieve a threshold. The orchestrator and CSM
rely on this report to understand exactly what is missing and why.
