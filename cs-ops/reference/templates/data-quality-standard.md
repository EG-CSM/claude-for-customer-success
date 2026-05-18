# CS Data Quality Standard

**CS Data Quality Standard**
*[Version] · [Date] · INTERNAL — CS-Ops and RevOps use*

---

## Purpose

This standard defines the minimum data quality requirements for the CS book of record.
It governs field completeness, staleness thresholds, consistency rules, and ownership
for all fields used in health scoring, capacity planning, and renewal forecasting.

---

## Required fields

| Field | Required completeness | Owner | Notes |
|-------|----------------------|-------|-------|
| Account name | 100% | CRM Admin | Must match contract entity name |
| ARR | 100% | RevOps | Contract ARR; not usage-based estimate |
| Segment | 100% | CS Ops | Must match configured segment definitions |
| CSM owner | 100% | CS Lead / CS Ops | Required for coverage ratio calculations |
| Health tier | 95% | CS Platform | Auto-assigned where model is active |
| Renewal date | 100% | RevOps | Must be within contract term; no estimated dates |
| Lifecycle stage | 90% | CS Platform / CSM | Required for play routing and CTA logic |

**Completeness targets are measured at the portfolio level.** Individual account gaps are
acceptable within the threshold; systemic gaps in a segment or CSM's book trigger a
data quality review.

---

## Staleness thresholds

| Field | Max staleness | Action if exceeded |
|-------|--------------|-------------------|
| Health score | [configured threshold, e.g., 14 days] | Flag account in health model; health score excluded from distribution until refreshed |
| Health components | [configured threshold, e.g., 7 days] | Flag component; component excluded from health calculation or zeroed per model config |
| Last contact date | [configured threshold, e.g., 30 days] | Surface in capacity planner as lapsed; CSM notified |
| Lifecycle stage | [configured threshold, e.g., 30 days] | Flag in segment analyzer; exclude from lifecycle-based reporting |

---

## Consistency rules

| Rule | Fields involved | Violation action |
|------|----------------|-----------------|
| Segment matches ARR range | Segment, ARR | Flag as reclassification candidate; do not auto-reclassify |
| Health tier matches health score | Health tier, Health score | Flag discrepancy; CS Ops resolves against CS platform source of truth |
| Renewal date not in past | Renewal date | Flag as stale; RevOps refreshes from contract system within [configured SLA] |
| Lifecycle stage consistent with renewal proximity | Lifecycle stage, Renewal date | Flag when lifecycle = Onboarding but renewal < 90 days |
| CSM assignment consistent with segment motion | CSM owner, Segment | Flag when account segment requires high-touch motion but CSM is assigned tech-touch only accounts |

---

## Field ownership matrix

| Field | Primary owner | Backup owner | Update frequency |
|-------|--------------|-------------|-----------------|
| ARR | RevOps | CS Ops (escalation) | On contract change; quarterly reconciliation |
| Segment | CS Ops | CS Lead | On reclassification decision; quarterly review |
| CSM owner | CS Lead / CS Ops | N/A | On account transfer or territory change |
| Health tier | CS Platform (auto) | CS Ops (manual override) | Per platform refresh cadence |
| Health components | CS Platform (auto) | CS Ops (data quality) | Per component data source cadence |
| Renewal date | RevOps | CS Ops | Per contract; verified quarterly |
| Lifecycle stage | CS Platform (auto) / CSM | CS Ops | On milestone event; CSM confirms at QBR |
| Last contact date | CS Platform (auto from activity log) | CSM (manual) | Per activity; reviewed monthly |

---

## Standard change process

Changes to this standard — field definitions, completeness targets, staleness thresholds,
consistency rules, or ownership assignments — require:

1. CS Ops proposes change with rationale
2. RevOps reviews fields owned by RevOps
3. CS Lead approves
4. Change logged in version history below
5. Affected skills and health model config updated to reflect new thresholds

**Version history:**

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | [date] | Initial standard | [Author] |
