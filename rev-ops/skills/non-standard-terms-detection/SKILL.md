---
name: non-standard-terms-detection
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Scans deal notes and opportunity fields for payment terms, contract structures, and custom provisions outside the standard playbook. Detection patterns: payment terms net >30 days, multi-year ramps/price locks, SLA commitments, data residency requirements, indemnification carve-outs, source code escrow. Routes to Legal or Finance when required. Triggers: 'non-standard terms', 'off-playbook deal', 'custom provisions', 'payment terms', 'SLA commitment', 'data residency'."
---

[PROPOSED]

# Non-Standard Terms Detection

Catches off-playbook provisions before they become legal or financial surprises.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `payment_terms_standard_days`, `linear_connected`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `payment_terms_standard_days`, `linear_connected`

---

## Use when
- Deal notes or contract terms contain non-standard language that needs flagging before close
- Legal or finance review triggers need to be identified from deal context
- Deal desk submission requires non-standard terms inventory

## Do NOT use for
- Full deal desk routing (use deal-desk-workflow-management)
- Revenue leakage structural analysis (use revenue-leakage-scanning)
- ARR classification (use deal-classification)

## Typical Activation
"Non-standard terms", "flag unusual contract terms", "what terms need legal review", "non-standard terms for [deal]", "check deal notes for flags"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of non-standard terms request is this?
   - Single-deal scan (one account — full pattern check across all six detection categories)
   - Deal desk pre-submission review (comprehensive inventory before deal desk routing)
   - Targeted provision check (user flagging a specific clause type — payment terms, SLA, data residency)
   - Batch pipeline scan (multiple deals flagged for terms review before quarter close)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting terms review for a specific deal or set of deals
   2. Pull deal notes and contract fields from HubSpot; declare connector status and data-as-of timestamp per G6
   3. Apply G1 — payment terms affecting revenue recognition require Finance routing before deal close
   4. Apply Write-tier — Linear issue creation to Legal or Finance requires explicit user confirmation before execution
   5. Confirm `payment_terms_standard_days` from config before classifying payment term deviations
   6. Confirm `linear_connected` from config before proposing Linear issue creation
   7. Route mandatory provisions (indemnification carve-outs, source code escrow) to Legal regardless of deal size

3. **EXPERT CHECK**: What would a veteran RevOps deal desk analyst verify before surfacing findings?
   - Are payment terms classified against the configured standard, not a generic assumption? Net 30 is common
     but not universal — the configured `payment_terms_standard_days` is the baseline, not training memory.
   - Is the Finance routing trigger applied correctly for deferred or quarterly billing? These structures
     affect revenue recognition timing, not just cash flow — RevRecog review is a separate requirement
     from Finance approval, and both must surface explicitly.
   - Are mandatory Legal provisions flagged unconditionally? Indemnification carve-outs and source code
     escrow requests are mandatory Legal review regardless of other deal signals — they cannot be
     downgraded based on deal size or segment.
   - Is the Write-tier confirmation surfaced before queuing any Linear issue? A finding log and an issue
     are different outputs — the finding goes in the report; the issue requires explicit confirmation.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Classifying payment terms against a generic net-30 assumption instead of `payment_terms_standard_days`
   - Omitting RevRecog review flag on deferred/quarterly billing structures (Finance approval ≠ RevRecog review)
   - Downgrading mandatory Legal provisions (indemnification, source code escrow) based on deal size
   - Queuing Linear issues without surfacing Write-tier confirmation prompt first (G9 analog for legal routing)
   - Pulling HubSpot deal notes without data-as-of timestamp (G6 violation)

**After execution**, verify:
- G1 qualifier present — payment terms with RevRecog implications flagged for Finance routing before close
- G6 data-as-of label applied to all HubSpot deal note reads
- Write-tier confirmation surfaced for all proposed Linear issues — none queued autonomously
- Mandatory provisions (indemnification, source code escrow) routed to Legal unconditionally
- Confidence: High when HubSpot connected and deal notes current; Moderate when connector unavailable or terms sourced from rep-provided notes only
- Confidence: [High] when HubSpot connected and deal notes current / [Medium] when connector unavailable or terms from rep-provided notes / [Low] if all inputs are manual or unverified

---

## Detection Patterns and Routing

```
Payment terms:
  net > payment_terms_standard_days → Finance review
  quarterly/deferred billing → Finance + RevRecog review

Multi-year structures:
  Price lock clauses → Finance approval
  Ramp schedules → Finance + RevOps approval
  Renewal caps → Legal + Finance review

Custom provisions:
  SLA commitments → Legal + CS Ops review
  Data residency requirements → Legal + Eng review
  Indemnification carve-outs → Legal review (mandatory)
  Source code escrow requests → Legal + Eng review (mandatory)
```

---

## Output

```
NON-STANDARD TERMS — [Account Name]
[HubSpot ✓ live — as of YYYY-MM-DD]

Findings:
  [Term type]  Standard: [what's standard]  Found: [what's in the deal]
               Route to: [Legal / Finance / Both]  Priority: [HIGH/MEDIUM]

No non-standard terms detected: [if clean]

Linear issues to create:
  [ ] Legal: [specific provision] — confirm to create
  [ ] Finance: [specific provision] — confirm to create
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

- G1: RevRecog implications require Finance routing before deal close
- Write-tier: Issue creation requires confirmation
