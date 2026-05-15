---
name: risk-assessment
description: >
  Structured churn risk assessment for a single renewal account. Aggregates
  signals across product usage, engagement, support history, sentiment, and
  relationship health into a risk tier (Low / Medium / High / Critical) with
  an escalation routing recommendation and TARO play suggestion. Use at the
  90/60/30-day outreach windows, when a churn signal is detected, or when an
  account needs triage before a pipeline review. Pulls live data from CRM and
  CS Platform when connectors are available.
argument-hint: "[<account-name-or-ID>] [--deep | --quick | --triage]"
version: "1.0.0"
---

# /renewals:risk-assessment

Structured risk assessment for a renewal account — signals, tier, escalation path,
and recommended play.

---

## Pre-flight

Read both configuration files before assessing any account:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in churn-signal fields,
stop:

> "Your renewals practice profile isn't configured yet — specifically the churn signal
> definitions and escalation matrix. Run `/renewals:cold-start-interview` to configure
> these fields. Risk assessment without your defined signals will use generic defaults
> that may not match your product or motion."

If the profile is configured but churn signals are generic placeholders, proceed
with a notice:
> "Note: churn signals are still at placeholder values — using general SaaS risk
> signals. Run `/renewals:cold-start-interview --section churn-signals` to configure
> your specific signals."

