# QBR Prep Agent — Deployment & Configuration Guide

## What This Agent Does

The QBR Prep Agent is an on-demand agent that assembles a complete quarterly business
review package for a single account. It pulls data from CRM, product usage, support,
and NPS connectors; assesses goal achievement against configured or CSM-provided success
criteria; and produces a narrative draft and slide outline, both marked for CSM review.

The agent does not run the QBR. It prepares the materials the CSM uses to run it. All
output is a starting point — the CSM adapts language, adds context, and adjusts emphasis
before the meeting.

**Outputs:**
- Achievement analysis: goals scored as achieved, partially achieved, not achieved, or
  evidence unclear, with supporting data from connectors
- Narrative draft: full QBR story from opening framing through renewal context, in the
  CS methodology tone configured for the account's segment
- Slide outline: deck structure matched to the configured template type with content
  guidance per slide — not a finished deck; a structured guide for the CSM
- All output sections carry `[DRAFT — requires CSM review]`

---

## Architecture

```
Orchestrator: QBR Prep Agent
│
├── Subagent 1: Account Data Assembler
│   Pulls account record, stakeholders, product usage, support history, and
│   NPS/CSAT from all configured connectors. CRM is required — halts if
│   unavailable. Other connectors are optional; failures are noted and work
│   continues with null fields. Returns a structured account profile.
│
├── Subagent 2: Achievement Analyzer
│   Receives the account profile and the configured (or CSM-provided) success
│   criteria. Scores each goal against available data. Returns a scored
│   achievement record with supporting evidence and a recommended narrative
│   framing per goal.
│
├── Subagent 3a: Narrative Drafter         ← dispatched simultaneously with 3b
│   Takes the account profile and achievement analysis and writes the full
│   QBR narrative draft. Sections: opening framing, what was accomplished,
│   headwinds, data highlights, look-ahead, and renewal context.
│
└── Subagent 3b: Slide Outline Generator   ← dispatched simultaneously with 3a
    Takes the account profile and achievement analysis and produces a slide-
    by-slide outline matched to the configured template type. Includes content
    guidance and data references per slide. This is a guide, not a commitment.
```

Subagents 3a and 3b run in parallel after Subagent 2 completes. The orchestrator
assembles their outputs into the final package.

---

## Prerequisites

### Required Connectors

| Connector | Role |
|-----------|------|
| CRM (HubSpot, Salesforce, etc.) | Account record, stakeholders, success criteria, renewal date |

### Optional Connectors

| Connector | Role |
|-----------|------|
| Product usage platform | Active users, adoption score, top features used |
| Support platform | Ticket history, P1 count, resolution time |
| NPS / CSAT platform | Sentiment score, trend, most recent response |

Optional connectors are recommended but not required. When unavailable, the affected data
sections are marked as unavailable in the output and the narrative draft notes the gap.

---

## Configuration

