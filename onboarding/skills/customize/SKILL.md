---
name: customize
description: >
  View and update your onboarding plugin configuration — the profile that drives
  milestone targets, TtV benchmarks, success criteria format, escalation contacts,
  graduation criteria, and CS methodology references. Use --view (default) to display
  current configuration with section-by-section status, --update to change specific
  settings by section name, --reset to restore a section to its template defaults, or
  --validate to check the configuration for missing required fields, placeholder values,
  and internal consistency issues before running onboarding skills.
argument-hint: "[--view | --update <section> | --reset <section> | --validate]"
version: "1.0.0"
deployment_target: plugin
config_skill: true
---

<!-- Status: [PROPOSED] -->

# /onboarding:customize

Onboarding profile configuration management.

---

## Pre-flight
- Confirm account context (company name, CSM, current onboarding stage)
- Identify customization goals for this account
- Note any existing onboarding plan or prior session outputs

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Trigger Precision

**Use when:**
- Viewing current onboarding configuration (`--view`)
- Updating a specific configuration section after methodology, team, integration, or escalation matrix changes (`--update <section>`)
- Resetting a configuration section back to placeholder state (`--reset <section>`)
- Validating configuration completeness before running onboarding operations (`--validate`)

**Do NOT use for:**
- Initial configuration setup from scratch (use `/onboarding:cold-start-interview --full`)
- Running onboarding operations — this skill only reads and writes configuration

## Typical Activation
- "Show me my current onboarding config"
- "Update my escalation matrix"
- "Validate my config before I run the onboarding plan"
- CSM runs `/onboarding:customize --view` to display current configuration
- CSM runs `/onboarding:customize --update escalation` to update a specific section
- CSM runs `/onboarding:customize --validate` to check config completeness before running onboarding operations

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of configuration request is this?
   - **View / Status Check**: Read-only — CSM wants current state, completeness indicators, or section-level detail. No writes. Optimize for clarity on what's complete, what's blocking, and what to fix first.
   - **Section Update**: CSM wants to change values within a named section. Requires before/after confirmation, consistency checks against adjacent sections, and immediate-effect warning.
   - **Section Reset**: Destructive operation — restores template defaults, erasing custom values. Verify intent (reset vs. update confusion is common), show current values before executing, require typed confirmation.
   - **Validation / Health Check**: Cross-section audit — placeholder scan, required field presence, and internal consistency. Must map failures to downstream skill impact, not just report PASS/FAIL.
   - **Scope Redirect**: Request targets company-level settings (company name, products, segments) that belong in `company-profile.md`. Redirect to the CS Ops plugin's customize skill for company-level settings (if the `cs-ops` plugin is installed, run `/cs-ops:customize`) — never write company-level values into the onboarding config.

2. **CONSTRAINTS**: What limits the solution space?
   - G1: Config changes take effect immediately — no staging environment. Warn the CSM when a change could alter in-progress account workflows. No write without explicit user confirmation.
   - G2: Section-targeted writes only — updates modify the named section; adjacent sections are preserved exactly as they exist. Read-before-write is mandatory. Never infer or default-fill missing values.
   - G5: TtV values are always labeled `[review — internal planning target]` — these must never appear in customer-facing output.
   - Escalation contact accuracy is the CSM's responsibility — record what they provide, remind them to verify contacts are aware and current.
   - Reset is destructive and cannot be undone without manual re-entry — always offer `--update` as the less destructive alternative first.

3. **EXPERT CHECK**: What would a veteran CS ops practitioner verify first?
   - Does this change create a cross-section consistency conflict? Milestone day changes ripple into TtV targets; model changes ripple into escalation path requirements. Check the cascade before writing.
   - Is the CSM asking to reset when they actually want to update one value? The reset-vs-update confusion accounts for most unintended data loss in config management.
   - Are placeholder sections mapped to the specific downstream skills they block? A generic "section incomplete" message doesn't convey urgency — "graduation missing blocks `/onboarding:handoff-doc`" does.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - ❌ Writing a milestone day target without cross-checking TtV consistency — M4 changes invalidate TtV targets silently.
   - ❌ Executing a reset without first asking whether the CSM wants to fix a specific value or truly restore defaults for the whole section.
   - ❌ Reformatting or rewriting sections not targeted by the current update — adjacent sections must be preserved byte-for-byte.
   - ❌ Reporting validation PASS on sections that are structurally complete but operationally nonsensical (all milestones at the same day target, TtV of 1 day).
   - ❌ Displaying section status without mapping incomplete sections to the specific skills they block.
   - ❌ Writing company-level settings (company name, products, segments) into the onboarding config instead of redirecting to the CS Ops plugin's customize skill (if the `cs-ops` plugin is installed, run `/cs-ops:customize`).

