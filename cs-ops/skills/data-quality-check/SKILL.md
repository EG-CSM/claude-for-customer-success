---
name: data-quality-check
description: >
  Audit CRM and CS platform data quality against configured field requirements —
  completeness, staleness, consistency, and orphaned records. Use before reporting
  cycles, after CSM transitions, or when analytics outputs appear unreliable.
  Produces a field-level data quality scorecard with a prioritized remediation
  backlog. Distinct from health-model-review: this skill audits the data feeding
  the health model; health-model-review audits the model itself.
argument-hint: "[--full | --completeness | --staleness | --consistency | --field <field-name>]"
version: "1.0.0"
---

# /cs-ops:data-quality-check

Data quality problems don't announce themselves — they surface as incorrect
dashboards, missed renewals, and capacity plans built on fictional account counts.

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
and `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/cs-ops:cold-start-interview`.

Critical configuration to apply:
- Required CRM fields and their completeness expectations
- Health data staleness threshold (e.g., "health scores must update within 30 days")
- Segment assignment method — informs whether segment field is required vs. computed
- CSM assignment model — informs whether CSM owner field is always expected

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G7 (the purpose of this skill is to surface stale data — every stale record flagged must include source date and staleness indicator).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--full`: Complete data quality audit — completeness, staleness, consistency,
and orphaned record checks across all configured required fields. **Default.**

`--completeness`: Field completeness audit only — which required fields are
missing values, for how many accounts, and at what ARR concentration.

`--staleness`: Staleness audit only — fields that have not been updated within
the configured threshold. Produces a stale-record list.

`--consistency`: Consistency audit only — cross-field logic violations
(e.g., segment classification inconsistent with ARR, health tier inconsistent
with score range, renewal date in the past with no churn record).

`--field <field-name>`: Single-field deep audit — completeness, staleness,
and consistency for one named field across the full account list.

---

## Data gathering

Pull from connected integrations:
- CRM: all account records with all field values (not just populated fields)
- CS Platform: health scores, component scores, lifecycle stages, last-updated timestamps
- CS-Ops config: required field list, staleness thresholds

If nothing is connected:
> "To run a data quality check, I need a full account export — one row per
> account, all columns including blank/null values. Do not filter to populated
> fields only — the blank fields are what I'm looking for.
>
> Required columns: account name, ARR, segment, health tier, CSM owner,
> renewal date, lifecycle stage, and any other fields configured as required.
> Share a CSV or paste the data and I'll run the audit."

Minimum required before proceeding: account list with at least 3 of the
configured required fields — including ARR and CSM owner.

---

## Full data quality audit (`--full`)

---

**Data Quality Audit**
*[Date] · [N] accounts · $[total ARR] · INTERNAL — CS-Ops use only*
*Required fields audited: [N] (per cs-ops CLAUDE.md configuration)*

---

### Executive summary

| Dimension | Score | Accounts affected | ARR affected |
|-----------|-------|------------------|-------------|
| Completeness | [%] | [N] with ≥1 missing required field | $[amount] |
| Staleness | [%] | [N] with ≥1 stale required field | $[amount] |
| Consistency | [%] | [N] with ≥1 logic violation | $[amount] |
| Orphaned records | — | [N] accounts with no CSM and no segment | $[amount] |
| **Overall data quality score** | **[%]** | **[N] clean accounts** | **$[clean ARR] ([%] of total)** |

**Overall interpretation:**
[2-3 sentences on the most significant data quality finding and its
downstream impact. Example: "CSM owner is missing on [N] accounts ($[ARR]),
which means the capacity planner is undercounting load and the at-risk report
is excluding those accounts from CSM-level triage. This is the highest-priority
remediation item — unowned accounts represent a coverage blindspot, not just
a data hygiene issue."]

---

### Field completeness audit (`--completeness` content)

---

**Field Completeness Report — [Date]**

| Field | Required | Complete | Missing | Missing % | ARR in missing accounts | Priority |
|-------|---------|---------|---------|-----------|------------------------|---------|
| CSM owner | ✅ Required | [N] | [N] | [%] | $[amount] | [High / Medium / Low] |
| ARR | ✅ Required | [N] | [N] | [%] | — | |
| Segment | ✅ Required | [N] | [N] | [%] | $[amount] | |
| Health tier | ✅ Required | [N] | [N] | [%] | $[amount] | |
| Renewal date | ✅ Required | [N] | [N] | [%] | $[amount] | |
| Lifecycle stage | ✅ Required | [N] | [N] | [%] | $[amount] | |
| [Additional configured fields] | | | | | | |

**Completeness flags:**

For each field missing on more than [configured threshold, e.g., 5%] of accounts:

> **[Field name] — [Missing %] incomplete ([N] accounts · $[ARR])**
> Missing [field name] affects: [which downstream skills and reports are impacted].
> [Specific impact]: "Without renewal date, the renewal forecast excludes these
> accounts and the at-risk report cannot surface renewals approaching in <90 days."
>
> **Root cause hypothesis:** [Data entry gap / CSM transition — records not updated /
> Automated sync failure / Field not required in CRM workflow] `[review]`
>
> **Remediation:** [Specific action — e.g., "Assign CS Ops to audit and backfill
> [field] for all [N] accounts within [timeframe]. Use [CRM report] to identify records."]

**Accounts missing multiple required fields:**

| Accounts with missing field count | Number of accounts | ARR | Risk |
|----------------------------------|-------------------|-----|------|
| Missing 1 required field | [N] | $[amount] | Moderate |
| Missing 2–3 required fields | [N] | $[amount] | High |
| Missing 4+ required fields | [N] | $[amount] | **Critical — effectively invisible** |

Accounts missing 4 or more required fields cannot be included in any meaningful
CS analytics. They are effectively invisible to portfolio management. List them:

| Account | ARR | Fields missing |
|---------|-----|---------------|
| [Account] | $[amount] | CSM owner, segment, health tier, renewal date |

---

### Staleness audit (`--staleness` content)

---

**Staleness Report — [Date]**
*Threshold: health scores updated within [configured threshold] days*

| Field | Staleness threshold | Stale accounts | Stale % | ARR in stale accounts |
|-------|-------------------|---------------|---------|----------------------|
| Health score | [N] days | [N] | [%] | $[amount] |
| Health score components | [N] days | [N] | [%] | $[amount] |
| Lifecycle stage | [N] days | [N] | [%] | $[amount] |
| CSM last contact date | [N] days | [N] | [%] | $[amount] |
| [Additional configured fields] | | | | |

**Staleness distribution (health score):**

| Days since last update | Accounts | ARR |
|----------------------|---------|-----|
| ≤[threshold] — current | [N] | $[amount] |
| [threshold+1]–60 days | [N] | $[amount] |
| 61–90 days | [N] | $[amount] |
| >90 days — severely stale | [N] | $[amount] |

**Most stale accounts (health score):**

| Account | Segment | ARR | Health tier | Last score update | Days stale |
|---------|---------|-----|------------|-----------------|-----------|
| [Account] | [Seg] | $[amount] | 🟡 Yellow | [date] | [N] |

**Staleness root cause patterns:**

[Identify common patterns — e.g., "Stale records are concentrated in the
SMB segment, which may indicate the tech-touch motion relies on manual score
updates that are not being performed. Enterprise accounts are all current.
Recommend an automated scoring trigger for SMB accounts or a monthly forced
update cadence."] `[review]`

---

### Consistency audit (`--consistency` content)

---

**Consistency Report — [Date]**
*Cross-field logic violations*

Consistency checks applied:

| Check | Rule | Violations | ARR in violations |
|-------|------|-----------|------------------|
| Segment ↔ ARR | Account ARR should match configured segment ARR range | [N] | $[amount] |
| Health tier ↔ score | Health tier should match the configured score threshold | [N] | $[amount] |
| Renewal date in past | Renewal date <today with no churn record in CRM | [N] | $[amount] |
| Lifecycle stage ↔ renewal date | "Churned" lifecycle stage with active renewal date | [N] | $[amount] |
| CSM owner ↔ segment | CSM motion mismatches segment (e.g., tech-touch CSM on Enterprise account) | [N] | $[amount] |
| Health tier change without CTA | Health tier degraded since last update with no active CTA | [N] | $[amount] |

**Violation detail:**

For each check with violations:

> **[Check name] — [N] violations ($[ARR])**
> **What this means:** [Explain the implication — which downstream function breaks]
> **Sample violations:**
>
> | Account | Field 1 value | Field 2 value | Conflict |
> |---------|-------------|-------------|---------|
> | [Account] | Segment: Enterprise | ARR: $35K | ARR below Enterprise floor of $[threshold] |
>
> **Remediation:** [Specific action]

---

### Orphaned record audit

Orphaned records are accounts that exist in the CRM but lack the minimum
fields needed to participate in any CS workflow.

**Orphaned record definition (this audit):**
An account with no CSM owner AND no segment classification. These accounts
cannot appear in capacity planning, segment analysis, or health reporting.

| Orphaned accounts | ARR | Avg ARR | Red health (if scored) |
|-----------------|-----|---------|----------------------|
| [N] | $[amount] | $[avg] | [N] ([%]) |

**Orphaned account list:**

| Account | ARR | Health tier (if present) | Renewal date (if present) | Age in CRM |
|---------|-----|------------------------|--------------------------|-----------|
| [Account] | $[amount] | None / [tier] | [date / None] | [N days] |

**Orphaned record disposition:**

Each orphaned account requires one of:
1. **Assign** — CSM owner and segment populated; account enters standard workflow
2. **Archive** — account is churned or inactive; remove from active portfolio
3. **Investigate** — account status unclear; escalate to CS lead

---

### Single-field deep audit (`--field <field-name>`)

---

**Field Audit — [Field name] — [Date]**

| Metric | Value |
|--------|-------|
| Field | [Field name] |
| Required | [Yes / No] |
| Total accounts | [N] |
| Populated | [N] ([%]) |
| Missing | [N] ([%]) |
| ARR in missing accounts | $[amount] |
| Staleness threshold | [N days / Not applicable] |
| Stale (if applicable) | [N] ([%]) |
| Consistency rule | [Rule applied / Not applicable] |
| Consistency violations | [N] ([%]) |

**Distribution of field values:**

| Value | Accounts | ARR | Notes |
|-------|---------|-----|-------|
| [Value 1] | [N] | $[amount] | |
| [Blank / Null] | [N] | $[amount] | ⚠️ Missing |

**Historical trend (if available):**

| Period | Missing % | Change |
|--------|-----------|--------|
| Current | [%] | — |
| Prior period | [%] | [↑ / ↓ N pp] |

**Remediation recommendation for [field name]:**
[Specific action to resolve missing, stale, or inconsistent values for
this field. Include the CRM object, field API name if known, and who should
own the remediation.]

---

### Remediation backlog

Ranked by impact (ARR affected × severity):

| Priority | Issue | Field(s) | Accounts | ARR affected | Assigned to | Due |
|---------|-------|---------|---------|-------------|-----------|-----|
| P1 | [Issue] | [Field] | [N] | $[amount] | [Role / TBD] | [date / TBD] |
| P2 | | | | | | |
| P3 | | | | | | |

**Estimated remediation effort:**

| Effort level | Items | Description |
|-------------|-------|-------------|
| Quick fix (<1 hour) | [N] | [e.g., Bulk CSM assignment via CRM report] |
| Manual review (1 day) | [N] | [e.g., Renewal date backfill for [N] accounts] |
| Integration fix (1+ week) | [N] | [e.g., Health score sync not firing for SMB] |

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CRM ✓ live | CS Platform ✓ live | user-provided export — [date] | conversation context only]
> - **Required fields audited:** [Configured in cs-ops CLAUDE.md | User-provided this session]
> - **Staleness threshold applied:** [Configured threshold from cs-ops CLAUDE.md — [N] days | Default 30 days — not formally configured]
> - **Consistency checks applied:** [N] rules — see consistency audit section
> - **Accounts excluded:** [N] accounts with no ARR — excluded from ARR-impact calculations; included in field count
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before acting on remediation backlog:** Assign ownership — data quality issues not assigned to a named owner are not fixed.

---

## Output

Data quality audit report — format driven by `--quick` (default) or `--full` flag.
Produces a structured markdown report with: coverage summary table, field-level
completeness scores, data gap inventory, and prioritised remediation actions.
See **Full data quality audit** section for field-level detail.

## Guardrails

**Missing data is not neutral.** An account missing a required field is
excluded from any analysis that requires that field. This is not a minor
hygiene issue — it is a coverage blindspot that affects every downstream
report and plan. Quantify the ARR impact of every data gap before reporting.

**Staleness thresholds are configured — do not invent them.** If no threshold
is configured, flag the gap and recommend one; do not apply an arbitrary
default without surfacing it. The staleness section must state which threshold
was applied.

**Consistency violations may be legitimate.** A segment mismatch may reflect
a manual override (e.g., a high-touch account below the standard ARR floor
due to strategic importance). Flag it; do not auto-correct. Corrections require
CS lead judgment.

**Orphaned records are not always errors.** Some orphaned accounts may be
legacy records from prior CRM migrations or churned accounts awaiting formal
close. Investigate before assigning — do not mass-assign CSMs to accounts
that may be inactive.

**Remediation backlog requires ownership.** The backlog output is a starting
point. Each item must be assigned to a named owner with a due date before
any improvement occurs. A data quality audit without assigned remediation
produces a document, not a fix.

**Data quality is a shared responsibility.** CRM hygiene involves CS,
CS Ops, RevOps, and CRM admins. Recommendations that require CRM workflow
changes or integration fixes belong to RevOps or CRM admin — flag the owner
clearly rather than implying CS Ops can resolve everything unilaterally.

---

## After the audit

- "Data gaps confirmed — fix orphaned accounts before next reporting cycle: `/cs-ops:capacity-planner`"
- "Health score staleness identified — review the health model's reliability: `/cs-ops:health-model-review`"
- "Segment mismatches found — run reclassification queue: `/cs-ops:segment-analyzer --reclassification`"
- "Remediation complete — regenerate the metrics dashboard with clean data: `/cs-ops:metric-dashboard`"
- "Staleness is a recurring pattern — build a data quality standard: `/cs-ops:process-doc --data-quality`"
