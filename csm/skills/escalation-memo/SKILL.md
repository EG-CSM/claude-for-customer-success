---
name: escalation-memo
description: >
  Create, update, or close a formal escalation record for any escalation type —
  technical (unresolved P1/P2), customer complaint, executive escalation request,
  or internal process failure. Distinct from risk-flag's escalation output: this
  skill manages the escalation lifecycle, produces stakeholder communications, and
  tracks resolution. Use when a customer issue exceeds normal support handling,
  when an executive stakeholder requests formal escalation, or when a risk-flag
  memo has been accepted and escalation needs to be formally opened and tracked.
argument-hint: "[account name] [--open | --update | --close] [--type technical|complaint|executive|internal]"
version: "1.0.0"
---

# /escalation-memo

Open, manage, and close formal escalations with the right stakeholders, the right
framing, and a clear resolution path — built from your configured escalation matrix.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to apply:
- Escalation matrix — routing for each escalation type and severity level
- ARR escalation threshold — determines whether VP CS / CRO are in the loop
- SLA commitments — what response times are promised at each tier
- Escalation owner by type (e.g., Support Manager for P1 technical; VP CS for churn risk)

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G3 (any revenue impact language must carry commitment language + Finance validation callout), G4 (verify a named escalation path is configured before generating the memo), G5 (confidentiality check before distributing the memo beyond the CS team).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--open`: Create a new formal escalation record. Produces: escalation brief for
the escalation owner, customer-facing acknowledgment draft, and internal tracking
block. **Default mode.**

`--update`: Update an existing open escalation — new information, status change,
resolution progress. Requires the escalation ID or account + type context.

`--close`: Close an escalation with a resolution summary. Produces a close-out
communication for the customer and an internal lessons-learned note.

---

## Escalation type

`--type technical`: Unresolved P1/P2 ticket; product bug with customer impact;
SLA breach. Route: Support → Engineering escalation path.

`--type complaint`: Customer has formally expressed dissatisfaction — NPS detractor
follow-up not resolved, executive complaint, or public-facing concern.

`--type executive`: An executive stakeholder at the customer has requested VP or
C-level involvement. May overlap with churn risk but is triggered by relationship
posture, not always by health signals.

`--type internal`: An internal process failure has affected the customer — missed
handoff, broken commitment, SLA breach caused by internal team, not the product.

If no type is specified, ask ONE question to determine escalation type before
proceeding.

---

## Data gathering

Pull from connected integrations:
- Support platform: ticket ID, severity, open duration, SLA status, assigned agent
- CRM: ARR, renewal date, contract terms, escalation history for this account
- CS Platform: current health score, lifecycle stage, prior escalations
- Call recording: any recent call where the issue was raised — what was said,
  commitments made

If nothing is connected:
> "Tell me what's happening. What's the issue? Who's involved? What was the
> triggering event? I'll build the escalation record from what you share."

Do not produce a formal escalation without: account name, issue description, the
triggering event, and at least one affected stakeholder (internal or customer-facing).

---

## Escalation open structure (`--open`)

Produce two outputs: **Internal escalation brief** (full context for the escalation
owner) and **Customer acknowledgment draft** (external, professional).

---

### Internal Escalation Brief

---

**Escalation Brief — [Account Name]**
*[Date] · [Escalation type] escalation · INTERNAL — not for distribution*
*Escalation ID: [ESC-YYYYMMDD-[account abbreviation]] — use this ID in all follow-up*

---

**Escalation summary**

| Field | Detail |
|-------|--------|
| Account | [Account name] |
| ARR | $[amount] |
| Renewal | [date] — [N] days |
| Segment | [segment] |
| Escalation type | [Technical / Complaint / Executive / Internal] |
| Severity | [P1 / P2 / High / Medium — per configured definitions] |
| Opened by | [CSM name] |
| Escalation owner | [configured escalation owner from matrix] |
| SLA | [Response: X hours / Resolution target: Y hours — from config] |

---

**The issue**

What happened — specific, factual, in sequence:

> "On [date], [customer contact name] reported [specific issue]. [What was
> communicated to the customer at the time — any commitment or ETA given].
> The issue has been open for [N] days without resolution. [What has been
> tried so far]. The customer is [specific expression of impact or frustration —
> quoted if available]."

Do not generalize. Name the specific issue, the specific person who raised it,
and the specific business impact the customer described.

---

**Customer impact**

| Impact dimension | Detail |
|-----------------|--------|
| Business impact | [What the customer says cannot happen because of this issue] |
| Users affected | [N users / entire account / specific team] |
| Revenue impact to customer | [If stated by customer — quote it] |
| Relationship impact | [Executive aware? Sentiment shift? Escalation demand?] |

---

**Escalation history for this account**

Pull from CRM if available. If no prior escalations: "No prior escalations on
record for this account."

| Date | Type | Issue | Resolution | Time to close |
|------|------|-------|-----------|---------------|
| [Date] | [Type] | [1-line] | [1-line] | [N days] |

Pattern note: If this is a repeat escalation type: `[review — repeat escalation;
root cause may not have been fully resolved]`

---

**Internal context (CSM perspective)**

What the escalation owner needs to know that is not in the ticket:

- **Relationship context:** [Is this account at risk? Is the executive sponsor engaged?
  Is the champion under pressure?]
- **Prior commitments:** [Any commitments made by CSM, AE, or Support that are relevant]
- **Customer expectation:** [What the customer has specifically said they need to
  consider this resolved]
- **Renewal context:** [If renewal is <180 days or account is Yellow/Red: note it]

---

**Escalation routing**

Apply the configured escalation matrix exactly.

| Condition | Route to | Via | SLA |
|-----------|----------|-----|-----|
| [Matching condition from matrix] | [configured escalation owner] | [channel] | [SLA] |

If ARR meets the configured churn-risk threshold:
> "ARR ($[amount]) exceeds the configured escalation threshold ($[threshold]).
> Include [configured VP/CRO contact] in escalation communications within [SLA]."

---

**Recommended actions for escalation owner**

Specific, not generic. Owner reads this and knows exactly what to do.

**Within [SLA hours]:**
1. [Specific action — e.g., "Acknowledge to [customer contact] that the issue has
   been escalated and [escalation owner name] is now personally engaged."]
2. [Specific action — e.g., "Contact [support engineer assigned] directly to confirm
   current status and resolution ETA — do not relay information through the ticket queue."]
3. [Specific action — if applicable, "Loop in [AE name] — account is within <90 days
   of renewal."]

**Resolution target: [configured SLA]**

---

### Customer Acknowledgment Draft

---

**[Customer contact name],**

Thank you for flagging this — and I want to make sure it gets the attention it
deserves.

I've escalated [brief description of the issue] to [escalation owner name / "our
[role]"] who is now personally engaged. [He/She/They] will be in touch with you
directly by [specific time commitment — do not use vague language].

Here's what's happening:
- [1-line status of the issue]
- [What we're doing right now to resolve it]
- [When you'll have a substantive update — be specific]

I know this has been frustrating, and I want to be direct with you: [personalized
one sentence acknowledging the specific impact to their business — not generic
empathy language].

I'll stay closely involved. If anything changes or you need to reach me directly:
[CSM contact information].

[CSM name]

---

> **Note:** Edit the draft before sending. Replace all bracketed fields. Adjust tone
> to match relationship with this customer. Do not include internal SLA language,
> escalation IDs, or internal routing in the customer-facing email.

---

## Escalation update structure (`--update`)

Use the escalation ID from the original brief.

---

**Escalation Update — [Account Name]**
*[Date] · [Escalation ID] · INTERNAL*

**Status:** [Open — in progress / Open — awaiting customer response /
Open — awaiting engineering / Resolved — pending close-out]

**Update:**

> What has changed since the last update. What was done. What the customer has
> been told. What is outstanding.

**New information from customer:**
> [Quote or paraphrase if the customer has provided new context or expressed
> a change in position]

**Updated ETA:** [Specific date/time for next milestone or resolution]

**Updated escalation routing:** [Any change to who is now accountable]

**Customer communication sent:** [Yes, [date] / Not yet — draft needed]

---

**Customer update draft (if needed):**

> "[Customer contact], I wanted to give you a quick update on [issue].
> [What has been accomplished]. [What we're still working on]. [When you'll
> have the next update — specific]. Please reach out to me directly if you
> have questions in the meantime.
> [CSM name]"

---

## Escalation close structure (`--close`)

---

**Escalation Close-Out — [Account Name]**
*[Date] · [Escalation ID]*

**Resolution summary:**

| Field | Detail |
|-------|--------|
| Issue | [1-line description] |
| Opened | [date] |
| Closed | [date] |
| Duration | [N days] |
| Resolution | [What was done to resolve it] |
| Root cause | [If identified — specific, not "internal process"] |

**Was the SLA met?** [Yes / No — [configured SLA] / Resolution required [N] days]

**Customer confirmed resolution?** [Yes / No — pending confirmation]

---

**Internal lessons learned:**

> "What should have prevented this escalation from reaching this severity?"
> [1-3 specific process or communication changes that would reduce recurrence]

If this is a repeat escalation type for this account:
> "This is the [N]th escalation of type [type] for [account]. Pattern indicates
> [specific root cause hypothesis — not generic]. Route this observation to
> [configured CS Ops or VP CS contact] for systemic review." `[review]`

---

**Customer close-out communication:**

**[Customer contact name],**

I'm writing to confirm that [brief description of the issue] has been resolved.

Here's what we did: [Specific resolution steps — 1-3 sentences. Plain language.]

Root cause: [If you're able to share — be honest. "An internal process gap
caused [X]" is better than vague language.] We've taken [specific steps] to
prevent recurrence.

We take issues like this seriously, and I appreciate your patience while we
worked through it. [Any goodwill action taken — discount, credit, added support,
executive follow-up call — name it if applicable].

I'd like to reconnect with you [specific timeframe] to make sure everything is
working well and to address any remaining concerns.

Thank you for your continued partnership.

[CSM name]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [Support platform ✓ live — ticket details | CRM ✓ live — ARR, history | user provided | conversation context only]
> - **Escalation type:** [Technical / Complaint / Executive / Internal]
> - **Escalation routing:** [Applied configured matrix — verify escalation owner name and contact is current]
> - **Data as of:** [timestamp per source]
> - **SLA clock:** [Escalation opened at [timestamp] — [configured SLA] response window closes at [timestamp]]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sending customer draft:** Edit all bracketed fields. Do not include internal escalation IDs or routing in customer-facing email.

---

## Output

Escalation memo — format driven by lifecycle flag (`--open`, `--update`, `--close`).
Each mode produces a structured markdown document ready for internal distribution
or customer delivery. See mode-specific sections for field-level structure.

## Guardrails

**No escalation without a path.** Every escalation names the owner, channel, and
SLA from the configured matrix. An escalation without a resolution owner is not
an escalation — it's a complaint log.

**Customer language is not internal language.** The internal brief and customer
communication are always separate. Health scores, escalation IDs, internal routing
names, and revenue threshold references never appear in the customer draft.

**Commitments must be specific.** "We'll get back to you soon" is not a
commitment. The customer acknowledgment draft specifies a time. If no time can
be committed, say "by end of business [specific date]" — never leave it open-ended.

**Repeat escalation flag.** If CRM shows prior escalations of the same type,
flag it explicitly. Patterns require systemic review, not just case-by-case
resolution.

**Root cause in close-out.** A close-out without a root cause assessment allows
recurrence. Even if root cause is preliminary, name the hypothesis and the evidence.

**Revenue language.** If the escalation memo includes ARR, renewal dates, or
revenue-at-risk language, validate figures with CRM before sharing with leadership
or finance.

---

## After the memo

- "Escalation open — want to track risk holistically? `/csm:risk-flag [account]`"
- "Escalation resolved — should this inform the next QBR? `/csm:qbr-builder [account]`"
- "Pattern of escalations — route to CS Ops for systemic review: `/cs-ops:playbook-auditor`"
- "Renewal approaching during an open escalation — run: `/csm:renewal-readiness [account]`"
