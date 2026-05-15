# QBR Prep Agent — Managed Agent Cookbook

**Agent type:** On-demand orchestrator with 4 subagents  
**Cadence:** On-demand (triggered per account before QBR)  
**Trigger:** On-demand via `/csm:qbr-prep-agent <account-name>` or scheduled 5 days before renewal  
**Output:** Complete QBR preparation package — data pull, narrative draft, slide outline, and talking points

---

## What This Agent Does

The QBR Prep Agent automates the most time-consuming part of QBR preparation: gathering
data across systems and drafting the narrative. A CSM triggering this agent gets back a
complete prep package in minutes rather than spending 2–4 hours assembling the deck manually.

The agent does not replace the CSM's judgment — it assembles the facts, surfaces the
story the data tells, and produces draft materials that the CSM reviews and personalizes.
Every output is explicitly labeled as a draft.

**Outputs:**
- Account data pull: ARR, renewal date, stakeholder map, usage metrics, support history
- Success criteria achievement assessment against the account's stated goals
- Narrative draft: what went well, what to address, strategic context for next period
- Slide-by-slide outline with talking points (not a built deck — a structured guide)
- Renewal risk flag if signals warrant attention before the QBR

---

## Architecture

```
Orchestrator: QBR Prep Agent
│
├── Subagent 1: Account Data Assembler
│   Pulls account data from all available connectors: CRM (account history, ARR,
│   stakeholders, renewal date), product usage, support history. Returns a
│   structured account profile for the QBR period.
│
├── Subagent 2: Achievement Analyzer
│   Reviews the account's success criteria (from onboarding plan or CSM input)
│   against the data assembled. Produces an achievement assessment: what was
│   accomplished, what wasn't, and what the evidence shows.
│
├── Subagent 3: Narrative Drafter
│   Writes the QBR narrative — a structured story arc that covers the review
│   period, achievement highlights, challenges, and strategic look-ahead.
│   Drafted for CSM review and customization.
│
└── Subagent 4: Slide Outline Generator
    Produces a slide-by-slide outline with recommended content per slide and
    talking points for each. Does not generate slide files — produces a
    structured guide the CSM uses to build the actual deck.
```

The orchestrator sequences subagents, passing the account profile forward through
the chain. The Narrative Drafter and Slide Outline Generator work in parallel after
the Achievement Analyzer returns — the orchestrator manages this parallelism.

---

## Orchestrator System Prompt

```
You are the QBR Prep Agent orchestrator for a Customer Success team. Your job is to
produce a complete QBR preparation package for a specific account.

Your configuration lives at:
~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md

And company profile at:
~/.claude/plugins/config/claude-for-customer-success/company-profile.md

Read both before starting. Fields you need:
- CRM connector name
- Product usage connector (if configured)
- Support connector (if configured)
- QBR template preference (executive / operational / renewal-focused)
- CS methodology (for recommended next plays in the narrative)
- CSM name (for authored sections)

Account identification:
  Ask: "Which account and what is the QBR date?" if not provided as an argument.

Execution sequence:

STEP 1 — Dispatch Account Data Assembler
  Pass: account name/ID, QBR date, connector names, review period (default: last 90 days)
  Receive: complete account profile (ARR, renewal, stakeholders, usage metrics, support
    history, account history notes)
  Do not proceed until complete.

STEP 2 — Dispatch Achievement Analyzer
  Pass: account profile from Step 1 + success criteria (from CRM or ask CSM)
  Receive: achievement assessment — scored review of each success criterion with
    evidence and status
  
  If success criteria are not in the CRM, pause and ask:
  "What are [account name]'s stated success criteria? I'll use these to frame
  the achievement assessment." Collect criteria before dispatching.

STEP 3 — Dispatch Narrative Drafter AND Slide Outline Generator in parallel
  Both subagents receive: account profile + achievement assessment + QBR template
  preference + CSM name + company profile context
  
  Narrative Drafter: returns full narrative draft
  Slide Outline Generator: returns slide outline

STEP 4 — Assemble and deliver
  Combine outputs into a single QBR prep package. Save to configured output path
  and/or present inline.
  Mark all sections explicitly as [DRAFT — requires CSM review].

Rules:
- Never present the narrative draft as final. Every narrative section carries
  [DRAFT — requires CSM review].
- If product usage data is unavailable, note this prominently in the achievement
  assessment — do not fabricate usage metrics.
- Renewal date must be pulled from CRM, not estimated. If CRM is unavailable,
  ask the CSM directly.
- Never include TtV figures or [review — internal planning target] metrics in any
  QBR output — these are internal planning benchmarks, not customer-facing metrics.
- The slide outline is a guide, not a commitment. Each slide's content is a
  recommendation; the CSM adapts based on the account relationship.
```

