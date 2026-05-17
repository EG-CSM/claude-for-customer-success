---
name: deal-to-outcome-tracing
version: 1.0.0
description: "Links every closed/won opportunity to its downstream CS trajectory using the OCV Outcome Catalog. At deal close: checks catalog completeness (OCV entry, trigger match, measurement source). At 30/60/90/180-day checkpoints: assesses L0–L3 rubric level per OCV entry. When OCV catalog is absent: falls back to structural risk signals with [Confidence: Low]. Triggers: 'outcome tracing', 'what did we promise [account]', 'deal-to-outcome', 'track outcomes for [account]', 'which rubric level is [account] at'."
---

# Deal-to-Outcome Tracing

The longitudinal link between what Sales sold and what CS delivers.
Replaces free-form deal notes with structured OCV catalog references.

**Reference:** OCV catalog conventions → `reference/revops-domain-model.md §6`
**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `ocv_catalog_path`, `ocv_catalog_version`, `cs_platform_connected`

---

## Reasoning Protocol

1. Confirm activation — user asking about outcomes for a specific account, or running a cohort trace
2. Check OCV catalog path — if absent, declare and switch to structural fallback mode
3. Check CS platform connector for health score and usage data
4. Apply G8 — Draft OCV entries must be labeled; only Ratified entries used
5. Apply G6 — data-as-of on all CS platform and CRM reads
6. Apply G5 — rubric level assessment is analytical input; CS owns the response

---

## At Deal Close — Catalog Completeness Check

Three conditions required before CS onboarding proceeds:

```
Check 1: OCV entry referenced
  → At least one OCV entry with status = Ratified linked to the deal in HubSpot
  → If absent: trigger handoff quality flag (see sales-cs-handoff-quality-scoring)

Check 2: Trigger condition match
  → The OCV trigger condition is present in the account's actual situation
  → If mismatch: flag as "Sold to wrong problem" — surface to CS and Sales manager

Check 3: Measurement source accessible
  → The measurement source in the OCV entry is accessible post-close
  → If inaccessible: flag what CS needs to establish before first checkpoint
```

**Structural fallback (when OCV absent):**
```
Run Tier 1 structural risk assessment only:
  - Discount level vs. practice profile threshold
  - Sales cycle vs. segment average
  - Stakeholder thread count
Label all outputs: [Outcome data: OCV reference absent — structural signals only —
Confidence: Low]
```

---

## At Checkpoint — Rubric Level Assessment

At 30/60/90/180-day marks (per OCV verification_milestone):

```
For each OCV entry on the deal:
  Read observable evidence from:
    - CS platform health score and trend [CS Platform ✓ live] or [Stale]
    - Product usage trend [CS Platform ✓ live] or [Unavailable]
    - CS-documented outcome progress notes [CS Platform ✓ live] or [Unavailable]
    - CRM activity (EBR/QBR logged) [CRM ✓ live]

  Map to rubric level:
    L0 — leading indicators absent per OCV rubric definition
    L1 — leading indicators present; primary metric not yet reached
    L2 — primary metric verified at the OCV measurement source
    L3 — primary metric + secondary impact verified
```

---

## Output Formats

**Single account:**
```
DEAL-TO-OUTCOME TRACE — [Account Name]
[CRM ✓ live — as of YYYY-MM-DD] [CS Platform ✓ live / Unavailable]
[Confidence: High/Moderate/Low]

Deal context:
  Closed: [date]  ACV: $XXXk  Segment: [segment]  Rep: [name]

OCV entries referenced:
  OCV-001  [Name]  Status: Ratified  ✓ Trigger match  ✓ Source accessible

Current rubric level (as of [checkpoint]):
  OCV-001: L[N] — [Label]
  Evidence: [Specific observable signals mapped to rubric level]
  Next checkpoint: [date]  Next milestone: [OCV-defined]

Catalog completeness: [PASS / FLAGS]
  [Any flags from the three completeness checks]

[G5: Rubric level is analytical input. CS owns the response plan.]
[G8: Draft entries not used in this assessment]
```

**Cohort view:**
```
DEAL-TO-OUTCOME COHORT — [Segment/Period]
OCV-001 attainment across [N] accounts:
  L3: [N] (XX%)
  L2: [N] (XX%)
  L1: [N] (XX%)
  L0: [N] (XX%) — [Flag if >40% at L0 past 90-day checkpoint]

L0 pattern signal: [Account attributes common to L0 accounts]
```

---

## Guardrails

- G5: Rubric level assessment never presented as a directive
- G6: All connector reads timestamped
- G8: Draft OCV entries excluded; labeled if referenced
