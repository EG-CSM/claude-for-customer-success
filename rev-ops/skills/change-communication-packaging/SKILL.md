---
name: change-communication-packaging
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Produces a three-part communication package for sensitive planning changes: (1) data-backed rationale memo for reps, (2) FAQ with top 5 anticipated objections and data responses, (3) rollout sequence with audience, channel, and order. Triggered automatically by annual-planning-workflow for territory, quota, or comp changes. Requires RevOps lead review before any distribution. Triggers: 'communicate changes', 'territory announcement', 'quota rationale', 'comp change communication', 'help me tell reps about [change]'."
---

[PROPOSED]

# Change Communication Packaging

The best data in the world fails if reps don't trust it.
Every planning change that affects rep behavior needs a communication package
before it leaves RevOps.

## Use when
- RevOps change (quota, territory, comp, process) needs communication packaging for affected stakeholders
- Change announcement requires audience-specific framing (reps vs managers vs leadership)
- Post-decision communication plan needed before rollout

## Do NOT use for
- Designing the change itself (use the relevant planning skill)
- Escalation communications mid-incident (use different escalation path)
- Customer-facing communications

## Typical Activation
"Package the territory changes for communication", "draft the comp plan announcement", "change communication for [change type]", "how do we communicate [change] to the field"

**Reference:** Output destination labels → `../../../shared/revops-domain-model.md §11`
**Reference:** Governance tiers → `../../../shared/revops-domain-model.md §9`
**Config reads:** `primary_segment`, `current_ae_count`

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: `primary_segment`, `current_ae_count`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of change communication request is this?
   - Territory change announcement
   - Quota change announcement
   - Comp plan change announcement
   - Other RevOps process change

2. **CONSTRAINTS**: What limits the solution space?
   1. Confirm activation — user packaging a change for rep communication
   2. Identify change type: territory / quota / comp / other
   3. Apply G4 for territory: confirm dual-confirmation is complete before packaging
   4. Apply G3 for comp: confirm HR + Finance dual review is complete before packaging
   5. Deliver as [DRAFT] — RevOps lead must approve before any communication is sent
   6. Output destination: [Rep-facing] label on all content

3. **EXPERT CHECK**: What would a veteran RevOps communicator verify first?
   - Is the governance gate cleared before packaging? (G4 for territory, G3 for comp)
   - Does the rationale memo use specific data, not vague reassurances?
   - Are the FAQ objections written as reps would actually say them — bluntly?
   - Does the rollout sequence put managers before reps — always?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Packaging a change before governance approval is confirmed (G4/G3 violation)
   - Writing the rationale memo for leadership instead of reps
   - FAQ answers that use reassurance language instead of data
   - Sending rep communications before manager communications

**After execution**, verify:
- All output is labeled [DRAFT] — no distribution before RevOps lead review
- [Rep-facing] label applied to all rep-facing content
- G4/G3 confirmation notes present for territory and comp changes respectively
- Confidence: High when data inputs are specific; Moderate when change details are estimated
- Confidence: [High] when data inputs are specific and governance gates confirmed / [Medium] when change details estimated / [Low] if all inputs are manual or unverified

---

## Three-Part Package

### Part 1 — Rationale Memo (rep-facing)

Written for the rep, not for leadership. Explains the data behind the change
in plain language. Specific numbers. Acknowledges the impact honestly.

```
Structure:
  Why we made this change — the data, not the spin
  What specifically changed for [rep/team/segment]
  Why this is the right call — evidence, not reassurance
  What this means for you going forward — practical, concrete

Tone: Direct. Honest about tradeoffs. Grounded in data.
NOT: Corporate smoothing language or vague positivity.
```

### Part 2 — FAQ (top 5 anticipated objections)

Written from the rep's perspective — the objections they will actually raise.

```
Format per FAQ item:
  Q: [The objection, stated bluntly — as the rep would say it]
  A: [Data-backed response — specific numbers, not reassurances]
     Source: [CRM / Company profile / UoG model]
```

Common objection categories by change type:
- Territory: "My territory got smaller / I lost my best accounts"
- Quota: "This quota is not achievable" / "Other reps got easier numbers"
- Comp: "My OTE is lower" / "The accelerators are worse"

### Part 3 — Rollout Sequence

```
Who hears what, in what order, through which channel.

Sequence:
  1. [Role — e.g., Sales VPs]: [Channel] on [date]
     Content: [what they receive — leadership brief or full rationale]
  2. [Role — e.g., AE managers]: [Channel] on [date]
     Content: [manager brief + coaching guidance]
  3. [Role — e.g., Individual AEs]: [Channel] on [date]
     Content: [rep-facing rationale memo + FAQ]

No rep learns about a territory/quota/comp change from an email blast.
Managers hear before their reps — always.
```

---

## Output

```
CHANGE COMMUNICATION PACKAGE — [Change type] — [DRAFT]

[Part 1 — Rationale Memo]
[Part 2 — FAQ]
[Part 3 — Rollout Sequence]

[DRAFT — requires RevOps lead approval before any distribution]
[Rep-facing content labeled: [Rep-facing]]
[G4: Territory changes confirmed dual-approved before this package was generated]
[G3: Comp changes confirmed HR + Finance dual-reviewed before this package was generated]
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

## Security & Permissions

**Network access:** None direct — all external data access is mediated by host-provided MCP connector tools (HubSpot, CS platform, Slack, Linear). This skill makes no direct outbound HTTP calls.
**Filesystem scope:** None — this skill does not read or write local files. All data is provided at runtime via parameters or MCP connector responses.
**Subprocess execution:** None.
**Dynamic code execution:** None — pseudocode in this skill represents the logic contract and is not executed at runtime.
**Data sensitivity:** Inputs may contain confidential revenue planning and compensation data. Handle with RevOps-level confidentiality.

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.

## Guardrails

- G3: Comp change packages carry mandatory HR + Finance review confirmation note
- G4: Territory change packages carry mandatory dual-confirmation note
- All output is [DRAFT] until RevOps lead approves for distribution
