# DVT-1: Inter-Skill Contract Validation Report

**Report date:** 2026-05-18  
**Validator:** Agent-Architect (automated validation pass)  
**Contract:** `csm:expansion-business-case [mode=csql]` → `rev-ops:csql-tracking [operation=create]`  
**Producer version:** expansion-business-case v1.0.0 [PROPOSED]  
**Consumer version:** csql-tracking v1.0.0 [VALIDATED]  
**Status:** VALIDATED — all gaps resolved; re-validated 2026-05-18

---

## Scope

This validation confirms that the output schema of `csm:expansion-business-case` in
`csql` mode aligns with the input contract of `rev-ops:csql-tracking` at the `create`
operation. The authoritative contract specification is the **Inter-Skill Contract**
section of `rev-ops/skills/csql-tracking/SKILL.md` (lines 389–414).

---

## Field Mapping Verification

The consumer defines the following field mapping (csql-tracking SKILL.md, Inter-Skill
Contract section):

| Producer field               | Consumer parameter   | Required | Verified |
|------------------------------|---------------------|----------|----------|
| `Account` header field       | `account_name`      | Yes (non-empty) | ✅ |
| `Prepared by` CSM name       | `csm_name`          | Yes (non-empty) | ⚠️ GAP |
| Full package document        | `csql_package`      | Yes (non-empty) | ✅ |
| `Proposed expansion` line    | `expansion_product` | Yes (non-empty) | ✅ |
| `Estimated expansion value`  | `expansion_amount`  | No (optional)   | ✅ |
| `Handoff to` AE field        | `ae_owner`          | No (optional)   | ⚠️ MINOR |

### Verification details

**`account_name` ← `Account` header field**  
- Template: `**Account:** [Account Name]` (csql-package-template.md line 19)
- Producer parameter: `account_name` — required, non-empty string (expansion-business-case SKILL.md line 79)
- Result: ✅ Field name matches; non-empty guaranteed by required parameter contract.

**`csm_name` ← `Prepared by` CSM name**  
- Template: `**Prepared by:** [CSM Name] | [Date]` (csql-package-template.md line 20)
- Producer parameter: No `csm_name` parameter exists in expansion-business-case parameter list
- Result: ⚠️ **GAP — no source parameter defined for `[CSM Name]` in the producer.** Template placeholder has no documented resolution path. csql-tracking requires this field non-empty at `create`. See Gap Analysis below.

**`csql_package` ← Full package document**  
- The complete rendered CSQL package document is stored verbatim by csql-tracking.
- If Phase 6 POST-EXECUTION completes without error, the document is always non-empty.
- Result: ✅ Non-empty guaranteed on successful generation.

**`expansion_product` ← `Proposed expansion` line**  
- Template: `**Proposed expansion:** [Expansion Product — specific name, tier, or capability]`
- Producer parameter: `expansion_product` — required, non-empty string (line 80); additionally guarded by E-2 expert check for specificity
- Result: ✅ Field name matches; non-empty guaranteed by required parameter + E-2 guard.

**`expansion_amount` ← `Estimated expansion value`**  
- Template: `**Estimated expansion value:** [Budget range or "TBD — AE to confirm"]`
- Producer parameter: `expansion_amount` — optional string (line 85); omitted from template if absent per Default #4
- Result: ✅ Optional on both sides; consistent omission behavior.

**`ae_owner` ← `Handoff to` AE field**  
- Template: `**Handoff to:** [AE Name or "Assign AE"]`
- Consumer default: `[Unassigned]` when field absent or empty
- Producer template default text: "Assign AE"
- Result: ⚠️ **MINOR** — sentinel value mismatch. Producer uses "Assign AE"; consumer defaults to `[Unassigned]`. When no AE is specified, the csql-tracking record will store "Assign AE" as `ae_owner` rather than `[Unassigned]`. Functional behavior is equivalent (both signal unassigned state) but string values differ. Documented as G-1 in OQ-4.

---

## Gap Analysis

### G-1 (BLOCKING): `csm_name` has no source parameter in producer

**Description:** The csql-package-template.md contains the placeholder `[CSM Name]` in
the `**Prepared by:**` header. The csql-tracking consumer maps this to `csm_name` and
requires it non-empty at `create`. However, `expansion-business-case` has no parameter
named `csm_name` (or equivalent) in its parameter specification.

**Impact:** At template population time, `[CSM Name]` has no defined resolution path.
Three failure modes exist:
1. Placeholder left literal → csql-tracking `create` operation receives "[CSM Name]" as `csm_name` — technically non-empty but semantically invalid
2. Field resolved from implicit session context → depends on runtime CSM identity being available; no documented mechanism
3. Field silently omitted → csql-tracking `create` operation fails with "required field missing" error

**Note:** OQ-4 in expansion-business-case (line 753) records that a contract validation
was performed on 2026-05-17, but this gap was not captured. G-1 references only the
`ae_owner` sentinel mismatch, not the `csm_name` source gap. This gap is newly identified
in this validation pass.

**Remediation options:**

| Option | Description | Recommendation |
|--------|-------------|----------------|
| A | Add `csm_name` as explicit required parameter to expansion-business-case | ✅ Preferred — self-documenting, consistent with other required fields |
| B | Document resolution from implicit session context (authenticated CSM identity) | Fragile — depends on unspecified runtime mechanism |
| C | Mark `csm_name` optional in producer with fallback `[CSM — confirm]`; document as MVP gap | Acceptable for MVP if Option A deferred; weakens non-empty guarantee |

**Recommended action:** Apply Option A — add `csm_name` as a required `string` parameter
to expansion-business-case, populate `[CSM Name]` from `safe_csm_name` (escaped).
Requires SKILL.md update + re-validation.

### G-2 (MINOR): `ae_owner` sentinel value mismatch

**Description:** When no AE is specified, the csql-package-template.md fallback text is
"Assign AE". csql-tracking stores this verbatim as `ae_owner`. The csql-tracking skill
documents its own default as `[Unassigned]`, but this default only applies when the field
is absent — not when the template provides a non-empty string.

**Impact:** `ae_owner` in csql-tracking records created via this handoff will contain
"Assign AE" rather than `[Unassigned]`. Query filters on `ae_owner` looking for
`[Unassigned]` will miss these records.

**Remediation:** Align sentinel values. Either:
- Update csql-package-template.md to use `[Unassigned]` as the default text, OR
- Update csql-tracking to accept "Assign AE" as an equivalent unassigned sentinel in query filter logic

Recommend updating csql-package-template.md (simpler, fewer downstream effects).

---

## Required Fields — Non-Empty Guarantee Summary

| Field | Guaranteed non-empty | Mechanism |
|-------|---------------------|-----------|
| `account_name` | ✅ Yes | Required parameter in producer |
| `csm_name` | ⚠️ No | **No source parameter — G-1** |
| `csql_package` | ✅ Yes | Full rendered document; always non-empty on success |
| `expansion_product` | ✅ Yes | Required parameter + E-2 expert check |

---

## Verdict

**CONDITIONAL PASS**

The inter-skill contract is structurally sound on four of five required field mappings.
All five header field names align exactly between the producer template and the consumer
field mapping table. The contract cannot be marked VALIDATED until G-1 is resolved.

| Check | Result |
|-------|--------|
| All 5 header field names match | ✅ |
| `account_name` non-empty guaranteed | ✅ |
| `csm_name` non-empty guaranteed | ⚠️ GAP (G-1) |
| `csql_package` non-empty guaranteed | ✅ |
| `expansion_product` non-empty guaranteed | ✅ |
| `expansion_amount` optional on both sides | ✅ |
| `ae_owner` optional on both sides | ✅ |
| `ae_owner` sentinel alignment | ⚠️ MINOR (G-2) |

---

## Required Actions Before VALIDATED

1. **G-1 remediation (BLOCKING):** Add `csm_name` as required parameter to
   `expansion-business-case` SKILL.md. Update Phase 1 CLASSIFY Step 3 to escape it
   (`safe_csm_name`), Phase 2 PRE-FLIGHT to scan it, and template population to use it.
   Then re-run DVT-1.

2. **G-2 remediation (MINOR, recommended):** Align `ae_owner` sentinel value. Update
   `csql-package-template.md` `**Handoff to:**` fallback from "Assign AE" to
   `[Unassigned]`.

3. **OQ-4 update:** Update expansion-business-case OQ-4 to reference this report and
   document G-1 (new finding) alongside existing G-1 (ae_owner — now renamed G-2 in this
   report for clarity).

---

## Files Inspected

- `rev-ops/skills/csql-tracking/SKILL.md` — Inter-Skill Contract section (lines 389–414)
- `csm/skills/expansion-business-case/SKILL.md` — full file (660 lines)
- `csm/skills/expansion-business-case/reference/csql-package-template.md` — full file (110 lines)

---

## Re-validation Run: 2026-05-18

**Re-run trigger:** G-1 (BLOCKING) and G-2 (MINOR) patches applied.
**Validator:** Agent-Architect re-run

### G-1 Verification

**PASS** — All four required patch elements confirmed present in `expansion-business-case/SKILL.md`:

1. `csm_name` declared as required `string` parameter — line 79: `| 'csm_name' | 'string' | Yes | CSM name for document attribution (used in CSQL package header via 'safe_csm_name')`
2. `safe_csm_name = xml_structural_escape(csm_name)` present in CLASSIFY Phase 1 Step 3 — line 154
3. `safe_csm_name` included in `inputs_to_scan` list in PRE-FLIGHT Phase 2 Step 2 — line 233 (index 3 of the scan list)
4. Resolution path for `[CSM Name]` placeholder in csql-package-template.md confirmed via `safe_csm_name`; OQ-4 (line 755) documents the mapping explicitly

Non-empty guarantee is now in force: `csm_name` is a required parameter; empty string would fail parameter validation before reaching template population.

### G-2 Verification

**PASS** — `csql-package-template.md` line 20 now reads:

```
**Handoff to:** [AE Name or "[Unassigned]"]
```

Sentinel `[Unassigned]` matches the csql-tracking filter token exactly. Prior version read `"Assign AE"`. Mismatch eliminated.

### Full Field Pass

| csql-tracking required field | Producer source | Non-empty guarantee | Result |
|------------------------------|----------------|---------------------|--------|
| `account_name` | `account_name` parameter (required); escaped to `display_account`; maps to `**Account:**` header | Required parameter contract | ✅ PASS |
| `csm_name` | `csm_name` parameter (required); escaped to `safe_csm_name`; maps to `**Prepared by:**` header | Required parameter contract (G-1 fix) | ✅ PASS |
| `expansion_product` | `expansion_product` parameter (required); E-2 expert check enforces specificity | Required parameter + E-2 guard | ✅ PASS |
| `ae_owner` | `ae_owner` optional parameter; sentinel `[Unassigned]` aligned in template (G-2 fix) | Optional on both sides; sentinel aligned | ✅ PASS |
| `champion` | `csql_context.champion` (optional in csql-tracking); maps to MEDDIC Champion row; template provides "Identify — confirm with AE" framing when absent | Optional on both sides; documented fallback | ✅ PASS |

### Final Status: VALIDATED

All previously identified gaps are resolved:
- G-1 (BLOCKING): `csm_name` parameter added, escaped, scanned, and mapped — non-empty guarantee in force
- G-2 (MINOR): `ae_owner` sentinel aligned to `[Unassigned]` — query filter consistency restored

No new gaps identified in this re-validation pass. The inter-skill contract between `csm:expansion-business-case [mode=csql]` and `rev-ops:csql-tracking [operation=create]` is fully validated across all required fields.

**Updated report status:** VALIDATED — all gaps resolved; re-validated 2026-05-18
