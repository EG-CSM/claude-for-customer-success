# RevOps Domain Model — claude-for-customer-success

Shared reference for the rev-ops plugin. Skills read this model for consistent
definitions, formulas, guardrails, and governance conventions. Do not override
these definitions in individual skill instructions — configure thresholds and
practice-specific values in the plugin CLAUDE.md.

---

## 1. Overview

This document is the single source of truth for the rev-ops plugin. It is
referenced by section anchor (`§N`) throughout all rev-ops skills. Where a
skill notes `[revops-domain-model.md §N]`, the authoritative definition lives
in the corresponding section below.

Sections in this document:

| Section | Content |
|---------|---------|
| §1 | Overview (this section) |
| §2 | Confidence Bands |
| §3 | Data Authority Hierarchy |
| §4 | Variance Classification Taxonomy |
| §5 | CS Capacity Formulas (UoG) |
| §6 | OCV Catalog Conventions |
| §7 | Pipeline Coverage Signal Thresholds |
| §8 | Churn Signal Tiers |
| §9 | Governance Tiers and Write Protocol |
| §10 | Handoff Quality Scoring Rubric |
| §11 | Output Destination Labels |

---

## 2. Confidence Bands

Used to label analytical outputs with their reliability level. All rev-ops
skills apply these bands to distinguish live-connector data from inferred,
user-provided, or fallback calculations.

| Band | Meaning | Typical source |
|------|---------|---------------|
| High | Retrieved from live connector this session; cross-referenced where possible | CRM or CS platform ✓ live |
| Moderate | Single source, not cross-referenced; or derived through calculation from verified inputs | Single-connector read, config-derived formula |
| Low | Inferred from partial data; OCV catalog absent; fallback structural signals only | Structural fallback mode, stale data |

**Labeling convention:**

```
[Confidence: High]     — live connector, primary source
[Confidence: Moderate] — single source or calculated
[Confidence: Low]      — inferred, fallback, or stale
```

**Staleness rule:** Any connector data older than 14 days is labeled
`[stale — N days]` and automatically downgrades the output to
`[Confidence: Low]`.

**Deal health bands** (as applied in deal-health-scoring):

| Band | Score range | Label |
|------|-------------|-------|
| Healthy | 75–100 | Routine engagement |
| Watch | 50–74 | Proactive outreach; identify root cause |
| At-risk | <50 | Escalation required; owner must be named |

Scores below 50 trigger `next-best-action-recommendation`. Deal health
scores are analytical inputs — the rep and manager own the response.

---

## 3. Data Authority Hierarchy

When two systems report conflicting data, the authority hierarchy below
determines the governing source. Skills never silently resolve conflicts —
they surface the conflict and apply this hierarchy to recommend which source
to use for which purpose.

```
Priority 1: HubSpot CRM
  — Governing source for: opportunity data, account records, contact data,
    deal stage, closed/won, close date, rep assignment

Priority 2: Finance-owned Sheets (Google Drive)
  — Governing source for: quota, territory assignments, comp plan baseline,
    annual plan targets

Priority 3: CS platform (via Zapier)
  — Governing source for: health scores, ARR at risk, NRR actuals,
    product usage signals, onboarding milestone status

Priority 4: Slack / Linear
  — Context only; no numerical authority.
    Use for: timing, intent signals, escalation history, commentary.
    Never override a number from Priority 1–3 with a Slack/Linear value.
```

**Root cause taxonomy for conflicts:**

| Root cause | Definition |
|------------|-----------|
| Definition mismatch | Systems use different definitions for the same metric (e.g., CRM counts by close date; Finance counts by invoice date) |
| Timing difference | Systems snapshot at different points in time (e.g., CRM is live; Finance report is month-end close) |
| Data entry gap | A transaction exists in one system but has not yet been entered in another (e.g., verbal commitment in CRM; not yet in Finance model) |
| Scope difference | Systems cover different populations (e.g., CRM includes all segments; Finance model covers Enterprise only) |

