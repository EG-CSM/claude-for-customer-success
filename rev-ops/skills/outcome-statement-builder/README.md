# outcome-statement-builder

**Version:** 1.2.0 | **Status:** [PROPOSED] | **Author:** SuccessCOACHING

Transforms raw product or service capabilities into structured, verifiable outcome statements
using the Seven-Stage Value Chain. Operates in two phases with an explicit approval gate:
Phase 1 evaluates and transforms capabilities into outcome language; Phase 2 assigns business
metrics, generates four-level achievement rubrics, and produces two output artifacts.

---

## Folder Structure

```
outcome-statement-builder/
│
├── README.md                          ← This file
├── SKILL.md                           ← Skill definition (559 lines)
│
├── references/
│   ├── worked-examples.md             ← Phase 1 walkthrough: OCV-001 and OCV-002
│   └── reference-registry.md          ← Canonical schema: all 6 entries with rubrics
│
├── gong-outcome-value-registry.md     ← Live Phase 2 registry output (Gong.io CRO)
└── gong-outcome-review-deck.html      ← Live HTML review deck (Gong.io CRO)
```

---

## File Descriptions

### `SKILL.md`
The executable skill definition. Contains the full two-phase workflow, input/output schemas,
madlib template for outcome statement construction, rubric generation instructions, output
artifact specifications, guardrails, and failure mode recovery. Load this file to activate
the skill in claude.ai or Cowork.

**Key sections:**
- Overview and activation triggers
- Input/Output Schema (Phase 1 and Phase 2)
- Core Workflow — 10 steps across two phases with approval gate at Step 5
- Madlib template with slot definitions and fill rules
- Seven-Stage Value Chain classification guidance
- Four-level rubric template (L0 Not Achieved → L3 Exceeded)
- Step 10 — Output artifact generation (Markdown registry and HTML review deck)
- Guardrails: NEVER / ALWAYS / Failure Modes

---

### `references/worked-examples.md`
Two complete Phase 1 walkthroughs using Gong.io capabilities for a CRO customer segment.
Use this when running Phase 1 to understand what the evaluation, transformation, and stage
classification steps should look like in practice.

**Contains:**
- **Example A — OCV-001: Win Rate via Conversation Intelligence**
  Shows all three evaluation failure modes firing simultaneously on a single input (capability
  vs. outcome, measurability, role anchoring). Full slot-by-slot madlib annotation. Elevation
  from Stage 2 to Stage 3 with rationale.
- **Example B — OCV-002: Outbound Pipeline Efficiency**
  Shows partial role anchoring failure — correct product area, wrong buyer lens (rep-level
  framing for a CRO segment). Recovery to Stage 4 with board-level metric. Stage 4 flag and
  Business Impact Statement note.
- **Comparison table** — both examples side-by-side showing failure patterns, recovery moves,
  stage reached, and renewal conversation implication.

---

### `references/reference-registry.md`
The canonical schema reference and complete populated example. All 6 entries from the
Gong.io CRO test run — full Phase 1 + Phase 2 output with value assignment, rubrics, and
registry metadata — in the exact schema the skill produces.

**Contains:**
- Entry Index table (all 6 OCV entries with stage and status)
- OCV-001 through OCV-006 in full schema format
- Schema notes section for machine consumers (entry ID conventions, status field constraints,
  table header consistency, TBD magnitude pattern, stage format)
- Registry metadata YAML block

**Use as:** The authoritative template for what a completed registry entry looks like. When
producing a new registry for a different product, match this schema exactly.

---

### `gong-outcome-value-registry.md`
The live Phase 2 registry output produced during the Gong.io CRO test run. This is the
production artifact — not a template, but an actual output. Entries OCV-001 through OCV-006
with all values populated, TBD magnitudes flagged, and status set to `Draft`.

**Contains:**
- Header block: product name, segment, version, status, owner
- Entry Index (all 6 entries)
- OCV-001 through OCV-006 in production registry format
- Registry metadata YAML block with `magnitude_status: unverified` flag

**Use as:** The live reference for what the Markdown registry output looks like at scale.
When running the skill for a new product, the output file follows the same structure with
`[product-slug]-outcome-value-registry.md` naming.

**Pending:** All 6 entries have `[TBD — source required]` magnitude values. These must be
replaced with verified customer evidence before any entry is used in a Sales commitment or
CS plan. Requires cross-functional ratification (Sales, Marketing, RevOps, CS) to advance
from `Draft` to `Ratified` status.

