# CSE Evaluation Report: renewals:churn-rca

**Spec ID:** EVAL-20260517-renewals-churn-rca  
**Mode:** Evaluator  
**Input Artifact:** DS-20260517-renewals-churn-rca (DVT-8)  
**Evaluated:** 2026-05-17  
**Evaluator:** critical-skill-evaluator v1.5.0  
**Stream:** B-β  
**Linear Issue:** DVT-8  

EVAL-MARKER-DVT8-OSCAR-7714-DELTA

---

## Verdict

**3 BLOCKs | 4 WARNs | 4 NOTEs**

**BLOCKED — do not proceed to build until all 3 BLOCKs are resolved.** The DS contains a direct behavioral contract conflict between §1 and §3.1b (BLOCK-03), and two missing error message specifications that would leave the builder with undefined behavior at critical failure paths (BLOCK-01, BLOCK-02). These are design gaps that cannot be resolved during build; they require DS revision.

---

## Findings

### BLOCKs (3)

**BLOCK-01 — `portfolio_size = 0` division-by-zero: validation declared but error message unspecified [Security/Quality]**

- **Location:** §10 Trust & Verification — `portfolio_size validated as positive integer; zero or negative values rejected with clear error`; §3.1b systemic threshold calculation: `churn_rate = len(accounts) / portfolio_size × 100`
- **Evidence:** §10 asserts that `portfolio_size` is validated against zero and negative values. However, NO error message text is specified anywhere in the DS for this validation failure. The builder has no contract to implement against. Additionally, the `portfolio_size` field appears only in the cohort `rca` operation inputs table (§3.1b) without a documented default value or behavior when omitted — a `portfolio_size = 0` or absent `portfolio_size` would cause division by zero in `churn_rate` calculation without a guard clause specification.
- **Required fix:** Specify the exact error message for `portfolio_size` validation failure — e.g., `Validation error: portfolio_size must be a positive integer. Received: [value].` — in the DS (§3.1b or §10). Also clarify whether `portfolio_size` is required or optional, and what happens if omitted (default behavior or rejection).

**BLOCK-02 — `export` operation: not-found error declared but message unspecified [Security/Quality]**

- **Location:** §10 Trust & Verification — `rca_id resolution for export uses file scan against context/churn-rca-*; if not found, returns clear not-found error`
- **Evidence:** §10 states the `export` operation returns "a clear not-found error" when the target `rca_id` cannot be resolved to a file. No error message text is specified anywhere in the DS. The `export` operation specification in §3.2 does not define error handling at all — only the happy path (successful export) is described. The builder has no contract for the failure path.
- **Required fix:** Add error message specification for `export` not-found failure — e.g., `Error: No churn RCA found for rca_id [value]. Verify the ID and check context/churn-rca-* files.` — in §3.2 or §10. Align with the not-found error patterns used in sibling skills (DVT-7 uses `Immutable field error: [field_name] cannot be modified...`; DVT-9 uses `Error: No communication plan found for [csm_name]...`).

**BLOCK-03 — Systemic threshold definition: §1 vs §3.1b direct conflict [Architecture/Quality]**

- **Location:** §1 — "systemic escalation triggers at ≥25% churn rate OR ≥3 accounts in cohort"; §3.1b — `systemic_threshold_met = churn_rate >= 25.0` ONLY
- **Evidence:** §1 states two independent conditions trigger systemic escalation: (1) churn_rate ≥ 25% OR (2) ≥3 accounts in the cohort. §3.1b defines the calculation as `churn_rate >= 25.0` only. The "≥3 accounts" condition appears only as a MINIMUM cohort size requirement (hard reject if < 3 accounts), not as an additional systemic trigger. These two specifications directly contradict each other. A builder reading §3.1b would implement churn_rate-only threshold; a builder reading §1 would implement OR logic. The behavior for a 3-account cohort with churn_rate = 10% is undefined.
- **Required fix:** Choose one of two resolutions and update both §1 and §3.1b to be consistent:
  - **Option A (recommended):** Remove "OR ≥3 accounts in cohort" from §1. Systemic threshold = `churn_rate >= 25.0` only. The 3-account minimum is a cohort size gate, not a systemic trigger.
  - **Option B:** Add the OR condition to §3.1b explicitly: `systemic_threshold_met = (churn_rate >= 25.0) OR (len(accounts) >= 3)`. Update the systemic escalation output section to describe behavior when only the account-count condition triggers (low churn_rate but ≥3 accounts in cohort).

---

### WARNs (4)

**W-1 — No Reasoning Protocol section [Architecture]**

- **Location:** DS document — section list
- **Evidence:** Both `rca` operations (individual and cohort) involve multi-stage inference: churn signal classification, value chain failure mapping, win-back prioritization, and cohort theme identification. No `## Reasoning Protocol` section exists. Per CSE v1.5.0, missing reasoning protocol = automatic BLOCK in gate mode; WARN in evaluator mode.
- **Recommendation:** Add `## Reasoning Protocol` to SKILL.md at build time covering: (1) individual mode — signal classification → failure map → remedy prioritization, (2) cohort mode — per-account classification → theme extraction → systemic threshold evaluation → escalation output.

**W-2 — Cohort `safe_cohort_name` derivation: source field not defined [Quality]**

- **Location:** §5.1 naming pattern — cohort file: `context/churn-rca-cohort-[safe_cohort_name]-[YYYY-MM-DD].md`
- **Evidence:** The cohort file naming pattern uses `safe_cohort_name` but no input field named `cohort_name` exists in the cohort `rca` inputs table (§3.1b). The inputs include `accounts` (list), `portfolio_size`, `reporting_period`, `cohort_identifier` (optional), and `notes`. The `cohort_identifier` field is optional. The DS does not specify what `safe_cohort_name` is derived from when `cohort_identifier` is not provided.
- **Recommendation:** Define `safe_cohort_name` derivation explicitly: when `cohort_identifier` is provided, derive from it; when absent, generate a fallback (e.g., `cohort-[YYYYMMDD]` or `cohort-[first-account-safe-name]`).

**W-3 — Downgrade scope note vs DVT-7 churn redirect asymmetry [Ecosystem]**

- **Location:** §9 Inter-Skill Contract — "Sibling: `renewals:downgrade-analysis` (DVT-7)"
- **Evidence:** DVT-7 specifies a hard redirect when full churn is detected: `Scope redirect: This request describes full contract cancellation, not a downgrade. Please use renewals:churn-rca for churn analysis.` DVT-8 specifies only a soft scope note: `Scope note: The described scenario may be a downgrade rather than a full churn event. Consider using renewals:downgrade-analysis if the customer intends to reduce rather than cancel.` The asymmetry (hard redirect vs soft note) is documented but inconsistent in UX. A user who accidentally runs churn-rca for a downgrade gets a suggestion; a user who accidentally runs downgrade-analysis for a churn gets a hard stop.
- **Recommendation:** Document the asymmetry rationale in §9 or accept that churn-rca is the more permissive entry point. The current behavior is defensible (churn-rca can analyze downgrades as data; downgrade-analysis cannot analyze full cancellations without scope expansion) but should be explicitly rationalized.

**W-4 — Export operation: no pagination or size limit on output [Architecture]**

- **Location:** §3.2 export operation
- **Evidence:** The `export` operation returns the full RCA content. For cohort RCAs covering many accounts (no documented maximum), the output could be very large. The DS specifies no truncation, pagination, or size-limit behavior. This is particularly relevant for org-rollup-level exports (if DVT-11 integration is ever implemented).
- **Recommendation:** Add a note to §3.2 specifying that export output is unbounded in v1 (acceptable for plugin use where output is delivered to the user's session), or add an advisory output size limit and truncation behavior.

---

### NOTEs (4)

**N-1 — `ocy_snapshot` field name inconsistency (individual mode only) [Quality]**

- **Location:** §3.1a inputs table (row: `ocy_snapshot`)
- **Evidence:** Individual `rca` mode accepts `ocy_snapshot` — likely a typo for `ocv_snapshot` consistent with DVT-7. Cohort mode does not include an OCV snapshot input at all. The inconsistency is the same as found in DVT-7; the resolution decision should be coordinated across both skills.
- **Impact:** Low — naming quirk only; no behavioral impact if consistently implemented.

**N-2 — Individual mode churn signal classification taxonomy not defined in DS [Architecture]**

- **Location:** §3.1a — "Churn signal classification: categorize churn signals into primary driver (value gap, product-market fit, competitive loss, relationship failure, budget/ROI)"
- **Evidence:** Five churn signal categories are named inline in the DS but not formally defined anywhere. The reference file `churn-rca-taxonomy.md` will presumably contain these definitions, but the DS does not specify classification criteria, signal vocabulary, or detection heuristics. The builder must either infer these from the reference file or from general knowledge.
- **Recommendation:** Add classification heuristics or signal vocabulary to §3.1a, or explicitly state "classification criteria defined in `churn-rca-taxonomy.md`" to make the reference file dependency explicit.

**N-3 — Cohort theme extraction algorithm not specified [Architecture]**

- **Location:** §3.1b — "Cohort theme identification: identify 2–5 dominant themes across the cohort"
- **Evidence:** The DS specifies the output (2–5 dominant themes) but not the method: how themes are extracted, how dominance is measured, and what constitutes a distinct theme vs a variant of the same theme. The `cohort-analysis-framework.md` reference file presumably covers this, but the dependency is not stated.
- **Recommendation:** Add a note: "Theme extraction methodology defined in `cohort-analysis-framework.md`" or provide a minimum specification (e.g., themes derived from majority-signal churn driver classification across accounts in the cohort).

**N-4 — Immutable fields list includes `churn_rate` and `systemic_threshold_met` [Architecture]**

- **Location:** §7 Immutable Fields — includes `churn_rate`, `systemic_threshold_met`
- **Evidence:** These fields are computed outputs, not user-provided inputs. Treating them as immutable after creation is correct (auditable record) but requires that any correction to `portfolio_size` (which affects `churn_rate`) necessitates a new `rca_id` rather than a corrected re-run. This has implications: if a user provides a wrong `portfolio_size`, there is no `update` operation, so the only remedy is a new RCA. The DS does not document this limitation.
- **Recommendation:** Add a note to §7 or §3.1b: "If `portfolio_size` was entered incorrectly, create a new RCA with corrected inputs. Computed fields `churn_rate` and `systemic_threshold_met` are immutable and cannot be corrected post-creation."

---

## Required DS Revisions Before Build

| BLOCK | Fix Required |
|-------|-------------|
| BLOCK-01 | Add `portfolio_size` validation error message; clarify required vs optional |
| BLOCK-02 | Add `export` not-found error message to §3.2 or §10 |
| BLOCK-03 | Choose Option A or B; make §1 and §3.1b consistent on systemic threshold definition |

| WARN | Addressable At |
|------|---------------|
| W-1 | Build time — add Reasoning Protocol to SKILL.md |
| W-2 | DS revision — define `safe_cohort_name` source field |
| W-3 | Accept asymmetry or document rationale in §9 |
| W-4 | Accept unbounded export in v1 or add size advisory |

---

## Stream Status

**Stream B-β** — DVT-8 is **BLOCKED** by 3 BLOCKs. DS revision required before build dispatch. DVT-7 may proceed independently.

---

*Report generated: 2026-05-17 | critical-skill-evaluator v1.5.0 | Evaluator mode*
