# rev-ops.duplicate-detection

Detects duplicate accounts, contacts, and opportunities using multi-signal matching. Assigns confidence scores (High: 2+ signals no conflict, Medium: 1 strong signal with differences, Low: partial match). Never merges records autonomously (G9); all findings are proposals for human review.

## Use it for

- Identify duplicate account, contact, or opportunity records in CRM
- Score confidence of each duplicate match
- Produce merge candidate report for human review
- Feed duplicate dimension into crm-hygiene-audit

## Don't use it for

- Merging or deleting records autonomously (G9)
- Full CRM hygiene audit (use crm-hygiene-audit)

## How to trigger it

Say something like:

- "duplicate accounts"
- "duplicate contacts"
- "find duplicates"
- "deduplication"
- "duplicate detection"

## What you get

- Duplicate candidate report with confidence scores (Markdown)

## Prerequisites

- CRM data access (HubSpot preferred)
- Matching signal configuration (domain, name similarity, email, phone)

## Governance

- {'G6': 'data-as-of timestamp on all CRM reads'}
- {'G9': 'no autonomous record merges or deletes'}

## See also

- rev-ops.crm-hygiene-audit
- rev-ops.cross-system-reconciliation

---

*Domain: `rev-ops` · Skill ID: `rev-ops.duplicate-detection`*
