# CS Domain Model — claude-for-customer-success

Shared reference for all plugins. Skills read this model for consistent
definitions, formulas, and guardrails. Do not override these definitions
in individual skill instructions — configure thresholds in plugin CLAUDE.md.

---

## 1. Health Model

### Score range and bands

| Band | Score range | Label | Default action |
|------|-------------|-------|---------------|
| Healthy | 75–100 | 🟢 Green | Routine engagement; monitor for expansion signals |
| Watch | 50–74 | 🟡 Yellow | Proactive outreach; identify root cause within 14 days |
| At Risk | 25–49 | 🔴 Red | Escalation required; owner must be named |
| Critical | 0–24 | 🔴 Red (Critical) | Immediate executive involvement |

Thresholds (Green/Yellow cutoffs) are configured in each plugin's CLAUDE.md and
override these defaults. The band labels and escalation logic above are shared
across all plugins.

### Component model

Health score = weighted sum of configured components. Typical components:

| Component | Typical weight range | Signal type |
|-----------|---------------------|-------------|
| Product usage | 30–50% | Quantitative — DAU, feature adoption, last login |
| Engagement | 15–25% | Qualitative — call frequency, stakeholder breadth |
| Support load | 10–20% | Inverse — open P1/P2 tickets, escalation history |
| NPS / sentiment | 10–20% | Survey — most recent score, trend |
| Outcome achievement | 10–20% | Milestone or success criteria completion |

Actual components and weights are defined in the plugin CLAUDE.md. Skills
read configured weights; they do not apply the default table above if config
is present.

### Staleness threshold

Health data older than **14 days** is considered stale. When any component
data exceeds this threshold:
- Flag it in the Reviewer note as `[stale — [N] days since last update]`
- Downgrade the health classification confidence to `[Low Confidence]`
- Do not suppress the health score output — surface it with the staleness flag

### Health score interpretation rule

Health scores are **heuristics**, not verdicts. A Red classification means
the configured thresholds are breached, not that churn is certain. Skills
never say "this account will churn." They say "the health classification is
Red based on [component evidence]" and recommend CSM action.

---

## 2. Customer Segmentation

Standard segment labels used across all plugins:

| Segment | Typical ARR range | CS motion |
|---------|------------------|-----------|
| Enterprise | Top tier (configure in company-profile) | High-touch / named CSM |
| Mid-Market | Mid tier | Scaled high-touch |
| SMB | Entry tier | Tech-touch / pooled |

Segment boundaries are configured in company-profile.md. These labels are
placeholders — the configured values govern. Skills that segment output
(portfolio triage, TtV analysis, segment-analyzer) read segment definitions
from config.

---

## 3. Revenue Formulas

### GRR (Gross Revenue Retention)

```
GRR = (Starting ARR − Churn ARR − Contraction ARR) / Starting ARR × 100
```

- **Starting ARR**: Total ARR at the beginning of the measurement period
- **Churn ARR**: ARR from accounts that did not renew (lost)
- **Contraction ARR**: ARR reduction at renewal (downsell)
- **Expansion is excluded from GRR** — always
- GRR ceiling: 100% (cannot exceed starting ARR without expansion)

### NRR (Net Revenue Retention)

```
NRR = (Starting ARR − Churn ARR − Contraction ARR + Expansion ARR) / Starting ARR × 100
```

- **Expansion ARR**: New ARR from upsell or cross-sell within existing accounts
- NRR can exceed 100% when expansion exceeds churn + contraction
- Expansion is included in NRR **only when**: (a) an economic buyer qualifying
  conversation has occurred AND (b) the expansion is in formal pipeline

Unqualified expansion is tagged `[early signal — not yet qualified]` and shown
separately in NRR calculations.

---

## 4. Renewal Forecast

### Default pipeline stage weights

| Stage | Definition | Default weight |
|-------|-----------|---------------|
| Open | Outreach initiated; no directional signal | 70% |
| Verbal commitment | Customer indicated renewal intent, no signature | 90% |
| At risk | Active churn signals; escalation in progress | 25% |
| Won | Renewal executed; ARR confirmed | 100% |
| Lost / Churn | Non-renewal confirmed | 0% |

