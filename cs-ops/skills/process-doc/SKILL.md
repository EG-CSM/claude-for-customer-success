---
name: process-doc
description: >
  Create or update CS Ops process documentation — SOPs, governance records,
  handoff guides, decision logs, and data quality standards. Use when a CS
  process needs to be codified, a governance decision needs a permanent record,
  or a recurring workflow needs a repeatable SOP. Produces publication-ready
  Markdown documentation calibrated to the specified process type. Distinct from
  /cs-ops:capacity-planner and /cs-ops:playbook-auditor which produce analysis
  outputs; this skill produces durable process documentation.
argument-hint: "[--csm-handoff | --playbook-governance | --data-quality | --escalation | --segment-change | --sop <process-name>]"
version: "1.0.0"
---

# /cs-ops:process-doc

Good process documentation is the difference between a decision that sticks
and one that has to be re-made every quarter.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
and `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/cs-ops:cold-start-interview`.

Critical configuration to apply:
- Escalation matrix — required for `--escalation` doc; informs escalation path
  sections in all other doc types
- CSM roster and roles — required for any handoff, RACI, or ownership sections
- Segment definitions — required for `--segment-change` doc
- Configured playbook — required for `--playbook-governance` doc

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G7 (flag any process data or account records that are stale relative to the configured staleness threshold).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--csm-handoff`: CSM account handoff guide — structured SOP for transferring
accounts during a departure, leave, or planned territory change. Covers
prioritization, warm handoff steps, CRM update checklist, and communication
templates.

`--playbook-governance`: Playbook governance record — decision log for play
additions, modifications, retirements, and trigger changes. Produces both the
governance framework document and an individual change record.

`--data-quality`: Data quality standard — the authoritative document defining
required fields, staleness thresholds, consistency rules, and ownership for
CRM and CS platform data. Serves as the reference standard for
`/cs-ops:data-quality-check` audits.

`--escalation`: Escalation SOP — step-by-step guide for handling account
escalations from trigger to resolution to post-escalation follow-up. Covers
severity tiers, response time SLAs, owner assignments, and communication
cadence.

`--segment-change`: Segment reclassification procedure — SOP for moving an
account between segments, including approval workflow, CSM transition steps,
motion change management, and customer communication guidance.

`--sop <process-name>`: General-purpose SOP — structured process document for
any named CS Ops process not covered by the above modes. Produces a
purpose-built SOP using the standard format.

If no mode flag is provided, ask:

> "Which process do you need to document?"
> Options: CSM account handoff · Playbook governance · Data quality standard ·
> Escalation SOP · Segment reclassification · Other (describe)

---

## CSM Account Handoff Guide (`--csm-handoff`)

---

**CSM Account Handoff Guide**
*[Version] · [Date] · INTERNAL — CS-Ops use only*
*Applies to: planned departures · unplanned departures · territory restructures · leave coverage*

---

### Purpose and scope

This document governs the transfer of customer accounts from one CSM to another.
It applies to all account transfers regardless of cause. The goal is continuity
of customer relationship and zero coverage gaps during transition.

**This SOP does not apply to:** temporary coverage (< 2 weeks) where a covering
CSM manages accounts without formal ownership transfer.

---

### Handoff trigger classification

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

### Step 1 — Build the transfer roster

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

### Step 2 — Redistribution plan

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

### Step 3 — Warm handoff execution

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

### Step 4 — CRM and system updates

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

### Step 5 — Post-handoff follow-up

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

### Handoff checklist summary

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

---

## Playbook Governance Record (`--playbook-governance`)

---

**CS Playbook Governance Framework**
*[Version] · [Date] · INTERNAL — CS-Ops use only*

---

### Purpose

This document governs how plays are added, modified, and retired from the CS
playbook. Without a governance process, playbooks bloat with plays that were
relevant once and remain forever — or lose plays that should be preserved.

---

### Governance principles

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

### Change types

| Change type | Who can initiate | Who must approve | Record required |
|------------|-----------------|-----------------|----------------|
| New play — Add | CS Lead, CS Ops | CS Lead | Yes |
| Play modification — Trigger change | CS Ops, CS Lead | CS Lead | Yes |
| Play modification — Steps only | CSM, CS Ops | CS Lead (review) | Yes |
| Play modification — Outcome definition | CS Ops | CS Lead | Yes |
| Archival — Dead play | CS Ops | CS Lead | Yes |
| Emergency suspension — Active play with safety concern | CS Lead | VP CS | Yes — within 24 hours |

---

### Play change record format

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

### Governance log index

Maintain a running index of all change records:

| Change ID | Date | Play | Change type | Approved by |
|----------|------|------|------------|------------|
| PCR-YYYY-001 | [date] | [play] | Archive | [name] |
| PCR-YYYY-002 | [date] | [play] | Trigger change | [name] |

---

## Data Quality Standard (`--data-quality`)

---

**CS Data Quality Standard**
*[Version] · [Date] · INTERNAL — CS-Ops and RevOps use*
*This document is the authoritative standard applied by `/cs-ops:data-quality-check` audits.*

---

### Purpose

This document defines what "good data" means for the CS portfolio — which fields
are required, how current they must be, what valid values look like, and who is
responsible for maintaining each field.

Audits run against this standard. Violations reported in audit outputs reference
rules defined here. Changes to this standard require the change process in
Section 5.

---

### Required fields

| Field | CRM object | Required for | Completeness target | Owner |
|-------|-----------|-------------|--------------------|----|
| Account name | Account | All CS functions | 100% | CRM admin |
| ARR | Account | All CS functions | 100% | RevOps |
| Segment | Account | Capacity, coverage, reporting | 100% | CS Ops |
| CSM owner | Account | All CS functions | 100% — exceptions logged | CS Ops |
| Health tier | CS Platform | Health reporting, at-risk triage | [configured threshold]% | CS Platform |
| Renewal date | Account/Opportunity | Renewal forecast, at-risk | 100% | RevOps |
| Lifecycle stage | Account | Reporting, plays | [configured threshold]% | CS Ops |
| [Additional configured fields] | | | | |

---

### Staleness thresholds

| Field | Threshold | Rationale | Owner |
|-------|----------|-----------|-------|
| Health score | [N] days | Scores older than [threshold] do not reflect current account state | CS Platform (auto) / CSM (manual) |
| Health score components | [N] days | Component data sources must refresh within [threshold] | Integration / CS Platform |
| CSM last contact date | [N] days | Absence of contact beyond [threshold] triggers no-contact-in-N-days play | CSM |
| Lifecycle stage | [N] days | Stage should advance per milestone; stale stage indicates missed milestone or stale data | CSM / CS Ops |

**Staleness is measured from the field's last-updated timestamp**, not from the
data's creation date. A health score of 72 that was last updated 45 days ago is
stale even if the account hasn't changed.

---

### Consistency rules

The following cross-field relationships must hold. Violations are flagged in
data quality audits.

| Rule | Field A | Field B | Condition | Exception process |
|------|---------|---------|---------|------------------|
| Segment ↔ ARR | Segment classification | ARR | Account ARR should fall within configured segment ARR range | CS lead documents override rationale in account record |
| Health tier ↔ score | Health tier label | Health score | Tier label must match the score's configured range | Platform sync issue — escalate to CS Ops + integration team |
| Renewal date in past | Renewal date | Lifecycle stage | Past renewal date with "Active" lifecycle stage requires a renewal record or correction | RevOps or CS Ops to update |
| Lifecycle ↔ renewal | Lifecycle stage = Churned | Renewal date | Churned accounts should not have a future renewal date | RevOps to archive opportunity |
| CSM ↔ segment motion | CSM assignment type | Segment | A tech-touch CSM should not be assigned as the primary owner of an Enterprise account without a motion-override flag | CS Ops documents override in account record |

**Exceptions are legitimate — unapproved deviations are not.** Segment overrides
are sometimes intentional (e.g., a strategic SMB account managed high-touch).
Document the rationale; do not rely on the exception remaining undiscovered.

---

### Field ownership matrix

| Role | Creates | Updates | Audits |
|------|---------|---------|--------|
| RevOps | ARR, renewal date, contract fields | ARR changes, renewal date changes | Quarterly |
| CS Ops | Segment, CSM owner, lifecycle stage | Reclassifications, territory changes | Monthly |
| CSM | Health notes, contact date, success plan | Account-level updates post-contact | Ongoing |
| CS Platform (auto) | Health score, component scores | Per configured refresh cadence | Continuous |
| CRM Admin | Account name, technical CRM fields | Merge, dedupe, field config | As needed |

**Shared ownership items (RevOps + CS Ops):**
- Segment classification — CS Ops assigns; RevOps confirms against ARR
- Renewal date — RevOps creates; CS Ops flags when incorrect per CS platform lifecycle

---

### Standard change process

Changes to this standard (adding/removing required fields, adjusting thresholds,
adding consistency rules) require:

1. CS Ops drafts the proposed change with rationale
2. RevOps reviews changes that affect shared fields (ARR, renewal date)
3. CS Lead approves all changes
4. Updated standard published and communicated to CSM team
5. Version number incremented; change logged in document history

| Version | Date | Change | Approved by |
|---------|------|--------|------------|
| 1.0 | [date] | Initial standard | [name] |
| [N] | [date] | [Change summary] | [name] |

---

## Escalation SOP (`--escalation`)

---

**CS Escalation Standard Operating Procedure**
*[Version] · [Date] · INTERNAL — CS and CS-Ops use*

---

### Purpose and scope

This SOP defines how CS handles account escalations from initial trigger through
resolution and post-escalation follow-up. An escalation is a situation where
a customer's issue, concern, or relationship risk requires a coordinated response
beyond standard CSM engagement.

---

### Escalation severity tiers

| Tier | Definition | Examples | Response time SLA |
|------|-----------|---------|------------------|
| **S1 — Critical** | Existential business risk, imminent churn of high-ARR account, public threat, legal or compliance concern | Threat to cancel >$[threshold] ARR contract; regulatory complaint; security incident | < 2 hours |
| **S2 — High** | Unresolved platform issue affecting business outcomes, executive sponsor disengagement, active competitor evaluation | P1 support ticket open >72 hours; CFO threatening to review contract; RFP to competitor confirmed | < 24 hours |
| **S3 — Standard** | Recurring issue pattern, relationship cooling, NPS detractor without recovery | 3+ support tickets same issue; NPS score <5 with no recovery conversation; CSM contact requested by CS lead | < 48 hours |

---

### Escalation workflow

**Step 1 — Trigger**

An escalation is triggered when:
- A CSM identifies a situation meeting the severity criteria above
- A support ticket is flagged by the support team as escalation-eligible
- An executive or stakeholder contacts CS leadership directly with a concern
- A health score drops to Red with a high-ARR account

**Step 2 — Triage and classification**

Escalating CSM or CS lead classifies the severity. For S1: CS lead notified
immediately. For S2–S3: CSM logs escalation in [CRM/platform] and assigns
severity within 1 hour of identification.

**Step 3 — Owner assignment**

| Tier | Primary owner | Executive sponsor | Support liaison |
|------|--------------|-----------------|----------------|
| S1 | CS Lead / VP CS | VP CS (or C-suite per config) | Support Lead |
| S2 | CS Lead | VP CS (informed) | Support Lead (if technical) |
| S3 | CSM | CS Lead (informed) | Support (as needed) |

**Step 4 — Customer communication**

| Tier | First contact | Update cadence | Resolution communication |
|------|--------------|----------------|------------------------|
| S1 | < 2 hours | Every 4 hours until resolved | Executive-to-executive + written summary |
| S2 | < 24 hours | Daily | CS Lead summary + next-step plan |
| S3 | < 48 hours | Every 3 business days | CSM resolution note + follow-up touch |

**Step 5 — Resolution**

Escalation is resolved when:
- The triggering issue is addressed (product issue resolved, executive
  relationship restored, competitive threat addressed)
- Customer has confirmed satisfaction or the situation has stabilized
- A post-escalation follow-up plan is in place

**Resolution is not the same as issue closure.** An S1 account may require
30-60 days of elevated engagement after the incident is resolved before the
escalation is fully closed.

**Step 6 — Post-escalation follow-up**

For S1 and S2 escalations:
- 30-day health check — is the account trending toward recovery?
- Sentiment recovery play activated if health tier remains Red at 30 days
- Retrospective: what could have prevented this escalation? CS lead documents.

---

### Escalation log entry format

Each escalation is logged in CRM with:

| Field | Value |
|-------|-------|
| Account | [Name] |
| Severity | S1 / S2 / S3 |
| Trigger | [Brief description — what happened] |
| Opened by | [Name] |
| Opened date | [Date] |
| Primary owner | [Name] |
| Root cause | [Product / Relationship / Commercial / External] |
| Resolution date | [Date] |
| Outcome | [Retained / Churn risk reduced / At-risk / Churned] |
| Follow-up required | [Yes — specify / No] |

---

## Segment Reclassification Procedure (`--segment-change`)

---

**Segment Reclassification Procedure**
*[Version] · [Date] · INTERNAL — CS-Ops use*

---

### Purpose

This SOP governs moving an account from one segment to another. Reclassification
changes the CS motion, CSM assignment, and engagement model for the account.
Done without structure, it creates coverage gaps and relationship disruption.

---

### Reclassification triggers

**Upward reclassification** (e.g., SMB → Mid-market, Mid-market → Enterprise):
- Account ARR has exceeded the new segment floor for [configured threshold, e.g.,
  two consecutive quarters]
- Account is identified as strategic despite sub-threshold ARR (requires CS lead
  approval and manual override flag in CRM)

**Downward reclassification** (e.g., Enterprise → Mid-market):
- Account ARR has fallen below the current segment floor for [configured threshold]
- Account has reduced to a level where the current CS motion is not commercially
  justified (rare — requires VP CS approval before executing)

---

### Reclassification workflow

**Step 1 — Candidate identification**

Source: `/cs-ops:segment-analyzer --reclassification` identifies candidates
based on configured ARR thresholds.

| Account | Current segment | Current ARR | Threshold crossed | Direction |
|---------|----------------|------------|-----------------|-----------|
| [Account] | [Seg] | $[amount] | $[threshold] | Up / Down |

**Step 2 — CS lead review**

Downward reclassification: Requires explicit CS lead approval before proceeding.
Flag accounts where the relationship is sensitive (Green health, active QBR,
executive relationship) — these require a customer conversation plan.

**Step 3 — CSM assignment planning**

Identify the receiving CSM for the new segment before executing the change:
- Upward: identify a high-touch CSM with capacity; plan warm handoff
- Downward: determine if an existing tech-touch CSM will absorb or if the account
  will enter an automated tech-touch pool

**Step 4 — Customer communication (upward reclassification)**

Upward reclassification involves a CSM change and increased engagement — customers
typically view this positively. Communicate proactively:

> "As part of our continued investment in your success with [Product], I'm
> pleased to introduce [new CSM name], who will be your dedicated Customer
> Success Manager going forward. [New CSM name] has deep expertise in [area]
> and will be reaching out shortly to schedule an introductory call."

Downward reclassification: Do not reference "reclassification" in customer
communication. Frame any motion change as an evolution of engagement model,
not a reduction. Requires CS lead to approve communication before sending.

**Step 5 — CRM and system updates**

- [ ] CRM: Segment field updated
- [ ] CRM: CSM owner updated
- [ ] CS Platform: Account assignment updated; new CSM has account access
- [ ] Capacity planner: Ratios recalculated for both segments affected
- [ ] Active plays: Reviewed for motion compatibility in new segment

**Step 6 — Change log entry**

| Field | Value |
|-------|-------|
| Account | [Name] |
| From segment | [Old segment] |
| To segment | [New segment] |
| ARR at change | $[amount] |
| ARR trigger threshold crossed | $[threshold] |
| Approved by | [CS lead name] |
| Effective date | [Date] |
| Previous CSM | [Name] |
| New CSM | [Name] |
| Customer notified | [Yes / No — reason if No] |

---

## General-purpose SOP (`--sop <process-name>`)

---

**[Process Name] — Standard Operating Procedure**
*[Version] · [Date] · INTERNAL — [Audience]*

---

### Purpose and scope

[1-2 sentences defining what this SOP covers and what it does not cover.]

**Applies to:** [Roles, teams, or situations covered]
**Does not apply to:** [Explicit exclusions]

---

### Triggers

This SOP is activated when:
- [Trigger 1]
- [Trigger 2]

---

### Roles and responsibilities

| Role | Responsibility in this process |
|------|-------------------------------|
| [Role 1] | [What they own] |
| [Role 2] | [What they own] |

---

### Procedure

**Step 1 — [Step name]**

[Description. What happens, who does it, how.]

**Step 2 — [Step name]**

[Description.]

**Step N — [Step name]**

[Description.]

---

### Quality gate

Before moving to the next process step, confirm:
- [ ] [Check 1]
- [ ] [Check 2]

---

### Exceptions

| Exception | How to handle | Who approves |
|-----------|-------------|-------------|
| [Exception 1] | [Handling] | [Role] |

---

### Version history

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | [date] | Initial | [name] |

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Document type:** [CSM handoff / Playbook governance / Data quality standard / Escalation SOP / Segment reclassification / General SOP]
> - **Sources applied:** [cs-ops CLAUDE.md configuration ✓ | company-profile.md ✓ | user-provided details this session | template defaults — customize before publishing]
> - **Placeholder markers:** Review all `[configured threshold]`, `[N]`, `$[amount]`, and `[name]` markers — fill in values from your cs-ops configuration before distributing
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before distributing:** All process documents should be reviewed by CS lead for accuracy and by legal/HR for any handoff or termination-adjacent procedures
> - **Versioning:** Increment version number each time a document is updated; communicate changes to affected roles

---

## Output

Process documentation artifact — format driven by the document-type flag
(`--csm-handoff`, `--playbook-governance`, `--data-quality`, `--escalation`,
`--segment-change`, `--sop`). Each mode produces a structured markdown document
ready for team review and adoption. See mode-specific sections for field-level structure.

## Guardrails

**Process documents must be owned.** An SOP without a named owner is not
maintained. Every published document in this system must have an owner who is
responsible for keeping it current. Default owner: CS Ops.

**Templates are starting points.** The output of this skill contains placeholder
markers that must be replaced with your organization's specifics before the
document is useful. A document with `[configured threshold]` markers is a draft,
not a policy.

**Downward reclassification requires care.** Never recommend executing a
downward segment change without flagging the customer relationship risk.
Reducing engagement on a Green account can damage trust even when the
commercial logic is sound.

**Escalation SOPs must match escalation matrix config.** The response times and
owner assignments in the escalation SOP must match what's configured in
`../../CLAUDE.md`. If they diverge, the SOP is wrong — update it.

**Handoff documents are not auditable without the log.** The departure checklist
confirms steps were completed. Without a log entry, there is no evidence the
handoff was executed properly. Completion of the checklist alone is not
sufficient — the log must be updated.

**Governance documents are only as good as adoption.** A playbook governance
framework that nobody uses is worse than no framework — it implies decisions are
being governed when they're not. CS Ops is responsible for enforcing the
governance process, not just documenting it.

---

## After documentation

- "Handoff SOP complete — check current CSM coverage: `/cs-ops:capacity-planner`"
- "Data quality standard published — run the first baseline audit: `/cs-ops:data-quality-check`"
- "Playbook governance framework in place — run initial playbook audit: `/cs-ops:playbook-auditor`"
- "Escalation SOP finalized — verify escalation matrix config is consistent: `/cs-ops:customize --section escalation`"
- "Segment reclassification procedure documented — run reclassification queue: `/cs-ops:segment-analyzer --reclassification`"
- "All CS-Ops process docs complete — generate baseline metrics: `/cs-ops:metric-dashboard`"