Reconciliation memos carry the output label `[Human resolution required
before either number is used in board or leadership output]`.

---

## 4. Variance Classification Taxonomy

Used by forecast-variance-analysis to classify the root cause of the gap
between submitted forecast and actual closed/won.

**Variance formulas:**

```
Variance Amount = Submitted Forecast − Actual Closed/Won
Variance %      = Variance Amount ÷ Submitted Forecast
```

**Classification categories:**

| Category | Definition |
|----------|-----------|
| Rep-level | A specific rep consistently over- or under-calls; the pattern is attributable to individual forecasting behavior |
| Deal-size band | Deals within a specific ACV range are systematically slipping; the variance concentrates in a size cohort |
| Stage-entry | Deals entering a particular stage have a structural close-rate issue from that point forward |
| Seasonal | Quarter-end compression, holiday patterns, or fiscal year dynamics are the primary driver |
| Product/segment | A specific product line or customer segment has a structural close-rate problem |

**Pattern confidence gate:**

A variance is classified as a systemic pattern only when:

- Rep-level: ≥3 deals from the same rep, or the same rep in ≥2 consecutive quarters
- All other categories: ≥3 deals matching the pattern criterion

Below threshold, use: "Insufficient data to classify as systemic — noted
as isolated variance."

**Pipeline coverage formula** (used in pipeline-coverage-analysis):

```
Required Coverage = 1 ÷ Win Rate
Pipeline Target   = New ARR Target × Required Coverage
```

---

## 5. CS Capacity Formulas (UoG)

Used by closed-won-to-cs-capacity-modeling to translate incoming sales
volume into CS resource demand. "UoG" refers to the Unit of Growth model —
each additional unit of closed ARR drives a proportional CS capacity need.

**Three-scenario capacity check:**

```
For each scenario (P10 / P50 / P90):
  New_Customers     = Scenario_New_ARR ÷ avg_deal_acv
  Total_Future_ARR  = current_arr + Scenario_New_ARR
  CSMs_Required     = CEILING(Total_Future_ARR ÷ arr_per_csm)
  CS_Gap            = CSMs_Required − current_csm_count
  Constraint_Signal = derived from CS headroom thresholds below
```

Input values (`avg_deal_acv`, `arr_per_csm`, `current_csm_count`,
`csm_avg_ramp_days`) are configured in the plugin CLAUDE.md.

**CS headroom signal thresholds:**

| Headroom % | Signal | Interpretation |
|------------|--------|---------------|
| < 0% | CRITICAL | CS already over capacity — churn risk live now |
| 0–10% | AT-RISK | Near ceiling — CS hiring is the primary growth constraint |
| 10–25% | LIMITED | Limited headroom — model next quarter before hiring AEs |
| > 25% | HEALTHY | Healthy headroom |

**Hiring lead time calculation:**

```
If CS_Gap > 0:
  Hire_By = quarter_close_date − csm_avg_ramp_days
  If Hire_By < today:
    → "CS ramp period means any hire today won't be productive
       before Q[N] close."
```

**UoG plan baseline comparison:**

When `uog_baseline_path` is present, compare CSMs_Required to the
baseline's `csm_required` value. Surface whether the practice is ahead
of, on, or behind the plan's CS hiring assumptions.

All capacity outputs carry `[G2: Structural input. Hiring requires budget
approval and HR process.]`

---

## 6. OCV Catalog Conventions

Used by deal-to-outcome-tracing and skills that reference outcome catalog
entries. OCV = Outcome & Value Catalog. Entries codify the outcome that was
sold and define how CS will verify delivery.

**Entry status lifecycle:**

| Status | Meaning |
|--------|---------|
| Draft | Entry exists but is not yet ratified; cannot satisfy handoff or rubric checks |
| Ratified | Approved entry; qualifies for D1 handoff dimension and rubric level assessment |
| Deprecated | Entry superseded; do not apply to new deals |

