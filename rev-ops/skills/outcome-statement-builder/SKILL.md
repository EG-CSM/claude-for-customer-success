---
name: outcome-statement-builder
description: "Outcome Statement Builder -- transform raw product or service capabilities into structured, verifiable outcome statements using the Seven-Stage Value Chain, then assign tangible business metrics and generate a multi-level achievement rubric. Use during Outcome Catalog development to convert capability inputs into catalog-ready outcome entries with approval checkpoints and rubric-based evaluation criteria. Produces a local Outcome & Value Registry in machine-readable Markdown and a presentation-ready HTML review deck for cross-functional ratification with Sales, Marketing, RevOps, and CS."
---

# Outcome Statement Builder

## Overview

Transforms raw capability inputs into structured, verifiable outcome statements aligned to
the Seven-Stage Value Chain. After user approval, assigns specific business metrics and
generates a four-level achievement rubric for each outcome. Produces two output artifacts:
a machine-readable Markdown registry and a presentation-ready HTML review deck.

Operates in two sequential phases with an explicit approval gate between them.

**Use when:**
- You have product or service capabilities to translate into customer outcome language
- You need outcome statements that can pass catalog entry standards (measurable, role-specific, trigger-conditioned)
- You want to assign business metrics and achievement levels to an approved outcome set
- You are building or populating a local Outcome & Value Registry
- You need a cross-functional review artifact for Sales, Marketing, RevOps, or CS ratification sessions

**Do NOT use for:**
- Editing or updating existing catalog entries (use outcome-catalog-entry-builder)
- Generating a full catalog from research data (use provisional-outcome-catalog-generator)
- Competitive analysis or benchmarking
- Capabilities that are not yet delivered — this skill works with what exists, not roadmap items

**Typical activation:**
- "Help me turn these capabilities into outcomes"
- "Transform my capability list into outcome statements"
- "Build outcomes from these features and generate the registry"
- "I need to create outcome statements, rubrics, and a review deck"

---

## Specification

| Attribute | Value |
|-----------|-------|
| Phases | 2 (with approval gate) |
| Value Chain | Seven-Stage (SuccessCOACHING) |
| Output Format | Outcome Statement → Approval → Value Assignment → Rubric → Registry + HTML Deck |
| Interaction Mode | Collaborative — user approves or edits before Phase 2 |
| Complexity | T2 — Professional |
| Worked Examples | See `references/worked-examples.md` — Gong.io CRO segment, OCV-001 and OCV-002 |
| Reference Output | See `references/reference-registry.md` — complete 6-entry populated registry |

---

## Input Schema

**Phase 1 — Capability Intake:**
```
capability_input:
  capabilities: list[str]          # Raw capabilities, features, or functional descriptions
  product_or_service_name: str     # What the capability belongs to
  customer_segment: str            # Who uses this (role, company size, industry)
  context: str | None              # Optional — what problem this solves or use case
```

**Phase 2 — Value Assignment (after approval):**
```
approved_outcomes: list[str]       # Outcomes approved or edited in Phase 1
value_context: str | None          # Optional — known customer metrics, industry benchmarks
```

---

## Output Schema

**Phase 1 Output — Outcome Statement Set:**
```
outcome_statement_set:
  - capability_input: str
    evaluation:
      issues: list[str]            # What makes the raw input fall short
      strength: str                # What is usable
    outcome_statement: str         # Transformed, structured statement
    value_chain_stage: str         # Stage 2 / 3 / 4 with explanation
    approval_status: pending | approved | edited | regenerate
```

