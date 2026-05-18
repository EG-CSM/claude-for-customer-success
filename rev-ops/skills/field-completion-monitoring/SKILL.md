---
name: field-completion-monitoring
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Tracks required field completion rates by stage gate across both Sales new-logo pipeline and CS expansion/renewal pipeline. Flags missing data that will break downstream forecasting before quarter close. CS expansion gates include OCV entry reference, commercial terms, and churn risk resolution. Escalates deals in Negotiation+ or Commercial Terms+ with missing fields 2 weeks before quarter close. Triggers: 'missing fields', 'field completion', 'gate fields', 'pre-quarter-close hygiene', 'what fields are missing', 'CS expansion field compliance'."
---

# Field Completion Monitoring

Stage gate field enforcement. Most important skill for forecast accuracy —
missing gate fields are the primary cause of forecast surprises.

**Reference:** Handoff quality scoring → `../../../shared/revops-domain-model.md §10`
**Config reads:** `crm_system`, `primary_segment`

---

## Use when
- Required CRM field completion rates need to be tracked over time — applies to both Sales new-logo pipeline and CS expansion pipeline
- Field compliance reporting required for rep, CSM, or team review
- Specific high-value fields (close date, ACV, next step) need completion rate trending
- CS expansion deals moving through the CS pipeline need equivalent stage gate enforcement before commercial terms are processed

## Do NOT use for
- Full CRM hygiene audit (use crm-hygiene-audit)
- Stage integrity checking (use stage-integrity-audit)
- Duplicate record detection (use duplicate-detection)

## Typical activation
"Field completion monitoring", "field completion rate for [field/team]", "required field compliance", "how complete is our CRM data", "track field fill rates"

---

## Reasoning Protocol

1. Confirm activation — user requesting field completion check or pre-close hygiene
2. Check HubSpot — field reads required; declare fallback if unavailable
3. Apply G6 — data-as-of required
4. For quarter-close escalations: confirm escalation path and owner (G7)
5. Write-tier for any CRM field updates — proposals only

---

## Stage Gate Fields

### Sales New-Logo Pipeline

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

### CS Expansion Pipeline

Expansion deals originating from CS (CSQLs, renewal upsells, cross-sell motions)
require equivalent field completion discipline as they move through the CS deal desk.
Missing fields here break expansion forecasting and revenue recognition the same way
missing Sales fields break new-logo forecasting.

```
Expansion Identified → Qualified:
  expansion_scope_documented, ocv_entry_referenced_for_expansion,
  economic_buyer_confirmed_at_account, csm_sponsor_identified

Qualified → Commercial Terms:
  expansion_arr_estimated, commercial_terms_documented,
  legal_contact_identified, procurement_process_documented

Commercial Terms → Closed/Won (Expansion):
  signed_expansion_order_confirmed, expansion_go_live_date_confirmed,
  renewal_contract_updated_or_pending

Renewal Due → Renewal Closed:
  renewal_terms_confirmed, churn_risk_flag_resolved_or_escalated,
  renewal_signed_order_confirmed
```

**CS-specific gate fields of record:**
- `ocv_entry_referenced_for_expansion` — links expansion scope to the OCV catalog entry
  defining what was committed and at what rubric level. Required before commercial terms.
- `renewal_contract_updated_or_pending` — confirms whether base contract is being amended
  or a new order form is in play. Required before close.
- `churn_risk_flag_resolved_or_escalated` — for renewals with an open churn signal:
  confirms the risk has been addressed or escalated before the renewal is logged as clean.

---

## Output Format

```
FIELD COMPLETION — [Scope/Stage] — [Date]
[HubSpot ✓ live — as of YYYY-MM-DD] [Confidence: High]

SALES NEW-LOGO PIPELINE
  Completion by stage gate:
    Discovery→Qual:         XX%  ([N] deals missing fields)
    Qual→Proposal:          XX%  ([N] deals missing fields)
    Proposal→Negotiation:   XX%  ([N] deals — includes OCV check)
    Negotiation→Close:      XX%  ([N] deals — PRE-CLOSE CRITICAL)

  ⚠ PRE-CLOSE FLAGS (Negotiation+ with missing fields, <2 weeks to quarter end):
    [Account A]  Missing: signed_order_form_confirmed, cs_handoff_owner_assigned
                 Rep: [name]  ACV: $XXXk  Close: [date]
                 → Escalate to [rep manager] immediately

  Rep completion rates:
    Rep       Completion   Deals with gaps
    [Rep A]   94%          1
    [Rep B]   71%          4  ⚠

CS EXPANSION PIPELINE
  Completion by stage gate:
    Expansion ID→Qualified:     XX%  ([N] deals missing fields — incl. OCV ref)
    Qualified→Commercial Terms: XX%  ([N] deals missing fields)
    Commercial Terms→Close:     XX%  ([N] deals — PRE-CLOSE CRITICAL)
    Renewal Due→Renewal Closed: XX%  ([N] renewals — churn risk check)

  ⚠ PRE-CLOSE FLAGS (CS expansion/renewal with missing fields, <2 weeks to quarter end):
    [Account B]  Missing: ocv_entry_referenced_for_expansion, commercial_terms_documented
                 CSM: [name]  Expansion ACV: $XXXk  Close: [date]
                 → Escalate to CS manager immediately

  CSM completion rates:
    CSM       Completion   Deals with gaps
    [CSM A]   91%          1
    [CSM B]   68%          3  ⚠

[Write-tier: Field updates require human confirmation]
[G7: Pre-close escalation path: [manager] via [channel] within 24h]
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

- G7: Pre-close flags name the escalation path and owner
- G6: Data-as-of required
- G9: No autonomous field updates
