# Planning Cycle Orchestrator
## claude-for-customer-success / rev-ops plugin

Managed-agent cookbook that tracks a GTM planning cycle through five sequential
phases, evaluates pipeline coverage via HubSpot, gates every state write behind
a human confirmation prompt, and delivers a formatted digest to Slack after every
run. Designed for quarterly GTM planning cadences managed by a RevOps lead.

---

## Architecture

The orchestrator delegates to three specialised subagents. Each subagent holds
only the permissions it needs — no subagent can both write state and post to
Slack, and no subagent can both read HubSpot and write the state file.

```
planning-cycle-orchestrator/
├── agent.yaml
├── agents/
│   └── planning-cycle-orchestrator.md
├── subagents/
│   ├── phase-state-reader.yaml
│   ├── phase-state-reader.md
│   ├── phase-gate-writer.yaml
│   ├── phase-gate-writer.md
│   ├── cycle-digest-poster.yaml
│   └── cycle-digest-poster.md
├── steering-examples.json
└── README.md
```

### Subagent Tool Assignment

| Subagent | Filesystem | HubSpot MCP | Slack MCP |
|---|---|---|---|
| phase-state-reader | read only | ✓ | — |
| phase-gate-writer | write only | — | — |
| cycle-digest-poster | none | — | ✓ |
| Orchestrator | read + task | ✓ | ✓ |

---

## Prerequisites

- Claude Agent SDK (managed-agent runtime)
- HubSpot MCP server with deal pipeline read access
- Slack MCP server with `chat:write` scope on the alert channel
- A `practice_profile.json` (or equivalent) in the rev-ops plugin providing
  the fields listed below

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `HUBSPOT_MCP_URL` | URL of the HubSpot MCP server |
| `SLACK_MCP_URL` | URL of the Slack MCP server |

---

## Company Profile Fields

The orchestrator reads the following fields from the company profile. Fields
marked **required** trigger a hard stop if absent.

| Field | Required | Default | Purpose |
|---|---|---|---|
| `company_name` | **required** | — | Used in digest header and all subagent payloads |
| `planning_cycle_name` | recommended | `"Planning Cycle"` | Human-readable cycle label in digest |
| `planning_quarter` | recommended | `"Current Quarter"` | Quarter label (e.g. `"Q2 2026"`) |
| `pipeline_coverage_target` | optional | `3.0` | Coverage ratio target for pipeline-review evaluation |
| `quota_lock_date` | optional | `null` | ISO date; surfaced in digest when quota-setting is active |
| `alert_channel` | optional | `"#revops-alignment"` | Slack channel for digest delivery |
| `cycle_state_path` | optional | `"~/.cs-agent/planning-cycle-state.json"` | Filesystem path to the cycle state file |

---

## Planning Cycle Phases

The five phases run in strict sequence. A phase may not open until all
preceding phases are `complete`. No phase can be skipped.

| # | `phase_id` | Name | Purpose |
|---|---|---|---|
| 1 | `pipeline-review` | Pipeline Review | Validate pipeline coverage against target ratio before quota-setting begins |
| 2 | `quota-setting` | Quota Setting | Set individual and team quotas for the planning period |
| 3 | `territory-design` | Territory Design | Define account and geographic territories aligned to quotas |
| 4 | `resource-planning` | Resource Planning | Confirm headcount, tools, and budget against the plan |
| 5 | `launch-readiness` | Launch Readiness | Final go/no-go check before the planning cycle is declared complete |

---

## Governance Protocol — Write-Audit Log

Every state mutation is gated behind a **single-record human confirmation
prompt** presented by phase-gate-writer before any file is touched.

```
CONFIRMATION GATE RULES:
- require_confirmation is always true — not configurable
- The gate is presented for: phase advances, blocker additions, blocker resolutions
- Accepted responses: "confirm" (proceed) or "skip" / any other (cancel)
- A skip is a valid outcome — not an error
- The state file is NEVER written without an explicit "confirm" response
```

Every write attempt (successful, skipped, or failed) produces a write-audit
log entry:

```json
{
  "timestamp": "ISO timestamp",
  "skill_name": "planning-cycle-orchestrator/phase-gate-writer",
  "operation_type": "advance | add_blocker | resolve_blocker",
  "cycle_id": "string",
  "phase_id": "string",
  "cycle_state_path": "string",
  "human_approval_status": "approved | skipped",
  "approver_response": "operator's exact response",
  "outcome": "written | skipped | failed",
  "detail": "string describing what changed, or why it failed"
}
```

