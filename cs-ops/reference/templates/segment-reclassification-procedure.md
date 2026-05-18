# Segment Reclassification Procedure

**Segment Reclassification Procedure**
*[Version] · [Date] · INTERNAL — CS-Ops use*

---

## Purpose

This procedure governs how accounts move between segments when their ARR crosses a
configured threshold. Reclassification changes the CS motion, CSM assignment model,
and engagement cadence for an account. It must be handled deliberately — especially
downward reclassification, which can affect customer perception of service level.

---

## Reclassification triggers

**Upward reclassification** (e.g., SMB → Mid-market, Mid-market → Enterprise):
- Account ARR has exceeded the new segment floor for [configured threshold, e.g., 2
  consecutive quarters or a single expansion event above threshold]
- Triggered by: expansion event in CRM, renewal at higher ARR, CS Platform alert

**Downward reclassification** (e.g., Enterprise → Mid-market, Mid-market → SMB):
- Account ARR has fallen below the current segment floor for [configured threshold,
  e.g., 2 consecutive quarters or a contraction event below threshold]
- Triggered by: contraction event in CRM, partial churn, downsell at renewal
- **Downward reclassification requires CS Lead review before proceeding** — a currently
  Green account in an active relationship should not be moved to a lower-touch model
  without a customer communication plan.

---

## Reclassification workflow

### Step 1 — Candidate identification

CS Ops or the segment-analyzer skill (`--reclassification` mode) identifies accounts
that have crossed a configured ARR threshold. Output: reclassification candidate list
with account name, current segment, current ARR, threshold crossed, direction
(upward/downward), and current health tier.

### Step 2 — CS Lead review

CS Lead reviews the candidate list:
- Confirm each candidate is a genuine crossing (not a data error)
- For downward candidates: assess relationship health and relationship risk of segment
  change before approving
- Approve, defer, or reject each candidate; document rationale for deferred/rejected
  items

**CS Lead sign-off required before any reclassification executes.** `[review]`

### Step 3 — CSM assignment planning

For approved reclassification candidates:
- Upward: identify the receiving CSM segment (may require a new CSM if current CSM
  does not cover the new segment's motion)
- Downward: confirm whether the current CSM remains assigned or whether tech-touch
  coverage replaces dedicated CSM coverage
- Capacity planner (`/cs-ops:capacity-planner`) to confirm receiving CSM has capacity

### Step 4 — Customer communication

**Upward reclassification:** Send a customer communication introducing the new CSM
(if CSM changes) and the enhanced engagement model. Use the transition email template
from the CSM Account Handoff Guide if a CSM change is involved.

**Template for upward reclassification (no CSM change):**

> Subject: Your [Company] Success plan — an update
>
> Hi [Contact name],
>
> As your team has grown, so has our commitment to your success. Starting [date],
> [Contact name] will be transitioning to our [new segment, e.g., Enterprise] program,
> which includes [brief description of enhanced engagement — e.g., quarterly business
> reviews, a dedicated technical resource, and priority support access].
>
> [CSM name] will reach out to schedule an introduction to the new engagement model.
>
> Thank you for your continued partnership.
>
> [Signature]

**Downward reclassification:** Customer communication is required only if the change
results in a CSM change or visible reduction in engagement. CS Lead decides case by case.

### Step 5 — CRM and system updates

Complete within [configured SLA, e.g., 5 business days] of CS Lead approval:

- [ ] CRM: Account segment field updated
- [ ] CS Platform: Account segment and motion updated; health model reapplied if
      segment has different health model configuration
- [ ] CSM assignment updated if motion change requires new owner
- [ ] Active plays and CTAs: Confirm play logic is still valid for new segment motion;
      close or reassign plays that no longer apply
- [ ] Capacity ratios: CS Ops recalculates after transfer

### Step 6 — Change log entry

| Field | Value |
|-------|-------|
| Account | [Account name] |
| Previous segment | [Segment] |
| New segment | [Segment] |
| Direction | [Upward / Downward] |
| ARR at reclassification | $[amount] |
| Threshold crossed | $[threshold] |
| Approved by | [CS Lead name] |
| Approval date | [Date] |
| Effective date | [Date] |
| Customer communication sent | [Yes / No / Not required] |
| CSM change | [Yes — [from CSM] → [to CSM] / No] |

**Rationale:**
[Why reclassification was approved. For downward: confirm CS Lead explicitly accepted
relationship risk.] `[review]`
