---
name: churn-analysis
description: >
  Root cause analysis of a closed churn or contraction event — signal timeline
  reconstruction, root cause categorization, lessons captured, and portfolio
  pattern flagging. Surfaces whether the signals that led to this churn are
  present in other active accounts and recommends pre-emptive actions. Use
  within 30 days of a confirmed non-renewal or contraction to capture learning
  before context decays. Distinct from risk-assessment (which acts before churn)
  — this skill acts after the loss to extract structured intelligence.
argument-hint: "[<account-name-or-ID>] [--deep | --quick | --portfolio-scan]"
version: "1.0.0"
---

# /renewals:churn-analysis

Root cause analysis of a closed churn or contraction. Extract what happened,
why it happened, and whether it's about to happen again somewhere else.

---

## Pre-flight

Read both configuration files before running any churn analysis:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in churn-signal
or escalation fields, proceed with a notice:

> "Your churn signal definitions are not configured. The analysis will use
> general SaaS churn patterns. Run `/renewals:cold-start-interview --section
> churn-signals` to configure your specific signals — this will make future
> churn analysis and portfolio scanning more accurate for your product and motion."

Fields read from config:
- Primary churn drivers (configured signals to check against)
- Competitive threats (known displacement patterns)
- Customer segments and average deal size
- Escalation matrix (to assess whether escalation was triggered at the right
  time in the timeline)
- Health score threshold configuration (to assess whether health score
  reflected the churn risk before it was confirmed)

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G1 (health scores and churn signals are heuristics — do not present as predictive certainty).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## This Skill vs. Risk Assessment

**`/renewals:risk-assessment`** — Use when an account is approaching renewal
and you need to assess churn risk in time to act. Output: risk tier, escalation
routing, save options.

**`/renewals:churn-analysis`** — Use after the account has churned or contracted.
Output: what went wrong, when the signals appeared, whether the response was
timely, lessons captured, whether the pattern exists in active accounts.

Running churn analysis on an account that hasn't churned yet is the wrong tool —
route to `/renewals:risk-assessment` instead.

---

## Mode

`--deep` (default): Full analysis — signal timeline, root cause categorization,
response adequacy assessment, lessons captured, and portfolio scan for matching
signal patterns in active accounts.

`--quick`: Abbreviated analysis — primary root cause, two-sentence lesson, and
whether a portfolio scan is warranted. Use when processing multiple losses at
once (e.g., quarter-end retrospective) and full analysis isn't needed for each.

`--portfolio-scan`: Skip the single-account analysis and run the pattern-matching
step across the active book. Use when you already have the root cause from a
prior analysis and need to identify which current accounts share it.

---

## Account identification and event data

Ask: "Which account churned or contracted? Provide the account name, the
confirmed non-renewal or contraction date, the ARR lost, and the stated reason
if captured."

If a CRM connector is available, pull:
- Closed/lost reason from the renewal opportunity
- Account ARR and close date
- Original contract start date (tenure at churn)
- CSM owner history during the account lifecycle
- Support ticket history
- Last meaningful customer contact before churn was confirmed
- Any competitor mentioned in opportunity notes

Confirm the pull:
> "[CRM]: [account name] · $[ARR lost] lost · closed [date] · tenure [N]
> months · reason captured: [yes — '[reason]' | no] · last contact: [date]"

If CRM data is unavailable:
> "Working from what you provide. Tell me: ARR, tenure, reason if known,
> and what you remember about the last 90 days of the relationship."

---

## Signal timeline reconstruction

Build the timeline of signals chronologically — when they first appeared,
when they were noticed, and when action was taken (if it was).

| Date | Signal | Domain | First noticed | Action taken |
|------|--------|--------|--------------|-------------|
| [date] | [specific signal] | [adoption / engagement / support / commercial / renewal posture] | [date first noticed] | [action / none] |

Fill the timeline from:
- CRM activity log (call dates, email dates, opportunity stage changes)
- Call recording timestamps (if connector available)
- Support ticket open/close dates
- Health score history (if CS Platform available)
- User-provided recollection

**Key questions the timeline must answer:**

1. How many days before renewal was the first signal visible?
2. How many days before renewal was the signal noticed by the CSM?
3. Was a risk-assessment run? If so, when, and what tier was assigned?
4. Was an escalation triggered? If so, when?
5. Was the escalation within the SLA configured in the escalation matrix?
6. What was the last action taken before churn was confirmed — and was it
   the right action?

