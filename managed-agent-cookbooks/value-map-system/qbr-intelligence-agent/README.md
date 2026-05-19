# QBR Intelligence Agent (QBR)

**Type:** Green (Read authority — writes brief file only, not Value Map)
**Role in System:** QBR preparation engine. Generates a structured, evidence-grounded intelligence brief for a CSM conducting a Quarterly Business Review.

---

## Purpose

QBR answers the preparation problem every CSM faces before a QBR: pulling together value delivered, account trajectory, risk areas, and expansion angles from scattered systems into a coherent narrative in time for the meeting.

It reads the full Value Map (including version history), collects 90-day evidence from CS platform and product analytics, and produces a structured Markdown brief. The brief is opinionated — it flags active leakage as risk topics, blocks expansion sections when leakage exists in the delivered quadrant, and cites every figure to a named source.

---

## Prerequisites

1. HIE must have fired for the account (Value Map must exist).
2. VMB must have run at least once (`meta.last_value_map_build` populated).
3. If the map is stale (`signals.scanner_stale_flag: true`), the brief is generated with a data confidence warning.

---

## Trigger

On demand, pre-QBR:

```bash
claude --agent qbr-intelligence-agent \
  --input '{
    "account_id": "ACC-67890",
    "meeting_date": "2026-06-15",
    "stakeholders": ["Jane Smith (CFO)", "Mark Reyes (VP Ops)"]
  }'
```

---

## Subagents

| Subagent | Role | Writes |
|---|---|---|
| `evidence-collector` | Pulls 90-day touchpoints, health trend, usage events, workflow completion rates, renewal date, and stakeholder list from all connected MCP sources | Nothing |
| `value-narrative-generator` | Constructs the QBR brief narrative: executive summary, value delivered, value chain position, active leakage, and recommended conversation topics | Nothing |
| `expansion-angle-identifier` | Reviews unrealized_potential for expansion-flagged items; produces 1–3 specific named expansion angles; blocks this section if active leakage exists in delivered quadrant | Nothing |

The orchestrator assembles and writes the final brief after all three subagents complete.

---

## MCP Dependencies

| Server | Access | Required |
|---|---|---|
| `crm` | Read | Yes |
| `cs-platform` | Read | Yes |
| `product-analytics` | Read | Yes |
| `slack` | Write (brief delivery notification) | Yes |

---

## Brief Output Structure

The brief is a Markdown document written to `briefs/{account_id}-{meeting_date}.md`:

```
1. Account Snapshot
   Key metadata: ARR, renewal date, segment, CSM owner, champion, exec sponsor

2. Executive Summary
   One paragraph, referenced metrics only

3. Value Delivered This Quarter
   realized_value items with evidence sources and before/after metrics

4. Value Chain Position
   Current stage status, trajectory, and what progression to stage N+1 requires

5. Risk Flags / Active Leakage
   Severity-ranked leakage patterns; each with description and recommended topic

6. Recommended Conversation Topics
   Derived from leakage patterns and stalled stages

7. Expansion Angles
   1–3 specific, named angles from unrealized_potential
   — OR —
   [BLOCKED] section with reason (active leakage in delivered quadrant)

8. Data Confidence Notes
   data_source per quadrant; stale map flag; any gaps noted
```

---

## Expansion Blocking Rule

If `signals.hard_block_active: true` OR `signals.intervention_priority` is P1 or P2, the expansion section is replaced with a blocked notice. The determination uses **only** these two signal fields — quadrant-level leakage pattern fields (e.g., `leakage_diagnostics.patterns.*`) are NOT checked for this purpose.

```
## Expansion Angles

> **[BLOCKED]** Expansion angles are not presented when signals.hard_block_active
> is true or signals.intervention_priority is P1 or P2.
> Resolve the active intervention before advancing an expansion conversation.
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `CRM_MCP_URL` | CRM MCP server URL |
| `CS_PLATFORM_MCP_URL` | CS platform MCP server URL |
| `PRODUCT_ANALYTICS_MCP_URL` | Product analytics MCP server URL |
| `SLACK_MCP_URL` | Slack MCP server URL |
| `VALUE_MAP_BASE_PATH` | Absolute path to value-maps/ root |
| `QBR_BRIEFS_PATH` | Path to briefs/ output directory |
| `QBR_LOOKBACK_DAYS` | Evidence collection window in days (default: 90) |

---

## Output Receipt

```json
{
  "status": "success",
  "account_id": "ACC-67890",
  "meeting_date": "2026-06-15",
  "brief_path": "briefs/ACC-67890-2026-06-15.md",
  "value_chain_position_summary": "Stage 4 confirmed; Stage 5 in_progress with medium confidence",
  "active_leakage_count": 1,
  "expansion_angles_count": 2,
  "expansion_blocked": false,
  "data_confidence_flags": ["realized_value sourced from file (not live_mcp)"]
}
```

---

## NEVER Rules

- NEVER generate a QBR brief without reading the full Value Map history.
- NEVER present expansion angles when `signals.hard_block_active` is true OR `signals.intervention_priority` is P1 or P2 — show the blocked section with reason. Do NOT check quadrant-level leakage pattern fields for this determination.
- NEVER fabricate metrics or evidence. Every figure must cite a named source.
- NEVER write to any Value Map field, including signals.
- NEVER produce vague expansion language. Every angle must be specific and named.

---

## Relationship to Other Cookbooks

QBR reads VMB's quadrant data and VCS's priority classification for context. It does not trigger ERD — expansion angle identification in QBR is preparatory context for the CSM; ERD is the system that formally scores and signals readiness. Brief content and ERD output are complementary but independent.
