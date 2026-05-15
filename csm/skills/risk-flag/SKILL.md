---
name: risk-flag
description: >
  Structured risk memo for an at-risk account — signals present, severity
  assessment, escalation routing from your configured matrix, and recommended
  intervention. Use when a health alert fires, a churn signal is detected, or
  you need to communicate account risk to leadership. Produces a CSM brief and
  an escalation-ready summary separately.
argument-hint: "[account name] [--brief | --escalation-memo]"
version: "1.0.0"
---

# /risk-flag

Document the risk clearly, name the routing, and give the CSM a specific path
forward — not just a flag.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to apply:
- Churn signal definitions — which signals are configured as high/medium/low weight
- Escalation matrix — routing for each risk scenario
- Health model thresholds — Red and Yellow classification
- CS motion — shapes the intervention approach

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G1 (health scores are heuristics — do not frame as churn predictions), G3 (any revenue impact framing carries commitment language), G4 (no escalation triage without a named escalation path).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--brief`: CSM-facing risk summary. Internal use — full signal breakdown,
health context, and CSM action plan. Default.

`--escalation-memo`: Produce a clean, escalation-ready summary for the CSM's
manager, VP CS, or CRO. Concise. Designed for rapid review by someone who
doesn't know the account details. Includes: account, ARR, renewal date,
risk signals, recommended action, and routing.

Both modes can be run for the same account. Default is `--brief`.

---

## Data gathering

Pull from connected integrations (per configured profile):
- CS Platform: current health score, component breakdown, CTAs, lifecycle stage
- CRM: ARR, renewal date, contract terms, stakeholder contacts, account history
- Call recording: last 2-3 calls — tone, topics, any risk signals mentioned
- Document storage: last success plan or QBR — open items, committed actions

If account-research was run this session: use that context.

If nothing connected, prompt:
> "Tell me what's happening at [account]. What triggered this risk flag? What
> signals are you seeing? I'll build the memo from what you share."

Do not generate a risk memo without at least one concrete risk signal from the
CSM or from live data.

---

## Risk flag structure

---

### CSM Risk Brief — [Account Name]
*[Date] · INTERNAL · [CS motion] · [Segment]*

---

**Account snapshot**

| Field | Value |
|-------|-------|
| ARR | $[amount] |
| Renewal date | [date] — [N] days |
| Segment | [segment] |
| Health | [Red / Yellow] |
| CSM | [name] |
| AE / AM | [name] |
| Executive sponsor | [name] — [last contact: date] |

---

**Risk signals — what triggered this flag**

List each signal present with evidence. No inferred signals without evidence.

| Signal | Present | Evidence | Weight per config |
|--------|---------|----------|------------------|
| Executive sponsor departure or disengagement | [Yes/No/Unknown] | [specific evidence] | High |
| Product usage drop >[configured threshold]% | [Yes/No] | [% change over period] | High |
| Open escalation or unresolved P1 ticket | [Yes/No] | [ticket details] | High |
| NPS detractor + no recovery conversation | [Yes/No] | [score + date] | Medium |
| Missed QBR or no-show pattern | [Yes/No] | [dates] | Medium |
| Competitor evaluation | [Yes/No/Unknown] | [source of signal] | High |
| No CSM contact in >[threshold] days | [Yes/No] | [last contact date] | Medium |
| [Additional configured signal] | | | |

**Primary risk driver:** [The signal with the most direct path to churn]

---

**Risk severity**

Classify based on configured thresholds and signal weight:

> **Severity: [Critical / High / Medium]**
>
> Classification rationale: [1-3 sentences. Which signals drove this. Why this
> severity level vs. adjacent options.]

- **Critical:** Multiple high-weight signals present; renewal within 90 days; ARR
  above escalation threshold → immediate executive-level escalation required
- **High:** One high-weight signal or multiple medium signals; requires CSM
  intervention within 48h; monitor daily
- **Medium:** Medium-weight signals; proactive outreach warranted; monitor weekly

---

**Root cause hypothesis**

What is the most likely reason for the risk?

> "The most plausible explanation is [X] — based on [specific evidence]. Alternative
> explanations: [Y] (possible if [condition]) / [Z] (possible if [condition]).
> The champion should be asked directly whether [root cause question] is accurate
> before the CSM builds a recovery plan."

Do not present the hypothesis as fact. It is the leading interpretation based on
available data. The CSM confirms or refutes it in the next customer interaction.

---

**Escalation routing**

Apply the configured escalation matrix exactly.

| Condition | Route to | Via | SLA |
|-----------|----------|-----|-----|
| [Matching scenario from matrix] | [configured contact] | [configured channel] | [configured SLA] |

If multiple matrix rows apply, show all and note the primary route.

If this account's ARR meets the configured churn-risk threshold:
> "ARR ($[amount]) exceeds the configured escalation threshold ($[threshold]).
> Route to [configured contact] via [channel] within [SLA]. Include this memo."

If below the threshold:
> "ARR is below the configured escalation threshold. CSM-managed intervention.
> Notify [CS lead] if severity escalates to Critical."

---

**Recommended intervention plan**

Specific actions with owners and timelines. Not generic.

**Immediate (within 24-48h):**
1. [Specific action — e.g., "Request executive sponsor check-in call. Purpose: confirm
   sponsor status and surface any org changes. Do not lead with health score."]
2. [Specific action — e.g., "Review open tickets — contact support team to confirm
   P2 ticket [ID] has a resolution timeline and communicate it to the champion."]
3. [Escalation action — e.g., "Notify [CS lead] per escalation matrix via Slack.
   Share this memo as context."]

**This week:**
1. [Action — e.g., "Meet with champion to understand usage drop root cause.
   Prepare 3 questions: [specific questions based on signals]."]
2. [Action — e.g., "Update health assessment in CS Platform with current signals."]

**If [specific trigger] occurs:**
1. [Escalation path — e.g., "If sponsor confirms departure, escalate to Critical
   immediately. Route to [VP CS] within [SLA]. Loop in AE."]

---

**Success criteria for recovery**

What does "risk resolved" look like? Define 1-3 observable conditions:
- [Condition 1 — e.g., "Usage returns to >[threshold]% of baseline within 30 days"]
- [Condition 2 — e.g., "Executive sponsor re-engaged and confirmed for next QBR"]
- [Condition 3 — e.g., "Champion confirms competitor evaluation is not active"]

Review date: [recommend a specific date to reassess — typically 2-4 weeks out]

---

## Escalation memo (`--escalation-memo`)

One-page version for the CSM's manager, VP CS, or CRO. No internal health model
details — just the facts they need to act.

---

**Account Risk Memo — [Account Name]**
*[Date] · Prepared by: [CSM name]*

**For:** [Manager / VP CS / CRO — configured escalation contact]

---

| Field | Detail |
|-------|--------|
| Account | [Account name] |
| ARR | $[amount] |
| Renewal | [date] — [N days] |
| Segment | [segment] |
| Risk level | [Critical / High / Medium] |

**Risk signals:**
- [Signal 1]: [1-line evidence]
- [Signal 2]: [1-line evidence]
- [Signal 3 if present]: [1-line evidence]

**Most likely root cause:**
[2-3 sentences. Plain language. What is the risk and why.]

**Recommended action from CSM:**
[What the CSM is doing. What they need from leadership.]

**If no action is taken:**
[Likely outcome — e.g., "Renewal at risk of churn or significant contraction
based on signals present. Renewal is in [N] days."]

**Next step:**
[Specific ask — e.g., "Request 20 minutes with the customer's CFO to reinforce
the executive relationship. CSM to arrange. Your name on the invite increases
response rate significantly."]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live | CRM ✓ live | call notes: [date] | user-provided context | conversation context only]
> - **Data as of:** [timestamp per source]
> - **Risk signals:** [Confirmed from data | CSM-reported — not independently verified]
> - **Escalation routing:** [Applied configured matrix — verify contact names are current]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before escalating:** Confirm ARR and renewal date with CRM before sharing escalation memo with leadership.

---

## Output

Risk flag report — format driven by `--standard` (default) or `--escalation-memo`
flag. Standard output produces a structured risk summary with signal inventory,
severity tier, and recommended response actions. Escalation memo mode produces a
full internal memo. See mode-specific sections for field-level structure.

## Guardrails

**Risk signals require evidence.** A signal is listed as Present only if there is
direct evidence. Absence of engagement is "Unknown" or "Declining," not "Confirmed
at risk."

**Root cause is a hypothesis, not a verdict.** The memo names the leading
explanation and the evidence behind it. It does not state the account will churn.

**No escalation without a path.** Every escalation recommendation names the
contact, channel, and SLA from the configured matrix. A risk flag without a
routing is not actionable.

**Escalation memo is not the full brief.** The escalation memo omits health model
component weights, internal stakeholder notes, and expansion context. Those stay
in the CSM brief.

**Expansion context.** If the account has expansion signals, do not include them
in the risk memo. Risk memos focus on risk mitigation, not opportunity. Expansion
context routes to the AE separately.

**Revenue accountability.** If the memo estimates ARR at risk or implies a renewal
probability, the CSM reviewer validates the figure before the memo reaches finance
or board reporting.

---

## After the memo

- "Want a full escalation memo to send to leadership? Run again with `--escalation-memo`."
- "Renewal within 90 days — run renewal readiness: `/csm:renewal-readiness [account]`"
- "Need to track intervention progress? Update the account in `/csm:account-research` after each action."
- "Want to map the stakeholder risk specifically? `/csm:stakeholder-map [account] --sponsor-risk`"