> ⚠️ Timeline lag is a key diagnostic. If the first signal appeared 90 days
> before renewal and action wasn't taken until day 20, the system didn't
> fail — the process did. If the signal appeared at day 20 and wasn't visible
> earlier, that's a signal-coverage gap. These have different fixes.

---

## Root cause categorization

Assign a primary root cause and up to two contributing factors. Use the
configured primary churn drivers where available; otherwise use the standard
taxonomy below.

### Standard root cause taxonomy

**Adoption failure**
The product was deployed but never successfully integrated into the customer's
workflow. Characterized by low active user counts, core features never
activated, and champion feedback that value wasn't realized.

*Sub-types:* Onboarding gap (never properly implemented) / usage plateau
(adopted initially, then declined) / champion-dependent (single user drove
adoption; their departure ended it)

**Relationship gap**
The relationship with the account was too thin or too narrow to survive normal
business turbulence. Characterized by single-threaded relationships, executive
sponsor changes with no backup relationship, or a champion who left without
a handoff.

*Sub-types:* Champion departure without replacement / executive sponsor
change without re-engagement / CSM transition without proper handoff

**Commercial misalignment**
The price-to-value equation failed — either the price increased without
corresponding value realization, or the account's budget was reduced and
the product wasn't protected.

*Sub-types:* Price increase triggered departure / budget cut without save
conversation / contract terms that were never satisfactory

**Product gap**
The product didn't do what the customer needed — either a specific feature
gap, a reliability or performance issue, or a product direction that moved
away from the customer's use case.

*Sub-types:* Feature gap (missing capability) / reliability/performance
issue / roadmap misalignment / integration failure

**Competitive displacement**
A competitor won the account. The loss may have been driven by product gaps,
pricing, or relationship factors — but a competitor captured the replacement.

*Sub-types:* Direct feature replacement / pricing undercut / internal-build
decision / point solution replacing platform

**External / force majeure**
The customer's business changed in a way unrelated to product or relationship
quality: acquisition, company closure, budget elimination, regulatory change,
or team elimination.

---

### Root cause assignment format

> **Primary root cause:** [Category] — [Sub-type]
> **Contributing factors:** [Factor 1] / [Factor 2 if applicable]
>
> **Evidence:** [2–3 specific signals from the timeline that support this
> assignment — not general observations, specific data points]

Do not assign a root cause without evidence. If the evidence is insufficient,
say so:
> "Root cause cannot be reliably determined — [specific data point] is missing.
> The most likely candidate is [category] based on [available evidence], but
> this should be treated as [Low Confidence] until [missing data] is obtained."

---

## Response adequacy assessment

Evaluate whether the CS team's response was appropriate given what was visible.
This is a diagnostic, not a blame assignment.

| Criterion | Assessment | Notes |
|-----------|-----------|-------|
| Signal appeared early enough to act | [Yes — N days before renewal / No — inside [N] days] | |
| Signal was noticed within reasonable time | [Yes / No — N day lag] | |
| Risk assessment was run | [Yes — [date] / No] | |
| Risk tier was accurate | [Yes / No — was [tier], should have been [tier]] | |
| Escalation was triggered | [Yes — [date] / No] | |
| Escalation was within SLA | [Yes / No — SLA was [N] days, triggered at [N] days] | |
| Save strategy was deployed | [Yes — [strategy] / No] | |
| Save strategy was appropriate | [Yes / No — should have been [alternative]] | |

**Summary:**
> "[Account name] churned due to [root cause]. The first signal appeared [N]
> days before renewal. [Action was taken within SLA / action was delayed by
> N days / no escalation was triggered]. The save strategy [was appropriate /
> was insufficient because [reason] / was not deployed]."

This assessment is internal. It surfaces process gaps — signal coverage, SLA
compliance, save strategy selection — that can be improved for future accounts.

---

## Lessons captured

Three to five lessons, each tied to a specific observation from this account.
A lesson must be actionable — it must describe what to do differently, not just
what went wrong.

**Lesson format:**