Plugin CLAUDE.md may override default weights. Skills apply configured weights
when present; fall back to this table when not configured.

### Scenario modeling parameters

| Scenario | Open accounts | Verbal | At risk | Expansion |
|----------|--------------|--------|---------|-----------|
| Best case | 85% | 100% | 50% save | 30% (if signaled) |
| Likely | 70% (default weight) | 100% | 20% save | Excluded |
| Worst case | 50% | 90% | 0% save | Excluded |

Likely case is the submit-to-leadership number. Best and worst bracket the range.

---

## 5. Time-to-Value (TtV)

### Definition

**TtV** = number of days from contract start date to M4 (First Value) completion —
the date the customer achieves their first measurable outcome per their success
criteria.

M5 is the graduation/handoff milestone. M4 is the value milestone. TtV measures
M0 (contract start) → M4.

### Pace multiplier

```
Pace multiplier = actual days elapsed / planned days elapsed
                  (at the most recently completed milestone)
```

| Pace multiplier | Interpretation |
|----------------|---------------|
| < 0.85 | Ahead of target (>15% faster) — verify milestone completion criteria |
| 0.85–1.15 | On target |
| > 1.15 | Behind target (>15% slower) — flag as TtV at risk |

### Projected TtV

```
Projected TtV = M4 day target × pace multiplier
```

Requires at least M1 completion. A projection with zero completed milestones
is a target estimate, not a pace-based projection — label it accordingly.

### TtV framing rule

TtV figures are **internal planning targets only**. They are never included in
customer-facing documents or communications. Every TtV output carries the tag
`[review — internal planning target]`.

---

## 6. Source Attribution Taxonomy

When skills report data sources in the Reviewer note, use these labels:

| Label | Meaning |
|-------|---------|
| `[CRM ✓ live]` | Retrieved from CRM connector this session |
| `[CS Platform ✓ live]` | Retrieved from CS Platform connector this session |
| `[PM ✓ live]` | Retrieved from project management tool connector |
| `[user provided]` | Supplied by the user in this conversation |
| `[config]` | Derived from plugin CLAUDE.md or company-profile.md |
| `[inferred]` | Calculated or derived from other available data |
| `[stale — N days]` | Data is older than the 14-day staleness threshold |
| `[unknown]` | Source cannot be determined |

Data that is `[inferred]` or `[unknown]` must be flagged in the Reviewer note
and assigned `[Low Confidence]` or lower.

---

## 7. Shared Guardrails

These seven guardrails apply across all skills in all plugins. They cannot
be overridden by plugin configuration or user instruction.

### G1 — Health scores are heuristics

Health scores represent threshold crossings against a configured model.
They are not churn predictions. Skills never assert that an account "will churn"
or "is likely to churn." Language: "the health classification is [tier] based on
[evidence]."

### G2 — Expansion qualification required

Expansion ARR is not counted as qualified pipeline until: (a) an economic buyer
qualifying conversation has occurred AND (b) the opportunity is in formal pipeline
(CPQ quote or CRM opportunity stage). Prior to that, tag expansion as
`[early signal — not yet qualified]` and never include it in GRR.

### G3 — Revenue commitment language

Any GRR/NRR projection, renewal scenario total, or ARR forecast is a **working
forecast**, not a revenue commitment. Every output containing forecast figures
carries: `[review — could be read as a revenue commitment]` and a Reviewer note
directing Finance/RevOps validation before distribution.

### G4 — No triage without escalation path

When a skill identifies a Red or at-risk account, it names the escalation route
(person, channel, SLA) from the configured escalation matrix. A risk flag without
an escalation path does not unblock the account.

### G5 — Confidentiality

Account-level data (ARR, health scores, pipeline stages, renewal status) is
confidential. Skills include a destination check before any output that contains
this data — e.g., "Before sharing: verify recipient has access to account-level
financial data."

### G6 — TARO plays are leads

TARO play recommendations are starting points, not prescriptions. The CSM
determines whether the recommended play fits the specific account context.
Skills surface the play with its trigger rationale; the CSM makes the judgment call.

### G7 — No silent data freshness

Skills never present stale data without labeling it. If any data source is older
than the configured staleness threshold (default: 14 days), it is flagged in the
Reviewer note with the data-as-of date and the staleness indicator.