---

### `gong-outcome-review-deck.html`
The live HTML review deck produced during the Gong.io CRO test run. Presentation-ready for
screen-share with Sales, Marketing, RevOps, and CS in cross-functional ratification sessions.

**Contains:**
- Cover header: Gong.io Outcome & Value Registry — CRO Review, version date, entry count
- TBD magnitude warning banner (persistent — displayed because all magnitudes are unverified)
- Navigation index: all 6 entries as clickable summary cards
- Per-entry layout: outcome statement callout, business metric table, value chain rationale,
  four rubric level cards (L0 gray → L1 amber → L2 accent blue → L3 success green), and
  ratification status row
- Footer: registry metadata and ratification disclaimer
- SuccessCOACHING brand: Poppins font, primary `#24718E`, accent `#34A7D2`, success `#90C83D`

**Use as:** The visual and structural template for all subsequent HTML deck outputs. When
running the skill for a new product, match this layout, color treatment, card structure,
and typography exactly. Naming convention: `[product-slug]-outcome-review-deck.html`.

---

## How the Files Work Together

```
Phase 1 Run                   Phase 2 Run                    Output
─────────────────             ─────────────────────────────  ───────────────────────────
User provides                 User approves → skill runs      gong-outcome-value-registry.md
capabilities                  Step 6–9:                         (machine-readable registry)
    ↓                           - Value assignment
SKILL.md Steps 1–5             - Rubric generation            gong-outcome-review-deck.html
  (guided by                    - Artifact generation           (HTML presentation deck)
   worked-examples.md)
    ↓                         guided by:
User approves                 - reference-registry.md
outcome set                     (schema reference)
    ↓
→ Ready for Phase 2
```

**When the skill asks "what should this look like?"**
- Phase 1 evaluation and transformation → `references/worked-examples.md`
- Phase 2 registry schema and entry structure → `references/reference-registry.md`
- Full live registry at scale → `gong-outcome-value-registry.md`
- HTML deck visual template → `gong-outcome-review-deck.html`

---

## Quick-Reference: Output Naming Conventions

| Artifact | Convention | Gong.io Example |
|----------|-----------|-----------------|
| Markdown registry | `[product-slug]-outcome-value-registry.md` | `gong-outcome-value-registry.md` |
| HTML review deck | `[product-slug]-outcome-review-deck.html` | `gong-outcome-review-deck.html` |

---

## Current Test Run — Gong.io CRO Segment

| Entry | Name | Stage | Metric | Status |
|-------|------|-------|--------|--------|
| OCV-001 | Win Rate via Conversation Intelligence | Stage 3 | Competitive win rate % | Draft |
| OCV-002 | Outbound Pipeline Efficiency | Stage 4 | Qualified pipeline per SDR | Draft |
| OCV-003 | Late-Stage Deal Slippage Reduction | Stage 3 | Late-stage deal slippage rate | Draft |
| OCV-004 | Forecast Variance Reduction | Stage 4 | Forecast variance % | Draft |
| OCV-005 | Rep Ramp and Performance Scaling | Stage 3 | Time-to-quota-attainment | Draft |
| OCV-006 | Regulated Segment Revenue Coverage | Stage 3 | Regulated-segment pipeline coverage | Draft |

**All magnitudes:** `[TBD — source required]` — unverified, not ready for Sales or CS use.

---

## Installation Note

The installed version of this skill at `/mnt/skills/user/outcome-statement-builder/` is
**v1.1.0** and contains only `SKILL.md`. The reference files and live output artifacts in
this package are not yet co-located with the installed skill. To fully activate the skill
with all reference material, copy the complete package contents to the installation directory:

```
outcome-statement-builder/
├── SKILL.md                           (update to v1.2.0)
├── references/
│   ├── worked-examples.md
│   └── reference-registry.md
├── gong-outcome-value-registry.md
└── gong-outcome-review-deck.html
```

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `outcome-catalog-entry-builder` | Use for editing or validating individual existing entries — this skill builds new ones |
| `provisional-outcome-catalog-generator` | Use for generating a full catalog from research data — this skill works entry-by-entry with user approval |
| `evidence-confidence-scorer` | Use after this skill to score evidence quality on the [TBD] magnitude values |

---

*outcome-statement-builder v1.2.0 | SuccessCOACHING Skills Ecosystem*
*Research foundation: SuccessCOACHING Seven-Stage Value Chain, Outcome Catalog methodology*
