---
name: cold-start-interview
version: 1.0.0
deployment_target: plugin
status: PROPOSED
description: "Rev-ops plugin setup. Reads existing company-profile.md if present, then collects only rev-ops-specific configuration: planning parameters, headcount, discount thresholds, lead definitions, OCV catalog path, and connector status. Writes ~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md. Run once at install; re-run after major planning cycle changes."
---

[PROPOSED]

# Cold-Start Interview

Configures the rev-ops plugin by reading any existing C4CS company profile and
collecting only the fields that are specific to RevOps. Writes the company profile
that all rev-ops skills read at runtime.

**Run once at install.** Re-run after:
- A new annual planning cycle finalizes
- Segment, motion, or touch model changes
- Headcount changes by >2 FTEs in any function
- OCV catalog is ratified or replaced

---

## Use when
- New installation of the rev-ops agent requires company profile setup
- Company profile is missing or incomplete and skills are degrading to fallback mode
- RevOps configuration needs to be captured or updated for the first time

## Do NOT use for
- Updating individual skill configurations after cold start is complete
- Running operational skills (this skill produces the config that other skills read)
- Reporting or analysis tasks

## Typical Activation
"Cold start", "set up the rev-ops agent", "configure the company profile", "first-time setup", "profile is missing", "run cold start interview"

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md` and
`~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/rev-ops:cold-start-interview`.

Note from config: This skill writes the company profile; no config values are required at intake.

**G-code dependency:** All G-code guardrails referenced in this skill (G1–G9) are defined in the CLAUDE.md config loaded above. If Pre-flight halts or config is missing, G-codes are undefined — do not proceed with partial config.
---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of cold-start request is this?
   - New installation (no existing profiles — full interview required)
   - Update mode (existing company profile present — ask which fields to change)
   - Full re-run (existing profile, user wants fresh setup)
   - Partial update (specific fields only — collect only the changed fields)

2. **CONSTRAINTS**: What limits the solution space?
   1. Check for existing company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`
   2. Check for existing rev-ops company profile — if present, offer update vs. full re-run
   3. Collect required fields in priority order; skip inherited fields
   4. Validate completeness against `reference/config-schema.md`
   5. Write company profile; confirm written successfully

3. **EXPERT CHECK**: What would a veteran RevOps admin verify first?
   - Is company-profile.md present? If absent, direct user to C4CS plugin cold-start first — do not re-collect company-level fields here.
   - Is connector detection run before questions? Connector status affects which capability clusters show as Full vs. Partial in the readiness table.
   - Is cs_operating_model captured in Group C2? This gates four capability clusters — missing it produces a misleading readiness table.
   - Is the OCV catalog path confirmed or marked [PENDING]? Outcome-linked skills degrade without it.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Re-asking company-level questions that are already in company-profile.md
   - Skipping connector detection — readiness table will misreport Full capability for disconnected tools
   - Writing the company profile before all required field groups are complete
   - Omitting cs_operating_model scoring — the capability table depends on this field

**After execution**, verify:
- Company profile written to `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`
- Readiness table reflects actual connector status and cs_operating_model value
- Degraded skills listed with specific improvement path
- Confidence: High when all required groups are answered and connectors confirmed; Moderate when any field group is estimated or connector status is uncertain
- Confidence: [High] when all required groups are answered and connectors confirmed / [Medium] when any field group is estimated or connector status is uncertain / [Low] if all inputs are manual or unverified

---

## Step 1 — Check Existing Profiles

Before asking anything, check:

```
~/.claude/plugins/config/claude-for-customer-success/company-profile.md
~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md
```

**If company-profile.md exists:** Read it silently. Confirm which fields are already
known. Do not re-ask them. Tell the user: "I found your existing C4CS company profile.
I'll skip company-level questions and ask only for RevOps-specific configuration."

**If rev-ops/CLAUDE.md already exists:** Ask: "You already have a RevOps practice
profile. Would you like to update specific fields, or run the full setup again?"
Update mode: ask only which fields need changing. Full re-run: proceed with all steps.

**If neither exists:** Run the full interview. Company-level questions are NOT in scope
— direct the user to run `/csm:cold-start-interview` (or any other C4CS plugin) first
if company profile is missing. Offer to proceed with a minimal profile using only
session-provided values if they want to skip full setup.

---

## Step 2 — Connector Detection

Check which connectors are live. Report status before asking configuration questions.

```
Checking connectors...
  HubSpot:      [connected / not connected]
  Google Drive: [connected / not connected]
  Slack:        [connected / not connected]
  Linear:       [connected / not connected]
  Zapier:       [connected / not connected]
  CS Platform:  [connected via [platform] / not connected]
```

Connectors affect which skills have full vs. degraded capability. Confirm the list
with the user and ask them to connect any missing connectors before proceeding — or
continue with degraded mode acknowledged.

---

## Step 3 — RevOps-Specific Questions

Ask in this order. One group at a time. Do not batch unrelated questions.

