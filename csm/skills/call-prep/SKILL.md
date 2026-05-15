---
name: call-prep
description: >
  Pre-call preparation brief — agenda, attendee context, recommended talking
  points, and questions calibrated to your CS motion and account state.
  Use 24-48 hours before any customer call: kickoff, QBR, health check,
  renewal conversation, or ad-hoc check-in. Pairs with account-research for
  full context.
argument-hint: "[account name] [call type: kickoff | qbr | health | renewal | check-in | custom]"
version: "1.0.0"
---

# /call-prep

Produce a focused pre-call brief: what to cover, who's attending, what to listen
for, and what to leave the call having accomplished.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- CS motion — shapes how directive vs. collaborative the agenda framing is
- Health model — determines which signals to surface before the call
- Playbook sources — pull call-specific templates if configured
- Escalation matrix — know the routing before the call if risk signals are present

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G1 (health scores are heuristics — do not frame as churn probability), G2 (expansion signals require economic buyer qualification), G5 (confidentiality check before distributing internal account data externally).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Call type detection

If the user provides a call type argument, use it. If not, infer from context:

- **Kickoff** — first call with a new account; onboarding just started
- **QBR** (Quarterly Business Review) — periodic value review; typically Q-aligned
- **Health check** — triggered by health signal; may be Yellow/Red account
- **Renewal** — within 90 days of renewal date; commercial context present
- **Check-in** — regular cadence call; no major trigger
- **Custom** — user describes the call purpose; adapt the brief structure to it

If type cannot be determined: ask one question — "What's the purpose of this call?"
Do not build a generic brief.

---

## Data gathering

Before building the brief, pull what's available.

**First, check if an account-research brief exists in this session.** If the user
already ran `/csm:account-research` for this account, use that context instead of
re-pulling from connectors.

**If no prior account-research:**

Pull from connected integrations (per configured profile):
- CRM: account snapshot, renewal date, ARR, key contacts and their titles
- CS Platform: health score and components, open CTAs
- Call recording: last 1-2 calls — date, attendees, key topics, open action items
- Document storage: most recent success plan or QBR (date + status)

Minimum viable brief (no connectors):
> "I don't have live account data. Tell me: Who's on the call? What's the account
> health? Any recent context I should know? I'll build the brief from what you share."

---

## Brief structure

Produce in this order. Omit sections with no data rather than filling with placeholders.

---

### Call Prep — [Account Name]
*[Call type] · [Date / time if known] · [Duration if known]*

---

**Purpose and desired outcome**

One sentence: why this call exists.
One sentence: what "a good call" looks like at the end.

Examples by type:
- Kickoff: "Establish shared success criteria, introduce the onboarding plan,
  and confirm sponsor engagement — account leaves knowing what happens next."
- QBR: "Demonstrate value delivered against agreed success criteria and align
  on next-period priorities — customer leaves feeling forward momentum."
- Health check: "Understand the root cause of [specific signal], agree on a
  recovery action, and set a follow-up date — call leaves no ambiguity about
  next steps."
- Renewal: "Surface value realized, pre-empt known objections, advance toward
  renewal commitment — call ends with a next step, not an open loop."

---

**Who's on the call**

| Name | Title | Role in account | Notes |
|------|-------|----------------|-------|
| [Name] | [Title] | [Executive sponsor / Champion / End user / Finance contact / Detractor] | [Last contact date / relationship note] |

Flag:
- Any attendee who is new or unrecognized — "This may be your first call with
  [name]; intro context before the call if possible."
- Missing executive sponsor: "Executive sponsor [name] is listed but not confirmed
  on this call — flag if absent at start."
- High-value attendees who haven't been on a call in >60 days.

Internal attendees (AE, SE, CSM manager) — list separately if provided.

---

**Suggested agenda**

Calibrate depth and format to call type and configured CS motion.

For **high-touch** motion: named agenda items with owner and time box.
For **tech-touch** motion: three bullet points; the call is shorter.
For **hybrid**: match the segment this account sits in.

*[Call type: Kickoff — example structure]*

| Time | Agenda item | Owner |
|------|-------------|-------|
| 0:00–0:05 | Introductions and call purpose | CSM |
| 0:05–0:20 | Customer goals and success criteria (draft to validate) | Customer |
| 0:20–0:35 | Onboarding plan walkthrough — milestones, owners, timeline | CSM |
| 0:35–0:45 | Q&A and open items | Both |
| 0:45–0:55 | Next steps — confirmed actions, dates, owners | CSM |
| 0:55–1:00 | Buffer | — |

*[Call type: QBR — example structure]*

| Time | Agenda item | Owner |
|------|-------------|-------|
| 0:00–0:05 | Welcome and framing | CSM |
| 0:05–0:20 | Value delivered — metrics vs. success criteria | CSM |
| 0:20–0:35 | Customer highlights and wins | Customer |
| 0:35–0:45 | Challenges and roadblocks | Both |
| 0:45–0:55 | Next quarter priorities and roadmap alignment | Both |
| 0:55–1:00 | Next steps | CSM |

