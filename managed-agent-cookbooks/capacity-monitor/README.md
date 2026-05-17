# capacity-monitor
## Managed Agent Cookbook — rev-ops plugin v1.1.0

Monitors CS capacity headroom on a scheduled or on-demand basis. Computes
max supportable ARR against current CSM headcount, applies NRR-adjusted growth
projections, and fires threshold alerts to `#revops-alignment` with CS leadership
cc when headroom crosses critical boundaries. Surfaces hiring lead-time flags
before capacity is breached.

---

## What This Agent Does

1. Reads the practice profile from `~/.cs-agent/practice-profile.json`
2. Pulls closed-won QTD actuals from HubSpot (live connector)
3. Loads the Unit of Growth baseline file if configured
4. Computes the CS capacity model: max supportable ARR, headroom %, CSMs required, hire-by date
5. Assigns an alert level (CRITICAL / HIGH / MEDIUM / HEALTHY)
6. Posts a formatted alert to Slack — every run, including healthy ones

Healthy runs still post to confirm the monitor ran (silent-green pattern).
CRITICAL and HIGH alerts cc `#cs-leadership`.

---

## Architecture

```
capacity-monitor/
├── agent.yaml                        ← Orchestrator definition
├── README.md                         ← This file
├── steering-examples.json            ← 8 test scenarios
├── agents/
│   └── capacity-monitor.md           ← Orchestrator system prompt
└── subagents/
    ├── capacity-reader.yaml          ← Reader definition
    ├── capacity-reader.md            ← Reader system prompt
    ├── capacity-reporter.yaml        ← Reporter definition
    └── capacity-reporter.md         ← Reporter system prompt
```

### Subagent Tool Assignment

| Subagent | Filesystem | HubSpot | Slack | task |
|---|---|---|---|---|
| capacity-monitor (orchestrator) | `read` | ✓ | ✓ | ✓ |
| capacity-reader | `read` (UoG baseline) | ✓ | — | — |
| capacity-reporter | — | — | ✓ | — |

Principle of least privilege: capacity-reporter has zero filesystem access. It formats what it receives and posts to Slack — nothing more.

---

## Deployment Prerequisites

Before running for the first time:

- [ ] `rev-ops cold-start` complete — practice profile written to `~/.cs-agent/practice-profile.json`
- [ ] Required profile fields present: `current_arr`, `arr_per_csm`, `current_csm_count`
- [ ] HubSpot MCP connected (for closed-won QTD actuals; degrades to Low confidence if absent)
- [ ] Slack MCP connected (alerts delivered in-session if Slack unavailable)
- [ ] `csm_avg_ramp_days` configured (required for hire-by date calculation)
- [ ] `uog_baseline_path` optionally configured — points to `~/.cs-agent/uog-baseline.json` for plan comparison; omitting degrades confidence to Low

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `HUBSPOT_MCP_URL` | Yes | HubSpot MCP server endpoint |
| `SLACK_MCP_URL` | Yes | Slack MCP server endpoint |

---

## Practice Profile Fields (capacity-monitor consumes)

| Field | Type | Required | Description |
|---|---|---|---|
| `company_name` | string | Yes | Used in alert headers |
| `primary_segment` | string | Yes | SMB / Mid-Market / Enterprise / Strategic |
| `current_arr` | number | **Required** | Current ARR in dollars |
| `arr_per_csm` | number | **Required** | ARR each CSM manages at full capacity |
| `current_csm_count` | number | **Required** | Active CSMs today |
| `csm_avg_ramp_days` | number | Yes | Days from hire to full productivity |
| `target_growth_pct` | float | Yes | ARR growth target (decimal, e.g. 0.20 = 20%) |
| `nrr_current` | float | Yes | Net Revenue Retention (decimal, e.g. 1.08 = 108%) |
| `uog_baseline_path` | string | Optional | Path to UoG baseline JSON; empty string if not configured |

If `current_arr`, `arr_per_csm`, or `current_csm_count` are missing, the orchestrator stops and reports the missing fields. No subagents are invoked.

---

## Capacity Model Formulas

All computed by `capacity-reader` using the domain model from `rev-ops/reference/revops-domain-model.md`:

```
Max Supported ARR    = current_csm_count × arr_per_csm
Max Incremental ARR  = Max Supported ARR − current_arr
CS Headroom %        = (Max Supported ARR − current_arr) ÷ current_arr × 100

NRR_adjusted_target  = (current_arr × target_growth_pct)
                       − (current_arr × nrr_current − current_arr)

Total Managed ARR    = current_arr + NRR_adjusted_target
CSMs Required        = CEILING(Total Managed ARR ÷ arr_per_csm)
CSMs to Hire         = max(0, CSMs Required − current_csm_count)

Hire-by Date         = today − csm_avg_ramp_days
```

---

## CS Headroom Signal Thresholds

| Headroom % | Label | Alert Level | Action |
|---|---|---|---|
| < 0% | OVER_CAPACITY | **CRITICAL** | Post to both channels; G2 disclaimer; hire-by shown |
| 0–10% | NEAR_CEILING | **HIGH** | Post to both channels; G2 disclaimer |
| 10–25% | LIMITED | **MEDIUM** | Post to primary channel only |
| > 25% | HEALTHY | **HEALTHY** | Post to primary channel (confirms run) |

**Alert level overrides:**
- `hire_by_urgency = OVERDUE` → override to CRITICAL regardless of headroom
- `hire_by_urgency = URGENT` (within 30 days) → upgrade to HIGH if currently MEDIUM or below

---

## Hire-By Urgency Labels

| Condition | Label |
|---|---|
| Hire-by date is in the past | **OVERDUE** |
| Hire-by date < today + 30 days | **URGENT** |
| Otherwise | **OK** |

---

## Run Modes

### Default Run (on-demand)
```
Run /rev-ops:capacity-monitor
```
Reads practice profile, pulls HubSpot, posts live alert to Slack.

### Preview Mode
```
Run /rev-ops:capacity-monitor with preview_mode=true
```
Formats the alert and renders it in the session. No Slack posts made.
Use to inspect output before enabling a scheduled run.

### Custom Channel
```
Run /rev-ops:capacity-monitor with alert_channel="#my-channel"
```
Override the default alert destination (`#revops-alignment`).

### Scheduled Run (recommended)
Add a weekly cron trigger via the scheduled tasks system:

```
cron: 0 9 * * 1        # Every Monday at 09:00
prompt: Run /rev-ops:capacity-monitor
```

Best practice: run after the RevOps forecast update cycle (typically Monday morning).

---

## Alert Output Reference

### CRITICAL / OVER_CAPACITY Alert
```
🚨 *CS Capacity Alert — OVER_CAPACITY*
HubSpot ✓ live — as of 2026-05-15 08:30

*Vertex Growth Inc — CS headroom: -12.7%*

• Max supportable ARR: $9,600,000
• Current ARR: $11,000,000
• Headroom: *-12.7%* — OVER_CAPACITY

*CSM headcount:*
• Current: 8 CSMs
• Required at target: 11 CSMs
• Gap: *3 to hire*
• Hire-by date: *2026-02-14* — OVERDUE

⚠ _This model is a structural input. Hiring decisions require budget approval and HR process._

[Confidence: Moderate]
```

### HIGH Alert
```
⚠️ *CS Capacity Alert — LIMITED HEADROOM*
HubSpot ✓ live — as of 2026-05-15 08:30

*Meridian SaaS — CS headroom: 8.1%*

• Max supportable ARR: $20,000,000
• Headroom: *8.1%* — model next quarter before hiring AEs
• CSMs required at target: 12 | Gap: 2

• 🔶 Hire-by date approaching: *2026-06-01* (within 30 days)

⚠ _This model is a structural input. Hiring decisions require budget approval and HR process._

[Confidence: High]
```

### MEDIUM Alert
```
📊 *CS Capacity Check — NorthStar Customer Success*
HubSpot ✓ live — as of 2026-05-15 08:30

Headroom: *20.0%* — LIMITED
• Max supportable ARR: $36,000,000
• CSMs required at target: 14 | Gap: 2

No immediate action required. Recommend quarterly review.

[Confidence: High]
```

