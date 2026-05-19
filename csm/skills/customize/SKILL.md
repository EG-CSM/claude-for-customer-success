---
name: customize
description: >
  Configure the CSM plugin for your company — CS motion, health model, churn
  signal definitions, escalation matrix, playbook, and tool integrations. Runs
  a guided interview and writes your company profile to the plugin config files.
  Use when your CS practice changes materially (new segments,
  new CS platform, motion change, escalation routing update). Alias for
  cold-start-interview when run fresh; also supports partial reconfiguration
  of specific sections without a full re-run.
argument-hint: "[--full | --section <section-name> | --reset]"
version: "1.0.0"
deployment_target: plugin
config_skill: true
---

# /csm:customize

[PROPOSED]

## Use When
- Updating a specific config section without re-running the full interview (`--section <name>`)
- CS practice has changed: new segments, motion change, escalation routing update, new CS platform
- Resetting all configuration to start fresh (`--reset`)

## Do NOT Use For
- Running the full guided interview for the first time — prefer `/csm:cold-start-interview` for a cleaner first-run experience
- Answering CS strategy questions — answer directly
- Configuring other plugins (cs-ops, renewals, onboarding)

## Typical Activation
"/csm:customize"
"/csm:customize --section escalation-matrix"
"/csm:customize --section health-model"
"/csm:customize --reset"
"Update my churn signal definitions"

---

Configure the CSM plugin to match your company's CS practice — so every other
skill runs against your actual model, not a generic template.

---

## Pre-flight

Check for existing config files at:
- `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`
- `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

For `--full` or no argument: proceed regardless of whether files exist — this skill creates or overwrites them.
For `--section <name>`: load existing config file content before displaying current values alongside each question.
For `--reset`: display a destructive-clear warning and require explicit confirmation before proceeding.

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of customization request is this?
   - **Full Configuration**: Major practice change — all 8 interview sections, both config files from scratch
   - **Section Reconfiguration**: Single section update — preserve existing config around the edit, validate cross-section consistency
   - **Motion Change**: CS motion shift — cascading impact on engagement model, escalation matrix, playbook, and account loads
   - **Integration Swap**: CS platform or CRM replacement — health model source, churn signal data dependencies, and integration priority all shift
   - **Reset and Rebuild**: Destructive clear — requires double confirmation, cross-plugin impact warning

2. **CONSTRAINTS**: What limits the solution space?
   - Config files govern all downstream skills — every value propagates; no silent defaults
   - `company-profile.md` is shared across four plugins — edits have cross-plugin blast radius
   - User must review and explicitly confirm before any file write
   - Placeholders are acceptable; invented values are not
   - G4: Do not recommend escalation without a named escalation path — the escalation matrix must have named, contactable owners before skills can route escalations

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - Does the mode (`--full`, `--section`, `--reset`) match the actual scope of change?
   - Are there cross-section dependencies affected by this change (e.g., health model change → churn signal thresholds)?
   - Does every escalation row have a named, contactable owner — not just a role title?
   - Do health model components have a confirmed data source, not just a label?
   - If motion is changing, are engagement cadences, account loads, and escalation SLAs also being updated?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - ❌ Pre-filling config values the user hasn't provided — gaps must be `[PLACEHOLDER]`, never guesses
   - ❌ Updating one section without checking cross-references in adjacent sections
   - ❌ Accepting "all High" churn signal weights without challenge — if everything is high priority, nothing is
   - ❌ Writing config files before displaying them for user review and confirmation
   - ❌ Running `--section company-profile` without warning about impact on cs-ops, renewals, and onboarding plugins

**After execution**, verify:
- Does every config section contain real values or explicit `[PLACEHOLDER]` markers — no silent gaps?
- Are cross-section references consistent (churn signals align with health model, escalation matrix covers all segments)?
- Confidence: [High] if all interview questions answered and confirmed; [Medium] if placeholders remain; [Low] if motion change with unchecked downstream sections


## What this does

Every skill in the CSM plugin reads two config files before executing:

1. `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` — your
   CS company profile (this file, written by this skill)
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md` — your
   company and product profile (shared across all four CS plugins)

If either file is missing, has `[PLACEHOLDER]` markers, or is outdated, the skills
in this plugin prompt you to run `/csm:customize` or `/csm:cold-start-interview`.

---

## Mode

`--full`: Run the complete guided interview and regenerate both config files.
Equivalent to `/csm:cold-start-interview`.

`--section`: Reconfigure one section without re-running the full interview.
Available sections:
- `health-model` — update health components, weights, and thresholds
- `escalation-matrix` — update routing, contacts, and SLAs
- `churn-signals` — update signal definitions and weights
- `cs-motion` — update CS motion type and engagement model
- `playbook` — update or add plays to the configured playbook
- `integrations` — update which tools are connected and in what priority order
- `company-profile` — update company name, product, primary value metric,
  and value categories

`--reset`: Clear both config files and restart from scratch. Prompts for
confirmation before clearing — this is destructive.

---

## Guided interview — full configuration

Run this interview in sequence. Each section asks focused questions and confirms
the answers before moving to the next section. At the end, produce both config
files and display them for review before writing to disk.

