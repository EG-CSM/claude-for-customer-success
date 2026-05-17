---
name: field-completion-monitoring
version: 1.0.0
description: "Tracks required field completion rates by rep and deal stage gate. Flags missing data that will break downstream forecasting before quarter close. Escalates deals in Negotiation+ with missing gate fields 2 weeks before quarter close. Triggers: 'missing fields', 'field completion', 'gate fields', 'pre-quarter-close hygiene', 'what fields are missing'."
---

# Field Completion Monitoring

Stage gate field enforcement. Most important skill for forecast accuracy —
missing gate fields are the primary cause of forecast surprises.

**Reference:** Handoff quality scoring → `reference/revops-domain-model.md §10`
**Config reads:** `crm_system`, `primary_segment`

---

## Reasoning Protocol

1. Confirm activation — user requesting field completion check or pre-close hygiene
2. Check HubSpot — field reads required; declare fallback if unavailable
3. Apply G6 — data-as-of required
4. For quarter-close escalations: confirm escalation path and owner (G7)
5. Write-tier for any CRM field updates — proposals only

---

## Stage Gate Fields

```
Discovery → Qualification:
  company_size, segment, primary_use_case, economic_buyer_identified

Qualification → Proposal:
  budget_confirmed, timeline_confirmed, decision_criteria_documented

Proposal → Negotiation:
  legal_contact_identified, procurement_process_documented, ocv_entry_referenced

Negotiation → Closed/Won:
  signed_order_form_confirmed, go_live_date_confirmed, cs_handoff_owner_assigned
```

---

## Output Format

```
FIELD COMPLETION — [Scope/Stage] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

Completion by stage gate:
  Discovery→Qual:    XX%  ([N] deals missing fields)
  Qual→Proposal:     XX%  ([N] deals missing fields)
  Proposal→Negotiation: XX%  ([N] deals — includes OCV check)
  Negotiation→Close: XX%  ([N] deals — PRE-CLOSE CRITICAL)

⚠ PRE-CLOSE FLAGS (Negotiation+ with missing fields, <2 weeks to quarter end):
  [Account A]  Missing: signed_order_form_confirmed, cs_handoff_owner_assigned
               Rep: [name]  ACV: $XXXk  Close: [date]
               → Escalate to [rep manager] immediately

Rep completion rates:
  Rep       Completion   Deals with gaps
  [Rep A]   94%          1
  [Rep B]   71%          4  ⚠

[Write-tier: Field updates require human confirmation]
[G7: Pre-close escalation path: [manager] via [channel] within 24h]
```

---

## Guardrails

- G7: Pre-close flags name the escalation path and owner
- G6: Data-as-of required
- G9: No autonomous field updates
