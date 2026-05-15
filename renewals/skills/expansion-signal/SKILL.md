---
name: expansion-signal
description: >
  Identify and qualify expansion signals in a renewal account — seat growth,
  usage expansion, product line upsell, and adjacent team opportunities. Maps
  each signal to a qualification tier (early signal / pipeline-ready / qualified)
  and recommends a TARO play for conversion. Use during pre-renewal research,
  QBR prep, or after an adoption milestone to surface upsell and cross-sell leads.
  Expansion leads are never included in GRR calculations and require a qualifying
  economic buyer conversation before entering NRR pipeline.
argument-hint: "[<account-name-or-ID>] [--deep | --quick | --catalog]"
version: "1.0.0"
---

# /renewals:expansion-signal

Surface and qualify expansion signals in a renewal account. Every signal found
here is a lead until proven otherwise.

---

## Pre-flight

Read both configuration files before analyzing any account:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in the pricing,
renewal book, or methodology sections, stop and route to
`/renewals:cold-start-interview`. Without pricing model, product structure, and
configured NRR target, expansion signal outputs will be untethered from your
actual commercial posture.

Fields read from config:
- Pricing model (per seat / usage-based / flat fee / tiered / hybrid)
- Product line or tier structure (from company profile)
- NRR target
- Customer segments and average deal size
- AE partner (for expansion handoff routing)
- Configured TARO playbook sources / SuccessCOACHING methodology flag

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G2 (expansion ARR is not counted until an economic buyer has been qualified).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--deep` (default): Full signal audit across all expansion domains with
qualification tier assignment, TARO play mapping, and recommended next actions.
Pulls live data when connectors are available.

`--quick`: Targeted pass — asks 4–5 focused questions to surface the highest-
probability expansion signal in the account and recommend one immediate action.
Use when you have limited prep time before a renewal call.

`--catalog`: List all expansion signal types the skill can detect for the configured
pricing model, with descriptions and qualifying questions for each. Use to educate
the team or build a pre-call checklist.

---

## Account identification and data pull

Ask: "Which account are you researching for expansion signals? Provide the account
name, and tell me ARR, renewal date, and current product tier/license count if you
have them."

If a CRM connector is available, pull:
- Current ARR and product tier
- Contract seat count or usage limit
- Contract start date and renewal date
- Expansion history (prior upsell or cross-sell events and dates)
- Open expansion opportunities in pipeline

If a CS Platform connector is available, pull:
- Active user count vs. licensed seat count
- Product feature adoption breadth (which modules are in use)
- Team or department breakdown of active users
- Usage trend (growing / flat / declining) over last 90 days
- Any usage-based overage or approaching limit signals

Confirm data pull before proceeding:
> "[CRM + CS Platform]: [account name] · $[ARR] ARR · [N] licensed seats / [N]
> active users · [module adoption] · data as of [timestamp]"

---

## Signal catalog — six expansion types

Evaluate each signal type based on data pulled or user input.

### 1. Seat expansion
- Active users approaching or exceeding licensed seat count
- New team members onboarded since last renewal not yet on license
- Departments using product via shared credentials (workaround for unlicensed seats)
- Recent hiring activity in teams using the product

Qualifying question to surface: "Are there users at this account accessing the
product outside of licensed seats, or departments that would benefit from access
but aren't currently licensed?"

### 2. Usage-based expansion (usage-model accounts only)
- Usage approaching or exceeding contracted volume limit
- Recent consumption spike vs. prior period
- Seasonal usage pattern suggesting coming overage
- Usage growing faster than contracted tier covers

Qualifying question: "Their usage is at [N]% of contracted volume — have you
discussed an upgrade conversation or are they managing to stay under the cap?"

### 3. Product tier or feature upsell
- Core tier features fully adopted; advanced tier features not unlocked
- Customer requesting features that exist in a higher tier
- Feature gap expressed in support tickets or CSM notes
- Recent product release unlocking new tier features customer has expressed interest in

Qualifying question: "Which features are they asking about that they don't
currently have access to?"

### 4. Multi-product or cross-sell
- Adjacent product line that addresses a problem mentioned in calls or QBRs
- Integration between current product and a new product line customer could benefit from
- Customer currently solving a problem with a competitor product or manual process
  that your product line addresses

Qualifying question: "Is there a workflow they're handling manually or with a
point solution that [product] could replace?"

### 5. Geographic or team expansion
- New office, region, or subsidiary not yet on the product
- M&A activity — acquisition target not yet onboarded
- Separate team or business unit at the same company evaluating independently

Qualifying question: "Are there other teams or offices at this account that
aren't currently on the product?"

### 6. Professional services or implementation
- Complex use case mentioned that requires configuration or integration support
- Customer building internal workarounds that a services engagement could replace
- Expansion of use case scope that warrants a new implementation project

Qualifying question: "Are they building something internally that your PS team
would normally handle?"

---

## Qualification tier assignment

For each signal identified, assign a qualification tier:

| Tier | Definition | NRR treatment | Next action |
|------|-----------|--------------|-------------|
| **Early signal** | Data or conversation suggests expansion need; no economic buyer conversation yet | `[early signal — not yet qualified]` — not in NRR | Validate with champion; set qualifying conversation goal |
| **Pipeline-ready** | Champion has confirmed interest; economic buyer awareness but no commitment | `[early signal — not yet qualified]` — not in NRR | Book qualifying conversation with economic buyer |
| **Qualified** | Economic buyer has confirmed interest or approved expansion budget; expansion is in formal pipeline | Include in NRR forecast; create CPQ quote or opportunity | Route to AE partner; build expansion proposal |

> **Signal qualification rule (non-negotiable):** Expansion signals are tagged
> `[early signal — not yet qualified]` unless an economic buyer conversation has
> occurred AND the expansion has moved to formal pipeline (CPQ quote, opportunity
> stage, or written commitment). Do not include unqualified signals in NRR figures.

---

## TARO play recommendation

For each qualified or pipeline-ready signal, recommend a TARO play:

**Trigger:** The specific adoption, usage, or need signal that makes this expansion
timely and relevant to surface now.

**Action:** The recommended play — reference configured playbook if available.
Common expansion plays: Adoption milestone review → tier upgrade conversation;
Usage approaching limit → proactive expansion proposal; Adjacent team discovery →
multi-product introduction.

**Resource:** What to bring to the expansion conversation. Consider:
- Usage data showing value delivered to current team
- ROI evidence or case study relevant to the expanding use case
- Product roadmap items relevant to expanded tier or cross-sell product
- Pricing and packaging options within your configured discount authority

**Outcome:** Observable state marking the play successful (expansion opportunity
created in CRM / CPQ quote generated / economic buyer meeting scheduled /
expansion contract signed).

> TARO play recommendations are leads, not mandates. Validate the trigger against
> what you know from direct account experience before executing.

---

## AE handoff guidance

For any signal at Pipeline-ready or Qualified tier, note the AE handoff:

> "Expansion signals at [pipeline-ready / qualified] tier should be routed to
> [AE partner from config] for the commercial conversation. Prepare:
> - Account context brief (current ARR, expansion signal, qualifying conversation summary)
> - Proposed expansion scope (seats / tier / product)
> - Draft pricing or CPQ input within your configured parameters
> - Recommended timing relative to renewal date"

If no AE partner is configured:
> "No AE partner is configured in your practice profile. Run
> `/renewals:cold-start-interview --section team` to add your AE contact."

---

## Output format

---

**Expansion Signal Report — [Account Name]**
*ARR: $[amount] · Renewal: [date] · [N] days out*
*Analyzed: [date] · Sources: [list]*

**Expansion signals found: [N]**

| Signal type | Tier | ARR potential | Qualifying question answered? |
|-------------|------|--------------|-------------------------------|
| [Type] | [Early / Pipeline-ready / Qualified] | $[estimate] `[early signal — not yet qualified]` | [Y / N] |

> Note: ARR potential figures are estimates `[Low Confidence]` until a formal
> expansion proposal is built and reviewed with the economic buyer.

**Signal detail**

*[For each signal: 2–3 sentences on what was observed, why it indicates expansion,
and what the immediate next step is.]*

**TARO play recommendations**

*[For pipeline-ready and qualified signals: Trigger / Action / Resource / Outcome]*

**AE handoff items**
*[What to prepare for AE routing, if applicable]*

**Next actions**
1. [Specific action for highest-probability signal]
2. [Qualifying conversation goal]
3. [AE handoff item, if applicable]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | CS Platform ✓ verified | call notes | manual input]
> - **Data as of:** [timestamp per source | N/A]
> - **Read:** [account record | usage data | expansion history | [N] call notes]
> - **Flagged for your judgment:** [N items — expansion qualification tiers pending
>   buyer conversation | none]
> - **Before including in NRR forecast:** Validate qualification tier for each signal —
>   `[early signal — not yet qualified]` signals must NOT appear in NRR figures

---

> [review before sending]

## Guardrails

**Expansion requires qualification.** Every expansion signal is tagged
`[early signal — not yet qualified]` until an economic buyer conversation has
occurred and the expansion is in formal pipeline. This tag is not removed by
champion confirmation alone. This guardrail cannot be overridden by configuration
or conversation.

**ARR potential estimates are speculative.** Expansion ARR estimates before a
formal proposal are `[Low Confidence]`. Do not present them as committed pipeline.
Flag any estimate that could be read as a revenue forecast.

**Expansion is not included in GRR.** GRR calculations never include expansion
ARR. This is mathematically correct and a shared guardrail — never include
expansion in a GRR projection regardless of how the expansion is framed.

**AE routing on qualified signals.** For any signal that reaches Qualified tier,
the commercial conversation routes to the AE partner. The renewals manager owns
the signal identification and qualification handoff; the AE owns the commercial
conversion unless configured otherwise.

**Renewal risk first.** If the account also has active churn risk signals,
surface them before expansion signals and recommend `/renewals:risk-assessment`
before pursuing expansion. An at-risk account's priority is renewal, not growth.