**Phase 2 Output — Rubric Set + Registry Artifacts:**
```
rubric_set:
  - outcome_statement: str
    business_metric: str           # Specific, named metric
    measurement_source: str        # Where this is measured
    rubric:
      level_0: str                 # Not achieved — leading indicators absent
      level_1: str                 # Partial — leading indicators present, lagging not yet
      level_2: str                 # Achieved — primary metric verified
      level_3: str                 # Exceeded — primary metric plus secondary impact verified
    verification_method: str       # How CS confirms achievement

artifacts:
  - [product-slug]-outcome-value-registry.md   # Machine-readable + human-readable registry
                                                # e.g., gong-outcome-value-registry.md
  - [product-slug]-outcome-review-deck.html    # Presentation-ready cross-functional review artifact
                                                # e.g., gong-outcome-review-deck.html
```

For the exact structure of both artifacts from a live test run, see:
- `references/reference-registry.md` — canonical registry schema (6-entry Gong.io CRO example)
- `gong-outcome-value-registry.md` — live registry output from the Gong.io test run
- `gong-outcome-review-deck.html` — live HTML deck from the same test run

---

## Core Workflow

### PHASE 1 — Capability Intake and Outcome Transformation

**Step 1 — Receive and Validate Capabilities**

When the user provides capabilities, confirm the minimum viable inputs before proceeding:
- Product or service name (ask if not provided)
- Customer segment — role, company type, size range (ask if not provided)
- The capability list (one per input acceptable; comma-separated or bulleted also accepted)

If any required input is missing, ask for it before proceeding. Ask one item at a time.

**Step 2 — Evaluate Each Capability**

For each capability input, run the following evaluation before transforming it.

Evaluate against three criteria:
1. **Capability vs. outcome test** — Does the input describe what the product *does* (capability) or what the customer *achieves* (outcome)? Flag if it describes a feature or activation state.
2. **Measurability test** — Is there a direction, magnitude, or change-in-state implied? Flag if it is directionally vague ("improves," "helps," "enables") without specifying what changes.
3. **Role anchoring test** — Is there a clear customer role who achieves this? Flag if the subject is the product ("the system does X") rather than the customer role ("the Controller achieves X"). Also flag if the named role is correct but the lens is wrong — e.g., a rep-level activity framed for a CRO segment.

Present evaluation feedback before the transformed statement — the user sees the diagnosis, not just the result.

For detailed evaluation examples including all three failure modes and their recovery moves, see `references/worked-examples.md`.

**Step 3 — Transform Using the Outcome Statement Madlib**

Apply this template to produce each outcome statement:

```
OUTCOME STATEMENT TEMPLATE

When [TRIGGER: specific business situation or work context — not a product activation event],
[ROLE: named customer role at named organization type]
achieves [CHANGE: direction + metric + magnitude + timeframe]
through [MECHANISM: product capability or workflow used to achieve it],
enabling [FUNCTIONAL OUTCOME: what they can now do or stop doing — in their language]
that advances [BUSINESS GOAL: organizational objective in leadership-level language].
```

**Madlib slot definitions and fill guidance:**

| Slot | Definition | Fill Rule | Fail Signal |
|------|-----------|-----------|-------------|
| TRIGGER | The business situation that makes this outcome relevant | Describe the customer's work context before and without the product | Contains "when customer activates" or "when feature is enabled" |
| ROLE | Who in the customer org achieves this | Name the function and level — "Controller," "VP of CS," "CRO" | "Users," "customers," "the team" without specificity |
| CHANGE | The measurable change in state | Must contain: direction + metric + magnitude (user-supplied from their own evidence) + timeframe | Missing any of the four elements; using [TBD] without flagging it |
| MECHANISM | What capability or workflow produces the change | Name the specific feature, workflow, or integration — not just the product name | "Using our platform" or product name only |
| FUNCTIONAL OUTCOME | What the customer can now accomplish | Write in customer language — what they tell their team happened | Abstract nouns only ("efficiency," "visibility") without specificity |
| BUSINESS GOAL | The organizational objective this supports | Name the metric the CFO or CEO tracks | Department-level language when board-level is needed |

