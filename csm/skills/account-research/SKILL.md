---
name: account-research
description: >
  Pre-call and pre-meeting account brief — pulls CRM data, health signals,
  call history, and usage context into a structured one-page snapshot.
  Use before any customer call, QBR, health review, or stakeholder meeting.
  Works standalone (paste context) or with connected CRM, CS Platform, and
  call recording tools.
argument-hint: "[account name or CRM ID] [--brief | --deep | --stakeholders]"
version: "1.0.0"
---

# /account-research

Produce a one-page account brief calibrated to your CS motion, health model,
and escalation matrix from the configured practice profile.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either file is missing or still contains `[PLACEHOLDER]` markers, stop:

> "This skill needs your practice profile before it can produce calibrated output.
> Run `/csm:cold-start-interview` — it takes 2 minutes for a quick start or 15
> minutes for full setup. Without it, account research output will be generic and
> won't reflect your health model, escalation chain, or CS motion."

If configured, note:
- CS motion (high-touch / tech-touch / hybrid / implementation+handoff)
- Health model components and Red/Yellow thresholds
- Available integrations (from `## Available integrations` in the config)

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of account research request is this?
   - **Pre-Call Snap Brief**: Time-pressured, single account, call imminent. Optimize for speed and recency over completeness.
   - **QBR / Executive Meeting Prep**: Higher-stakes audience, needs polished structure with validated health components and stakeholder context.
   - **Risk / Escalation Review**: Account is Red or trending down. Brief feeds an escalation workflow — separate leading from lagging indicators.
   - **Portfolio Scan**: Multiple accounts for pipeline review or 1:1. Requires consistent structure, per-account staleness, and confidentiality controls.
   - **Stakeholder-Focused**: Request centers on who matters — engagement gaps, shadow stakeholders, influence mapping.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: Health scores are component signals, not churn verdicts — decompose into observable signals, never frame as "will churn."
   - G2: Expansion signals are internal-only, tagged `[early signal — not yet qualified]`, and routed to AE/AM — never in customer-facing output.
   - G4: Escalation recommendations must route through the configured escalation matrix with named owner, channel, and SLA — no generic "escalate to your manager."
   - G5: Confidentiality check required before any output containing ARR, contract terms, or health scores leaves the CSM's view — especially portfolio-level briefs.
   - G7: Flag stale data with source date and staleness indicator — CRM >7 days, CS Platform >3 days, call data >14 days.
   - Connected integrations limit what can be retrieved — flag gaps, never silently omit.

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - What changed since the last touchpoint? The delta matters more than the current state — surface it explicitly.
   - Is the health score decomposed into actionable components, or is it just a color? If just a color, decompose before presenting.
   - Are there shadow stakeholders (on calls but not in CRM) or ghost stakeholders (in CRM but never on calls)? Cross-reference when call data is available.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting stale CRM or usage data without a timestamp or staleness flag — the CSM acts on outdated information.
   - Treating a composite health score as a churn prediction instead of decomposing its component signals.
   - Listing contacts without engagement recency — a name/title list is not a stakeholder map.
   - Surfacing expansion signals in output that could reach the customer.
   - Providing a generic escalation path ("talk to your manager") instead of routing through the configured matrix.
   - Generating deep-mode output for a CSM who needs a quick snap brief before a call in 10 minutes.

**After execution**, verify:
- Does the brief answer the implicit question ("am I prepared for this interaction")?
- Are all data sources timestamped and staleness-flagged per G7?
- Is the output mode (brief/deep/stakeholders) matched to the actual need?
- Confidence: [High] if 2+ live sources corroborate / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

## Output mode

Default: **brief** — one-page structured snapshot. Use for call prep, quick
account check-in, or pre-meeting review.

`--deep`: Adds a second section — call history themes, open support tickets
summary, detailed usage trend, and expansion signal scan.

`--stakeholders`: Adds a dedicated stakeholder map section — contacts, roles,
influence, relationship health, and engagement gaps. See also `/csm:stakeholder-map`
for a full standalone stakeholder analysis.

---

## Data gathering

### What to pull and from where

Check available integrations against the configured profile. Pull from all
connected sources; flag what was used and what wasn't.

