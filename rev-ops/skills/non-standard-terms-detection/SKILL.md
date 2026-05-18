---
name: non-standard-terms-detection
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Scans deal notes and opportunity fields for payment terms, contract structures, and custom provisions outside the standard playbook. Detection patterns: payment terms net >30 days, multi-year ramps/price locks, SLA commitments, data residency requirements, indemnification carve-outs, source code escrow. Routes to Legal or Finance when required. Triggers: 'non-standard terms', 'off-playbook deal', 'custom provisions', 'payment terms', 'SLA commitment', 'data residency'."
---

# Non-Standard Terms Detection

Catches off-playbook provisions before they become legal or financial surprises.

**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `payment_terms_standard_days`, `linear_connected`

---

## Use when
- Deal notes or contract terms contain non-standard language that needs flagging before close
- Legal or finance review triggers need to be identified from deal context
- Deal desk submission requires non-standard terms inventory

## Do NOT use for
- Full deal desk routing (use deal-desk-workflow-management)
- Revenue leakage structural analysis (use revenue-leakage-scanning)
- ARR classification (use deal-classification)

## Typical activation
"Non-standard terms", "flag unusual contract terms", "what terms need legal review", "non-standard terms for [deal]", "check deal notes for flags"

---

## Reasoning Protocol

1. Confirm activation — user requesting terms review for a specific deal
2. Read deal notes and contract fields from HubSpot
3. Classify each non-standard element by type and routing requirement
4. Apply G1 — payment terms affecting revenue recognition require Finance routing
5. Write-tier: Linear issue to Legal or Finance requires confirmation

---

## Detection Patterns and Routing

```
Payment terms:
  net > payment_terms_standard_days → Finance review
  quarterly/deferred billing → Finance + RevRecog review

Multi-year structures:
  Price lock clauses → Finance approval
  Ramp schedules → Finance + RevOps approval
  Renewal caps → Legal + Finance review

Custom provisions:
  SLA commitments → Legal + CS Ops review
  Data residency requirements → Legal + Eng review
  Indemnification carve-outs → Legal review (mandatory)
  Source code escrow requests → Legal + Eng review (mandatory)
```

---

## Output Format

```
NON-STANDARD TERMS — [Account Name]
[HubSpot ✓ live — as of YYYY-MM-DD]

Findings:
  [Term type]  Standard: [what's standard]  Found: [what's in the deal]
               Route to: [Legal / Finance / Both]  Priority: [HIGH/MEDIUM]

No non-standard terms detected: [if clean]

Linear issues to create:
  [ ] Legal: [specific provision] — confirm to create
  [ ] Finance: [specific provision] — confirm to create
```

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential deal and pipeline data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G1: RevRecog implications require Finance routing before deal close
- Write-tier: Issue creation requires confirmation
