---
name: cold-start-interview
version: 1.0.0
description: "Rev-ops plugin setup. Reads existing company-profile.md if present, then collects only rev-ops-specific configuration: planning parameters, headcount, discount thresholds, lead definitions, OCV catalog path, and connector status. Writes ~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md. Run once at install; re-run after major planning cycle changes."
---

# Cold-Start Interview

Configures the rev-ops plugin by reading any existing C4CS company profile and
collecting only the fields that are specific to RevOps. Writes the practice profile
that all rev-ops skills read at runtime.

**Run once at install.** Re-run after:
- A new annual planning cycle finalizes
- Segment, motion, or touch model changes
- Headcount changes by >2 FTEs in any function
- OCV catalog is ratified or replaced

---

## Reasoning Protocol (simplified — config skill, no guardrail checks)

1. Check for existing company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`
2. Check for existing rev-ops practice profile — if present, offer update vs. full re-run
3. Collect required fields in priority order; skip inherited fields
4. Validate completeness against `reference/config-schema.md`
5. Write practice profile; confirm written successfully

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
  Write `catalog_path: [PENDING]` in the practice profile and move on.

**Group F — Optional enrichment**

- "What is your average deal ACV? (Used for account-count capacity modeling — optional)"
- "What is your average sales cycle in days? (Used in churn detection — optional)"
- "Do you have a saved unit-of-growth-calculator output for the current plan year? If so, what is the file path?"

---

## Step 4 — Write Practice Profile

Once all required fields are collected, write the practice profile using the template
in `reference/config-schema.md`. Confirm the path:

`~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`

After writing, display a summary of what was written and what was left as defaults.
Flag any required fields that are still missing.

---

## Step 5 — Capability Readiness Summary

After writing, produce a readiness table:

```
REV-OPS PLUGIN READINESS
─────────────────────────────────────────────────────────────
SA1 Forecast Intelligence      ✓ Full    HubSpot connected
SA2 Pipeline Health            ✓ Full    HubSpot connected
SA3 Planning Engine            ✓ Full    UoG baseline present
SA4 CRM Data Quality           ✓ Full    HubSpot connected
SA5 Revenue Continuity         ⚡ Partial OCV catalog not configured
SA6 Deal Desk                  ✓ Full    Thresholds configured
ARIA Orchestrator              ✓ Full    All agents ready

Skills running in degraded mode:
  outcome-to-value-tracking    [Confidence: Low] — OCV catalog absent
  deal-to-outcome-tracing      [Confidence: Low] — OCV catalog absent
  early-churn-downgrade        [Tier 1: Rule mode] — no cohort data

To improve: run /csm:cold-start-interview --generate-outcome-catalog to build your OCV catalog.
The path will be registered in company-profile.md and read automatically by rev-ops skills.
─────────────────────────────────────────────────────────────
```

---

## Guardrails

This is a configuration skill. No account data is produced. Guardrails G1–G8
do not apply to interview outputs.

## Security & Permissions

- Reads: `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`
- Writes: `~/.claude/plugins/config/claude-for-customer-success/rev-ops/CLAUDE.md`
- No CRM or connector calls during setup
- No customer or account data processed
