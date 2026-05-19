---
name: discount-threshold-monitoring
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Flags deals where discount exceeds the approved threshold for that segment. Routes approval to the correct authority based on discount depth using thresholds from company profile. Tracks discount frequency by rep and segment. Never approves deals autonomously. Triggers: 'discount approval', 'discount threshold', 'discount frequency by rep', 'is this discount approved', 'flag a discount'."
---

[PROPOSED]

# Discount Threshold Monitoring

Threshold-based routing — not subjective review. The approval tier is determined
by the discount depth against company profile thresholds.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
`discount_executive_threshold_pct`, `linear_connected`,
`cs_expansion_discount_standard_threshold_pct` (optional — defaults to Sales threshold if absent),
`cs_expansion_discount_elevated_threshold_pct` (optional — defaults to Sales elevated threshold if absent)

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
`discount_executive_threshold_pct`, `linear_connected`,
`cs_expansion_discount_standard_threshold_pct`, `cs_expansion_discount_elevated_threshold_pct`

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Use when
- Deal discount needs to be evaluated against configured thresholds to determine approval tier — applies to both Sales new-logo deals and CS-originated expansion deals
- User needs to know which approval authority a deal requires based on discount level
- Discount pattern monitoring across deals, reps, or CSMs is needed

## Application context
This skill covers two distinct deal flows with potentially separate threshold configs:
- **Sales new-logo deals:** Standard approval chain — AE manager → RevOps lead → CRO → CRO + Finance
- **CS expansion deals:** CS-specific approval chain — CS manager → CS leader → CRO. Thresholds may differ from new-logo thresholds and are configured separately via `cs_expansion_discount_*_threshold_pct`. If CS-specific thresholds are not configured, defaults to Sales thresholds.

Discount pattern monitoring tracks both Sales reps and CSMs on the same trailing-90-day basis.

## Do NOT use for
- Full deal desk routing and tracking (use deal-desk-workflow-management)
- Discount negotiation decisions (output is analytical input only)
- Revenue leakage structural analysis (use revenue-leakage-scanning)

## Typical Activation
"Discount threshold check", "which tier does this deal require", "discount monitoring", "is this discount within policy", "discount level for [deal]"

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of discount monitoring request is this?
   - Single deal threshold check (one opportunity — tier determination + required approver)
   - Discount pattern monitoring (rep or CSM trailing-90-day frequency report)
   - Approval routing (above-threshold deal — Linear issue creation + SLA assignment)
   - CS expansion deal check (CS-specific threshold chain vs. Sales thresholds)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user flagging a discount or requesting discount review
   2. Read configured thresholds from company profile — never estimate thresholds
   3. Determine deal type (Sales new-logo vs. CS expansion) before applying threshold chain
   4. Apply G1 — discount approval does not constitute revenue commitment
   5. Apply G6 — data-as-of on all HubSpot reads
   6. Create Linear issue for above-threshold deals only — Write-tier, confirm before creating
   7. Never approve deals autonomously

3. **EXPERT CHECK**: What would a veteran RevOps analyst verify first?
   - Are configured thresholds from the company profile, not estimated? Hardcoded
     thresholds drift from policy — always read from config before routing.
   - Is the deal type correctly identified before applying thresholds? CS expansion deals
     may have separate cs_expansion_* thresholds — misapplying Sales thresholds to CS
     deals routes to the wrong approver chain.
   - Is the SLA window correct for time of quarter? Standard SLA is 24h; final 2 weeks
     of quarter is 4h — a wrong SLA assignment at quarter-end misses the close window.
   - Is the discount frequency report scoped to trailing 90 days? Wider windows
     dilute pattern signals; narrower windows miss rep behavior trends.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Using estimated or hardcoded thresholds instead of configured company profile values (G1 violation)
   - Applying Sales new-logo threshold chain to CS expansion deals when cs_expansion_* config exists
   - Creating a Linear issue without Write-tier confirmation (G9 violation)
   - Surfacing HubSpot reads without data-as-of timestamp (G6 violation)

**After execution**, verify:
- G1 qualifier present: discount approval does not lock revenue or constitute a commitment
- G6 data-as-of label applied to all HubSpot reads
- Deal type (Sales vs. CS expansion) declared; correct threshold chain applied
- Confidence: High when HubSpot is connected and company profile thresholds are configured; Moderate when thresholds are defaulted from Sales config due to absent CS-specific config
    - Confidence: [High] when HubSpot is connected and company profile thresholds are configured / [Medium] when thresholds are defaulted from Sales config due to absent CS-specific config / [Low] if all inputs are manual or unverified

---

## Approval Routing

```
SALES NEW-LOGO DEALS (use discount_*_threshold_pct):
  ≤ discount_standard_threshold_pct    → AE manager sign-off (log in CRM)
  > standard, ≤ elevated threshold     → RevOps lead approval
  > elevated, ≤ executive threshold    → CRO sign-off
  > executive threshold                → CRO + Finance dual approval

CS EXPANSION DEALS (use cs_expansion_discount_*_threshold_pct if configured,
                   else fall back to Sales thresholds):
  ≤ cs_expansion_standard_threshold   → CS manager sign-off (log in CRM)
  > standard, ≤ elevated threshold    → CS leader approval
  > elevated, ≤ executive threshold   → CRO sign-off
  > executive threshold               → CRO + Finance dual approval

SLA:
  Standard quarter: 24-hour SLA
  Final 2 weeks of quarter: 4-hour SLA
  SLA breach → escalate to #revops-ops
```

---

## Output

```
DISCOUNT FLAG — [Account Name]
[HubSpot ✓ live — as of YYYY-MM-DD]

Deal: [link]  ACV: $XXXk  Proposed discount: XX%
Threshold crossed: [Standard / Elevated / Executive]
Required approver: [Role]  SLA: [N] hours

Linear issue: [created #N / confirm to create]

Rep discount frequency (trailing 90 days):
  [Rep name]: [N] discounts, avg XX%, [N] above threshold
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
**Data sensitivity:** Inputs may contain confidential deal, customer, and revenue data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- Never approve autonomously
- G1: Discount approval does not lock revenue
- Write-tier: Linear issue requires confirmation before creation
