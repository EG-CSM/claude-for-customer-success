---
name: segment-analyzer
description: >
  Analyze the CS book by segment — ARR distribution, health distribution per
  segment, CSM coverage ratios, motion-to-segment fit, and reclassification
  candidates. Use for quarterly planning, headcount requests, CS motion
  calibration, or when leadership asks "how is [segment] performing?" Produces
  a segment analysis report and optional reclassification queue. Distinct from
  health-model-review: this skill analyzes by segment, not by health component.
argument-hint: "[--full | --segment <name> | --reclassification | --at-risk]"
version: "1.0.0"
deployment_target: plugin
---

# /cs-ops:segment-analyzer

Understand the book by segment — who's in each tier, how coverage looks,
and where motion-to-segment fit is breaking down.

[PROPOSED]

---

## Use when

- Running quarterly planning and need a cross-segment ARR and health view
- Building a headcount request that requires segment-level coverage data
- Leadership asks "how is [segment] performing?" and you need a structured answer
- Reclassification candidates need to be identified after an ARR threshold change
- A health model review has surfaced a segment-level anomaly worth investigating
- Weekly triage requires an at-risk account view segmented by ARR exposure

## Do NOT use for

- Portfolio-wide health model calibration (use `/cs-ops:health-model-review`)
- Individual account health reviews (use `/csm:health-score-review`)
- CSM capacity load analysis (use `/cs-ops:capacity-planner`)
- Updating segment definitions in config (use `/cs-ops:customize --section segments`)

## Typical activation

- `/cs-ops:segment-analyzer` — full cross-segment analysis (default)
- `/cs-ops:segment-analyzer --segment <name>` — deep dive on one segment
- `/cs-ops:segment-analyzer --reclassification` — accounts that have crossed ARR thresholds
- `/cs-ops:segment-analyzer --at-risk` — Red and Yellow accounts by segment for triage

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
and `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/cs-ops:cold-start-interview`.

Critical configuration to apply:
- Segment definitions — names, ARR ranges, reclassification thresholds
- Target CSM-to-account ratios per segment
- CS motion by segment (high-touch / hybrid / tech-touch)
- Segment assignment method (automated vs. manual)
- Primary performance indicator and reporting period

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of segment analysis request is this?
   - **Full Portfolio Review**: All-segment analysis for planning, headcount, or board reporting. Optimize for cross-segment comparison and structural insights over per-account detail.
   - **Single-Segment Deep Dive**: One segment under the microscope — health, coverage, motion fit. Benchmark against portfolio norms to distinguish segment-specific problems from portfolio-wide patterns.
   - **Reclassification Queue**: Accounts crossing ARR thresholds that need segment reassignment. Separate upward (opportunity) from downward (relationship risk) moves — they require different handling.
   - **At-Risk Triage**: Red and Yellow accounts by segment for weekly triage or escalation prioritization. ARR-weight everything — dollar exposure drives priority, not account count.

2. **CONSTRAINTS**: What limits the solution space?
   - G2: Segment definitions from cs-ops config are authoritative — flag reclassification candidates, never silently reclassify.
   - G4: Coverage ratios require CSM assignment data — if CSM owner is missing for accounts, flag the gap rather than extrapolating. Missing data skews ratios.
   - G5: Output containing ARR, health scores, or coverage ratios is internal CS-Ops material — apply confidentiality check before distribution beyond the CS team.
   - G7: Flag stale data with source date — CRM >7 days, CS Platform >3 days. At-risk ARR figures require validation against CRM renewal dates before sharing with finance or leadership.

3. **EXPERT CHECK**: What would a veteran CS-Ops leader verify first?
   - Is ARR concentration accounted for — or is the analysis misleading by treating all accounts as equal weight? One Enterprise Red account may outweigh 20 SMB Red accounts.
   - Are coverage ratios paired with ARR-per-CSM, not just accounts-per-CSM? A CSM at target ratio but holding 60% of their ARR in 3 accounts has a concentration problem the ratio hides.
   - Does the motion-to-segment fit assessment distinguish between a coverage quantity gap (not enough CSMs) and a coverage quality gap (wrong engagement model)?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Producing segment summary tables without cross-segment interpretation — tables are data, the interpretation naming the structural imbalance is the analysis.
   - Comparing segments by account count instead of ARR weight — misleads headcount and resource allocation decisions.
   - Treating reclassification as mechanical ARR-threshold math without flagging relationship risk on downward moves or elapsed time on stale crossings.
   - Listing at-risk accounts without ARR ranking — wastes triage time; sort by dollar exposure, not health severity.
   - Reporting a segment's Red percentage in isolation without benchmarking against the portfolio average — 30% Red looks alarming until the portfolio average is 28%.
   - Omitting "Active play?" status on at-risk accounts — an account with an active intervention is a different triage priority than one with none.

