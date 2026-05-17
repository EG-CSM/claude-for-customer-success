---
name: data-decay-tracking
version: 1.0.0
description: "Monitors contact and account data freshness. Flags records where title, company, or contact data has likely changed and enrichment is overdue. Decay signals: contact title unchanged >18 months, account employee count stale >12 months, primary contact no email activity >6 months, account domain change detected. Prioritizes enterprise accounts. Triggers: 'stale contacts', 'data decay', 'enrichment needed', 'contact freshness', 'stale account data'."
---

# Data Decay Tracking

Data decay is the slow death of CRM quality. Contacts leave roles. Companies
get acquired. Enrichment overdue means signals are built on wrong data.

**Reference:** Confidence bands → `reference/revops-domain-model.md §2`
**Config reads:** `primary_segment`, `crm_system`

---

## Reasoning Protocol

1. Confirm activation — user requesting freshness review or enrichment candidates
2. Check HubSpot contact and account data; declare fallback if unavailable
3. Apply G6 — stale data must be labeled; decay findings are themselves evidence of staleness
4. Prioritize enterprise tier accounts in output
5. No autonomous enrichment calls — flag candidates for human action

---

## Four Decay Signals

```
Signal 1: Contact title unchanged >18 months (avg B2B tenure)
Signal 2: Account employee count not updated >12 months
Signal 3: Primary contact — no email activity >6 months (possible departure)
Signal 4: Account domain change detected (acquisition or rebrand)
```

---

## Output Format

```
DATA DECAY REPORT — [Tier/Scope] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

Enterprise accounts — enrichment overdue:
Account         Signal                              Last updated   Priority
[Company A]     Domain change detected              14 months ago  HIGH
[Company B]     Champion title unchanged 22 months  22 months ago  MEDIUM
[Company C]     Primary contact no activity 7mo     7 months ago   MEDIUM

Mid-Market accounts — enrichment overdue: [N] accounts

All accounts summary:
  Total flagged:      [N] accounts
  High priority:      [N]  (domain change or champion likely departed)
  Medium priority:    [N]  (title/count stale)

Recommended action: Enrich [N] high-priority accounts before next QBR cycle.
Enrichment tool: [user's configured enrichment source if available, else manual]

[No autonomous enrichment calls will be made]
[Write-tier: Contact/account updates require human confirmation]
```

---

## Guardrails

- G6: Decay report outputs themselves note staleness risk on every flagged record
- G9: No autonomous enrichment API calls
