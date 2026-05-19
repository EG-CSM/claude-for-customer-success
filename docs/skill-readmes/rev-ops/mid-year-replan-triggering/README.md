# rev-ops.mid-year-replan-triggering

Monitors four trigger conditions and produces a replan memo when any fires: ARR drift >15% from UoG baseline, CS headroom <10%, AE attainment shortfall >20pp for ≥2 consecutive months, or territory disruption event. Produces the memo only — not the replan itself. Routes memo to RevOps lead.

## Use it for

- Monitor the four replan trigger conditions
- Produce replan trigger memo when any condition fires
- Route memo to RevOps lead for go/no-go on replan
- Coordinate with growth-model-vs-actuals-tracking for ARR drift trigger

## Don't use it for

- Executing the replan itself (requires human-led process)
- Annual planning workflow (use annual-planning-workflow)
- CRM edits (G9)

## How to trigger it

Say something like:

- "mid-year replan"
- "trigger replan"
- "do we need to replan"
- "replan trigger check"
- "are we off track enough to replan"

## What you get

- Replan trigger memo with condition(s) fired and evidence (Markdown)

## Prerequisites

- UoG baseline and current actuals (for ARR drift trigger)
- CS headroom current state
- AE attainment by rep for 2-month window
- Territory disruption event description if applicable

## Governance

- {'G1': 'all ARR figures flagged [review — not yet a revenue commitment]'}
- {'G2': 'capacity signals are structural; not hiring mandates'}
- Memo only; replan execution is human-led

## See also

- rev-ops.growth-model-vs-actuals-tracking
- rev-ops.annual-planning-workflow
- rev-ops.closed-won-to-cs-capacity-modeling

---

*Domain: `rev-ops` · Skill ID: `rev-ops.mid-year-replan-triggering`*
