---
name: value-statement
description: >
  Build a value statement for an account — what value has been realized, against
  which success criteria, with what evidence. Use before a QBR, executive check-in,
  renewal conversation, or when preparing an expansion signal handoff to the AE.
  Produces two versions: an internal analysis (with health signals and expansion
  context) and a customer-facing value narrative (clean, evidence-based, no internal
  data). Distinct from qbr-builder: this skill isolates the value story without
  the full QBR structure.
argument-hint: "[account name] [--internal | --customer | --exec-brief | --ae-handoff]"
version: "1.0.0"
---

# /value-statement

Articulate the value this account has received — in their terms, with evidence,
calibrated to the audience.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to apply:
- Primary value metric — the configured north-star measure of customer success
- Success criteria model — account-specific or standard template
- CS motion — shapes narrative depth and audience framing
- Value categories configured for the company (e.g., efficiency, risk reduction,
  revenue impact, cost savings, user experience)

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of value statement request is this?
   - **Evidence-Rich ROI Narrative** — account has quantitative data and agreed success criteria; build a metrics-backed value story
   - **Criteria-Gap Value Framing** — no formal success criteria exist; infer value from usage signals and flag every claim as unvalidated
   - **Renewal-Context Value Defense** — value statement serves an upcoming renewal; lead with strongest verified outcome, acknowledge gaps honestly
   - **Expansion-Signal Packaging** — value statement supports an AE handoff; separate proven ROI from speculative expansion signals
   - **Executive Visibility Summary** — C-level audience; prose-only, 2-3 headline outcomes with one number each, under 400 words

2. **CONSTRAINTS**: What limits the solution space?
   - Value claims require evidence with source annotation — unsupported claims get `[review]` or are omitted from customer output
   - Expansion signals never appear in customer-facing output under any circumstances
   - Revenue implications (ARR trajectory, renewal probability) require reviewer validation before distribution
   - Customer-facing output uses the customer's business language, not product terminology
   - Success criteria gaps must be acknowledged explicitly — never construct post-hoc success framing silently

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - Are the success criteria sourced from an agreed document (success plan, kickoff, prior QBR), or are they inferred? If inferred, flag before proceeding.
   - Does every metric map to a goal the customer actually stated, or is it a product adoption proxy dressed as customer value?
   - Is the data current enough to stake a conversation on? (Usage >30 days old is directional; NPS >90 days is stale.)

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Metric dump without narrative — tables of numbers the customer cannot interpret as business value
   - Proxy metric substitution — reporting DAU when the customer's goal was cost reduction
   - Gap hiding in renewal context — omitting known underperformance the customer already sees
   - Signal-as-opportunity leap — treating a champion's casual mention as a qualified expansion opportunity
   - Feature-language leakage — using product names in customer-facing or exec-level output
   - Confidence inflation — presenting single-source or anecdotal evidence with the same certainty as verified outcomes

**After execution**, verify:
- Does the output answer the implicit question the CSM is asking?
- Are all data sources timestamped and staleness-flagged?
- Is the output mode matched to the actual need?
- Confidence: [High] if 2+ live sources corroborate / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

## Mode

`--internal`: Full value analysis for CSM use — health signals included, expansion
signals tagged, source annotations on every value claim. **Default.**

`--customer`: Clean, customer-facing value narrative. Evidence-based. No internal
health data, no expansion signals, no source annotations. Appropriate to share
directly or embed in a deck or email.

`--exec-brief`: 1-page executive summary version of the customer-facing statement.
Built for a C-level audience. No metrics tables — prose narrative with 2-3 headline
outcomes. Under 400 words.

`--ae-handoff`: Expansion-signal handoff package for the AE/AM. Internal. Includes
qualified expansion signals, account health context, and CSM-recommended next step
for the commercial conversation.

---

## Data gathering

**First, check if account-research or qbr-builder ran this session.** Use that
context rather than re-pulling from connectors.

**If not, pull from connected integrations:**
- CS Platform: product usage trends, milestone completion, feature adoption
- CRM: ARR, contract terms, stakeholder contacts, prior value conversation notes
- Document storage: existing success plan, prior QBR, kickoff notes
- NPS: most recent score and verbatim if available

**Success criteria source:** From configured success criteria model, or from a
connected success plan document. If neither is available:

> "To build a meaningful value statement, I need this account's agreed success
> criteria. What did the customer say they wanted to accomplish — at kickoff,
> in their success plan, or in a prior QBR? Paste the criteria or describe them."

