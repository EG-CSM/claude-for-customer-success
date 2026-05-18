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
version: "1.1.0"
deployment_target: plugin
config_skill: true
---

# /cs-ops:customize

Update CS-Ops configuration without re-running the full cold-start interview.

[PROPOSED]

---

## Use when

- Onboarding to the plugin for the first time (filling placeholder sections)
- After organizational changes — territory restructure, headcount shift, segment redefinition
- An audit skill (`data-quality-check`, `health-model-review`, `segment-analyzer`,
  `playbook-auditor`) has flagged a configuration mismatch and the root cause is in config
- Confirming or reviewing current configuration state before running dependent skills

## Do NOT use for

- Initial blank-slate setup (use `/cs-ops:cold-start-interview`)
- Running audits or analysis (use the relevant audit skill)
- Reclassifying accounts after segment changes (use `/cs-ops:segment-analyzer --reclassification`)

## Typical activation

- `/cs-ops:customize --show` — review current configuration across all sections
- `/cs-ops:customize --section segments` — update segment ARR definitions
- `/cs-ops:customize --section escalation` — update severity tiers and owner assignments
- `/cs-ops:customize --section team` — add, update, or remove a CSM from the roster
- `/cs-ops:customize --reset <section-name>` — wipe a section back to placeholder state

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

Before generating output, apply these primers:

1. **CLASSIFY**: What type of configuration request is this?
   - **Single-Section Update**: User knows which section to change and has values ready. Guided update with confirmation.
   - **Multi-Section Cascade**: Structural change (territory restructure, headcount shift, segment redefinition) requiring coordinated updates across 2+ sections.
   - **Audit-Triggered Remediation**: User arrives from an audit skill output — trace root cause before fixing.
   - **Cold-Start Completion**: Configuration exists but has multiple placeholder sections. User wants to fill gaps without re-running cold-start-interview.
   - **Configuration Review (--show)**: Read-only inspection of current state, health assessment, and completeness check.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: Health tier thresholds must cover the full 0–100 range with no gaps or overlaps — validate arithmetic before confirming any health model write.
   - G2: Segment changes do not automatically reclassify accounts — surface the migration impact before confirming the write.
   - G4: Escalation matrix changes must be checked against published SOPs — config and documentation out of sync is worse than no documentation.
   - G5: Playbook archival requires explicit CS lead approval confirmation before proceeding — governance is non-optional.
   - G7: Never write without showing the before/after diff and receiving explicit user confirmation — no silent updates, even for "obvious" changes.

3. **EXPERT CHECK**: What would an experienced CS-Ops administrator verify first?
   - Does this change cascade to other sections? A segment change touches ratios, team assignments, health thresholds, and possibly playbook triggers — map the full cascade before the first write.
   - Is the user fixing a symptom or a root cause? If they arrived from an audit output, trace the finding back to the specific config value before proposing a change.
   - Has the configuration drifted from actual practice? If `--show` hasn't been run recently, current values may not reflect reality — ground the conversation in current state first.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Writing a segment update without creating or updating the matching ratio entry and team assignment — creates cross-section orphans.
   - Filling placeholder sections with industry-average defaults instead of running the guided interview questions to get user-specific values.
   - Batching multiple changes into a single confirmation prompt — each proposed change gets its own show-and-confirm cycle.
   - Updating one section of a multi-section cascade without mapping downstream sections.
   - Proposing a config fix for an audit finding without asking "what changed in your org that caused this?"
   - Accepting a `--reset` without the two-gate confirmation sequence — resets are destructive and not easily reversible.

**After execution**, verify:
- Is the configuration internally consistent across all sections that reference the changed values?
- Were all downstream impacts surfaced — which skills will behave differently, which documents need updating?
- Did every write follow the show-diff / confirm / write / confirm-write sequence?
- Confidence: [High] if isolated single-section change / [Medium] if cascade mapped and all affected sections updated / [Low] if cascade may have missed downstream references.

---

## Mode

`--show`: Display current configuration — all sections, formatted for review.
Surfaces any remaining `[PLACEHOLDER]` markers. No edits made.

Read `reference/cs-ops-show-template.md` and populate it from the values in
`~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`.
Render as human-readable configuration — do not display raw CLAUDE.md markdown.

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

## Section update workflows

### Segments (`--section segments`)

Display current segments table from config. Ask one question at a time:

1. Add a new segment, modify an existing segment, or remove a segment?

For **add:** Name · ARR floor and ceiling · CS motion (High-touch / Hybrid / Tech-touch) · Reclassification trigger threshold · Target CSM-to-account ratio

For **modify:** Which segment? · Which field(s)? (ARR range / motion / reclassification threshold / target ratio) · New value(s)?

For **remove:** Which segment? Warn: removing requires migrating all accounts currently in it. Confirm migration handled before removing config.

After update: show updated segments table, confirm before writing.

> ✅ Segments updated. Note: existing accounts are not automatically reclassified.
> Run `/cs-ops:segment-analyzer --reclassification` to identify accounts that
> should move based on the new definitions.

---

### Ratios (`--section ratios`)

Display current ratios table from config.

Questions: Which segment's ratio? · New target accounts-per-CSM? · What's driving the change? (feeds the rationale field in the configuration change log)

After update:
> ✅ Ratio updated: [Segment] changed from [old] to [new] accounts per CSM.
> Run `/cs-ops:capacity-planner --current` to see load against the new targets.

---

### Health model (`--section health`)

Display current health model (tier thresholds, staleness, component weights) from config.

Questions: What to update? (Tier thresholds / Staleness threshold / Component weights)

For **tier thresholds:** New score range for each tier (Green / Yellow / Red). Must be contiguous and cover full 0–100 range.