---

## Cycle State File Format

The state file is a single JSON object at `cycle_state_path`. It is created on
the **first confirmed gate write** of a cycle — a status check alone never
creates the file.

```json
{
  "cycle_id": "string (e.g. fy27-gtm-q2-2026)",
  "company_name": "string",
  "planning_cycle_name": "string",
  "planning_quarter": "string",
  "created_at": "ISO timestamp",
  "last_updated_at": "ISO timestamp",
  "overall_status": "on_track | at_risk | blocked | complete",
  "phases": [
    {
      "phase_id": "pipeline-review",
      "name": "Pipeline Review",
      "status": "pending | in_progress | complete | blocked",
      "owner": "string or null",
      "target_date": "ISO date or null",
      "completed_date": "ISO date or null",
      "entry_criteria": [
        {
          "criterion_id": "string",
          "description": "string",
          "met": true | false | null,
          "unevaluable": true | false,
          "unevaluable_reason": "string or null"
        }
      ],
      "exit_criteria": [ ... same schema as entry_criteria ... ],
      "blockers": [
        {
          "blocker_id": "blk-[phase_id_slug]-[epoch_seconds]",
          "description": "string",
          "raised_at": "ISO timestamp",
          "raised_by": "operator",
          "resolved_at": "ISO timestamp or null"
        }
      ],
      "transitions": [
        {
          "from_status": "string",
          "to_status": "string",
          "transitioned_at": "ISO timestamp",
          "approved_by": "operator"
        }
      ]
    }
    // ... 4 more phase objects
  ]
}
```

### Key Invariants

- **State file lifecycle** — A missing state file initialises an empty
  5-phase structure in memory only. The file is only written to disk on
  the first confirmed gate write. A corrupt (invalid JSON) state file
  triggers a hard stop — it is never repaired or overwritten.

- **Transitions are append-only** — The `transitions` array is never
  overwritten; every state change appends a new record. This provides a
  full audit trail for the cycle lifetime.

- **Blocker records persist** — Resolved blockers have `resolved_at` set
  but remain in the `blockers` array. Records are never deleted.

- **Phase returns to `in_progress` only when ALL blockers are resolved** —
  A partial resolution (some blockers resolved, others not) leaves the
  phase `blocked`.

- **Exit criteria confirmation** — Exit criteria are marked `met: true`
  ONLY when the operator explicitly transitions a phase to `complete`.
  HubSpot data alone never confirms exit criteria — this is the core
  integrity constraint of the gate system.

- **`completed_date`** — Set only on the phase being explicitly
  transitioned to `complete`. Never set speculatively.

- **`blocker_id` format** — `blk-[phase_id_slug]-[epoch_seconds]`
  (e.g. `blk-quota-setting-1747302000`). Generated by phase-gate-writer
  at write time.

---

## Slack Digest Format

The digest is posted to `alert_channel` after every run (Mode A, B, and C).

### Digest Structure

```
*[company_name] — Planning Cycle Status*
[planning_cycle_name] — [planning_quarter]  |  Cycle: [cycle_id]
Status: [STATUS_EMOJI] [overall_status_label]  |  Data as of: [hubspot_data_as_of]

*Phase Status*
─────────────────────────────────────────────────────────
1. Pipeline Review      [EMOJI] [status]   [owner_or_dash]   [target_date_or_dash]
2. Quota Setting        [EMOJI] [status]   [owner_or_dash]   [target_date_or_dash]
3. Territory Design     [EMOJI] [status]   [owner_or_dash]   [target_date_or_dash]
4. Resource Planning    [EMOJI] [status]   [owner_or_dash]   [target_date_or_dash]
5. Launch Readiness     [EMOJI] [status]   [owner_or_dash]   [target_date_or_dash]
─────────────────────────────────────────────────────────

*Pipeline Coverage*
Open pipeline:  $[total_open_pipeline]  ([open_deal_count] deals)
Coverage ratio: [pipeline_coverage_ratio]×  (target: [pipeline_coverage_target]×)
Coverage gap:   [COVERAGE_EMOJI] [gap_label]

[🔴 *[phase_name] — Blocked*  — shown only when a phase is blocked]
  • [description]  |  Raised by: [raised_by]  |  [raised_at YYYY-MM-DD HH:MM]

*Next Action*
[NEXT_EMOJI] [next_actionable_phase or "Cycle complete — all phases finished"]

*Gate Write*
[WRITE_EMOJI] [write_summary_label]

_Phase status and entry/exit criteria are analytical inputs. The RevOps lead and planning committee own the go/no-go decision for each phase._
```