**G8 rule (universal):** Draft OCV entries do not count toward D1 (handoff
quality scoring) and do not qualify for rubric level assessment. Any output
referencing a Draft entry is labeled `[OCV: Draft entry — Ratified entry
required for D1 credit]`.

**OCV catalog completeness check at deal close:**

Three conditions required before CS onboarding proceeds:

```
Check 1: OCV entry referenced
  → At least one Ratified OCV entry linked to the deal in HubSpot
  → If absent: trigger handoff quality flag

Check 2: Trigger condition match
  → The OCV trigger condition is present in the account's actual situation
  → If mismatch: flag as "Sold to wrong problem"

Check 3: Measurement source accessible
  → The measurement source in the OCV entry is accessible post-close
  → If inaccessible: flag what CS needs to establish before first checkpoint
```

**Structural fallback (when OCV absent):**

```
Run Tier 1 structural risk assessment only:
  - Discount level vs. company profile threshold
  - Sales cycle vs. segment average
  - Stakeholder thread count

Label all outputs:
  [Outcome data: OCV reference absent — structural signals only — Confidence: Low]
```

**Rubric level definitions:**

| Level | Label | Definition |
|-------|-------|-----------|
| L0 | Pre-activation | Leading indicators absent per OCV rubric definition |
| L1 | In progress | Leading indicators present; primary metric not yet reached |
| L2 | Primary verified | Primary metric verified at the OCV measurement source |
| L3 | Full impact | Primary metric + secondary impact verified |

Rubric level assessment is an analytical input — CS owns the response plan.
Outputs carry `[G5: Rubric level is analytical input. CS owns the response.]`

---

## 7. Pipeline Coverage Signal Thresholds

Used by pipeline-coverage-analysis to classify coverage adequacy and signal
appropriate action.

| Coverage multiple | Signal | Interpretation |
|------------------|--------|---------------|
| < 2× | CRITICAL | Insufficient coverage — close gap immediately |
| 2×–3× | AT-RISK | Below healthy range — add pipeline this quarter |
| 3×–5× | HEALTHY | Standard coverage range |
| > 5× | INSPECT | Unusually high — verify quality; may mask selectivity issues |

Coverage thresholds are configurable in the plugin CLAUDE.md. When not
configured, the table above applies.

**Coverage calculation:**

```
Required Coverage = 1 ÷ Win Rate
Coverage Multiple = Current Pipeline ÷ New ARR Target
```

Segment-level thresholds may differ from portfolio-level thresholds.
When segment coverage is calculated, label each segment separately.

---

## 8. Churn Signal Tiers

Moves churn detection upstream from the renewal conversation to deal close.
Used by early-churn-downgrade-signal-detection and cross-referenced by
csm-risk flagging.

**Tier summary:**

| Tier | Timing | Signal type | Action owner |
|------|--------|-------------|-------------|
| Tier 1 | At deal close | Structural deal attributes | RevOps / AE manager |
| Tier 2 | 30–90 days post-onboarding | Behavioral product and engagement signals | CS manager / CSM |
| Tier 3 | 90–120 days pre-renewal | Late-stage risk signals | CS manager / executive sponsor |

### Tier 1 — Structural risk (at deal close)

Two modes; declare mode on every output:

`[Tier 1: Rule mode — configurable thresholds]`
`[Tier 1: Cohort mode — correlation-based]`

**Rule mode signals** (thresholds from company profile):

```
discount_pct > discount_elevated_threshold_pct
sales_cycle_days > avg_sales_cycle_days × tier1_long_cycle_multiplier
stakeholder_threads = 1   (single-threaded, when tier1_single_thread_flag = true)
ocv_entry_referenced = false  (no Ratified OCV at close)
```

**Cohort mode:** Requires `churn_cohort_data_path` in company profile.
Compares deal attributes to historical closed/won-to-churn cohort.
Cohort mode is unavailable below 6 months of outcome data.

### Tier 2 — Behavioral risk (30–90 days post-onboarding)