**After execution**, verify:
- Did the output match the classified request type (view/update/reset/validate/redirect)?
- For writes: was before/after shown and confirmation obtained before writing?
- For updates: were cross-section consistency checks run before confirming?
- Confidence: [High] for read operations and structural validation / [Medium] for advice on appropriate values (company-specific) / [Low] for content suggestions (only the CSM knows their org).

## Config file location

This skill reads and writes:

```
~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md
```

The shared company profile at:

```
~/.claude/plugins/config/claude-for-customer-success/company-profile.md
```

is read-only from this skill — changes to company-level settings (company name,
products, segments, primary methodology) are managed through the CS Ops plugin's customize skill (if the `cs-ops` plugin is installed, run `/cs-ops:customize`).

---

## Mode

`--view` (default): Display all configuration sections with current values and
completeness status. Flags sections with `[PLACEHOLDER]` values that will block
skill execution. Use before running onboarding skills to confirm the profile is
complete.

`--update <section>`: Guided update for one named section. Presents current values,
asks what to change, writes the update, and confirms with a before/after comparison.
Available sections: `milestones`, `ttv-targets`, `onboarding-models`, `success-criteria`,
`escalation`, `graduation`, `methodology`, `integrations`.

`--reset <section>`: Restore a named section to its template default values. Replaces
all custom values in that section with the defaults from the cold-start-interview
template. Use when a section has been corrupted or when starting a new role with
different standards. Requires explicit confirmation before writing.

`--validate`: Configuration health check. Scans all sections for `[PLACEHOLDER]`
markers, missing required fields, and internal consistency issues (e.g., M5 day target
earlier than M4; TtV target shorter than M4 day target). Produces a report with
PASS/WARN/FAIL status per section and a prioritized fix list.

---

## `--view` mode

Read `~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`
and present each section's current values with a completeness indicator.

Output format: render each section with a header bar, current values, and a completeness indicator — `[✓ Complete]`, `[⚠ Partial]`, `[✗ Missing]`, or `[— Optional]`. End with a summary count (sections complete / partial / missing) and a prioritized attention list. See `references/skill-impact-map.md` for the full output template and section-by-section field reference.

---

## `--update <section>` mode

### Section: `milestones`

Present current M1–M5 values. Ask:

1. "Which milestone are you updating? (M1 / M2 / M3 / M4 / M5 / all)"
2. For the selected milestone(s), ask:
   - "New day target? (current: Day [X])"
   - "Updated completion criteria? (describe what must be true for this milestone
     to be marked complete)"
   - "Updated at-risk signals? (what observable signals indicate this milestone
     is in danger of being missed?)"

After collecting input, show the before/after:

```
Changes to Milestone Framework:

  M3 First use — before:
    Day target:          Day 21
    Completion criteria: [previous value]
    At-risk signal:      [previous value]

  M3 First use — after:
    Day target:          Day [new value]
    Completion criteria: [new value]
    At-risk signal:      [new value]

Write these changes? (yes / no)
```

If confirmed, write the updated values to the config file.

**Consistency check before writing:** Flag if any of these conditions exist:
- M5 day target ≤ M4 day target
- M4 day target ≤ M3 day target
- M3 day target ≤ M2 day target
- M2 day target ≤ M1 day target
- Any TtV target is shorter than the new M4 day target (TtV can't be shorter
  than the milestone that defines first value)

If a consistency issue is found, present it and ask to confirm before writing.

---

### Section: `ttv-targets`

Present current TtV targets per segment. Remind: these are internal planning
benchmarks only — not commitments to customers.

Ask: "Which segment are you updating? (Enterprise / Mid-Market / SMB / all)"

For each segment, ask: "New TtV target in days? (current: [X] days)"

Minimum check: TtV target must be ≥ M4 day target for that segment's typical
milestone framework. If the entered value is less than M4 day target, flag:

> "⚠ A TtV target of [X] days is shorter than the M4 day target ([Y] days).
> TtV measures time to first value (M4) — a target shorter than M4 is logically
> inconsistent. Recommend: TtV target ≥ M4 day target. Confirm to write anyway?"

Show before/after with `[review — internal planning target]` label on all values.
Write if confirmed.

---

### Section: `onboarding-models`