**Status emojis:**
- `on_track` → ✅  `at_risk` → ⚠️  `blocked` → 🔴  `complete` → 🏁

**Phase status emojis:**
- `pending` → ⬜  `in_progress` → 🔵  `complete` → ✅  `blocked` → 🔴

**Gate Write labels:**
- `completed` → `✅  [operation_performed]`
- `skipped` → `⏭️  Operator skipped gate write — no state changes made`
- `failed` → `⚠️  Gate write failed — [operation_performed]`
- `not_triggered` → `—  No gate write triggered (status check only)`

### Sample Digest — On Track

```
*Meridian Systems — Planning Cycle Status*
FY27 GTM Planning — Q2 2026  |  Cycle: fy27-gtm-q2-2026
Status: ✅ On Track  |  Data as of: 2026-05-15T14:30:00Z

*Phase Status*
─────────────────────────────────────────────────────────
1. Pipeline Review      ✅ complete      —   —
2. Quota Setting        🔵 in_progress   —   —
3. Territory Design     ⬜ pending       —   —
4. Resource Planning    ⬜ pending       —   —
5. Launch Readiness     ⬜ pending       —   —
─────────────────────────────────────────────────────────

*Pipeline Coverage*
Open pipeline:  $4,200,000  (38 deals)
Coverage ratio: 4.2×  (target: 3.0×)
Coverage gap:   ✅  1.2× above target

*Next Action*
🔵 Quota Setting — in progress

*Gate Write*
—  No gate write triggered (status check only)

_Phase status and entry/exit criteria are analytical inputs. The RevOps lead and planning committee own the go/no-go decision for each phase._
```

### Sample Digest — Blocked

```
*Meridian Systems — Planning Cycle Status*
FY27 GTM Planning — Q2 2026  |  Cycle: fy27-gtm-q2-2026
Status: 🔴 Blocked  |  Data as of: 2026-05-15T14:30:00Z

*Phase Status*
─────────────────────────────────────────────────────────
1. Pipeline Review      ✅ complete      —   —
2. Quota Setting        🔴 blocked       —   —
3. Territory Design     ⬜ pending       —   —
4. Resource Planning    ⬜ pending       —   —
5. Launch Readiness     ⬜ pending       —   —
─────────────────────────────────────────────────────────

*Pipeline Coverage*
Open pipeline:  $4,200,000  (38 deals)
Coverage ratio: 4.2×  (target: 3.0×)
Coverage gap:   ✅  1.2× above target

🔴 *Quota Setting — Blocked*
  • Finance approval for Q3 quota bands pending — Sarah Chen OOO until May 20  |  Raised by: operator  |  2026-05-15 10:30

*Next Action*
🔴 Quota Setting — blocked; resolve blockers before advancing

*Gate Write*
✅  Add blocker to quota-setting: Finance approval for Q3 quota bands pending — Sarah Chen OOO until May 20

_Phase status and entry/exit criteria are analytical inputs. The RevOps lead and planning committee own the go/no-go decision for each phase._
```

---

## HubSpot Unavailable Behaviour

**This orchestrator does NOT hard-stop when HubSpot is unavailable** — this is
a deliberate design difference from deal-desk-watcher, which does hard-stop.

When HubSpot is unreachable:

- The `pipeline-review` phase criteria that require HubSpot data are marked
  `unevaluable: true` with `unevaluable_reason: "HubSpot unavailable"`
- The digest header shows:
  `Data as of: unavailable — HubSpot offline`
- The Pipeline Coverage section shows:
  `⚠️  HubSpot unavailable — pipeline coverage data not evaluated`
- The run continues through all remaining orchestrator steps
- HubSpot status is recorded in `scan_metadata.hubspot_status: "unavailable"`

The digest is still posted to Slack. Phase state reads and gate writes proceed
normally. Only pipeline-coverage-dependent criteria are affected.

---

## Data Gap Behaviour

| Condition | Behaviour | Hard Stop? |
|---|---|---|
| `company_name` missing from company profile | Report missing field; show recovery hint | **Yes** |
| State file is invalid JSON | Report corruption; show recovery hint | **Yes** |
| State file does not exist | Initialise empty 5-phase structure in memory only | No |
| HubSpot unavailable | Mark pipeline criteria `unevaluable`; continue run | No |
| HubSpot returns no open deals | Report 0 pipeline; coverage ratio = 0; run continues | No |
| Phase sequence violation (e.g. skip a phase) | Report violation; do not invoke phase-gate-writer | No |
| Operator declines confirmation ("skip") | Record `write_status: skipped`; post digest with pre-write state | No |
| Slack post fails | Record `delivery_status: failed`; include failure reason in response | No |

