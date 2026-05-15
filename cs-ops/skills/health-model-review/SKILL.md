---
name: health-model-review
description: >
  Audit the portfolio health model — distribution analysis, component weight
  validation, threshold calibration, signal freshness, and predictive accuracy
  assessment. Use quarterly or when churn patterns diverge from health
  classifications. Produces an ops-level health model assessment with
  calibration recommendations, not account-level health reviews (use
  /csm:health-score-review for individual accounts).
argument-hint: "[--distribution | --calibration | --component-audit | --full]"
version: "1.0.0"
---

# /cs-ops:health-model-review

Audit the health model at the portfolio level — does it actually predict
churn, or does it just classify accounts?

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
and `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/cs-ops:cold-start-interview`.

Critical configuration to apply:
- Health model source of truth (CS platform / CRM / manual)
- Components and weights as configured
- Green / Yellow / Red thresholds
- Last calibration date against churn outcomes
- Data quality staleness threshold

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G1 (health scores are heuristics — calibration findings must not be framed as churn predictions).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--full`: Complete health model audit — distribution, component analysis,
threshold calibration, and recommendations. **Default.**

`--distribution`: Portfolio health distribution snapshot only — how many
accounts are in each tier, ARR concentration, and trend vs. prior period.
Lightweight; suitable for weekly leadership reporting.

`--calibration`: Predictive accuracy assessment — did Red accounts actually
churn at higher rates? Did Green accounts renew? Requires historical data.

`--component-audit`: Component-by-component scoring review — which components
are driving classification changes, which are stale, which lack data coverage.

---

## Data gathering

Pull from connected integrations:
- CS Platform: health scores, component scores, lifecycle stages, CTA counts
- CRM: ARR by account, renewal dates, churned accounts (last 12 months),
  expansion/contraction events, segment classification

If nothing is connected:
> "To run a health model review, I need portfolio-level health data.
> Share a health score export — one row per account with: account name,
> ARR, segment, health score, component scores if available, and renewal date.
> I'll run the analysis from what you provide."

Minimum required before proceeding: health classification for each account
(Red/Yellow/Green or numeric score), ARR per account, segment.

---

## Full health model audit (`--full`)

---

**Health Model Audit**
*[Date] · INTERNAL — CS-Ops use only*
*Health model source: [configured source] · Data as of: [timestamp]*

---

### Portfolio health distribution

| Tier | Accounts | % of book | ARR | % of ARR | Prior period | Change |
|------|----------|-----------|-----|----------|-------------|--------|
| 🟢 Green | [N] | [%] | $[amount] | [%] | [N] | [↑↓→ N] |
| 🟡 Yellow | [N] | [%] | $[amount] | [%] | [N] | [↑↓→ N] |
| 🔴 Red | [N] | [%] | $[amount] | [%] | [N] | [↑↓→ N] |
| **Total** | [N] | 100% | $[total ARR] | 100% | | |

**ARR at risk (Red + Yellow):** $[amount] — [%] of total ARR

**Distribution interpretation:**
[2-3 sentences on what the distribution signals — not just restating the table.
E.g., "The Red tier concentration in the Enterprise segment represents [%] of
total ARR, which is [above / below / at] the typical 10–15% benchmark for
well-functioning CS organizations. The Yellow-to-Red migration rate of [N] accounts
in [period] warrants investigation into whether Yellow thresholds are correctly
calibrated or whether recovery plays are failing to prevent deterioration."]

---

### Distribution flags

Automated checks against the configured model:

| Check | Status | Detail |
|-------|--------|--------|
| Red ARR > 20% of total | [⚠️ Flag / ✅ OK] | [Red ARR is [%] of total] |
| Green-tier accounts with upcoming renewal (<90 days) | [N accounts / [%] of Green] | [Names or count] |
| Red-tier accounts without an active CTA or play | [N accounts / $ARR] | [Data gap — accounts at risk with no assigned action] |
| Health scores not updated in >[configured threshold] days | [N accounts] | [Stale data risk] |
| Accounts with no health score assigned | [N accounts / $ARR] | [Coverage gap] |

---

### Component analysis (`--component-audit` content)

For each configured health component:

| Component | Weight | Avg score (Green) | Avg score (Yellow) | Avg score (Red) | Data coverage | Staleness |
|-----------|--------|------------------|--------------------|-----------------|--------------|-----------|
| [Component 1, e.g., Usage] | [40%] | [score] | [score] | [score] | [%] of accounts have data | [% updated in threshold window] |
| [Component 2, e.g., Engagement] | [20%] | | | | | |
| [Component 3, e.g., Support load] | [20%] | | | | | |
| [Component 4, e.g., NPS] | [20%] | | | | | |

**Component interpretation:**

For each component where anomalies exist:

> **[Component name] — [flag type]:**
> [What the anomaly is, what it might mean, what action it implies]
>
> Example: "Usage is weighted at 40% but has only 67% data coverage — meaning
> 33% of accounts receive a health score with usage defaulted to zero or averaged
> from available data. This artificially depresses scores for accounts where
> product instrumentation is incomplete, not where usage is actually low.
> Recommend: resolve instrumentation gaps before the next health model calibration,
> or weight usage conditionally by segment." `[review]`

---

### Threshold calibration assessment (`--calibration` content)

Requires historical churn data (last 12 months minimum).

**Predictive validity check:**

| Health tier at 90 days pre-renewal | Churned | Renewed | Expanded | Predictive accuracy |
|------------------------------------|---------|---------|----------|---------------------|
| 🔴 Red | [N] ([%]) | [N] ([%]) | [N] ([%]) | [Red → churn rate] |
| 🟡 Yellow | [N] ([%]) | [N] ([%]) | [N] ([%]) | [Yellow → churn rate] |
| 🟢 Green | [N] ([%]) | [N] ([%]) | [N] ([%]) | [Green → churn rate] |

**Calibration verdict:**

| Finding | Detail |
|---------|--------|
| Red accounts that renewed | [N] — false positives driving unnecessary escalation |
| Green accounts that churned | [N] — false negatives that bypassed churn intervention |
| Predictive accuracy score | [Red churn rate − Green churn rate] — [interpretation] |

**Calibration interpretation:**

[2-3 sentences on whether the health model is predictive. Name the primary failure
mode: false positives (over-flagging healthy accounts) or false negatives
(missing accounts that churn). Recommend threshold adjustment if warranted.]

If historical data is not available:
> "Calibration assessment requires historical churn data (which accounts churned,
> their health classification at 90 days pre-renewal). This data was not available
> from connected sources. Recommend running the calibration assessment manually:
> pull churned accounts from the last 12 months, join to their health scores at
> 90-day pre-renewal, and compare classification to outcome." `[review]`

---

### Health model recommendations

Ranked by impact. Specific and actionable — not generic.

**Priority 1 — [Recommendation headline]:**
[What to change, why, what outcome to expect. Reference specific data from
the audit above. Example: "Reduce the Green threshold from >70 to >75 — [N]
accounts currently classified Green would move to Yellow, better reflecting
the [%] of accounts in the 70-75 range that churned in the last 12 months."]

**Priority 2 — [Recommendation headline]:**
[...]

**Priority 3 — [Recommendation headline]:**
[...]

If no changes are warranted:
> "The health model is performing within expected parameters. No calibration
> changes are recommended at this time. Schedule next review for [date — per
> configured review cadence]."

---

### Portfolio health distribution only (`--distribution`)

---

**Portfolio Health Snapshot — [Date]**
*[N] accounts · $[total ARR] · Source: [configured health source]*

| Tier | Accounts | ARR | Change (WoW / MoM) |
|------|----------|-----|---------------------|
| 🟢 Green | [N] ([%]) | $[amount] ([%]) | [↑↓→] |
| 🟡 Yellow | [N] ([%]) | $[amount] ([%]) | [↑↓→] |
| 🔴 Red | [N] ([%]) | $[amount] ([%]) | [↑↓→] |

**ARR at risk:** $[Red + Yellow ARR] ([%] of total)

**Movement since last snapshot:**
- Green → Yellow: [N accounts, $ARR]
- Yellow → Red: [N accounts, $ARR]
- Red → Yellow (recovering): [N accounts, $ARR]
- New Red this period: [N accounts, $ARR]

**Top Red accounts by ARR:** [list with renewal dates — for weekly triage]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live | CRM ✓ live | user-provided export — [date] | conversation context only]
> - **Health model version applied:** [Configured model — components and weights | No formal model — tier signals only]
> - **Calibration data:** [Historical churn data available — [period] | Not available — calibration assessment skipped]
> - **Component coverage gaps:** [N components with <80% data coverage — flagged in component analysis]
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Threshold changes require:** Sign-off from [configured health model owner] before applying in CS platform.

---

## Output

Health model audit report — format driven by `--quick` (default) or `--full` flag.
Produces a structured markdown report with: scoring signal inventory, weight
justifications, threshold analysis, benchmark comparison, and recommended changes.
See **Full health model audit** section for field-level detail.

## Guardrails

**Health scores are heuristics.** The health model review identifies
calibration issues; it does not override individual CSM judgment on
specific accounts. Component anomalies are audit findings, not
directives.

**Calibration requires historical data.** A calibration assessment
without churn outcome data produces a description, not a verdict.
Surface the data gap explicitly rather than speculating on predictive
accuracy.

**Threshold changes affect active escalations.** Before recommending
threshold changes, note that accounts currently in Red may move to Yellow
(or vice versa), affecting active CTAs and escalation routing. Recommend
a transition plan alongside any threshold change.

**Coverage gaps vs. score problems.** Distinguish between a component
that is scoring poorly and a component that has no data. A zero-coverage
component is a data pipeline problem; a poorly-scoring component with
full coverage is a calibration problem. The corrective action differs.

**No revenue implications without validation.** ARR-at-risk figures from
the distribution must be validated against CRM renewal dates and contract
values before sharing with finance or leadership.

---

## After the review

- "Red-tier accounts need triage — run: `/cs-ops:segment-analyzer --at-risk`"
- "Component coverage gaps identified — check data quality: `/cs-ops:data-quality-check`"
- "Threshold change recommended — update the model: `/cs-ops:customize --section health-model`"
- "Want the portfolio metrics dashboard: `/cs-ops:metric-dashboard`"
- "Capacity issues surfaced in Red tier — check CSM load: `/cs-ops:capacity-planner`"
