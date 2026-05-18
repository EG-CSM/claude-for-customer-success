# CSE Evaluation Report: renewals:downgrade-analysis

**Spec ID:** EVAL-20260517-renewals-downgrade-analysis  
**Mode:** Evaluator  
**Input Artifact:** DS-20260517-renewals-downgrade-analysis (DVT-7)  
**Evaluated:** 2026-05-17  
**Evaluator:** critical-skill-evaluator v1.5.0  
**Stream:** B-β  
**Linear Issue:** DVT-7  

EVAL-MARKER-DVT7-SIERRA-6693-NOVEMBER

---

## Verdict

**0 BLOCKs | 4 WARNs | 5 NOTEs**

**Proceed to build.** No blocking issues. W-4 (OQ-1 severity_score) is a pre-authoring resolution recommended before build to prevent a downstream integration gap with DVT-11. All other WARNs are addressable during build or reference file authoring.

---

## Findings

### BLOCKs (0)

None.

---

### WARNs (4)

**W-1 — Driver inference conflicts not formally defined [Architecture]**

- **Location:** §3.1, driver category inference logic table
- **Evidence:** The table maps signal vocabulary to categories cleanly for single-signal cases. The spec states: "If signals are mixed, skill reports the primary inferred category and flags secondary signals in the analysis." No rule defines how primary is determined when signals split evenly (e.g., 2 budget signals, 2 competitive signals). No tiebreaker documented.
- **Recommendation:** Add a tiebreaker rule to the inference logic — e.g., priority ordering across categories (`dissatisfaction` > `competitive_pressure` > `budget_pressure` > others) or a default to the first-matched category. Document the rule in `downgrade-driver-taxonomy.md` reference file.

**W-2 — No Reasoning Protocol section [Architecture]**

- **Location:** DS document — section list
- **Evidence:** The DS specifies 2 operations (`analyze`, `update`) where `analyze` involves multi-signal inference, failure classification (Missing/Broken link determination), and counter-proposal generation — all judgment-intensive tasks. No `## Reasoning Protocol` section is present in the DS. Per CSE v1.5.0 gate mode requirements, missing reasoning protocol = automatic BLOCK; in evaluator mode this is a WARN.
- **Recommendation:** Add `## Reasoning Protocol` section to the SKILL.md at build time covering: (1) how driver inference is sequenced (signal scan → primary classification → secondary flag), (2) how value chain failure is classified (check OCV delivery gap → check adoption signals → classify Missing/Broken/Non-VCF), (3) how counter-proposal inputs are structured given the driver and failure type.

**W-3 — `update` operation append semantics underspecified for driver reclassification [Quality]**

- **Location:** §3.2, update operation
- **Evidence:** When `revised_driver_category` is provided, the spec states "appends a driver reclassification note with rationale." However, the spec does not define: (1) whether the original driver_category in the YAML frontmatter should be updated to reflect the revision or left as the original, (2) whether the value chain failure map section should be re-run for the new driver category or the revision is purely a log entry. The update block format shows `**Driver reclassification:** [if applicable — from X to Y, rationale]` but the scope of impact on the artifact is not defined.
- **Recommendation:** Explicitly state in §3.2 whether `revised_driver_category` triggers: (a) frontmatter-only update to `driver_category` field, (b) a re-run of value chain failure map appended as a new section, or (c) log-entry only with no structural change to the analysis body. This is a behavior contract that the builder will need to implement deterministically.

**W-4 — OQ-1 severity_score not in v1; creates integration gap with DVT-11 [Ecosystem]**

- **Location:** §13 Open Questions, OQ-1
- **Evidence:** OQ-1 asks: "Should `analyze` support a `severity_score` output (e.g., downgrade risk score 1–10) to enable portfolio-level triage? Useful for rev-ops:portfolio-health-report integration." DVT-11 (`rev-ops:portfolio-health-report`) uses `risk_score = ARR × severity_weight` for at-risk account prioritization. Downgrade scenarios are not currently surfaced in the DVT-11 data model. Without a severity_score or similar signal, downgrade analysis outputs are invisible to portfolio health reporting.
- **Recommendation:** Resolve OQ-1 before build. Recommended resolution: add `severity_score` (integer 1–10) as an optional output field in `analyze`, computed from `driver_category` and `downgrade_request` signals. Document the scoring rubric in `downgrade-driver-taxonomy.md`. This enables DVT-11 to consume downgrade severity as a portfolio risk signal without requiring DVT-11 schema changes.

---

### NOTEs (5)

**N-1 — `ocy_snapshot` field name inconsistency [Quality]**

- **Location:** §3.1 inputs table (row: `ocy_snapshot`), §3.2 update inputs table (row: `ocy_snapshot`)
- **Evidence:** The field is named `ocy_snapshot` throughout the DS. The logical field name for Outcome & Value Catalog data is `ocv_snapshot`. This appears to be a typo consistent with DVT-8 (`renewals:churn-rca`), suggesting a common authoring error rather than intentional naming.
- **Impact:** Low — this is a DS-level naming inconsistency. The builder will implement whatever name is in the DS. If the field name is corrected in the DS, it must be corrected consistently in both DVT-7 and DVT-8 simultaneously to maintain sibling skill consistency.
- **Recommendation:** Decision required: preserve `ocy_snapshot` as-is (acceptable; creates quirky but internally consistent naming) OR correct to `ocv_snapshot` across DVT-7 and DVT-8 simultaneously before build. Not a blocker either way.

**N-2 — Escalation trigger condition in counter-proposal framework is structural only [Quality]**

- **Location:** §3.1, Analysis output structure — `Recommended Response Strategy > Escalation Trigger`
- **Evidence:** The spec requires `[Condition under which this should escalate beyond CSM/AM]` as a named output field. No reference to what conditions qualify as escalation-worthy is provided in the DS body. This content will need to be authored in `counter-proposal-framework.md` at build time. If the reference file is incomplete, the skill output may produce generic escalation triggers rather than driver-specific ones.
- **Recommendation:** Ensure `counter-proposal-framework.md` includes driver-specific escalation trigger conditions for all 5 categories. Flag in build brief.

**N-3 — No formal output for OCV correlation [Architecture]**

- **Location:** §3.1, optional `ocy_snapshot` input
- **Evidence:** The DS states OCV snapshot is "used to assess value delivery vs downgrade driver correlation." The output structure shows `[Narrative: what failed, where in the value chain, evidence from request and OCV]` in the Value Chain Failure Map section. There is no structured OCV correlation output — it is folded into the narrative. For downstream skills or human readers who need to extract the OCV correlation data, this makes it hard to parse programmatically.
- **Recommendation:** Consider adding a structured `### OCV Correlation` subsection in the value chain failure map output even when OCV data is present. Acceptable to leave as narrative in v1; flag for v2 consideration.

**N-4 — `safe_account` derivation from `account_name` has edge case with all-numeric names [Security]**

- **Location:** §5.1 naming pattern, §10 Trust & Verification
- **Evidence:** The sanitization rule is: lowercase → replace non-alphanumeric with `-` → collapse consecutive hyphens → trim to 30. An account_name that is purely numeric (e.g., "123456") would produce `safe_account = "123456"` — valid per the rule but potentially confusing. An account name like "--- ---" (all dashes/spaces) would produce empty string after sanitization, which would create an invalid file path. The DS does not specify behavior for empty `safe_account` results.
- **Recommendation:** Add an edge case clause: if sanitization produces an empty string, generate a fallback (`unknown-account`). Document in §10 Trust & Verification.

**N-5 — OQ-3 has architectural implications if addressed [Architecture]**

- **Location:** §13 OQ-3
- **Evidence:** OQ-3 asks whether `update` should support a category override that re-runs the analysis (not just appends a note). If addressed in v1, this would change the `update` operation from append-only to partially mutable — conflicting with the append-only semantic declared in §3.2 and §7 immutable fields. Introducing selective re-analysis would require specifying which sections are regenerated vs preserved, adding significant complexity.
- **Recommendation:** Leave OQ-3 out of scope for v1. The current append-only `update` model is clean and auditable. If re-analysis is needed, the appropriate pattern is a new `analyze` operation with a new `dga_id`. Document this recommendation in the build brief.

---

## Pre-Build Resolutions Required

| Item | Resolution Needed Before Build |
|------|-------------------------------|
| W-1 | Add tiebreaker rule to driver inference logic |
| W-2 | Add Reasoning Protocol section to SKILL.md at build time |
| W-3 | Clarify driver reclassification scope in `update` operation |
| W-4 | Resolve OQ-1 — add `severity_score` output or explicitly defer |
| N-1 | Decision: preserve `ocy_snapshot` or correct to `ocv_snapshot` across DVT-7 + DVT-8 |

---

## Reference File Build Notes

| File | Build Guidance |
|------|---------------|
| `downgrade-driver-taxonomy.md` | Include: 5 category definitions, signal vocabulary per category, inference tiebreaker rule (W-1), diagnostic questions per category, severity scoring rubric (W-4) |
| `value-chain-failure-map.md` | Include: Missing link / Broken link / Non-VCF definitions, detection patterns from request + OCV signals, driver reclassification scope clarification (W-3) |
| `counter-proposal-framework.md` | Include: retention levers per driver category, negotiation anchor patterns, driver-specific escalation trigger conditions (N-2) |

---

## Stream Status

**Stream B-β** — DVT-7 is **build-ready** pending W-4 (OQ-1) resolution. DVT-8 (`renewals:churn-rca`) carries 3 BLOCKs; that stream is blocked until DVT-8 DS revision is complete. DVT-7 and DVT-8 are sibling skills; building DVT-7 before DVT-8 is unblocked is acceptable — they share only the namespace contract, not input/output dependencies.

---

*Report generated: 2026-05-17 | critical-skill-evaluator v1.5.0 | Evaluator mode*
