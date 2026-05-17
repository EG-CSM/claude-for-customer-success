---
title: "Reasoning Blueprint: Health Model Review"
type: reasoning-blueprint
skill: health-model-review
version: 1.0.0
---

# Reasoning Blueprint: Health Model Review

Load this blueprint when Tier 3 reasoning is activated for portfolio health
model auditing. It provides the domain-specific taxonomy, heuristics, and
expert judgment patterns that shape expert-level health model calibration
and predictive accuracy assessment.

---

## Problem Classification Taxonomy

### Type A: Distribution Anomaly
**Characteristics**: Portfolio health tier distribution is skewed — too many accounts in one tier, ARR concentration in Red/Yellow, or sudden tier migration patterns.
**Primary Risk**: Misattributing a threshold calibration problem to an actual portfolio health shift.
**Expert Focus**: Separate real deterioration from model miscalibration by checking whether the shift correlates with churn outcomes or just scoring drift.

### Type B: Predictive Accuracy Failure
**Characteristics**: Health classifications do not correlate with renewal outcomes — Green accounts churn, Red accounts renew. Requires historical data.
**Primary Risk**: Declaring the model "broken" without distinguishing false positives (over-flagging) from false negatives (missing churners) — they have different fixes.
**Expert Focus**: Calculate directional accuracy (Red churn rate minus Green churn rate) before recommending threshold changes.

### Type C: Component/Weight Misconfiguration
**Characteristics**: Individual components are stale, lack data coverage, or carry disproportionate weight relative to their predictive value.
**Primary Risk**: Confusing a data pipeline gap (zero coverage) with a scoring problem (low scores with full coverage) — the corrective actions differ entirely.
**Expert Focus**: Check coverage percentage before interpreting average scores — a component scoring "zero" at 30% coverage is a data problem, not a signal.

### Type D: Threshold Recalibration
**Characteristics**: Explicit request to adjust Green/Yellow/Red boundaries, often triggered by findings from Types A-C.
**Primary Risk**: Recommending threshold changes without modeling the cascade — accounts currently in escalation workflows may change tier, breaking active CTAs.
**Expert Focus**: Quantify how many accounts and how much ARR would migrate between tiers before recommending any change.

### Secondary Dimension: Data Maturity
- **Instrumented**: Live integrations, historical churn data, component-level scores available.
- **Partial**: Some components connected, churn data limited or manual.
- **Manual**: User-provided exports only — no live feeds, limited history.

---

## Domain Heuristics

1. **The 80/20 Distribution Rule**: If more than 80% of accounts are Green, the model is almost certainly too lenient — well-calibrated models typically show 60-70% Green, 20-25% Yellow, 10-15% Red.

2. **The Coverage-Before-Score Rule**: Never interpret a component's average score until you've confirmed >80% data coverage. Below that threshold, the score reflects data gaps, not account health.

3. **The False Negative Priority Rule**: One Green-that-churned is more damaging than three Red-that-renewed. False negatives bypass intervention entirely; false positives waste effort but still get attention.

4. **The 90-Day Lookback Rule**: Predictive validity is measured at 90 days pre-renewal, not at current state. A Red account that was Green 90 days before churn is a model failure.

5. **The Cascade Impact Rule**: Before recommending any threshold change, calculate accounts affected and ARR migrating — threshold changes that move >15% of accounts between tiers need a transition plan.

6. **The Stale Signal Rule**: A health component not updated within its configured freshness window is worse than no component — it creates false confidence. Flag staleness before interpreting scores.

7. **The Single-Component Dominance Rule**: If one component weighted >50% drives >80% of tier classifications, the model is effectively single-signal — recommend weight redistribution or validate that single-signal accuracy justifies the concentration.

---

## Common Failure Modes by Audit Type

### Distribution Anomaly Failures
- **Benchmark without context**: Comparing distribution to industry benchmarks without accounting for the company's segment mix or lifecycle stage.
  → Fix: Normalize by segment before benchmarking — Enterprise and SMB distributions differ structurally.
- **Mistaking seasonality for drift**: Flagging distribution shifts that recur quarterly (e.g., renewal-season Yellow spikes).
  → Fix: Compare to same period prior year, not just prior period.

### Predictive Accuracy Failures
- **Survivorship bias**: Only analyzing accounts that renewed or churned, ignoring accounts still in contract (which could churn later).
  → Fix: Restrict analysis to accounts past their renewal decision point.
- **Missing the denominator**: Reporting "5 Green accounts churned" without stating what percentage of Green that represents.
  → Fix: Always report both count and rate — 5 of 200 Green (2.5%) vs. 5 of 20 Green (25%) are different findings.

### Component/Weight Failures
- **Averaging across segments**: Reporting portfolio-wide component averages that mask segment-level anomalies (e.g., Enterprise usage is strong while SMB usage is collapsing).
  → Fix: Break component analysis by segment when segment count >1.
- **Treating zero-coverage as zero-score**: Interpreting missing data as poor health rather than flagging it as a coverage gap.
  → Fix: Separate "no data" from "bad data" in every component row.

### Threshold Recalibration Failures
- **Changing thresholds without a transition plan**: Recommending new boundaries without accounting for in-flight escalations and CTAs.
  → Fix: List affected accounts and active workflows before any threshold recommendation.
- **Optimizing for one metric**: Adjusting thresholds to reduce false negatives while ignoring the false positive increase (or vice versa).
  → Fix: Report both rates and the tradeoff explicitly.

---

## Expert Judgment Patterns

### Scope Decisions
- If the user asks for "full audit" but has no historical churn data, downgrade calibration to descriptive mode and flag the data gap rather than skipping the section silently.
- If only one mode is requested but findings clearly implicate another (e.g., distribution review reveals component coverage gaps), recommend the additional mode rather than expanding scope unasked.

### Depth Decisions
- Distribution-only mode should complete in one pass — do not add component or calibration analysis unless explicitly requested.
- Full audit with all data available warrants all four sections; full audit with partial data warrants all sections with explicit data-gap callouts per section.

### Confidence Decisions
- Calibration verdicts require 12+ months of churn data and 30+ renewal events to reach [High] confidence. Below those thresholds, state [Medium] or [Low] with the specific gap.
- Distribution findings are [High] confidence when sourced from live integrations; [Medium] from user exports with stated date; [Low] from conversation context alone.

### Recommendation Decisions
- Never recommend more than 3 priority changes — ops teams that receive 7 recommendations execute zero.
- Rank recommendations by ARR impact, not by analytical elegance.
- If no changes are warranted, say so explicitly — "no change needed" is a valid and valuable finding.

---

*Reasoning Blueprint: Health Model Review v1.0*
*For use with health-model-review when Tier 3 reasoning is activated*
