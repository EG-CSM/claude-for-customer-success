---
name: customize
description: >
  Update the CS-Ops plugin configuration — segment definitions, CSM ratios,
  health thresholds, playbook settings, escalation matrix, data quality rules,
  and reporting defaults. Use when onboarding to the plugin for the first time,
  after organizational changes (territory restructure, headcount change, segment
  redefinition), or when audit outputs reveal configuration mismatches. Wraps
  the cold-start-interview configuration into targeted section updates without
  requiring a full re-interview. Distinct from /cs-ops:cold-start-interview
  which is the initial setup flow for a blank configuration.
argument-hint: "[--section <section-name> | --show | --reset <section-name>]"
version: "1.0.0"
config_skill: true
---

# /cs-ops:customize

Update CS-Ops configuration without re-running the full cold-start interview.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`.

If the file is missing: route to `/cs-ops:cold-start-interview` — this skill
updates an existing configuration; it cannot build one from scratch.

If the file exists but contains pervasive `[PLACEHOLDER]` markers (more than 3
unconfigured sections): recommend `/cs-ops:cold-start-interview` as a faster
path to a complete configuration than section-by-section update.

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — No domain guardrails apply — this skill configures the environment rather than generating outputs.
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--show`: Display current configuration — all sections, formatted for review.
Surfaces any remaining `[PLACEHOLDER]` markers. No edits made.

`--section <section-name>`: Update one named configuration section.
Valid section names:

| Section | Controls |
|---------|---------|
| `segments` | Segment definitions, ARR ranges, reclassification thresholds |
| `ratios` | Target CSM-to-account ratios per segment and motion |
| `health` | Health tier thresholds, staleness rules, component weights |
| `playbook` | Configured plays, trigger conditions, outcomes |
| `escalation` | Escalation matrix — severity tiers, response SLAs, owners |
| `data-quality` | Required fields, staleness thresholds, consistency rules |
| `reporting` | Primary performance indicator, reporting cadence, dashboard defaults |
| `team` | CSM roster, motion assignments, ARR thresholds for high-touch triggers |

`--reset <section-name>`: Reset one named section to blank/placeholder state.
Requires explicit confirmation before executing — reset removes configured values.

If no flag is provided:
> "Which section of the CS-Ops configuration do you want to update?"
> Options: Segments · Ratios · Health model · Playbook · Escalation matrix ·
> Data quality · Reporting defaults · Team roster · Show current config

---

## Display current configuration (`--show`)

---

**CS-Ops Plugin Configuration**
*`~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`*
*Retrieved: [timestamp]*

---

### Configuration health

| Section | Status | Issues |
|---------|--------|--------|
| Segments | [✅ Configured / ⚠️ Partial / ❌ Placeholder] | [Issues if any] |
| Ratios | [✅ / ⚠️ / ❌] | |
| Health model | [✅ / ⚠️ / ❌] | |
| Playbook | [✅ / ⚠️ / ❌] | |
| Escalation matrix | [✅ / ⚠️ / ❌] | |
| Data quality | [✅ / ⚠️ / ❌] | |
| Reporting | [✅ / ⚠️ / ❌] | |
| Team | [✅ / ⚠️ / ❌] | |

**Overall configuration completeness:** [N/8 sections fully configured]

[If any sections have ❌ Placeholder status:]
> ⚠️ [N] sections still contain placeholder values. Skills that depend on
> unconfigured sections will prompt for `/cs-ops:cold-start-interview` or
> ask for session-level input. Run `/cs-ops:customize --section <name>` to
> configure each section, or `/cs-ops:cold-start-interview` to complete all
> at once.

---

### Current configuration — full display

[Display all configured values from `../../CLAUDE.md` in readable format,
organized by section. Do not display raw CLAUDE.md markdown — render the
values as human-readable configuration. Replace `[PLACEHOLDER]` markers with
⚠️ PLACEHOLDER — not configured.]

**Segments:**
| Segment | ARR floor | ARR ceiling | Motion | Reclassification threshold |
|---------|----------|------------|--------|--------------------------|
| [Name] | $[floor] | $[ceiling] | [motion] | $[threshold] |

