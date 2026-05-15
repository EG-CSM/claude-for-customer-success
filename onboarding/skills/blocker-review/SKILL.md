---
name: blocker-review
description: >
  Diagnose and resolve onboarding blockers — anything preventing a customer from
  reaching their next milestone on time. Classifies blockers by type and severity,
  routes to the correct resolution path per your escalation matrix, and produces
  a clear action plan with named owners and deadlines. Reads escalation thresholds
  and escalation contacts from your onboarding profile. Use --diagnose (default) to
  work through a current blocker with a guided diagnostic, --escalate to produce a
  formatted escalation brief for a specific contact, or --log to record a resolved
  blocker for the account history.
argument-hint: "[<account-name-or-ID>] [--diagnose | --escalate | --log]"
version: "1.0.0"
---

# /onboarding:blocker-review

Blocker diagnosis, escalation, and resolution tracking.

---

## Pre-flight

Read both configuration files before running any blocker review:
1. `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Fields read from onboarding config:
- Escalation matrix (who gets notified at each severity tier; named escalation contacts)
- Onboarding model (white-glove escalations reach executive sponsor; partner-led
  escalations route through the partner first)
- Milestone framework (at-risk signals per milestone — used to classify the blocker's
  milestone impact)
- CS methodology (TARO play references in resolution steps; SuccessCOACHING cadence
  rules for follow-up)

If escalation matrix is `[PLACEHOLDER]`:
> "Escalation contacts aren't configured. Run
> `/onboarding:cold-start-interview --section escalation` to define your escalation
> matrix before routing blockers. I'll describe the resolution path without naming
> specific contacts."

Proceed with a generic escalation path description if the user confirms.

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G4 (verify a named escalation path is configured before generating triage output).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--diagnose` (default): Guided diagnostic session. Asks structured questions to
classify the blocker, assess its milestone impact, and produce a ranked action plan
with owners and deadlines. Use when the CSM knows something is wrong but hasn't
fully characterized the problem.

`--escalate`: Produce a formatted escalation brief for a specific escalation contact
(AE, manager, exec sponsor, implementation engineer, or support). The brief includes
account context, blocker description, milestone impact, actions already taken, and
the specific ask. Use when the CSM has already diagnosed the blocker and needs to
involve another party.

`--log`: Record a resolved blocker for the account history. Captures blocker type,
root cause, resolution action, days lost (if any), and preventability assessment.
Use after a blocker is resolved to build institutional knowledge for future accounts
in the same segment or model.

---

## Account identification

Ask: "Which account is experiencing the blocker?"

If CRM connector available, pull: account name, segment, current milestone, contract
start date, CSM/AE names, and any prior escalation history on this account.

Confirm: "[CRM]: [account name] · [segment] · currently in M[#] · CSM: [name]
· data as of [timestamp]"

If no CRM: "Tell me the account name and which milestone you're currently trying to
complete — I'll work from there."

---

## Blocker classification

Every blocker is classified on two axes: **type** and **severity**.

### Type

**Customer-side blockers:**
- `adoption` — Customer team is not using the product as expected; low login activity,
  skipped training, low engagement
- `bandwidth` — Customer team lacks time or headcount to complete required actions
- `champion-absent` — The primary champion is unavailable (travel, leave, departure)
- `priority-shift` — Internal customer initiative deprioritized onboarding; competing
  internal project
- `stakeholder-misalignment` — Disagreement within the customer team about goals,
  scope, or ownership

**Technical blockers:**
- `integration` — Required integration is incomplete, broken, or waiting on IT approval
- `data-quality` — Customer data needed for product setup is missing, dirty, or
  inaccessible
- `provisioning` — User accounts, permissions, or SSO not configured
- `environment` — Firewall, VPN, or security policy blocking product access

**CSM-side blockers:**
- `unclear-ask` — Customer is uncertain what to do next; the CSM's instructions were
  unclear or misunderstood
