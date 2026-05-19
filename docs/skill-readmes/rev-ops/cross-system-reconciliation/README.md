# rev-ops.cross-system-reconciliation

Reconciles ARR, account, and pipeline data across CRM, Finance sheets, CS platform, and billing systems using the data authority hierarchy (HubSpot > Finance Sheets > CS platform > Slack/Linear). Surfaces discrepancies with delta magnitude and recommended resolution path. Never overwrites source systems autonomously.

## Use it for

- Reconcile ARR figures across CRM and Finance sheets
- Surface account record discrepancies between CRM and CS platform
- Identify pipeline count or stage mismatches across systems
- Flag which system holds authoritative value per data authority hierarchy

## Don't use it for

- Overwriting source systems (G9)
- Forecasting or pipeline coverage analysis (separate skills)
- Territory or quota data (use planning sub-skills)

## How to trigger it

Say something like:

- "reconcile the data"
- "CRM vs Finance discrepancy"
- "cross-system reconciliation"
- "why don't the numbers match"
- "systems out of sync"

## What you get

- Discrepancy report with delta magnitudes and authority resolution (Markdown)

## Prerequisites

- {'Access to at least two of': 'CRM, Finance sheets, CS platform, billing'}
- Data authority hierarchy configuration (from domain CLAUDE.md)

## Governance

- {'G6': 'data-as-of timestamp on all reads'}
- {'G9': 'no autonomous system writes; discrepancies are flagged, not corrected'}
- Data authority hierarchy must be applied; HubSpot wins on conflict unless Finance has override

## See also

- rev-ops.crm-hygiene-audit
- rev-ops.data-decay-tracking
- rev-ops.field-completion-monitoring

---

*Domain: `rev-ops` · Skill ID: `rev-ops.cross-system-reconciliation`*
