# CSE Evaluation Report: csm:customer-comms

**Spec ID:** EVAL-20260517-csm-customer-comms  
**Mode:** Evaluator  
**Input Artifact:** DS-20260517-csm-customer-comms (DVT-10)  
**Evaluated:** 2026-05-17  
**Evaluator:** critical-skill-evaluator v1.5.0  
**Stream:** B-γ  
**Linear Issue:** DVT-10  

EVAL-MARKER-DVT10-NOVEMBER-5527-KILO

---

## Verdict

**0 BLOCKs | 4 WARNs | 5 NOTEs**

**Proceed to build — with OQ-4 resolved before dispatch.** No blocking issues. W-1 (Reasoning Protocol) must be added at build time. W-3 (no-write enforcement) is the highest architectural risk — the builder must explicitly enforce session-only output with no fallback path to filesystem. W-4 (OQ-4 `Green-maintain` gate scope) should be resolved before build dispatch since it affects a hard gate condition. All NOTEs are advisory.

---

## Findings

### BLOCKs (0)

None.

---

### WARNs (4)

**W-1 — No Reasoning Protocol section [Architecture]**

- **Location:** DS document — section list
- **Evidence:** The `draft` operation involves sequential multi-stage inference: (1) `communication_type` validation against 9-value enum, (2) gate condition evaluation (expansion gate OR confirmation gate), (3) health-calibrated tone selection from 4×9 matrix, (4) draft generation, (5) mandatory private rationale construction. Each stage is a judgment decision with non-trivial branching (especially gate enforcement order and tone override when health is Red). No `## Reasoning Protocol` section exists in the DS. Per CSE v1.5.0, missing reasoning protocol = automatic BLOCK in gate mode; WARN in evaluator mode.
- **Recommendation:** Add `## Reasoning Protocol` to SKILL.md at build time covering: (1) input validation sequence — `communication_type` enum check, `account_health` taxonomy check, gate condition evaluation in declared order, (2) tone selection — health segment maps to tone profile; `communication_type` may further modulate tone within segment, (3) gate evaluation order — expansion gate checked before draft generation; risk-notice gate wraps the already-drafted output, (4) rationale construction — written last, after draft complete; cites health segment, tone selection, and gate outcomes.

**W-2 — Gate evaluation order for simultaneous gate conditions underspecified [Quality]**

- **Location:** §3.1 Gate enforcement — expansion gate and risk-notice confirmation gate defined separately; no combined-gate case addressed
- **Evidence:** The DS defines two independent gate conditions. The expansion gate fires when `communication_type == "expansion-intro"` AND health or `ocv_expansion_flag` is non-compliant — returning an error before draft generation. The risk-notice gate fires when `communication_type == "risk-notice"` AND `confirmed != true` — returning a pending draft after generation. These two types cannot logically co-occur (a `communication_type` value cannot simultaneously be `expansion-intro` and `risk-notice`), but the DS does not explicitly state this mutual exclusivity. A builder may leave an undefined case if a future `communication_type` is added that triggers both gate conditions simultaneously.
- **Recommendation:** Add a clarifying note to §3.1 gate enforcement: "Gate conditions are mutually exclusive by communication_type — a single communication type can trigger at most one gate. If a future communication type were subject to multiple gates, expansion gate takes priority (rejects before draft generation); confirmation gate wraps a completed draft." This documents the intent and future-proofs the gate architecture.

**W-3 — Session-only output enforcement mechanism not specified [Architecture]**

- **Location:** §2 Scope (Out of Scope: "Saving drafts to filesystem"), §5 Context File Architecture ("Not applicable"), §8 Filesystem Constraints ("Write scope: none")
- **Evidence:** The DS correctly declares session-only output and no filesystem writes in three separate sections. However, the builder has no explicit contract for HOW to enforce this — there is no `## Filesystem Constraints` enforcement clause that states what happens if the builder accidentally includes a file-write instruction in the SKILL.md body, and no specification for what the skill should do if a tool calling path would result in a write (i.e., the enforcement is declarative, not procedural). In a TDD+ build, the RED phase needs a failing test for "output not written to filesystem." The DS provides the intent but not the guard.
- **Recommendation:** Add a one-line enforcement clause to §8: "SKILL.md must contain no file-write tool calls. If a tool call path would write a file, reject that path in implementation. The RED test suite must include a test case: `generate draft → verify no file exists at any context/ path after invocation`." This makes the no-write contract testable and provides the builder with a concrete implementation criterion.

**W-4 — OQ-4: `Green-maintain` as valid health segment for `expansion-intro` not resolved [Quality]**

- **Location:** §13 OQ-4 — "Is `Green-maintain` a valid health segment for `expansion-intro`? Current spec: yes (Green-priority OR Green-maintain). May need to restrict to `Green-priority` only, since Green-maintain implies low-growth posture."
- **Evidence:** The expansion gate in §3.1 currently permits `expansion-intro` for both `Green-priority` and `Green-maintain` accounts. OQ-4 explicitly flags this as unresolved. This is not merely a quality preference — it affects the hard gate condition that the builder will implement. If OQ-4 is resolved post-build as "Green-priority only," the gate condition in the built SKILL.md would require a code change. Since the gate logic is relatively simple to specify at this stage, the risk of a post-build gate revision outweighs the cost of resolution now.
- **Recommendation:** Resolve OQ-4 before build dispatch. Recommended resolution: restrict `expansion-intro` to `Green-priority` only, since Green-maintain explicitly represents low-growth, steady-state posture — an expansion introduction in this segment is incongruent with the segment definition. Update §3.1 expansion gate condition from "`Green-priority` or `Green-maintain`" to "`Green-priority` only" and update the gate violation message accordingly. If the business rationale for including Green-maintain is confirmed, document it explicitly so the gate intent is clear.

---

### NOTEs (5)

**N-1 — Health label pass-through: caller-provided `account_health` not cross-validated against DVT-9 plan [Architecture]**

- **Location:** §9 Inter-Skill Contract — DVT-9 mapping contract table
- **Evidence:** §9 maps DVT-9's `health_status` output to DVT-10's `account_health` input. However, this mapping is a human-mediated pass-through — the CSM reads the account's health from the DVT-9 plan and manually supplies it as a DVT-10 input parameter. DVT-10 does not read the DVT-9 plan file. This means a CSM could call DVT-10 with `account_health: Green-priority` for an account whose communication plan shows `Red` health — and the draft would be generated with the wrong tone profile. The DS correctly declares this is out of scope (no file read), but does not document the mismatch risk or advise the CSM to verify.
- **Impact:** Low — input is caller responsibility. Consistent with the skill's stateless design.
- **Recommendation:** Add a caller advisory note to §9: "CSM is responsible for ensuring `account_health` provided to DVT-10 matches the account's current health classification in the DVT-9 communication plan. Mismatched health will produce drafts with incorrect tone calibration. DVT-10 does not validate against the DVT-9 plan file."

**N-2 — `context_notes` influence on draft generation underspecified [Quality]**

- **Location:** §3.1 inputs table — `context_notes`: "CSM-provided context notes — incorporated into rationale; may influence draft emphasis"
- **Evidence:** The input description states `context_notes` is "incorporated into rationale; may influence draft emphasis." The qualifier "may" makes the influence on the draft body itself ambiguous. The builder must decide whether `context_notes` can modify draft content (e.g., a CSM note saying "this account's champion just left" should probably shift tone even within a `Yellow` segment) or is strictly confined to the rationale section. The reference file `csm-rationale-templates.md` may specify this, but the DS body does not.
- **Impact:** Low — likely resolved by reference file at build time. Flag for verification.
- **Recommendation:** In `csm-rationale-templates.md`, specify explicitly: (a) `context_notes` is ALWAYS reflected in the rationale, and (b) `context_notes` MAY influence draft body language when the note contains specific factual signals (e.g., contact departure, escalation trigger, milestone miss) — builder should treat it as tone-modulating input within the health segment's tone profile, not as an override.

**N-3 — OQ-1: `churn-save` confirmation gate not addressed; risk acknowledged but unresolved [Quality]**

