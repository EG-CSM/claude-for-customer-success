---
name: crm-hygiene-audit
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Overall CRM health score plus rep-level hygiene scorecard across three dimensions: completeness, accuracy, and recency. Produces weekly hygiene report for RevOps review before sharing with Sales managers. Never writes to CRM — all corrections are proposals. Triggers: 'CRM hygiene', 'data quality', 'hygiene report', 'field completeness', 'CRM health score'."
---

[PROPOSED]

# CRM Hygiene Audit

Three-dimension health score at portfolio and rep level. All corrections are
proposals — requires Write-tier confirmation before any CRM edits.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `crm_system`, `primary_segment`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `crm_system`, `primary_segment`

---

## Use when
> Routing: Use this skill when a **point-in-time CRM health score** is needed — for field completion rates over time use `field-completion-monitoring`; for contact/record age and enrichment staleness use `data-decay-tracking`.
- CRM data quality needs a structured audit across key pipeline fields
- Missing fields, stale close dates, or inactive deals need systematic identification
- Pre-forecast hygiene sweep required to improve forecast accuracy

## Do NOT use for
- Stage entry/exit criteria validation (use stage-integrity-audit)
- Duplicate contact or company detection (use duplicate-detection)
- Field completion rate monitoring over time (use field-completion-monitoring)
- CS platform data quality — use /cs-ops:data-quality-check

## Typical Activation
"CRM hygiene audit", "audit the CRM", "hygiene sweep before forecast", "clean up the pipeline"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of CRM hygiene request is this?
   - Full portfolio hygiene audit (all reps, all dimensions)
   - Pre-forecast hygiene sweep (current quarter pipeline only)
   - Rep-level scorecard (specific rep or team)
   - Single-dimension check (completeness, accuracy, or recency only)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting hygiene audit or data quality review
   2. Check HubSpot — full field scan required; declare scope limits if data is large
   3. Apply G6 — data-as-of on all field reads
   4. Apply governance Write-tier — no autonomous CRM edits; all corrections are proposals
   5. Confirm scope: full portfolio, current quarter pipeline, or specific rep

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Is the scope confirmed before pulling data? Full portfolio scans on large CRMs may be slow or incomplete.
   - Is the Write-tier gate explicit in the output? Managers may act on scorecard data — corrections must be clearly labeled as proposals.
   - Are close date anomalies cross-referenced with stage? A past close date on a deal that hasn't moved stages is a different problem than one that has.
   - Is the data-as-of timestamp surfaced before the score? A score without a timestamp is meaningless for trend tracking.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Surfacing a health score without a data-as-of label (G6 violation)
   - Presenting rep scorecard without the Write-tier confirmation note
   - Running full portfolio scan without declaring scope limits when HubSpot data is large
   - Treating hygiene flags as autonomous correction triggers — all corrections are proposals

**After execution**, verify:
- G6 data-as-of label present on all HubSpot reads
- Write-tier confirmation note present on all correction proposals
- Rep scorecard labeled [DRAFT — for RevOps review before sharing with Sales managers]
- Confidence: High when HubSpot is connected and data is fresh; Moderate when any field group is estimated or connector data is stale
    - Confidence: [High] when HubSpot is connected and data is fresh / [Medium] when any field group is estimated or connector data is stale / [Low] if all inputs are manual or unverified

---

## Three Dimensions

**Completeness** — Required fields populated at each stage gate
(per `field-completion-monitoring` gate definitions)

**Accuracy** — Field values passing format and logic validation:
- Close dates not in the past on open deals
- Stage inconsistent with activity history
- ACV outside segment range (flag for review, not auto-correct)
- Contact email format invalid

**Recency** — Staleness signals:
- Last activity date >14 days on open deal (G6 threshold)
- Last contact update >90 days
- Last stage change >30 days on non-stale deal

---

## Output

```
CRM HYGIENE AUDIT — [Scope] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

Overall health score: [N]/100  (vs. [N] prior week  ↑/↓)

Dimension breakdown:
  Completeness:  [N]/100  [N] deals with missing stage-gate fields
  Accuracy:      [N]/100  [N] deals with logic/format issues
  Recency:       [N]/100  [N] deals with stale activity (>14 days)

Rep scorecard:
Rep       Completeness   Accuracy   Recency   Overall
[Rep A]   92             88         85        88
[Rep B]   71             90         62        74  ⚠
[Rep C]   55             78         70        67  ⚠

Top 5 hygiene issues by revenue impact:
1. [Issue type] — [N] deals, $XXXk ACV — Action: [what to fix]
2. ...

[DRAFT — for RevOps review before sharing with Sales managers]
[Write-tier: CRM corrections require human confirmation before execution]
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

- G6: Data-as-of required
- G9 (Write Protocol): No autonomous CRM edits
- G5: Rep scorecard shared with manager — manager owns the coaching response
