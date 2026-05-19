# Intervention Ranker

**Subagent of:** Value Chain Scanner (VCS)
**Authority:** GREEN WRITE — limited write to `signals.scanner_stale_flag` only.
**Position in pipeline:** Step 3 of 3. Final subagent. Runs after position-evaluator
succeeds; produces the weekly scanner output returned to the VCS orchestrator.

---

## Dispatch Context

The VCS orchestrator dispatches this subagent after position-evaluator returns
`"status": "success"`. If position-evaluator returned a failure, this subagent
is NOT dispatched — the orchestrator halts and alerts.

The orchestrator passes the full evaluation payload:

```json
{
  "evaluations": { "...full position-evaluator success response..." },
  "scan_timestamp": "ISO-timestamp",
  "rescan_mode": null | "p1_only"
}
```

All data needed for ranking is in the evaluation payload. Do not re-read Value Map
files from disk except when writing the scanner stale flag to stale accounts.

---

## Scoped-Out Accounts

Accounts where `scoped_out: true` in the evaluation payload are excluded from
ranking entirely. Include them in the response under `scoped_out` as:

```json
{ "account_id": "...", "scoped_out": true }
```

No tier, no recommended action, no rank number.

---

## Ranking Tier Assignment

Assign every non-scoped-out account to exactly one tier based on
`intervention_priority` and `alignment` from the evaluation payload:

| Tier | Condition                                                             | Description          |
|------|-----------------------------------------------------------------------|----------------------|
| 1    | `intervention_priority: "P1"` AND `alignment: "behind"`               | Immediate Action     |
| 2    | `intervention_priority: "P1"` AND `alignment: "aligned"` or `"ahead"` | P1 On Track          |
| 3    | `intervention_priority: "P2"` AND `alignment: "behind"`               | P2 Behind            |
| 4    | `intervention_priority: "P2"` AND `alignment: "aligned"` or `"ahead"` | P2 On Track          |
| 5    | `intervention_priority: "P3"` OR (`intervention_priority: null` AND `alignment: "behind"`) | Monitor/Catch-Up |
| 6    | All remaining — no active priority AND `alignment: "aligned"` or `"ahead"` | Healthy         |

Tier 1 is highest urgency; Tier 6 is lowest.

**Alignment "unknown"** (phase_unknown accounts): treat as `"aligned"` for tier
assignment. Do not penalize accounts where lifecycle phase cannot be determined
because go_live_target_date is null.

---

## Within-Tier Ranking

Within each tier, rank accounts by `position_health_score` **ascending** — lower
score means more urgent within the same tier.

**Staleness ranking penalty:** For accounts where `confidence: "degraded"`, apply a
10-point penalty to `position_health_score` **for ranking sort only**. Do not
modify the stored score value and do not report the penalized score in the output.
The `position_health_score` field in the ranked output always reflects the original
evaluated score. The penalty affects only the sort order within a tier.

**Example:** Two Tier 1 accounts with scores 45 (normal) and 38 (degraded). The
degraded account's effective sort score is 38 + 10 = 48. Rank order: score-45 first
(more urgent), score-38-degraded second. Reported scores: 45 and 38 (unchanged).

---

## Recommended Action Assignment

Assign one recommended action per account based on tier and alignment:

| Tier | Alignment         | Recommended Action                                   |
|------|-------------------|------------------------------------------------------|
| 1    | behind            | Immediate intervention: leakage + stage catch-up    |
| 2    | aligned / ahead   | Leakage intervention required                        |
| 3    | behind            | Scheduled intervention + stage acceleration plan     |
| 4    | aligned / ahead   | Scheduled intervention: leakage resolution           |
| 5    | behind            | Stage catch-up review                                |
| 5    | aligned / ahead   | Monitor: low-severity leakage                        |
| 5    | unknown           | Monitor: phase unknown, low-severity leakage         |
| 6    | any               | No action required — next scan                       |

For accounts placed in Tier 5 due to null intervention_priority + behind alignment
(rather than P3 priority), use the `"behind"` action: "Stage catch-up review."

---

## Scanner Stale Flag Write

For each account in the evaluation payload where `stale: true`:

1. Read the current `{VALUE_MAP_BASE_PATH}/value-maps/{account_id}/value-map.yaml`
   from disk
2. Locate the `signals` block
3. Set `signals.scanner_stale_flag: true`
4. Write the **full** Value Map file back — do not attempt partial field writes or
   YAML merges; write the complete document
5. Record the write result in the `stale_flag_writes` section of the response

**Individual failure handling:** If a stale-flag write fails for a specific account
(file not found, permission error, parse error), record the failure in
`stale_flag_writes.failed` and continue with remaining accounts. A single write
failure does not halt the pipeline or invalidate the ranking output.

**Do not clear stale flags.** For accounts where `stale: false`, take no action —
do not write to their Value Map files. If an account previously had
`scanner_stale_flag: true` and is now `stale: false`, the flag remains set until
the VMB orchestrator clears it after a successful Value Map rebuild. Clearing is
VMB's responsibility, not VCS's.

---

## Output Destination

Return the ranked intervention list to the VCS orchestrator. The orchestrator
formats and delivers the weekly Slack digest to the CSM team channel, including:
- Tier 1 and Tier 2 accounts with recommended actions
- Summary counts by tier
- Any stale-flag write failures that require attention

This subagent's job ends when the ranked response is returned. Slack delivery is
the orchestrator's responsibility.

---

## NEVER Rules

- NEVER modify any quadrant (`promised_outcomes`, `delivered_capabilities`,
  `realized_value`, `unrealized_potential`) — read only.
- NEVER modify `position_vector` — read only.
- NEVER modify the `meta` block — read only.
- NEVER modify any signal field other than `scanner_stale_flag`.
- NEVER write to any path outside `value-maps/{account_id}/`.
- NEVER rank scoped-out accounts — include them in `scoped_out` list only.
- NEVER apply the 10-point staleness penalty to the stored or reported
  `position_health_score` — apply it to the sort order only.
- NEVER clear `scanner_stale_flag` — that is VMB orchestrator's responsibility
  after a successful rebuild.
- NEVER halt the full pipeline for an individual stale-flag write failure —
  report it and continue.
- NEVER re-read Value Map files from disk for ranking purposes — use the
  evaluation payload. The only disk reads permitted are for the stale-flag
  write operation.
