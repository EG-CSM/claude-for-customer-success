# CSM Account Handoff Guide

**CSM Account Handoff Guide**
*[Version] · [Date] · INTERNAL — CS-Ops use only*
*Applies to: planned departures · unplanned departures · territory restructures · leave coverage*

---

## Purpose and scope

This document governs the transfer of customer accounts from one CSM to another.
It applies to all account transfers regardless of cause. The goal is continuity
of customer relationship and zero coverage gaps during transition.

**This SOP does not apply to:** temporary coverage (< 2 weeks) where a covering
CSM manages accounts without formal ownership transfer.

---

## Handoff trigger classification

| Trigger | Lead time | Urgency |
|---------|-----------|---------|
| Planned departure (resignation with notice) | 2–4 weeks | Standard |
| Unplanned departure (immediate termination, emergency leave) | 0 days | Urgent |
| Parental / medical leave | 1–4 weeks | Standard |
| Territory restructure | 2–6 weeks | Planned |
| Performance action | As directed by HR | Confidential — CS lead coordinates |

**For urgent (0-day) triggers:** Skip to Priority Account Triage — complete steps
1–3 within 24 hours before completing the full SOP.

---

## Step 1 — Build the transfer roster

Pull the departing CSM's account list from CRM. For each account, capture:

| Account | ARR | Segment | Health tier | Renewal date | Active play/CTA | Days since last contact |
|---------|-----|---------|------------|-------------|----------------|------------------------|
| [Account] | $[amount] | [Seg] | 🔴/🟡/🟢 | [date] | [Yes/No] | [N] |

**Priority classification:**

Assign each account to a priority tier before redistribution:

| Priority | Criteria | Action timeline |
|---------|---------|----------------|
| **P1 — Immediate** | 🔴 Red health OR renewal ≤60 days OR active escalation | Assign within 24 hours |
| **P2 — Standard** | 🟡 Yellow health OR renewal 61–90 days OR active play | Assign within 1 week |
| **P3 — Routine** | 🟢 Green health AND renewal >90 days AND no active work | Assign within 2 weeks |

---

## Step 2 — Redistribution plan

**Redistribution constraints:**
- Do not assign P1 accounts to a CSM already at or above target ratio
- Do not assign more than [configured threshold, e.g., 3] P1 accounts to any single receiving CSM
- Accounts with ARR above $[configured threshold] require a warm introduction — no cold transfers
- Active escalations must transfer with explicit escalation owner designation, not implicit account ownership

**Proposed redistribution table:**

| Account | Priority | To CSM | Rationale | Receiving CSM capacity (before/after) |
|---------|---------|--------|-----------|--------------------------------------|
| [Account] | P1 | [CSM] | [Reason] | [N] → [N] of [target] |

**CS lead sign-off required before redistribution executes.** `[review]`

---

## Step 3 — Warm handoff execution

For all accounts above $[configured ARR threshold] and all P1 accounts:

**Internal handoff meeting** (departing + receiving CSM + CS lead):
- Account background: business goals, product usage, relationship history
- Open items: active plays, CTAs, renewal conversation status, escalation history
- Known risks: executive relationships, support issues, pending product gaps
- Communication plan: how the transition will be messaged to the customer

**Customer communication:**

For accounts at or above the configured high-touch threshold — send a transition
email from the departing CSM (or CS lead if departure is immediate) within
[configured timeline, e.g., 5 business days] of transfer.

Template:
> Subject: Your [Company] Customer Success team — a quick introduction
>
> Hi [Contact name],
>
> [I'm writing / I wanted to reach out] to let you know that [departing CSM name]
> will be transitioning off your account on [date]. I'm glad to introduce
> [receiving CSM name], who will be your Customer Success Manager going forward.
>
> [Receiving CSM name] has [brief context — e.g., "extensive experience in the
> [industry] space and has worked with similar teams on [use case]"]. They will
> be in touch shortly to schedule an introductory call.
>
> Thank you for your partnership — [receiving CSM name] is looking forward to
> working with you.
>
> [Signature]

**Tech-touch accounts:** No customer communication required unless the account
has had meaningful direct engagement in the last 90 days.

---

## Step 4 — CRM and system updates

Complete within 24 hours of formal transfer:

- [ ] CRM: CSM owner field updated for all transferred accounts
- [ ] CS Platform: CSM assignment updated; account notes accessible to receiving CSM
- [ ] Active plays/CTAs: Re-assigned to receiving CSM in CS platform
- [ ] Escalations: Escalation owner updated in escalation log; stakeholders notified
- [ ] Scheduled QBRs: Receiving CSM added; calendar invites updated
- [ ] Success plans: Ownership transferred in [CS platform]; receiving CSM has edit access
- [ ] Shared Slack channels (if used): Receiving CSM added; customer notified of team member change

**Verification:** CS Ops confirms CRM assignment is complete and capacity counts updated. `[review]`

---

## Step 5 — Post-handoff follow-up

Within 30 days of transfer:
- Receiving CSM has completed introduction call or touch for all P1 and P2 accounts
- P1 accounts have no degradation in health tier from pre-transfer baseline
- No active escalations were created as a result of the transition

CS lead reviews at 30-day mark:

| Account | Pre-transfer health | 30-day health | Change | Notes |
|---------|-------------------|--------------|--------|-------|
| [Account] | 🟡 | 🟢 | Improved | |
| [Account] | 🟢 | 🔴 | **Degraded — investigate** | |

---

## Handoff checklist summary

**For departing CSM:**
- [ ] Account roster exported and priority tier assigned
- [ ] Handoff meeting completed for all P1 and high-ARR accounts
- [ ] Account notes and success plans updated and current
- [ ] Open plays, CTAs, and escalations documented with status
- [ ] CRM handover notes added to each account

**For receiving CSM:**
- [ ] Introduction call scheduled for all P1 accounts within first week
- [ ] Customer communication sent for high-ARR accounts
- [ ] Active plays resumed with no gap in execution
- [ ] 30-day health review scheduled

**For CS Ops:**
- [ ] CRM field updates verified
- [ ] Capacity ratios recalculated post-transfer
- [ ] Redistribution plan archived in `/cs-ops:process-doc` records
- [ ] 30-day follow-up scheduled
