---
title: Success Plan Canvas Reasoning Blueprint
type: reasoning-blueprint
skill: success-plan-canvas
version: 1.0.0
---

# Success Plan Canvas — Reasoning Blueprint

## Problem Classification Taxonomy

### Type A — Initial Onboarding Canvas
- **Characteristics:** New customer; no prior plan exists; CSM is building the first success plan
- **Primary Risk:** Generic or incomplete canvas — missing CCSM-104 components or vague success criteria that cannot be measured at review time
- **Expert Focus:** All 7 CCSM-104 components present; success criteria are specific and measurable; stakeholders mapped to their roles

### Type B — Pre-Expansion Canvas
- **Characteristics:** Existing customer; expansion motion underway; canvas must reflect expansion scope distinctly from initial plan
- **Primary Risk:** Blending initial and expansion framing — expansion canvas should not simply restate the initial plan; it must reflect the new scope, new stakeholders, and new success definition
- **Expert Focus:** Expansion-specific framing throughout; clear distinction from the initial plan; OCV outcomes surfaced for the expansion scope

### Type C — Pre-Renewal Review Canvas
- **Characteristics:** Renewal approaching; canvas documents current state and surfaces OCV gaps
- **Primary Risk:** Weak gap analysis — renewal canvas without OCV gap analysis leaves the CSM without the strongest retention argument
- **Expert Focus:** OCV gap analysis must explicitly list committed-but-not-delivered outcomes; prior success criteria evaluated against current delivery state

### Type D — Canvas Refresh (Update)
- **Characteristics:** Existing canvas needs objectives, OCV data, or notes updated; no new dated artifact generated
- **Primary Risk:** Silently overwriting prior state — refresh must preserve the prior canvas version with a clear distinction between original and updated content
- **Expert Focus:** Change scope is limited; only the updated sections are modified; prior plan structure and dated artifacts are preserved

## Domain Heuristics

### H1 — Plan Type Drives Structure
The three plan types (`initial`, `expansion`, `renewal-refresh`) produce distinct document structures. Do not apply initial-plan structure to an expansion canvas or renewal refresh. The label in the document title must match the plan type.

### H2 — OCV Integration Is Required for Renewal-Refresh
Pre-renewal canvases must include OCV snapshot data. A renewal-refresh canvas without OCV gap analysis is structurally incomplete regardless of health status.

### H3 — Success Criteria Must Be Measurable
Success criteria in the plan must be observable and measurable. Criteria like "customer is happy" or "adoption is good" are not acceptable. Push for specific metrics, behaviors, or milestone completions.

### H4 — Canvas Is Upstream of Progress Review
The canvas is the authoritative source for `csm:success-plan-progress-review`. Any ambiguity or incompleteness in the canvas propagates downstream. Completeness at generation time prevents problems at review time.

### H5 — New Dated Artifact for New Plans, Refresh for Updates
A `generate` operation creates a new dated artifact. A `refresh` operation updates the existing artifact. Never create a new dated artifact for a refresh — it fragments the account history.

### H6 — Plan-Type Guide Is Authoritative
Consult `reference/plan-type-guide.md` for plan type definitions, structure requirements, and labeling conventions before generating any canvas. Do not infer structure from context alone.

## Common Failure Modes

### Type A (Initial)
1. **Missing CCSM-104 components** — Canvas generated without all 7 required components. Fix: Enumerate each component before generating; flag any that lack sufficient input.
2. **Success criteria are unmeasurable** — Criteria stated as general satisfaction rather than specific outcomes. Fix: Require CSM to specify metrics or observable behaviors before accepting criteria.

### Type B (Expansion)
1. **Reusing initial plan framing** — Expansion canvas reads like a copy of the initial plan with minor edits. Fix: Expansion scope, stakeholders, and success definition must be explicitly different and clearly labeled.
2. **Missing expansion context** — Canvas created without linking back to the CSQL win that triggered the expansion motion. Fix: Reference the expansion trigger in the plan header.

### Type C (Pre-Renewal)
1. **No OCV gap analysis** — Renewal canvas generated without surfacing committed-but-not-delivered outcomes. Fix: OCV gap section is mandatory for renewal-refresh; if OCV data is unavailable, flag the gap explicitly.
2. **Success criteria never updated since onboarding** — Stale criteria evaluated at renewal. Fix: Check criteria currency against what the customer actually cares about now; update if needed.

### Type D (Refresh)
1. **Full regeneration instead of targeted update** — Refresh operation produces a completely new document. Fix: Scope the refresh to changed sections only; preserve the original artifact.
2. **No change marker** — Refresh applied without indicating what changed and when. Fix: Add a dated change note to the document header.

## Expert Judgment Patterns

### Scope Decisions
- If plan type is ambiguous, ask before generating — the plan type drives every structural decision
- If OCV data is available, surface it for all plan types, not just renewal-refresh
- If success criteria are absent or unmeasurable, pause and request clarification before proceeding

### Operation Routing
- `generate`: new canvas, new dated artifact, full plan-type structure
- `refresh`: targeted update to existing canvas, no new artifact, dated change note

### Depth Decisions
- Initial canvas: maximum depth — all 7 CCSM-104 components need substantive content
- Renewal-refresh: emphasis on OCV gap analysis and prior success criteria evaluation
- Expansion canvas: emphasis on expansion scope differentiation and new stakeholder mapping

### Confidence Decisions
- OCV snapshot from live catalog data: high confidence
- Success criteria from CSM verbal input: moderate confidence — document as stated by CSM
- Stakeholder roles inferred from account context (no CRM data): low confidence — flag as needing verification
