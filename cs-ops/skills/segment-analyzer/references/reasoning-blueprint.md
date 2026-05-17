---
title: "Reasoning Blueprint: Segment Analysis"
type: reasoning-blueprint
skill: segment-analyzer
version: 1.0.0
---

# Reasoning Blueprint: Segment Analysis

Load this blueprint when Tier 3 reasoning is activated for segment analysis work.
It provides the domain-specific taxonomy, heuristics, and expert judgment patterns
that shape expert-level CS book-of-business segment analysis.

---

## Problem Classification Taxonomy

### Type A: Full Portfolio Segmentation Review
**Characteristics**: Leadership or planning-driven request covering all segments — ARR distribution, health distribution, coverage ratios, and motion fit across the entire book.
**Primary Risk**: Drowning in data without surfacing the cross-segment insight that actually matters (e.g., ARR concentration risk masked by account count balance).
**Expert Focus**: Cross-segment comparison — where is the structural imbalance that won't fix itself?

### Type B: Single-Segment Deep Dive
**Characteristics**: Focused on one segment — health, coverage, renewal pressure, and motion fit within that tier only.
**Primary Risk**: Analyzing the segment in isolation without benchmarking against portfolio norms — a 30% Red rate looks alarming until you see the portfolio average is 28%.
**Expert Focus**: Is this segment's performance a segment-specific problem or a portfolio-wide pattern showing up here first?

### Type C: Reclassification Queue
**Characteristics**: Accounts that have crossed ARR thresholds and need segment reassignment — triggers motion changes and CSM reassignment.
**Primary Risk**: Treating reclassification as a mechanical ARR-threshold exercise without accounting for relationship disruption, especially on downward moves.
**Expert Focus**: Separate upward (opportunity) from downward (risk) reclassifications — they require different handling and stakeholder communication.

### Type D: At-Risk Triage
**Characteristics**: Filtered view of Red and Yellow accounts by segment — feeds weekly triage, escalation prioritization, or headcount justification.
**Primary Risk**: Listing at-risk accounts without ARR-weighting — a segment with 5 Red SMB accounts looks worse than one with 1 Red Enterprise account worth 10x the ARR.
**Expert Focus**: ARR-at-risk concentration — where is the biggest dollar exposure, not the biggest account count?

---

## Domain Heuristics

1. **The 80/20 ARR Rule**: In most portfolios, one segment holds 60-80% of total ARR but only 20-40% of accounts. Start every analysis by confirming where ARR concentrates — that segment's health drives portfolio health.

2. **The Coverage Ratio Lie**: A CSM carrying 25 accounts at target ratio of 25 looks fine — until you check ARR variance. If 3 of those accounts represent 60% of their book's ARR, the ratio is misleading. Always cross-reference ratio with ARR concentration per CSM.

3. **The Motion Mismatch Signal**: When a segment's Red percentage exceeds the portfolio average by >10 points AND CSM ratios are at or above target, the motion is likely wrong — not the CSMs. Coverage quantity is adequate but coverage quality (touch model) is insufficient.

4. **The Reclassification Lag Rule**: Accounts that crossed an ARR threshold >90 days ago without reclassification are accumulating motion debt — they're receiving the wrong engagement model. Flag elapsed time, not just threshold crossing.

5. **The Renewal Cluster Test**: If >30% of a segment's ARR renews within the same 90-day window, that's a concentration risk regardless of health scores. One bad quarter in that window compounds across the segment.

6. **The Unclassified Account Tax**: Unclassified accounts always receive the wrong motion (usually none). If unclassified accounts exceed 5% of the book, the segment model has a coverage gap that silently generates churn.

---

## Common Failure Modes by Analysis Type

### Full Portfolio Failures
- **Summary without insight**: Producing segment tables without cross-segment interpretation — the tables are data, the interpretation is the analysis.
  -> Fix: After every summary table, write a 2-3 sentence interpretation naming the most significant finding and its operational implication.
- **Account-count bias**: Comparing segments by account count instead of ARR weight — misleads resource allocation.
  -> Fix: Always present both account count AND ARR percentage side by side; lead with ARR in recommendations.

### Single-Segment Failures
- **Isolation analysis**: Analyzing segment health without benchmarking against portfolio averages — every metric needs a comparison point.
  -> Fix: Include portfolio average as a comparison column in every per-segment metric table.
- **CSM ratio without ARR context**: Reporting accounts-per-CSM without showing ARR-per-CSM — hides workload imbalance.
  -> Fix: Always pair account ratio with ARR ratio in coverage analysis.

### Reclassification Failures
- **Mechanical threshold application**: Moving accounts purely on ARR without flagging relationship risk on downward moves.
  -> Fix: Tag every downward reclassification with a relationship risk note and require CS lead confirmation.
- **Missing elapsed time**: Flagging threshold crossings without noting how long ago — recent crossings are routine, stale ones indicate process failure.
  -> Fix: Include "days since threshold crossed" column in reclassification queue.

### At-Risk Triage Failures
- **Equal-weight listing**: Listing all Red/Yellow accounts without ARR ranking — wastes triage time on low-ARR accounts first.
  -> Fix: Sort by ARR descending; lead the triage with highest-dollar exposure.
- **Missing active play status**: Listing at-risk accounts without noting whether a save play or intervention is already active.
  -> Fix: Include "Active play?" column — an at-risk account with an active intervention is a different priority than one with none.

---

## Expert Judgment Patterns

### Scope Decisions
- Full portfolio analysis when the question is strategic (planning, headcount, board prep); single-segment when operational (CSM coaching, motion tuning).
- Default to `--full` when the requester is CS leadership; default to `--segment` when the requester is a segment lead or individual CSM.

### Depth Decisions
- If segment count is 3 or fewer, always include per-segment deep view — the overhead is low and the cross-segment comparison is the whole point.
- If segment count exceeds 5, produce summary + flag the 1-2 segments with the most concerning metrics for deep view — full deep view on 5+ segments overwhelms.

### Prioritization Decisions
- At-risk triage always ranks by ARR, not by health score severity — a Yellow $500K account outranks a Red $20K account in triage priority.
- Reclassification urgency ranks by elapsed time since threshold crossing, not by ARR delta — an account $1K over threshold for 6 months is more urgent than one $50K over for 1 week.

### Confidence Decisions
- If segment definitions come from configured profile: high confidence on classification accuracy.
- If segment definitions are inferred from data patterns: medium confidence — flag that reclassification thresholds may not match organizational intent.
- If CSM assignment data is incomplete (>10% unassigned): low confidence on all coverage ratio calculations — state the gap prominently.

---

*Reasoning Blueprint: Segment Analysis v1.0*
*For use with segment-analyzer when Tier 3 reasoning is activated*
