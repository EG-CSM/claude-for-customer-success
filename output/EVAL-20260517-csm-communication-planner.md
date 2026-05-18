# CSE Evaluation Report: csm:communication-planner

**Spec ID:** EVAL-20260517-csm-communication-planner  
**Mode:** Evaluator  
**Input Artifact:** DS-20260517-csm-communication-planner (DVT-9)  
**Evaluated:** 2026-05-17  
**Evaluator:** critical-skill-evaluator v1.5.0  
**Stream:** B-γ  
**Linear Issue:** DVT-9  

EVAL-MARKER-DVT9-LIMA-3391-PAPA

---

## Verdict

**0 BLOCKs | 5 WARNs | 6 NOTEs**

**Proceed to build.** No blocking issues. W-2 (Green-priority expansion_flag touch rule) is a pre-build resolution recommended before dispatch — the builder currently has no explicit contract for how `expansion_flag: true` modifies touch frequency. W-5 (capacity_threshold persistence gap) and W-4 (shared contract governance) are addressable during build or at DVT-11 contracting time. All NOTEs are advisory.

---

## Findings

### BLOCKs (0)

None.

---

### WARNs (5)

**W-1 — No Reasoning Protocol section [Architecture]**

- **Location:** DS document — section list
- **Evidence:** The `plan` operation involves multi-stage judgment: health segment classification of 4 buckets, per-segment touch frequency rule application, non-discretionary mandatory minimum enforcement for Red accounts, capacity arithmetic (total weekly touches), capacity warning threshold comparison, critical flag logic, and optional Green-maintain suppression. These are judgment-intensive sequencing decisions, not pure calculation. No `## Reasoning Protocol` section exists in the DS. Per CSE v1.5.0, missing reasoning protocol = automatic BLOCK in gate mode; WARN in evaluator mode.
- **Recommendation:** Add `## Reasoning Protocol` to SKILL.md at build time covering: (1) segment classification → touch rule lookup → account-level schedule generation, (2) capacity calculation → threshold comparison → warning/critical flag decision, (3) Green-maintain suppression logic → count-vs-display distinction.

**W-2 — Green-priority `expansion_flag` touch rule informally specified [Quality]**

- **Location:** §3.1 segmentation table — `Green-priority` row: "Minimum 2x/month... Expansion-focused; higher if expansion_flag = true"; OQ-2: "Should `Green-priority` touch frequency increase automatically when `expansion_flag: true` (current spec: yes, informally)?"
- **Evidence:** The DS states in the segmentation table that touch frequency is "higher if expansion_flag = true" but marks this as informal in OQ-2. No explicit touch frequency target is given for `expansion_flag: true` accounts. The builder must invent a rule ("3x/month"? "weekly"?) without a contract. This is the single most likely source of builder divergence from product intent.
- **Recommendation:** Resolve OQ-2 before build. Recommended resolution: define explicit touch frequency for `Green-priority + expansion_flag: true` accounts — e.g., 1x/week — and add the rule to both §3.1 and `touch-frequency-rules.md`. This prevents the builder from making an arbitrary choice that may conflict with CSM workflow norms.

**W-3 — `capacity_threshold` minimum validation: error message unspecified [Quality]**

- **Location:** §3.1 inputs table — `capacity_threshold`: "Default: 12. Minimum: 1."
- **Evidence:** The DS declares a minimum value of 1 but does not specify the error message for values ≤ 0. Unlike DVT-8 BLOCK-01 (where `portfolio_size = 0` causes a division-by-zero with no guard), here the minimum is declared — making this a WARN rather than a BLOCK — but the error message the builder should produce is still absent. Consistency with sibling skills (DVT-7, DVT-8) requires explicit error message specification for input validation failures.
- **Recommendation:** Add error message specification for `capacity_threshold` validation failure — e.g., `Validation error: capacity_threshold must be a positive integer (minimum 1). Received: [value].` — in §3.1 or §10 Trust & Verification.

**W-4 — SHARED CONTRACT governance mechanism not specified [Ecosystem]**

