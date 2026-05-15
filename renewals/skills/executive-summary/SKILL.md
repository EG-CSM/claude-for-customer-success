---
name: executive-summary
description: >
  Generate an executive-ready renewal summary for a strategic account — written
  for CRO, CEO, or board consumption. Surfaces commercial status, relationship
  health, risk tier, save strategy, and recommended executive action in a format
  calibrated for leaders who need the bottom line without raw signal data.
  Suppresses internal positioning, walk-away figures, and operational detail from
  the output. All ARR figures flagged for Finance/RevOps review before distribution.
  Use for strategic accounts requiring executive sponsorship, escalated renewals,
  or board/investor reporting packages.
argument-hint: "[<account-name-or-ID>] [--brief | --full | --board]"
version: "1.0.0"
---

# /renewals:executive-summary

Strategic account renewal summary calibrated for executive audiences.

---

## Pre-flight

Read both configuration files before building any executive summary:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in fields this
skill requires (GRR/NRR targets, customer segments, escalation matrix,
company name, executive contacts), stop:

> "Your renewals practice profile isn't configured — specifically the company
> profile and executive contact fields. Run `/renewals:cold-start-interview`
> to configure these. An executive summary built without your actual targets
> and company context will require significant manual editing before it's
> usable."

Fields read from config:
- Company name and brand (for header)
- Customer segments and deal size tiers (for strategic account qualification)
- GRR and NRR targets (for target gap framing)
- Escalation matrix — Head of CS, CRO, CEO contacts (for recommended action)
- AE partner (for co-sponsorship context)
- Negotiation posture (affects how risk and save strategy are framed)

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G3 (revenue and forecast figures carry commitment language + Finance validation callout), G5 (confidentiality check before distributing portfolio-level financial data).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## What makes an account eligible for executive summary

An executive summary is warranted when one or more of the following applies:
- ARR at or above the strategic account threshold configured in your profile
- Account is at High or Critical risk tier (from `/renewals:risk-assessment`)
- Executive escalation has been requested by either side
- The renewal requires CRO or CEO involvement to close
- The account is being included in board or investor materials
- A competitor displacement threat is confirmed

If none of these apply:
> "This account doesn't appear to meet the strategic account threshold for
> an executive summary. Consider `/renewals:negotiation-prep` or
> `/renewals:risk-assessment` instead — or confirm that executive visibility
> is needed here before proceeding."

---

## Mode

`--brief` (default): One-page executive summary — commercial status, risk
tier, key relationship signals, recommended executive action, and one clear
ask. Appropriate for CRO weekly review or escalation routing brief.

`--full`: Extended summary — all `--brief` content plus competitive context
(if applicable), relationship timeline, value delivered summary, and proposed
executive engagement plan. Appropriate for accounts requiring active executive
co-sponsorship or QBR preparation with the customer's executive.

`--board`: Board or investor format — narrows to: ARR at stake, risk level,
current trajectory, and one recommended action. No customer-specific relationship
detail. Uses only language appropriate for board audiences. Appropriate for
board materials, investor briefings, and strategic account portfolio summaries.

---

## Account identification and data pull

Ask: "Which account is this executive summary for? Provide the account name,
and tell me the ARR, renewal date, current risk tier (if known), and any
signals you want me to include."

If a CRM connector is available, pull:
- ARR and product tier
- Renewal date and days remaining
- Opportunity stage
- Escalation history (prior escalations, who was involved, outcomes)
- Executive sponsor and champion records
- Open support tickets or unresolved escalations
- Prior renewal history (tenure, prior renewals, expansion history)

If a risk assessment has already been run:
> "Import the risk tier from `/renewals:risk-assessment` output if available —
> this summary should reflect the same tier, not re-derive it independently."

Confirm the pull:
> "[CRM]: [account name] · $[ARR] · renewal [date] · [N] days out ·
> risk tier: [Critical/High/Medium/Low from risk-assessment or 'not yet assessed']
> · data as of [timestamp]"

---

## Executive summary content — `--brief`

The brief format is a single-page document structured for a 90-second read.
Every section should be answerable in 1–3 sentences. Do not pad.

---

### Section 1 — Bottom line

