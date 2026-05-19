# rev-ops.discount-threshold-monitoring

Monitors deal discounts against configured thresholds and routes approval requirements to the correct tier (standard/elevated/executive). Creates Linear issues for elevated and executive approvals. Never approves discounts autonomously. Sub-component of deal-desk-workflow-management.

## Use it for

- Compare deal discount to standard/elevated/executive threshold tiers
- Identify which approval tier is required
- Create Linear issue for elevated or executive approval tracking
- Surface discount pattern trends across pipeline (when scoped to team/period)

## Don't use it for

- Approving discounts autonomously
- Full deal desk routing (use deal-desk-workflow-management for full workflow)
- CRM record edits (G9)

## How to trigger it

Say something like:

- "discount approval"
- "is this discount within threshold"
- "discount monitoring"
- "discount threshold check"

## What you get

- Threshold comparison result with approval tier (Markdown)
- Linear issue for elevated/executive approval (Write-tier)

## Prerequisites

- Discount threshold configuration by tier (from domain CLAUDE.md)
- Deal ARR and proposed discount

## Governance

- {'G1': 'ARR figures flagged [review — not yet a revenue commitment]'}
- Never approves discounts; routes only

## See also

- rev-ops.deal-desk-workflow-management
- rev-ops.non-standard-terms-detection

---

*Domain: `rev-ops` · Skill ID: `rev-ops.discount-threshold-monitoring`*
