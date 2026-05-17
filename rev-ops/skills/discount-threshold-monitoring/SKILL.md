---
name: discount-threshold-monitoring
version: 1.0.0
description: "Flags deals where discount exceeds the approved threshold for that segment. Routes approval to the correct authority based on discount depth using thresholds from practice profile. Tracks discount frequency by rep and segment. Never approves deals autonomously. Triggers: 'discount approval', 'discount threshold', 'discount frequency by rep', 'is this discount approved', 'flag a discount'."
---

# Discount Threshold Monitoring

Threshold-based routing — not subjective review. The approval tier is determined
by the discount depth against practice profile thresholds.

**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `discount_standard_threshold_pct`, `discount_elevated_threshold_pct`,
`discount_executive_threshold_pct`, `linear_connected`

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
Discount depth (from practice profile):
  ≤ discount_standard_threshold_pct    → AE manager sign-off (log in CRM)
  > standard, ≤ elevated threshold     → RevOps lead approval
  > elevated, ≤ executive threshold    → CRO sign-off
  > executive threshold                → CRO + Finance dual approval

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

## Guardrails

- Never approve autonomously
- G1: Discount approval does not lock revenue
- Write-tier: Linear issue requires confirmation before creation