> **Lesson [N]:** [Label]
> **Observation:** [Specific thing that happened or didn't happen in this account]
> **Root connection:** [How this observation connects to the root cause]
> **Action change:** [What the team should do differently for this class of account]
> **Applicable to:** [Signal type / account segment / tenure stage / CS motion]

> ⚠️ Lessons are not performance notes. They describe process improvements,
> signal gaps, and response timing improvements — not assessments of individual
> CSM performance. If a lesson reveals a systemic gap (e.g., "no escalation
> protocol exists for [signal type]"), flag it for Head of CS review.

---

## Portfolio pattern scan

After completing the single-account analysis, scan the active book for accounts
that share the primary root cause signal pattern.

Ask: "Do you want me to scan your active renewal book for accounts showing
similar signals? This requires either CRM connector access or a list of your
current accounts."

If CRM is available, check active accounts for:
- The same signal combination that drove this churn
- Accounts at a similar tenure stage (churn risk often clusters by tenure)
- Accounts in the same segment or vertical as the churned account
- Accounts with the same root cause sub-type (e.g., single-threaded champion
  relationship, low feature adoption, budget freeze mentioned)

**Portfolio scan output:**

| Active account | ARR | Renewal date | Matching signals | Recommended action |
|---------------|-----|-------------|------------------|--------------------|
| [name] | $[ARR] | [date] | [1-2 signals] | `/renewals:risk-assessment` / monitor / no action |

> ⚠️ Portfolio scan results are leads for risk assessment — not risk tiers.
> An active account with a similar signal pattern requires a full
> `/renewals:risk-assessment` before a risk tier is assigned. Do not use
> portfolio scan output as a substitute for individual account assessment.

If no accounts match:
> "No active accounts show the primary signal pattern from this loss. Either
> the pattern is isolated to this account's circumstances, or the signals
> aren't captured in the current CRM data. Verify data coverage before
> concluding the book is clean."

---

## Output format

---

**Churn Analysis — [Account Name]**
*ARR lost: $[amount] · Closed: [date] · Tenure: [N] months*
*Analyzed: [date] · Analyst: [CSM name from config if available]*
*Sources: [CRM ✓ verified | call recordings | manual input]*

**Root Cause:** [Primary] — [Sub-type]
**Contributing factors:** [Factor 1] / [Factor 2 if applicable]

**Signal Timeline**
[Timeline table]

**Timeline lag:** First signal [N] days before renewal / Noticed [N] days
before renewal / Escalated [N] days before renewal [or not escalated]

**Response Assessment**
[Assessment table with summary]

**Lessons Captured**
[Lesson 1 through [N] in structured format]

**Portfolio scan:** [N accounts flagged for review | No pattern matches found]
[Portfolio scan table if accounts flagged]

**Recommended actions**
1. [Immediate — run risk-assessment on flagged accounts]
2. [Process — share lesson with Head of CS]
3. [Signal — add [signal type] to churn signal config if not present]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | call recordings ✓ verified | manual input]
> - **Data as of:** [timestamp per source | N/A — retrospective analysis]
> - **Root cause confidence:** [High Confidence — multiple supporting signals /
>   Moderate — one supporting signal, others inferred / Low Confidence — reason]
> - **Flagged for your judgment:** [Items where evidence is insufficient for
>   confident root cause assignment | none]
> - **Before sharing:** This analysis contains ARR and account health data —
>   confirm the recipient is authorized to see this account's information.
>   Lessons section is safe to share with the broader team without
>   account-specific data attached.

---

> [review before sending]

## Guardrails

**Analysis, not attribution.** Churn analysis identifies process gaps and
signal patterns — it does not assess or imply individual performance. Lessons
surface what to do differently, not who failed. If a lesson surfaces a systemic
gap, route it to Head of CS — not into a performance conversation.

**Root cause requires evidence.** Do not assign a root cause category without
specific, named evidence from the account timeline. An inferred root cause must
be labeled `[Low Confidence]` and noted as requiring verification.

**Portfolio scan is a lead generator, not a risk tier.** Any active account
surfaced by the portfolio scan requires a full `/renewals:risk-assessment`
before a risk tier is assigned or an escalation is triggered.

**Timing lag is diagnostic data.** The gap between when a signal first appeared
and when it was noticed is process intelligence — not fault assignment. Surface
it honestly; use it to improve signal coverage and escalation SLAs.

**Confidentiality.** Churn analysis contains account ARR, relationship health,
and stakeholder details. Lessons can be shared broadly (stripped of account-
specific data); the full analysis requires recipient authorization.

**Distinguish controllable from uncontrollable.** External/force majeure churn
(acquisition, company closure, regulatory change) is not a process failure. Flag
it as uncontrollable and confirm that the loss shouldn't drive process changes
that address a problem the team couldn't have solved. Don't over-index on
uncontrollable losses when designing prevention systems.

**Retrospective window.** The analysis is most accurate within 30 days of
the churn event — context decays quickly. Flag analyses run more than 60 days
after close:
> "⚠️ This analysis is being run [N] days after the churn event. Recollections
> may be incomplete and CRM data may have been modified. Treat the timeline
> reconstruction as [Moderate] confidence unless corroborated by call recordings
> or timestamped CRM entries."
