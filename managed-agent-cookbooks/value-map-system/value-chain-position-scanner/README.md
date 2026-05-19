# Value Chain Position Scanner (VCS)

**Type:** Green (Read authority — writes signal flags only)
**Role in System:** Portfolio-wide weekly scan. Classifies every account's value chain position against lifecycle expectations and surfaces intervention priorities to CSMs.

---

## Purpose

VCS answers the question every CS team needs answered weekly: which accounts are falling behind where they should be in the value chain, and how urgent is it?

It reads every account's Value Map, compares their current position_vector status against the lifecycle × value chain matrix, classifies P1–P4 intervention priority, and writes priority signals back to each map. P1 accounts get Slack alerts to their CSM owner and a Thursday mid-week re-scan to confirm whether the situation is deteriorating.

VCS is read-only at the data level — it never modifies quadrants, position_vector, or leakage diagnostics. It writes to the `signals` block only.

---

## Trigger

Scheduled weekly (Monday 06:00) or on-demand:

```bash
# Full portfolio scan
claude --agent value-chain-position-scanner

# P1 mid-week re-scan (Thursday 06:00)
claude --agent value-chain-position-scanner \
  --input '{"rescan_mode": "p1_only"}'
```

---

## Subagents

| Subagent | Role | Writes |
|---|---|---|
| `portfolio-reader` | Discovers and loads all Value Maps; validates each; flags corrupted or missing maps | Nothing |
| `position-evaluator` | Compares each account's position_vector against the lifecycle × value chain matrix; identifies below-threshold accounts and stale maps | Nothing |
| `intervention-ranker` | Classifies P1–P4 priority for every account; ranks P1 accounts for immediate escalation | Nothing |

The orchestrator writes signal fields to each Value Map after all three subagents complete.

---

## MCP Dependencies

| Server | Access | Required |
|---|---|---|
| `cs-platform` | Read (lifecycle stage, health scores) | Yes |
| `slack` | Write (P1 alerts to CSM owners) | Yes |

---

## Lifecycle × Value Chain Matrix

Expected minimum position by lifecycle stage:

| Lifecycle Stage | Duration | Expected Value Chain Position |
|---|---|---|
| Onboarding | 0–90 days | Stages 1–2 confirmed |
| Early Adoption | 91–180 days | Stage 3 in_progress or better |
| Adoption | 181–365 days | Stages 3–4 confirmed |
| Value Realization | 1–2 years | Stages 5–6 confirmed |
| Renewal / Expansion | 2+ years | Stages 6–7 in_progress or better |

Accounts below the expected minimum trigger alert classification.

---

## Priority Classification

| Priority | Condition |
|---|---|
| **P1** | Below expected position AND health score declining. Thursday re-scan required. |
| **P2** | Below expected position OR health score declining (not both). |
| **P3** | At expected position but active leakage patterns detected. |
| **P4** | At or above expected position, no active leakage, healthy trajectory. |

---

## P1 Mid-Week Re-Scan (Thursday 06:00)

For all accounts where `p1_midweek_rescan_required: true`:
- Re-evaluate current position
- If deterioration confirmed → escalate to P0, Slack alert tagged "ESCALATED TO P0"
- If stable or improved → update priority to P2 or better; clear the re-scan flag

---

## Stale Map Detection

A Value Map is considered stale if `meta.last_value_map_build` is older than 30 days (configurable via `VCS_STALE_THRESHOLD_DAYS`). Stale maps are scanned and classified, but their priority rating is noted as reduced confidence in the scan report.

---

## Signal Fields Written

VCS writes to these Value Map signal fields only:

```yaml
signals:
  scanner_stale_flag: true/false
  scanner_stale_flagged_at: "ISO-timestamp"
  intervention_priority: P1 | P2 | P3 | P4
  intervention_classified_at: "ISO-timestamp"
  p1_midweek_rescan_required: true/false
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `CS_PLATFORM_MCP_URL` | CS platform MCP server URL |
| `SLACK_MCP_URL` | Slack MCP server URL |
| `VALUE_MAP_BASE_PATH` | Absolute path to value-maps/ root |
| `SLACK_ALERT_CHANNEL` | Channel for P1 alerts |
| `VCS_STALE_THRESHOLD_DAYS` | Days before a map is considered stale (default: 30) |

---

## Output

```json
{
  "status": "success",
  "scan_timestamp": "2026-05-18T06:00:00Z",
  "accounts_scanned": 147,
  "accounts_skipped": 3,
  "priority_distribution": { "P1": 4, "P2": 12, "P3": 28, "P4": 103 },
  "p1_accounts": [
    {
      "account_id": "ACC-00123",
      "csm_owner": "sarah.chen@company.com",
      "gap_description": "Stage 4 stalled for 45 days; health declining 3 weeks consecutive"
    }
  ],
  "stale_maps": ["ACC-00456", "ACC-00789"],
  "slack_alerts_sent": 4
}
```

---

## NEVER Rules

- NEVER write to quadrants, position_vector, or leakage_diagnostics.
- NEVER modify any meta field except the five signal fields listed above.
- NEVER escalate a P1 to P0 without running the Thursday re-scan and confirming deterioration.
- NEVER skip stale maps — scan them, note staleness in the report.

---

## Relationship to Other Cookbooks

VCS reads from VMB's output. ERD monitors VCS's `expansion_readiness_signal` (set by ERD itself, not VCS) and the overall priority classification. QBR uses the priority context when preparing briefs. VCS is the portfolio-wide early warning system that drives the downstream intervention chain.