**Magnitude rule:** Supply actual ranges from your own customer evidence, documented results,
or internal benchmarks. Do not use illustrative numbers. If data is not yet available, use the
placeholder format `[TBD% — source required]` and flag the entry as unverified. Unverified
magnitude placeholders are acceptable in a working draft but must be resolved before any
outcome is used in a Sales commitment or CS plan.

**Step 4 — Stage Classification**

After each outcome statement, classify and explain which Value Chain stage it primarily represents:
- Stage 2 (Deliverable Outcome) — what the customer can accomplish using the product. Flag: this is the floor, not the target.
- Stage 3 (Desired Outcome) — what the customer is actually trying to achieve in their work. Target.
- Stage 4 (Business Goal) — the organizational objective this supports. Best.

If transformation only reaches Stage 2, note it and offer to push to Stage 3.

**Stage 4 note:** When an outcome reaches Stage 4, flag that the renewal conversation changes posture — Stage 4 outcomes are presented to the CFO alongside the CS leader, not just to the primary buyer. They require a dollar-value calculation as the next step (Business Impact Statement), which is beyond this skill's scope but should be noted as the required next layer.

**Step 5 — Present for Approval**

```
OUTCOME REVIEW — [Product/Service Name]

─────────────────────────────────────────
CAPABILITY INPUT [N]: [original text]

EVALUATION:
  Issues found: [list what fell short]
  Usable strength: [what carried over]

OUTCOME STATEMENT:
  When [trigger], [role] achieves [change] through [mechanism],
  enabling [functional outcome] that advances [business goal].

VALUE CHAIN STAGE: Stage [N] — [label] | [one-line rationale]
─────────────────────────────────────────

[Repeat for each capability]

─────────────────────────────────────────
APPROVAL OPTIONS:
  For each outcome, reply with one of:
  ✓  Approve as written
  E  [your edited version]
  R  Regenerate — [tell me what to change]
  X  Remove this one

  When all outcomes are resolved, say "Ready for Phase 2"
─────────────────────────────────────────
```

Do not proceed to Phase 2 until the user has explicitly resolved all outcomes and confirmed readiness.

---

### PHASE 2 — Value Assignment, Rubric Generation, and Output Artifacts

**Step 6 — Receive Approved Outcome Set**

Confirm which outcomes are in the approved set. If any were edited during Phase 1 review,
use the edited version. Never revert to the original after an edit has been approved.

**Step 7 — Assign Business Metrics**

For each approved outcome, identify the primary business metric that would verify achievement.

A valid business metric must be:
- **Named and specific** — "Days to close" not "efficiency"; "NRR %" not "retention"
- **Sourced** — attributable to a named system, report, or data source the customer controls
- **Directional** — the direction of change is unambiguous (lower is better / higher is better)
- **Customer-reportable** — something the customer presents to their own leadership

```
VALUE ASSIGNMENT TEMPLATE

Outcome: [approved outcome statement]
Primary Business Metric: [named metric]
Measurement Source: [system or report]
Baseline Capture Method: [how pre-implementation baseline is established]
Verified Through: [who verifies, using what artifact, at what milestone]
Direction of Success: [lower is better / higher is better / target range]
```

**Step 8 — Build the Four-Level Achievement Rubric**

For each outcome with its assigned metric, generate a rubric with four levels. Each level
describes observable, verifiable evidence — not traits, intentions, or effort.

