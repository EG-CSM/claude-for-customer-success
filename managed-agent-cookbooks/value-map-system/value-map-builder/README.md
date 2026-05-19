# Value Map Builder (VMB)

**Type:** Blue (Write authority — quadrants, position_vector, leakage_diagnostics)
**Role in System:** Post-sale data integrator. Builds and maintains the full four-quadrant Customer Value Map from live CS platform, product analytics, and CRM data.

---

## Purpose

VMB is the primary data engine of the Value Map System. Where HIE captures what was promised at the point of sale, VMB captures what is actually happening post-sale: which capabilities are being used, which outcomes are being realized, where value is leaking, and how far the account has progressed through the seven-stage value chain.

VMB runs on demand (pre-QBR, pre-renewal), on a scheduled cadence, or when a CSM flags the map as stale. It follows a Manual-First fallback order: it tries live MCP data first, falls back to file-based input, then falls back to interactive prompting. Each quadrant records its `data_source` (live_mcp, file, manual, not_populated) for audit transparency.

---

## Prerequisites

HIE must have already fired for the account. VMB will halt if no Value Map exists at the expected path.

---

## Trigger

On demand or scheduled:

```bash
claude --agent value-map-builder \
  --input '{"account_id": "ACC-67890"}'
```

With file-based data fallback:

```bash
# Place data file before running:
# value-map-builder/inbox/ACC-67890-data.yaml
claude --agent value-map-builder \
  --input '{"account_id": "ACC-67890", "data_source_override": "file"}'
```

---

## Subagents

| Subagent | Role | Writes |
|---|---|---|
| `data-aggregator` | Pulls live data from CS platform (touchpoints, health, adoption), product analytics (usage, workflow completion), and CRM (account metadata refresh) | Nothing |
| `value-map-synthesizer` | Updates all four quadrants and all seven position_vector stages with evidence citations; tags each quadrant with data_source | Nothing |
| `leakage-diagnoser` | Runs all five leakage pattern checks; records active/severity/description/detected_at for each pattern | Nothing |

The orchestrator writes the assembled Value Map after all three subagents complete.

---

## MCP Dependencies

| Server | Access | Required |
|---|---|---|
| `crm` | Read | Yes |
| `cs-platform` | Read | Yes |
| `product-analytics` | Read | Yes |

---

## Manual-First Fallback

When live MCP is unavailable:
1. Check `inbox/{account_id}-data.yaml` for pre-staged data
2. If not present, prompt CSM to provide values interactively

The `data_source` field in each quadrant records which path was used. Green agents (VCS, QBR, ERD) can inspect this field to assess data reliability.

---

## Five Leakage Patterns

VMB runs all five diagnostics on every build:

| Pattern | What It Detects |
|---|---|
| `capability_outcome_gap` | Capabilities are delivered but not connected to promised outcomes |
| `outcome_goal_misalignment` | Realized outcomes don't map to stated business goals |
| `expectation_reality_disconnect` | Promised outcomes differ materially from delivered capabilities |
| `value_perception_disconnect` | Customer doesn't perceive or acknowledge delivered value |
| `impact_communication_failure` | Value delivered but not communicated to executive stakeholders |

---

## Environment Variables

| Variable | Description |
|---|---|
| `CRM_MCP_URL` | CRM MCP server URL |
| `CS_PLATFORM_MCP_URL` | CS platform MCP server URL |
| `PRODUCT_ANALYTICS_MCP_URL` | Product analytics MCP server URL |
| `VALUE_MAP_BASE_PATH` | Absolute path to value-maps/ root |
| `VMB_INBOX_PATH` | Path to inbox/ directory for file-based data fallback |

---

## Output

```json
{
  "status": "success",
  "account_id": "ACC-67890",
  "value_map_path": "value-maps/ACC-67890/value-map.yaml",
  "version_number": 5,
  "quadrants_updated": ["delivered_capabilities", "realized_value", "unrealized_potential"],
  "position_vector_summary": {
    "stage_1": "confirmed",
    "stage_2": "confirmed",
    "stage_3": "in_progress",
    "stage_4": "in_progress",
    "stage_5": "stalled",
    "stage_6": "not_yet_assessed",
    "stage_7": "not_yet_assessed"
  },
  "leakage_active_count": 2,
  "active_leakage_patterns": ["expectation_reality_disconnect", "value_perception_disconnect"],
  "data_sources_used": {
    "promised_outcomes": "live_mcp",
    "delivered_capabilities": "live_mcp",
    "realized_value": "file",
    "unrealized_potential": "manual"
  }
}
```

---

## NEVER Rules

- NEVER advance a value chain stage without cited evidence from a named source. Health score trends and relationship length are not evidence.
- NEVER write to a Value Map without archiving the previous version to `history/`.
- NEVER overwrite `meta.created_at` or `meta.created_by` — those are HIE-owned.
- NEVER fire an expansion signal — that is ERD's authority.
- NEVER write to the `signals` block.
- NEVER run without an existing Value Map (HIE prerequisite must be met).

---

## Relationship to Other Cookbooks

VMB is the data foundation for all Green agents. VCS reads VMB's position_vector to classify intervention priority. QBR reads VMB's realized_value and unrealized_potential to build the QBR narrative. ERD reads VMB's signals and leakage_diagnostics before generating an expansion brief.
