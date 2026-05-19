# rev-ops.quota-sensitivity-analysis

Builds quota models from UoG-confirmed AE headcount and revenue target. Models structural achievability at five attainment levels (50/65/75/85/100%). Flags when hitting plan requires attainment above the 75th percentile of historical actuals. Used inside annual-planning-workflow Phase 4 or standalone.

## Use it for

- Model per-rep quota from UoG output and revenue target
- Surface attainment scenarios and their ARR outcomes
- Flag structurally challenging quotas as risk disclosure for leadership

## Don't use it for

- Setting or approving quota (G2 — structural input; leadership decides)
- Changing OTE or comp structure without HR + Finance dual review (G3)

## How to trigger it

Say something like:

- "quota model"
- "is quota achievable"
- "quota sensitivity"
- "quota attainment model"
- "what does quota need to be"

## What you get

- Quota sensitivity table (five attainment levels × ARR outcomes)
- Structural achievability flag with KBCM median citation

## Prerequisites

- UoG-confirmed AE count and revenue target (from annual-planning-workflow Phase 2 or practice profile)
- ae_quota from practice profile
- Historical attainment actuals (trailing 4Q) for achievability flag

## Governance

**Approval required** — output must be reviewed before distribution.
- G1 — revenue projections require forecast qualification language
- G2 — quota output is structural input; decisions require leadership approval
- G3 — if output changes OTE/comp, HR + Finance dual review required
- Structural achievability flag is risk disclosure, not quota rejection

## See also

- rev-ops.annual-planning-workflow
- rev-ops.unit-of-growth-calculator
- rev-ops.scenario-modeling

---

*Domain: `rev-ops` · Skill ID: `rev-ops.quota-sensitivity-analysis`*
