# rev-ops.closed-won-to-cs-capacity-modeling

Models CSM headroom consumption from closed-won deals. Maps new ARR to CSM pod capacity using UoG pod structure; computes headroom signals (<0% over capacity, 0-10% near ceiling, 10-25% limited, >25% healthy). Output is structural signal only — not a hiring mandate.

## Use it for

- Calculate CSM capacity impact of closed-won deal batch
- Compute headroom signal by pod or segment
- Flag near-ceiling or over-capacity conditions for leadership review
- Feed capacity data into annual-planning-workflow Phase 3

## Don't use it for

- Issuing hiring decisions or headcount requests (G2)
- Territory or quota modeling (separate sub-skills)
- CRM edits

## How to trigger it

Say something like:

- "capacity impact of new deals"
- "CSM headroom after close"
- "closed-won capacity modeling"
- "how much capacity do these deals consume"

## What you get

- Headroom signal report by pod/segment (Markdown)
- Capacity summary table

## Prerequisites

- Closed-won deal list with ARR values
- Current CSM pod structure and headroom baseline (from UoG)

## Governance

- {'G2': 'capacity outputs are structural signals, not hiring mandates'}
- {'G1': 'ARR figures flagged [review — not yet a revenue commitment]'}

## See also

- rev-ops.unit-of-growth-calculator
- rev-ops.annual-planning-workflow
- rev-ops.mid-year-replan-triggering

---

*Domain: `rev-ops` · Skill ID: `rev-ops.closed-won-to-cs-capacity-modeling`*
