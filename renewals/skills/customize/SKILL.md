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
deployment_target: plugin
---

# /renewals:customize [VALIDATED]

Update specific sections of your renewals practice profile without re-running the
full interview.

---

## Use when
- A specific configuration field has changed and the rest of the profile is accurate (discount authority updated, new AE partner, revised GRR/NRR targets, escalation contact change)
- A single section needs a targeted rebuild without touching other sections
- You want to audit the full profile for missing fields, `[PLACEHOLDER]` markers, or internal consistency issues (`--validate` mode)
- Cold-start left incomplete sections and you are filling them in post-setup

## Do NOT use for
- First-time configuration or complete profile rebuilds — use `/renewals:cold-start-interview`
- Updates spanning 3 or more sections simultaneously — cold-start has lower error surface for bulk configuration
- Any operational renewals task (risk assessment, contract review, forecast) — this skill edits config only
- Verifying integration connectivity — use `/renewals:cold-start-interview --check-integrations`

## Typical activation
> `/renewals:customize --section discount-authority` — update a single config section directly
> `/renewals:customize --validate` — audit the full profile for missing fields and consistency issues before a renewal motion
> `/renewals:customize` — prompted section selection when no section argument is provided

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of profile customization request is this?
   - **Single-Field Update**: One field changed (new AE partner, revised discount ceiling, updated GRR target). Rest of profile is accurate — targeted edit with downstream trace.
   - **Section Rebuild**: Multiple fields within one section need updating (new escalation matrix, full pricing restructure, team turnover). Treat the section as a unit — validate internal consistency across all fields.
   - **Validation Audit**: User runs `--validate` or asks what's missing. Diagnostic only — no edits. Run structural completeness AND logical consistency checks.
   - **Post-Cold-Start Completion**: Cold-start left placeholders or incomplete sections. Sequence completions by downstream dependency, not file order.

2. **CONSTRAINTS**: What limits the solution space?
   - G1 (Read before write): Always display current field values before collecting new input — config fields drive financial decisions and an incorrect silent overwrite is worse than a missing field.
   - G2 (Confirm before writing): Present a diff-style summary and require explicit confirmation — never auto-write, even for single-field changes.
   - G4 (Section isolation): Writing one section must not alter any other section. If the write mechanism can't guarantee isolation, abort and alert.
   - G5 (No speculative values): Never infer or suggest field values without user confirmation — "your discount authority is probably around X%" is prohibited.
   - G7 (Three-section threshold): If 3+ sections need updating, route to `/renewals:cold-start-interview` — customize is a scalpel, not a rebuild tool.

3. **EXPERT CHECK**: What would a veteran renewal operations lead verify first?
   - Does the changed field create a cross-field consistency violation? Run the four checks: GRR/NRR inversion, discount floor vs. anchor, escalation SLA vs. renewal window, strategic threshold vs. deal size.
   - Which downstream skills consume this field? Surface affected skills in the confirmation output so the user knows what to re-run.
   - If multiple placeholders exist, are they being resolved in dependency order (company → team → targets → escalation → rest)?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - ❌ Writing an update without tracing downstream skill impact — user acts on stale skill output without realizing a config change invalidated it.
   - ❌ Updating one field in a section while leaving related fields stale — partial section updates create internal contradictions.
   - ❌ Running validate mode and reporting only missing fields without checking logical consistency (GRR < NRR, threshold math).
   - ❌ Collecting all field values at once instead of field-by-field — increases error rate on structured values like escalation contacts.
   - ❌ Accepting a value in a format downstream skills don't expect (e.g., "about ten percent" instead of "10%") without normalizing against field definitions.
   - ❌ Routing a user through customize when 3+ sections need work — cold-start-interview has lower error surface for bulk configuration.

**After execution**, verify:
- Were current values displayed before every edit and confirmation obtained before every write?
- Were cross-field consistency checks run for any change to `targets`, `discount-authority`, or `pricing`?
- Were downstream skill implications surfaced in the confirmation output?
- Confidence: [High] if field has clear schema and unambiguous value / [Medium] if downstream consistency implications not yet validated / [Low] if target field is ambiguous or value seems inconsistent with other configured fields.


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

---

## Security & Permissions

```
network:        none — no external API calls or web fetch
read_scope:     ~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md
                ~/.claude/plugins/config/claude-for-customer-success/company-profile.md
write_scope:    ~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md
                ~/.claude/plugins/config/claude-for-customer-success/company-profile.md
subprocess:     none
dynamic_code:   none — no eval, no exec, no runtime code execution
```

This skill reads and writes exclusively within the plugin config directory. No account data, contract content, or customer PII is written to configuration. All written values are practitioner-provided descriptions, thresholds, and contact information — not customer records.

---

## Trust & Verification

**Read before write:**
Current field values are displayed before any new input is collected. Silent overwrites are prohibited. This applies in all modes: `--edit` (default), `--section`, and post-cold-start completion flows.

**Confirm before write:**
A diff-style summary of all changes is presented and explicit "yes" confirmation is required before any file write. "No" discards changes without writing. "Edit" returns to field collection. Auto-write is never permitted — this confirmation step is non-skippable.

**Section isolation:**
Writing to one section of a config file must not alter any other section. If the file write cannot guarantee section isolation, the operation is aborted and the user is alerted before any write occurs.

**No speculative field values:**
This skill never infers, suggests, or pre-populates field values without user confirmation. Config fields drive financial decisions — an incorrect value entered silently is worse than a missing one.

**Downstream impact transparency:**
After every successful write, skills affected by the changed field are surfaced so the user knows which operational skills to re-run before the next renewal motion.

---

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