Fields read from config:
- Primary churn drivers
- High-risk indicators (auto-escalate triggers)
- Early warning signals (monitoring flags)
- Competitive threats at renewal
- Health score threshold for risk workflow trigger
- Escalation matrix (route / how / SLA by situation)
- Configured discount authority (for save-offer validation)
- AE partner, Head of CS, Finance/RevOps contacts

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G1 (health scores are heuristics — never frame risk level as a churn prediction).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--deep` (default): Full signal aggregation across all five signal domains,
risk tier assignment, escalation routing, TARO play recommendation, and
suggested save actions.

`--quick`: Rapid pass — collects the three most important signals, assigns
preliminary risk tier, and surfaces the immediate next action. Use when you
need a fast read on multiple accounts. Takes 2–3 minutes per account.

`--triage`: Multi-account triage mode. Accepts a list of account names or
ARR figures and assigns preliminary risk tier to each based on minimal
signal input. Outputs a ranked triage table. Use for pipeline review prep.
After triage, run `--deep` on any Critical or High-tier accounts.

---

## Account identification

Ask: "Which account are you assessing? Provide the account name, and tell me
the renewal date and ARR if you have them."

If a CRM connector is available, attempt to look up the account by name and pull:
- ARR and renewal date
- Opportunity stage
- Last activity date (calls, emails, meetings)
- Open support tickets or recent escalations
- CSM owner and AE partner

Confirm: "[CRM — Salesforce/HubSpot]: found [account name] · $[ARR] ARR · renewal
[date] · [N] open tickets · last activity [date]"

If the account is not found or CRM is unavailable:
> "I'll work from what you tell me. Provide: ARR, renewal date, current opportunity
> stage, and any signals you've observed."

---

## Signal collection — five domains

Collect signals across five domains. For each domain, pull from live connectors
where available; otherwise ask the user.

### Domain 1 — Product adoption

| Signal | Source | Status |
|--------|--------|--------|
| Login frequency trend (last 30/60/90 days) | CS Platform / Product analytics | [data] |
| Active users vs. licensed seats | CS Platform | [data] |
| Core feature adoption rate | Product analytics | [data] |
| Recent adoption change (up / flat / declining) | CS Platform | [data] |

Red flags (flag if present):
- Login drop >30% in last 30 days
- Active users <40% of licensed seats
- Core feature never activated

### Domain 2 — Engagement and relationship

| Signal | Source | Status |
|--------|--------|--------|
| Last meaningful customer contact | CRM / Call recording | [date] |
| QBR completed in last quarter | CRM | [Y / N / overdue] |
| Executive sponsor still in role | User provided / CRM | [Y / N / changed] |
| Champion role change | User provided / CRM | [Y / N] |
| Meeting response rate last 60 days | User provided | [high / normal / dropped] |

Red flags:
- No meaningful contact in 30+ days (within negotiation window)
- Executive sponsor departed in last 90 days
- Champion changed roles or left company
- QBR missed or declined

### Domain 3 — Support and satisfaction

| Signal | Source | Status |
|--------|--------|--------|
| Open P1/P2 tickets | CRM / Support | [N] |
| Unresolved escalations | CRM | [Y / N] |
| NPS score (last survey) | CS Platform | [score] |
| CSAT trend | CS Platform | [up / flat / declining] |
| Time-to-resolution on recent tickets | Support | [data] |

Red flags:
- Open unresolved P1 ticket
- NPS <6 or NPS decline of >2 points in last cycle
- 3+ unresolved tickets open simultaneously

### Domain 4 — Commercial signals

| Signal | Source | Status |
|--------|--------|--------|
| Invoice payment status | CRM / Finance | [current / late / disputed] |
| Budget freeze mentioned | User provided / Call recording | [Y / N / uncertain] |
| Contract terms under negotiation | CRM / Contract storage | [Y / N] |
| Competitor evaluation confirmed | User provided / Gong | [Y / N] |
| Expansion in prior years | CRM | [Y / N — amount] |

Red flags:
- Invoice 15+ days late
- Competitor evaluation confirmed
- Budget freeze mentioned by economic buyer
- No expansion in Year 2+ (for growth-model accounts)

### Domain 5 — Renewal posture

| Signal | Source | Status |
|--------|--------|--------|
| Non-renewal notice received | User provided / CRM | [Y / N] |
| Price objection raised | User provided / Call recording | [Y / N] |
| Contract terms pushed back | User provided | [Y / N] |
| Mutual action plan / renewal agreement in place | CRM | [Y / N] |
| Days to renewal date | Calculated | [N] |

Red flags:
- Non-renewal notice received (auto-escalate regardless of ARR)
- Price objection combined with competitor mention
- No mutual action plan inside 30-day window

---

## Risk tier assignment

After signal collection, assign a risk tier:

| Tier | Criteria | Default action |
|------|----------|---------------|
| **Critical** | Non-renewal notice received; OR ≥2 auto-escalate triggers present; OR key executive sponsor departed + competitor confirmed | Escalate immediately — today |
| **High** | ≥3 red flags across domains; OR login drop + NPS <6 + no executive engagement in 45 days | Escalate within 24–48h per configured SLA |
| **Medium** | 1–2 red flags; early warning signals without confirmed churn intent | CSM action plan; monitor weekly |
| **Low** | No red flags; engagement healthy; renewal posture positive | Standard renewal motion; check in at configured window |

State the tier clearly:

> **Risk tier: [Critical / High / Medium / Low]**
> *Basis: [list the specific signals that drove the tier, not a summary]*

Health scores are an input signal — not the tier determination. If the account has a
health score below the configured escalation threshold, note it, but the tier is
determined by signal aggregation, not the score alone.

---

## Escalation routing

For Critical and High tier accounts, name the escalation path from the configured matrix:

| Situation | Route to | How | SLA |
|-----------|---------|-----|-----|
| [Matched situation from config] | [Configured owner] | [Configured method] | [Configured SLA] |

> "Escalation needed: route this account to [owner] via [method] within [SLA].
> Prepare: [what the escalation owner will need — account context, ARR at stake,
> signals summary, save options within your discount authority]."

If the situation doesn't exactly match the configured escalation matrix:
> "This situation doesn't map cleanly to a configured escalation scenario.
> Closest match: [scenario]. Recommend routing to [owner] — confirm with your
> Head of CS."

For Medium tier: name the CSM action required and the monitoring cadence.
For Low tier: confirm standard renewal motion is appropriate.

---

## TARO play recommendation

Match the account's risk profile to a renewal TARO play. Reference configured
playbook sources. If SuccessCOACHING methodology is configured, apply TARO:

**Trigger:** The specific signals present in this account that match a play trigger.

**Action:** The recommended play — state name if playbook is configured; describe
action steps if not.

**Resource:** What to bring to the customer conversation (data, case studies,
ROI evidence, executive involvement, product roadmap).

**Outcome:** The observable state that marks the play successful (renewal signed /
escalation resolved / executive sponsor re-engaged / mutual action plan agreed).

> Note: this play recommendation is a lead, not a mandate. Validate the trigger
> against what you know from direct account experience before executing. You own
> the decision.

---

## Save options

If the account is Critical or High tier, surface save options within the
configured parameters:

- **Discount authority:** You can approve up to [configured limit] without escalation.
  Any save offer above this threshold requires approval from [configured escalation route].
- **Multi-year offer:** If configured — [standard multi-year incentive from config].
- **Non-commercial saves:** Executive engagement, product roadmap preview,
  dedicated support or CSE involvement, success planning refresh.

Flag any save offer that exceeds discount authority:
> `[review — proposed save offer of [%] exceeds your configured authority of [%].
> Requires approval from [configured owner] before presenting to customer.]`

---

## Output format

---

**Risk Assessment — [Account Name]**
*ARR: $[amount] · Renewal: [date] · [N] days out*
*Assessed: [date] · Sources: [list]*

**Risk Tier: [Critical / High / Medium / Low]**

**Signal Summary**
[Domain-by-domain signal table — only show domains with findings for Clean accounts;
show all for Critical/High]

**Key signals driving tier:**
- [Signal 1 — specific, not summarized]
- [Signal 2]
- [Signal 3]

**Escalation path**
[Named route, method, SLA, and what to prepare]

**Recommended play**
[TARO structure: Trigger / Action / Resource / Outcome]

**Save options within authority**
[Options list with any discount flag if applicable]

**Immediate next actions**
1. [Action 1 — specific and time-bounded]
2. [Action 2]
3. [Action 3 — or "No immediate action required — continue standard motion" for Low]

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | CS Platform ✓ verified | Gong ✓ verified | manual input]
> - **Data as of:** [timestamp per source | N/A]
> - **Read:** [account record | renewal opportunity | last [N] calls | health score history | support tickets]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before escalating:** Confirm the signals are current — [specific items to verify before
>   presenting this assessment to your escalation owner]

---

## Guardrails

**Health scores are heuristics, not verdicts.** Assign the risk tier from signal
aggregation. Cite the health score as one input. Never present a health score as
the risk determination.

**No escalation recommendation without a named owner.** A risk flag names who
handles it, how they're reached, and what they need from you. An escalation route
without an owner is not an escalation route.

**Discount authority check on every save offer.** Any discount proposed in a save
recommendation must be checked against the configured authority ceiling. Flag any
offer that exceeds it before surfacing it to the user.

**Auto-escalate triggers are non-negotiable.** If any configured auto-escalate
trigger is present (non-renewal notice, executive escalation from customer, NPS
below threshold), the tier is Critical regardless of other signals. These triggers
do not require signal aggregation to meet a tier threshold.

**Account content is confidential.** This assessment contains customer ARR, health
data, and stakeholder information. Confirm the destination before sharing this
output — is the recipient authorized to see this account's renewal data?

**Data freshness.** State data-as-of for every source. CRM data older than 7 days
triggers a freshness warning before the tier assignment.
