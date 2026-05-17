---
name: change-communication-packaging
version: 1.0.0
description: "Produces a three-part communication package for sensitive planning changes: (1) data-backed rationale memo for reps, (2) FAQ with top 5 anticipated objections and data responses, (3) rollout sequence with audience, channel, and order. Triggered automatically by annual-planning-workflow for territory, quota, or comp changes. Requires RevOps lead review before any distribution. Triggers: 'communicate changes', 'territory announcement', 'quota rationale', 'comp change communication', 'help me tell reps about [change]'."
---

# Change Communication Packaging

The best data in the world fails if reps don't trust it.
Every planning change that affects rep behavior needs a communication package
before it leaves RevOps.

**Reference:** Output destination labels → `reference/revops-domain-model.md §11`
**Reference:** Governance tiers → `reference/revops-domain-model.md §9`
**Config reads:** `primary_segment`, `current_ae_count`

---

## Reasoning Protocol

1. Confirm activation — user packaging a change for rep communication
2. Identify change type: territory / quota / comp / other
3. Apply G4 for territory: confirm dual-confirmation is complete before packaging
4. Apply G3 for comp: confirm HR + Finance dual review is complete before packaging
5. Deliver as [DRAFT] — RevOps lead must approve before any communication is sent
6. Output destination: [Rep-facing] label on all content

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
     Source: [CRM / Practice profile / UoG model]
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

## Guardrails

- G3: Comp change packages carry mandatory HR + Finance review confirmation note
- G4: Territory change packages carry mandatory dual-confirmation note
- All output is [DRAFT] until RevOps lead approves for distribution