**CRM (Salesforce / HubSpot or equivalent):**
- Account name, ARR, contract start and renewal date, contract terms
- Primary industry / segment
- CSM owner; AE / AM owner
- Contacts — name, title, department, email
- Open opportunities (expansion, renewal stage)
- Recent activity log (last 3-5 notable entries)

**CS Platform (Gainsight / Totango / ChurnZero / Vitally / Planhat):**
- Current health score and component breakdown (match against configured health model)
- Red/Yellow CTA or task queue
- Product usage — DAU, feature adoption, last login, usage trend (direction, not just number)
- NPS score and date, if available
- Account lifecycle stage (onboarding / adoption / value realized / at risk / churned)

**Call recording (Gong / Chorus):**
- Last 2-3 calls: date, attendees, key topics, action items mentioned
- Sentiment trend if the platform provides it
- Any flagged risks or objections from recent calls

**Document storage (Drive / SharePoint / Box):**
- Most recent success plan or QBR deck — pull date and headline status
- Open action items from last customer-facing document

**Fallback — nothing connected:**
> "I don't have live access to your CRM or CS Platform for this account. Paste
> the account details, recent call notes, or health snapshot and I'll build
> the brief from what you share."

### Probing order

1. Call CRM first — account identity anchor
2. CS Platform — health overlay
3. Call recording — recency context
4. Document storage — open items from last deliverable
5. Summarize what was retrieved and what gaps remain

If a tool call fails, note it in the reviewer note and proceed with available data.
Never infer health status from partial data without flagging the gap.

---

## Brief structure

Produce the brief in this order. Suppress headers if a section has no data.

---

### [Account Name] — Account Brief
*[CS motion] · [Segment] · Data as of [timestamp]*

---

**Account snapshot**

| Field | Value |
|-------|-------|
| ARR | $[amount] |
| Renewal date | [date] — [N days] away |
| Segment | [SMB / Mid-market / Enterprise] |
| CSM owner | [name] |
| AE / AM owner | [name] |
| Contract start | [date] — [N months] tenure |
| Lifecycle stage | [Onboarding / Adoption / Value Realized / At Risk] |
| Health | [Red / Yellow / Green] — see signals below |

---

**Health signals**

Apply configured health model components and thresholds. Show components, not
just the verdict.

> Health as of [timestamp from CS Platform, or "not live — user-provided"]:
> - Product usage: [direction + specific signal, e.g., "weekly active users down 18% vs. 30-day avg"]
> - Engagement: [last call date, last exec contact, email response rate if known]
> - Support: [open tickets, any P1/P2 escalations, ticket trend]
> - NPS: [score and date if available; "not available" if not]
> - [Additional configured component]: [signal]
>
> Overall: [Red / Yellow / Green] — above configured [Red threshold] / [Yellow threshold]
> from profile.
>
> *Health scores are component signals, not churn verdicts. These signals inform
> judgment; they don't replace it.*

If health score is unavailable (no CS Platform connected or no data returned):
> "Health signals unavailable — no CS Platform data retrieved this session. Health
> assessment based on conversation context only."

---

**Key stakeholders**

List the contacts that matter most for this account. Flag engagement gaps.

| Name | Title | Department | Last contact | Notes |
|------|-------|------------|-------------|-------|
| [Name] | [Title] | [Dept] | [Date] | [Executive sponsor / Champion / Detractor / Unknown] |

If an executive sponsor role is empty or last contact is >60 days: flag `[review]`
with the gap explicitly noted.

In high-touch motion, flag any key stakeholder not contacted in >30 days.
In tech-touch motion, flag any account with no contact in >90 days.
Adjust thresholds based on configured CS motion.

---

**Recent activity**

2-4 bullets. Recency over completeness.

- [Date] — [call / email / QBR / support ticket / health alert] — [1-line summary]
- [Date] — [...]

If call recording is connected: pull the last 2 calls. Note key topics and any
open action items from the calls. Do not summarize call content in customer-safe
framing without checking the destination audience.

---

**Open items**

From last customer-facing document or call action items. Flag stale items.

