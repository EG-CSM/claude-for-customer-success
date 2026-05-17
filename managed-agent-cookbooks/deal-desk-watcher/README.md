# deal-desk-watcher
## Managed Agent Cookbook — rev-ops plugin v1.0.0

Monitors all in-flight deals for SLA breaches across four signal types:
stage age, approval aging, close date drift, and single-threaded late-stage
risk. Breach records are written to a local SLA log with a mandatory human
confirmation gate. A prioritized breach digest is delivered to Slack.

---

## Architecture

```
deal-desk-watcher/
├── agent.yaml                          # Orchestrator manifest
├── agents/
│   └── deal-desk-watcher.md            # Orchestrator behavioral spec
├── subagents/
│   ├── deal-stage-reader.yaml          # CRM evaluation subagent manifest
│   ├── deal-stage-reader.md            # CRM evaluation spec
│   ├── sla-log-writer.yaml             # Local log write subagent manifest
│   ├── sla-log-writer.md               # Local log write spec
│   ├── deal-alert-poster.yaml          # Slack delivery subagent manifest
│   └── deal-alert-poster.md            # Slack delivery spec
├── steering-examples.json              # 9 behavioral test scenarios
└── README.md                           # This file
```

### Subagent tool assignment

| Subagent | Filesystem | HubSpot | Slack |
|----------|-----------|---------|-------|
| deal-stage-reader | read only | ✓ | — |
| sla-log-writer | **write only** | — | — |
| deal-alert-poster | **none** | — | ✓ |
| Orchestrator | read + task | ✓ | ✓ |

The sla-log-writer has write but NOT read access. It receives all data it
needs via the orchestrator payload — read access would only widen the attack
surface without adding capability.

---

## Prerequisites

- rev-ops plugin installed (`../../rev-ops`)
- Practice profile at `~/.cs-agent/practice-profile.json` (see § Practice Profile)
- Two MCP connectors configured:
  - `HUBSPOT_MCP_URL` — deal pipeline data
  - `SLACK_MCP_URL` — alert delivery
