---
name: pipeline-coverage-analysis
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Calculates pipeline coverage ratio by segment, rep, and quarter. Flags when coverage falls below the threshold derived from win rate (not a universal 3x). Produces an exposure ranking and week-over-week trend. Use when assessing pipeline health before a forecast call, board review, or quarter-close. Triggers: 'pipeline coverage', 'coverage ratio', 'are we covered for Q[N]', 'pipeline risk by segment'."
---

[PROPOSED]

# Pipeline Coverage Analysis

Calculates pipeline coverage ratio and surfaces exposure risk before it becomes
a missed quarter. Coverage threshold is always derived from win rate — never a
universal 3x rule.

**Reference:** Coverage thresholds → `../../../shared/revops-domain-model.md §7`
**Config reads:** `win_rate` (user-provided or company profile), `current_arr`,
`target_growth_pct`, `nrr_current`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `win_rate`, `current_arr`, `target_growth_pct`, `nrr_current`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- User needs pipeline coverage ratio analysis against quota or target
- Forecast call preparation requires coverage gap identification by rep, segment, or team
- Coverage adequacy assessment needed before end of quarter

## Do NOT use for
- Individual deal health scoring (use deal-health-scoring)
- Pipeline velocity or stage conversion analysis (use pipeline-velocity-tracking)
- Full forecast number generation (use forecast-variance-analysis)

## Typical Activation
"Pipeline coverage analysis", "do we have enough pipeline?", "coverage ratio for Q[N]", "pipeline vs quota for [rep/team]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of pipeline coverage request is this?
   - Full team coverage summary (all segments — coverage ratio, signal, exposure ranking)
   - Single-segment or rep coverage check (one scope — ratio + gap calculation)
   - Pre-forecast coverage review (quarter close prep — CRITICAL/AT-RISK flags + trend)
   - Coverage gap projection (forward-looking — weeks to gap close at current add rate)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user asking about coverage, pipeline sufficiency, or quarter risk
   2. Check HubSpot connector for pipeline data; declare fallback if unavailable
   3. Read company profile for win rate, target growth, segment definition
   4. Apply G6 — data-as-of timestamp required on all pipeline figures
   5. Apply G1 — coverage output for leadership or board requires forecast language qualification
   6. Apply G5 — coverage ratio is a structural signal; Sales leadership owns the response
   7. Confirm output destination before delivering — internal RevOps vs. leadership vs. finance

3. **EXPERT CHECK**: What would a veteran RevOps pipeline analyst verify first?
   - Is the win rate source declared? A 3x universal rule applied without win rate data is
     analytically invalid — the required coverage multiple must be derived from actual win rate
     or explicitly flagged as an assumed default.
   - Is the pipeline pull scoped to the correct quarter close date? Pulling all open pipeline
     without date filtering overstates coverage for the current quarter close.
   - Is G5 qualification present if the output includes rep-level coverage? Coverage ratios
     by rep are structural signals — the coaching response belongs to Sales management, not RevOps.
   - Is the INSPECT signal explained? Coverage above 5x can indicate pipeline inflation
     or sandbagging — surfacing it without explanation misleads the forecast call.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Applying a universal 3x coverage threshold without deriving from win rate (invalidates the analysis)
   - Surfacing HubSpot pipeline data without data-as-of timestamp (G6 violation)
   - Presenting rep-level coverage as a performance directive rather than structural signal (G5 violation)
   - Applying G1 forecast qualification only to total coverage but not to segment-level projections

**After execution**, verify:
- G1 qualification present if coverage output is destined for leadership or board
- G5 qualifier present on any rep-level coverage surfaced in output
- G6 data-as-of label applied to all pipeline figures from HubSpot
- Coverage threshold derivation declared — win rate source named and labeled
- Confidence: High when HubSpot is connected and data is current; Moderate when data is stale, win rate is assumed, or connector is unavailable
    - Confidence: [High] when HubSpot is connected and data is current / [Medium] when data is stale, win rate is assumed, or connector is unavailable / [Low] if all inputs are manual or unverified

---

## Inputs

**Connector error categorization:** When a connector call fails, distinguish the error type before proceeding:
- **Rate-limited (transient):** Connector returns HTTP 429 or equivalent throttle signal. Note the rate limit explicitly in output ("CRM data temporarily rate-limited — retry in 60 seconds recommended") and offer to retry rather than proceeding with degraded output.
- **Unavailable (permanent for this session):** Connector is not configured, authentication has expired, or service is down. Fall back to user-provided data and label all affected sections as "connector unavailable — manual input used."
Do not conflate these — a rate-limited connector will return data shortly; an unavailable connector will not.

Required (from company profile or user):
- Current pipeline value by stage (from HubSpot or user-provided)
- Win rate (company profile or user-stated)
- New ARR target (derived from company profile or user-provided)

Optional:
- Segment filter, rep filter, quarter filter

---

## Workflow

**Step 1 — Derive required coverage**
```
Required Coverage = 1 ÷ Win Rate  [revops-domain-model.md §4]
Pipeline Target   = New ARR Target × Required Coverage
```
State the win rate used and its source `[Company profile]` or `[User provided]`.

**Step 2 — Calculate current coverage by segment**
Pull open pipeline from HubSpot filtered to current quarter close dates.
For each segment:
```
Current Coverage = Current Pipeline Value ÷ New ARR Target
Pipeline Gap     = Pipeline Target − Current Pipeline Value
```

**Step 3 — Apply coverage signal thresholds** `[revops-domain-model.md §7]`
- Below 2x → CRITICAL
- 2x–3x → AT-RISK
- 3x–5x → HEALTHY
- Above 5x → INSPECT

**Step 4 — Produce exposure ranking**
Sort segments and reps by gap magnitude. Name the top 3 most exposed.

**Step 5 — Week-over-week trend**
Compare to prior week's pipeline pull if available in session history.
If not available, note: "Prior week data unavailable — trend not calculated."

---

## Output

```
PIPELINE COVERAGE ANALYSIS
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High/Moderate]

Required coverage: [N]x (1 ÷ [win_rate]% win rate)
─────────────────────────────────────────────────────
Segment          Coverage   Signal      Gap
Enterprise       2.8x       AT-RISK     $420K short
Mid-Market       4.1x       HEALTHY     —
SMB              1.6x       CRITICAL    $280K short
─────────────────────────────────────────────────────
Overall          3.1x       HEALTHY     $700K short in 2 segments

Top exposures:
1. SMB — $280K gap; pipeline at 1.6x vs 4.0x required
2. Enterprise — $420K gap; thin buffer against plan

Week-over-week: [+$X / −$X / unavailable]

[DRAFT — RevOps internal] [Confidence: High]
```

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

- G1: If output is for leadership or board, add: "Coverage as of [date]. Subject to
  pipeline movement before quarter close."
- G6: Always surface data-as-of timestamp
- G5: "Coverage ratio is a structural signal. Sales leadership owns the response."
