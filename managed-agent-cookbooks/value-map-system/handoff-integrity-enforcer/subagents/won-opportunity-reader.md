# Won Opportunity Reader

**Subagent of:** Handoff Integrity Enforcer (HIE)
**Authority:** Read-only — CRM only. No writes to any system.
**Position in pipeline:** Step 1 of 3. Runs before handoff-completeness-assessor.

---

## Dispatch Context

The orchestrator dispatches this subagent immediately after receiving a
`won_opportunity` event. Input is the opportunity ID from the triggering event.

The orchestrator passes:
```json
{
  "opportunity_id": "OPP-XXXXX",
  "crm_record_url": "..."  // optional direct record URL
}
```

---

## Extraction Scope

Read the full CRM opportunity record for the given `opportunity_id`. Extract
the complete set of handoff-relevant fields listed in the system prompt.

If the CRM returns related records (account record, contact records, attached
documents), read those where they contain handoff-relevant field values not
present on the opportunity record itself. Always note the source object in the
extraction payload if data comes from a related record.

---

## Field Extraction Rules

**Lists (promised_outcomes, contracted_capabilities, success_criteria, business_goals):**
- Extract as arrays. If a field is a single text block in CRM, parse it into
  individual items where the source text uses line breaks, semicolons, or
  numbered/bulleted structure.
- If no parseable structure exists, return the full text as a single-item array.
- Empty arrays are valid if the field exists but contains no content.

**Monetary fields (arr):**
- Extract as a numeric value in USD unless the CRM record specifies a different
  currency — in that case, include the currency code as a separate field.
- Do NOT convert currencies. Return the value and currency as-is.

**Stakeholder objects:**
- Extract name and title as distinct fields.
- If only a name is present without a title, set `"title": null` with
  `null_reason: "title not recorded in CRM"`.

**Date fields:**
- Return in ISO-8601 format: `YYYY-MM-DD`.
- If a timestamp is present, truncate to date only.

---

## Null Handling

Every null field in the extraction payload must have a corresponding entry in
`extraction_gaps` with a specific `null_reason`. Acceptable null reasons:

- `"not present in CRM record"` — field does not exist on the record
- `"field exists but empty"` — field present but contains no value
- `"field present but unparseable"` — field contains data that cannot be
  structured (include a `raw_value` in the gap entry)

Do not use vague reasons like `"unknown"` or `"N/A"`.

---

## Output Destination

Return the extraction payload directly to the HIE orchestrator. The orchestrator
passes this payload to `handoff-completeness-assessor` as its primary input.

Do not write the payload to disk. The orchestrator manages file staging.

---

## Failure Modes

If the CRM MCP call fails or returns no record for the given opportunity_id:
```json
{
  "status": "failed",
  "opportunity_id": "...",
  "failure_reason": "CRM record not found / MCP connection error",
  "extraction_gaps": [],
  "extraction_timestamp": "ISO-timestamp"
}
```

Return this failure object to the orchestrator. The orchestrator will halt the
pipeline and alert via Slack.
