---
name: discount-threshold-monitoring
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Flags deals where discount exceeds the approved threshold for that segment. Routes approval to the correct authority based on discount depth using thresholds from practice profile. Tracks discount frequency by rep and segment. Never approves deals autonomously. Triggers: 'discount approval', 'discount threshold', 'discount frequency by rep', 'is this discount approved', 'flag a discount'."
---

# Discount Threshold Monitoring

Threshold-based routing — not subjective review. The approval tier is determined
by the discount depth against practice profile thresholds.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
`discount_executive_threshold_pct`, `linear_connected`,
`cs_expansion_discount_standard_threshold_pct` (optional — defaults to Sales threshold if absent),
`cs_expansion_discount_elevated_threshold_pct` (optional — defaults to Sales elevated threshold if absent)

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

## Typical activation
"Discount threshold check", "which tier does this deal require", "discount monitoring", "is this discount within policy", "discount level for [deal]"

---

## Reasoning Protocol

1. Confirm activation — user flagging a discount or requesting discount review
2. Read discount thresholds from practice profile
3. Determine approval tier from discount depth
4. Apply G1 — discount approval does not constitute revenue commitment
5. Create Linear issue for above-threshold deals (Write-tier — confirm before creating)
6. Never approve deals autonomously

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

## Output Format

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