**After execution**, verify:
- Does the analysis answer the operational question behind the request (headcount justification, motion recalibration, triage prioritization)?
- Are all data sources timestamped and staleness-flagged per G7?
- Is the output mode (--full / --segment / --reclassification / --at-risk) matched to the actual need?
- Confidence: [High] if live CRM + CS Platform with configured segment definitions / [Medium] if single source or partially stale / [Low] if user-provided context only — state which.

## Mode

`--full`: Complete segment analysis across all configured segments. **Default.**

`--segment <name>`: Deep analysis of one segment only — health, coverage,
at-risk accounts, and motion fit within that segment.

`--reclassification`: Identify accounts that have crossed a configured ARR
threshold and should move to a different segment. Produces a reclassification
queue with recommended actions for each account.

`--at-risk`: Filter view — Red and Yellow accounts only, segmented, with
ARR-at-risk totals by segment. Suitable for weekly triage reporting.

---

## Data gathering

Pull from connected integrations:
- CRM: ARR per account, segment classification, CSM owner, renewal date
- CS Platform: health score and tier per account, lifecycle stage
- CS-Ops config: target ratios, motion assignments, segment thresholds

If nothing is connected:
> "To analyze the book by segment, I need an account-level export with:
> account name, ARR, segment, health tier, and CSM owner.
> Share a CSV or paste the data and I'll run the analysis."

Minimum required: ARR, segment, and health classification per account.
CSM owner is required for coverage ratio analysis.

---

## Full segment analysis (`--full`)

---

**Segment Analysis Report**
*[Date] · [N] total accounts · $[total ARR] · INTERNAL — CS-Ops use only*

---

### Portfolio by segment — summary

| Segment | Accounts | % of book | ARR | % of ARR | Avg ARR |
|---------|----------|-----------|-----|----------|---------|
| [Enterprise] | [N] | [%] | $[amount] | [%] | $[avg] |
| [Mid-market] | [N] | [%] | $[amount] | [%] | $[avg] |
| [SMB] | [N] | [%] | $[amount] | [%] | $[avg] |
| [Unclassified] | [N] | [%] | $[amount] | [%] | — |
| **Total** | [N] | 100% | $[total] | 100% | |

---

### Per-segment deep view

Repeat this block for each configured segment:

---

#### [Segment name] — [configured ARR range]

**Overview**

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Accounts | [N] | — | — |
| ARR | $[amount] | — | — |
| Avg ARR per account | $[amount] | — | — |
| CSMs assigned | [N] | — | — |
| Accounts per CSM | [ratio] | [configured target] | [✅ At target / ⚠️ Over / ⚠️ Under] |
| CS motion | [configured motion] | [configured motion] | — |

**Health distribution within segment**

| Tier | Accounts | % of segment | ARR | % of segment ARR |
|------|----------|-------------|-----|-----------------|
| 🟢 Green | [N] | [%] | $[amount] | [%] |
| 🟡 Yellow | [N] | [%] | $[amount] | [%] |
| 🔴 Red | [N] | [%] | $[amount] | [%] |

**ARR at risk in segment:** $[Red + Yellow] — [%] of segment ARR

**CSM coverage**

| CSM | Accounts | ARR | Health mix (G/Y/R) | Notes |
|-----|----------|-----|--------------------|-------|
| [CSM 1] | [N] | $[amount] | [N]/[N]/[N] | [Over capacity / At target / Under] |
| [CSM 2] | | | | |
| [CSM 3] | | | | |

**Upcoming renewals (next 90 days in segment)**

| Account | ARR | Health | Renewal date | CSM |
|---------|-----|--------|-------------|-----|
| [Account] | $[amount] | [🟢/🟡/🔴] | [date] | [name] |

**Segment observations:**

[2-3 sentences specific to this segment. What's notable about the health
distribution, coverage load, or upcoming renewal concentration? Name specifics —
not generic observations.]

---

### Cross-segment comparison

| Dimension | [Enterprise] | [Mid-market] | [SMB] |
|-----------|-------------|-------------|-------|
| At-risk ARR (Red + Yellow) | $[amount] ([%]) | | |
| Accounts per CSM (actual vs. target) | [N] / [N] | | |
| Green % | [%] | [%] | [%] |
| Renewals next 90 days (ARR) | $[amount] | | |
| Reclassification candidates | [N] | [N] | [N] |

**Cross-segment interpretation:**
[2-3 sentences on the most significant cross-segment finding — motion fit,
ARR concentration risk, coverage imbalance, or renewal pressure. Specific.]

---

### Motion-to-segment fit assessment

