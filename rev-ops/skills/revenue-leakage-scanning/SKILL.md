---
name: revenue-leakage-scanning
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Identifies deal structures leaving money on the table before close: underpriced professional services, missing expansion clauses in multi-year deals, renewal terms misaligned with ARR classification, missing success milestone gates for expansion. Fires at Negotiation stage — before close locks the structure. Triggers: 'revenue leakage', 'missing expansion clause', 'mispriced services', 'deal structure review', 'are we leaving money on the table'."
---

[PROPOSED]

# Revenue Leakage Scanning

Structural leakage is easier to fix before the contract is signed.
Primary detection window: Negotiation stage — before close.

**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `avg_deal_acv`, `primary_segment`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `avg_deal_acv`, `primary_segment`

---

## Use when
- Deal is at Negotiation stage and structure needs review before close locks terms
- PS pricing, expansion clauses, or renewal terms need structural review
- User asks whether a deal structure is leaving money on the table

## Do NOT use for
- Post-close deal review (lower leverage — flag this explicitly)
- ARR classification decisions (use deal-classification)
- Deal health or risk scoring (use deal-health-scoring)

## Typical activation
"Revenue leakage scan", "are we leaving money on the table", "missing expansion clause", "mispriced services", "deal structure review for [account]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of revenue leakage scan is this?
   - Single-deal scan (one account at Negotiation stage — full four-pattern check)
   - Deal-cohort scan (multiple deals — pattern frequency across pipeline)
   - Pre-close structural review (deal at Negotiation — action window open)
   - Closed-deal audit (deal already closed — lower leverage; flag this explicitly)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user reviewing deal structure for a specific deal or cohort
   2. Pull deal structure fields, PS line items, contract terms, and product configuration from HubSpot
   3. Check deal stage — flag immediately if deal is already closed (post-close is lower leverage)
   4. Evaluate all four leakage patterns; quantify estimated ARR impact where possible
   5. Apply G1 — leakage estimates shared beyond RevOps require forecast qualification language
   6. Apply G6 — data-as-of timestamp required on all HubSpot reads
   7. Surface findings with specific pre-close actions while action window is open

3. **EXPERT CHECK**: What would a veteran deal desk analyst verify before surfacing leakage findings?
   - Is the PS ratio benchmark contextualized? A ≤25% PS-to-ACV ratio is a signal, not a rule —
     implementation complexity notes must corroborate before flagging underpricing. Without
     complexity context, the flag is noise, not signal.
   - Is the expansion clause gap specific? "Missing expansion clause" needs the contract term
     length confirmed — flagging a missing expansion right on a 1-year deal is low value; on
     a 3-year deal it's a material ARR growth constraint.
   - Is the ARR classification mismatch actionable before close? Flagging renewal-term / ARR
     classification misalignment only matters if there's time to add a price increase clause —
     confirm with the AE that the contract is not yet countersigned.
   - Is the success milestone gate absence framed as a CS enablement gap, not a CS failure?
     Missing milestone gates hurt expansion motion — the fix is a contract amendment, not a
     coaching conversation.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Running a scan on a closed deal without explicitly flagging the reduced leverage window
   - Surfacing PS underpricing estimates without G1 qualification when output goes to Finance
   - Pulling HubSpot deal data without data-as-of timestamp (G6 violation)
   - Flagging all four patterns as equally urgent — prioritize by estimated ARR impact and
     ease of fix before close

**After execution**, verify:
- G1 qualification present on all leakage estimates shared beyond RevOps
- G6 data-as-of label applied to all HubSpot reads
- Deal stage confirmed — action window status declared (open / closed)
- Leakage findings prioritized by estimated ARR impact
- Confidence: High when HubSpot connected and deal structure fields complete; Moderate when fields missing or deal is post-close

---

## Four Leakage Patterns

```
Pattern 1 — Professional services underpriced
  Signal: implementation_complexity notes suggest high effort;
          PS line item ≤25% of ACV (typical PS ratio for complexity level)
  Impact estimate: [estimated PS underprice amount]

Pattern 2 — Expansion clause missing
  Signal: multi-year contract (≥2 years) without usage-based expansion clause
          or seat-based expansion rights
  Impact: No contractual mechanism to grow ARR within the contract term

Pattern 3 — Renewal terms / ARR classification mismatch
  Signal: deal counted as New ARR but renewal terms allow flat renewal
          with no price increase clause
  Impact: ARR classification may overstate true growth quality

Pattern 4 — Success milestone gate missing
  Signal: no EBR/QBR or milestone-based check-in tied to expansion conversation
  Impact: CS has no contractual trigger for expansion motion
```

---

## Output

```
REVENUE LEAKAGE SCAN — [Account Name] — [Stage]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: Moderate]

Deal: [link]  ACV: $XXXk  Stage: [stage]  Close: [date]

Leakage findings:
  [Pattern type]  Estimated impact: $XXXk  Action: [specific fix before close]
  [Pattern type]  Impact: [structural]      Action: [specific fix]

No leakage patterns detected: [if clean]

Window: [deal is at Negotiation — action window is open / deal is closed — lower leverage]

[DRAFT — RevOps internal]
[G1: Leakage estimates are models. Not revenue commitments.]
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

- G1: Leakage estimates require qualification when shared beyond RevOps
- Most valuable when run at Negotiation stage — flag this explicitly on closed deals
