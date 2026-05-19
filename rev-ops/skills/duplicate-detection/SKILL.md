---
name: duplicate-detection
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Identifies duplicate accounts, contacts, and opportunities in HubSpot. Produces merge candidates with confidence scores (High/Medium/Low). Never merges autonomously — all merges require Write-tier human confirmation. Triggers: 'duplicates', 'merge candidates', 'duplicate accounts', 'duplicate contacts', 'clean up CRM duplicates'."
---

[PROPOSED]

# Duplicate Detection

Merge candidates with confidence scores. High-confidence duplicates batch-
presented for bulk approval. No autonomous merges — ever.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `crm_system`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `crm_system`

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

Before generating output, apply these primers:

1. **CLASSIFY**: What type of duplicate detection request is this?
   - Single object scan (accounts, contacts, or opportunities — merge candidates for one object type)
   - Multi-object sweep (full CRM across all three object types)
   - Pre-import deduplication (scan before data load — flag conflicts before they enter CRM)
   - Merge candidate review (user reviewing previously surfaced candidates — confirm or dismiss)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting duplicate detection or merge candidates
   2. Check HubSpot connector — read access to accounts, contacts, opportunities required; declare fallback if absent
   3. Confirm object scope before pulling data: accounts / contacts / opportunities / all
   4. Apply G6 — data-as-of on all HubSpot reads
   5. Apply G9 — no autonomous merges; all merge actions require explicit Write-tier human confirmation
   6. Present High-confidence candidates in batch approval format; Medium and Low require individual review

3. **EXPERT CHECK**: What would a veteran RevOps data hygiene analyst verify first?
   - Is the matching signal quality sufficient for the confidence tier assigned? A single
     name-similarity match without corroborating signals should never reach High confidence —
     over-confident scoring causes legitimate record merges.
   - Is data freshness confirmed before scoring? Stale connector reads may miss recent
     record updates that resolve apparent duplicates — declare data age before presenting candidates.
   - Are High-confidence candidates reviewed for merge risk before batch approval? Even
     High-confidence pairs can carry legitimate differences (e.g., separate subsidiaries with
     similar names) — surface any anomalies before queuing for bulk merge.
   - Is the object scope confirmed before running? A full multi-object sweep on a large CRM
     may return partial data — scope the scan and declare any data limits upfront.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Merging records autonomously without Write-tier human confirmation (G9 violation)
   - Surfacing HubSpot reads without data-as-of timestamp (G6 violation)
   - Assigning High confidence based on a single matching signal without corroboration
   - Running a multi-object sweep without declaring scope and data volume limits

**After execution**, verify:
- G6 data-as-of label applied to all HubSpot reads
- G9 Write-tier qualifier present: all merges require explicit human confirmation before execution
- Confidence tier (High/Medium/Low) correctly assigned per matching signal count and quality
- Confidence: High when HubSpot is connected and data is current; Moderate when data is stale or connector is unavailable

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

## Output

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

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

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