```
RUBRIC TEMPLATE

Outcome: [statement]
Metric: [named metric]

LEVEL 0 — Not Achieved
  Definition: The change in state has not occurred. Leading indicators are absent
              or implementation conditions are not yet in place.
  Observable Evidence: [what CS would see — leading indicators absent, baseline unchanged]
  Verification Status: No measurement possible / Baseline captured only
  CS Action: [what CS does at this level — intervention trigger]

LEVEL 1 — Partial Achievement
  Definition: Leading indicators are present and moving in the right direction,
              but the primary metric has not yet reached the achievement threshold.
  Observable Evidence: [specific leading indicators with directional movement]
  Magnitude Range: [X–Y% or X–Y units toward the target]
  Verification Status: Leading indicators verified; lagging metric not yet
  CS Action: [what CS does at this level — on-track confirmation or coaching]

LEVEL 2 — Achieved
  Definition: The primary metric has reached or exceeded the documented achievement
              threshold within the specified timeframe.
  Observable Evidence: [specific data point, report, or artifact that confirms achievement]
  Magnitude Range: [minimum threshold that qualifies as achieved]
  Verification Status: Primary metric verified from [named source]
  CS Action: [what CS does — document, present at BVR, advance renewal conversation]

LEVEL 3 — Exceeded / Compounding Impact
  Definition: The primary metric has been achieved AND a secondary business impact
              is verifiable — the outcome has generated downstream value beyond
              the original scope.
  Observable Evidence: [primary metric + secondary metric or downstream effect]
  Secondary Impact: [what additional business metric has moved — must be named specifically]
  Verification Status: Both primary and secondary metrics verified
  CS Action: [what CS does — case study candidate, expansion signal, executive story]
```

**Step 9 — Present Rubric Set for Final Approval**

Present all rubrics in consolidated format. After presenting, collect approval:

```
RUBRIC SET — [Product/Service Name] — [count] outcomes

[For each outcome:]
──────────────────────────────────────────
OUTCOME [N]: [short label]
Statement: [approved outcome statement]
Metric: [assigned metric] | Source: [source]
Direction: [lower/higher is better]

L0 — Not Achieved:    [evidence description]
L1 — Partial:         [evidence + magnitude range]
L2 — Achieved:        [evidence + threshold]
L3 — Exceeded:        [evidence + secondary impact]
──────────────────────────────────────────

OPTIONS:
  ✓  Accept this rubric
  E  [edit a specific level — tell me which and what to change]
  M  [adjust the metric — tell me the replacement]
```

**Step 10 — Generate Output Artifacts**

After all rubrics are approved, offer:

```
OUTPUT OPTIONS

Your approved outcomes and rubrics are ready. I can produce:

  A  Outcome & Value Registry (Markdown)
     Structured .md document with consistent schema across all entries.
     Machine-readable by other skills and agents; human-readable for review.
     Designed for local version control alongside your specs.

  B  Review Deck (HTML)
     Presentation-ready HTML artifact for cross-functional review with
     Sales, Marketing, RevOps, and CS.
     Includes: outcome statements, value chain stage badges, metric tables,
     four-level rubric cards (L0–L3), and per-entry ratification status field.

  C  Both

Reply with A, B, or C.
```

**When A is selected — produce the Markdown Registry:**

**Filename convention:** `[product-slug]-outcome-value-registry.md`
e.g., for Gong.io CRO segment: `gong-outcome-value-registry.md`

For a live populated example of this file at full scale, open `gong-outcome-value-registry.md`
in the package root — all six Gong.io CRO entries with complete rubrics and registry metadata.

Each entry follows this schema (consistent headers required for machine readability):

```markdown
# Outcome & Value Registry
**Product / Service:** [name]
**Customer Segment:** [segment]
**Version:** [date]
**Status:** [Draft | Under Review | Ratified]
**Owner:** [name or team]

---

## Entry Index
| ID | Name | Value Chain Stage | Primary Metric | Status |

---

## [OCV-NNN] — [Entry Name]

### Outcome Statement
> [full outcome statement]

### Value Chain Classification
| Stage | [N — label] |
| Rationale | [one sentence] |

### Business Metric
| Metric | [named metric] |
| Source | [system or report] |
| Baseline Method | [how pre-implementation baseline is captured] |
| Direction | [lower / higher is better] |
| Verification Milestone | [milestone] |

### Achievement Rubric
| Level | Label | Observable Evidence | Magnitude | CS Action |

### Status
| Entry Status | [Draft | Under Review | Ratified | Deprecated] |
| Ratification Notes | [empty until review] |
| Magnitude Verified | [Yes / No — all values TBD] |
| Last Updated | [date] |

---

## Registry Metadata
[YAML block with registry_id, product, segment, entry_count,
 status_values, magnitude_status, schema_version, generated_by,
 generated_date, ratification_required_before]
```

