---
name: customize
description: >
  Update your renewals practice profile — edit any section of the renewals
  CLAUDE.md or company-profile.md without rerunning the full cold-start
  interview. Use when a specific field has changed (discount authority updated,
  new escalation matrix, pricing model revision, new AE partner, churn signal
  added) or when you want to extend a section that was left incomplete during
  cold-start. Displays current values before editing and confirms changes before
  writing. Use /renewals:cold-start-interview for first-time setup or a complete
  profile rebuild.
argument-hint: "[--section <section-name>] [--show | --edit | --validate]"
version: "1.0.0"
config_skill: true
---

# /renewals:customize

Update specific sections of your renewals practice profile without re-running the
full interview.

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — No domain guardrails apply — this skill configures the environment rather than generating outputs.
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?


## This Skill vs. Cold-Start Interview

**`/renewals:cold-start-interview`** — Use for first-time configuration, complete
profile rebuilds, or when more than half the profile needs updating. Runs the full
interview section by section and writes all fields.

**`/renewals:customize`** — Use when a specific field has changed and the rest of the
profile is accurate. Targets a single section; reads current values first; confirms
before writing.

---

## Mode

`--show`: Display the current value of a section or field without editing.
Use to audit what's configured before a renewal motion.

`--edit` (default): Display current value, collect new value, confirm, then write.

`--validate`: Check the current profile for missing fields, `[PLACEHOLDER]` markers,
and internal consistency issues (e.g., discount authority floor higher than anchor,
NRR target below GRR target, escalation matrix contacts missing). Does not edit —
surfaces what needs attention.

---

## Sections available for update

The following sections map directly to blocks in the renewals CLAUDE.md and
company-profile.md. Each section can be updated independently.

| Section name | What it controls | Skills affected |
|-------------|-----------------|----------------|
| `pricing` | Pricing model, tier structure, standard increase %, multi-year incentive | negotiation-prep, price-increase-prep |
| `discount-authority` | Discount authority ceiling, approval chain, approval method | negotiation-prep |
| `targets` | GRR target, NRR target, segment-level targets | renewal-forecast, expansion-signal |
| `escalation` | Escalation matrix — Head of CS, CRO, CEO contacts, SLA by risk tier | risk-assessment, executive-summary |
| `churn-signals` | Primary churn drivers, competitive threats, health score thresholds | risk-assessment, churn-analysis |
| `team` | AE partner, CSM name, Head of CS contact | negotiation-prep, price-increase-prep, expansion-signal |
| `segments` | Customer segments, average deal size, strategic account threshold | executive-summary, expansion-signal |
| `contracts` | Standard contract terms, standard payment terms, price protection baseline | contract-review, price-increase-prep |
| `negotiation-posture` | Consultative / direct / data-led / segment-dependent framing | negotiation-prep, price-increase-prep |
| `company` | Company name, brand name, product name, customer-facing language | All skills (used in output headers) |

---

## Execution protocol

### Step 1 — Identify the target section

If `--section` argument is provided, go directly to that section.

If no section is specified, ask:
> "Which section of your renewals profile do you want to update? Options:
> pricing, discount-authority, targets, escalation, churn-signals, team,
> segments, contracts, negotiation-posture, or company.
>
> Or use `--validate` to see what's missing or outdated across the full profile."

### Step 2 — Show current values

Read the current value from the config file before asking for new input.

> "Here's what's currently configured for **[section]**:"
>
> [Display current field values, formatted as a readable list. If any field contains
> `[PLACEHOLDER]`, flag it: ⚠️ This field was never completed.]

If the file doesn't exist:
> "The renewals config file doesn't exist yet. Run `/renewals:cold-start-interview`
> to build the full profile from scratch — `customize` updates an existing profile."

### Step 3 — Collect new values

For each field in the section, present the current value and ask for the updated value.

> "Current value: [value]
> New value (press Enter to keep current):"

Accept user input field by field. For fields with structured values (e.g., escalation
matrix with multiple contacts), collect each contact separately.

Do not ask for all fields at once — work through them in sequence, one question per
interaction.

### Step 4 — Confirm before writing

Before writing any changes, display a summary of what will change:

> "Here's what I'm about to update:
>
> | Field | Old value | New value |
> |-------|----------|-----------|
> | [field] | [old] | [new] |
>
> Write these changes? (yes / no / edit)"

If the user selects "edit", return to Step 3 for the affected field.
If "no", discard changes and confirm no file was modified.
If "yes", proceed to Step 5.

### Step 5 — Write changes

Write the updated values to the appropriate config file:
- Pricing, discount-authority, targets, escalation, churn-signals, team, segments,
  contracts, negotiation-posture: → `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
- Company: → `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

Preserve all other sections exactly as they are — only modify the target section.
Do not reformat, reorder, or restructure fields outside the target section.

### Step 6 — Confirm write and surface downstream implications

After writing:
> "Updated. The **[section]** section is now current as of [date].
>
> [If applicable: downstream implications:]
> - [e.g., 'Your new discount authority ceiling affects the negotiation-prep brief
>   — run a new brief before your next renewal call']
> - [e.g., 'The updated escalation matrix will be used by risk-assessment for
>   all future escalation routing']"

---

## Validate mode (`--validate`)

Scan both config files for:

### Missing or incomplete fields

| Check | Status | Action |
|-------|--------|--------|
| Company name | ✅ / ⚠️ [PLACEHOLDER] | `--section company` |
| Pricing model | ✅ / ⚠️ [PLACEHOLDER] | `--section pricing` |
| Discount authority ceiling | ✅ / ⚠️ not set | `--section discount-authority` |
| GRR target | ✅ / ⚠️ not set | `--section targets` |
| NRR target | ✅ / ⚠️ not set | `--section targets` |
| Escalation matrix — Head of CS | ✅ / ⚠️ [PLACEHOLDER] | `--section escalation` |
| Escalation matrix — CRO | ✅ / ⚠️ not set | `--section escalation` |
| Churn signals configured | ✅ / ⚠️ none defined | `--section churn-signals` |
| AE partner | ✅ / ⚠️ not set | `--section team` |
| Standard contract terms | ✅ / ⚠️ [PLACEHOLDER] | `--section contracts` |

### Internal consistency checks

Check for logical inconsistencies that would produce unreliable skill output:

- **GRR/NRR inversion**: NRR target below GRR target is mathematically impossible
  (NRR includes GRR plus expansion). Flag if NRR ≤ GRR.
  > "⚠️ NRR target ([N]%) is at or below GRR target ([N]%). NRR must exceed GRR —
  > NRR includes all expansion revenue. Update `--section targets`."

- **Discount authority floor above full-price anchor**: If the discount authority
  ceiling produces a floor above the full-price anchor, the walk-away is above the
  ask — which is not actionable.
  > "⚠️ Discount authority configuration produces an illogical walk-away floor.
  > Review `--section discount-authority`."

- **Escalation SLA longer than renewal window**: If the risk-escalation SLA for
  Critical accounts is longer than the typical renewal runway for the segment,
  escalation will always be late. Flag if SLA > 30 days for Critical tier.

- **Strategic account threshold gap**: If the strategic account threshold in `segments`
  is below the average deal size, most accounts would qualify as strategic — which
  defeats the threshold. Flag if threshold < average deal size.

### Validate output

> "**Profile validation — [date]**
>
> **Missing or incomplete:** [N fields] — [list by section]
> **Consistency issues:** [N] — [list by check]
> **Fully configured:** [N fields]
>
> Recommended: update [section 1], then [section 2] to close the gaps that affect
> your highest-priority skills."

If the profile is clean:
> "Profile is complete and internally consistent as of [date]. No missing fields
> or consistency issues detected."

---

## Section reference — field definitions

Use these definitions when collecting new values to ensure the field is entered in the
format the downstream skills expect.

### `pricing` section

- **Pricing model**: `per-seat` / `usage-based` / `flat-fee` / `tiered` / `hybrid`
- **Tier structure**: Named tiers and price points (e.g., Starter $X/seat, Professional
  $Y/seat, Enterprise custom)
- **Standard price increase**: `[N]% annually` / `CPI + [N]%` / `market-rate review`
  / `no standard increase`
- **Multi-year incentive**: What discount applies for 2-year or 3-year commitments
  (used in negotiation-prep scenario modeling)

### `discount-authority` section

- **Authority ceiling**: Maximum % discount CSM can approve without escalation
- **Approval chain**: [Title] → [Title] → [Title] (escalation order)
- **Approval method**: Email / Slack / Formal approval system (how to request approval)
- **Turnaround SLA**: How quickly approvals are expected to come back

### `targets` section

- **GRR target**: Company or team GRR target as % (e.g., 92%)
- **NRR target**: Company or team NRR target as % (e.g., 110%)
- **Segment targets**: If different targets apply by segment, list segment name and target
- **Measurement period**: Annual / quarterly

### `escalation` section

- **Head of CS**: Name, title, contact method
- **CRO**: Name, title, contact method
- **CEO**: Name, title, contact method (for board-level escalations)
- **Escalation SLA by tier**:
  - Critical: [N] business days after tier assigned
  - High: [N] business days after tier assigned
  - Medium: [N] days — monitor only
  - Low: no escalation

### `churn-signals` section

- **Primary churn drivers**: List your top 3–5 historical churn causes (drives
  risk-assessment domain weighting and churn-analysis root cause matching)
- **Competitive threats**: Known competitors with displacement patterns; any known
  pricing or positioning context
- **Health score thresholds**: Score at which an account is flagged as at-risk in
  your CS platform (if applicable)

### `team` section

- **CSM name**: The CSM using the plugin (appears in output attribution)
- **AE partner**: Name and contact for AE co-ownership on expansion and strategic accounts
- **Head of CS**: Name — should match escalation section

### `segments` section

- **Segment names**: List your customer segments (e.g., SMB, Mid-Market, Enterprise)
- **Average deal size by segment**: Used for calibration, not as a hard threshold
- **Strategic account threshold**: ARR floor above which an account qualifies for
  executive summary and escalated renewal motion

### `contracts` section

- **Standard payment terms**: Net 30 / Net 45 / Net 60 / invoiced annually in advance
- **Standard price protection**: None / CPI cap / N-year rate lock (for flagging deviations)
- **Standard termination notice**: [N] days (to flag contracts with shorter windows)
- **Standard data deletion**: [N] days post-termination (for SLA compliance)

### `negotiation-posture` section

- **Default posture**: `consultative` / `direct` / `data-led`
- **Segment-specific overrides**: [Segment] → [posture] (if different segments warrant
  different approaches)

### `company` section

- **Company name**: Legal or trading name (used in output headers and customer-facing exports)
- **Brand name**: Customer-facing brand if different from legal name
- **Product name**: Primary product name used in customer communications

---

## Output format — Edit mode

---

**Profile Update — [Section]**
*Updated: [date]*

| Field | Updated value |
|-------|--------------|
| [field 1] | [new value] |
| [field 2] | [new value] |

**Downstream skills affected:** [list]

**Next recommended action:** [e.g., "Run `/renewals:renewal-forecast` to see updated
NRR projections with new targets" / "No further action required"]

---

> [review before sending]

## Guardrails

**Read before write.** Always display current field values before collecting new input.
Never overwrite without showing what will be replaced.

**Confirm before writing.** Always present a diff-style summary of changes and require
explicit confirmation before writing to any config file.

**Preserve untouched sections.** Writing to one section of the config file must not
alter any other section. If the file write cannot guarantee section isolation, abort
and alert the user before proceeding.

**Validate does not edit.** `--validate` mode is read-only. It reports issues; it does
not fix them. Run `--edit` to fix what validate surfaces.

**Cold-start for full rebuilds.** If more than 3 sections are incomplete or the user
wants to reconfigure the full profile, route to `/renewals:cold-start-interview`.
Customize is a targeted update tool, not a full configuration workflow.

**No speculative field values.** Do not infer or suggest field values (e.g., "your
discount authority is probably around X%") without the user confirming. Config fields
drive financial decisions — an incorrect value entered silently is worse than a missing
one.

**Downstream impact transparency.** After any edit, surface which skills are affected
by the changed field so the user knows what to re-run before the next renewal motion.
