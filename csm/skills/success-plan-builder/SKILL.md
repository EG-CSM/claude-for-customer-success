---
name: success-plan-builder
description: >
  Build or update a customer success plan — account-specific success criteria,
  measurable milestones, engagement cadence, and mutual commitments. Use at
  kickoff for new accounts, when success criteria have drifted, or when an
  account needs a plan reset. Produces a co-authored document, not a CSM
  internal tracker.
argument-hint: "[account name] [--new | --reset | --review]"
version: "1.0.0"
---

# /success-plan-builder

Build a success plan that the customer will actually sign off on — account-specific
success criteria, measurable milestones, joint ownership, and a cadence that
reflects your configured CS motion.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- Success criteria model (account-specific vs. standard template)
- Primary value metric
- CS motion — shapes plan depth, cadence, and co-authorship approach
- Customer-facing plan format preference
- Playbook sources — use configured success plan template if available

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G3 (revenue outcome targets carry commitment language + Finance validation callout), G5 (confidentiality check before distributing the plan beyond the CS team).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--new`: Build a success plan from scratch for a new or recently kicked-off account.

`--reset`: Rebuild success criteria for an existing account where the original
plan has drifted, criteria were never properly established, or account context
has materially changed (new sponsor, new use case, new segment).

`--review`: User provides an existing success plan; skill reviews it for
completeness, specificity, and whether criteria are actually measurable. Returns
specific edits.

Default: prompt once — "Is this a new plan or an update to an existing one?"

---

## Data gathering

**What's needed before building:**

1. **Account goals** — what the customer said they wanted to accomplish
   (from kickoff notes, sales handoff notes, or user-provided context)

2. **Product context** — which features / modules are in scope for this account

3. **Stakeholder context** — who owns success on the customer side; who measures it

4. **Timelines** — contract duration, key milestones already committed, renewal date

5. **Existing success criteria** — if a plan exists, pull it before rebuilding

Pull from connected sources where available:
- CRM: contract duration, renewal date, stakeholder contacts, sales handoff notes
- Document storage: existing success plan, kickoff deck, onboarding notes
- CS Platform: account lifecycle stage, current health signals

Minimum viable prompt if nothing is connected:

> "To build a success plan that the customer will actually own, I need the customer's
> stated goals. What did they tell you — during the sales process or kickoff — that
> they want to accomplish with [product]? Paste notes, a handoff doc, or a
> quote if you have one."

Do not build a generic success plan from product features alone. Success criteria
must come from the customer's stated business outcomes, not assumed use cases.

---

## Success plan structure

---

**[Account Name] — Customer Success Plan**
*[Quarter / date range]*
*Prepared jointly by: [CSM name], [Company] · [Customer sponsor name], [Account]*

---

### 1. About this plan

One paragraph. Plain language. Why this document exists and how it will be used.

> "This success plan captures what [Account] is trying to accomplish with [product],
> the milestones we'll use to measure progress, and the commitments both teams are
> making to get there. We'll review it at each [cadence per CS motion: monthly /
> quarterly] check-in and update it as priorities shift."

---

### 2. Your goals

The customer's goals in their language — not product feature descriptions.

**Business goal [1]:** [What the customer said they want to achieve]
*Why it matters:* [Business context — e.g., "the team is scaling from 50 to 200
users and needs faster onboarding" — not assumed]

**Business goal [2]:** [...]

Do not translate customer goals into product language here. Keep the customer's
framing. Translation to product features happens in Section 3.

If goals are unclear or unstated: flag in the reviewer note and add a `[review]`
marker — "Customer's stated goals not confirmed. Review with sponsor before plan
is finalized."

---

### 3. Success criteria

For each business goal, define one or more observable, measurable criteria.

Apply configured success criteria model:
- If account-specific model: build criteria in collaboration with the customer
- If standard template: start from the template and customize per account goals

**Success criterion format:**

> **[Criterion name]**
> - **Measure:** [Specific metric — e.g., "% of licensed users who complete first workflow within 30 days of license activation"]
> - **Baseline:** [Where the account is today, if known]
> - **Target:** [The agreed number or milestone — e.g., ">70% within 90 days"]
> - **Evidence source:** [Where this will be measured — CS Platform / product analytics / customer-reported]
> - **Review cadence:** [When this will be checked — e.g., "monthly at check-in"]

Criteria that cannot be measured get a `[review]` flag: "This criterion as stated
is not measurable — agree on a specific metric with the customer before finalizing."

**Primary value metric:** [Configured primary value metric from company profile]
— this should appear as one of the success criteria or as an explicit success
criterion overlay.

---

### 4. Milestones

Time-bound markers that show the account is on track. Not a task list — milestones
mark when something meaningful has been accomplished.

| Milestone | Description | Target date | Owner | Health signal if missed |
|-----------|-------------|------------|-------|------------------------|
| M1 | [First meaningful event — e.g., "All users activated and first workflow completed"] | [Date] | [Customer / CSM / Joint] | [Flag if missed by [date+buffer]] |
| M2 | [Second milestone] | | | |
| M3 | [First value milestone — primary value metric achieved] | [Date — ideally within configured TtV target] | | |
| M4 | [Adoption milestone — criteria threshold reached] | | | |
| M5 | [Renewal-ready milestone — all success criteria at target] | [Date before renewal] | | |

Milestones are co-owned — mark the owner. A milestone owned entirely by the CSM
is an internal commitment, not a joint one.

---

### 5. Engagement cadence

What the customer can expect — and what's expected of them.

| Touchpoint | Frequency | Format | Attendees | Purpose |
|-----------|-----------|--------|-----------|---------|
| Check-in call | [Monthly / quarterly — per CS motion] | [Video call / async update] | [CSM + customer sponsor] | [Progress review, issue triage] |
| QBR | Quarterly | [60-min video] | [CSM + AE + exec sponsor] | [Value review, next-quarter alignment] |
| Health review | [As needed / triggered by health signal] | [Email or call] | [CSM] | [Risk identification] |
| Executive sponsor call | [Semi-annually or as needed] | [30-min video] | [CS lead + exec sponsor] | [Strategic alignment] |

Calibrate frequency to configured CS motion:
- High-touch: monthly minimum; QBR at each quarter
- Tech-touch: quarterly check-in standard; no standing monthly call
- Hybrid: match the segment this account sits in

---

### 6. Mutual commitments

What each party commits to. Both sides have responsibilities — a plan that only
lists CSM commitments is not a mutual plan.

**[Company] commits to:**
- [Specific commitment — e.g., "Respond to support tickets within [SLA]"]
- [Specific commitment — e.g., "Provide a dedicated CSM point of contact"]
- [Specific commitment — e.g., "Share product roadmap quarterly"]

**[Account name] commits to:**
- [Customer commitment — e.g., "Assign an internal project champion with time allocation"]
- [Customer commitment — e.g., "Provide feedback within 5 business days of deliverables"]
- [Customer commitment — e.g., "Ensure executive sponsor attends semi-annual reviews"]

If mutual commitments section is left to generic placeholders, flag `[review]` —
a plan without customer commitments isn't co-owned.

---

### 7. How to reach us

| Need | Contact | Channel | Response time |
|------|---------|---------|--------------|
| Day-to-day | [CSM name] | [email / Slack] | [1 business day] |
| Urgent | [Support] | [channel] | [per SLA] |
| Escalation | [CS lead or VP] | [email] | [per escalation matrix] |

---

### 8. Plan history

| Date | Change | Updated by |
|------|--------|-----------|
| [Date] | Initial plan created | [CSM name] |

---

## Review mode (`--review`)

When reviewing a submitted success plan, check:

- [ ] Success criteria are measurable — specific metric, target, evidence source
- [ ] Customer's goals are stated in the customer's language, not product feature language
- [ ] Milestones have owners — not just the CSM
- [ ] Engagement cadence matches configured CS motion
- [ ] Mutual commitments section includes customer commitments, not only CSM
- [ ] Primary value metric from company profile is reflected in criteria
- [ ] No internal health signals or escalation routing in the customer-facing document
- [ ] Plan has a review / update cadence — it's a living document, not a one-time deliverable

Return specific edits with section references.

---

## Reviewer note (internal)

> **⚠️ Reviewer note**
> - **Sources:** [Customer goals: [source] | CRM ✓ live | Document: [doc name, date] | user-provided]
> - **Success criteria source:** [Account-specific from [source] | configured standard template — customize before finalizing]
> - **Data as of:** [timestamp]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sending:** Verify customer has reviewed and agreed to the success criteria in Section 3 before treating this as a mutual plan. Success criteria agreed verbally but not in writing are flagged `[review]`.

---

## Output

Success plan document — format driven by `--draft` (default) or `--review` flag.
Draft mode produces a full structured plan with goals, milestones, metrics, and
owner assignments. Review mode produces a gap analysis against an existing plan.
See **Success plan structure** section for field-level detail.

## Guardrails

**No invented goals.** Do not infer success criteria from product features or
industry benchmarks. Criteria come from stated customer goals. If goals are
unknown, the reviewer note says so explicitly and the plan is marked `[DRAFT]`.

**Co-authorship is the goal.** A plan the customer never saw is an internal CSM
document. The plan is not finalized until the customer sponsor has reviewed and
agreed to the success criteria.

**Quiet mode.** The customer-facing plan contains no internal health scores,
no expansion signal tags, no escalation routing. Those stay in the reviewer note.

**Renewal language.** If the plan covers a period that includes the renewal window,
do not include language that implies renewal likelihood — flag for reviewer
validation before sharing with leadership or finance.

**Primary value metric.** The configured primary value metric from the company
profile must be traceable in the success criteria. If it's absent, flag it.

---

## After the plan

- "Plan drafted. Want to walk through the success criteria with the customer?
  I can prepare talking points. `/csm:call-prep [account] kickoff`"
- "Want to set a milestone review reminder? Run `/csm:renewal-readiness [account]`
  when you reach M5."
- "Ready to build the QBR when M4 or M5 are complete? `/csm:qbr-builder [account]`"