```
usage_below_adoption_curve   — product usage below expected level for this tier
ocv_rubric_stuck_at_L0       — past first checkpoint with no rubric progression
champion_departure_detected  — contact role change in CRM
ebr_qbr_rescheduled_twice    — ≥2 reschedules logged
```

### Tier 3 — Late-stage risk (90–120 days pre-renewal)

```
health_score_declining_trend     — ≥3 consecutive weeks of health score decline
renewal_conversation_not_initiated — past the renewal_conversation_window_days threshold
support_ticket_spike             — ticket volume >2× baseline
executive_sponsor_disengaged     — no activity in configured inactivity window
```

**G7 rule:** Every Tier 2 and Tier 3 flag must include a named escalation
path and owner before the flag is surfaced. A churn signal without an
escalation path is incomplete output.

---

## 9. Governance Tiers and Write Protocol

Used by deal-desk-workflow-management and discount-threshold-monitoring.
Defines the approval authority hierarchy for deal approvals and write
actions that affect production systems.

### Discount approval tiers

Thresholds are configured in the plugin CLAUDE.md. The routing logic below
applies; the numeric thresholds are practice-specific.

```
≤ discount_standard_threshold_pct      → AE manager sign-off (log in CRM)
> standard, ≤ elevated threshold       → RevOps lead approval
> elevated, ≤ executive threshold      → CRO sign-off
> executive threshold                  → CRO + Finance dual approval
```

**SLA:**

```
Standard quarter:        24-hour approval SLA
Final 2 weeks of quarter: 4-hour approval SLA
SLA breach:              Escalate to #revops-ops
```

### Deal desk workflow stages

```
Stage 1: Submission
  AE submits deal to deal desk via Linear or Slack command

Stage 2: Context brief
  RevOps assembles brief from CRM, territory, and comp data

Stage 3: Routing
  Skill determines approval tier from discount depth and deal structure

Stage 4: Decision
  Appropriate approver reviews and decides

Stage 5: Outcome log
  Decision logged in CRM and Linear; deal proceeds or is revised
```

**Routing rule:** The deal-desk skill routes only — it never approves deals
autonomously. All approvals require explicit human confirmation.

### Write Protocol

Write actions affecting production systems (CRM updates, Linear issue
creation, Slack messages) are governed by this two-tier model:

| Tier | Examples | Requirement |
|------|---------|------------|
| Read | Pulling pipeline data, generating reports | No confirmation required |
| Write | CRM field updates, Linear issue creation, Slack posts | Surface as draft; require explicit user confirmation before execution |

All Write-tier actions are surfaced as proposals. The skill describes what
will be written and waits for confirmation. No write executes without
`[User confirmed]`.

---

## 10. Handoff Quality Scoring Rubric

Used by sales-cs-handoff-quality-scoring. Five dimensions, 20 points each,
100-point total. Pass threshold: 80/100. Below-threshold deals trigger an
escalation workflow.

### Five dimensions

| Dim | Name | Points | PASS condition |
|-----|------|--------|---------------|
| D1 | OCV entry referenced | 20 | ≥1 Ratified OCV entry linked to deal in HubSpot |
| D2 | Trigger condition match | 20 | OCV trigger condition confirmed present in account context |
| D3 | Measurement source accessible | 20 | Measurement source in OCV entry is accessible to CS post-close |
| D4 | Stakeholder map transferred | 20 | Economic buyer + champion + technical contact named and tagged |
| D5 | Risk flags documented | 20 | Deal notes include risk flags OR explicit "none identified" |

FAIL condition is the inverse of PASS. D1 FAIL requires a Ratified OCV
entry — Draft entries do not satisfy D1 (G8).

### Below-threshold action (score < 80)

```
1. Create Linear issue:
   Title: "Handoff quality below threshold — [Account Name]"
   Assigned to: [AE manager]
   SLA: 48 hours
   Body: deal link, ACV, close date, failed dimensions, required actions

2. Notify CSM:
   "Handoff for [Account] is below threshold (score: [N]/100).
   Missing: [dimensions]. Linear issue [#N] assigned to [AE manager].
   Onboarding proceeds — please flag if blockers surface."

3. Log in audit trail:
   timestamp, deal ID, score, failed dimensions, issue number, CSM notified
```

