---
name: taro-play-runner
description: >
  Select and execute a TARO play (Trigger, Action, Resource, Outcome) from your
  configured playbook for an account situation. Use when a health alert fires,
  a lifecycle stage transition occurs, or you need a structured play for a common
  CS motion — adoption push, executive re-engagement, at-risk recovery, or
  expansion readiness. Identifies the right play, contextualizes it to the account,
  and produces execution-ready outputs (email drafts, agenda, talking points, action
  plan) — not a generic playbook excerpt.
argument-hint: "[account name] [--situation <description> | --play <play-name>]"
version: "1.0.0"
---

# /taro-play-runner

Run the right play for this account's situation — not a template, a
contextualized execution plan.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Critical configuration to apply:
- Configured playbook (plays available, triggers, standard outcomes)
- CS motion — determines play depth, outreach channel, and frequency
- Primary value metric — anchors the outcome frame for every play
- Health model thresholds — confirms which plays are appropriate for current health
- Escalation matrix — some plays include escalation steps; route per configured matrix

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G2 (expansion signals require economic buyer qualification), G4 (no escalation triage without a named escalation path), G6 (TARO play outputs are leads for CSM judgment — not prescriptions).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Play selection

**If `--situation` is provided:** Describe the situation in plain language.
The skill matches it to the most appropriate configured play and explains
why that play fits. If multiple plays are applicable, presents the top two
with a brief rationale for each and asks for confirmation before proceeding.

**If `--play` is provided:** Use that play directly. Confirm it is in the
configured playbook before proceeding; if not found, surface available plays
and ask for correction.

**If neither is provided:** Ask ONE question:
> "What's happening at [account] right now? Describe the situation and I'll
> match it to the right play from your playbook."

---

## Standard play library

If no playbook is configured, apply these standard plays. When a playbook IS
configured, these are available as defaults if the configured playbook doesn't
cover the situation.

| Play | Trigger | Primary outcome |
|------|---------|----------------|
| `adoption-push` | Usage below adoption threshold; onboarding milestone missed | Drive feature adoption to configured target within timeframe |
| `executive-re-engagement` | Executive sponsor engagement declining or dormant | Re-establish executive relationship before renewal window |
| `at-risk-recovery` | Account classified Red; one or more high-weight churn signals | Reduce churn risk; stabilize relationship; address root cause |
| `renewal-acceleration` | Renewal <90 days; health is Yellow or Green; no active risk | Secure renewal commitments; identify expansion opportunity |
| `expansion-readiness` | Expansion signals present; account is healthy; champion engaged | Qualify expansion signal; route to AE with context |
| `champion-departure` | Known or suspected champion departure or role change | Identify and onboard new champion before relationship gap opens |
| `nps-recovery` | NPS detractor score received; no recovery conversation yet | Acknowledge detractor signal; surface root cause; initiate recovery |
| `stalled-onboarding` | Onboarding milestones missed >2 weeks; engagement declining | Re-engage stakeholders; unblock adoption; reset timeline |
| `qbr-refresh` | >90 days since last QBR; account approaching renewal | Schedule and deliver QBR; realign success criteria |
| `value-realization` | Account at or past first value milestone; ready for expansion narrative | Document value delivered; prepare customer for next-stage outcomes |

---

## Play execution output

For each play, produce the following:

---

### Play: [Play name] — [Account Name]
*[Date] · [CS motion] · [Segment] · Play selected because: [1-line trigger rationale]*

---

**TARO frame**

| Component | Detail |
|-----------|--------|
| **Trigger** | [Specific trigger condition met for this account — with evidence] |
| **Action** | [What the CSM will do — sequence of steps for this play] |
| **Resource** | [Configured resources for this play: templates, docs, talk tracks] |
| **Outcome** | [What success looks like for this play — measurable, specific] |

The TARO frame is the CSM's contract with themselves. If the trigger is not
confirmed, the play should not launch. If the outcome is not measurable, the
play will not be evaluated correctly.

---

**Why this play now**

1-2 sentences connecting the account's current state to the play trigger. Specific
to this account — not a generic play description.

> "Usage dropped 18% over 30 days and the champion hasn't responded to two
> outreach attempts. The adoption-push play is triggered because the account has
> crossed the Yellow threshold on the usage component and the trend is continuing
> downward."

---

**Execution steps**

Sequence of actions. Each step is specific — who does what, by when, via which
channel. Calibrated to the configured CS motion.

**Step 1 — [Action]:** [When / channel / who]
> [Specific description of what to do, what to say/not say, what to listen for]

**Step 2 — [Action]:** [When / channel / who]
> [...]

**Step 3 — [Action]:** [...]

**Decision point:** After Step [N], one of three paths:

| Signal | Next step |
|--------|-----------|
| [Positive signal — e.g., customer re-engages] | [Advance play: Step N+1] |
| [Neutral signal — e.g., no response] | [Recovery path: Step N+1 alt] |
| [Negative signal — e.g., customer confirms churn intent] | [Escalate: route per matrix] |

---

**Execution-ready outreach**

Produce the first outreach communication for this play — email or Slack message,
calibrated to the CS motion and the account relationship. Not a template — written
specifically for this account.

---

**Subject:** [Account-specific subject line — not a generic template header]

**[Contact name],**

[Opening that references something specific to this account — recent conversation,
a milestone, a shared context. Not "I hope this email finds you well."]

[The reason for reaching out — honest, direct, account-specific. One paragraph.]

[The ask — specific: a 20-minute call, a piece of information, a decision.
One clear call to action only.]

[Close — professional, warm, calibrated to relationship maturity]

[CSM name]

---

> **Before sending:** Edit to match your relationship tone with this contact.
> Remove any signals that reference internal health scores or escalation routing.

---

**Key talking points (if a call is part of this play)**

3-5 specific points. Each is a statement or question — not a topic label.

- [Point 1 — e.g., "Ask directly: what's changed for your team in the last 30 days?
  Don't anchor on the usage data first — let them tell you."]
- [Point 2 — e.g., "Reference [specific milestone] from the success plan — did they
  consider that achieved? How did they measure it internally?"]
- [Point 3 — e.g., "Confirm executive sponsor [name] is still in scope for the
  upcoming renewal conversation — don't assume."]

---

**What to listen for**

Signals that change the play trajectory:

| Signal | What it means | What to do |
|--------|--------------|------------|
| [Risk signal — e.g., "budget freeze mentioned"] | [Interpretation] | [Escalate / update health / adjust play] |
| [Positive signal — e.g., "sponsor confirms expansion interest"] | [Interpretation] | [Route to AE / advance to expansion play] |
| [Neutral signal — e.g., no specific feedback on product] | [Interpretation] | [Stay on current play; check in at next step] |

---

**Play timeline**

| Step | Due | Owner | Status |
|------|-----|-------|--------|
| [Step 1] | [Date] | [CSM] | Not started |
| [Step 2] | [Date] | [Customer / CSM / Joint] | |
| [Play outcome check] | [Date — end of play window] | [CSM] | |

---

**Outcome criteria — how you'll know the play worked**

Define success before executing. Not "the account is healthy again."

- [Observable criterion 1 — e.g., "Customer completes usage milestone X within
  [N] days of play launch"]
- [Observable criterion 2 — e.g., "Executive sponsor attends next check-in call"]
- [Observable criterion 3 — e.g., "Champion explicitly confirms issue is resolved"]

If no criterion is met by the play window end:
[Next play recommendation — e.g., "Advance to at-risk-recovery" or
"Escalate per matrix and open risk-flag"]

---

## Play note (internal)

> **⚠️ Play note**
> - **Play selection:** [Play name] — matched to [trigger condition from config or standard library]
> - **Playbook source:** [Configured playbook from company profile | Standard library default — no configured playbook found]
> - **Account data used:** [CRM ✓ live | CS Platform ✓ live | user provided | conversation context only]
> - **Data as of:** [timestamp]
> - **TARO framing:** [Trigger confirmed from data | Trigger reported by CSM — not independently verified in data]
> - **Outreach draft:** Edit before sending. Remove internal references. Adjust tone to match relationship.

---

## Output

Play execution package — structured markdown with: selected play name and rationale,
account-contextualised action steps, ready-to-use deliverables (email draft, agenda,
talking points, or action plan depending on play type), and success criteria.
See **Play execution output** section for field-level detail.

> [review before sending]

## Guardrails

**TARO plays are leads, not mandates.** The skill selects and contextualizes
the play; the CSM decides whether to run it and owns the execution. The play note
says "recommended" — not "required."

**Trigger must be confirmed.** A play runs against a confirmed trigger, not a
suspected one. If the trigger is CSM-reported and not verified in connected data,
the play note flags it.

**No expansion language in at-risk plays.** Expansion signals are noted internally
but do not appear in at-risk play outreach. An account in recovery mode should not
receive expansion-framed communication.

**Escalation within plays.** If a play step requires escalation (e.g., executive
re-engagement requires VP involvement), name the configured escalation route.
Do not describe escalation generically.

**Outcome window.** Every play has a time-bounded outcome window. If the window
closes without success criteria met, the next step is explicit — not "monitor further."

---

## After the play

- "Play running — want to document risk formally? `/csm:risk-flag [account]`"
- "Play step requires a call — get call prep: `/csm:call-prep [account]`"
- "Executive re-engagement play — check sponsor status: `/csm:stakeholder-map [account] --sponsor-risk`"
- "Expansion signal confirmed — want to prepare the handoff to AE? `/csm:value-statement [account]`"
- "Play complete — update the health review: `/csm:health-score-review [account]`"