For **staleness:** Days before health score is considered stale. Same threshold for all tiers or varies?

For **component weights:** Components (e.g., product usage, NPS, support ticket volume, QBR completion) · Weight for each (must sum to 100%).

After update:
> ✅ Health model updated. Threshold changes take effect immediately in future skill
> outputs. Historical health data is not retroactively recalculated.
> Run `/cs-ops:health-model-review` to assess whether new thresholds change the
> health distribution materially.

---

### Playbook (`--section playbook`)

Display current play list from config.

Operations: Add play / Update play / Archive play

For **add play:** Name · Trigger condition (specific and measurable — include threshold and source) · Steps overview (brief) · Outcome definition (observable state at close) · CS motion scope · Owner

For **update play:** Which play? · What's changing? · New value? · Reason for change? (becomes governance log entry rationale)

Governance note: every play change creates a governance record. After writing:
> ✅ Play updated. Governance record created:
> **PCR-[YYYY-NNN]: [Play name] — [Change type]**
> Rationale: [user-provided reason] · Effective: [today] · Review date: [90 days]
>
> Archive this record in your playbook governance log. Use
> `/cs-ops:process-doc --playbook-governance` to generate the full governance
> framework if you haven't already.

For **archive play:** Two confirmation gates:
1. "Archiving [play name] removes it from CSM visibility. Are you sure?"
2. "Has this been approved by the CS lead?" (Require explicit yes before proceeding)

After both confirmations: mark play archived in config, create governance record.

---

### Escalation matrix (`--section escalation`)

Display current escalation matrix from config.

Questions: Which tier to update? (S1 / S2 / S3 / All) · For each tier: Definition / ARR threshold / Response time SLA / Owner assignments

After update:
> ✅ Escalation matrix updated.
> If you have a published `/cs-ops:process-doc --escalation`, update it to
> match the new matrix values.

---

### Data quality (`--section data-quality`)

Display current data quality configuration from config.

Operations: Required fields / Staleness threshold / Consistency rules

For **required fields:** Adding or removing? · Field name and CRM object · Completeness target · Owner

For **staleness:** Which field? · New threshold in days?

For **consistency rules:** Adding or removing? · Rule description: Field A should be consistent with Field B per [logic].

After update:
> ✅ Data quality configuration updated.
> The next `/cs-ops:data-quality-check` audit will apply the new rules.
> If you have a published Data Quality Standard (from `/cs-ops:process-doc --data-quality`),
> update it to reflect the new configuration.

---

### Reporting (`--section reporting`)

Display current reporting configuration from config.

Questions: What's changing? (Primary KPI / Default dashboard cadence / ARR threshold) · New value?

After update:
> ✅ Reporting configuration updated. Future `/cs-ops:metric-dashboard` runs will
> use the new defaults. Mode flags still override the default for individual runs.

---

### Team (`--section team`)

Display current CSM roster table from config.

Operations: Add CSM / Update CSM / Remove CSM

For **add CSM:** Name · CS motion (High-touch / Hybrid / Tech-touch) · Segment(s) assigned · Start date

For **update CSM:** Which CSM? · What's changing? (Motion / Segment / Name correction)

For **remove CSM:** Which CSM? Warning: removing a CSM does not reassign their accounts. Run `/cs-ops:capacity-planner --departure <name>` before removing if accounts are still assigned.

After update:
> ✅ Team configuration updated.
> Run `/cs-ops:capacity-planner --current` to see updated capacity ratios.

---

### Section reset (`--reset <section-name>`)

Resetting a section removes all configured values and replaces them with `[PLACEHOLDER]`
markers. Skills that read the reset section will prompt for `/cs-ops:cold-start-interview`
or request session-level input.

**Confirmation required:**
> "Resetting [section name] will remove all configured values for this section.
> This cannot be undone from within the plugin — you will need to reconfigure manually.
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

2. **Require confirmation** before writing. Never write without explicit user confirmation.

3. **Write the change** to `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`.

4. **Confirm the write** with timestamp and section updated.

5. **Surface downstream impacts** — which skills will behave differently and whether any published process documents need updating.

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

## Guardrails

**Never write without explicit confirmation.** Configuration changes affect every
CS-Ops skill. Show the proposed change, get a yes, then write. No silent updates.

**Validate thresholds for internal consistency.** If health tier thresholds are
updated, confirm they cover the full 0–100 range with no gaps or overlaps before
writing. A gap will cause health assignments to fail silently.

**Segment changes require account migration awareness.** Changing a segment
definition does not automatically move accounts. Surface the reclassification
impact before confirming the write.

**Escalation matrix changes must match published SOPs.** If a published
escalation SOP exists, flag that it needs updating. Configuration and documentation
out of sync is worse than no documentation.

**Playbook archival is not a deletion.** Archived plays remain in the governance
log. They can be reinstated. Do not use "delete" language when archiving plays.

**Configuration drift is a real risk.** The CLAUDE.md configuration is the single
source of truth for all CS-Ops skills. Encourage quarterly `/cs-ops:customize --show`
reviews to catch drift before it affects skill outputs.

---

## After configuration update

- "Configuration updated — run a full capacity check: `/cs-ops:capacity-planner --current`"
- "New segments defined — run reclassification queue: `/cs-ops:segment-analyzer --reclassification`"
- "Health thresholds changed — check model against current portfolio: `/cs-ops:health-model-review`"
- "Playbook updated — run full playbook audit with new plays: `/cs-ops:playbook-auditor --full`"
- "Data quality rules updated — run baseline audit against new standard: `/cs-ops:data-quality-check`"
- "Configuration complete — generate metrics dashboard: `/cs-ops:metric-dashboard`"
