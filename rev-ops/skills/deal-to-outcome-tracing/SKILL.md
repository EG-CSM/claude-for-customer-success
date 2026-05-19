---
name: deal-to-outcome-tracing
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Links every closed/won opportunity to its downstream CS trajectory using the OCV Outcome Catalog. At deal close: checks catalog completeness (OCV entry, trigger match, measurement source). At 30/60/90/180-day checkpoints: assesses L0–L3 rubric level per OCV entry. When OCV catalog is absent: falls back to structural risk signals with [Confidence: Low]. Triggers: 'outcome tracing', 'what did we promise [account]', 'deal-to-outcome', 'track outcomes for [account]', 'which rubric level is [account] at'."
---

[PROPOSED]

# Deal-to-Outcome Tracing

The longitudinal link between what Sales sold and what CS delivers.
Replaces free-form deal notes with structured OCV catalog references.

**Reference:** OCV catalog conventions → `../../../shared/revops-domain-model.md §6`
**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `ocv_catalog_path`, `ocv_catalog_version`, `cs_platform_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `ocv_catalog_path`, `ocv_catalog_version`, `cs_platform_connected`

---

## Use when
- Closed/won deal needs longitudinal tracing from sale to CS outcome delivery
- OCV catalog completeness needs verification at deal close
- 30/60/90/180-day rubric level assessment required for a specific account or cohort
- User asks what was promised to an account and how delivery is tracking

## Do NOT use for
- Pre-close deal structure review (use revenue-leakage-scanning)
- Churn signal detection without outcome context (use early-churn-downgrade-signal-detection)
- OCV catalog entry creation
- Portfolio-level value realization mapping and outcome-to-value linkage (use outcome-to-value-tracking)

## Typical Activation
"Outcome tracing for [account]", "what did we promise [account]", "deal-to-outcome", "track outcomes", "which rubric level is [account] at", "30-day checkpoint for [account]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of deal-to-outcome request is this?
   - Single account trace (one deal, full OCV catalog completeness + rubric assessment)
   - Checkpoint assessment (30/60/90/180-day rubric level for one account or cohort)
   - Cohort view (segment or period — aggregate rubric distribution + L0 pattern signal)
   - Catalog completeness check (at deal close — OCV entry, trigger match, source accessible)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about outcomes for a specific account, or running a cohort trace
   2. Check OCV catalog path — if absent, declare and switch to structural fallback mode
   3. Check CS platform connector for health score and usage data
   4. Apply G8 — Draft OCV entries must be labeled; only Ratified entries used
   5. Apply G6 — data-as-of on all CS platform and CRM reads
   6. Apply G5 — rubric level assessment is analytical input; CS owns the response

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Is the OCV catalog status confirmed before using any entry? Draft entries produce
     misleading rubric assessments — only Ratified entries carry measurement authority.
   - Is the checkpoint date aligned to the OCV verification_milestone, not a calendar default?
     30/60/90/180-day marks mean nothing without the OCV milestone anchor.
   - Is the structural fallback clearly labeled when OCV is absent? Presenting structural
     signals as outcome signals is a confidence misrepresentation — G8 violation.
   - Is the trigger condition match verified against the account's actual situation?
     A mismatch between what was sold and what the account has is a "Sold to wrong problem"
     flag — surfaces to CS and Sales manager, not buried in the output.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Using Draft OCV entries in rubric assessment (G8 violation — only Ratified entries)
   - Surfacing connector reads without data-as-of timestamp (G6 violation)
   - Presenting rubric level as a directive rather than analytical input (G5 violation)
   - Omitting catalog completeness flags when OCV reference is absent or mismatched

**After execution**, verify:
- G5 qualifier present: rubric level is analytical input; CS owns the response plan
- G6 data-as-of label applied to all CS platform and CRM reads
- G8 confirmation: Draft OCV entries excluded; labeled if referenced
- Confidence: High when OCV catalog is current and CS platform is connected; Moderate when
  either is unavailable; Low when OCV catalog is absent (structural fallback mode)
    - Confidence: [High] when OCV catalog is current and CS platform is connected / [Medium] when either is unavailable / [Low] when OCV catalog is absent (structural fallback mode)

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
  - Discount level vs. company profile threshold
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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential customer, deal, and operational data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G5: Rubric level assessment never presented as a directive
- G6: All connector reads timestamped
- G8: Draft OCV entries excluded; labeled if referenced
