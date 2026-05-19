---
name: data-decay-tracking
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Monitors contact and account data freshness. Flags records where title, company, or contact data has likely changed and enrichment is overdue. Decay signals: contact title unchanged >18 months, account employee count stale >12 months, primary contact no email activity >6 months, account domain change detected. Prioritizes enterprise accounts. Triggers: 'stale contacts', 'data decay', 'enrichment needed', 'contact freshness', 'stale account data'."
---

[PROPOSED]

# Data Decay Tracking

Data decay is the slow death of CRM quality. Contacts leave roles. Companies
get acquired. Enrichment overdue means signals are built on wrong data.

**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `primary_segment`, `crm_system`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `primary_segment`, `crm_system`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
> Routing: Use this skill when **contact or company record age is the specific concern** — for a point-in-time CRM health score use `crm-hygiene-audit`; for field completion rates over time use `field-completion-monitoring`.
- CRM record staleness needs to be quantified and trended
- Data freshness audit required before a planning or forecast cycle
- Records without activity within a configurable window need identification

## Do NOT use for
- Full CRM hygiene audit (use crm-hygiene-audit)
- Field completion compliance (use field-completion-monitoring)
- Duplicate detection (use duplicate-detection)

## Typical Activation
"Data decay tracking", "stale records", "how old is our data", "data decay report for [object/period]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of data decay request is this?
   - Single-account decay audit (one account — all four signals checked across contacts and account record)
   - Segment-level freshness sweep (enterprise tier, mid-market, or full portfolio — prioritized by segment)
   - Signal-specific scan (user requesting a targeted check on one decay signal type — title age, employee count, email activity, or domain change)
   - Pre-cycle enrichment triage (identifying enrichment candidates before a planning, forecast, or QBR cycle)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting freshness review, enrichment candidates, or CRM data quality assessment
   2. Pull HubSpot contact and account data; declare connector status and data-as-of timestamp per G6
   3. Apply G6 — stale data must be labeled; decay findings are themselves evidence of staleness; every flagged record carries its own data-as-of note
   4. Apply G9 — no autonomous enrichment API calls; flag candidates for human action only
   5. Prioritize enterprise tier accounts in output; surface mid-market as secondary tier
   6. Confirm `primary_segment` from config to scope tier-level prioritization correctly
   7. Confirm output destination before delivering — internal RevOps enrichment queue vs. CSM account review vs. leadership data quality report

3. **EXPERT CHECK**: What would a veteran RevOps data quality analyst verify before surfacing findings?
   - Is the title-unchanged signal calibrated to B2B tenure, not calendar time? The 18-month threshold reflects average B2B role tenure — applying it uniformly to individual contributors and executives produces different false-positive rates. Flag when the contact is a champion or economic buyer, not just any contact.
   - Is the email activity gap distinguished from enrichment staleness? A contact with no email activity in 6 months may still have a current title — the signal indicates possible departure, not confirmed departure. The output must not conflate "likely departed" with "confirmed stale."
   - Is the domain change signal sourced from a reliable detection mechanism? Domain changes flagged from deal notes or rep-entered data carry lower confidence than those detected from connector-side validation. Declare the detection source and confidence level.
   - Is the enterprise account list scoped to the configured `primary_segment`? Applying enterprise-tier prioritization to a primarily SMB or mid-market book produces a misleading high-priority list. Confirm segment alignment before ranking.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Conflating "no email activity >6 months" with "confirmed contact departure" — label as departure signal, not confirmed fact (G6 violation if presented as fact)
   - Flagging title-unchanged signal on all contacts regardless of role seniority — champion and economic buyer contacts are the high-value targets; all-contact title sweeps generate noise
   - Pulling HubSpot contact/account data without data-as-of timestamp (G6 violation)
   - Surfacing domain change findings without declaring detection source confidence
   - Proposing autonomous enrichment API calls — all enrichment is flagged for human action per G9

**After execution**, verify:
- G6 data-as-of label applied to all HubSpot contact and account reads
- G9 compliance — no autonomous enrichment calls proposed; all findings are human-action candidates
- Departure signal labeled as signal, not confirmed fact — no overstatement of contact status
- Enterprise tier accounts prioritized per `primary_segment` config
- Confidence: High when HubSpot connected and contact/account data current; Moderate when connector unavailable or decay signals sourced from last-known update timestamps only
- Confidence: [High] when HubSpot connected and contact/account data current / [Medium] when connector unavailable or data estimated / [Low] if all inputs are manual or unverified

---

## Four Decay Signals

```
Signal 1: Contact title unchanged >18 months (avg B2B tenure)
Signal 2: Account employee count not updated >12 months
Signal 3: Primary contact — no email activity >6 months (possible departure)
Signal 4: Account domain change detected (acquisition or rebrand)
```

---

## Output

```
DATA DECAY REPORT — [Tier/Scope] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

Enterprise accounts — enrichment overdue:
Account         Signal                              Last updated   Priority
[Company A]     Domain change detected              14 months ago  HIGH
[Company B]     Champion title unchanged 22 months  22 months ago  MEDIUM
[Company C]     Primary contact no activity 7mo     7 months ago   MEDIUM

Mid-Market accounts — enrichment overdue: [N] accounts

All accounts summary:
  Total flagged:      [N] accounts
  High priority:      [N]  (domain change or champion likely departed)
  Medium priority:    [N]  (title/count stale)

Recommended action: Enrich [N] high-priority accounts before next QBR cycle.
Enrichment tool: [user's configured enrichment source if available, else manual]

[No autonomous enrichment calls will be made]
[Write-tier: Contact/account updates require human confirmation]
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

- G6: Decay report outputs themselves note staleness risk on every flagged record
- G9: No autonomous enrichment API calls