- Write access to `~/.cs-agent/` (for SLA log)

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HUBSPOT_MCP_URL` | HubSpot MCP server URL |
| `SLACK_MCP_URL` | Slack MCP server URL |

---

## Practice Profile

The orchestrator reads `~/.cs-agent/practice-profile.json` before invoking
any subagent. The following fields govern deal watcher behavior:

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `company_name` | **yes** | — | Displayed in digest header; watcher stops if missing |
| `stage_sla_days` | no | `14` | Days in a deal stage before flagging SLA breach |
| `approval_aging_hours` | no | `48` | Hours a pricing/discount approval can be pending |
| `close_date_drift_count` | no | `2` | Times a close date can move in a quarter before flagging |
| `late_stage_threshold_pct` | no | `75` | Deal probability % above which single-threaded flag applies |
| `min_acv_filter` | no | `0` | Minimum deal ACV to include in scan; 0 = all deals |
| `open_stage_names` | no | `null` | Stage names considered in-flight; null = auto-detect |
| `alert_channel` | no | `"#revops-alignment"` | Primary Slack channel |
| `sla_log_path` | no | `"~/.cs-agent/deal-desk-sla-log.json"` | SLA breach log path |

If `company_name` is missing, the orchestrator stops before invoking any
subagent and reports the configuration error.

---

## SLA Breach Types

### Breach Type 1 — Stage SLA

**Condition:** `days_in_stage > stage_sla_days`

Computed as calendar days since `stage_entered_date`. Severity scales with
overage: Critical if overage exceeds 2× the threshold; High if within 2×.

### Breach Type 2 — Approval Aging

**Condition:** `pending_approval_type` is non-null AND `hours_pending > approval_aging_hours`

Applies to discount and pricing exception approvals. Always rated Critical —
an aging approval blocks deal progression and risks close date slip.

### Breach Type 3 — Close Date Drift

**Condition:** Close date moved ≥ `close_date_drift_count` times within the current calendar quarter

Counts moves within the current quarter only (Q start = first day of current
quarter). Rated High. If `close_date_history` is unavailable from HubSpot,
this signal is marked `unevaluable` for that deal.

### Breach Type 4 — Single-Threaded Late Stage

**Condition:** `deal_probability_pct >= late_stage_threshold_pct` AND `contact_count <= 1`

High-probability deals with only one contact are single points of failure.
Rated Medium. Surfaces before the deal is at risk, not after.

---

## Severity Tiers

| Breach Type | Condition | Severity |
|-------------|-----------|---------|
| `approval_aging` | Any | Critical |
| `stage_sla` | Overage > 2× threshold | Critical |
| `stage_sla` | Overage ≤ 2× threshold | High |
| `close_date_drift` | Move count ≥ threshold | High |
| `single_threaded_late_stage` | Probability ≥ threshold, ≤ 1 contact | Medium |

When a deal has multiple breach types, deal-level severity = highest severity
among individual breach types.

Digest sort order: Critical → High → Medium, ACV descending within each tier.

---

## Governance Protocol — Section 9 Write Tier

Appending records to the SLA log is a **Write** operation. The sla-log-writer
enforces a mandatory human confirmation gate before any filesystem write.

**Confirmation flow:**

1. Subagent renders a proposed record table:
   ```
   | # | Deal | ACV | Severity | Breach Types | Owner |
   ```

2. Operator responds:
   - `"confirm all"` — write all records
   - `"confirm N, M"` — write records N and M only
   - `"skip all"` — do not write any records

3. Records are written only for confirmed entries.

4. A write-audit log entry is produced for each record:
   ```json
   {
     "timestamp": "ISO timestamp",
     "skill_name": "deal-desk-watcher/sla-log-writer",
     "operation_type": "sla_log_append",
     "deal_id": "...",
     "deal_name": "...",
     "log_path": "...",
     "human_approval_status": "approved | skipped",
     "approver_response": "confirm all | confirm N,M | skip all",
     "outcome": "written | skipped | failed"
   }
   ```

This gate is **not skippable** — not even when only one breach record is
present. The `require_confirmation: true` flag is always sent by the
orchestrator.

Downstream Slack delivery is not blocked by the log write decision: the
digest posts regardless of whether records are written, skipped, or if the
log write fails.

---

## SLA Log Format

Each record appended to `~/.cs-agent/deal-desk-sla-log.json`:

```json
{
  "log_id": "ddw-[deal_id]-[epoch_seconds]",
  "timestamp": "ISO timestamp",
  "company_name": "string",
  "deal_id": "string",
  "deal_name": "string",
  "owner": "string or null",
  "acv": 0,
  "stage_name": "string",
  "close_date": "YYYY-MM-DD",
  "severity": "Critical | High | Medium",
  "breach_types": ["string"],
  "breach_details": [...],
  "scan_run_at": "ISO timestamp",
  "logged_by": "deal-desk-watcher/sla-log-writer"
}
```

The log is **append-only**. Existing records are never overwritten or deleted.
If the file does not exist at `sla_log_path`, it is created with an empty
array `[]` before the first record is appended.

---

## Slack Alert Format

### Structure

| Section | Always shown | Condition |
|---------|-------------|-----------|
| Header (company, deal counts, data freshness) | ✓ | — |
| Breach rows (sorted by severity, then ACV) | — | breaches non-empty |
| No-breach confirmation | — | breaches empty |
| SLA log write summary | ✓ | — |
| G5 disclaimer | ✓ | — |

### Sample breach row

```
🔴 *Acme Corp Enterprise — $210,000*
Owner: Sarah Chen | Stage: Proposal | Close: 2026-05-31
Breach: Approval aging: pricing_exception pending 61h (threshold 48h)
---
🟠 *Globex Industries — $95,000*
Owner: unassigned | Stage: Discovery | Close: 2026-06-15
Breach: Stage SLA: 31d in stage (threshold 14d, 17d over)
---
🟡 *Initech LLC — $320,000*
Owner: Tom Kaplan | Stage: Negotiation | Close: 2026-05-28
Breach: Single-threaded: 80% probability, 1 contact(s)
```

### Sample no-breach digest

```
*Acme Corp — Deal Desk Watcher*
Deals evaluated: 14 | Breaches found: 0
Data as of: 2026-05-15 09:22

✅  No SLA breaches detected. All in-flight deals are within thresholds.