**Target ratios:**
| Segment | Motion | Target accounts/CSM |
|---------|--------|-------------------|
| [Name] | [motion] | [N] |

**Health model:**
| Tier | Score range | Action threshold |
|------|------------|-----------------|
| 🟢 Green | [range] | — |
| 🟡 Yellow | [range] | CTA triggered |
| 🔴 Red | [range] | Immediate CSM action |

*Staleness threshold:* [N] days

**Playbook:** [N plays configured — list names only in --show mode]
*Full play details: use `/cs-ops:playbook-auditor --full`*

**Escalation matrix:**
| Tier | Definition | Response SLA | Owner |
|------|-----------|-------------|-------|
| S1 | [definition] | [SLA] | [owner] |
| S2 | [definition] | [SLA] | [owner] |
| S3 | [definition] | [SLA] | [owner] |

**Data quality:**
*Required fields:* [list] · *Staleness threshold:* [N] days · *Consistency rules:* [N configured]

**Reporting:**
*Primary KPI:* [GRR / NRR / Logo retention] · *Reporting cadence:* [Weekly / Monthly] ·
*Dashboard default:* [--weekly / --monthly / --quarterly]

**Team:** [N CSMs configured — use `/cs-ops:capacity-planner` for full roster view]

---

## Section update workflows

---

### Segments (`--section segments`)

**Current configuration:**

| Segment | ARR floor | ARR ceiling | Motion | Reclassification threshold |
|---------|----------|------------|--------|--------------------------|
| [Existing] | | | | |

Ask one question at a time:

1. Do you want to **add** a new segment, **modify** an existing segment,
   or **remove** a segment?

For **add:**
- Name of new segment?
- ARR floor and ceiling? (e.g., $100K–$500K — enter "No floor" or "No ceiling" for open-ended)
- CS motion for this segment? (High-touch / Hybrid / Tech-touch)
- Reclassification trigger threshold? (ARR amount that moves an account into or out of this segment)
- Target CSM-to-account ratio for this segment?

For **modify:**
- Which segment?
- Which field(s)? (ARR range / motion / reclassification threshold / target ratio)
- New value(s)?

For **remove:**
- Which segment? Warn: removing a segment requires migrating all accounts currently in it.
  Confirm this has been handled before removing the configuration.

**After update:**

Show the updated segments table. Confirm with user before writing to CLAUDE.md.

> "I'll update the segments configuration with these changes. Shall I apply them?"

On confirmation: write to `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`.

> ✅ Segments configuration updated. Note: existing accounts are not automatically
> reclassified. Run `/cs-ops:segment-analyzer --reclassification` to identify
> accounts that should move segments based on the new definitions.

---

### Ratios (`--section ratios`)

**Current configuration:**

| Segment | Motion | Target accounts/CSM |
|---------|--------|-------------------|
| [Existing] | | |

Questions:
1. Which segment's ratio do you want to update?
2. What is the new target accounts-per-CSM for [segment] [motion] CSMs?

Context to request if needed: "What's driving the change? (Headcount change /
industry benchmark update / capacity data showing consistent over/under-loading)"
— this feeds the rationale field in the configuration change log.

After update:

> ✅ Ratio updated: [Segment] target changed from [old] to [new] accounts per CSM.
> Run `/cs-ops:capacity-planner --current` to see current load against the new targets.

---

### Health model (`--section health`)

**Current configuration:**

| Tier | Score range | Staleness threshold |
|------|------------|-------------------|
| 🟢 Green | [range] | [N days] |
| 🟡 Yellow | [range] | [N days] |
| 🔴 Red | [range] | [N days] |

*Component weights (if configured):*
[Component list with weights]

Questions:
1. What do you want to update? (Tier thresholds / Staleness threshold / Component weights)

For **tier thresholds:**
- What score range should define each tier? (Green / Yellow / Red)
- Note: thresholds must be contiguous and cover the full 0–100 range.

For **staleness:**
- How many days before a health score is considered stale?
- Is this threshold the same for all tiers, or does it vary by tier?