For each segment, assess whether the configured CS motion is delivering the
right level of engagement given current health and CSM load:

| Segment | Configured motion | CSM load | Health outcome | Fit assessment |
|---------|-----------------|----------|---------------|----------------|
| [Enterprise] | High-touch | [N accounts/CSM] | [Green %] | [Well-fit / Overstretched / Under-engaged] |
| [Mid-market] | [motion] | | | |
| [SMB] | [motion] | | | |

If motion-to-segment fit is poor:
> "The [segment] motion appears [overstretched / mismatched] — CSMs are carrying
> [actual ratio] accounts vs. the [target ratio] target, and the Red tier in this
> segment is [%] above the portfolio average. This may indicate a coverage gap
> that is manifesting as health deterioration rather than a product or relationship
> problem." `[review]`

---

### Reclassification candidates (`--reclassification` content)

Accounts that have crossed a configured ARR threshold and should move segments:

| Account | Current segment | Current ARR | Threshold crossed | Recommended segment | CSM | Action |
|---------|----------------|------------|-----------------|-------------------|-----|--------|
| [Account] | [Segment] | $[amount] | $[threshold] ([up/down]) | [New segment] | [CSM] | Reassign by [date] |

**Reclassification notes:**
- Upward reclassification (e.g., SMB → Mid-market): triggers higher-touch
  motion assignment. Assign a dedicated CSM before the next renewal cycle.
- Downward reclassification (e.g., Mid-market → SMB): confirm with CS lead
  before moving — downward reclassification during an active relationship can
  be perceived as a service reduction.

**Total reclassification candidates:** [N] accounts · $[ARR impact]

---

### At-risk segment view (`--at-risk`)

---

**At-Risk Accounts by Segment — [Date]**
*Red and Yellow accounts only*

| Segment | Red accounts | Red ARR | Yellow accounts | Yellow ARR | Total at-risk ARR |
|---------|-------------|---------|----------------|------------|------------------|
| [Enterprise] | [N] | $[amount] | [N] | $[amount] | $[amount] |
| [Mid-market] | | | | | |
| [SMB] | | | | | |
| **Total** | [N] | $[amount] | [N] | $[amount] | $[amount] |

**Top 10 at-risk accounts by ARR:**

| Account | Segment | Tier | ARR | Renewal | CSM | Active play? |
|---------|---------|------|-----|---------|-----|-------------|
| [Account] | [Seg] | 🔴 | $[amount] | [date] | [name] | [Yes / No] |

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live | CS Platform ✓ live | user-provided export — [date] | conversation context only]
> - **Segment definitions applied:** [Configured definitions from cs-ops CLAUDE.md | Company-profile.md | User provided this session]
> - **Coverage ratios:** [Calculated from CSM assignment data | CSM assignments not available — ratios estimated]
> - **Reclassification:** [Based on configured ARR thresholds | Thresholds not configured — skipped]
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before acting on reclassification:** Confirm with CS lead — segment changes may affect CSM relationships and engagement cadence.

---

## Output

Segment analysis report — format driven by the mode flag
(`--full`, `--segment <name>`, `--reclassification`, or `--at-risk`).
Produces a structured markdown report with: segment health summary, ICP alignment
scores, misfit account inventory, and recommended segment or coverage adjustments.
See **Full segment analysis** section for field-level detail.

## Guardrails

**Segment definitions are authoritative.** If an account's ARR falls in a
different segment range than its current classification, flag it as a
reclassification candidate — do not silently reclassify in the analysis.

**Coverage ratios require CSM assignment data.** If CSM owner is missing
for accounts, flag the coverage gap rather than extrapolating from available
accounts. Missing data skews ratio calculations.

**Motion-to-segment fit is a hypothesis.** Observations about motion fit
are directional — confirm with the CS lead before recommending motion changes.
A coverage ratio that looks overstretched may reflect a CSM who is highly
efficient, not a structural problem.

**Downward reclassification requires care.** Flag it — do not recommend
it without noting the relationship risk. An account that is currently Green
and generating goodwill should not be moved to a lower-touch model without
a customer conversation plan.

**At-risk ARR figures require validation.** Before sharing at-risk ARR with
finance or leadership, validate against CRM renewal dates and contract values.

---

## After the analysis

- "Segment analysis done — check CSM capacity: `/cs-ops:capacity-planner`"
- "Reclassification queue identified — update config: `/cs-ops:customize --section segments`"
- "At-risk concentration in [segment] — run health audit: `/cs-ops:health-model-review`"
- "Coverage gap identified — build headcount case: `/cs-ops:capacity-planner --headcount`"
- "Need the full metrics dashboard: `/cs-ops:metric-dashboard`"