---

### Section 1 — Company and product

1. What is your company name?
2. What is your product name? (If multiple products, which is this plugin for?)
3. What type of software do you sell? (B2B SaaS / B2B platform / other — describe)
4. What are the primary value categories your customers care about?
   Examples: efficiency, risk reduction, revenue growth, cost savings, user experience,
   compliance. List the ones most relevant to your customers.
5. What is your primary value metric — the single most important measure of whether
   a customer is succeeding? (e.g., time to first outcome, feature adoption rate,
   user activation rate, outcome achieved)
6. What is your target time to first value for new accounts?
   (e.g., 30 days to first activated workflow, 60 days to first report generated)

---

### Section 2 — Customer segments

7. What customer segments do you serve?
   Examples: SMB (under $50K ARR), Mid-market ($50K–$200K), Enterprise ($200K+).
   Use your internal definitions — name the segments and the ARR ranges for each.
8. For each segment, what is the standard CS motion?
   - SMB: [tech-touch / pooled CSM / community-led]
   - Mid-market: [scaled / hybrid / high-touch]
   - Enterprise: [high-touch / dedicated CSM]
9. What is your ARR threshold for a high-touch vs. tech-touch motion?
   (e.g., "accounts above $75K ARR get a dedicated CSM")

---

### Section 3 — Health model

10. What components make up your health score? List each and its weight.
    Example: usage (40%), engagement (20%), support load (20%), NPS (20%)
    If you don't have a formal health score: what signals tell you an account is
    healthy or at risk? List 3-5.
11. What are the thresholds for each health classification?
    - Green: [score range or criteria]
    - Yellow: [score range or criteria — "watch" tier]
    - Red: [score range or criteria — "at risk" tier]
12. Is health score calculated by a CS platform (e.g., Gainsight, ChurnZero,
    Totango, Planhat, Vitally) or do you track it manually?

---

### Section 4 — Churn signal definitions

13. What signals tell you an account may churn? List up to 8.
    For each signal, specify its weight: **High**, **Medium**, or **Low**.

    Standard signals (confirm which apply and adjust weight):
    - Executive sponsor departure or disengagement [High / Medium / Low]
    - Product usage drop (specify threshold: >__% over __ days) [High / Medium / Low]
    - Open escalation or unresolved P1/P2 ticket [High / Medium / Low]
    - NPS detractor score + no recovery conversation [High / Medium / Low]
    - Missed QBR or no-show pattern (__ consecutive) [High / Medium / Low]
    - Competitor evaluation underway [High / Medium / Low]
    - No CSM contact in >__ days [High / Medium / Low]
    - [Custom signal — describe] [High / Medium / Low]

14. What is the threshold for automatic escalation based on churn signals?
    (e.g., "any two High signals present = escalate immediately")

---

### Section 5 — Escalation matrix

15. Who owns escalation for each scenario? Provide the contact name and role.
    Complete this matrix:

    | Scenario | Escalation owner | Channel | SLA |
    |----------|-----------------|---------|-----|
    | Critical risk (multiple High signals, renewal <90 days) | | Slack / email / phone | |
    | High risk (one High signal or ARR above threshold) | | | |
    | Medium risk (multiple Medium signals) | | | |
    | Executive sponsor departure | | | |
    | Technical P1 (unresolved >48h) | | | |
    | Customer complaint / executive demand | | | |

16. What is the ARR threshold at which a VP CS or CRO must be looped into
    escalation communications? (e.g., "ARR over $150K")
17. Who is the default CS team lead for CSM escalations?
    (name and contact method)

---

### Section 6 — Engagement model

18. For high-touch accounts, what is the standard engagement cadence?
    - Check-in call frequency: [monthly / bi-weekly / quarterly]
    - QBR cadence: [quarterly / semi-annual / annual]
    - Executive sponsor touch cadence: [quarterly / semi-annual]
19. For tech-touch accounts:
    - Primary engagement channel: [email / in-product / community / CSM pool]
    - Check-in frequency: [quarterly / triggered by health signal only]
20. What is the maximum number of accounts a CSM typically carries?
    (e.g., "High-touch CSMs carry 40-60 accounts; tech-touch carry 200+")

---

### Section 7 — Playbook

21. Do you have a set of standard plays for common CS situations?
    If yes, list them by name and trigger condition. (Paste from your playbook
    documentation, or describe them verbally.)
    If no: use the standard TARO play library as the default.