- **Location:** §13 OQ-1 — "Should `churn-save` also require a confirmation gate similar to `risk-notice`? Current spec: no gate."
- **Evidence:** §13 explicitly notes that `churn-save` misuse risk is "real" and recommends "revisiting before SKILL.md implementation." This is effectively the same priority signal as a W-4 recommendation — yet it's filed as an OQ at NOTE severity. Given that `churn-save` is likely the highest-stakes communication type in the enumeration, a missed confirmation gate could result in a CSM accidentally sending an emotionally charged retention communication without review.
- **Impact:** Moderate-to-low — depends on organizational risk tolerance for unconfirmed churn-save communications.
- **Recommendation:** Resolve OQ-1 before build dispatch. Recommended resolution: add a confirmation gate to `churn-save` using the same pattern as `risk-notice` — return as `[PENDING — REQUIRES CONFIRMATION]` until `confirmed: true`. The incremental implementation cost is negligible (same gate pattern already exists), and the operational risk of an unconfirmed churn-save communication is disproportionate to the cost of the gate.

**N-4 — Draft length / format expectations absent from DS [Quality]**

- **Location:** §3.1 draft operation — output section states "draft text + `## CSM Rationale (Private)` section returned in session"; no length or format guidance
- **Evidence:** The DS defines the communication types and tone profiles but does not specify any constraints on draft length, formatting, or structure (e.g., should `qbr-invite` include an agenda placeholder? Should `risk-notice` follow a specific structure: acknowledgment → root cause → recovery path → next step?). This leaves the builder with wide latitude that could produce inconsistent output across communication types.
- **Impact:** Low — reference file `communication-types.md` is expected to cover this per §11. Flag for reference file authoring.
- **Recommendation:** In `communication-types.md`, specify for each of the 9 types: (a) target draft length range (e.g., 2–4 sentences for `check-in`, 3–5 paragraphs for `risk-notice`), (b) required structural elements if any (e.g., `risk-notice` must include: acknowledgment, recovery path, next step), (c) example opening line as already specified in the DS.

**N-5 — No output persistence + no audit trail: acknowledged risk not formally closed [Quality]**

- **Location:** §2 Out of Scope ("Editing or versioning prior drafts"), §4 Status State Machine ("Not applicable"), §5 Context File Architecture ("Not applicable")
- **Evidence:** The session-only design is intentional and correctly documented. However, the DS does not acknowledge the implication: there is no record of what communications were drafted or sent. If an account escalates and the CSM is asked "what did you communicate to this account last week?", DVT-10 drafts are invisible. This is a deliberate trade-off but is not formally documented as such — there is no "Design Decision" record or rationale note explaining why audit trail was explicitly excluded.
- **Impact:** Low — operational awareness issue, not an implementation defect.
- **Recommendation:** Add a "Design Decision" note to §2: "Session-only output is intentional. No audit trail is maintained by DVT-10. CSMs who require audit trails of sent communications must record drafts in their CRM or communication log manually. This is a deliberate trade-off: session-only output eliminates filesystem dependency and simplifies the skill's security footprint."

---

## Pre-Build Resolutions Required

| Item | Resolution Needed Before Build |
|------|-------------------------------|
| W-1 | Add Reasoning Protocol section to SKILL.md at build time |
| W-2 | Add mutual-exclusivity clause to gate enforcement in §3.1 |
| W-3 | Add enforcement clause to §8: no-write contract must be testable in RED phase |
| W-4 | Resolve OQ-4 — define explicit gate condition for `expansion-intro` (Green-priority only vs. both Green segments) |

---

## Reference File Build Notes

| File | Build Guidance |
|------|---------------|
| `communication-types.md` | Include: all 9 type definitions, purpose, use case, gate conditions (expansion + confirmation), draft length range, required structural elements, example opening lines |
| `health-tone-matrix.md` | Include: tone profiles per health segment, tone language examples per segment, tone escalation rules for Red accounts, how `communication_type` modulates tone within a segment |
| `csm-rationale-templates.md` | Include: rationale section structure, language guidance per communication type per health segment, template phrases, gate evaluation language ("I evaluated the expansion gate — account_health is Green-priority and ocv_expansion_flag is true"), first-person CSM framing, `context_notes` integration guidance (N-2 resolution) |

---

## Stream Status

**Stream B-γ** — DVT-10 is **build-ready pending W-4 (OQ-4) resolution before dispatch.** DVT-9 (`csm:communication-planner`) must be built first — DVT-10 depends on the health taxonomy and communication plan output format produced by DVT-9. After DVT-9 build completes and `health-taxonomy.md` is authored, DVT-10 build dispatch is cleared.

---

*Report generated: 2026-05-17 | critical-skill-evaluator v1.5.0 | Evaluator mode*