The agent reads from:
`~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

Run `/csm:cold-start-interview` to configure this file if it contains `[PLACEHOLDER]`
values.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `crm_connector` | CRM MCP connector name | `hubspot-mcp` |
| `qbr_template_preference` | Default slide template | `executive` |
| `output_path` | Directory for saving the completed package | `~/qbr-packages/` |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `usage_connector` | Product usage connector name | — |
| `support_connector` | Support platform connector name | — |
| `nps_connector` | NPS / CSAT connector name | — |
| `cs_methodology` | Methodology context for narrative tone | none |
| `review_period_days` | Days back from QBR date to define the review window | `90` |

### Template Types

| Template | Slide Count | Best For |
|----------|-------------|---------|
| `executive` | 8–10 slides | C-suite or sponsor audience; strategic framing |
| `operational` | 12–15 slides | Power user or technical champion audience |
| `renewal-focused` | 10–12 slides | Accounts with renewal conversation embedded in the QBR |

The template type controls the slide outline structure. It does not affect the narrative
draft. Set `qbr_template_preference` to the most common type for your book; override
per-invocation using natural language when needed.

---

## Scheduling

### This Agent Is On-Demand Only

The QBR Prep Agent does not run on a schedule. It is invoked per account when the CSM
prepares for a quarterly review.

### Trigger Methods

**Named command:**
```
/csm:qbr-prep-agent <account-name>
```

**Natural language:**
```
Prepare the QBR package for Meridian Labs — the meeting is June 15.
Run QBR prep for Northwave Financial. Use the renewal-focused template.
Get Apex Systems ready for their quarterly review next Thursday.
```

See `steering-examples.json` for the full prompting pattern library.

---

## Success Criteria Handling

The Achievement Analyzer requires success criteria (agreed goals from the prior QBR or
onboarding). The orchestrator looks for them in this order:

1. CRM — the configured success criteria field on the account record
2. CSM prompt — if not in CRM, the orchestrator pauses and asks the CSM to provide them
   before dispatching the Achievement Analyzer

**The orchestrator never proceeds without success criteria.** A QBR without goals
scored against evidence is not a QBR prep package — it is a data summary. If criteria
are not yet in CRM, the CSM must provide them in the invocation or in response to the
pause prompt.

---

## Output Reference

### Achievement Analysis

Each success criterion is scored:

| Symbol | Meaning |
|--------|---------|
| ✓ | Achieved — supporting evidence meets or exceeds the goal |
| ◐ | Partially achieved — evidence shows progress but the goal was not fully met |
| ○ | Not achieved — evidence shows the goal was missed |
| ? | Evidence unclear — data is insufficient to score confidently |

Each scored goal includes: the original goal text, the score, up to three supporting data
points from connectors, and a recommended narrative framing for the CSM to adapt.

### Narrative Sections (fixed order)

| Section | Contents |
|---------|----------|
| Opening framing | Account context, why this QBR matters now, tone setter |
| What was accomplished | Achieved and partially achieved goals with evidence |
| Headwinds | Challenges and not-achieved goals, framed constructively |
| Data highlights | Usage, support, and sentiment highlights for the review period |
| Look-ahead | Proposed goals or priorities for the next quarter |
| Renewal context | Renewal date, ARR, and any relevant renewal signals (present only when renewal date is within 120 days) |

The narrative draft is written in the first person for the CSM ("In the last quarter,
your team..."). The CSM should review every section for accuracy and adjust voice.

### Slide Outline

The slide outline maps narrative content to slides following the configured template type.
Each slide entry includes: slide title, recommended content points (not full prose),
data references the CSM should pull, and any formatting notes.

The outline is a guide. CSMs adapt structure and depth based on the meeting.

### Output Status

Every output section carries `[DRAFT — requires CSM review]`. This label is never
omitted — the agent does not produce finalized materials.

---

## Data Gap Behavior

| Situation | Behavior |
|-----------|----------|
| CRM unavailable | Halt immediately — no package produced; error surfaced to CSM |
| Product usage connector unavailable | Continue; usage sections marked as unavailable in package |
| Support connector unavailable | Continue; support sections marked as unavailable |
| NPS connector unavailable | Continue; sentiment sections marked as unavailable |
| Renewal date not in CRM | Renewal Context section omitted; flag noted in package |
| Success criteria not in CRM | Orchestrator pauses and asks CSM before proceeding |
| Success criteria provided by CSM via prompt | Proceed; note source as "CSM-provided" in achievement analysis |
| No CRM notes in review period | Achievement Analyzer and Narrative Drafter note the gap; continue |
| ARR not in CRM | Package renders without ARR; flag noted |

---

## Customization

### Changing the Review Period

The default review period is 90 days back from the QBR date. Set `review_period_days`
in config to change the default. Override per-invocation by specifying the window in the
prompt: "Prepare the QBR for Apex Systems — review the last 6 months."

### Changing the Template Type

Set `qbr_template_preference` in config for the default. Override per-invocation:
"Run QBR prep for Meridian Labs using the operational template."

### CS Methodology Context

Set `cs_methodology` to the name of the methodology your team follows (e.g., TARO, LAER,
EBR). When set, the Narrative Drafter uses that methodology's language conventions. When
not set, the narrative uses neutral CS language.

### Adding Success Criteria to CRM

The cleanest workflow is to store success criteria directly in a CRM field on the account
record. The orchestrator will find them automatically on the next run. If your CRM does
not have a dedicated field, add the criteria as the most recent tagged note and configure
the CRM connector's criteria lookup to use notes.

---

## Subagent Reference

| Subagent | File | Role |
|----------|------|------|
| Account Data Assembler | `subagents/account-data-assembler.md` | CRM and connector data retrieval |
| Achievement Analyzer | `subagents/achievement-analyzer.md` | Goal scoring and evidence mapping |
| Narrative Drafter | `subagents/narrative-drafter.md` | Full QBR narrative draft |
| Slide Outline Generator | `subagents/slide-outline-generator.md` | Slide-by-slide outline |