If no criteria are available: build with usage and engagement signals, flag every
value claim as `[review — not validated against agreed success criteria]`, and
recommend establishing criteria as an explicit action.

---

## Internal value analysis (`--internal`)

---

**Value Analysis — [Account Name]**
*[Date] · INTERNAL — not for distribution*

---

**Account snapshot**

| Field | Value |
|-------|-------|
| ARR | $[amount] |
| Renewal | [date] — [N] days |
| Segment | [segment] |
| Health | [Red / Yellow / Green] |
| CS motion | [High-touch / Tech-touch / Hybrid] |
| Primary value metric | [configured metric] |

---

**Value realized — against success criteria**

For each agreed success criterion, show current status:

| Success Criterion | Target | Actual | Status | Evidence source |
|-------------------|--------|--------|--------|----------------|
| [Criterion 1] | [metric] | [result] | ✅ / 🟡 / ⛔ / ⏳ | [CS Platform / CRM / self-reported] |
| [Criterion 2] | | | | |
| [Primary value metric] | [configured target] | [actual] | | |

If success criteria are unknown: replace with "signals observed" framing.

---

**Value narrative (internal)**

Interpret the table in 3-5 sentences. Go beyond restating the data.

> "The account has achieved [Criterion 1] — their team activated [N] users
> in [feature], which directly addressed the onboarding bottleneck they described
> at kickoff. [Criterion 2] is partial: they've reached [X%] of target, but
> adoption of [specific feature] is lagging; champion's last call indicated
> [reason]. The primary value metric — [configured metric] — is at [result],
> which [beats / misses / meets] the agreed target. The overall value story
> is strong but has one gap that should be addressed before the renewal
> conversation leads with outcomes."

---

**Value by configured category**

| Category | Evidence | Strength |
|----------|----------|---------|
| [e.g., Efficiency] | [Specific metric or outcome — sourced] | [Strong / Partial / Weak / Unknown] |
| [e.g., Risk reduction] | [Specific metric or outcome] | |
| [e.g., Revenue impact] | [Specific metric or outcome] | |
| [e.g., User experience] | [Specific metric or outcome] | |

Only populate categories where evidence exists. Do not invent value claims.

---

**Expansion signals (internal — not for customer-facing output)**

List any signals that indicate potential for expansion. Tag each as
`[early signal — not yet qualified]`.