Present current model configuration. Ask which aspect to update:
- Default model (which model applies when an account isn't explicitly assigned)
- Model assignment rules (e.g., "Enterprise accounts use white-glove")
- Available models (add or remove a model from the active list)

For default model, offer the four options:
- `white-glove` — high-touch, executive-relationship-focused
- `guided-self-serve` — structured but lower-touch CSM involvement
- `implementation-plus-handoff` — includes implementation engineer phase
- `partner-led` — primary delivery through a partner; CSM in oversight role

For model assignment rules, collect: "How do accounts get assigned to a model?
(by segment / by ARR / by product tier / by manual assignment / other)"

Show before/after. Write if confirmed.

---

### Section: `success-criteria`

Present current criteria format and review cadence. Ask:

1. "Criteria format: outcome-based / metric-based / milestone-based? (current: [value])"
2. "When do you formally review success criteria with customers? (e.g., M2, M4, M5)"
3. "Minimum and maximum criteria count per account? (current: [N]–[N])"

If the format changes (e.g., from outcome-based to metric-based), note:
> "Changing criteria format doesn't update existing account criteria — it affects
> how new criteria are structured going forward. Existing accounts keep their current
> criteria format."

Show before/after. Write if confirmed.

---

### Section: `escalation`

Present current escalation matrix. For each tier, ask for the named contact
(name + role + preferred contact method):

1. "CSM self-resolve threshold: days overdue before involving another party?
   (current: [X] days)"
2. "First escalation contact (typically AE or team lead): name, role, how to reach?"
3. "Second escalation contact (manager/director): name, role, how to reach?"
4. "Executive sponsor escalation (white-glove model only): who triggers this, and who
   is contacted?"
5. "Partner escalation path (partner-led model only): partner contact name and role?"

For each contact, if the user enters a name, ask: "Is this person's contact info
(email/Slack/phone) in your CRM, or do you want to add it here for quick reference?"

Show before/after. Flag any tier that remains `[PLACEHOLDER]` after the update.
Write if confirmed.

---

### Section: `graduation`

Present current graduation criteria. Ask:

"What conditions must be met before you consider an account graduated from onboarding?
List each condition — I'll format them into the checklist the `/onboarding:handoff-doc` skill uses."

Prompt for at least these graduation gates (can be customized):
- M5 milestone complete
- Success criteria confirmed (written or verbal acknowledgment from customer)
- User provisioning complete (all required users logged in at least once)
- Active integrations validated
- Customer post-onboarding contact named
- Open items documented with transferred ownership
- Receiving team introduced (or introduction scheduled)

For white-glove accounts, also ask: "Executive sponsor updated?"
For implementation-plus-handoff: "Implementation handoff complete?"
For partner-led: "Partner alignment confirmed?"

Show the drafted graduation checklist before writing. Write if confirmed.

---

### Section: `methodology`

Present current CS methodology setting. Ask:

1. "Primary CS methodology? (TARO / SuccessCOACHING / Custom — current: [value])"
2. If TARO or SuccessCOACHING: "Which plays from your methodology are most relevant
   to the onboarding workflow? (These are referenced in the recommended-plays section
   of the handoff document.)"
3. If Custom: "What is your methodology called, and where is it documented?"

Show before/after. Write if confirmed.

---

### Section: `integrations`

Present current integration configuration. Ask for each:

1. "CRM connector: Salesforce / HubSpot / None / Other? (current: [value])"
2. "PM connector: Asana / Linear / Jira / Monday / None? (current: [value])"
3. "Document storage: Notion / Google Drive / Confluence / None? (current: [value])"

For each connector that is configured, note:
> "Integration presence is noted in your config. Actual connector availability
> depends on your Claude plugins setup — this setting tells onboarding skills
> whether to attempt connector pulls. If a connector is listed here but not
> installed, skills will fall back to manual input mode."

Show before/after. Write if confirmed.

---

## `--reset <section>` mode

Restores one section to the template defaults from the cold-start-interview template.
This erases all custom values in that section.

Before proceeding:

```
⚠ You are about to reset [section] to template defaults.

Current values will be replaced with:
[Show the template default values for that section]

This cannot be undone without manually re-entering your custom values.
Type 'reset [section]' to confirm, or press Enter to cancel.
```

If confirmed, write the template defaults to that section and show confirmation:

```
[section] has been reset to defaults.
Current values: [show the defaults now in the config]

Run /onboarding:customize --update [section] to reconfigure.
```

**Reset-safe sections only:** All 8 sections support reset. However, for the
`escalation` section, flag that resetting removes all named contacts:
> "Resetting escalation will remove all named escalation contacts. The
> `/onboarding:blocker-review` skill will fall back to generic escalation path descriptions
> until you reconfigure contacts."

---

## `--validate` mode

Perform a configuration health check. Read the full onboarding config and run these
checks:

### Placeholder scan

For each section, scan for any `[PLACEHOLDER]` markers. Each occurrence is a FAIL.

### Required field presence and consistency checks

See `references/skill-impact-map.md` for the complete required fields per section, internal consistency rules, and downstream skill impact map — which skills read each configuration section and what behavior changes when values are updated.

Missing required fields = FAIL. Consistency violations = WARN (skill will still run but may produce unexpected results).

### Output format

```
Configuration Validation Report
Generated: [today]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Placeholder Scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  milestones:       ✓ No placeholders
  ttv-targets:      ✓ No placeholders
  onboarding-models: ✓ No placeholders
  success-criteria: ✓ No placeholders
  escalation:       ✗ 2 placeholders found
                      · AE escalation contact: [PLACEHOLDER]
                      · Manager escalation contact: [PLACEHOLDER]
  graduation:       ✗ Entire section is [PLACEHOLDER]
  methodology:      ✓ No placeholders
  integrations:     ✓ No placeholders

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required Field Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  milestones:        ✓ All required fields present
  ttv-targets:       ✓ All required fields present
  onboarding-models: ✓ All required fields present
  success-criteria:  ✓ All required fields present
  escalation:        ⚠ First escalation contact missing name
  graduation:        ✗ Section absent — 0 criteria configured
  methodology:       ✓ All required fields present
  integrations:      ✓ All required fields present

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Consistency Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Milestone day order (M1<M2<M3<M4<M5): ✓ Pass
  TtV targets ≥ M4 day target:           ✓ Pass
  Graduation references M5:              ✗ Cannot check — graduation missing
  White-glove escalation path:           ✓ Present
  Partner-led escalation path:           — Not applicable (no partner model)
  Connector names recognized:            ✓ Pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  FAIL:  2 sections — escalation, graduation
  WARN:  0 sections
  PASS:  6 sections

  Skills blocked by current config:
  · /onboarding:handoff-doc (--readiness, --draft): graduation section missing
  · /onboarding:blocker-review (--escalate): escalation contacts incomplete

  Recommended fix order:
  1. /onboarding:customize --update graduation   [blocks /onboarding:handoff-doc]
  2. /onboarding:customize --update escalation   [blocks blocker-review]
```

---

## Write safety

Before writing any change to the config file:

1. **Read-before-write**: Read the current config file in full before writing
   any update — never overwrite without loading the current state first.

2. **Section-targeted writes**: Updates modify only the named section. Adjacent
   sections are preserved exactly as they exist. Never reformat or rewrite sections
   not being updated.

3. **Backup offer (for reset only)**: Before a `--reset`, offer to show the current
   values in full so the user can copy them if needed:
   > "Before resetting, do you want to see the full current values for [section]
   > so you can save them? (yes / no)"

4. **No writes without confirmation**: Every update mode shows a before/after
   and asks for confirmation before writing. `--view` and `--validate` are
   always read-only.

## Reference Files

- `references/reasoning-blueprint.md` — reasoning framework for this skill
- `references/skill-impact-map.md` — output template, section-by-section field reference, required fields per section, internal consistency rules, and downstream skill impact map

---

## Security & Permissions

This skill reads and writes configuration files at `~/.claude/plugins/config/claude-for-customer-success/`.
No other filesystem paths are written. No subprocess execution, no dynamic code execution.
All data access is through explicitly connected MCP connectors; no outbound network calls are made directly.

## Trust & Verification

Configuration changes made by this skill take effect immediately across all onboarding skills that read config on invocation.
The `--validate` mode performs read-only checks and never modifies configuration.
The `--reset` mode restores placeholder values — CSM must confirm before reset is applied.
CSM review is required before treating any config change as final.

---

## Guardrails

**This skill manages onboarding config only.** Company-level settings (company
name, products, segments, primary CS methodology) live in `company-profile.md`
and are modified through the CS Ops plugin's customize skill. If the user tries to change a
company-level setting here, redirect:
> "Company profile settings are shared across all plugins and managed through
> the CS Ops plugin's customize skill (if the `cs-ops` plugin is installed, run
> `/cs-ops:customize`). I can update the onboarding-specific portion, but company
> name, product catalog, and segment definitions should be changed there."

**TtV values are always labeled.** When displaying TtV target values in any mode,
always include `[review — internal planning target]` after TtV section headings and
values. These values must never appear in customer-facing output, and the label is
the persistent reminder.

**Escalation contact accuracy is a CSM responsibility.** This skill records
what the CSM provides — it cannot verify that named contacts are correct, current, or
willing to accept escalations. After updating escalation contacts, include:
> "Contact details recorded. Verify with each named contact that they're aware
> of and aligned to this escalation path — an escalation to an unaware contact
> creates delays at the worst possible moment."

**`--reset` is destructive.** Template defaults are functional starting points,
not the CSM's tailored configuration. After a reset, the section will function
with generic values — the CSM must re-enter their custom settings using `--update`
to restore full skill accuracy.

**Validate after major updates.** After updating milestones, TtV targets, or
graduation criteria, run `--validate` to confirm internal consistency. Day-target
changes to M4 ripple into TtV assessments; graduation changes affect handoff
readiness checks. Validation catches cross-section conflicts that section-level
updates cannot.

**Config changes take effect immediately.** There is no staging environment — once
written, skills read the new values on their next invocation. If a change produces
unexpected behavior, use `--reset` for that section or `--update` to correct the
specific field.
