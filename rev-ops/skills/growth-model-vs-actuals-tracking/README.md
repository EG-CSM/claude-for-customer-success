# rev-ops.growth-model-vs-actuals-tracking

Tracks actuals against the Unit of Growth (UoG) baseline across three vectors: new logo ARR (threshold >15% drift), NRR (>5pp), and GRR (>3pp). When any threshold fires, produces a variance memo and routes to mid-year-replan-triggering. Reporting-mode only when UoG baseline is absent.

## Use it for

- Compare period actuals to UoG baseline on three vectors
- Fire variance memo when drift threshold exceeded on any vector
- Route to mid-year-replan-triggering on threshold breach
- Produce growth tracking report for RevOps lead review

## Don't use it for

- Building the UoG baseline (use unit-of-growth-calculator)
- Executing the replan (routes to mid-year-replan-triggering, which produces memo only)
- CRM edits (G9)

## How to trigger it

Say something like:

- "growth model tracking"
- "actuals vs growth model"
- "are we on track to the plan"
- "growth model variance"
- "UoG drift check"

## What you get

- Growth tracking report with vector-level delta (Markdown)
- Variance memo when threshold fires

## Prerequisites

- UoG baseline by vector (new logo ARR, NRR, GRR)
- Period actuals from CRM and Finance sheets

## Governance

- {'G1': 'all ARR figures flagged [review — not yet a revenue commitment]'}
- {'G6': 'data-as-of timestamp on all reads'}
- Reporting-mode only when UoG baseline absent; disclose limitation

## See also

- rev-ops.unit-of-growth-calculator
- rev-ops.mid-year-replan-triggering
- rev-ops.annual-planning-workflow

---

*Domain: `rev-ops` · Skill ID: `rev-ops.growth-model-vs-actuals-tracking`*
