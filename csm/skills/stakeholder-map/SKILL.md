---
name: stakeholder-map
description: >
  Build or update a stakeholder map for an account — contacts, roles, influence,
  relationship health, engagement gaps, and sponsor risk assessment. Use when
  preparing for a QBR, after an org change, or when relationship coverage feels
  thin. Produces both an internal analysis and a clean contact reference.
argument-hint: "[account name] [--map | --gap-analysis | --sponsor-risk]"
version: "1.0.0"
---

# /stakeholder-map

Surface who matters in this account, how healthy those relationships are,
and where engagement gaps create risk — calibrated to your CS motion.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/csm:cold-start-interview`.

Note from config:
- CS motion — high-touch has deeper stakeholder coverage requirements than tech-touch
- Escalation matrix — know who to loop in if executive sponsor is at risk
- Health model — sponsor engagement is often a health component; apply thresholds

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of stakeholder mapping request is this?
   - **Coverage Assessment** — baseline view of known contacts, missing roles, and role coverage against CS motion requirements
   - **Engagement Gap Detection** — contacts are known but engagement is cold or uneven; focus on who dropped off and what it signals
   - **Sponsor Risk Evaluation** — executive sponsor stability concern: departure signals, tenure, succession gaps, renewal proximity
   - **Influence Mapping** — understanding decision dynamics: who blocks, who accelerates, who holds real authority vs. named authority
   - **Pre-Event Preparation** — map built or refreshed for an upcoming QBR, renewal, or executive meeting; recency is critical

2. **CONSTRAINTS**: What limits the solution space?
   - CS motion (high-touch vs. tech-touch) determines minimum role coverage and dormancy thresholds — check config before applying defaults
   - Data source freshness: CRM contact lists decay; never present contacts as current without verifying last-activity date
   - Confidentiality: stakeholder maps are internal documents — never include in customer-facing deliverables
   - Escalation matrix must be configured before routing sponsor risk actions — flag if missing
   - Detractor designation requires direct evidence (stated opposition, negative NPS) — inference from silence or title is prohibited

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - Is this account single-threaded? (Only one active contact across all roles = immediate risk regardless of other signals)
   - Does the executive sponsor's observed behavior match their CRM role? (Title ≠ authority — verify through contract signatures, QBR attendance, stated decision power)
   - Are dormancy thresholds role-appropriate? (Executive quarterly contact is healthy; champion 30-day silence in high-touch is declining)

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Presenting CRM contact lists as stakeholder coverage — CRM includes departed, inactive, and irrelevant contacts; filter by recency and verify role
   - Treating all silence equally — a 45-day gap means different things for an executive sponsor vs. a day-to-day champion
   - Inferring influence from org-chart proximity instead of observed behavior (call attendance, stated authority, escalation patterns)
   - Labeling contacts as detractors based on silence or tone without direct evidence
   - Escalating sponsor risk from a single signal (one missed QBR, one LinkedIn update) — require 2+ independent signals
   - Building an exhaustive 20+ contact map when the top 8-10 by influence and recency would surface the actual signal

**After execution**, verify:
- Does the output answer the implicit question the CSM is asking?
- Are all data sources timestamped and staleness-flagged?
- Is the output mode matched to the actual need?
- Confidence: [High] if 2+ live sources corroborate / [Medium] if single-source or partially stale / [Low] if user-provided context only — state which.

**For complex scenarios**, load additional reasoning:
- Domain-specific blueprint: `references/reasoning-blueprint.md`

## Mode

`--map`: Full stakeholder map — all known contacts, roles, influence, last contact,
relationship health, and engagement notes.

`--gap-analysis`: Focus on engagement gaps — who should be engaged but isn't,
how long since last contact, risk of orphaned relationships.

`--sponsor-risk`: Assess executive sponsor health specifically — tenure, engagement
history, signals of departure risk, succession path.

Default: `--map`.

---

## Data gathering

**Pull from connected integrations:**

- CRM: contact list with titles, departments, roles, last activity date
- Call recording: attendees across last 3-5 calls — who's been on calls,
  who's dropped off
- CS Platform: any stakeholder engagement health signals if tracked

**Prompt for missing context:**

> "To build a useful stakeholder map, I need to know who's involved at [account].
> Tell me: who's the executive sponsor? Who's the day-to-day champion? Are there
> any stakeholders who've gone quiet or changed recently?"

For high-touch motion: aim for at minimum executive sponsor + champion + end-user
representative in the map. Flag any missing tier as a gap.

For tech-touch motion: key contact minimum is one champion or primary point of
contact. Executive sponsor may not be a regular touchpoint — note the difference.

---

## Stakeholder map structure

---

**Stakeholder Map — [Account Name]**
*[Date] · INTERNAL — not for distribution*

---

### Contact register

| Name | Title | Department | Role in account | Influence | Last contact | Engagement health |
|------|-------|------------|----------------|-----------|-------------|-------------------|
| [Name] | [Title] | [Dept] | [Executive sponsor / Champion / End user / Economic buyer / Detractor / Unknown] | [High / Medium / Low] | [Date or "never"] | [Active / Declining / Dormant / Unknown] |

**Role definitions for this account:**
- **Executive sponsor:** Ultimate budget authority; renewal decision-maker; attends exec reviews
- **Champion:** Day-to-day advocate; drives internal adoption; primary CSM contact
- **Economic buyer:** Signs contracts; may not be involved in day-to-day
- **End user representative:** Provides product feedback; adoption signal
- **Detractor:** Known or suspected resistance to the product or the relationship
- **Unknown:** Contact identified but role and influence not yet assessed

**Engagement health thresholds (from configured CS motion):**
- High-touch: Declining = >30 days no contact; Dormant = >60 days no contact
- Tech-touch: Declining = >60 days; Dormant = >90 days
- Adjust thresholds for executive vs. operational contacts

---

### Relationship health summary

**Strong relationships:**
- [Name] ([role]): [1-line note on what makes this relationship strong]

**Relationships at risk:**
- [Name] ([role]): [Last contact: date] — [specific risk signal] `[review]`
- [Name] ([role]): [Dormant / never engaged / tone shifted on last call]

**Missing coverage:**
- [Role / tier] not currently covered — no known contact in this role at [account]

---

### Executive sponsor assessment

**Current executive sponsor:** [Name], [Title]

| Signal | Status | Notes |
|--------|--------|-------|
| Tenure in role | [N months] | [New exec, established, or unknown] |
| Last direct contact | [Date] — [N days ago] | [Call / email / meeting] |
| QBR attendance | [Regular / Irregular / Never] | [Last attended: date] |
| LinkedIn activity | [Active / Not monitored] | [Recent company change signal if visible] |
| Internal champion report | [Stable / Concerned] | [What the champion has said, if anything] |
| Contract signatory | [Yes / No / Unknown] | |

**Sponsor risk level:** [Low / Medium / High]

Risk indicators:
- New in role (<90 days) → onboarding exposure; build relationship before renewal
- Long-tenured but disengaged → may be a figurehead; find the real decision-maker
- Recent org change at their level → potential departure risk
- Missed two consecutive QBRs → engagement risk; escalate per matrix

**Succession plan:**
Who is the secondary sponsor or internal champion who could fill this role?
[Name / "Unknown — no identified successor"] `[review if unknown]`

---

### Influence map

Narrative description of how decisions move through this account. Who influences
whom? Who blocks decisions? Who accelerates them?

> "[Champion name] is the primary driver of internal adoption — all end-user
> onboarding goes through them. [Exec sponsor name] is the economic buyer but
> delegates day-to-day decisions to [Champion]. [Finance contact name] surfaces
> at renewal; has blocked two vendor renewals in the past 18 months per public
> filings [if known from external research]."

Keep this concise — 3-5 sentences. If influence dynamics are unknown, say so.
Don't fabricate relationship dynamics from titles alone.

---

### Engagement gap analysis

**Who should be engaged but isn't:**

| Contact | Role | Gap | Why it matters | Recommended action |
|---------|------|-----|---------------|--------------------|
| [Name] | [Role] | [N days / never] | [Risk if gap continues] | [Specific action] |

**Who has gone quiet (declining engagement):**

| Contact | Role | Previously engaged | Last contact | Signal |
|---------|----|------|------------|--------|
| [Name] | [Role] | [How engaged they were] | [Date] | [Drop off pattern] |

**Who is new and not yet mapped:**

> "[Account] has an org change — [Name] joined as [title] on [date]. No contact
> established yet. Recommend an introduction call before the next QBR." `[review]`

---

### Recommended actions

1-3 specific actions based on the gap analysis. Not generic.

Examples:
- "Schedule an executive sponsor touch before [date] — last contact was [N] days ago,
  approaching the configured [threshold] for high-touch accounts. Suggested: 15-minute
  briefing on [relevant topic]."
- "Identify a secondary champion — [current champion name] is the only internal
  advocate; single-threaded relationship is a renewal risk."
- "Request introduction to [Economic buyer name] before renewal — they sign contracts
  but have never been on a call."
- "Route exec sponsor risk per escalation matrix: notify [configured contact] via
  [channel] within [SLA]."

---

## Sponsor risk mode (`--sponsor-risk`)

Output only the executive sponsor assessment section plus a 1-paragraph risk
narrative and specific next action. Use this for a quick check rather than a
full map rebuild.

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live — [N] contacts retrieved | call recording: attendees from last [N] calls | user provided | conversation context]
> - **Data as of:** [timestamp]
> - **Relationship health assessments:** [Based on last-contact dates from CRM | partially inferred from call attendee patterns | user-provided description]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Internal document:** Do not share this map or the engagement health assessments externally without removing internal notes and health signals.

---

## Output

Stakeholder map — format driven by `--standard` (default) or `--sponsor-risk` flag.
Standard output: contact table with role, influence tier, sentiment, and engagement
recommendation. Sponsor risk mode adds executive vulnerability assessment and
mitigation actions. See mode-specific sections for field-level structure.

## Guardrails

**Relationship health is a heuristic.** Engagement gap thresholds are configurable
baselines, not diagnostic verdicts. A contact who hasn't replied in 45 days may
be on leave, may be thriving, or may be disengaged — the map flags the gap for
the CSM's judgment, not for automatic escalation.

**Influence dynamics require caution.** Inferences about who influences whom must
be drawn from direct observations (call attendance, communication patterns,
stated roles) — not from org chart proximity alone.

**Detractor designation.** Only label a contact as a detractor if there is direct
evidence (expressed opposition, negative NPS, stated objection). Do not infer
detractor status from lack of engagement or from a title.

**Sponsor departure signal.** If the executive sponsor shows departure risk signals
(new role on LinkedIn, internal champion mentions transition), route per the
configured escalation matrix before drawing conclusions.

**No customer-facing distribution.** The stakeholder map is an internal document.
Do not share with the customer or include in customer-facing deliverables.

---

## After the map

- "Want to run a health review for this account? `/csm:health-score-review [account]`"
- "Sponsor risk is high — want a risk memo? `/csm:risk-flag [account]`"
- "Building a QBR? Add stakeholder context to it: `/csm:qbr-builder [account]`"
- "Prepping for a call with the exec sponsor? `/csm:call-prep [account]`"
