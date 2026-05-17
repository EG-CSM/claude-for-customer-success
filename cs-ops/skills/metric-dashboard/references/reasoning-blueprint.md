---
title: "Reasoning Blueprint: CS Metrics Dashboard"
type: reasoning-blueprint
skill: metric-dashboard
version: 1.0.0
---

# Reasoning Blueprint: CS Metrics Dashboard

Load this blueprint when Tier 3 reasoning is activated for CS metrics
dashboard generation. It provides the domain-specific taxonomy, heuristics,
and expert judgment patterns that shape expert-level dashboard construction
and metrics reporting.

---

## Problem Classification Taxonomy

### Type A: Operational Triage (Weekly)
**Characteristics**: Time-sensitive, action-oriented — health movements, at-risk renewals, CSM capacity flags. Audience is the CS team in a working session.
**Primary Risk**: Presenting stale health scores as current movements — a tier change may reflect a delayed score update, not a real relationship shift.
**Expert Focus**: Validate health score freshness before computing WoW deltas; prioritize Red accounts renewing within 30 days over all other signals.

### Type B: Leadership Performance Summary (Monthly)
**Characteristics**: Retention metrics, program execution, and narrative for VP CS / CRO. Requires period-over-period comparison and target variance.
**Primary Risk**: Misaligned retention period definitions — GRR/NRR calculated on a different period basis than finance uses, producing numbers that won't reconcile.
**Expert Focus**: Confirm period start/end and ARR baseline match the finance definition before computing retention metrics.

### Type C: Strategic Scorecard (Quarterly / Board)
**Characteristics**: High-stakes audience, lagging indicators, cohort analysis, capacity assessment. Board mode is a strict subset — 5 metrics and a 3-sentence narrative.
**Primary Risk**: Presenting lagging metrics without leading indicators — the board sees last quarter's results but not what predicts next quarter.
**Expert Focus**: Pair every lagging metric with its leading indicator counterpart; validate cohort churn-vs-health correlation to test health model predictive validity.

### Type D: CSM Performance Review
**Characteristics**: Individual CSM metrics for calibration reviews and 1:1s. Sensitive data requiring management context before distribution.
**Primary Risk**: Attributing portfolio outcomes to individual performance without controlling for portfolio composition, segment mix, and tenure.
**Expert Focus**: Surface portfolio composition context alongside every performance metric; flag bottom-quartile CSMs with inherited-risk portfolios before any performance narrative.

---

## Domain Heuristics

1. **The Freshness-Before-Delta Rule**: Never compute week-over-week or month-over-month health movements without first confirming health scores were updated within the configured freshness threshold. Stale scores produce phantom movements.

2. **The Finance Reconciliation Rule**: Any retention metric (GRR, NRR, logo retention) shared beyond the CS team must use the finance-agreed period definition and ARR baseline. If unconfigured, flag before generating — never default silently.

3. **The 90-Day Lookback Rule**: Churn predictive validity is tested by checking health tier at 90 days pre-renewal against actual outcomes. If Red-tier churn rate is not materially higher than Green-tier churn rate, the health model needs recalibration — say so.

4. **The Portfolio Composition Rule**: CSM performance metrics are meaningless without portfolio context. A CSM with 60% inherited Red accounts will show lower GRR than one with a stable book regardless of effort. Always surface composition before performance narrative.

5. **The Audience Escalation Rule**: Board-level output gets 5 metrics and 3 sentences — no operational detail. Monthly gets full program execution. Weekly gets action items. Never send operational detail upward or strategic summary downward.

6. **The Expansion Attribution Rule**: "CS-sourced expansion" has no universal definition. If the configured definition is missing, flag the gap rather than defaulting — misattributed expansion ARR creates cross-functional conflict.

7. **The Leading-Lagging Pair Rule**: Every lagging metric (GRR, NRR, churn rate) should be paired with its leading indicator (health distribution, at-risk pipeline, Red accounts without active plays) when the audience can act on both.

---

## Common Failure Modes by Dashboard Type

### Operational Triage Failures
- **Phantom health movements**: WoW changes driven by score update timing, not relationship changes.
  → Fix: Check health score timestamp; suppress movements where score age exceeds freshness threshold.
- **Missing renewal urgency sort**: Renewal pipeline not sorted by risk (Red + soonest first).
  → Fix: Always sort by health tier descending then renewal date ascending.

### Leadership Summary Failures
- **Period mismatch with finance**: GRR/NRR calculated on calendar month while finance uses fiscal quarter.
  → Fix: State period definition explicitly; add "confirm with Finance before external use."
- **Narrative without specificity**: Generic observations ("retention was strong") instead of named segments, amounts, and drivers.
  → Fix: Every narrative sentence must include at least one named segment or specific dollar amount.

### Strategic Scorecard Failures
- **Board deck with operational detail**: Including CSM-level data or weekly triage items in board output.
  → Fix: Board mode has exactly 5 metrics and 3 sentences — enforce the constraint.
- **Cohort analysis without predictive check**: Presenting churn cohort data without testing whether health tier predicted the outcome.
  → Fix: Always include the health-at-90-days vs. churn-rate correlation and comment on model validity.

### CSM Performance Failures
- **Ranking without composition context**: Presenting bottom-quartile CSMs without portfolio composition, segment mix, and tenure data.
  → Fix: Every performance flag must include the composition context check before any performance narrative.
- **Distributing without management review**: Sending individual performance data directly to CSMs without CS lead context.
  → Fix: Always include the management-review gate language; tag output as management-only.

---

## Expert Judgment Patterns

### Audience Calibration Decisions
- Match dashboard depth to audience: CS team gets actions, VP gets metrics + narrative, board gets 5 numbers and 3 sentences.
- When mode is ambiguous, default to the most recently used cadence if configured; otherwise ask — never guess the audience.

### Data Sufficiency Decisions
- Minimum viable dashboard requires health distribution + ARR by tier. All other sections degrade gracefully.
- When a data source is unavailable, show "Data not available — [what's needed]" rather than omitting the section silently.
- If retention metrics lack finance-agreed definitions, produce the dashboard with a prominent methodology flag rather than withholding.

### Sensitivity Decisions
- CSM performance data routes through CS lead before any CSM sees it — no exceptions.
- Portfolio-level ARR and retention data requires confidentiality check before leaving the CS org.
- Expansion ARR attribution disputes are flagged, not resolved — the dashboard surfaces the number with the configured definition, not a judgment call.

---

*Reasoning Blueprint: CS Metrics Dashboard v1.0*
*For use with metric-dashboard when Tier 3 reasoning is activated*