**Group A — Planning parameters** (required)

- "What is your ARR growth target for this fiscal year? (e.g., 45% → enter 0.45)"
- "What is your current Net Revenue Retention? (e.g., 108% → enter 1.08)"
- "What is your primary sales motion? [Outbound-Heavy / Mixed / Inbound-Dominant / PLG]"
- "What is your CS touch model? [High-Touch / Tech-Touch / Pooled]"
- "What is the annual new ARR quota for a fully-ramped AE?"
- "What is your target ARR per CSM?"

**Group B — Current headcount** (required)

- "How many fully-ramped AEs do you currently have?"
- "How many CSMs do you currently have?"
- "How many open AE and CSM requisitions are currently in process?"

**Group C — Discount and deal desk** (required)

- "What is the maximum discount an AE manager can approve without escalation? (e.g., 15% → 0.15)"
- "What is the maximum discount a RevOps lead can approve?"
- "What is your standard payment terms (net-N days)? [Default: 30]"
- "How many days before renewal do you initiate the renewal conversation? [Default: 90]"

**Group C2 — CS operating model maturity** (required — gates revenue function clusters)

This group determines whether the CS org is operating as a revenue center or a
delivery/retention function. The answer gates four capability clusters that are only
applicable if CS owns pipeline and carries quota.

Ask these questions as a single decision point:

- "Does your CS organization currently carry a revenue quota? [Yes / No / Planned for next cycle]"
- "Does CS own and forecast an expansion pipeline independently? [Yes / No]"
- "Does CS own renewal revenue (GRR accountability) with a named CS leader carrying that number? [Yes / No]"

**Scoring logic (write `cs_operating_model` to company profile):**

```
If all three Yes (or Yes/Planned mix for #1):
  cs_operating_model: revenue_center
  → Enable all CS revenue function clusters

If Yes on renewal ownership only (GRR accountability present, no expansion quota):
  cs_operating_model: retention_center
  → Enable: CS renewal book, GRR monitoring, churn model
  → Disable: CS expansion deal desk, CS expansion forecasting, quota modeling, comp simulation

If No on all three:
  cs_operating_model: delivery_function
  → Enable: handoff quality, OCV delivery, churn monitoring
  → Disable: all CS revenue function clusters (they will show as [Not applicable — delivery model])

If Planned on quota/pipeline:
  cs_operating_model: revenue_center_transition
  → Enable all clusters but label them [Transition mode — configure when quota is live]
  → Prompt: "I'll configure the revenue function clusters in placeholder mode. Run
     cold-start-interview again once quota is assigned and pipeline ownership is live."
```

**Follow-up questions if `cs_operating_model = revenue_center` or `revenue_center_transition`:**

- "What is the CS expansion quota for the current fiscal year? (Total expansion ARR target)"
- "What is the maximum expansion discount a CS manager can approve without escalation?
   [Default: same as Sales standard threshold — enter to use default or specify separately]"
- "What is the maximum expansion discount a CS leader can approve?
   [Default: same as Sales elevated threshold — enter to use default or specify separately]"
- "Does your CS org use quota-based compensation (OTE model)? [Yes / No]"
  → If Yes: "What is the CS variable payout split (expansion vs. renewal vs. other)?
     (e.g., 60% expansion / 40% renewal)" [Used by cs-quota-sensitivity skill]

**Follow-up questions if `cs_operating_model = retention_center`:**

- "What is your GRR target for this fiscal year? (e.g., 88% → enter 0.88)"
- (Expansion discount thresholds: skip — not applicable)

---

**Group D — Lead definitions** (required)

- "How do you define an MQL?"
- "How do you define an SAL?"
- "How do you define an SQL?"

**Group E — OCV catalog** (optional — check company-profile.md first)

- Before asking, check `company-profile.md` for an existing `catalog_path` value.
- If `catalog_path` is already set (not `[PLACEHOLDER]` or `[PENDING]`):
  Tell the user: "Your Outcome & Value Catalog is already registered at [path]. Rev-ops skills will read it automatically."
  Ask: "What version is it, and when was it last ratified?" (to populate `catalog_version` and `ratified_date` if PLACEHOLDER).
- If `catalog_path` is `[PLACEHOLDER]` or `[PENDING]` (catalog not yet built):
  Tell the user: "No Outcome & Value Catalog is registered yet. Your rev-ops skills will run in degraded mode for outcome-linked skills until one exists."
  Offer: "Run `/csm:cold-start-interview --generate-outcome-catalog` to automatically build your catalog from public product sources. The path will be registered in company-profile.md and read by all C4CS agents — including rev-ops — automatically."
  Write `catalog_path: [PENDING]` in the company profile and move on.

**Group F — Optional enrichment**

- "What is your average deal ACV? (Used for account-count capacity modeling — optional)"
- "What is your average sales cycle in days? (Used in churn detection — optional)"
- "Do you have a saved unit-of-growth-calculator output for the current plan year? If so, what is the file path?"