- [Signal 1 — e.g., "Champion mentioned [adjacent team] is evaluating a similar
  workflow — not a formal request yet"] `[early signal — not yet qualified]`
- [Signal 2 — e.g., "Usage of [feature] is at 94% of licensed capacity —
  potential seat expansion"] `[early signal — not yet qualified]`

If none: "No expansion signals in available data."

Expansion signals go to the AE. Do not include in customer-facing value output.
Use `--ae-handoff` to build the handoff package.

---

**Open items that weaken the value story**

Things that should be resolved before using this value statement in a customer
conversation:

| Item | Impact | Recommended action |
|------|--------|-------------------|
| [e.g., NPS from 6 months ago] | [Stale sentiment — may not reflect current state] | [Request updated NPS before renewal conversation] |
| [e.g., Criterion 2 below target] | [Customer may not view this as full value delivery] | [Understand root cause; include in plan for next quarter] |

---

## Customer-facing value narrative (`--customer`)

---

**What we've accomplished together — [Account Name]**
*[Quarter / date range]*

---

This document captures the value [Account name] has realized from [product] over
[period], measured against the outcomes [Account name] said mattered at the start
of [project/engagement/quarter].

---

**Your outcomes — what you said you wanted**

[Customer goal 1 — in their words, not product language]

[Customer goal 2]

---

**What we delivered — evidence**

**[Outcome 1 — headline]**

[2-3 sentences. Specific. Sourced. In the customer's business language, not
product language. Example: "Your team now processes [N] [workflows] per week,
compared to [baseline] before implementation — a [%] improvement that [business
impact the customer described]."]

Source: [CS Platform / customer-reported / [specific data source]]

**[Outcome 2 — headline]**

[2-3 sentences.]

---

**[Primary value metric — configured]:** [Result vs. target]

[If achieved: 1 sentence on what this means for their business.]
[If not yet achieved: 1 sentence on trajectory and what's needed to reach it.]

---

**What's next**

[1-2 sentences on the next value horizon — what success looks like in the next
quarter. Forward-looking, based on agreed success criteria. Not a feature roadmap.]

---

> **Note:** Remove source annotations before sharing. Verify all figures against
> current data before distribution. Do not include health scores, expansion signals,
> or internal account notes in the customer-facing version.

---

## Executive brief (`--exec-brief`)

---

**[Account Name] — Value Summary**
*Prepared by [CSM name] · [Date]*

[2-3 sentences establishing the business context. What the company was trying
to do when they partnered with [product]. Keep it in their language.]

**What's working:**
[Headline outcome 1 with a specific number. One sentence.]
[Headline outcome 2. One sentence.]
[Headline outcome 3 if applicable. One sentence.]

**What we're focused on next:**
[One forward-looking sentence on next-period priorities. Not a feature list.]

[Optional closing sentence reinforcing partnership — genuine, not promotional.]

---

*[Company name] · [CSM name] · [contact]*

---

## AE handoff package (`--ae-handoff`)

For internal use. Route to AE/AM — not to the customer.

---

**Expansion Signal Handoff — [Account Name]**
*[Date] · INTERNAL · Route to: [AE/AM name]*

**CSM:** [name]
**Account health:** [Red / Yellow / Green]
**Renewal:** [date] — [N] days

---

**Why I'm flagging this now**

[1-2 sentences. What specific signal triggered this handoff. Why now is the right
moment to have the commercial conversation.]

---

**Expansion signals**

| Signal | Evidence | Confidence | Recommended approach |
|--------|----------|-----------|---------------------|
| [Signal 1] | [Specific evidence] | [High / Medium / Low] | [Commercial angle] |
| [Signal 2] | | | |

**Important:** These are unqualified signals at this point. The AE should validate
them directly with the customer. The CSM has not made any expansion commitment or
implied pricing.

---

**Value context for the commercial conversation**

[2-3 sentences on realized value. What has the customer achieved? What's the
strongest outcome to reference as proof of ROI before discussing expansion?]

---

**Stakeholder context**

| Name | Role | Engagement | Notes |
|------|------|------------|-------|
| [Champion] | [Role] | [Active / Declining] | [Relevant note for expansion conversation] |
| [Exec sponsor] | [Role] | [Active / Declining] | [Relevant note] |
| [Economic buyer if known] | | | |

---

**CSM recommended next step for AE**

[Specific ask — e.g., "Schedule a 30-minute call with [champion name] to
explore [use case]. I'll be on the call to anchor on realized value before
you introduce the expansion topic. Avoid leading with pricing — they're still
in the trust-building phase with the platform."]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live | CRM ✓ live | success plan from [date] | user provided | conversation context only]
> - **Success criteria source:** [Account-specific from [source] | configured standard template | CSM-provided — verify with customer before using in customer-facing communication]
> - **Value claims:** [Sourced from data — see inline annotations | CSM-reported — not independently verified]
> - **Data as of:** [timestamp per source]
> - **Expansion signals:** [In internal version only — not in customer-facing output]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]

---

## Output

Value statement output — format driven by flag (`--internal`, `--customer`,
`--exec-brief`, `--ae-handoff`). Ranges from internal analysis with ROI evidence
to customer-facing narratives to AE handoff packages. See mode-specific sections
for field-level structure.

## Guardrails

**Value claims require evidence.** A claim without a source is not a value claim.
Flag unsupported claims `[review]` in the internal version; omit from customer-facing
output until verified.

**Customer language for customer output.** The customer-facing narrative uses the
customer's words for their goals — not the product's feature names or the CSM's
internal categorization.

**Expansion stays internal.** Expansion signals appear only in the internal analysis
and AE handoff. They do not appear in customer-facing value output under any
circumstances.

**No revenue implications without validation.** If the value statement implies
ARR trajectory, renewal probability, or revenue impact, flag for reviewer validation
before sharing with leadership or finance.

**Criteria gap acknowledgment.** If success criteria were never formally agreed,
the value statement says so explicitly rather than constructing a post-hoc success
frame. Propose establishing criteria as a next action.

---

## After the statement

- "Customer-facing version ready — embed in a QBR: `/csm:qbr-builder [account]`"
- "Expansion signals confirmed — build the AE handoff: use `--ae-handoff` mode"
- "Preparing for a renewal conversation — run: `/csm:renewal-readiness [account]`"
- "Executive brief for exec check-in — add call prep: `/csm:call-prep [account]`"