**Schema conventions for machine consumers:**
- Entry IDs: `OCV-NNN` format — sequential, unique, stable
- Status field: constrained to `Draft | Under Review | Ratified | Deprecated`
- Table headers: identical across all entries — parse by column label
- Magnitude placeholders: pattern `[TBD` signals unverified — treat as unverified in any downstream output
- Value Chain Stage: format `Stage N — Label` — integer N is extractable

For a complete populated example of this schema with all six entries, see `references/reference-registry.md`.

**When B is selected — produce the HTML Review Deck:**

Generate a clean HTML artifact using SuccessCOACHING brand colors and Poppins font.

**Filename convention:** `[product-slug]-outcome-review-deck.html`
e.g., for Gong.io CRO segment: `gong-outcome-review-deck.html`

For the structure and formatting of a complete live example, open
`gong-outcome-review-deck.html` — this is the direct output from the Gong.io CRO test run
and should be used as the visual and structural template for all subsequent decks.

Required structure:

- Cover header: product name, version date, entry count, status badge
- Warning banner: TBD magnitude notice (persistent if any entries have unverified magnitudes)
- Navigation index: all entries as clickable cards with ID, name, and stage
- Per-entry layout:
  - Entry header: ID, name, stage pill (color-coded by stage), status badge
  - Outcome statement in a left-bordered callout block
  - Two-column: Business Metric table + Value Chain Rationale
  - Four-column rubric cards: L0 gray → L1 amber → L2 accent blue → L3 success green
  - Ratification status row with status badge and notes field
- Footer: registry metadata + ratification disclaimer

The deck is designed for screen-share in review sessions — each entry self-contained on scroll,
no navigation required between entries during discussion.

---

## Guardrails

### NEVER
- Present a Stage 2 outcome as catalog-ready without flagging it and offering to elevate it
- Accept "improves," "enables," or "helps" as magnitude indicators
- Allow a TRIGGER slot to describe product activation rather than customer business context
- Build a rubric before outcomes are explicitly approved — the approval gate is mandatory
- Use the product as the subject of the outcome statement — the customer role is always the subject
- Accept "customers" or "users" as the ROLE slot — a named function and level is required
- Generate Level 3 without specifying a named secondary metric — "additional value" is not a secondary metric
- Surface unverified [TBD] magnitudes in Sales or CS-facing outputs without flagging them
- Produce registry output artifacts before Step 9 rubric approval is complete

### ALWAYS
- Evaluate the raw capability input before transforming it — diagnosis before cure
- Classify the Value Chain stage for every outcome and explain why
- Require explicit confirmation before moving from Phase 1 to Phase 2
- Use the approved/edited version of each outcome as Phase 2 input — never revert to original
- Anchor every rubric level to observable evidence, not intent or effort
- Name the measurement source for every assigned metric
- Flag Stage 4 outcomes as requiring a dollar-value Business Impact Statement as the next layer
- Include the registry metadata YAML block in every Markdown registry output
- Add the schema notes section to every Markdown registry output for downstream consumers

### Failure Modes and Recovery

| Failure | Signal | Recovery |
|---------|--------|----------|
| Capability list is entirely feature descriptions | All inputs fail capability vs. outcome test | Flag the pattern explicitly; ask for business context before transforming; don't silently transform features into vague outcomes |
| Customer segment too vague to anchor ROLE slot | "our customers" or no segment provided | Ask for segment before generating any statement |
| Role is correct product area but wrong buyer lens | Rep-level activity, CRO-level segment | Flag the lens mismatch explicitly; elevate to the buyer's accountability metric |
| User skips approval and asks to jump to Phase 2 | "just generate the rubric" | Confirm: "I want to make sure we're working from approved outcomes. Can you confirm the outcome set?" |
| Metric cannot be named specifically | Domain too specialized | Name what can be verified; flag the gap rather than filling with a generic placeholder |
| Phase 2 metric conflicts with Phase 1 outcome | Assigned metric doesn't align to stated change | Surface the conflict before building the rubric; ask which should govern |
| User requests registry before rubric approval | "give me the markdown now" | Complete the rubric approval step first; registry artifacts are generated from approved rubrics, not from Phase 1 outcomes alone |