SLA Log: No breaches to log
_Deal stage data and SLA flags are analytical inputs. The deal owner and RevOps team own the decision._
```

### Staleness warning

If HubSpot data is more than 24 hours old, the digest header includes:
```
⚠️  HubSpot data is stale ([age]h old) — flags should be verified before action.
```

---

## Data Gap Behavior

| Condition | Behavior |
|-----------|----------|
| HubSpot unavailable | **Hard stop** — orchestrator reports error and stops; no downstream subagents invoked |
| `stage_entered_date` missing | `stage_sla` signal marked `unevaluable` for that deal; other signals evaluated normally |
| `close_date_history` unavailable | `close_date_drift` signal marked `unevaluable` for that deal; other signals evaluated normally |
| `pending_approval_created_at` missing | `approval_aging` signal marked `unevaluable` for that deal; other signals evaluated normally |
| HubSpot data > 24 hours stale | All deals evaluated; staleness warning added to digest header |
| SLA log write fails | `write_status=failed` surfaced in digest; Slack delivery proceeds normally |

Unevaluable signals are surfaced explicitly in the breach row so the RevOps
team knows which signals were not assessed and can check HubSpot directly.

---

## Run Modes

| Mode | Command | Behavior |
|------|---------|----------|
| Standard run | `run deal desk watcher` | Full evaluation, log confirmation gate, Slack delivery |
| Preview | `preview deal desk watcher` | Full evaluation, log confirmation gate, no Slack delivery |
| Scheduled | cron `0 8 * * 1` | Standard run at 08:00 every Monday |

For scheduled runs, set cron expression in your rev-ops plugin scheduler:
```
0 8 * * 1   # Every Monday at 08:00
0 8 * * *   # Every morning at 08:00
```

---

## Completion Summary Format

```
Deal Desk Watcher — Run Complete
─────────────────────────────────────
Company:          Acme Corp
Deals evaluated:  14
Breaches found:   3
Log entries:      3 written (completed)
Posted to:        #revops-alignment
Data freshness:   2026-05-15 09:22
Run at:           2026-05-15T09:23:44Z
```

When breaches are present, the completion summary appends:
```
[Internal — RevOps] — G8: all SLA flags include owner and age. Review deal health in HubSpot.
```

---

## Token Budget

| Stage | Estimated tokens |
|-------|-----------------|
| Orchestrator overhead + practice profile read | ~1,000 |
| deal-stage-reader (HubSpot pull + 4-signal evaluation) | ~3,000–6,000 (scales with deal count) |
| sla-log-writer (confirmation gate + file write) | ~1,000–1,500 |
| deal-alert-poster (format + Slack delivery) | ~1,200–2,000 |
| **Total (typical mid-market pipeline, 20–50 open deals)** | **~6,000–11,000** |

---

## Guardrails

**G5** — All deal risk outputs include:
*"Deal stage data and SLA flags are analytical inputs. The deal owner and
RevOps team own the decision."*

**G6** — Every digest surfaces the HubSpot data-as-of timestamp. Never omitted,
even when no breaches are present.

**G8** — Every breach row in the digest must name: deal owner (or "unassigned"),
days in stage or hours pending approval, and breach type. A flag without an
owner and age is noise. The deal-alert-poster enforces this on every breach row.

---

## Subagent Reference

| Subagent | Spec file | Purpose |
|----------|-----------|---------|
| deal-stage-reader | `subagents/deal-stage-reader.md` | Pulls HubSpot deal data; evaluates 4 SLA breach types; returns severity-sorted breach list |
| sla-log-writer | `subagents/sla-log-writer.md` | Human-confirmed append to local SLA log; write-audit per Section 9 |
| deal-alert-poster | `subagents/deal-alert-poster.md` | Formats breach digest; delivers to Slack or returns preview |

---

## Related Files

| File | Description |
|------|-------------|
| `../../rev-ops/skills/` | Rev-ops skill library loaded by orchestrator |
| `~/.cs-agent/practice-profile.json` | Practice configuration (SLA thresholds, filter settings) |
| `~/.cs-agent/deal-desk-sla-log.json` | Append-only SLA breach log (created on first write) |
| `steering-examples.json` | 9 behavioral test scenarios |
| `../churn-signal-scanner/` | Companion cookbook — account churn risk monitoring |
| `../capacity-monitor/` | Companion cookbook — CS headroom monitoring |
| `../gtm-pulse-runner/` | Companion cookbook — GTM KPI briefing |