- `missing-resource` — Required documentation, training, or configuration guide not
  provided
- `follow-through` — CSM committed to an action that hasn't been completed

**Vendor/product blockers:**
- `bug` — Product defect preventing a required workflow
- `feature-gap` — Customer needs a capability not yet in the product
- `support-queue` — Open support ticket blocking progress; resolution not yet received

**Partner blockers** (partner-led model only):
- `partner-bandwidth` — Partner is delayed on their implementation deliverables
- `partner-alignment` — Partner and CSM are misaligned on scope, timeline, or ownership

### Severity

| Severity | Definition | Example |
|----------|-----------|---------|
| P1 — Critical | Current milestone will be missed without immediate action | Integration broken 2 days before M2 |
| P2 — High | Current milestone is at risk if not resolved within 3 days | Champion absent for a week; no backup named |
| P3 — Medium | Next milestone is at risk; current milestone is still achievable | Data quality issue slowing M3 setup |
| P4 — Low | Non-blocking but needs tracking | Minor training gap; user onboarding delayed by 1 day |

---

## `--diagnose` mode: Diagnostic sequence

### Step 1: Describe the symptom

Ask: "What specifically is not happening that should be? What did you expect to
see by now that you haven't seen?"

Record the symptom verbatim. This anchors the diagnosis to observable behavior,
not interpretation.

### Step 2: Identify the milestone impact

Ask: "Which milestone does this affect — and by how much? Will this cause the
milestone to be missed, or is it a risk that could still be managed?"

Calculate: if the current milestone target date is [date] and the blocker is
estimated to take [N] days to resolve, the milestone is [on track / at risk / will
be missed]. Show the math transparently.

### Step 3: Classify the blocker

Use the type taxonomy above. Ask probing questions to narrow the classification:

- "Is the customer actively trying to complete this step but unable to?" → Technical
  or provisioning blocker
- "Has the customer engaged at all in the last 7 days?" → Adoption, bandwidth, or
  champion-absent
- "Did the customer agree on what needed to happen next?" → May be unclear-ask
  or stakeholder-misalignment
- "Is there an open support ticket?" → Support-queue blocker
- "Did we commit to something and not deliver?" → CSM-side follow-through

Present the classification:
> "Based on your description, this looks like a [type] blocker at [severity] — is
> that consistent with what you're seeing?"

Adjust based on CSM input.

### Step 4: Determine prior actions taken

Ask: "What have you already tried? Have you reached out to the champion, the AE,
or opened a support ticket?"

Record prior actions. Do not recommend actions already taken.

### Step 5: Action plan

Generate a ranked action plan. Each action includes:
- **Action:** [specific step]
- **Owner:** [CSM / customer champion / AE / support / implementation engineer]
- **Deadline:** [date — typically 24h for P1, 48–72h for P2, this week for P3]
- **Escalation trigger:** [if this action doesn't resolve the blocker by [date],
  escalate to [contact from config]]

Maximum 3 ranked actions. The first action should be the fastest path to unblocking
the milestone. Do not list every possible action — list the right ones in priority order.

If the action plan requires escalation, offer to run `--escalate` immediately:
> "This P1 blocker likely needs [AE / exec sponsor / implementation engineer] involvement.
> Run `/onboarding:blocker-review --escalate` to generate the escalation brief now."

---

## `--escalate` mode

Ask: "Who is this escalation going to?" Options from config escalation matrix:
- AE (account executive)
- Manager or team lead
- Implementation engineer
- Executive sponsor (white-glove model)
- Partner contact (partner-led model)
- Support / technical escalation

Generate the escalation brief:

```
**Escalation Brief — [Account Name]**
*To: [escalation contact name and role]*
*From: [CSM name]*
*Date: [today] · Severity: [P1/P2/P3]*

**Account context:**
[Account name] · [Segment] · Contract start: [date]
Current milestone: M[#] ([label]) · Target: [date] · [N] days [remaining / overdue]

**Blocker:**
[Blocker type: [classification]] — [1–2 sentence description of what is not happening
and what the symptom looks like]

**Milestone impact:**
[If unresolved by [date], M[#] will be missed. Current delay estimate: [N] days.]

**Actions already taken:**
- [Action 1] — [date taken] — [outcome]
- [Action 2] — [date taken] — [outcome]

**Your ask:**
[Specific, scoped request — not "help me fix this." E.g., "Reach out to [exec] to
confirm this is a priority," or "Unblock the support ticket [#] by EOD [date]," or
"Join the call on [date] to reset the integration scope."]

**If not resolved by [date]:**
[Next escalation step from config]
```

---

## `--log` mode

Ask: "What was the blocker, how was it resolved, and how many days did it cost?"

Produce a structured log entry for the account record:

```
Blocker Log — [Account Name]
Date opened: [date] · Date resolved: [date] · Days lost: [N]

Type: [classification]
Severity: [P1/P2/P3/P4]
Milestone affected: M[#]
Root cause: [1–2 sentences]
Resolution action: [what actually fixed it]
Owner of resolution: [CSM / AE / customer / partner / support]
Preventable: [Yes — how | No — why not]
Recommendation for future accounts in this segment/model: [brief]
```

If a PM connector is configured, offer to add this log entry to the account's
project as a closed task.

---

## Reviewer note (internal — `--diagnose` only)

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ | manual input]
> - **Data as of:** [timestamp]
> - **Config fields read:** escalation matrix ([contacts]), milestone at-risk signals
>   ([M# signals relevant to this blocker])
> - **Blocker classification:** [type] at [severity] — confidence: [High / Moderate
>   based on symptom description]
> - **Milestone impact assessment:** [on track / at risk / will be missed — based on
>   [N] days to target and [N] days estimated to resolve]
> - **Prior actions recorded:** [list or "none provided"]
> - **Escalation recommendation:** [escalate now / monitor / no escalation needed]
> - **Flagged for your judgment:** [any ambiguous classification or conflicting signals]

---

## Output

Blocker review output — format driven by flag (`--diagnose`, `--escalate`, `--log`).
Diagnose mode: structured diagnostic report with blocker inventory, severity tiers,
root cause analysis, and recommended actions. Escalate mode: escalation brief.
Log mode: CRM-ready note. See mode-specific sections for field-level structure.

> [review before sending]

## Guardrails

**Classify before acting.** A blocker misclassified as technical when it is actually
adoption-related will produce the wrong action plan. Run the full diagnostic sequence
before generating actions — do not skip to solutions based on the first symptom
described.

**Severity drives urgency, not the CSM's emotional state.** A CSM who says "this is
urgent" on a P3 blocker is reacting, not assessing. Use the milestone impact calculation
to determine severity — not the description of how the CSM feels about it.

**`--escalate` requires a specific ask.** An escalation brief without a clear,
scoped request creates confusion and delays resolution. Do not produce an escalation
that says "please help" — name exactly what action the escalation contact must take
and by when.

**Don't recommend actions already taken.** Before generating the action plan, ask
what's already been tried. Recommending the same outreach that failed last week wastes
the CSM's credibility with the customer.

**Partner-led blockers route through the partner first.** For accounts on the
partner-led model, a blocker that appears customer-side may actually be in the
partner's lane. Ask: "Is the partner aware of this? Has the partner reached out to
the customer about it?" before routing directly to the customer.

**`--log` builds institutional knowledge.** Blocker logs are not just housekeeping —
they are the data source for pattern recognition across accounts. Log every significant
blocker (P1 and P2 at minimum) after resolution. Unlogged blockers cannot inform
future proactive interventions.

**Escalation thresholds are minimums — not maximums.** The config escalation thresholds
define when escalation is required. A CSM may judge that an earlier escalation is
warranted given account context (strategic relationship, exec attention, partner
complexity). The config threshold is the floor; the CSM's judgment sets the ceiling.