---

## Subagent 1: Account Data Assembler

**File:** `subagents/account-data-assembler.md`

**Role:** Data retrieval. Pulls everything needed for QBR prep from configured connectors
and returns a structured account profile.

**Tools required:**
- CRM connector — required (account data, stakeholders, ARR, renewal, history)
- Product usage connector — recommended (login frequency, feature adoption, active users)
- Support connector — recommended (ticket volume, open tickets, P1 history)
- NPS/CSAT connector — optional (sentiment scores, trend)

**Inputs from orchestrator:**
- Account name/ID
- QBR date
- Review period (default: 90 days prior to QBR date)
- Connector names

**Output format:**
```
account:
  name: [name]
  id: [CRM ID]
  segment: [segment]
  arr: [ARR — from CRM]
  product_tier: [tier]
  csm: [name]
  ae: [name]
  contract_start: [date]
  renewal_date: [date — from CRM; flag if estimated]

stakeholders:
  - name: [name]
    role: [exec sponsor|champion|technical lead|billing]
    contact: [email or Slack]
    engagement_level: [high|medium|low]
    last_contact_date: [date]

usage_metrics:
  review_period: [start date → end date]
  active_users: [count or null]
  total_provisioned: [count or null]
  logins_per_week_avg: [N or null]
  feature_adoption_score: [0-100 or null]
  top_features_used: [list or null]
  connector_used: [name or "not available"]

support_history:
  review_period: [dates]
  total_tickets: [count or null]
  open_tickets: [count]
  p1_tickets_period: [count or null]
  avg_resolution_days: [N or null]
  notable_issues: [list of ticket summaries or null]
  connector_used: [name or "not available"]

sentiment:
  last_nps_score: [0-10 or null]
  last_nps_date: [date or null]
  last_csat_score: [0-5 or null]
  nps_trend: [improving|declining|stable|insufficient data]
  connector_used: [name or "not available"]

account_notes:
  [Last 5 notable CRM notes or activity log entries in the review period]

data_as_of: [timestamp]
connectors_used: [list]
connectors_unavailable: [list or empty]
```

**Full subagent spec:** See `subagents/account-data-assembler.md`

---

## Subagent 2: Achievement Analyzer

**File:** `subagents/achievement-analyzer.md`

**Role:** Achievement assessment. Reviews each success criterion against available
evidence and produces a structured achievement status.

**Tools required:** None — works on data passed from orchestrator.

**Inputs from orchestrator:**
- Account profile from Account Data Assembler
- Success criteria (from CRM or CSM-provided list)

**Achievement scoring per criterion:**

| Status | Definition |
|--------|-----------|
| ✓ Achieved | Evidence confirms criterion was met; customer acknowledged |
| ◐ Partially achieved | Progress demonstrated but criterion not fully met |
| ○ Not achieved | No evidence of achievement; criterion unmet at QBR |
| ? Evidence unclear | Usage or outcome data not available to confirm |

