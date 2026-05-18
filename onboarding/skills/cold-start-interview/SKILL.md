---
name: cold-start-interview
description: >
  First-time setup for your onboarding practice profile — collects your role,
  onboarding model, segment configuration, TtV targets, milestone definitions,
  success criteria model, kickoff and handoff format, escalation matrix,
  integrations, and CS methodology preferences. Writes everything to your
  onboarding CLAUDE.md so all other onboarding skills have the context they
  need to run. Run once at setup; use /onboarding:customize for targeted
  updates afterward. Use --quick for a 15-minute abbreviated setup that writes
  the minimum fields required for most skills to function.
argument-hint: "[--full | --quick | --redo | --check-integrations | --redo-company-profile | --section <name>]"
version: "1.0.0"
deployment_target: plugin
config_skill: true
---

# /onboarding:cold-start-interview

First-time configuration for your onboarding practice profile.

---

## When to Run This

Run `/onboarding:cold-start-interview` when:
- You are setting up the onboarding plugin for the first time
- Your company's onboarding model, segments, or targets have changed significantly
- More than half the fields in your onboarding CLAUDE.md contain `[PLACEHOLDER]` markers

For targeted updates to a single section, use `/onboarding:customize --section <name>` instead.

---

## Pre-flight

Before starting the interview, check whether a shared company profile already exists:

`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If the company profile exists:
> "I found your company profile — skipping Section 1. The company name, brand name,
> and product name are already configured. Starting at Section 2."

If the company profile does not exist, run Section 1 as normal.

---

## Trigger Precision

**Use when:**
- Setting up the onboarding plugin for the first time (no config file exists)
- Updating a specific configuration section after your methodology, team structure, or integrations change
- Re-running the full interview because the existing config is stale or substantially wrong
- Checking which integrations are detected and confirming connector availability

**Do NOT use for:**
- Viewing current configuration (use `/onboarding:customize --view`)
- Making targeted edits to an existing config section (use `/onboarding:customize --update <section>`)
- Running onboarding operations — this skill only generates configuration

**Typical activation:**
- "Set up my onboarding config"
- "I need to run the cold start interview"
- "My config is outdated — redo it"
- `/onboarding:cold-start-interview --full`
- `/onboarding:cold-start-interview --section milestones`

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of cold-start interview request is this?
   - **First-Time Full Setup**: No existing config. Running `--full` or default. Optimize for question sequencing and internal consistency validation across all 9 sections.
   - **Quick-Start Minimum Viable**: `--quick` flag. Collect 9 abbreviated questions, write placeholders for the rest, and produce an accurate unlock/blocked skill report.
   - **Reconfiguration / Redo**: `--redo` or `--section` against existing config. Display current values before asking, flag cross-section dependencies that the change may invalidate.
   - **Integration Health Check**: `--check-integrations` only. Test data accessibility (not just auth), update status fields, touch nothing else in the config.
   - **Company Profile Redo**: `--redo-company-profile`. Scoped to Section 1 only. Shared file across practice areas — changes propagate to renewals and other configs.

2. **CONSTRAINTS**: What limits the solution space?
   - G1 (No write without confirmation): Always display the full proposed configuration and require explicit "yes" before writing to any config file.
   - G2 (Never speculate field values): Do not suggest or infer values for fields the user has not provided — a silently incorrect config value is worse than a `[PLACEHOLDER]`.
   - G4 (Preserve untouched sections): When `--section` is used, write only to the target section. Verify file structure supports section-level isolation before writing.
   - G5 (Company profile boundary): `company-profile.md` is shared across practice areas. Never overwrite it during standard `--redo` — only `--redo-company-profile` touches it.
   - G7 (Escalation defaults require review): If user accepts all escalation defaults without named contacts, flag that blocker-review and milestone-tracker will produce unusable escalation output.

3. **EXPERT CHECK**: What would a veteran onboarding leader verify first?
   - Does the selected onboarding model match the user's described behaviors? "White-glove" with 50+ accounts or "guided-self-serve" with dedicated implementation engineers signals a mismatch — surface it before writing.
   - Are TtV targets, milestone day targets, and graduation criteria internally consistent? A TtV target of "21 days" with M4 (First value) at Day 30 is a misalignment worth flagging.
   - After any `--section` update, do adjacent sections still hold? Changing model from white-glove to guided-self-serve may invalidate milestone targets, kickoff format, and escalation SLAs.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Batching multiple questions in a single interaction instead of asking one at a time — prevents adaptive sequencing where earlier answers change what to ask next.
   - Reporting a skill as "unlocked" in the `--quick` summary without verifying the exact field-to-skill dependency — inaccurate unlock reports erode trust.
   - Accepting all defaults without flagging that default escalation contacts are role labels, not named people — downstream skills will produce generic, unusable escalation paths.
   - Overwriting an existing config without `--redo` flag and without explicit overwrite confirmation — silent data loss.
   - Updating one section during `--redo` without listing adjacent sections that may need review given the change — orphaned dependencies.
   - Testing integration connectivity (auth handshake) without verifying data accessibility (can actually pull account records, task lists, etc.).

**After execution**, verify:
- Does the written config accurately reflect every answer the user provided, with no inferred or default-substituted values they didn't confirm?
- Are all `[PLACEHOLDER]` fields traceable to the specific skills they block, and is the unlock/blocked report accurate?
- Is the config file structurally valid for section-level updates by `/onboarding:customize`?
- Confidence: [High] if user confirmed final summary and all sections completed / [Medium] if `--quick` with placeholders remaining / [Low] if `--section` update without cross-section dependency review — state which.

## Flags

`--full` (default): Run all 9 sections in order. Writes a complete configuration.

`--quick`: Collect the minimum fields required for most onboarding skills to run.
Ask 9 abbreviated questions; write remaining fields as `[PLACEHOLDER]`. At the end,
tell the user which skills are unlocked vs. still blocked, and how to complete the
remaining sections with `--redo`.

`--redo`: Re-run the full interview against an existing config. Displays current values
before asking for updates. Used when a major onboarding motion change requires
reconfiguring the full profile.

`--redo-company-profile`: Re-run only Section 1 (company identity). Use when the
company was acquired, rebranded, or the product name changed.

`--check-integrations`: Skip the interview and run only the live connectivity check
for configured integrations. Updates status fields in CLAUDE.md without changing
any other content. Use for periodic health checks or when re-connecting a tool.

`--section <name>`: Run a single section only. Valid section names:
`company`, `model`, `segments`, `milestones`, `success-criteria`, `kickoff`,
`escalation`, `integrations`, `methodology`

---

## Interview Sections

Work through each section in order. For each field, if `--redo` is active, display
the current value before asking for the new value. Accept Enter to keep the current
value unchanged.

Do not ask all fields at once — one question per interaction, in sequence.
After completing each section, confirm before writing and before moving to the next.

---

### Section 1 — Company identity

*Skip if company-profile.md already exists.*

1. **Company name** — Legal or trading name of your company.
2. **Brand name** — Customer-facing brand if different from legal name.
3. **Product name** — Primary product name used in customer communications.

Write to: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

---

### Section 2 — Role and onboarding model

4. **Your role** — Your title (e.g., Onboarding Manager, CSM, Implementation Specialist,
   Customer Success Engineer).
5. **Onboarding team structure** — Do you own accounts solo, or work with a technical
   counterpart? (e.g., "CSM + Implementation Engineer pairs" / "Solo CSM" /
   "Dedicated onboarding team")
6. **Onboarding model** — Which model best describes your motion?
   - `white-glove` — High-touch, largely managed by your team
   - `guided-self-serve` — Customer-led with structured touchpoints
   - `implementation-plus-handoff` — Technical implementation phase, then CSM handoff
   - `partner-led` — Partner or SI owns delivery, you own oversight
7. **Segments you own** — Which customer segments does your onboarding practice serve?
   (e.g., SMB / Mid-Market / Enterprise — or "all")
8. **Who defines success criteria** — You, the customer, or jointly? At which point in
   the onboarding process?

---

### Section 3 — Duration and TtV targets

9. **Average onboarding duration by segment** — Typical calendar days from kickoff to
   handoff-ready, per segment. (e.g., "SMB: 30 days, Mid-Market: 45 days, Enterprise: 90 days")
10. **Time-to-value target** — The milestone at which you consider the customer to have
    achieved initial value. (e.g., "First meaningful output from the product within 21 days")
11. **First milestone target** — How many days from contract sign to kickoff complete?
    (Populates the M1 deadline in milestone-tracker.)
12. **TtV measurement method** — How do you measure whether TtV was achieved?
    (e.g., specific feature activated / outcome metric / customer confirmation)

---

### Section 4 — Milestone definitions

The plugin ships with a default milestone framework:
M1 Kickoff complete (Day 5) → M2 Technical setup (Day 14) → M3 First use (Day 21) →
M4 First value (Day 30) → M5 Handoff ready (Day 60)

For each milestone, confirm or customize:

13. **M1 — Kickoff complete** — Day target and at-risk signals.
    Default: Day 5 / at-risk: no exec attendance, no agenda returned.
14. **M2 — Technical setup** — Day target and at-risk signals.
    Default: Day 14 / at-risk: integration blocked, IT access not granted.
15. **M3 — First use** — Day target and at-risk signals.
    Default: Day 21 / at-risk: no logins, feature not activated.
16. **M4 — First value** — Day target and at-risk signals.
    Default: Day 30 / at-risk: outcome metric not moving.
17. **M5 — Handoff ready** — Day target and at-risk signals.
    Default: Day 60 / at-risk: graduation criteria not met.

If defaults are acceptable as-is, accept all with a single "keep defaults" response.

---

### Section 5 — Success criteria model

18. **Success criteria template** — Do you use a standard template for success criteria
    docs? Where is it stored, or paste the structure here.
19. **Primary value metric by segment** — The one metric that most reliably indicates a
    customer is getting value, per segment. (e.g., "SMB: weekly active users > 5 /
    Enterprise: integration processing > 100 records/day")
20. **Success criteria review cadence** — How often do you review success criteria with
    the customer during onboarding? (e.g., "At M2, M4, and handoff")
21. **Handover to CSM** — What success criteria state is required before handoff?
    (Ties to graduation criteria in Section 6.)

---

### Section 6 — Kickoff and handoff format

22. **Kickoff format** — How is your kickoff typically structured?
    (e.g., "60-min video call / async loom + written agenda / in-person for Enterprise")
23. **Required kickoff attendees** — Who must attend from the customer side?
    (e.g., "Executive sponsor + technical lead + primary user")
24. **Graduation criteria** — What must be true before an account can move from
    onboarding to CS ownership? List each criterion. (e.g., "M4 achieved, success
    criteria agreed, primary user confirmed, support contact trained")
25. **Handoff format** — How do you hand off to the CSM?
    (e.g., "Written handoff doc + 30-min handoff call / async handoff doc only")

---

### Section 7 — Escalation matrix

For each situation, collect: who to escalate to, contact method, and SLA.

26. **M1 missed** — (Default: Onboarding lead / Head of CS — Slack — 24h)
27. **Technical blocker > 5 days** — (Default: SE / Product — Shared Slack — 48h)
28. **Executive sponsor unresponsive** — (Default: AE / Head of CS — Email + Slack — 48h)
29. **SLA breach risk** — (Default: Head of CS / Head of Onboarding — Slack — Same day)
30. **Customer wants to cancel** — (Default: Head of CS + AE — Email + meeting — Same day)

If defaults are acceptable as-is, confirm with "keep defaults."

---

### Section 8 — Integrations

Check which tools are connected and test live connectivity.

**Project management:**
31. Which PM tool do you use? (Asana / Linear / Jira / Monday / None)
32. Is it connected? (Test connection if MCP tool available.)

**CRM:**
33. Which CRM? (Salesforce / HubSpot / Other / None)
34. Connected? (Test connection if available.)

**Document storage:**
35. Which document platform? (Google Drive / SharePoint / Box / None)
36. Connected?

**CS Platform:**
37. Which CS Platform? (Gainsight / Totango / ChurnZero / Vitally / Planhat / None)
38. Connected?

For each connected tool, confirm what data the onboarding skills can pull:
- PM: task lists, milestone status, open blockers
- CRM: account record, contract start date, segment, AE/CSM owner
- Document storage: kickoff decks, success criteria docs, handoff documents
- CS Platform: health scores, activity data, milestone tracking (if configured there)

---

### Section 9 — CS methodology and communication style

39. **CS methodology** — Do you follow a structured framework?
    (TARO / SuccessCOACHING / Gainsight CTAs / Custom / None)
    If TARO: Where are your play definitions stored?
40. **Playbook location** — Where do your onboarding playbooks live?
    (URL or path — used by blocker-review and milestone-tracker to reference plays)
41. **Customer-facing plan format** — What format do customers receive their onboarding plan in?
    (Google Doc / Notion / PDF / Shared project tracker / Email)
42. **Internal status format** — How do you report onboarding status internally?
    (Weekly email / Slack update / CRM field / Dashboard)
43. **Communication style** — Your default style in customer-facing onboarding communication:
    `consultative` / `direct` / `structured-agenda` / `async-first`
44. **Escalation communication style** — When escalating internally, do you prefer
    structured brief or narrative update?

---

## After-Sections Review and Write

After completing all sections (or the minimum for `--quick`), display a structured
summary of what will be written:

> "Here's your onboarding practice profile — review before I write it:
>
> **Role & model:** [role] · [model] · Segments: [list]
> **Duration & TtV:** [by segment] · TtV target: [target]
> **Milestones:** M1 Day [N] → M2 Day [N] → M3 Day [N] → M4 Day [N] → M5 Day [N]
> **Success criteria:** [who defines] · Metric: [metric] · Review: [cadence]
> **Kickoff:** [format] · Required attendees: [list]
> **Graduation criteria:** [list]
> **Handoff:** [format]
> **Escalation matrix:** [5 rows]
> **Integrations:** [connected / not connected per tool]
> **Methodology:** [framework] · Playbooks: [location]
> **Communication:** [style] · Internal: [format]
>
> Write this configuration? (yes / no / edit [section name])"

If the user selects "edit [section name]", return to that section and re-collect.
If "no", discard all changes and confirm nothing was written.
If "yes", proceed to write.

---

## Configuration Write Protocol

Write the completed profile to:
`~/.claude/plugins/config/claude-for-customer-success/onboarding/CLAUDE.md`

If the file already exists and `--redo` was not specified:
> "A configuration file already exists. Writing will overwrite the current profile.
> Confirm to overwrite, or run `/onboarding:customize --section <name>` to update
> a specific section only. Overwrite? (yes / no)"

After writing:
> "Configuration written — [timestamp].
>
> Skills now available:
> ✅ kickoff-prep — ready (model, segment, kickoff format configured)
> ✅ onboarding-plan — ready (duration, milestones, methodology configured)
> ✅ milestone-tracker — ready (milestone definitions and escalation matrix configured)
> ✅ success-criteria — ready (success criteria model configured)
> ✅ blocker-review — ready (escalation matrix and playbook location configured)
> ✅ ttv-analysis — ready (TtV target and measurement method configured)
> ✅ handoff-doc — ready (graduation criteria and handoff format configured)
> ✅ customize — ready
>
> [If any fields were left as PLACEHOLDER:]
> ⚠️ [skill-name] — blocked: [field] is still [PLACEHOLDER]. Run
> `/onboarding:customize --section [section]` to complete it."

---

## `--check-integrations` Mode

Skip the interview. For each integration configured in CLAUDE.md, test live connectivity:

> "Running integration health check — [timestamp]
>
> | Tool | Configured | Live connection | Data accessible |
> |------|-----------|----------------|-----------------|
> | Asana | ✅ configured | ✅ connected | Tasks, milestones |
> | Salesforce | ✅ configured | ⚠️ auth expired | — |
> | Google Drive | ✅ configured | ✅ connected | Docs, sheets |
> | Gainsight | ❌ not configured | — | — |
>
> Action: Salesforce auth needs refresh. Re-authenticate via [method].
> Updated integration status written to config — [timestamp]."

---

## `--quick` Mode

Collect 9 abbreviated questions covering the minimum needed to run most skills:

1. Your role:
2. Onboarding model (white-glove / guided-self-serve / implementation-plus-handoff / partner-led):
3. Segments you own:
4. Average onboarding duration (overall or by segment):
5. TtV target (what does value look like and by when):
6. Milestone day targets (can accept defaults: 5/14/21/30/60):
7. Graduation criteria (what must be true before handoff):
8. Escalation — who do you go to for a stuck account (name and contact):
9. CS methodology or framework (or "none"):

After collecting:
> "Minimum configuration written — [timestamp].
>
> Skills unlocked: kickoff-prep, onboarding-plan, milestone-tracker (basic),
> blocker-review (basic), handoff-doc.
>
> Skills still blocked: success-criteria (needs success criteria template and metric),
> ttv-analysis (needs TtV measurement method), customize (needs full profile).
>
> Run `/onboarding:cold-start-interview --redo` to complete the full setup."

---

## Security & Permissions

This skill operates read-only against connected MCP data sources during integration detection.
Configuration output is written to `~/.claude/plugins/config/claude-for-customer-success/` — no other filesystem paths are written.
No subprocess execution, no dynamic code execution, no outbound network calls made directly.

## Trust & Verification

Configuration files generated by this skill are the authoritative source for all other onboarding skills.
All placeholder values are clearly marked `[PLACEHOLDER]` — no skill will silently use an empty or default value.
CSM review is required before treating any generated config as final — skill presents a proposed config, never self-activates.

## Guardrails

**No write without confirmation.** Always display the full proposed configuration and
require explicit confirmation before writing to any config file.

**Never speculate field values.** Do not suggest or infer values for fields the user
has not provided. Config fields drive account management decisions — a silently
incorrect value is worse than a placeholder.

**TtV targets are planning tools, not commitments.** When collecting TtV targets,
clarify: these are used to calibrate skill outputs, not as customer-facing promises.
The skill will label TtV estimates `[review — internal planning target]` in outputs.

**Preserve untouched sections.** When `--section` is used, write only to the target
section. Confirm the file structure supports section-level isolation before writing.

**Route to `--redo-company-profile` for company changes.** The shared company-profile.md
is used by both renewals and onboarding skills. Do not rewrite it during a standard
onboarding `--redo` unless the user explicitly selects `--redo-company-profile`.

**Escalation defaults require review.** If the user accepts all escalation defaults
without providing actual contact names, flag those fields:
> "⚠️ Escalation matrix uses default role labels, not named contacts. Run
> `/onboarding:customize --section escalation` to add real names before using
> blocker-review or milestone-tracker for live accounts."

**`--check-integrations` does not edit interview fields.** The connectivity check
updates integration status fields only — it does not re-run or overwrite any other
section of the config file.