- **Location:** §9 Inter-Skill Contract — SHARED TAXONOMY CONTRACT section
- **Evidence:** §9 declares that the 4-label health taxonomy is a shared contract with DVT-11, that DVT-9 owns `health-taxonomy.md`, and that "any change to this taxonomy requires coordinated update in both DS docs and both SKILL.md files." No formal change control mechanism is specified — there is no versioning protocol, no contract version field in the shared taxonomy file, no process defined for initiating a coordinated update. This is declarative governance without enforcement. If DVT-11 is built first and its team proposes a label change, there is no documented escalation path.
- **Recommendation:** Add a contract version field to `health-taxonomy.md` (e.g., `taxonomy_version: 1.0`) and document a simple change protocol in §9: changes require DS revision for DVT-9 AND DVT-11, SKILL.md updates in both skills, and re-evaluation at CSE gate before re-deployment. This is lightweight but gives the builder and future maintainers a clear contract.

**W-5 — `capacity_threshold` persistence gap between `plan` and `update` calls [Architecture]**

- **Location:** §3.2 `update` operation inputs — `capacity_threshold`: "Updated capacity threshold (optional override)"
- **Evidence:** The `update` operation accepts an optional `capacity_threshold` override. If a CSM runs `plan` with `capacity_threshold: 12` and later runs `update` with `capacity_threshold: 10`, the plan's capacity warning status will recalculate against the new threshold — but the original threshold is preserved in the YAML frontmatter (`capacity_threshold: 12`). This creates a state where the displayed capacity warning reflects threshold=10 while the stored metadata reflects threshold=12. The DS does not specify whether `update` should also update the frontmatter `capacity_threshold` field or leave it as the original.
- **Recommendation:** Explicitly state in §3.2 whether `capacity_threshold` override in `update` triggers a frontmatter update or is applied only for the recalculation. Recommended: update frontmatter field to reflect the new threshold, and append the threshold change to the update changelog entry.

---

### NOTEs (6)

**N-1 — `csm_name_safe` empty string edge case [Security]**

- **Location:** §5.1 naming pattern, §10 Trust & Verification
- **Evidence:** The sanitization rule (lowercase → replace non-alphanumeric with `-` → collapse → trim to 30) produces an empty string if `csm_name` consists entirely of special characters (e.g., "---"). An empty `csm_name_safe` would produce an invalid file path (`context/comm-plan--2026-05-17.md`) or a path with a leading hyphen. The DS does not specify a fallback for this edge case.
- **Impact:** Low — the edge case requires a highly unusual csm_name. Consistent with the same finding in DVT-7 N-4 (`safe_account` empty string).
- **Recommendation:** Add edge case clause to §10: if sanitization produces an empty string, generate fallback `unknown-csm` as the `csm_name_safe` value.

**N-2 — `plan_id` collision risk — no SEQ suffix [Quality]**

- **Location:** §6 Auto-ID Generation — format: `COMMPLAN-[CSM]-[YYYYMMDD]`
- **Evidence:** The `plan_id` format `COMMPLAN-[CSM]-[YYYYMMDD]` has no sequence suffix. If the same CSM runs `plan` twice on the same date (e.g., morning and afternoon plans with different account sets, or a re-plan after a roster change), both would generate identical `plan_id` values. DVT-7's `DGA-[ACCT]-[YYYYMMDD]-[SEQ]` and DVT-8's `RCA-[ACCT]-[YYYYMMDD]-[SEQ]` both include a SEQ suffix for this reason.
- **Impact:** Low in practice — multiple plans per CSM per day is unusual — but the lack of SEQ creates a latent integrity gap inconsistent with sibling skill patterns.
- **Recommendation:** Add SEQ suffix to `plan_id` format: `COMMPLAN-[CSM]-[YYYYMMDD]-[SEQ]`, using the same scan-and-increment pattern as DVT-7/DVT-8. Alternatively, document explicitly that only one plan per CSM per date is supported and enforce this as an input rejection.

**N-3 — Green-maintain suppression + capacity warning interaction [Architecture]**

- **Location:** §3.1 capacity warning logic, §2 Scope — "`include_green_maintain` flag suppresses from plan output"
- **Evidence:** §3.1 states capacity warning calculates "total recommended weekly touches across all non-suppressed accounts." When `include_green_maintain: false` (default), Green-maintain accounts are suppressed from the plan output but still counted in the capacity calculation total. CSMs may receive capacity warnings driven by Green-maintain accounts that are invisible in the plan detail — a confusing experience where the warning fires but no suppressed-segment accounts are visible in the output.
- **Impact:** Low behavioral ambiguity — the DS is technically consistent. The UX confusion is the concern.
- **Recommendation:** Add a clarifying note to the capacity warning logic in §3.1: "Green-maintain accounts are included in total weekly touch count regardless of `include_green_maintain` flag. Capacity warning header should indicate: 'X touches/week (includes [N] Green-maintain accounts not shown in detail)' when suppressed Green-maintain accounts contribute to the total."