State the commercial situation and recommended executive action in two sentences.
This is the first thing the executive reads; it must stand alone if they read
nothing else.

> "[Account name] ($[ARR]) renews [date] and is currently [on track / at risk
> / in active negotiation / escalated]. The recommended executive action is
> [specific: e.g., 'a call from [CRO name] to [Economic buyer name] this week'
> / 'executive sponsor engagement before [date]' / 'no action needed at executive
> level at this time']."

---

### Section 2 — Commercial status

| Field | Value |
|-------|-------|
| Current ARR | $[amount] |
| Proposed renewal ARR | $[amount] [flat / +X% increase / -X% contraction risk] |
| Renewal date | [date] — [N] days out |
| Renewal stage | [Open / Verbal commitment / At risk / In negotiation] |
| Risk tier | [Critical / High / Medium / Low] |
| GRR contribution | $[amount] `[review — not yet a revenue commitment]` |

---

### Section 3 — Relationship health

Surface the signals an executive needs — not the full domain breakdown from
risk-assessment. Keep to what's relevant for the executive action being
recommended.

> **Champion:** [Name, title] — [engaged / disengaged / recently changed]
> **Economic buyer:** [Name, title] — [aware of renewal / not yet engaged / leading negotiation]
> **Executive sponsor:** [Name, title] — [active / departed / not yet identified]
>
> **Key signal:** [One sentence — the single most important relationship fact
> the executive should know. Examples: "The economic buyer is new and hasn't
> built a relationship with our team." / "The champion left 60 days ago and has
> not been replaced." / "The executive sponsor has been vocal about value."]

---

### Section 4 — Risk summary

If risk tier is Low or Medium:
> "No executive action required. CSM is managing the renewal through the
> standard motion. [1 sentence on what would change this assessment.]"

If risk tier is High or Critical:
> "**Risk drivers:** [2–3 specific signals — not domain summaries, specific
> data points. Examples: 'Login activity dropped 40% in 90 days' / 'Competitor
> evaluation confirmed by champion on [date]' / 'No executive sponsor contact
> in 120 days']"
>
> "**Current save strategy:** [What the CSM is doing — specific, not generic]"
>
> "**What executive involvement changes:** [Specific: what an executive call or
> email from [name] accomplishes that the CSM cannot. Don't ask for executive
> involvement without a specific reason.]"

---

### Section 5 — Recommended executive action

State the action clearly. One of:

**Outreach ask:** "[CRO / CEO / Head of CS] — a [call / email] to [Economic
buyer name / Executive contact] by [date]. Purpose: [specific: relationship
check-in / strategic partnership signal / negotiation support]. Draft available
on request."

**Sponsorship ask:** "[Executive name] to join the [renewal call / QBR /
executive briefing] scheduled for [date]. Objective: [re-establish relationship /
signal strategic commitment / close the negotiation]."

**No action needed:** "No executive action required at this time. The renewal
is [on track / in negotiation within authority]. Next checkpoint: [date]."

**Escalation confirmation:** "This account is already escalated to [owner]. The
executive ask is to [authorize the save offer / directly engage the customer's
[title] / accelerate the decision timeline]."

---

### Section 6 — One clear ask

End with a single, time-bounded ask:

> **Ask:** [Specific action] by [date].

This is not a summary of the summary. It's the one thing the executive needs
to decide or do.

---

## Additional sections — `--full` mode

In `--full` mode, add after Section 6:

### Value delivered summary

2–4 sentences on what the customer has realized from the product. Specific,
data-backed, account-specific. No generic value language.

> "[Account name] has [specific adoption milestone / outcome / ROI evidence].
> [Usage data: X active users, Y% adoption of [feature], Z workflows enabled].
> [Business outcome if available: time saved, revenue impacted, efficiency gain]."

If data is unavailable:
> "[Value delivered data is not available from connected systems. Fill this
> section before sharing — generic value language will reduce the summary's
> credibility with an executive audience.]"

### Competitive context (if applicable)

Only include if a competitor evaluation is confirmed.

> "[Competitor name] is in an active evaluation. The evaluation was [triggered
> by / confirmed by] [source — champion mention / procurement RFP / call
> recording]. Our current positioning advantage: [specific]. The risk: [specific].
> Executive engagement helps because: [specific]."