**Output format:**
```
success_criteria_assessment:
  - criterion: [statement of criterion]
    status: [achieved|partial|not_achieved|unclear]
    evidence: [what the data shows — specific metrics or CRM notes]
    customer_acknowledgment: [confirmed|not confirmed|unknown]
    qbr_framing: [how to present this at the QBR — brief note]

overall_achievement:
  achieved_count: [N]
  partial_count: [N]
  not_achieved_count: [N]
  unclear_count: [N]
  summary: [2-3 sentences characterizing the overall achievement picture]

recommended_narrative_angle: [lead with success and address gaps | balanced review |
  address challenges directly and pivot to path forward]
renewal_risk_signal: [none | moderate — [reason] | high — [reason]]
```

**Full subagent spec:** See `subagents/achievement-analyzer.md`

---

## Subagent 3: Narrative Drafter

**File:** `subagents/narrative-drafter.md`

**Role:** Draft the QBR narrative. Produces a structured written narrative the CSM
reviews, personalizes, and adapts for the actual QBR conversation.

**Tools required:** None — works on data passed from orchestrator.

**Output format:**

```markdown
## QBR Narrative Draft — [Account Name]
[DRAFT — requires CSM review before use]
QBR date: [date] · Review period: [dates] · CSM: [name]

---

### Opening framing
[2-3 sentences: what this QBR covers and the relationship context. 
Written in first person from the CSM's voice.]

### What we accomplished together
[Achievement narrative: for each criterion marked Achieved or Partial,
describe what was accomplished in customer-outcome terms — not product terms.
Lead with outcomes the customer cares about.]

### Where we faced headwinds
[Honest, direct framing of unachieved criteria or challenges. Include what
was done to address them. Do not omit — unaddressed headwinds surface at
the QBR anyway; better to prepare than be caught.]

### What the data shows
[Usage metrics, support trends, sentiment — written as a narrative paragraph,
not a stat dump. Interpret what the numbers mean for the customer's goals.]

### Strategic look-ahead
[Based on CS methodology from config: recommended next plays and themes for
the coming period. 2-3 forward-looking points that connect to the customer's
stated goals.]

### Renewal context
[If renewal is within 90 days: brief, matter-of-fact framing. Do not open
renewal negotiation in the narrative — this is context for the CSM's
awareness, not scripted language for the QBR itself.]
```

All sections are explicitly marked [DRAFT]. The narrative is CSM-voiced but the CSM
is expected to rewrite heavily for their relationship context.

**Full subagent spec:** See `subagents/narrative-drafter.md`

---

## Subagent 4: Slide Outline Generator

**File:** `subagents/slide-outline-generator.md`

**Role:** Structure the QBR deck. Produces a slide-by-slide outline with recommended
content and talking points. Does not generate slide files.

**Tools required:** None — works on data passed from orchestrator.

**Template selection** (from config `qbr_template_preference`):

- `executive` — 8–10 slides, high-level, outcome-focused, minimal product detail
- `operational` — 12–15 slides, detailed usage metrics, feature adoption, roadmap
- `renewal-focused` — 10–12 slides, achievement-heavy opening, renewal value proposition

**Output format:**

```markdown
## QBR Slide Outline — [Account Name]
[DRAFT — structure only; CSM adapts content and ordering]
Template: [executive|operational|renewal-focused]

---

**Slide 1: Title and Agenda**
Recommended content: Account name, QBR date, CSM name, agenda list (3-4 items)
Talking point: [brief intro framing — 1 sentence]

**Slide 2: Partnership snapshot**
Recommended content: ARR, product tier, renewal date, key stakeholder names
Talking point: [acknowledge the relationship and review period]

**Slide 3: Goals we set together**
Recommended content: Success criteria stated at kickoff/last QBR
Talking point: [frame this as shared accountability, not a report card]

**Slide 4: What we accomplished**
Recommended content: Achieved criteria with evidence (usage, outcomes)
Talking point: [lead with customer-outcome language; avoid product feature language]

**Slide 5: Where we have more to do**
Recommended content: Partial or unachieved criteria with honest framing
Talking point: [name the challenge directly; pivot to what changes next period]

**Slide 6: Usage and adoption**
Recommended content: Active users, feature adoption trends, key metrics
Talking point: [connect adoption data to the outcomes they care about]

[Additional slides per template type]

**Slide [N]: What's next**
Recommended content: Top 3 recommended plays for next period
Talking point: [connect next-period work to the goals they've stated]

**Slide [N+1]: Renewal and partnership**
Recommended content: Renewal date, value delivered, next steps
Talking point: [for renewal-focused template only: value proposition restatement]
```

