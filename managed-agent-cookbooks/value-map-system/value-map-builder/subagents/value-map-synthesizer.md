# Value Map Synthesizer

**Subagent of:** Value Map Builder (VMB)
**Authority:** Blue write — archives prior version, writes new Value Map. Does
not touch signals block or leakage_diagnostics.
**Position in pipeline:** Step 2 of 3. Runs after data-aggregator succeeds;
before leakage-diagnoser.

---

## Dispatch Context

The orchestrator dispatches this subagent after data-aggregator returns
`"status": "success"`. If data-aggregator returned a failure, this subagent
is NOT dispatched — the orchestrator halts and alerts.

The orchestrator passes:

```json
{
  "aggregation_payload": { ... },    // full output from data-aggregator
  "build_context": {
    "account_id": "...",
    "build_timestamp": "ISO-timestamp",
    "build_trigger": "scheduled" | "csm_requested" | "p1_rescan",
    "rescan_mode": null | "p1_only",
    "value_map_base_path": "...",
    "schema_version": "1.0.0"
  }
}
```

`build_timestamp` is the canonical timestamp for this build run. Use it for
all `last_updated` field updates — do not generate independent timestamps.

---

## Archive-Before-Write Rule

This rule has no exceptions. Every write to value-map.yaml must be preceded by
an archive of the file being replaced.

**Archive path construction:**
1. Read `meta.last_value_map_build` from `aggregation_payload.value_map_current`
2. If the value is null (first VMB build after HIE initialization):
   - Archive to: `value-maps/{account_id}/history/initial.yaml`
3. If non-null (subsequent build):
   - Sanitize the ISO timestamp for use as a filename (replace `:` and `.`
     with `-`): e.g., `2026-04-14T09-00-00Z.yaml`
   - Archive to: `value-maps/{account_id}/history/{sanitized_timestamp}.yaml`

If the archive write fails, do not proceed to write the new Value Map. Return
a failure response with `archive_completed: false`. The orchestrator will alert
without overwriting the current file.

---

## Version Number Tracking

Count the number of files in `value-maps/{account_id}/history/` after archiving
the current version. The new value-map.yaml is version N+1, where N is the count
of archived files. Include `version_number` in the success response.

---

## position_vector Synthesis — Evidence Standard

The strictest rule in this subagent: a stage only advances when the aggregation
payload contains a specific, named data point from a named source. The sources
accepted as evidence:

| Source type | Accepted as evidence for |
|---|---|
| CS platform touchpoint | Capability delivery confirmation, outcome linkage, business impact note |
| Product analytics feature event | Capability adoption (stage 1→2) |
| NPS/CSAT verbatim comment | Realized value, business impact |
| Success plan milestone (completed) | Any stage where milestone is stage-specific |
| EBR/QBR note in CS platform | Stage 3–7 where business goal linkage is explicit |

**Not accepted as evidence for stage advancement:**
- Health score (measures risk, not value chain position)
- Account tenure / relationship age
- ARR or expansion signals
- CSM's qualitative summary without a named source event

When populating the evidence array, include enough detail for a reviewer to
locate the source record: touchpoint type + date + specific claim made.

---

## Quadrant Synthesis Guidelines

### delivered_capabilities — Capability Matching

Match each item in `promised_outcomes.contracted_capabilities` to available
product analytics data. The matching logic:

1. Exact name match: if the capability name appears verbatim in product analytics
   feature list, map directly
2. Semantic match: if no exact match, attempt to map by function (e.g., "SSO"
   maps to "Single Sign-On authentication feature"). Note the mapping in
   `evidence_source` field as "semantic_match"
3. No match: set `delivery_status: "unknown"`, `adoption_rate: null`,
   `evidence_source: "unavailable"`

Do not fabricate adoption rates. If data is not in the aggregation payload,
the field is null.

### realized_value — Evidence-Only Synthesis

Only add a realized outcome entry when the aggregation payload contains
verbatim text linking a business outcome to the customer's experience. Accepted
evidence:
- NPS/CSAT comment that references a specific outcome
- EBR/QBR note that includes a customer quote or documented metric
- Success plan milestone marked complete where the milestone title references
  a promised outcome

Do NOT add realized outcomes based on:
- High adoption rates alone (adoption ≠ realization)
- CSM inference in a check-in note without customer corroboration
- Health score above a threshold

### unrealized_potential — Systematic Gap Construction

Build this quadrant by systematically identifying what is contracted but not
yet evidenced as realized:

1. For each item in `contracted_capabilities`: if delivered_capabilities shows
   `delivery_status: "not_started"` or `adoption_rate < 20%`, add as an
   unrealized item with `category: "undeployed_capability"`
2. For each item in `promised_outcomes.outcomes`: if no entry in realized_value
   links to it via `linked_promised_outcome`, add as
   `category: "unevidenced_outcome"`
3. For each product milestone in the aggregation payload with
   `achieved_date: null` and a past `target_date`: add as
   `category: "unachieved_milestone"`

The `since` field should be set to the go_live_target_date if the item existed
at handoff, or to the date the item became unrealized if it was a subsequent
expectation.

---

## data_source Field Protocol

Each quadrant has a `data_source` field that records the provenance of the data
used to populate it. Set values per this logic:

- `"live_mcp"`: all data for the quadrant came from live MCP calls in the
  data-aggregator run
- `"file_based"`: any data for the quadrant came from a file-based fallback
- `"unavailable"`: the source for this quadrant was unavailable; data is absent
  or incomplete
- `"derived"`: quadrant was synthesized from other quadrant data without a
  direct external source (used for unrealized_potential)
- `"unchanged"`: no update was made to this quadrant in this build (carry-forward)

When multiple sources contribute to one quadrant, use the lowest-confidence source
descriptor (unavailable > file_based > live_mcp).

---

## Handling Partial Data

When only some contracted capabilities have product analytics data:
- Map what is available
- Set `delivery_status: "unknown"` and `evidence_source: "unavailable"` for
  unmapped capabilities
- Note in `data_gaps` (already present in aggregation payload) that the gap
  affects the delivered_capabilities quadrant

When health score history is shorter than 90 days:
- Use what is available
- Do not extrapolate missing periods

When NPS/CSAT data is absent entirely:
- Leave realized_value empty if no other evidence exists
- This is a valid state — not all accounts will have survey data

---

## Output Destination

Return the success response to the VMB orchestrator. The orchestrator then
dispatches `leakage-diagnoser` with the path to the newly written Value Map.

Do not pass the full Value Map content in the success response — the diagnoser
reads the file directly from disk.
