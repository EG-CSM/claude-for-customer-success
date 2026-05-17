---
name: duplicate-detection
version: 1.0.0
description: "Identifies duplicate accounts, contacts, and opportunities in HubSpot. Produces merge candidates with confidence scores (High/Medium/Low). Never merges autonomously — all merges require Write-tier human confirmation. Triggers: 'duplicates', 'merge candidates', 'duplicate accounts', 'duplicate contacts', 'clean up CRM duplicates'."
---

# Duplicate Detection

Merge candidates with confidence scores. High-confidence duplicates batch-
presented for bulk approval. No autonomous merges — ever.

**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `crm_system`

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

## Guardrails

- G9: No autonomous merges — always proposals
- G6: Data-as-of required
