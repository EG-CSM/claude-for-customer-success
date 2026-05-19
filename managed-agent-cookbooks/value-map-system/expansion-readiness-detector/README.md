# Expansion Readiness Detector (ERD)

**Type:** Green (Read authority — writes expansion signals and brief file only)
**Role in System:** Expansion gate. Scores an account against a configurable readiness threshold and produces a specific expansion brief when the threshold is met. Hard-blocked if active leakage exists in the Delivered Value quadrant.

---

## Purpose

ERD answers the question that precedes every expansion conversation: is this account actually ready? Not "is the renewal approaching?" but "have we delivered sufficient value and do we have a specific, credible angle?"

It evaluates seven scoring dimensions against an account's Value Map, computes a composite readiness score, compares it to a segment-appropriate threshold, and either fires the expansion signal (with a named brief) or explains why it didn't. The hard block on active leakage is non-negotiable — no expansion conversation should start while delivery problems exist.

---

## Prerequisites

1. HIE must have fired for the account (Value Map must exist).
2. VMB must have run at least once (quadrant data must be populated).
3. No active leakage in `delivered_capabilities` or `realized_value` quadrant (hard block — see below).

---

## Trigger

On demand, or triggered by VCS when `intervention_priority` is P4 and expansion context warrants investigation:

```bash
claude --agent expansion-readiness-detector \
  --input '{"account_id": "ACC-67890"}'
```

---

## Subagents

| Subagent | Role | Writes |
|---|---|---|
| `readiness-scorer` | Evaluates all seven scoring dimensions; computes composite score; compares to segment threshold | Nothing |
| `expansion-brief-generator` | Produces a specific, named expansion brief from unrealized_potential items; runs only when threshold is met | `signals/{account_id}-expansion-brief.md` |

The orchestrator checks the leakage hard-block before dispatching either subagent, and writes signal fields to the Value Map after scoring completes.

---

## MCP Dependencies

| Server | Access | Required |
|---|---|---|
| `cs-platform` | Read | Yes |
| `crm` | Read | Yes |
| `slack` | Write (expansion signal alert) | Yes |

---

## Hard Block: Active Leakage

If any active leakage pattern exists in the Delivered Value quadrant (`capability_outcome_gap`, `outcome_goal_misalignment`, or `expectation_reality_disconnect` where `active: true`), ERD fires no expansion signal. This is an absolute constraint with no override.

The output in this case:

```json
{
  "status": "blocked",
  "block_reason": "Active leakage in delivered quadrant",
  "active_leakage_patterns": ["capability_outcome_gap", "expectation_reality_disconnect"],
  "signal_fired": false
}
```

And a brief is written explaining the block so the CSM understands why expansion was not surfaced.

---

## Expansion Readiness Thresholds (Configurable)

| Segment | Default Threshold |
|---|---|
| Enterprise | 80 |
| Mid-Market | 75 |
| SMB | 70 |

Override via environment variables: `EXPANSION_THRESHOLD_ENTERPRISE`, `EXPANSION_THRESHOLD_MID_MARKET`, `EXPANSION_THRESHOLD_SMB`.

---

## Seven Scoring Dimensions

| Dimension | What It Measures | Weight |
|---|---|---|
| Value Chain Progression | Stages 5–7 status and trajectory | 20% |
| Outcome Realization Rate | realized_value count / promised_outcomes count | 20% |
| Capability Adoption Depth | adoption_rate_pct mean + workflow_completion_rates | 15% |
| Stakeholder Engagement | Confirmed CS platform touchpoints only (never inferred) | 15% |
| Business Goal Alignment | Stage 4 evidence linked to realized_value | 15% |
| Leakage-Free Delivery | Inverse of active leakage pattern count | 10% |
| Expansion Surface Area | unrealized_potential items with expansion_angle: true | 5% |

Weights are configurable via `SCORING_WEIGHTS` env var.

---

## Stakeholder Engagement Rule

**Only confirmed touchpoints recorded in the CS platform count toward Dimension 4.** Inferred relationship quality, relationship length, or deal history do not count. If no confirmed CS platform touchpoints exist for key stakeholders, Dimension 4 scores 0.

---

## Signal Fields Written

ERD writes to these Value Map signal fields only:

```yaml
signals:
  expansion_readiness_signal: true/false
  expansion_readiness_score: 0-100
  expansion_readiness_threshold: 80 | 75 | 70
  expansion_signal_fired_at: "ISO-timestamp"  # only when signal_fired: true
```

---

## Expansion Brief Structure

When threshold is met, the brief at `signals/{account_id}-expansion-brief.md` contains:

```
1. Expansion Readiness Score and Threshold
2. Scoring Dimension Breakdown
3. 1–3 Specific, Named Expansion Angles
   (each references a specific unrealized_potential item)
4. Evidence Citations per Angle
5. Recommended Next Action
   (named stakeholder, specific ask, timeframe)
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `CS_PLATFORM_MCP_URL` | CS platform MCP server URL |
| `CRM_MCP_URL` | CRM MCP server URL |
| `SLACK_MCP_URL` | Slack MCP server URL |
| `VALUE_MAP_BASE_PATH` | Absolute path to value-maps/ root |
| `ERD_SIGNALS_PATH` | Path to signals/ output directory |
| `SLACK_ALERT_CHANNEL` | Channel for expansion signal alerts |
| `EXPANSION_THRESHOLD_ENTERPRISE` | Enterprise threshold (default: 80) |
| `EXPANSION_THRESHOLD_MID_MARKET` | Mid-market threshold (default: 75) |
| `EXPANSION_THRESHOLD_SMB` | SMB threshold (default: 70) |
| `SCORING_WEIGHTS` | Comma-separated dimension:weight pairs |

---

## Output Receipt

```json
{
  "status": "success",
  "account_id": "ACC-67890",
  "segment": "enterprise",
  "expansion_readiness_score": 83,
  "expansion_readiness_threshold": 80,
  "signal_fired": true,
  "scoring_dimensions": {
    "value_chain_progression": 90,
    "outcome_realization_rate": 85,
    "capability_adoption_depth": 78,
    "stakeholder_engagement": 70,
    "business_goal_alignment": 88,
    "leakage_free_delivery": 100,
    "expansion_surface_area": 60
  },
  "brief_path": "signals/ACC-67890-expansion-brief.md",
  "slack_alert_sent": true
}
```

---

## NEVER Rules

- NEVER fire an expansion signal when active leakage exists in the Delivered Value quadrant. This is an absolute hard block.
- NEVER score stakeholder engagement from inferred relationship data. Only confirmed CS platform touchpoints count.
- NEVER produce an expansion brief without a specific, named expansion angle.
- NEVER write to any Value Map field other than the four signal fields listed above.

---

## Relationship to Other Cookbooks

ERD is the terminal gate in the expansion pipeline. VCS surfaces priority classification; ERD scores and signals. QBR may surface expansion angles in a brief, but ERD is the authoritative signal source for expansion readiness. When ERD fires `expansion_readiness_signal: true`, the expansion onboarding agent (a separate cookbook) picks up from that signal to initiate the expansion motion.
