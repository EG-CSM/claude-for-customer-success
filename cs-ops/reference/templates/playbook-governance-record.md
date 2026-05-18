# CS Playbook Governance Framework

**CS Playbook Governance Framework**
*[Version] · [Date] · INTERNAL — CS-Ops use only*

---

## Purpose

This document governs how plays are added, modified, and retired from the CS
playbook. Without a governance process, playbooks bloat with plays that were
relevant once and remain forever — or lose plays that should be preserved.

---

## Governance principles

1. **Every play change is a decision, not an edit.** Changes to the playbook
   require a named decision-maker, a rationale, and a log entry.
2. **Trigger changes require approval.** Narrowing or broadening a trigger
   condition changes when a play fires — this affects measurability and
   adoption. CS lead must approve all trigger changes.
3. **Archival is permanent until reversed.** A play removed from active status
   is not visible to CSMs. Reversals require a new change record.
4. **Performance data informs decisions — it does not make them.** A play with
   low activation may cover a rare-but-critical scenario. A play with high
   activation and poor outcomes may need trigger refinement, not removal.

---

## Change types

| Change type | Who can initiate | Who must approve | Record required |
|------------|-----------------|-----------------|----------------|
| New play — Add | CS Lead, CS Ops | CS Lead | Yes |
| Play modification — Trigger change | CS Ops, CS Lead | CS Lead | Yes |
| Play modification — Steps only | CSM, CS Ops | CS Lead (review) | Yes |
| Play modification — Outcome definition | CS Ops | CS Lead | Yes |
| Archival — Dead play | CS Ops | CS Lead | Yes |
| Emergency suspension — Active play with safety concern | CS Lead | VP CS | Yes — within 24 hours |

---

## Play change record format

Use one record per change. Archive in `playbook-governance-log.md`.

---

**Playbook Change Record — [Change ID: PCR-YYYY-NNN]**
*[Date] · Type: [Add / Modify / Archive / Suspend]*

| Field | Value |
|-------|-------|
| Play name | [Play name] |
| Change type | [Add / Modify trigger / Modify steps / Modify outcome / Archive / Suspend] |
| Initiated by | [Name, Role] |
| Approved by | [Name, Role] |
| Approval date | [Date] |
| Effective date | [Date] |

**Rationale:**
[Why this change is being made — minimum 2 sentences. Reference data where
available: activation rate, outcome achievement %, audit finding, churn pattern,
or strategic priority. Avoid single-word rationale like "Unused."]

**Before state:**
- Trigger: [Previous trigger text]
- Steps: [Count and summary, or "No prior version — new play"]
- Outcome: [Previous outcome definition]

**After state:**
- Trigger: [New trigger text]
- Steps: [Count and summary]
- Outcome: [New outcome definition]

**Expected impact:**
[What should change as a result — activation rate, CSM behavior, outcome
measurability. Used to evaluate the change at next playbook audit.]

**Review date:** [Date — typically 90 days post-change or at next quarterly audit]

---

**Archive record (for archival changes only):**

| Field | Value |
|-------|-------|
| Archive reason | [Scenario no longer relevant / Trigger too narrow / Coverage superseded by new play] |
| All-time activations | [N] |
| Last activation | [Date / Never] |
| Scenario frequency in next 12 months | [Expected: Low / Possible / Unknown] |
| Reversal authority | [CS Lead / VP CS] |

> ⚠️ Archiving removes this play from CSM visibility immediately. If this
> scenario recurs, there will be no structured response until the play is
> reinstated. Confirm CS lead has explicitly accepted this risk. `[review]`

---

## Governance log index

Maintain a running index of all change records:

| Change ID | Date | Play | Change type | Approved by |
|----------|------|------|------------|------------|
| PCR-YYYY-001 | [date] | [play] | Archive | [name] |
| PCR-YYYY-002 | [date] | [play] | Trigger change | [name] |