### HEALTHY Alert
```
✅ *CS Capacity Check — Acme CS Consulting*
HubSpot ✓ live — as of 2026-05-15 08:30

Headroom: *50.0%* — Healthy
No capacity constraints detected. Current CSM count (8) supports ARR target with headroom.

[Confidence: Moderate]
```

---

## Data Gap Behavior

| Condition | Behavior | Confidence Impact |
|---|---|---|
| HubSpot unavailable | Proceeds with profile ARR; freshness line shows "HubSpot — Unavailable" | Degrades to Low |
| UoG baseline file absent | Proceeds without plan comparison; no plan section in alert | Degrades to Low |
| UoG baseline file unreadable | Sets `uog_baseline_status = unavailable`; proceeds without baseline | Degrades to Low |
| Required profile fields missing | Orchestrator stops; error message lists missing fields; no subagents invoked | — |
| Slack unavailable | Alert rendered in session; delivery failure reported | No impact on model |
| HubSpot unavailable + UoG absent | Both degradations stack; confidence = Low | Low |

---

## Confidence Bands

| Condition | Confidence |
|---|---|
| HubSpot live + UoG baseline present + data < 14 days | **High** |
| HubSpot live + UoG baseline absent | **Moderate** |
| HubSpot unavailable (profile-only) | **Low** |
| Required profile fields missing | **Insufficient** — run stops |

---

## Slack Channel Routing

| Alert Level | Primary Channel | CC Channel |
|---|---|---|
| CRITICAL | `#revops-alignment` | `#cs-leadership` |
| HIGH | `#revops-alignment` | `#cs-leadership` |
| MEDIUM | `#revops-alignment` | — |
| HEALTHY | `#revops-alignment` | — |

Default channels are set in the orchestrator and can be overridden at invocation time.

---

## Guardrails

**G2 — Capacity as Structural Input**
All CRITICAL and HIGH alerts include the disclaimer:
> _"This model is a structural input. Hiring decisions require budget approval and HR process."_

This disclaimer is enforced by `capacity-reporter` and cannot be suppressed. It also appears in the orchestrator completion summary for HIGH and CRITICAL runs.

**G6 — Data Freshness**
Every alert includes a data-as-of timestamp or an explicit unavailability notice. The freshness line is never suppressed, even on healthy runs.

---

## Completion Summary Format

At the end of every run, the orchestrator reports:

```
Capacity Monitor — Run Complete
─────────────────────────────────
Company:       Meridian SaaS
CS Headroom:   8.1% — NEAR_CEILING
Alert level:   HIGH
Hire-by date:  2026-06-15
Posted to:     #revops-alignment, #cs-leadership
Confidence:    High
Run at:        2026-05-15T09:00:00Z
```

---

## Token Budget

| Run type | Typical tokens |
|---|---|
| HEALTHY run (HubSpot live, no baseline) | ~8,000 |
| MEDIUM/HIGH run with baseline | ~12,000 |
| CRITICAL run with full analysis | ~14,000 |
| Preview mode (no Slack calls) | ~6,000 |
| HubSpot unavailable (profile-only) | ~7,000 |

---

## Subagent Reference

| Subagent | Role | Key Tools |
|---|---|---|
| `capacity-reader` | Pull HubSpot actuals, load UoG baseline, compute model, assign alert level | `read` (filesystem) + HubSpot MCP |
| `capacity-reporter` | Format alert for alert level, check preview mode, post to Slack channels, return delivery receipt | Slack MCP only |

---

## Related Files

| File | Purpose |
|---|---|
| `rev-ops/reference/revops-domain-model.md` | Canonical capacity model formulas and threshold definitions |
| `rev-ops/skills/closed-won-to-cs-capacity-modeling/SKILL.md` | Skill invoked for standalone capacity analysis |
| `rev-ops/skills/unit-of-growth-calculator/SKILL.md` | UoG baseline computation (used as input to capacity model) |
| `~/.cs-agent/practice-profile.json` | Practice profile written by cold-start; read by this agent |
| `~/.cs-agent/uog-baseline.json` | UoG baseline (optional); path referenced in practice profile |
| `rev-ops/reference/token-economics.md` | Token budget details for all rev-ops managed agents |
