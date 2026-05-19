# rev-ops.comp-simulation

Models CSM and AE compensation plan outcomes against real or projected portfolio and pipeline data. Calculates attainment, payout, and acceleration tier projections under current and proposed plan structures. Outputs require HR and Finance dual review before distribution to reps (G3).

## Use it for

- Project individual rep payout under current quota and commission structure
- Compare payout outcomes across two or more comp plan variants
- Model impact of quota changes, accelerator threshold shifts, or kicker additions
- Identify plan design anomalies (cliff risk, attainment bunching, unintended upside)

## Don't use it for

- Comp plan design decisions (advisory modeling only — HR and Finance own plan design)
- Payroll processing or authoritative payout calculation
- New logo / AE quota setting (contacts rev-ops for pipeline segmentation first)

## How to trigger it

Say something like:

- "model comp outcomes"
- "comp simulation"
- "what would reps earn under this plan"
- "compare comp plan variants"
- "attainment projection"
- "accelerator modeling"

## What you get

- Comp simulation report (structured markdown)
- Attainment and payout table by rep or segment
- Plan variant comparison (if multiple plans modeled)

## Prerequisites

- Domain CLAUDE.md (reads at startup; routes to cold-start-interview if missing)
- {'Current comp plan structure': 'quota, base rate, tiers, accelerators, kickers'}
- {'Portfolio or pipeline data': 'ARR, renewal rates, expansion pipeline'}
- Rep name(s) or segment scope (or "all CSMs" / "all AEs")

## Governance

**Approval required** — output must be reviewed before distribution.
- {'G3': 'comp outputs require HR + Finance dual review before rep distribution'}
- {'G6': 'all data reads must surface data-as-of timestamp'}
- {'G1': 'outputs labeled as modeling scenarios, not authoritative payout figures'}

## See also

- rev-ops.forecast-variance-analysis
- rev-ops.growth-model-vs-actuals-tracking
- rev-ops.deal-classification

---

*Domain: `rev-ops` · Skill ID: `rev-ops.comp-simulation`*