Do not fabricate competitive intelligence. If not confirmed, omit.

### Proposed executive engagement plan

If executive sponsorship is recommended, provide a structured engagement plan:

| Step | Action | Owner | By when |
|------|--------|-------|---------|
| 1 | [Specific first action] | [Executive name] | [date] |
| 2 | [Follow-on action] | [CSM + Executive] | [date] |
| 3 | [Close action] | [CSM] | [date] |

---

## Board format — `--board` mode

Board format uses only aggregate or anonymized data appropriate for external
audiences. It does not include customer-specific relationship detail.

---

**Strategic Account Alert — [Your Company Name]**
*Prepared for: Board / Investor Review*
*Period: [date]*

| Field | Detail |
|-------|--------|
| Account (anonymized if required) | [Name or "Strategic Account [A/B/C]"] |
| ARR at stake | $[amount] `[review — not yet a revenue commitment]` |
| Renewal date | [date] |
| Risk level | [Critical / High / Medium] |
| Current trajectory | [On track / At risk / In negotiation] |
| Recommended action | [One sentence] |
| GRR impact if lost | -[%] from [segment] GRR target |

> ⚠️ Board materials note: All ARR figures require Finance/RevOps review before
> inclusion in board packages. Do not include an account-level ARR figure in
> board materials without confirming it represents the correct renewal scenario
> and hasn't been superseded by a signed amendment.

---

## Output format — Brief (`--brief`)

---

**Renewal Executive Summary — [Account Name]** *(internal — do not share)*
*ARR: $[amount] · Renewal: [date] · [N] days out · Risk: [tier]*
*Prepared: [date] · For: [CRO / CEO / Head of CS]*

**Bottom line:** [2 sentences]

**Commercial status:** [Table]

**Relationship health:** [Champion / Economic buyer / Executive sponsor / Key signal]

**Risk summary:** [Risk drivers + save strategy + what executive involvement changes]

**Recommended executive action:** [Specific action]

**Ask:** [Single time-bounded ask]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | risk-assessment imported | manual input]
> - **Data as of:** [timestamp]
> - **Risk tier source:** [risk-assessment run [date] / estimated from signals / not yet assessed]
> - **ARR figures:** `[review — not yet a revenue commitment]` — Finance/RevOps
>   review required before distributing to leadership or including in board materials
> - **Flagged for your judgment:** [Value delivered section requires account data /
>   competitive context unconfirmed / executive contacts need verification | none]
> - **Before distributing:** Confirm the recipient is authorized for this account's
>   ARR data. Confirm ARR figure reflects the current renewal scenario.

---

## Guardrails

**Executive asks must be specific.** An executive summary that asks for
"executive involvement" without naming the specific person, action, and date
is not useful — it will sit unread. Every summary must name who, what, and when.

**Value claims require evidence.** The value delivered section must contain
specific, account-sourced data — not generic value statements. If data is
unavailable, flag the section for manual completion before sharing. Do not
fabricate value evidence.

**Competitive intelligence must be confirmed.** Include competitive context
only when a competitor evaluation has been confirmed via call recording, CRM
notes, or direct customer communication. Do not infer competitive risk from
general market dynamics.

**Revenue commitment language.** All ARR figures in this output require
Finance/RevOps review before distribution to leadership or board audiences.
Flag every ARR figure with `[review — not yet a revenue commitment]`.

**Internal content stays internal.** The `--brief` and `--full` outputs are
internal. They contain risk tier, walk-away context (if imported), and
relationship health data not intended for the customer. Do not share the
summary with the customer — generate a `/renewals:negotiation-prep --export`
for customer-facing renewal proposals.

**Board format requires explicit authorization.** Do not generate `--board`
output without confirming that account-level data is authorized for board
distribution. Use anonymized account labels if account identity hasn't been
authorized for external sharing.

**Executive asks go up, not sideways.** An executive summary is a request
for executive sponsorship — it routes to Head of CS, CRO, or CEO depending
on the situation. It does not route to peers or AE partners (those requests
go through standard channels). Confirm the escalation path with the configured
escalation matrix before sending.
