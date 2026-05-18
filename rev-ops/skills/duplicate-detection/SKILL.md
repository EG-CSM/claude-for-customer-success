---
name: duplicate-detection
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Identifies duplicate accounts, contacts, and opportunities in HubSpot. Produces merge candidates with confidence scores (High/Medium/Low). Never merges autonomously — all merges require Write-tier human confirmation. Triggers: 'duplicates', 'merge candidates', 'duplicate accounts', 'duplicate contacts', 'clean up CRM duplicates'."
---

# Duplicate Detection

Merge candidates with confidence scores. High-confidence duplicates batch-
presented for bulk approval. No autonomous merges — ever.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `crm_system`

---

## Use when
- CRM contacts, companies, or deals need duplicate scanning before a data import or merge
- Duplicate records are suspected to be inflating pipeline or distorting metrics
- Data hygiene sprint includes deduplication as a required step

## Do NOT use for
- Full CRM hygiene audit (use crm-hygiene-audit)
- Field completion monitoring (use field-completion-monitoring)
- Merging records autonomously (outputs are proposals — G9 applies)

## Typical activation
"Find duplicates", "duplicate detection", "deduplicate the CRM", "flag duplicate contacts/companies", "duplicate scan before import"

---

## Reasoning Protocol

1. Confirm activation — user requesting duplicate detection or merge candidates
2. Check HubSpot — read access to accounts, contacts, opportunities required
3. Apply G6 — data-as-of on all reads
4. Apply governance Write-tier — merges require human confirmation
5. Confirm object scope: accounts / contacts / opportunities / all

---

## Matching Criteria

**Accounts:**
- Domain match (company email domain)
- Company name similarity >85% (fuzzy match)
- Same billing address

**Contacts:**
- Email address match (exact)
- First + last name + company match
- LinkedIn URL match (if field populated)

**Opportunities:**
- Same account + same product + close date within 30 days + ACV within 20%

---

## Confidence Scoring

- **High** — 2+ matching signals, no conflicting signals
- **Medium** — 1 strong signal, some field differences that may be legitimate
- **Low** — Partial match; requires human judgment before any action

---

## Output Format

```
DUPLICATE DETECTION — [Object type] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

HIGH confidence merge candidates ([N] pairs):
  [Company A] ←→ [Company A Inc]  Signals: domain match + name match
  [Contact X] ←→ [Contact X]      Signals: email match + LinkedIn match
  → Batch approval: confirm to queue all High for merge

MEDIUM confidence ([N] pairs):
  [Company B] ←→ [Company B Ltd]  Signals: name match | Diff: billing address
  → Review individually before merging

LOW confidence ([N] pairs):
  [Contact Y] ←→ [Contact Z]      Signal: name similarity only
  → Human judgment required

[Write-tier: All merges require human confirmation before execution]
[No autonomous merges will be performed]
```

---

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential customer, deal, and operational data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G9: No autonomous merges — always proposals
- G6: Data-as-of required
