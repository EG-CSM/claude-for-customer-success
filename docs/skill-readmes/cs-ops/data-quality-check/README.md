# cs-ops.data-quality-check

Audits CRM and CS Platform data quality across completeness, staleness, and consistency dimensions. Produces a field-level scorecard and prioritized remediation backlog. Never writes to source systems — all fixes are proposals.

## Use it for

- Weekly or monthly data quality audit
- Pre-QBR data hygiene check
- Field-specific completeness investigation
- Identifying data inconsistencies across systems

## Don't use it for

- Applying corrections autonomously
- CRM structural changes or field definitions

## How to trigger it

Say something like:

- "data quality"
- "CRM hygiene"
- "missing fields"
- "stale data"
- "data audit"

## What you get

- Field-level quality scorecard
- Remediation backlog (proposals only)

## Prerequisites

- cs-ops CLAUDE.md

## Governance

- Read-only — no autonomous writes to CRM or CS Platform

## See also

- rev-ops.crm-hygiene-audit
- rev-ops.duplicate-detection

---

*Domain: `cs-ops` · Skill ID: `cs-ops.data-quality-check`*