| Item | Owner | Due | Status |
|------|-------|-----|--------|
| [Action item] | [CSM / Customer / AE] | [Date] | [Open / Overdue / Blocked] |

If no document or call data available: "No open items retrieved — paste last QBR
or call notes to populate."

---

**Renewal context**

Surface only if renewal is within 180 days OR account is Yellow/Red.

> Renewal in [N] days — [on track / at risk / unknown].
> [1-2 sentences: key factors driving renewal confidence or risk]
> Escalation routing per configured matrix: [route to whom, how, SLA]

If outside 180-day window and account is Green: omit this section to keep the
brief focused.

---

**Recommended next actions**

1-3 specific actions calibrated to the account's current state and configured
CS motion. Not generic.

Examples by state:
- Green / healthy: "Prepare QBR agenda — last QBR was [date]; due within [N weeks] per cadence."
- Yellow: "Schedule executive check-in — sponsor [name] last contacted [date]. Address [specific signal]."
- Red: "Escalation: route per matrix — [route] within [SLA]. Prepare risk memo for [audience]."
- Approaching renewal: "Renewal readiness check — run `/csm:renewal-readiness [account]`."

---

## Reviewer note

Every brief includes:

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live | CS Platform ✓ live | Gong ✓ live | user provided | conversation context only]
> - **Data as of:** [timestamp per source, or "N/A — user-provided"]
> - **Retrieved:** [what was actually pulled — account record, health signals, last 2 calls, etc.]
> - **Gaps:** [what was not available — e.g., "no CS Platform data; health based on user-provided context"]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before sharing:** [destination check — is this brief going to the customer or staying internal?]

If clean: `⚠️ Reviewer note: CRM + CS Platform verified · data as of [timestamp] · no flags`.

---

## Deep mode additions (`--deep`)

Append after the standard brief:

**Call history themes** (last 90 days)
- [Theme 1]: mentioned in [N] of [M] calls — [1-line summary]
- [Theme 2]: [...]
- Objections / risks surfaced: [list or "none flagged"]

**Support ticket summary**
- Open: [N] tickets — [P1: N / P2: N / P3-P4: N]
- Trend: [up / down / flat vs. 30-day prior]
- Oldest open ticket: [date] — [1-line description]

**Usage trend**
- [Metric 1] (e.g., weekly active users): [value] — [direction and % change vs. 30-day avg]
- [Metric 2] (e.g., feature X adoption): [value] — [direction]
- Key drop or spike: flag any >20% movement since last brief

**Expansion signals** (tag as early leads only)
- [Signal]: [1-line observation] `[early signal — not yet qualified]`
- If none: "No expansion signals flagged in available data."

---

## Guardrails

These apply unconditionally:

**Health as heuristic.** Never frame a health score or color as "this account
will churn." Frame as specific signals observed: "usage is down 18% week-over-week,
which is below the configured Yellow threshold."

**Destination check.** The account brief is an internal document. Before sharing
any version with the customer or a third party, the reviewer must check that
account-specific details (ARR, contract terms, internal health scores, stakeholder
notes) are appropriate for that audience.

**Expansion stays internal.** Any expansion signal in the brief is tagged
`[early signal — not yet qualified]` and routes to the AE / AM — never appears
in customer-facing deliverables without explicit authorization.

**No silent staleness.** If CRM data was last updated more than 7 days ago,
flag it in the reviewer note. If CS Platform data is more than 3 days old, note it.

**Escalation routing comes from the matrix.** When the brief surfaces a risk that
meets an escalation threshold, route using the configured escalation matrix —
not a generic "escalate to your manager."

---

## After the brief

Offer contextual next steps based on account state:

- **Renewal <90 days + Yellow/Red:** "Want me to run a renewal readiness check? `/csm:renewal-readiness [account]`"
- **Risk signals:** "Want a structured risk memo for this account? `/csm:risk-flag [account]`"
- **QBR due:** "Ready to build the QBR? `/csm:qbr-builder [account]`"
- **Stakeholder gap flagged:** "Want a full stakeholder map? `/csm:stakeholder-map [account]`"
- **Call today:** "Need call prep? `/csm:call-prep [account]`"

Offer one suggestion — the most relevant one given the account's current state.
Don't list all five.
