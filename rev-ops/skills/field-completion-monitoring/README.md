# rev-ops.field-completion-monitoring

Monitors CRM field completion at four stage gate transitions. Escalates pre-close for Negotiation-stage deals with incomplete required fields within 2 weeks of quarter close. All findings are proposals (G9). Feeds into crm-hygiene-audit field-completion dimension.

## Use it for

- Check field completion against stage-gate requirements
- Identify incomplete required fields blocking stage advancement
- Escalate pre-close incomplete Negotiation+ deals near quarter close
- Feed field-completion score into crm-hygiene-audit

## Don't use it for

- Updating CRM fields autonomously (G9)
- Full hygiene audit (use crm-hygiene-audit)

## How to trigger it

Say something like:

- "field completion"
- "required fields missing"
- "stage gate fields"
- "CRM fields incomplete"
- "field completion check"

## What you get

- Field completion gap report by stage and owner (Markdown)
- Pre-close escalation list for Negotiation+ deals

## Prerequisites

- Required fields per stage gate (from domain CLAUDE.md)
- CRM data access
- Quarter-close date for pre-close escalation window

## Governance

- {'G6': 'data-as-of timestamp on all CRM reads'}
- {'G7': 'escalation path on pre-close incomplete deals'}
- {'G9': 'no autonomous CRM edits'}

## See also

- rev-ops.crm-hygiene-audit
- rev-ops.stage-integrity-audit

---

*Domain: `rev-ops` · Skill ID: `rev-ops.field-completion-monitoring`*