*[Call type: Health check — example structure]*

| Time | Agenda item | Owner |
|------|-------------|-------|
| 0:00–0:05 | Quick check-in | CSM |
| 0:05–0:15 | Review of specific signal: [signal from health model] | CSM opens |
| 0:15–0:30 | Customer's perspective — what's changed | Customer |
| 0:30–0:40 | Joint recovery plan — specific actions, owners, dates | Both |
| 0:40–0:45 | Confirm follow-up | CSM |

For custom call type: adapt the structure to the described purpose.

---

**Recommended talking points**

3-5 specific talking points calibrated to the account's current state and call type.
Not generic. Reference account-specific context where available.

Format:
- **[Topic]:** [One sentence context] → [Suggested framing or question]

Examples:
- **Success criteria progress:** "The team hit [metric] last quarter — X% above baseline.
  Lead with this before moving to gaps."
- **Usage signal:** "Weekly active users dropped 18% last month — ask what changed on
  their end before attributing it to product."
- **Renewal positioning:** "Renewal is in 67 days. This call isn't the commercial
  conversation — the goal is alignment, not close. Defer pricing until the sponsor
  is engaged."
- **Expansion lead (internal, don't raise directly):** "Champion mentioned interest
  in [feature] on the last call — listen for confirmation and route to AE if validated."

Flag any talking point that references a sensitive topic (executive departure, open
escalation, competitive evaluation) with `[review]` and a note on whether to raise
it proactively or wait for the customer to open it.

---

**Key questions to ask**

3-5 open questions to ask during the call. Not a script — prompts to open the
conversation in the direction that matters.

By call type:
- Kickoff: "What does success look like for you personally, not just the team?"
  / "Who will feel the impact most when this is working?"
- QBR: "What hasn't worked as well as you'd hoped?" / "What decision is this
  review helping you make?"
- Health check: "What's changed on your end in the last [timeframe]?" / "What
  would need to be true for this to be a non-issue in 30 days?"
- Renewal: "What would make you confident recommending a renewal to your leadership?"
  / "What's your main concern going into renewal?"

---

**What to listen for**

2-3 specific signals to track during the call. If heard, note them for post-call
action.

- **Risk signals:** executive sponsor departure signal, budget freeze language,
  competitor mention, "we're evaluating our options"
- **Expansion signals:** "we're thinking about [use case]", mention of new team
  or initiative that could use the product — tag `[early signal — not yet qualified]`
- **Relationship signals:** tone shift vs. previous calls, new decision-maker
  introduced without advance notice, team structure change mentioned

---

**Post-call actions (pre-loaded)**

Prepare these now so the call ends with immediate follow-through.

| Action | Owner | Due | Notes |
|--------|-------|-----|-------|
| Send follow-up email with recap and agreed actions | CSM | Within 24h | Use `/csm:account-research --brief` to verify action item list |
| Log call in CRM with next activity date | CSM | Same day | — |
| [Context-specific action] | [Owner] | [Date] | — |

If health check or risk call: pre-load the escalation routing per configured matrix.
"If [escalation trigger] is confirmed on this call, route to [person] via [channel]
within [SLA]."

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live | CS Platform ✓ live | Gong ✓ live | prior account-research session | user provided]
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before the call:** [1-2 specific things to confirm — e.g., "verify attendee list is current", "confirm exec sponsor is joining"]

If clean: `⚠️ Reviewer note: data verified · no flags · confirm attendee list before call`.

---

## Output

Call preparation brief — single structured markdown document. Sections vary by
detected call type (EBR, renewal, health check, expansion, escalation, kickoff).
All briefs include: account context snapshot, attendee profiles, agenda, key
questions, and suggested next step. See **Brief structure** section for field-level detail.

## Guardrails

**Expansion stays internal.** Any expansion signal in the call prep is for
internal reference — not a topic to raise with the customer unless the AE or
AM has qualified it.

**Health signals inform, not script.** If the account is Yellow/Red, the brief
names the signals and suggests questions — it doesn't tell the CSM to "tell
the customer they're at risk." That framing is the CSM's judgment call.

**Renewal framing is not a sales script.** In a renewal call, the brief
supports the conversation — it doesn't produce a pricing or negotiation script.
For commercial prep, use `/csm:renewal-readiness`.

**No destination check bypass.** If any part of this brief is shared externally
(e.g., a pre-read for the customer), the reviewer must remove internal health
scores, stakeholder notes, and any expansion signal tags before sending.

---

## After the brief

> "Brief ready. Anything you want to add or adjust before the call?"

If the call is less than 2 hours away: "Need a shorter version? I can trim to
agenda + talking points only."

Post-call: "Want to log action items and send the follow-up? Paste the call notes
and I'll draft the email and CRM update."
