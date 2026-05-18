---
name: early-churn-downgrade-signal-detection
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Three-tier churn signal model starting at deal close (not renewal). Tier 1 fires at close using configurable rule-mode thresholds (or cohort-mode correlations when 6+ months of data available). Tier 2 fires 30–90 days post-onboarding on behavioral signals. Tier 3 fires 90–120 days pre-renewal on late-stage risk. Every flag includes escalation path and owner. Triggers: 'churn signals', 'early churn', 'downgrade risk', 'at-risk accounts', 'churn detection', 'which accounts are at risk of churning'."
---

# Early Churn / Downgrade Signal Detection

Moves churn detection upstream from renewal conversation to deal close.
The earlier the signal, the more runway to act.

**Reference:** Churn signal tiers → `../../../shared/revops-domain-model.md §8`
**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `tier1_mode`, `discount_elevated_threshold_pct`,
`avg_sales_cycle_days`, `renewal_conversation_window_days`, `cs_platform_connected`

---

## Use when
- Account shows structural signals suggesting churn or downgrade risk
- Tier 1 accounts need proactive churn signal monitoring
- Deal desk context brief requires churn signal assessment for a specific account

## Do NOT use for
- Deal health scoring on pre-close pipeline (use deal-health-scoring)
- Outcome rubric level assessment (use deal-to-outcome-tracing)
- Revenue brief generation (this is a signal, not a brief)

## Typical activation
"Churn signal for [account]", "early churn detection", "downgrade risk", "Tier 1 churn signals", "flag at-risk accounts"

---

## Reasoning Protocol

1. Confirm activation — user asking about churn risk, at-risk accounts, or downgrade signals
2. Determine scope: single account or portfolio scan
3. Check CS platform for health score, usage, renewal date
4. Declare tier1_mode: rule or cohort [Practice profile]
5. Apply G7 — every Tier 2 and Tier 3 flag includes escalation path and named owner
6. Apply G5 — signals are analytical inputs; CS and CS manager own the response
7. Apply G6 — data-as-of on all reads

---

## Three Tiers `[revops-domain-model.md §8]`

### Tier 1 — Structural risk (at deal close)

Declare mode on every output:
`[Tier 1: Rule mode — configurable thresholds]` or
`[Tier 1: Cohort mode — correlation-based]`

**Rule mode signals (defaults from practice profile):**
```
discount_pct > discount_elevated_threshold_pct
sales_cycle_days > avg_sales_cycle_days × tier1_long_cycle_multiplier
stakeholder_threads = 1  (single-threaded, if tier1_single_thread_flag = true)
ocv_entry_referenced = false  (no Ratified OCV at close)
```

**Cohort mode:** Requires `churn_cohort_data_path` in practice profile.
Compares deal attributes to historical closed/won-to-churn cohort.

### Tier 2 — Behavioral risk (30–90 days post-onboarding)
```
usage_below_adoption_curve  — product usage below expected for tier
ocv_rubric_stuck_at_L0      — past first checkpoint
champion_departure_detected — contact role change in CRM
ebr_qbr_rescheduled_twice   — ≥2 reschedules logged
```

### Tier 3 — Late-stage risk (90–120 days pre-renewal)
```
health_score_declining_trend — ≥3 consecutive weeks of decline
renewal_conversation_not_initiated — past standard window
support_ticket_spike — ticket volume >2x baseline
executive_sponsor_disengaged — no activity in [N] days
```

---

## Output Formats

**Single account:**
```
CHURN SIGNAL ASSESSMENT — [Account Name]
[CRM ✓ live / CS Platform ✓ live — as of YYYY-MM-DD]
[Tier 1: Rule mode] [Confidence: High/Moderate]

ACV: $XXXk  Segment: [segment]  Days to renewal: [N]

Active signals:
  Tier 1: [✓ / —]  [Signal description if firing]
  Tier 2: [✓ / —]  [Signal description if firing]
  Tier 3: [✓ / —]  [Signal description if firing]

Highest active tier: [Tier N]
Recommended action: [Specific — not generic]
  WHO: [CS manager / CSM / AE]
  BY:  [Timeframe]

[G7: Escalation path — [CS manager name/role] via [channel] within [timeframe]]
[G5: Signal is analytical input. CS owns the response.]
```

**Portfolio scan:**
```
CHURN SIGNAL SCAN — [Portfolio/Segment] — [Date]
[CS Platform ✓ live — as of YYYY-MM-DD] [Tier 1: Rule mode]

Tier 3 (pre-renewal, immediate action):  [N] accounts  $XXXk ARR at risk
Tier 2 (behavioral, near-term action):   [N] accounts  $XXXk ARR at risk
Tier 1 (structural, monitor):            [N] accounts  $XXXk ARR at risk

Top 5 highest-ACV accounts by risk tier:
[table]

[G7: Each flagged account requires named escalation path]
[G5: Signals are inputs. CS leadership owns the response plan.]
```

---

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal, customer, and revenue data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G7: Every Tier 2 and Tier 3 flag requires escalation path and owner — no exceptions
- G5: Signals are inputs; rep and manager own judgment
- G6: Data-as-of required on all reads
- Cross-plugin: Tier 3 flags → suggest `/csm:risk-flag` and `/renewals:renewal-prep`
