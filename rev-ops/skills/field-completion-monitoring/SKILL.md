---
name: field-completion-monitoring
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Tracks required field completion rates by stage gate across both Sales new-logo pipeline and CS expansion/renewal pipeline. Flags missing data that will break downstream forecasting before quarter close. CS expansion gates include OCV entry reference, commercial terms, and churn risk resolution. Escalates deals in Negotiation+ or Commercial Terms+ with missing fields 2 weeks before quarter close. Triggers: 'missing fields', 'field completion', 'gate fields', 'pre-quarter-close hygiene', 'what fields are missing', 'CS expansion field compliance'."
---

[PROPOSED]

# Field Completion Monitoring

Stage gate field enforcement. Most important skill for forecast accuracy —
missing gate fields are the primary cause of forecast surprises.

**Reference:** Handoff quality scoring → `../../../shared/revops-domain-model.md §10`
**Config reads:** `crm_system`, `primary_segment`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `crm_system`, `primary_segment`

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

Before generating output, apply these primers:

1. **CLASSIFY**: What type of field completion request is this?
   - Single rep or CSM field completion report (one person — completion rate by stage gate + deal-level gaps)
   - Stage gate compliance scan (team or segment — aggregate completion rates across all gates)
   - Pre-quarter-close hygiene check (Negotiation+ or Commercial Terms+ deals with missing fields, <2 weeks to quarter end)
   - CS expansion pipeline field compliance (expansion/renewal deals moving through CS deal desk — equivalent gate enforcement to Sales)

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user requesting field completion check or pre-close hygiene
   2. Check HubSpot connector — field reads required for all pipeline objects; declare fallback if unavailable
   3. Confirm scope before pulling data: Sales new-logo / CS expansion / both pipelines
   4. Apply G6 — data-as-of on all HubSpot reads
   5. Apply G7 — pre-close escalation flags must include escalation path and named owner
   6. Apply G9 — no autonomous field updates; field corrections are proposals only

3. **EXPERT CHECK**: What would a veteran RevOps data integrity analyst verify first?
   - Is HubSpot data fresh enough to surface pre-close flags? Stale reads may miss fields
     added in the last 24–48h — declare data age before surfacing any pre-close flag.
   - Is the segment scope confirmed before running? Enterprise and SMB pipelines may have
     different gate field requirements — misscoping inflates or deflates completion rates.
   - Does every pre-close escalation flag name the escalation path and owner? "Escalate to
     manager" is not actionable — the named manager or role must appear on every flag.
   - Are CS expansion gate fields evaluated against the CS pipeline requirements, not Sales
     requirements? The OCV entry reference, commercial terms, and churn risk fields are
     CS-specific — applying Sales gate logic to CS deals misses required fields.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Surfacing HubSpot reads without data-as-of timestamp (G6 violation)
   - Omitting escalation path or named owner on any pre-close flag (G7 violation)
   - Proposing autonomous field updates or marking fields complete without human confirmation (G9 violation)
   - Applying Sales new-logo gate fields to CS expansion deals when CS-specific gates are defined

**After execution**, verify:
- G6 data-as-of label applied to all HubSpot reads
- G7 escalation path with named owner present on every pre-close flag
- G9 Write-tier qualifier present: field updates require human confirmation before execution
- Confidence: High when HubSpot is connected and data is current; Moderate when data is stale or connector is unavailable

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

## Output

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

- G7: Pre-close flags name the escalation path and owner
- G6: Data-as-of required
- G9: No autonomous field updates
