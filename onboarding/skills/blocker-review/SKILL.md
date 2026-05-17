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

Before generating output, apply these primers:

1. **CLASSIFY**: What type of blocker review request is this?
   - **Active Technical Impediment**: Something is broken or blocked in the product/environment — integration failure, provisioning gap, data quality, or product bug. Customer wants to proceed but cannot.
   - **Customer Engagement Stall**: Customer has stopped progressing — low activity, missed meetings, champion unavailable, internal reprioritization. No technical impediment exists.
   - **CSM Execution Gap**: Blocker traces back to something the CSM or vendor team failed to deliver — unclear instructions, missing resources, dropped follow-through.
   - **Vendor/Product Constraint**: Bug, feature gap, or support queue delay outside the CSM's direct control. Resolution depends on internal product or engineering teams.
   - **Multi-Party Coordination Failure**: Partner-led or multi-stakeholder blocker where ownership is ambiguous. Multiple parties each believe another owns the next step.

2. **CONSTRAINTS**: What limits the solution space?
   - G4: Escalation recommendations must route through the configured escalation matrix with a named owner, channel, and SLA — no generic "escalate to your manager." If the matrix is `[PLACEHOLDER]`, flag before proceeding.
   - G5: Confidentiality check required before any output containing account details leaves the CSM's view — especially escalation briefs sent to external parties.
   - G7: Flag stale CRM or usage data with source date and staleness indicator — never present undated data as current.
   - Mode constraint: Match output depth to the actual need — `--diagnose` for uncharacterized problems, `--escalate` only after diagnosis, `--log` only after resolution.
   - Partner-led model constraint: In partner-led accounts, blockers route through the partner before reaching the customer directly.

3. **EXPERT CHECK**: What would a veteran onboarding CSM verify first?
   - Is this actually a blocker, or is the customer simply not engaged? Ask whether the customer has attempted the blocked step before classifying it as technical.
   - Does the milestone math support the stated severity? Calculate days remaining minus estimated resolution time — trust the math over the CSM's emotional urgency.
   - Has the CSM already tried the obvious resolution paths? Never recommend actions already attempted — ask what's been tried before generating the action plan.

4. **ANTI-PATTERNS**: Common blocker review mistakes to avoid:
   - Accepting the first symptom description as the root cause — the presenting symptom is almost never the actual blocker. Run the full diagnostic sequence before classifying.
   - Classifying an engagement problem as a technical blocker because the CSM framed it that way — probe for actual customer activity before accepting the label.
   - Generating an escalation brief with a vague ask ("please help with this account") instead of a specific action, owner, and deadline.
   - Recommending outreach the CSM already attempted — repeating failed actions destroys credibility with the customer.
   - Routing directly to the customer in a partner-led model without confirming partner awareness first.
   - Logging a vendor blocker with a ticket number but no escalation trigger date — passive waiting is not a resolution path.

**After execution**, verify:
- Does the action plan address the root cause, not just the presenting symptom?
- Is every escalation path routed through the configured matrix with named contacts (or flagged if unconfigured)?
- Does the severity rating match the milestone impact math, not the CSM's emotional framing?
- Are all data sources timestamped and staleness-flagged per G7? (CRM >7 days, CS platform >3 days, call data >14 days.)
- Does the output mode (`--diagnose` / `--escalate` / `--log`) match the actual need — not a mode the CSM defaulted to?
- Confidence: [High] if CRM data + CSM confirmation corroborate the classification / [Medium] if single-source or partially stale data / [Low] if working from CSM description alone — state which.

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
