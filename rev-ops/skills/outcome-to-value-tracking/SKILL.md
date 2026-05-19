---
name: outcome-to-value-tracking
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Maps each customer to their L0–L3 rubric level on their referenced OCV entries at OCV-defined verification milestones (e.g., 90-day, 180-day). Portfolio view: % at each rubric level per OCV entry. Surfaces systemic L0 persistence (>40% of accounts stuck at L0 past 90-day milestone) as a delivery pattern signal. Triggers: 'outcome tracking', 'rubric level', 'L0 L1 L2 L3', 'value realization', 'are customers achieving outcomes', 'outcome portfolio health'."
---

[PROPOSED]

# Outcome-to-Value Tracking

Are customers achieving what they bought the product to do?
L0–L3 rubric level tracking per account and per OCV entry.

**Reference:** OCV catalog conventions → `../../../shared/revops-domain-model.md §6`
**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `ocv_catalog_path`, `cs_platform_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `ocv_catalog_path`, `cs_platform_connected`

---

## Use when
- Delivered customer outcomes need to be mapped to realized business value for reporting
- CS value realization tracking requires outcome-to-value linkage for a cohort or account
- QBR or EBR preparation needs structured outcome value evidence

## Do NOT use for
- Rubric level assessment at checkpoints (use deal-to-outcome-tracing)
- OCV catalog entry building
- Revenue forecast or ARR reporting

## Typical Activation
"Outcome to value tracking", "value realization report", "what value has [account] realized", "track outcomes to business value", "value evidence for [account]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of outcome tracking request is this?
   - Single-account rubric assessment (one account — L0–L3 mapping across all relevant OCV entries)
   - Cohort value realization report (set of accounts — rubric levels at a specific milestone)
   - Portfolio health sweep (all accounts — % distribution per OCV entry, L0 pattern detection)
   - QBR/EBR prep (structured outcome value evidence for a specific account and meeting)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about outcome attainment, value realization, or rubric levels
   2. Pull OCV catalog from configured path; declare fallback if absent or unavailable
   3. Pull CS platform data for health scores, usage trend, and outcome progress notes; declare connector status and data-as-of timestamp per G6
   4. Apply G8 — only Ratified OCV entries are used for assessment; Draft entries are excluded
   5. Apply G5 — rubric level assessment is an analytical input; CS owns the response plan
   6. Apply G6 — data-as-of timestamp required on all CS platform and CRM connector reads
   7. Confirm output destination before delivering — internal CS vs. QBR deck vs. leadership portfolio view

3. **EXPERT CHECK**: What would a veteran CS value realization analyst verify before surfacing findings?
   - Is rubric level determined from OCV evidence criteria, not inference? The rubric level must map
     to observable evidence defined in the OCV entry — not the analyst's judgment of how the account
     is "doing." If the OCV entry is absent or Draft, the assessment cannot proceed per G8.
   - Is the L0 pattern threshold applied correctly? The 40% threshold applies at the portfolio level
     at the 90-day milestone, not to individual accounts — surfacing a single L0 account as a "pattern"
     is a false positive that misdirects CS leadership attention.
   - Is the data source declared when product analytics are needed but unavailable? Analysis uses
     CS health scores and outcome progress notes; feature-level product analytics require a product
     analytics connector. Surfacing a rubric level as High confidence when product data was unavailable
     is a G6 violation — declare the gap explicitly.
   - Is the escalation path named before surfacing systemic L0 patterns? A delivery pattern signal
     (>40% L0 past 90-day) routes to CS + Product, not back to individual CSMs.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Mapping rubric level from inference rather than OCV-defined observable evidence
   - Using Draft OCV entries for assessment (G8 violation)
   - Pulling CS platform or CRM data without data-as-of timestamp (G6 violation)
   - Surfacing portfolio L0 pattern without naming the escalation path (CS + Product)
   - Presenting rubric level as a final verdict rather than an analytical input (G5 violation)

**After execution**, verify:
- G8 compliance — only Ratified OCV entries assessed; any Draft entries declared and excluded
- G5 qualifier present — rubric level named as analytical input; CS named as response owner
- G6 data-as-of label applied to all CS platform and CRM connector reads
- L0 pattern threshold applied at portfolio level at 90-day milestone, not per-account
- Confidence: High when CS platform connected and OCV catalog current; Moderate when connector unavailable or outcome progress sourced from rep notes only
- Confidence: [High] when CS platform connected and OCV catalog current / [Medium] when connector unavailable or data estimated / [Low] if all inputs are manual or unverified

---

## Rubric Level Assessment

For each account, at each OCV-defined verification milestone:

```
Read from OCV entry:
  - Observable evidence for L0, L1, L2, L3
  - business_metric and measurement_source
  - verification_milestone schedule

Read from connectors:
  - CS health score and trend [CS Platform ✓ live]
  - Product usage trend [CS Platform ✓ live]
  - CS-documented outcome progress notes [CS Platform ✓ live]
  - CRM: EBR/QBR logged, executive sponsor activity [CRM ✓ live]

Map to rubric level using OCV evidence criteria — not inference.
```

**Portfolio analysis scope boundary:**
Analysis uses CS health scores, product usage summaries, and CS-documented
outcome progress. Feature-level product analytics are out of scope unless a
product analytics connector is configured. When deeper investigation is warranted:
"Root cause may require product usage analytics. Recommend CS + Product review."

---

## Output

**Account-level:**
```
OUTCOME TRACKING — [Account Name]
[CS Platform ✓ live — as of YYYY-MM-DD] [CRM ✓ live]
[OCV catalog v[version] — Confidence: High/Moderate]

OCV-001 [Name]:
  Current rubric level: L[N] — [Label]
  Evidence: [Specific observable signals from OCV rubric — not generic]
  Milestone: [which checkpoint] | Next: [date]
  Recommended action: [if L0 or L1 and approaching next milestone]
  [G5: CS [name] owns the response plan]

[G8: Only Ratified entries assessed]
```

**Portfolio-level:**
```
OUTCOME PORTFOLIO HEALTH — [Period]
[CS Platform ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

OCV-001 [Name] — [N] accounts:
  L3: N (XX%)  L2: N (XX%)  L1: N (XX%)  L0: N (XX%)
  [⚠ L0 PATTERN if >40% at L0 past 90-day checkpoint]
    Common attributes: [segment / product tier / onboarding path]
    Signal: Delivery pattern — not account-specific. Escalate to CS + Product.

OCV-002 [Name] — [N] accounts: [same format]

Portfolio summary:
  Overall L2+ attainment: XX%
  Accounts at L0 past 90-day checkpoint: [N] — [HIGH/MODERATE concern]
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
**Data sensitivity:** Inputs may contain confidential deal, customer, and revenue data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G5: Rubric level assessments are analytical inputs — CS owns the response
- G8: Draft OCV entries excluded from assessment
- G6: All connector reads timestamped
- Portfolio analysis scope boundary: declare when product analytics would improve depth