---

## Worked Examples

Two full Phase 1 examples are provided in `references/worked-examples.md`:

**Example A — OCV-001: Win Rate via Conversation Intelligence (Gong.io, CRO segment)**
Demonstrates: all three evaluation criteria failing on a single input; elevation from Stage 2
to Stage 3; TRIGGER slot distinguishing business context from product activation.

**Example B — OCV-002: Outbound Pipeline Efficiency (Gong.io, CRO segment)**
Demonstrates: partial role anchoring failure (correct product area, wrong buyer lens);
elevation from rep-level to CRO-level framing; Stage 4 classification when the metric
is a CFO/board metric.

The worked examples also include a side-by-side comparison table showing the two failure
patterns, recovery moves, stage reached, and renewal conversation implications together.

For the complete Phase 2 output — all six entries with value assignment, rubrics, and
registry metadata — see `references/reference-registry.md`.

---

## Session Memory

On repeat use within a session:
- Retain the approved outcome set across phases — do not re-request approved outcomes when building rubrics
- If the user references "the outcomes we built" or "our outcome set," the current session's approved outcomes are the referent
- If the user wants to add a new capability mid-session, run the full Phase 1 evaluation cycle for the addition before folding it into the approved set
- Registry artifacts generated in Phase 2 reflect the full approved set at the time of generation — if outcomes are added after artifact generation, offer to regenerate

---

## Security & Permissions

This skill operates on user-provided text inputs only. It does not call external APIs,
access files, or write to any system. No elevated permissions required.

- Network access: none
- Filesystem access: none
- Tool calls: none
- Data retention: session scope only — no cross-session persistence without explicit user action

---

## Trust & Verification

All outcome statements are generated from user-provided capability inputs. This skill does
not fabricate metrics, benchmarks, or industry data.

Magnitude ranges in worked examples are illustrative only. The user must supply or confirm
actual ranges from their own customer evidence before treating any metric as catalog-ready.

Rubric levels describe observable evidence patterns drawn from the user's approved outcome
statements and assigned metrics. The verification method and measurement source in each rubric
must be confirmed by the user against their actual operational systems before the rubric is
used in a live CS motion.

Registry entries marked `Draft` require cross-functional ratification (Sales, Marketing,
RevOps, CS) and magnitude verification before use in Sales commitments or CS plans.

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/worked-examples.md` | Phase 1 evaluation and transformation for OCV-001 and OCV-002 (Gong.io CRO segment). Includes madlib slot-by-slot annotation, all three evaluation failure modes, and stage classification reasoning. Use as the template for showing Phase 1 evaluation work. |
| `references/reference-registry.md` | Canonical registry schema documentation with complete 6-entry populated example from the Gong.io CRO test run. Shows the full Phase 1 + Phase 2 output in the exact schema this skill produces. Includes schema notes for downstream machine consumers. |
| `gong-outcome-value-registry.md` | Live Phase 2 registry output from the Gong.io CRO test run. All 6 entries (OCV-001 through OCV-006) with value assignment, rubrics, and registry metadata in the production format. Use as the visual and structural reference for registry output. |
| `gong-outcome-review-deck.html` | Live HTML review deck from the Gong.io CRO test run. Full branded deck with all 6 entries, rubric cards, TBD magnitude banner, and ratification status fields. Use as the visual and structural template for all HTML deck outputs — match the layout, color treatment, card structure, and typography exactly. |

---

