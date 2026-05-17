---
name: non-standard-terms-detection
version: 1.0.0
description: "Scans deal notes and opportunity fields for payment terms, contract structures, and custom provisions outside the standard playbook. Detection patterns: payment terms net >30 days, multi-year ramps/price locks, SLA commitments, data residency requirements, indemnification carve-outs, source code escrow. Routes to Legal or Finance when required. Triggers: 'non-standard terms', 'off-playbook deal', 'custom provisions', 'payment terms', 'SLA commitment', 'data residency'."
---

# Non-Standard Terms Detection

Catches off-playbook provisions before they become legal or financial surprises.

**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `payment_terms_standard_days`, `linear_connected`

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

## Guardrails

- G1: RevRecog implications require Finance routing before deal close
- Write-tier: Issue creation requires confirmation
