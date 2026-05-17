---
title: "Reasoning Blueprint: CRM Data Quality Audit"
type: reasoning-blueprint
skill: data-quality-check
version: 1.0.0
---

# Reasoning Blueprint: CRM Data Quality Audit

Load this blueprint when Tier 3 reasoning is activated for data quality work.
It provides the domain-specific taxonomy, heuristics, and expert judgment
patterns that shape expert-level CRM and CS platform data quality auditing.

---

## Problem Classification Taxonomy

### Type A: Pre-Reporting Hygiene Check
**Characteristics**: Audit triggered before a reporting cycle, dashboard build, or capacity plan — the goal is to validate that downstream analytics will be trustworthy.
**Primary Risk**: Incomplete field coverage masking ARR concentration — a few high-value accounts with missing data silently skew every report.
**Expert Focus**: Check ARR-weighted completeness, not just record counts. 5% of accounts missing data could be 40% of ARR.

### Type B: Post-Transition Data Validation
**Characteristics**: Triggered after CSM reassignment, territory rebalance, or CRM migration. Data gaps are expected; the question is scope and severity.
**Primary Risk**: Orphaned records — accounts that lost their CSM owner during transition and now sit outside every workflow.
**Expert Focus**: Cross-reference the transition date against last-updated timestamps to distinguish pre-existing gaps from transition-caused gaps.

### Type C: Analytics Distrust Investigation
**Characteristics**: A dashboard number looks wrong, a report contradicts intuition, or a metric moved unexpectedly. The audit is forensic — find what broke.
**Primary Risk**: Fixing the symptom (one bad record) instead of the root cause (a sync failure, a workflow gap, or a field definition mismatch).
**Expert Focus**: Trace the suspicious metric back to its component fields and identify whether the issue is completeness, staleness, or consistency.

### Type D: Recurring / Scheduled Audit
**Characteristics**: Periodic data quality check (monthly, quarterly). No specific trigger event — the goal is trend tracking and regression detection.
**Primary Risk**: Audit fatigue — producing the same report with the same findings and no remediation progress.
**Expert Focus**: Compare against prior audit results. Highlight what improved, what regressed, and which remediation items remain unassigned.

---

## Domain Heuristics

1. **The ARR-Weighted Rule**: Never report data quality by record count alone. 10 accounts missing health scores could be $50K or $5M — the remediation priority is completely different. Always weight by ARR.

2. **The Orphan Gravity Rule**: Unowned, unsegmented accounts accumulate silently. If orphaned records exceed 3% of total ARR, the capacity planner and segment analyzer are producing fictional outputs.

3. **The Staleness Cascade Rule**: A stale health score doesn't just affect health reporting — it cascades into at-risk identification, renewal forecasting, and capacity planning. Flag staleness impact by downstream dependency count, not just days since update.

4. **The Consistency Triage Rule**: Not all consistency violations are errors. Segment-ARR mismatches above 15% of accounts usually indicate a systemic definition problem (segment thresholds changed, not updated in CRM). Below 5%, they're usually legitimate overrides. Between 5-15%, investigate before concluding.

5. **The Migration Residue Rule**: After any CRM migration, expect 10-20% of records to have at least one data quality issue in the first 90 days. If the rate is higher, the migration validation was insufficient. If the rate persists past 90 days, the ongoing data entry workflow has a gap.

6. **The Invisible Account Rule**: An account missing 4+ required fields is effectively invisible to CS operations — it cannot appear in any meaningful analysis. These accounts must be triaged (assign, archive, or investigate) before any other remediation.

---

## Common Failure Modes by Audit Type

### Pre-Reporting Hygiene Failures
- **Count-based false confidence**: Reporting "95% complete" when the missing 5% holds 30% of ARR.
  → Fix: Always compute ARR-weighted completeness alongside record-count completeness.
- **Threshold invention**: Applying staleness thresholds that aren't configured, producing arbitrary flags.
  → Fix: State the configured threshold source explicitly. If none exists, flag the gap — don't default silently.

### Post-Transition Validation Failures
- **Attribution confusion**: Blaming the transition for pre-existing data gaps.
  → Fix: Compare last-updated timestamps against transition date to separate old from new issues.
- **Mass assignment without investigation**: Auto-assigning orphaned records to new CSMs without checking if accounts are active.
  → Fix: Require disposition (assign/archive/investigate) per orphan, not bulk assignment.

### Analytics Investigation Failures
- **Symptom patching**: Correcting the one bad record that caused a dashboard anomaly without checking for systemic cause.
  → Fix: When a single record is wrong, query the same field across all records for the same failure pattern.
- **Silent scope narrowing**: Running only the mode that matches the symptom (e.g., --completeness) when the root cause is a consistency issue.
  → Fix: Start with --full for investigations; narrow after root cause is identified.

### Recurring Audit Failures
- **Groundhog Day reports**: Producing the same findings with no progress tracking.
  → Fix: Include a "vs. prior audit" comparison showing remediation progress on previously flagged items.

---

## Expert Judgment Patterns

### Scope Decisions
- If the request mentions a specific dashboard or report, run --full first but lead the output with the fields that feed that specific report.
- If time-constrained, --completeness is the highest-value single mode — missing data is more damaging than stale or inconsistent data.

### Severity Decisions
- ARR concentration determines severity, not account count. A single enterprise account missing renewal date is higher priority than 20 SMB accounts missing segment.
- Orphaned records above 3% of ARR are always P1 regardless of count.

### Remediation Decisions
- Quick fixes (bulk CRM updates) should be separated from integration fixes (sync failures) — they have different owners and timelines.
- Never recommend remediation without naming an owner role. Unowned remediation items are documentation, not action.

### Confidence Decisions
- [High] when auditing live CRM + CS Platform data updated within configured thresholds.
- [Medium] when working from a user-provided export (could be stale or filtered).
- [Low] when working from conversation context only — flag that the audit is indicative, not definitive.

---

*Reasoning Blueprint: CRM Data Quality Audit v1.0*
*For use with data-quality-check when Tier 3 reasoning is activated*