**Full subagent spec:** See `subagents/slide-outline-generator.md`

---

## Connector Requirements

| Connector | Required | Purpose |
|-----------|----------|---------|
| CRM (HubSpot, Salesforce, etc.) | Yes | Account data, renewal date, stakeholders, ARR |
| Product usage | Recommended | Adoption metrics for achievement evidence |
| Support (Zendesk, Intercom, etc.) | Recommended | Support history and ticket trends |
| NPS/CSAT | Optional | Sentiment evidence for achievement narrative |

If only the CRM is available, the agent still runs. The achievement assessment will note
which criteria cannot be evidenced due to missing connectors, and the narrative drafter
will flag those gaps explicitly rather than fabricating data.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Required config fields:
- `crm_connector`: CRM MCP connector name
- `qbr_template_preference`: `executive` | `operational` | `renewal-focused`
- `output_path`: Where to save the QBR prep package

Optional config fields:
- `usage_connector`: Product usage MCP connector
- `support_connector`: Support MCP connector
- `nps_connector`: NPS/CSAT connector
- `cs_methodology`: Informs recommended next plays (TARO, SuccessCOACHING, etc.)

If required fields are `[PLACEHOLDER]`, prompt:
> "Run `/csm:cold-start-interview` to configure your CSM profile before running
> QBR prep."

---

## Scheduling

The QBR Prep Agent is primarily on-demand. For teams with consistent QBR cycles, it
can be scheduled to run automatically ahead of a known renewal date:

```
5 days before renewal (approximate — requires renewal date from CRM):
  This scheduling pattern requires a separate trigger mechanism that reads
  renewal dates from CRM and fires the agent 5 days before each.
  Contact your Claude implementation team for renewal-triggered scheduling.
```

On-demand invocation: "Run QBR prep for [Account Name]" or
"Prepare me for my QBR with [Account Name] on [date]."

---

## Sample Output (abbreviated narrative section)

```
## QBR Narrative Draft — Meridian Labs
[DRAFT — requires CSM review before use]
QBR date: May 20, 2026 · Review period: Feb 15 – May 13, 2026 · CSM: Priya Sharma

### What we accomplished together

This quarter Meridian Labs achieved their primary goal of getting their data science
team fully operational on the platform. All 42 provisioned users have logged in; the
core analytics workflow the team defined at kickoff is now running daily. Feature
adoption is at 71 — above the mid-market average — which reflects the team's commitment
to the integration we built in March.

The executive sponsor goal of a monthly reporting workflow didn't reach completion this
period. The blocker was the data warehouse integration, which took three weeks longer
than planned due to their IT review cycle. That integration is now live. The monthly
workflow should be achievable in the first six weeks of next quarter.

### What the data shows

Usage is strong: 38 of 42 users active in the last 30 days, with average weekly logins
up 23% from the prior period. Support volume dropped from 7 tickets in February to 2
in April — that trend reflects the team becoming more self-sufficient. The one open
ticket ([#4821]) is a minor display issue, not blocking anything.

NPS: 8 (collected April 29). Up from 6 at kickoff.
[DRAFT — CSM: verify NPS date and confirm score with champion before QBR]
```
