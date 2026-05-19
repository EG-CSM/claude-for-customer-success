---
name: deal-classification
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Independently scores each open opportunity as Commit / Best Case / Pipeline using CRM activity data — without relying on rep self-reporting. Surfaces delta vs. rep's stated forecast category when classification disagrees by more than one tier. Triggers: 'deal classification', 'classify the pipeline', 'commit vs best case', 'independent forecast', 'override rep call'."
---

[PROPOSED]

# Deal Classification

Classifies open opportunities using CRM activity signals, not rep self-reporting.
Disagrees with rep calls only when evidence is clear — flags the delta, doesn't override.

**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `primary_segment`, `avg_sales_cycle_days`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `primary_segment`, `avg_sales_cycle_days`

---

## Use when
- Deal needs to be classified by type (New ARR, Expansion, Renewal, Reactivation) for ARR reporting accuracy and pipeline routing
- ARR classification is disputed or ambiguous for a specific opportunity
- Closed-won deal classification needs verification before CS handoff

## Do NOT use for
- Deal health or risk scoring (use deal-health-scoring)
- Revenue recognition decisions (classification is analytical input only)
- Bulk ARR reporting (classification feeds reporting but does not produce it)

## Typical Activation
"Classify this deal", "what type of ARR is [deal]", "is this new or expansion", "deal classification for [account]", "verify ARR classification"

## Classification routing
Deal type determines pipeline ownership and tracking destination:
- **New ARR / Reactivation** → Sales-owned pipeline; tracks to Sales new-logo forecast
- **Expansion** → CS-owned pipeline; tracks to CS expansion pipeline and CS deal desk for commercial terms; routes to `pipeline-coverage-analysis` for CS expansion attainment
- **Renewal** → CS-owned pipeline; tracks to CS renewal book of business and GRR monitoring

Classification is the routing mechanism. An Expansion or Renewal classification
means CS leadership and CS ops own the downstream tracking — not Sales.

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of deal classification request is this?
   - Single deal scoring (one opportunity, independent signal)
   - Portfolio classification sweep (rep / segment / all open pipeline)
   - Call validation (rep's stated category vs. model signal)
   - Closed-won verification before CS handoff

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user wants independent deal scoring or call validation
   2. Check HubSpot for activity data — required for classification; declare fallback if absent
   3. Apply G5 — classification is analytical input; rep and manager own the judgment
   4. Apply G6 — surface data-as-of on all activity reads
   5. Do not present classification as override — present as independent signal

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Is HubSpot activity data fresh enough to score? Stale data produces misleading signals — declare data age before presenting classification.
   - Is the scoring model applied consistently across all deals in a sweep? Rep-specific exceptions undermine portfolio-level credibility.
   - Is the delta between rep call and model call surfaced clearly without editorializing? The analyst's job is to flag — rep and manager own the resolution.
   - Is the classification being used in a forecast context? If so, G1 forecast language qualification is required before the output leaves RevOps.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting model classification as a forecast override (G5 violation)
   - Surfacing classification output without data-as-of timestamp (G6 violation)
   - Running a portfolio sweep without declaring scope (segment, rep, date range)
   - Omitting the G1 forecast qualification when classification feeds a leadership or board view

**After execution**, verify:
- G5 analytical input qualifier present on all outputs
- G6 data-as-of label applied to all HubSpot reads
- Delta column populated when rep call and model call diverge
- Confidence: High when HubSpot is connected and activity data is current; Moderate when data is stale or connector is unavailable
    - Confidence: [High] when HubSpot is connected and activity data is current / [Medium] when data is stale or connector is unavailable / [Low] if all inputs are manual or unverified

---

## Scoring Dimensions (20 points each, total 100)

| Dimension | Commit signal | Best Case signal | Pipeline signal |
|-----------|--------------|-----------------|----------------|
| **Activity recency** | Contact in ≤7 days | Contact in 8–21 days | No contact >21 days |
| **Stakeholder coverage** | EB + Champion + TC all engaged | 2 of 3 engaged | 1 or fewer engaged |
| **Stage progression rate** | On or ahead of historical avg | 0–25% behind avg | >25% behind avg |
| **Competitive signal** | No active competitor / counter-play logged | Competitor mentioned, response logged | Competitor active, no response |
| **Rep forecast accuracy** | Rep's trailing commit accuracy ≥70% | 50–70% | <50% |

**Classification:**
- 80–100 → Commit
- 55–79 → Best Case
- <55 → Pipeline

---

## Output

```
DEAL CLASSIFICATION — [Rep / Segment / All]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Deal             ACV      Rep Call    Model Call  Delta   Primary signal
[Account A]      $XXXk    Commit      Commit      —       Activity current, EB engaged
[Account B]      $XXXk    Commit      Best Case   ▼1      No EB contact in 18 days
[Account C]      $XXXk    Best Case   Pipeline    ▼1      Stage stalled 3x avg; no TC

Agreements:  [N] deals  (XX%)
Δ−1 (one tier down): [N] deals  (XX%)
Δ−2 (two tiers down): [N] deals  (XX%)

Adjusted pipeline summary (model-based):
  Commit:     $XXXk  (vs. $XXXk rep-reported)
  Best Case:  $XXXk
  Pipeline:   $XXXk

[DRAFT — RevOps internal] [Confidence: High/Moderate]
[G5: This is an analytical input. Rep and manager own the forecast call.]
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
**Data sensitivity:** Inputs may contain confidential deal and pipeline data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G5: Always include: "This classification is an analytical input based on CRM
  signals. The rep and their manager own the forecast judgment."
- G6: Data-as-of timestamp required
- G1: If summary is used in a forecast context, apply forecast language qualification