---

## Run Modes

| Mode | Trigger phrases | Phase-gate-writer invoked? | State file written? |
|---|---|---|---|
| **A — Status check** | "show planning cycle", "planning cycle status" | No | No |
| **B — Phase advance** | "open [phase]", "mark [phase] complete" | Yes (with confirmation) | Yes (on confirm) |
| **C — Blocker update** | "add blocker to [phase]: …", "resolve blocker [id]" | Yes (with confirmation) | Yes (on confirm) |
| **Preview** | Any command + `preview_mode: true` | No | No |
| **Scheduled** | Cron / scheduled task runner | No (status check only) | No |

---

## Completion Summary Format

After every run the orchestrator returns a structured completion summary:

```
Planning Cycle Orchestrator — Run Complete
──────────────────────────────────────────────────────
Company:         [company_name]
Planning cycle:  [planning_cycle_name] — [planning_quarter]
Overall status:  [STATUS_EMOJI] [overall_status_label]
Phases complete: [N]/5
Next action:     [next_actionable_phase or "Cycle complete"]
Gate write:      [WRITE_EMOJI] [write_summary_label]
Posted to:       [alert_channel or "—  preview mode"]
Data freshness:  [hubspot_data_as_of or "HubSpot offline"]
Run at:          [ISO timestamp]
──────────────────────────────────────────────────────
```

---

## Token Budget

| Mode | Approximate token range |
|---|---|
| Mode A — Status check (no write) | 4,500 – 7,000 |
| Mode B — Phase advance | 5,500 – 8,500 |
| Mode C — Blocker update | 5,500 – 8,500 |

Ranges vary with pipeline deal count and phase count. Larger HubSpot pipelines
increase Mode A cost; confirmation exchanges add one round-trip in Modes B/C.

---

## Guardrails

### G5 — Analytical Inputs Disclaimer

The disclaimer line:

> _Phase status and entry/exit criteria are analytical inputs. The RevOps lead and planning committee own the go/no-go decision for each phase._

must appear in **every digest, every run** — including previews and runs with
no gate write. It is never conditional.

### G6 — Data Freshness Timestamp

The `Data as of:` line in the digest header must appear in **every digest,
every run**. If HubSpot is unavailable, the line shows
`Data as of: unavailable — HubSpot offline` — it is never omitted.

### G8 — Blocked Phase Attribution

Every blocked-phase detail block must include the blocker **description**,
**raised_by**, and **raised_at**. If any attribution field is missing, the
block renders a visible inline warning:

```
• [description]  |  ⚠️  Attribution missing — raised_by or raised_at not recorded
```

Missing attribution is never silently suppressed.

---

## Subagent Reference

| Subagent | Spec file | What it does |
|---|---|---|
| `phase-state-reader` | `subagents/phase-state-reader.md` | Reads cycle state file + HubSpot pipeline; evaluates entry/exit criteria; returns phases array and scan metadata |
| `phase-gate-writer` | `subagents/phase-gate-writer.md` | Presents confirmation prompt; on confirm, applies advance / add_blocker / resolve_blocker to state file; returns write summary and audit log |
| `cycle-digest-poster` | `subagents/cycle-digest-poster.md` | Builds formatted Slack digest from orchestrator payload; posts to alert channel; returns delivery summary and `digest_preview` |

---

## Related Files

| File | Purpose |
|---|---|
| `agent.yaml` | Orchestrator manifest — model, tools, MCP servers, callable agents |
| `agents/planning-cycle-orchestrator.md` | Orchestrator system prompt — mode detection, sequence rules, hard stop conditions, subagent invocation logic |
| `steering-examples.json` | 10 behavioural test scenarios (SE-PCO-001 through SE-PCO-010) covering all modes, hard stops, sequence violations, HubSpot unavailability, and operator skip |
| `../../rev-ops/practice_profile.json` | Source of company_name, planning cycle name, quarter, coverage target, alert channel, and state file path |
| `../deal-desk-watcher/README.md` | Related cookbook — HubSpot deal monitoring; note behavioural difference: deal-desk-watcher hard-stops on HubSpot unavailability; this orchestrator does not |
