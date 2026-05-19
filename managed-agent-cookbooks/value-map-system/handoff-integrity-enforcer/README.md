# Handoff Integrity Enforcer (HIE)

**Type:** Blue (Write authority — Value Map initial creation)
**Role in System:** Sales-to-CS handoff gate. Fires on won-opportunity events and produces the initial Value Map for every new account.

---

## Purpose

HIE instruments the moment a deal closes. It reads the won opportunity from CRM, assesses how completely the sales team documented the value chain (stages 1–5: Product Capabilities through Expected Value), and writes a schema-valid initial Value Map to the filesystem control plane.

If the Value Map cannot be written in a schema-valid state, HIE halts completely and alerts the closing rep via Slack. There are no partial writes.

---

## Trigger

Won-opportunity event from CRM, or direct invocation:

```bash
claude --agent handoff-integrity-enforcer \
  --input '{"opportunity_id": "OPP-12345", "account_id": "ACC-67890"}'
```

---

## Subagents

| Subagent | Role | Writes |
|---|---|---|
| `won-opportunity-reader` | Pulls all available handoff data from the closed opportunity and related account record | Nothing |
| `handoff-completeness-assessor` | Scores completeness of stages 1–5 against Value Map schema; enumerates gaps by stage, field, and severity | Nothing |
| `value-chain-intake-recorder` | Validates the assembled map against the schema, archives any prior version, and writes `value-map.yaml` | `value-map.yaml`, `history/` |

---

## MCP Dependencies

| Server | Access | Required |
|---|---|---|
| `crm` | Read | Yes |
| `slack` | Write (alerts only) | Yes |

---

## Value Map Path Convention

```
value-maps/{account_id}/value-map.yaml
value-maps/{account_id}/history/{ISO-timestamp}.yaml
```

`VALUE_MAP_BASE_PATH` env var sets the root. Default: `managed-agent-cookbooks/value-map-system/value-maps/`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `CRM_MCP_URL` | CRM MCP server URL |
| `SLACK_MCP_URL` | Slack MCP server URL |
| `VALUE_MAP_BASE_PATH` | Absolute path to value-maps/ root |
| `SLACK_ALERT_CHANNEL` | Channel for hard-fail alerts (e.g., `#cs-handoff-alerts`) |

---

## Output

On success, returns a JSON handoff receipt:

```json
{
  "status": "success",
  "account_id": "ACC-67890",
  "opportunity_id": "OPP-12345",
  "value_map_path": "value-maps/ACC-67890/value-map.yaml",
  "handoff_integrity_score": 74,
  "handoff_gaps": [
    {
      "stage": 5,
      "field": "success_criteria",
      "description": "No quantified success metrics documented in opportunity",
      "severity": "major",
      "resolved": false
    }
  ],
  "version_number": 1
}
```

On failure, `status: "failed"` with `failure_reason` and Slack alert sent.

---

## NEVER Rules

- NEVER write a Value Map without passing full schema validation.
- NEVER create a Value Map for an account without a CRM opportunity record.
- NEVER write without archiving any prior version to `history/`.
- NEVER advance a value chain stage without cited evidence from a named source.
- NEVER populate `delivered_capabilities`, `realized_value`, `unrealized_potential`, or `position_vector` stages 6–7 — those are VMB's domain.

---

## Relationship to Other Cookbooks

HIE fires first. It produces the initial Value Map that every other cookbook reads. VMB picks up where HIE leaves off, populating the post-sale quadrants via live data. VCS, QBR, and ERD never run on accounts where HIE has not yet fired or has failed.