22. Are there any plays that are explicitly NOT used at your company?
    (e.g., "We do not run automated at-risk email campaigns — all at-risk
    outreach is CSM-initiated")

---

### Section 8 — Tooling

23. What is your CS platform? (Gainsight / ChurnZero / Totango / Planhat /
    Vitally / Salesforce CS / other / none)
24. What is your CRM? (Salesforce / HubSpot / other / none)
25. Do you use a call recording or conversation intelligence tool?
    (Gong / Chorus / Fireflies / other / none)
26. What do you use for document storage / customer-facing documents?
    (Google Drive / Notion / Confluence / SharePoint / other)
27. Any other tools relevant to CS workflow? (e.g., Gainsight for health +
    Salesforce for ARR — list both if applicable)

---

## Config file output

After completing the interview, generate both config files.

Do not write them to disk until the user has reviewed and confirmed.
Display both files in full. Then ask:

> "Does this look right? I'll write the config files once you confirm.
> You can also tell me what to change — I'll update before writing."

Once the user confirms, write using the following sequence:

**Write Safety Protocol — dual-location config write:**
1. Write to the primary location first: `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` (creating parent directories as needed).
2. Confirm the write succeeded by reading back the written content and verifying it matches what was generated.
3. Only proceed to write the secondary location (`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`) after step 2 confirms success.
4. If the secondary write fails: surface an explicit error to the user identifying exactly which file failed, what content was intended for that file, and what (if anything) was written. Do NOT silently proceed or assume both writes succeeded.
5. Provide the user with the full content that failed to write so they can manually apply it if needed.

---

### File 1: CSM Company Profile

**Path:** `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`

```markdown
# CSM Company Profile
# Generated by /csm:customize on [date]
# Rerun /csm:customize --section [section-name] to update a specific section

## Company
- Company name: [answer]
- Product name: [answer]
- Product type: [answer]
- Primary value metric: [answer]
- Target time to first value: [answer]

## Customer segments
[Table: segment name, ARR range, CS motion, dedicated CSM threshold]

## Health model
- CS platform: [answer]
- Components and weights: [table from answers]
- Green threshold: [answer]
- Yellow threshold: [answer]
- Red threshold: [answer]

## Churn signal definitions
[Table: signal, weight, threshold (where applicable)]

## Escalation matrix
[Table: scenario, owner, channel, SLA]
- ARR escalation threshold: $[answer]
- CS team lead: [name] — [contact method]

## Engagement model
### High-touch
- Check-in cadence: [answer]
- QBR cadence: [answer]
- Executive sponsor touch: [answer]
- Max accounts per CSM: [answer]

### Tech-touch
- Primary channel: [answer]
- Check-in cadence: [answer]
- Max accounts per CSM: [answer]

## Playbook
[List of configured plays with trigger conditions, or "Standard TARO library"]
[Any explicitly excluded plays]

## Integrations (priority order)
1. [CS platform name] — health, usage, CTAs
2. [CRM name] — ARR, contacts, history
3. [Call recording] — call history, transcripts
4. [Document storage] — success plans, QBRs
```

---

### File 2: Company Profile

**Path:** `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

```markdown
# Company Profile
# Shared across all claude-for-customer-success plugins
# Generated by /csm:customize on [date]

## Company
- Name: [answer]
- Product: [answer]
- Type: [answer]

## Value framework
- Primary value metric: [answer]
- Value categories: [list from answers]
- Target time to first value: [answer]

## Customer profile
- Segments: [list with ARR ranges]
- ICP description: [optional — add after initial setup]
```

---

## Section-level reconfiguration

When `--section` is specified, run only the questions for that section.
Display the current values (from the existing config file) alongside each
question, so the user can confirm or change. Only rewrite the affected section
— do not regenerate the full file.

Example: `--section escalation-matrix` → show current matrix → ask questions
15-17 → update only the escalation matrix section in the CLAUDE.md file.

---

> [review before sending]

## Guardrails

**Review before write.** Never write config files without displaying them and
receiving explicit user confirmation. These files govern how every other skill
behaves — an error in the config propagates to all downstream skills.

**No invented values.** Do not pre-fill config sections with assumed values.
If the user hasn't answered a question, mark the section `[PLACEHOLDER — run
/csm:customize to complete]` and surface the gap in the reviewer note.

**Reset confirmation.** `--reset` requires explicit confirmation before clearing
files. Display a warning: "This will clear all configuration. Every skill in
the CSM plugin will require reconfiguration before it can run. Confirm?"

**Shared file integrity.** `company-profile.md` is shared across all four
CS plugins. When updating it from this skill, note that changes will affect
cs-ops, renewals, and onboarding plugins as well. If those plugins have been
customized independently, alert the user to review for consistency.

**Write order integrity.** Always write `csm/CLAUDE.md` first, verify the readback,
then write `company-profile.md`. If `company-profile.md` fails after `csm/CLAUDE.md`
succeeds, stop and surface the failure explicitly — do not continue as if both writes
completed. The user must be able to recover the failed content manually.

---

## After setup

- "Plugin is configured. Run a health review on an account: `/csm:health-score-review [account]`"
- "Build account context before your next call: `/csm:account-research [account]`"
- "Run a portfolio triage to see where your book stands: `/csm:health-score-review --triage`"
- "Want to configure the other CS plugins? If the `cs-ops` plugin is installed, run `/cs-ops:customize`. If the `renewals` plugin is installed, run `/renewals:customize`. If the `onboarding` plugin is installed, run `/onboarding:customize`."

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: none
- filesystem_write: config files only (explicitly listed paths)
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- All config writes require explicit user confirmation before executing
- No values are invented — gaps use [PLACEHOLDER] markers
- Config files govern downstream skill behavior; treat writes as high-trust operations
