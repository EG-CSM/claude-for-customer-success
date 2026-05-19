# rev-ops.next-best-action-recommendation

Matches deal-health-scoring sub-50 signals to five intervention types (re-engagement, executive sponsor introduction, competitive displacement, pricing restructure, champion activation). Every recommendation includes what/who/why. Routes applicable flags to csm:risk-flag cross-plugin handoff. Output is guidance only (G5); escalation path required (G7).

## Use it for

- Receive deal health signals (sub-50 scores) and identify best intervention
- Match intervention type to signal pattern
- Produce structured recommendation with what/who/why for each deal
- Route CS-relevant flags to csm:risk-flag

## Don't use it for

- Executing interventions autonomously
- Deal health scoring (upstream — use deal-health-scoring)
- CRM edits (G9)

## How to trigger it

Say something like:

- "next best action"
- "what should we do with this deal"
- "intervention recommendation"
- "at-risk deal playbook"
- "deal recovery"

## What you get

- Next-best-action recommendation per deal with what/who/why (Markdown)

## Prerequisites

- Deal health scores (from deal-health-scoring output)
- {'Deal context': 'stage, stakeholders, competitive flags'}

## Governance

- {'G5': 'recommendations are guidance, not directives'}
- {'G7': 'escalation path present on all risk-flagged deals'}
- Never executes interventions autonomously

## See also

- rev-ops.deal-health-scoring
- csm.risk-flag
- rev-ops.pipeline-velocity-tracking

---

*Domain: `rev-ops` · Skill ID: `rev-ops.next-best-action-recommendation`*
