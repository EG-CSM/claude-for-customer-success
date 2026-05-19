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
deployment_target: plugin
---

# /renewals:risk-assessment [VALIDATED]

Structured risk assessment for a renewal account — signals, tier, escalation path,
and recommended play.

---

## Use when
- You are at the 90-, 60-, or 30-day outreach window for a renewal account and need a structured signal read before engaging
- A churn signal has been detected within the 90-day renewal window (login drop, NPS decline, executive sponsor departure, non-renewal notice) and the account needs immediate triage
- You need to prioritize accounts before a pipeline review and want a preliminary risk tier for each
- An account has been flagged by a health score alert and you need to decompose the score into actionable domain-level signals
- You are preparing an escalation and need a structured risk brief for your Head of CS or AE partner

## Do NOT use for
- Ongoing health monitoring without a specific renewal or churn trigger — use your CS Platform health dashboards for continuous monitoring
- Post-churn analysis after a cancellation has closed — use `/renewals:churn-rca` for root cause analysis
- Expansion opportunity identification — use `/renewals:expansion-signal`
- Generating an executive-ready renewal brief — run this skill first, then use `/renewals:executive-summary` to translate the tier output
- Batch pipeline forecasting without per-account triage — use `/renewals:renewal-forecast` for portfolio-level views
- Churn signal triage outside the 90-day renewal window — use `/csm:risk-flag` for day-to-day risk assessment outside the renewal motion

## Typical Activation
> `/renewals:risk-assessment Acme Corp` — full signal aggregation across all five domains for a named account
> `/renewals:risk-assessment Acme Corp --quick` — rapid three-domain pass for a time-pressured single account read
> `/renewals:risk-assessment --triage` — multi-account triage mode; provide a list of account names or ARR figures for ranked preliminary tier assignment

---

## Pre-flight

Read both configuration files before assessing any account:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in churn-signal fields,
stop:

> "Your renewals company profile isn't configured yet — specifically the churn signal
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

Before generating output, apply these primers:

1. **CLASSIFY**: What type of risk assessment request is this?
   - **Signal-Rich Triage**: Multiple live data sources available (CRM, CS Platform, call recording). Full five-domain signal collection is feasible. Optimize for cross-domain compound risk detection.
   - **Signal-Sparse Manual**: Limited or no connectors. CSM provides context verbally. Probe for absent signals — silence is not health. Flag every unassessed domain explicitly.
   - **Auto-Escalate Trigger Present**: A non-negotiable trigger is active (non-renewal notice, executive escalation, NPS below threshold). Tier is Critical — route escalation immediately, then backfill signal picture.
   - **Multi-Account Triage (--triage)**: Batch of accounts for pipeline review prep. Screen for auto-escalate triggers across the batch first, then assign preliminary tiers. Reserve deep mode for Critical/High only.
   - **Quick Spot-Check (--quick)**: Time-pressured single account. Collect the three highest-signal domains, assign preliminary tier, surface immediate next action. Do not attempt full five-domain aggregation.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: Health scores are component signals, not churn verdicts — decompose into observable signals, never frame as "this account will churn."
   - G2: No escalation recommendation without a named owner, channel, and SLA from the configured matrix — no generic "escalate to your manager."
   - G4: Auto-escalate triggers are non-negotiable — if present, tier is Critical regardless of other signals. These do not require aggregation to meet threshold.
   - G5: Account content is confidential — confirm the destination before sharing. ARR, health data, and stakeholder information require a recipient authorization check.
   - G7: State data-as-of for every source. CRM data >7 days old triggers a freshness warning before tier assignment. Flag connector gaps — never silently omit a domain.
   - Discount authority ceiling applies to every save offer — flag any proposed discount that exceeds configured authority before surfacing.

3. **EXPERT CHECK**: What would a veteran renewal risk analyst verify first?
   - Are there cross-domain compound signals that individually read Medium but together indicate High or Critical? Two Medium signals in different domains are worse than one High in a single domain.
   - Is the health score decomposed into domain-level signals, or is it being used as a shortcut for tier assignment? Composite scores mask domain-level degradation.
   - Has the champion or executive sponsor changed in the last 90 days? Relationship loss amplifies every other signal — treat it as a tier multiplier, not just another red flag.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - ❌ Using the composite health score as the risk tier instead of aggregating signals across all five domains.
   - ❌ Treating absent data as neutral — no logins, no calls, no tickets inside a renewal window is a red flag, not a non-signal.
   - ❌ Running full five-domain collection when an auto-escalate trigger is already present — route first, backfill second.
   - ❌ Surfacing a save offer above configured discount authority without flagging it for approval.
   - ❌ Anchoring on the signal the CSM mentions first (usually the most recent or dramatic) without probing all five domains.
   - ❌ Ranking triage accounts by signal severity alone without weighting by ARR at stake.

**After execution**, verify:
- Does the tier assignment trace to specific named signals, not a summary or composite score?
- Are all data sources timestamped and staleness-flagged per G7?
- Is the escalation route drawn from the configured matrix with named owner, method, and SLA?
- Confidence: [High] if 3+ domains have live-sourced <7-day-old data corroborating the tier / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

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

## Security & Permissions

```
network:        none — no external API calls, no web fetch
read_scope:     ~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md and
                ~/.claude/plugins/config/claude-for-customer-success/company-profile.md only;
                live connector reads (CRM, CS Platform, Gong) are read-only and scoped to
                the named account record only
write_scope:    none — all assessment output to conversation; no file writes
subprocess:     none
dynamic_code:   none — no eval, no exec, no runtime code execution
```

This skill operates in read-only mode. Config files are read at session start for churn signal definitions and escalation matrix. Connector reads (where available) are scoped to the named account record and are never written back. All assessment output is produced as conversation content only.

---

## Trust & Verification

**Signal data handling:**
CRM and CS Platform data is accepted as structured input through connectors or as CSM-provided context. Signal values are used for risk tier aggregation and display only — they are not executed, evaluated as code, or used to derive file paths. Free-text fields (`notes`, `additional_context`) are stored as display data.

**Health score integrity:**
Health scores are treated as one input signal among five domain signals. The skill never derives the risk tier from a health score alone. Composite score decomposition is required before any tier assignment — a health score below threshold triggers investigation, not automatic Critical tier.

**Discount authority enforcement:**
Save offer percentages are validated against the configured discount authority ceiling from the operator config before surfacing to the user. Any proposed discount exceeding the ceiling is flagged `[review]` and requires explicit approval from the configured escalation owner before presentation to the customer.

**Auto-escalate trigger integrity:**
Configured auto-escalate triggers (non-renewal notice, executive escalation from customer, NPS below threshold) produce a Critical tier assignment that cannot be overridden by aggregated signals. These triggers are read from the operator config and applied as non-negotiable gates — the skill does not accept user input that would suppress a Critical tier resulting from a confirmed auto-escalate trigger.

**Account data confidentiality:**
Account ARR, health data, and stakeholder information produced in this assessment are flagged as confidential in the output. The skill prompts confirmation of the recipient before any assessment is shared. This confirmation cannot be suppressed.

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

---

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill
