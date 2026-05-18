# CSE Evaluation Report: rev-ops:portfolio-health-report

**Spec ID:** EVAL-20260517-rev-ops-portfolio-health-report  
**Mode:** Evaluator  
**Input Artifact:** DS-20260517-rev-ops-portfolio-health-report (DVT-11)  
**Evaluated:** 2026-05-17  
**Evaluator:** critical-skill-evaluator v1.5.0  
**Stream:** D  
**Linear Issue:** DVT-11  

EVAL-MARKER-DVT11-ZULU-8841-VICTOR

---

## Verdict

**0 BLOCKs | 4 WARNs | 3 NOTEs**

**Proceed to build — with W-2 resolved before dispatch.** No blocking issues. W-1 (Reasoning Protocol) must be added at build time. W-2 (health-outcome misalignment detection algorithm) is the highest architectural risk — the reference file `health-outcome-misalignment-logic.md` must be fully specified before builder dispatch, as the DS body contains zero algorithm detail. W-3 (export not-found error) should be resolved at build time. W-4 (DVT-7 severity_score integration gap) is a known external dependency that does not block DVT-11 build but must be tracked. All NOTEs are advisory.

**Build dependency:** DVT-9 (`csm:communication-planner`) must be built first — DVT-11 reads `health-taxonomy.md` owned by DVT-9. The taxonomy reference file must exist before DVT-11 build proceeds.

---

## Findings

### BLOCKs (0)

None.

---

### WARNs (4)

**W-1 — No Reasoning Protocol section [Architecture]**

- **Location:** DS document — section list
- **Evidence:** The `generate` operation involves multi-stage inference with non-trivial branching: (1) input validation — Account Object schema compliance, health_status taxonomy validation, required field enforcement; (2) health segment classification — consumer of shared taxonomy, not generator; (3) health-outcome misalignment detection — Green health + OCV delivery gap = hidden risk; requires threshold comparison and output flag assignment; (4) risk ranking — ARR × severity_weight formula with no-ARR sort-to-bottom fallback; (5) expansion ranking — expansion_opportunity flag + signal extraction; (6) report assembly — csm_portfolio vs org_rollup mode determines output structure and level of detail. Each stage is a judgment decision point, especially misalignment detection (threshold evaluation across Green accounts) and dual-mode assembly. No `## Reasoning Protocol` section exists in the DS. Per CSE v1.5.0, missing reasoning protocol = automatic BLOCK in gate mode; WARN in evaluator mode.
- **Recommendation:** Add `## Reasoning Protocol` to SKILL.md at build time covering: (1) input validation sequence — Account Object schema check, health_status taxonomy validation against shared taxonomy, required field presence; (2) health-outcome misalignment detection — detect before risk ranking; Green accounts with OCV gap get `misalignment_flag: true`; (3) risk ranking — apply ARR × severity_weight; sort no-ARR accounts to bottom of ranked list; (4) expansion ranking — apply expansion_opportunity flag; extract expansion_signal for display; (5) mode-conditional assembly — csm_portfolio: per-CSM grouping with account-level detail; org_rollup: aggregated view across all CSMs.

**W-2 — Health-outcome misalignment detection algorithm deferred entirely to reference file with no DS body specification [Architecture]**

- **Location:** §3.1 `generate` operation — "Misalignment detection: Accounts where health_status is Green-priority or Green-maintain but OCV delivery ratio falls below a threshold are flagged as health-outcome misaligned. See `health-outcome-misalignment-logic.md` for full detection logic."
- **Evidence:** The DS body contains zero algorithm specification for misalignment detection. No threshold value, no formula, no OCV delivery ratio definition (ocv_delivered / ocv_total? something else?), no flag field name in the Account Object schema, no edge case handling for accounts with ocv_total = 0. The entire detection algorithm is deferred to `health-outcome-misalignment-logic.md`. The builder has no fallback contract if the reference file is incomplete — and the reference file has not yet been authored. This is the highest architectural risk in the DS: a core differentiator of the skill (described as a key feature in §1) with no operative specification in the DS body.
- **Recommendation:** Before build dispatch, add a minimum algorithm sketch to §3.1: define the OCV delivery ratio formula (`ocv_delivered / ocv_total`), define the default threshold (e.g., < 0.7 = misaligned), define the output flag field (`misalignment_flag: true/false`), and define the zero-OCV edge case (see N-3). Then specify `health-outcome-misalignment-logic.md` as the source for extended reasoning, threshold tuning guidance, and CSM-facing explanatory language. This split (operative spec in DS body, extended guidance in reference file) follows the same pattern as DVT-9's `touch-frequency-rules.md`.

**W-3 — `export` not-found error unspecified [Quality]**

- **Location:** §3.2 `export` operation inputs — `report_file`: "Path to the generated report file (required)"; no error handling defined for missing file
- **Evidence:** The `export` operation requires a `report_file` input pointing to a previously generated portfolio report. The DS does not specify the error message when the referenced file does not exist. This mirrors the pattern flagged as BLOCK-02 in DVT-8 (`renewals:churn-rca`) where `export` not-found handling was absent. DVT-11's `export` is a secondary operation (not the primary `generate`), reducing severity from BLOCK to WARN — but the error handling gap is identical.
- **Recommendation:** Add error message specification for `report_file` not-found case to §3.2 or §10 Trust & Verification — e.g., `Export error: report file not found at [report_file]. Run generate first to produce the report, then export.` Consistent with the pattern established in DVT-7 and DVT-8 for missing-file errors.

**W-4 — DVT-7 severity_score integration gap: risk_score formula cannot consume DVT-7 downgrade severity [Ecosystem]**

- **Location:** §3.1 risk ranking — `risk_score = ARR × severity_weight`; §9 Inter-Skill Contract — DVT-7 mapping table
- **Evidence:** DVT-11 ranks at-risk accounts by `risk_score = ARR × severity_weight` (Red=3, Yellow=1). DVT-7 (`renewals:downgrade-analysis`) produces a `severity_score` for downgrade risk that is directly relevant to Red/Yellow classification of renewal-at-risk accounts. DVT-7 OQ-1 (flagged as WARN in DVT-7 EVAL) asks whether `severity_score` should be part of DVT-7's v1 output contract. Until OQ-1 is resolved, DVT-11 cannot consume DVT-7's severity data — it falls back to the binary ARR × severity_weight formula with no downgrade severity gradient. This creates a known gap in the org_rollup report: accounts with identical ARR and health segment but very different downgrade severity scores will rank identically.
- **Recommendation:** Track DVT-7 OQ-1 as an explicit dependency in §9. Add a note: "If DVT-7 includes `severity_score` in its output contract (OQ-1 resolution), DVT-11 risk ranking should be upgraded to incorporate it — e.g., `risk_score = ARR × severity_weight × severity_score_modifier`. This is a v1.1 enhancement pending DVT-7 contract finalization."

---

### NOTEs (3)

**N-1 — `risk_score` sort behavior for no-ARR accounts documented in §13 OQ-5 RESOLVED only — not in operative §3 or §5 [Quality]**

- **Location:** §13 OQ-5 (RESOLVED): "No-ARR accounts: sort to bottom of ranked list; document as 'ARR not provided' in report output"; §3.1 Account Object schema — `arr` field: "(optional)"
- **Evidence:** The `arr` field is optional in the Account Object schema. When `arr` is absent, the risk_score formula (`risk_score = ARR × severity_weight`) produces an undefined result. The resolution to this is documented only in §13 OQ-5 (RESOLVED) as "sort to bottom of ranked list." This critical sort behavior — which every builder must implement correctly — is buried in the open questions section rather than stated as a rule in §3.1 or in the risk ranking operative spec. A builder who does not read §13 will produce undefined behavior for no-ARR accounts.
- **Impact:** Low — correctable during build, but the mislocation risks builder oversight.
- **Recommendation:** Promote the OQ-5 resolution to §3.1 in the Account Object schema description for `arr`: "Optional. When `arr` is absent, `risk_score` is undefined — accounts sort to the bottom of the risk-ranked list with a display note: 'ARR not provided.'" Cross-reference §13 OQ-5 as the resolution source.

**N-2 — `safe_identifier` function referenced in §10 but not formally defined; empty string edge case unaddressed [Security]**

- **Location:** §10 Trust & Verification — "identifier is sanitized before use in file path construction using `safe_identifier` function"; §5.1 naming conventions — "identifier: lowercase, alphanumeric + hyphens, max 30 chars"
- **Evidence:** §10 references a `safe_identifier` function for path safety, but §5.1 only describes the output rule informally (lowercase → replace non-alphanumeric with `-` → collapse → trim to 30 chars). No formal function definition exists. The edge case where sanitization produces an empty string (e.g., if `identifier` consists entirely of special characters like `---`) is not addressed — this would produce a path collision at `context/portfolio-health--[date].md`. This is the same edge case flagged as N-4 in DVT-7 (`safe_account` empty string), N-1 in DVT-9 (`csm_name_safe` empty string), and noted as a recurring pattern across the skill family.
- **Impact:** Low — consistent with sibling skill findings. Ecosystem-wide fix recommended.
- **Recommendation:** Add edge case clause to §10: if sanitization produces an empty string, generate fallback `unknown-id` as the `safe_identifier` value. Consistent with the recommended remediation in DVT-7 N-4 and DVT-9 N-1. An ecosystem-level fix to a shared `safe_identifier` utility function would address all occurrences simultaneously.

**N-3 — OCV gap edge case: `ocv_total = 0` accounts and misalignment detection undefined [Quality]**

- **Location:** §11 reference file guidance — `health-outcome-misalignment-logic.md`: "Must handle edge cases including ocv_total = 0 (no OCV commitments — no delivery gap by definition)"
- **Evidence:** The DS correctly notes in §11 that `health-outcome-misalignment-logic.md` must handle the `ocv_total = 0` edge case. However, the resolution is deferred — the DS body does not define the behavior: should a Green account with `ocv_total = 0` be flagged as misaligned (no outcomes delivered), flagged as not-applicable (no commitments made), or suppressed from misalignment analysis entirely? The three interpretations have meaningfully different operational implications for CSMs reading the report.
- **Impact:** Low — deferred to reference file. Correctly identified in the DS.
- **Recommendation:** In `health-outcome-misalignment-logic.md`, define the `ocv_total = 0` resolution explicitly: recommended treatment is "not-applicable" — zero OCV commitments means no delivery gap is measurable; exclude from misalignment flagging; optionally surface in a separate "No OCV Commitments" section if the reporting mode supports it.

---

## Pre-Build Resolutions Required

| Item | Resolution Needed Before Build |
|------|-------------------------------|
| W-1 | Add Reasoning Protocol section to SKILL.md at build time |
| W-2 | Author `health-outcome-misalignment-logic.md` with minimum algorithm spec before builder dispatch; promote OCV delivery ratio formula and threshold to DS §3.1 body |
| W-3 | Specify `export` not-found error message in §3.2 or §10 |
| W-4 | Track DVT-7 OQ-1 as explicit dependency in §9; document v1.1 enhancement path |

---

## Reference File Build Notes

| File | Build Guidance |
|------|---------------|
| `health-taxonomy.md` | SHARED — owned by DVT-9 (`csm:communication-planner`). DVT-11 reads by reference; must NOT duplicate. Health-taxonomy.md must be authored as part of DVT-9 build before DVT-11 build dispatch. |
| `portfolio-health-schema.md` | Include: Account Object field definitions (all 9 fields), required vs optional markers, csm_portfolio report format per-CSM section structure, org_rollup report format aggregate structure, capacity summary table format, same-date overwrite behavior (OQ-4 resolution pending), export file naming convention |
| `health-outcome-misalignment-logic.md` | Include: OCV delivery ratio formula (ocv_delivered / ocv_total), default misalignment threshold with rationale, Green segment eligibility for flagging (Green-priority and Green-maintain), ocv_total = 0 edge case handling (N-3 resolution), CSM-facing explanatory language for misaligned accounts, flag field name and schema contract (`misalignment_flag: true/false`) |

---

## Stream Status

**Stream D** — DVT-11 is **build-ready pending W-2 (`health-outcome-misalignment-logic.md`) authoring before build dispatch.** DVT-9 (`csm:communication-planner`) must be built first — DVT-11 depends on `health-taxonomy.md` owned by DVT-9. After DVT-9 build completes and `health-taxonomy.md` is authored, DVT-11 build dispatch is cleared (assuming W-2 reference file is authored simultaneously with DVT-9 reference files).

---

*Report generated: 2026-05-17 | critical-skill-evaluator v1.5.0 | Evaluator mode*
