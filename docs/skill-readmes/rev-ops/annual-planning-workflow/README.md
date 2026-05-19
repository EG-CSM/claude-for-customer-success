# rev-ops.annual-planning-workflow

Orchestrates the 7-phase annual GTM planning cycle — from scope setup through board ratification. Coordinates scenario-modeling, quota-sensitivity-analysis, unit-of-growth-calculator, and revenue-brief-generation as sub-agents. Each phase has a named human approval gate; the skill never advances past a gate without explicit user confirmation.

## Use it for

- Orchestrate the full annual planning cycle end-to-end
- Coordinate sub-agent calls (scenario, quota, UoG, territory, revenue-brief)
- Present phase deliverables and gate approval prompts to RevOps lead
- Route midcycle replans when drift triggers fire

## Don't use it for

- Executing individual sub-agent tasks directly (delegates to sub-skills)
- Issuing hiring decisions or comp changes (output is proposals only)
- CRM edits of any kind

## How to trigger it

Say something like:

- "annual planning"
- "GTM planning cycle"
- "run the planning process"
- "fiscal year planning"
- "start planning workflow"

## What you get

- Phase-gated planning memo per phase (Markdown)
- Final annual plan document pending board ratification

## Prerequisites

- Prior-year ARR actuals and growth rates
- Current pipeline snapshot (for scenario inputs)
- Headcount and pod structure for UoG calculation

## Governance

**Approval required** — output must be reviewed before distribution.
- {'G1': 'all ARR/revenue figures flagged [review — not yet a revenue commitment]'}
- {'G2': 'capacity outputs are structural signals, not hiring mandates'}
- {'G3': 'comp model proposals require HR + Finance dual review'}
- {'G4': 'territory outputs require RevOps lead + Sales lead dual confirmation'}
- Every phase gate requires explicit human approval before advancing

## See also

- rev-ops.mid-year-replan-triggering
- rev-ops.scenario-modeling
- rev-ops.quota-sensitivity-analysis
- rev-ops.unit-of-growth-calculator

---

*Domain: `rev-ops` · Skill ID: `rev-ops.annual-planning-workflow`*
