---
name: revenue-leakage-scanning
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Identifies deal structures leaving money on the table before close: underpriced professional services, missing expansion clauses in multi-year deals, renewal terms misaligned with ARR classification, missing success milestone gates for expansion. Fires at Negotiation stage — before close locks the structure. Triggers: 'revenue leakage', 'missing expansion clause', 'mispriced services', 'deal structure review', 'are we leaving money on the table'."
---

# Revenue Leakage Scanning

Structural leakage is easier to fix before the contract is signed.
Primary detection window: Negotiation stage — before close.

**Reference:** Confidence bands → `../../../shared/revops-domain-model.md §2`
**Config reads:** `avg_deal_acv`, `primary_segment`

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

1. Confirm activation — user reviewing deal structure for a specific deal or cohort
2. Read deal structure fields, notes, and product configuration from HubSpot
3. Identify leakage patterns — quantify estimated ARR impact where possible
4. Apply G1 — leakage analysis for finance requires qualification language
5. Surface findings before close; note if deal is already closed (post-close is lower value)

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

## Output Format

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
