---
name: gtm-unified-metrics-pulse
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Weekly cross-functional metrics report covering five sections: revenue system pipeline (new logo + expansion + renewal pipelines across Sales and CS), handoff quality (RevOps/CS ops), CS capacity status (leadership), early churn flags with account names (#cs-leadership only), outcome realization summary (aggregate to all, account-level to #cs-leadership). All Slack posts require Write-tier confirmation. Triggers: 'weekly pulse', 'GTM metrics', 'alignment pulse', 'cross-functional metrics', 'run the weekly pulse'."
---

[PROPOSED]

# GTM Unified Metrics Pulse

Five-section weekly signal for the full revenue lifecycle.
The one report that replaces "which number is right?" in the leadership meeting.

**Reference:** Output destination labels → `../../../shared/revops-domain-model.md §11`
**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `slack_connected`, `linear_connected`, `cs_platform_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `slack_connected`, `linear_connected`, `cs_platform_connected`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- Leadership needs a single-view metrics pulse across the full revenue system — Sales new logo pipeline, CS expansion pipeline, and CS renewal pipeline
- Weekly or monthly GTM metrics brief required across functions
- Board or exec review needs unified GTM health snapshot including CS-owned ARR

## Do NOT use for
- Deep-dive analysis on a specific metric (use the domain-specific skill)
- Narrative executive revenue brief — use `revenue-brief-generation`
- Pipeline analysis in isolation (use pipeline-coverage-analysis)

## Typical Activation
"GTM metrics pulse", "unified metrics brief", "GTM health check", "cross-functional metrics report", "weekly GTM pulse"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of GTM pulse request is this?
   - Full five-section pulse (all sections — weekly leadership-ready report)
   - Single-section deep dive (one section requested in isolation)
   - Slack delivery run (pulse already built — routing to correct channels)
   - Fallback-mode pulse (one or more connectors unavailable — labeled partial output)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting weekly pulse or GTM alignment report
   2. Check all connectors — HubSpot, CS platform, OCV catalog; pulse quality degrades section-by-section if unavailable
   3. Build each section independently; label connector status and data-as-of per section
   4. Apply G1 — forecast language qualification required in Section 1
   5. Apply G7 — Section 4 churn flags require escalation path and named owner per account
   6. Apply G6 — data-as-of timestamp required on every section header
   7. Confirm Slack destination before any post — Write-tier; RevOps lead preview required
   8. Route Sections 4–5 account-level data to #cs-leadership only; never to #revops-alignment

3. **EXPERT CHECK**: What would a veteran RevOps GTM analyst verify first?
   - Is data freshness declared on every section before surfacing numbers? A stale HubSpot read
     in Section 1 that doesn't show the data-as-of date misleads leadership on pipeline currency.
   - Are CS-owned vectors (Expansion and Renewal) correctly labeled as CS accountability signals,
     not Sales? Misattributing CS-owned ARR to Sales creates conflicting ownership in the meeting.
   - Does every Section 4 churn flag carry a named escalation owner? "Flag to CS team" is not
     actionable — the named CSM or CS manager must appear on every account-level flag.
   - Is the Slack destination confirmed for account-level data before any post? Section 4 and
     Section 5 account detail must never land in #revops-alignment — only #cs-leadership.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Producing any section from unavailable connector data without a labeled fallback (produces phantom metrics)
   - Posting account-level churn flags or outcome data to #revops-alignment instead of #cs-leadership
   - Applying G1 forecast qualification only to new logo pipeline but not to expansion or renewal forecast
   - Surfacing connector reads without data-as-of timestamp (G6 violation)

**After execution**, verify:
- G1 qualification present on all Section 1 forecast lines
- G6 data-as-of label applied to every section header with a connector read
- G7 escalation path with named owner present on every Section 4 churn flag
- Slack destination confirmed for account-level data — #cs-leadership only
- Confidence: High when all connectors are live and data is current; Moderate when any connector is unavailable or data is stale
    - Confidence: [High] when all connectors are live and data is current / [Medium] when any connector is unavailable or data is stale / [Low] if all inputs are manual or unverified

---

## Five Sections

### Section 1 — Revenue System Pipeline → Forecast → Closed/Won
```
Source: HubSpot + CS platform [CRM ✓ live — as of YYYY-MM-DD]

  NEW LOGO (Sales-owned)
  Pipeline total: $XXXk  (WoW: +$XXXk ↑ / −$XXXk ↓)
  Forecast (P50): $XXXk  (WoW: [delta])
  Closed/won MTD: $XXXk  (vs. $XXXk plan — XX% attainment)

  EXPANSION (CS-owned)
  Expansion pipeline: $XXXk  (WoW: +$XXXk ↑ / −$XXXk ↓)
  Expansion forecast (P50): $XXXk  (WoW: [delta])
  Expansion closed MTD: $XXXk  (vs. $XXXk plan — XX% attainment)

  RENEWAL (CS-owned)
  Renewal book at risk (next 90 days): $XXXk
  Renewal forecast GRR: XX%  (vs. XX% plan)
  Renewals closed MTD: $XXXk  (XX% of due book)

Why it changed: [One line per vector if WoW delta >threshold]
[G1: Forecast is a model. Not a revenue commitment.]
```

**Application context:** Section 1 covers the full revenue system.
Vector 1 (New logo) is Sales-owned. Vectors 2–3 (Expansion and Renewal)
are CS-owned — CS leaders are accountable for these numbers the same way
Sales is accountable for new logo attainment.

### Section 2 — Handoff Quality
```
Source: HubSpot + OCV catalog [CRM ✓ live]
  Deals closed this week: [N]
  Avg handoff score: [N]/100
  Below-threshold deals: [N] — Linear issues created ✓
[No account names — aggregate only]
```

### Section 3 — CS Capacity Signal
```
Source: Company profile + SA1 forecast [Company profile]
  CS headroom: XX%  [HEALTHY / AT-RISK / CRITICAL]
  At P50 forecast: CSMs needed [N], in seat [N], gap [+N/-N]
  Hiring lead time flag: [if applicable]
[G2: Structural signal. Hiring requires budget approval.]
```

### Section 4 — Early Churn Flags `[#cs-leadership ONLY]`
```
Source: CS platform + CRM [CS Platform ✓ live / Stale N days]
  Accounts crossing threshold this week: [N]
  [Account name]  Tier [N]  Signal: [specific]  ACV: $XXXk
  [Account name]  Tier [N]  Signal: [specific]  ACV: $XXXk
[G7: Each flag includes escalation path]
[DESTINATION: #cs-leadership only — do not post to #revops-alignment]
```

### Section 5 — Outcome Realization
```
Source: OCV catalog + CS platform [CS Platform ✓ live]
  Portfolio L2+ attainment: XX%  (WoW: +Xpp ↑ / −Xpp ↓)
  L0 accounts past 90-day checkpoint: [N]  (threshold: [N])
  [If cohort diverging: flag — aggregate description, no account names]
[Account-level detail → #cs-leadership only]
```

---

## Slack Delivery (Write-tier — requires confirmation)

```
Confirm before posting:
  Sections 1–3: → #revops-alignment [all C4CS users]
  Section 4 (account names): → #cs-leadership [CS leadership only]
  Section 5 (aggregate): → #revops-alignment
  Section 5 (account detail): → #cs-leadership

Preview shown to RevOps lead before any Slack post.
Once weekly schedule confirmed, subsequent posts auto-proceed UNLESS:
  - Section 4 contains a Tier 3 flag for an enterprise account (individual review)
```

---

## Fallback (connector unavailable)

```
Section 1: No HubSpot → "Pipeline data unavailable [HubSpot: Unavailable]"
Section 3: No CS platform → "CS capacity model running on CRM signals only [Confidence: Moderate]"
Section 4: No CS platform → "Churn signal scan unavailable [CS Platform: Unavailable]"
Section 5: No OCV catalog → "Outcome tracking unavailable — OCV catalog not configured"
```

Always declare what's missing. Never produce a section from unavailable data
without labeling it.

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

- G1: Section 1 forecast language qualification
- G2: Section 3 structural input qualifier
- G7: Section 4 every flag has escalation path and owner
- G6: Data-as-of on every section header
- Write-tier: Preview required before Slack posts