CS onboarding is not blocked by a below-threshold score — the CSM is
notified and the escalation runs in parallel.

### G8 rule

Draft OCV entries do not satisfy D1. An output crediting a Draft entry
toward D1 is incorrect.

---

## 11. Output Destination Labels

Every rev-ops output must carry a destination label before distribution.
The label controls who the output is appropriate for and whether additional
review is required.

| Label | Meaning | Distribution requirement |
|-------|---------|-------------------------|
| `[DRAFT — RevOps internal]` | Working analysis; not approved for distribution | RevOps lead review required before sharing |
| `[DRAFT — for RevOps lead review before distribution]` | Brief or summary requiring lead sign-off | RevOps lead approval required |
| `[Human resolution required before use in board or leadership output]` | Reconciliation memo with open conflict | Finance or RevOps must resolve before board use |
| `[G1: Forecast qualification]` | Forward-looking projection | Include with every forecast figure — not a revenue commitment |
| `[G2: Structural input]` | Capacity or planning model output | Not a hiring mandate; requires budget approval and HR process |
| `[G5: Analytical input]` | Signal or score requiring human judgment | Rep, CSM, or manager owns the response |
| `[G7: Escalation path required]` | At-risk flag or below-threshold score | Named owner and channel required; flag is incomplete without escalation path |
| `[G9: Write-tier confirmation]` | Any write action to CRM, Linear, or Slack | Explicit user confirmation required before execution |

### Fallback behavior when a source skill is unavailable

When any source data is unavailable for a section in a brief or summary:

```
[Section N: unavailable — [Connector]: Unavailable]
```

The brief is still produced. Available sections are delivered. Degraded
sections do not block the output, but each degraded section carries an
explicit unavailability label.

---

## 12. Shared RevOps Guardrails

These guardrails apply across all rev-ops skills. They cannot be overridden
by plugin configuration or user instruction.

### G1 — No revenue commitment language

Any forecast output, scenario total, or ARR projection is a working forecast.
Skills never assert a number as a revenue commitment. Every output containing
forward-looking revenue figures carries: `[G1: Not a revenue commitment —
RevOps/Finance validation required before distribution]`.

### G2 — Structural input qualifier

Capacity models and planning outputs are structural inputs, not mandates.
Hiring, territory, and quota decisions require budget approval and HR process.
Every capacity output carries: `[G2: Structural input — requires budget
approval and HR process]`.

### G5 — Signals are inputs; humans own the response

Churn signals, deal health scores, and rubric level assessments are analytical
inputs. Skills never direct a rep, CSM, or manager to take a specific action —
they surface the signal and the recommended action. The human owns the judgment
call.

### G6 — Data-as-of required on all reads

Every output section that draws on connector data must carry the data-as-of
timestamp:

```
[CRM ✓ live — as of YYYY-MM-DD]
[CS Platform ✓ live — as of YYYY-MM-DD]
[Stale — last updated YYYY-MM-DD]
```

Never present connector data without a timestamp.

### G7 — Every flag requires a named escalation path

Risk flags, churn signals (Tier 2 and Tier 3), below-threshold handoff scores,
and above-threshold discounts all require a named escalation path: a specific
person or role, a channel, and an SLA. A flag without an escalation path is
incomplete output.

### G8 — Draft OCV entries do not satisfy rubric checks

Draft OCV entries cannot satisfy D1 (handoff scoring), trigger check, or
rubric level assessment. Any output that credits a Draft entry for these
purposes is incorrect. Draft entries are labeled `[OCV: Draft — Ratified
entry required]` when referenced.

### G9 — Write-tier confirmation

No write action executes without explicit user confirmation. All writes to
CRM, Linear, Slack, or any connected system are surfaced as proposals first.
The skill describes what will be written and waits for `[User confirmed]`.