**N-4 — `update` operation "most recent plan" resolution underspecified [Quality]**

- **Location:** §3.2 `update` inputs — `plan_date`: "defaults to most recent plan for CSM"
- **Evidence:** When `plan_date` is not provided in `update`, the skill defaults to the most recent plan for the CSM. The DS does not specify how "most recent" is determined — by file modification date, by `plan_date` in frontmatter, or by file name sort order. If a CSM has multiple plans with different dates (e.g., `comm-plan-jane-smith-2026-05-01.md` and `comm-plan-jane-smith-2026-05-17.md`), the resolution order needs to be unambiguous.
- **Recommendation:** Specify the "most recent" resolution rule in §3.2 — e.g., "most recent by `plan_date` field in YAML frontmatter, not by file modification time." This prevents non-deterministic behavior when multiple plan files exist.

**N-5 — OQ-3 changelog format deferred to `comm-plan-schema.md` without fallback [Quality]**

- **Location:** §13 OQ-3 — "Should `update` append a changelog entry to the plan document (current spec: append update timestamp and change summary)? Format to be specified in `comm-plan-schema.md`."
- **Evidence:** The DS defers the `update` changelog format to `comm-plan-schema.md`. If that reference file is incomplete or inconsistently authored, the builder has no fallback contract for the update footer format. The file format skeleton in §5.2 shows `*Last updated: [timestamp] | Changes: [account list]*` as a one-liner, but the DS flags this as an open question — creating a conflict between the example and the deferred specification.
- **Recommendation:** In `comm-plan-schema.md`, define the update footer format explicitly before build. Alternatively, promote the §5.2 example as the normative format and close OQ-3 as resolved-by-example.

**N-6 — OQ-1 Yellow non-discretionary minimum rationale not documented [Quality]**

- **Location:** §13 OQ-1 — "Should `Yellow` accounts also have a non-discretionary minimum, or is it purely advisory?"
- **Evidence:** The DS correctly designates Yellow touch frequency as advisory-only (not non-discretionary), but does not document the rationale in §3.1 or §9. The asymmetry between Red (mandatory) and Yellow (advisory) is intentional but unexplained. CSMs reading the plan output may question why Yellow accounts lack the same enforcement. The absence of rationale creates a recurring re-evaluation risk at each review cycle.
- **Recommendation:** Add a one-line rationale note to the Yellow row in the §3.1 segmentation table: "Advisory — CSM judgment governs; non-discretionary enforcement reserved for accounts with confirmed churn or severe dissatisfaction signals (Red only)." Close OQ-1 as resolved-by-design.

---

## Pre-Build Resolutions Required

| Item | Resolution Needed Before Build |
|------|-------------------------------|
| W-1 | Add Reasoning Protocol section to SKILL.md at build time |
| W-2 | Resolve OQ-2 — define explicit touch frequency for `Green-priority + expansion_flag: true` |
| W-3 | Specify `capacity_threshold` validation error message in §3.1 or §10 |
| W-4 | Add contract version and change protocol to `health-taxonomy.md` and §9 |
| W-5 | Clarify `capacity_threshold` frontmatter update behavior in `update` operation §3.2 |

---

## Reference File Build Notes

| File | Build Guidance |
|------|---------------|
| `health-taxonomy.md` | Include: 4-label definitions, classification signal sources, DVT-11 shared contract declaration, taxonomy_version field (W-4), change protocol summary |
| `touch-frequency-rules.md` | Include: per-segment frequencies, non-discretionary trigger conditions, capacity calculation method, capacity warning threshold logic, critical flag criteria, `expansion_flag: true` touch rule for Green-priority (W-2) |
| `comm-plan-schema.md` | Include: YAML frontmatter field definitions, per-segment section structure, capacity summary table format, update changelog footer format (OQ-3 resolution) |

---

## Stream Status

**Stream B-γ** — DVT-9 is **build-ready** pending W-2 (OQ-2) resolution before build dispatch. DVT-10 (`csm:customer-comms`) depends on DVT-9's health taxonomy output contract; building DVT-9 first is required. DVT-10 carries OQ-4 open question requiring resolution before its build dispatch.

---

*Report generated: 2026-05-17 | critical-skill-evaluator v1.5.0 | Evaluator mode*
