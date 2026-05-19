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
deployment_target: plugin
---

# /call-prep

[PROPOSED]

## Use When
- 24-48 hours before any customer call: kickoff, QBR, health check, renewal, escalation, check-in
- Account has active risk signals and you need a structured brief before engaging
- Executive sponsor is attending and preparation needs to be higher-fidelity than usual
- Renewal is within 90 days and you need value alignment framing before the commercial conversation

## Do NOT Use For
- Post-call logging or follow-up drafting — use post-call workflow instead
- Renewal commercial prep (pricing, negotiation) — use /csm:renewal-readiness
- Account deep-dive research without a call scheduled — use /csm:account-research
- Routine check-ins with nothing substantive to discuss — recommend async instead

## Typical Activation
"/csm:call-prep Acme Corp qbr"
"/csm:call-prep Acme Corp renewal"
"/csm:call-prep Acme Corp kickoff"
"Prep me for my call with [customer] tomorrow"
"Build a brief for my health check with [account]"

---

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

Before generating output, apply these primers:

1. **CLASSIFY**: What type of call prep request is this?
   - **Discovery / Kickoff**: First or early-stage call — sparse historical data, goal is success criteria alignment and relationship establishment
   - **QBR / Executive Business Review**: Periodic value review with executive audience — requires metrics against success criteria, forward-looking priorities
   - **Health Check / At-Risk**: Triggered by a health signal — usage drop, NPS decline, support spike, or champion departure; shorter format, diagnostic focus
   - **Renewal Conversation**: Within 90 days of renewal — commercial context present but CSM role is value alignment and objection surfacing, not close
   - **Escalation / Recovery**: Active or recently resolved escalation — trust is damaged; goal is confidence restoration and remediation confirmation
   - **Routine Check-in**: Regular cadence call with no major trigger — risk of perfunctory meeting; may recommend async instead

2. **CONSTRAINTS**: What limits the solution space?
   - Which data sources are available? (CRM, CS platform, call recordings, documents) — fewer than 3 of 4 = low-confidence brief, flag explicitly
   - Is the attendee list confirmed or assumed? Unconfirmed attendees cap the brief's value
   - What was the outcome of the last call? Open action items carry forward — never drop them silently
   - Is there an active escalation or competitive signal that changes the entire call framing?
   - G4: Do not recommend escalation without a named escalation path configured in the escalation matrix
   - G5: Internal data (health scores, ARR, expansion signals) must never appear in customer-facing output
   - G7: Flag any data older than 30 days with source date and staleness indicator

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - Are the success criteria being referenced still the criteria the customer cares about, or have priorities shifted since they were set?
   - Is the right stakeholder on this call? Missing executive sponsor on a QBR or missing economic buyer on a renewal changes the call's ceiling
   - Has anything been promised to this customer (in escalation, prior calls, or success plans) that hasn't been delivered yet?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - :x: Building the brief around product usage metrics instead of business outcomes the customer's executive sponsor cares about
   - :x: Leading a health check or escalation call with platform data instead of opening with curiosity and listening
   - :x: Including expansion signals, health scores, or internal stakeholder assessments in any material that could reach the customer
   - :x: Preparing a full brief for a routine check-in when there's nothing substantive to discuss — recommend async instead
   - :x: Producing renewal prep that crosses into pricing, discount, or negotiation territory — that's AE/AM scope

**After execution**, verify:
- Does every talking point reference account-specific context, not generic advice?
- Is the internal/external boundary respected — no health scores, expansion tags, or relationship assessments in customer-visible content?
- Does the brief identify the single most important thing to accomplish on this call?
- Confidence: [High/Medium/Low] because [data source coverage, attendee confirmation status, signal freshness]

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

---

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: outbound_allowlist (CRM, CS platform, call recording tool, document storage per configured integrations)
- filesystem_write: false
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- Internal health scores, expansion tags, and stakeholder assessments must not appear in any customer-visible output
- If account-research context exists in the session, use it — do not re-pull from connectors
- If config files are missing or contain [PLACEHOLDER] markers, halt and prompt for /csm:cold-start-interview
- Reviewer note must always be present — flag data freshness and any items requiring CSM judgment