---

## Step 4 — Write Company Profile

Once all required fields are collected, write the company profile using the template
in `reference/config-schema.md`. Confirm the path:

`~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`

After writing, display a summary of what was written and what was left as defaults.
Flag any required fields that are still missing.

---

## Step 5 — Capability Readiness Summary

After writing, produce a readiness table. The table content depends on
`cs_operating_model` from Group C2.

**Base readiness table (all operating models):**

```
REV-OPS PLUGIN READINESS
─────────────────────────────────────────────────────────────
SA1 Forecast Intelligence      ✓ Full    HubSpot connected
SA2 Pipeline Health            ✓ Full    HubSpot connected
SA3 Planning Engine            ✓ Full    UoG baseline present
SA4 CRM Data Quality           ✓ Full    HubSpot connected
SA5 Revenue Continuity         ⚡ Partial OCV catalog not configured
SA6 Deal Desk (new-logo)       ✓ Full    Thresholds configured
ARIA Orchestrator              ✓ Full    All agents ready
```

**Append CS revenue function cluster rows based on cs_operating_model:**

```
IF cs_operating_model = revenue_center:
  CS Expansion Pipeline        ✓ Full    Quota configured, expansion thresholds set
  CS Renewal Book              ✓ Full    GRR target configured
  CS Forecast & Attainment     ✓ Full    Expansion pipeline active
  CS Deal Desk (expansion)     ✓ Full    CS expansion thresholds configured
  CS Quota Modeling            ✓ Full    [if cs_variable_comp = Yes]
                                ⚡ N/A   [if cs_variable_comp = No]

IF cs_operating_model = revenue_center_transition:
  CS Expansion Pipeline        ⚡ Transition  Quota not yet live — configure when active
  CS Renewal Book              ✓ Full         GRR target configured
  CS Forecast & Attainment     ⚡ Transition  Pipeline ownership pending
  CS Deal Desk (expansion)     ⚡ Transition  Thresholds in placeholder mode
  CS Quota Modeling            ⚡ Transition  [label: configure when quota is assigned]

IF cs_operating_model = retention_center:
  CS Renewal Book              ✓ Full    GRR target configured
  CS Expansion Pipeline        — N/A     CS does not own expansion pipeline
  CS Forecast & Attainment     — N/A     No CS expansion quota
  CS Deal Desk (expansion)     — N/A     Not applicable — delivery model
  CS Quota Modeling            — N/A     Not applicable — delivery model

IF cs_operating_model = delivery_function:
  CS Revenue Clusters          — Not applicable  CS operates as delivery function
  [All four clusters suppressed from capability table]
```

**Append degraded skill list (all models):**

```
Skills running in degraded mode:
  outcome-to-value-tracking    [Confidence: Low] — OCV catalog absent
  deal-to-outcome-tracing      [Confidence: Low] — OCV catalog absent
  early-churn-downgrade        [Tier 1: Rule mode] — no cohort data

To improve: run /csm:cold-start-interview --generate-outcome-catalog to build your OCV catalog.
The path will be registered in company-profile.md and read automatically by rev-ops skills.
─────────────────────────────────────────────────────────────
```

**If cs_operating_model = delivery_function or retention_center, append:**

```
Note: Four capability clusters are not active for your current CS operating model:
  • CS Expansion Pipeline & Forecasting
  • CS Deal Desk (expansion motion)
  • CS Planning & Incentive Design
  • CS Quota / Comp Simulation

These clusters activate when your CS org carries expansion quota and owns
expansion pipeline. Re-run cold-start-interview to enable them when your
operating model evolves.
─────────────────────────────────────────────────────────────
```

---

## Output

```
REV-OPS PLUGIN READINESS — [date written]
─────────────────────────────────────────────────────────────
[Connector status table]
[SA1–SA6 + ARIA readiness rows]
[CS revenue cluster rows based on cs_operating_model]
[Degraded skills list with improvement paths]
─────────────────────────────────────────────────────────────
Company profile written: ~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md
[DRAFT — review before using skills]
```

---

## Guardrails

This is a configuration skill. No account data is produced. Guardrails G1–G8
do not apply to interview outputs.

## Reference Files

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

## Security & Permissions

- Reads: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`
- Writes: `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`
- No CRM or connector calls during setup
- No customer or account data processed

## Trust & Verification

**Input trust model:** All user-provided parameters are treated as untrusted at intake. Numeric inputs are validated for plausible range before use in calculations. String inputs are not evaluated as code.
**Output trust model:** All outputs are proposals or analytical inputs — no outputs constitute approved decisions, revenue commitments, or system actions without explicit human confirmation.
**Connector data:** Data retrieved via MCP connectors is treated as read-only observed state. Timestamps and data-as-of labels are applied to all connector-sourced values per G6.
**Write-tier confirmation:** Any proposed write to HubSpot, Linear, or Slack is surfaced as a draft requiring explicit user confirmation before execution.
