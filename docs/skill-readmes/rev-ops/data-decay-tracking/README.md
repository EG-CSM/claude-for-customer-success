# rev-ops.data-decay-tracking

Tracks staleness of account, contact, and opportunity records against configurable decay thresholds. Produces a decay report ranked by staleness severity. Integrates into crm-hygiene-audit as a sub-dimension. All output is read-only; no autonomous CRM writes (G9).

## Use it for

- Identify accounts or contacts not updated within decay threshold
- Rank records by staleness severity
- Surface decay patterns by team, segment, or owner
- Feed decay dimension into crm-hygiene-audit composite score

## Don't use it for

- Updating or correcting stale records (G9)
- Full CRM audit (use crm-hygiene-audit for composite view)

## How to trigger it

Say something like:

- "stale records"
- "data decay"
- "accounts not updated"
- "contact decay report"
- "what data is going stale"

## What you get

- Decay report ranked by staleness (Markdown)

## Prerequisites

- CRM data access
- Decay threshold configuration (from domain CLAUDE.md or argument)

## Governance

- {'G6': 'data-as-of timestamp on all reads'}
- {'G9': 'no autonomous CRM edits'}

## See also

- rev-ops.crm-hygiene-audit
- rev-ops.cross-system-reconciliation
- rev-ops.field-completion-monitoring

---

*Domain: `rev-ops` · Skill ID: `rev-ops.data-decay-tracking`*