For **component weights:**
- What components does your health model use? (e.g., product usage, NPS, support ticket volume, QBR completion)
- What weight should each carry? (must sum to 100%)

After update:

> ✅ Health model configuration updated.
> Note: threshold changes take effect immediately in future skill outputs.
> Historical health data is not retroactively recalculated.
> Run `/cs-ops:health-model-review` to assess whether the new thresholds
> change the health distribution materially.

---

### Playbook (`--section playbook`)

**Current configuration:**

| Play | Trigger | Owner | Motion scope | Last updated |
|------|---------|-------|-------------|-------------|
| [Existing] | | | | |

Operations:
1. What do you want to do? (Add play / Update play / Archive play)

For **add play:**
- Play name?
- Trigger condition (specific and measurable — include threshold and source):
- Steps overview (brief — full TARO structure is in the play itself):
- Outcome definition (observable state at play close):
- CS motion scope (All / High-touch only / Tech-touch only):
- Owner (CSM / CS Lead / Automated):

For **update play:**
- Which play?
- What's changing? (Trigger / Steps / Outcome / Motion scope / Owner)
- New value?
- Reason for change? (This becomes the playbook governance log entry rationale)

Governance note: Every play change creates a record. After writing to CLAUDE.md:

> ✅ Play updated. A governance record has been created:
> **PCR-[YYYY-NNN]: [Play name] — [Change type]**
> Rationale: [User-provided reason]
> Effective: [today's date]
> Review date: [90 days from today]
>
> Archive this record in your playbook governance log. Use
> `/cs-ops:process-doc --playbook-governance` to generate the full governance
> framework if you haven't already.

For **archive play:**

Confirm with two gates:
1. "Archiving [play name] removes it from CSM visibility. Are you sure?"
2. "Has this been approved by the CS lead?" (Require explicit yes before proceeding)

After both confirmations: mark play as archived in config. Create governance record.

---

### Escalation matrix (`--section escalation`)

**Current configuration:**

| Tier | Definition | ARR threshold | Response SLA | Primary owner | Executive | Support |
|------|-----------|-------------|-------------|--------------|-----------|---------|
| S1 | | | | | | |
| S2 | | | | | | |
| S3 | | | | | | |

Questions:
1. Which tier do you want to update? (S1 / S2 / S3 / All)
2. For each tier: Definition / ARR threshold / Response time SLA / Owner assignments

After update:

> ✅ Escalation matrix updated.
> Note: the Escalation SOP document may reference the previous configuration.
> If you have a published `/cs-ops:process-doc --escalation`, update it to
> match the new matrix values.

---

### Data quality (`--section data-quality`)

**Current configuration:**

Required fields: [list]
Staleness threshold: [N days]
Consistency rules: [N configured]

Operations:
1. What do you want to update? (Required fields / Staleness threshold / Consistency rules)

For **required fields:**
- Adding or removing a required field?
- Field name and CRM object?
- Completeness target for this field?
- Owner (who is responsible for keeping this field populated)?

For **staleness:**
- Which field's threshold are you updating?
- New threshold in days?

For **consistency rules:**
- Adding or removing a rule?
- Rule description: Field A value should be consistent with Field B value per [logic].

After update:

> ✅ Data quality configuration updated.
> The next `/cs-ops:data-quality-check` audit will apply the new rules.
> If you have a published Data Quality Standard (from `/cs-ops:process-doc --data-quality`),
> update it to reflect the new configuration.

---

### Reporting (`--section reporting`)

**Current configuration:**

Primary KPI: [GRR / NRR / Logo retention]
Reporting cadence: [Weekly / Monthly]
Dashboard default: [--weekly / --monthly / --quarterly]
ARR threshold for high-touch reporting: $[amount]

Questions:
1. What's changing? (Primary KPI / Default dashboard cadence / ARR threshold)
2. New value?

After update:

> ✅ Reporting configuration updated. Future `/cs-ops:metric-dashboard` runs will
> use the new defaults. The `--weekly / --monthly / --quarterly` flags still
> override the default for individual runs.

---

### Team (`--section team`)

**Current configuration:**

| CSM | Motion | Segment assignment | ARR managed |
|-----|--------|-------------------|------------|
| [Existing] | | | |

Operations:
1. What do you want to update? (Add CSM / Update CSM / Remove CSM)

For **add CSM:**
- Name?
- CS motion (High-touch / Hybrid / Tech-touch)?
- Segment(s) assigned?
- Start date?

For **update CSM:**
- Which CSM?
- What's changing? (Motion / Segment / Name correction)

For **remove CSM:**
- Which CSM? Warning: removing a CSM from the configuration does not
  reassign their accounts. Run `/cs-ops:capacity-planner --departure <name>`
  before removing if accounts are still assigned.

After update:

> ✅ Team configuration updated.
> Run `/cs-ops:capacity-planner --current` to see updated capacity ratios.

---

### Section reset (`--reset <section-name>`)

Resetting a section removes all configured values for that section and replaces
them with `[PLACEHOLDER]` markers. Skills that read the reset section will
prompt for `/cs-ops:cold-start-interview` or request session-level input.

**Confirmation required:**

> "Resetting [section name] will remove all configured values for this section.
> This cannot be undone from within the plugin — you will need to reconfigure
> the section manually.
>
> Type CONFIRM to proceed, or anything else to cancel."

On CONFIRM: write placeholder markers to the section in CLAUDE.md.

> ✅ [Section name] reset to placeholder state.
> Run `/cs-ops:customize --section [section-name]` to reconfigure.

---

## Configuration write protocol

Every configuration change follows this sequence:

1. **Display the proposed change** before writing:
   > "I'll make the following change to `../../CLAUDE.md`:"
   > [Show before/after values]
   > "Confirm? (yes / no)"

2. **Require confirmation** before writing. Never write without explicit user
   confirmation.

3. **Write the change** to `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`.

4. **Confirm the write** with the timestamp and section updated.

5. **Surface downstream impacts** — which skills will behave differently and
   whether any published process documents need updating.

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Configuration source:** `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
> - **Sections modified this session:** [List of sections updated | None]
> - **Sections still at placeholder:** [List | None]
> - **Before treating configuration as complete:** Run `/cs-ops:customize --show`
>   to confirm all sections are fully configured — any remaining placeholders will
>   cause downstream skills to fall back to session-level prompts
> - **After configuration changes:** Skills run in the same session will use
>   the updated configuration immediately; no restart required

---

> [review before sending]

## Guardrails

**Never write without explicit confirmation.** Configuration changes affect every
CS-Ops skill. Show the proposed change, get a yes, then write. No silent updates.

**Validate thresholds for internal consistency.** If health tier thresholds are
updated, confirm they cover the full 0–100 range with no gaps or overlaps before
writing. A gap in the range will cause health assignments to fail silently.

**Segment changes require account migration awareness.** Changing a segment
definition does not automatically move accounts. Surface the reclassification
impact — how many accounts would change segments — before confirming the write.

**Escalation matrix changes must match published SOPs.** If a published
escalation SOP exists, flag that it needs updating. Configuration and documentation
out of sync is worse than having no documentation.

**Playbook archival is not a deletion.** Archived plays remain in the governance
log. They can be reinstated. The distinction matters — do not use "delete" language
when archiving plays.

**Configuration drift is a real risk.** The CLAUDE.md configuration is the
single source of truth for all CS-Ops skills. If it diverges from actual practice
(CSMs added without config update, ratios changed verbally but not written),
skills will produce analysis based on stale assumptions. Encourage quarterly
`/cs-ops:customize --show` reviews.

---

## After configuration update

- "Configuration updated — run a full capacity check: `/cs-ops:capacity-planner --current`"
- "New segments defined — run reclassification queue: `/cs-ops:segment-analyzer --reclassification`"
- "Health thresholds changed — check model against current portfolio: `/cs-ops:health-model-review`"
- "Playbook updated — run full playbook audit with new plays: `/cs-ops:playbook-auditor --full`"
- "Data quality rules updated — run baseline audit against new standard: `/cs-ops:data-quality-check`"
- "Configuration complete — generate metrics dashboard: `/cs-ops:metric-dashboard`"
