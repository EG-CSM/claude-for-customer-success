---
title: CSM Plugin Reasoning Blueprint — Framework Reference
type: reasoning-blueprint
scope: csm-plugin-root
version: 1.0.0
---

# CSM Plugin Reasoning Blueprint

This document is the root-level reasoning framework reference for the
`claude-for-customer-success` plugin. It defines the D1 primer structure that all
csm skills implement, the general cross-skill CSM reasoning principles that inform
those primers, and guidance on loading per-skill blueprints.

Individual skills reference their own `references/reasoning-blueprint.md` for
skill-specific problem classification taxonomy, domain heuristics, common failure
modes, and expert judgment patterns. This document governs the framework itself —
not the skill-specific content.

---

## The D1 Primer Framework

Every csm skill Reasoning Protocol section applies four primers before generating
output. The primers are numbered, bold, and applied in this fixed sequence:

```
1. **CLASSIFY** — Determine input type before selecting an approach
2. **CONSTRAINTS** — Apply governing limits before generating any output
3. **EXPERT CHECK** — Apply domain heuristics a veteran CSM applies first
4. **ANTI-PATTERNS** — Catch domain mistakes before they appear in output
```

The sequence is deliberate: classification determines which constraints apply;
constraints narrow the solution space; expert checks surface what the model
most commonly misses; anti-pattern scanning catches failure modes before output
is generated.

After output is produced, every skill applies a post-execution verification block:

```
**After execution**, verify:
- Does the output answer the actual request?
- [Skill-specific verification checks]
- Confidence: [High] if [condition] / [Medium] if [condition] / [Low] if [condition] — state which.
```

The confidence calibration is a three-band system:
- **[High]** — live integrations connected, all configured components present, data current
- **[Medium]** — partial integrations, some stale data, or mixed user-provided and live context
- **[Low]** — user-provided context only, no integrations connected, or significant data gaps

---

## Cross-Skill CSM Reasoning Principles

These principles apply across all csm skills regardless of function. They inform
how each skill's CLASSIFY, CONSTRAINTS, EXPERT CHECK, and ANTI-PATTERNS blocks
are written.

### On Classification

**What changes with input type changes everything downstream.** A single-account
review and a portfolio triage share no overlap in what matters. A reactive
alert-triggered review requires different expert checks than a proactive pre-renewal
review. Classification is not a formality — it gates which heuristics apply,
which constraints are active, and what output format is appropriate.

**Partial data is a classification input, not a failure state.** When data is
sparse, classify the input as data-sparse and adjust confidence accordingly.
Do not treat missing data as "nothing to say" — missing data is itself a signal
worth naming.

### On Constraints

**Constraints prevent harm, not just errors.** The most consequential constraints
in csm skills are not about output quality — they are about preventing internal
data from reaching customers (confidentiality firewall), preventing escalation
recommendations without a named escalation path (no path = no recommendation),
and preventing revenue figures from appearing in output without CRM validation.
These are hard stops, not quality guidance.

**Config-driven constraints are not optional.** Every csm skill reads
`CLAUDE.md` and `company-profile.md` before proceeding. When config is missing
or contains `[PLACEHOLDER]` markers, the skill halts and routes to
`/csm:cold-start-interview`. This is a constraint, not a preference.

**Data staleness has a threshold.** NPS older than 6 months = Unknown, not stale.
Health data older than 30 days must be flagged with source date and staleness
indicator. These thresholds are encoded in skill CONSTRAINTS blocks, not left to
the CSM's judgment.

### On Expert Checks

**Score-anchoring is the dominant failure mode.** Composite health scores hide
the signal that matters. Expert check blocks always decompose the composite to
identify the single leading component, then assess whether that component's
signal is trustworthy (live data vs. stale).

**Convergence signals outweigh individual signals.** Multiple moderate signals
across independent components (H7) carry more diagnostic weight than a single
strong signal in one component. Expert checks are structured to surface convergence
before producing a classification.

**Renewal proximity amplifies everything.** Accounts within 90 days of renewal
apply the renewal proximity amplifier (H6): Yellow-tier urgency is treated as
Red-tier. Expert check blocks in renewal-adjacent skills encode this amplifier
explicitly.

**Sponsor departure overrides component scores (H4).** If an executive sponsor
has departed or is at risk, the account risk classification should reflect that
regardless of what the composite score shows. Expert check blocks in health and
risk skills always surface sponsor status before finalizing a classification.

### On Anti-Patterns

**The anti-pattern block is a pre-output scan, not a style guide.** Each item
in the anti-patterns block describes a specific failure mode the skill has been
observed to produce without correction. The CSM domain has a well-documented set
of failure modes across account review, escalation, renewal, and expansion
contexts. Anti-pattern blocks encode the domain-specific ones for each skill.

**Generic outputs are the dominant anti-pattern.** "Monitor closely," "improve
engagement," and "continue to build the relationship" are not interventions —
they are placeholders. Every csm skill's anti-patterns block explicitly prohibits
generic language and requires specific who/what/when actions.

**Framing churn probability is the highest-stakes anti-pattern.** No csm skill
classifies an account as likely to churn or assigns a churn probability. Output
shows component signals and position relative to configured thresholds. The churn
inference is the CSM's judgment, not the skill's output. This constraint appears
in both CONSTRAINTS and ANTI-PATTERNS blocks for every risk-adjacent skill.

---

## Per-Skill Blueprint Structure

Each csm skill loads its own reasoning blueprint on demand from
`references/reasoning-blueprint.md` (or `reference/reasoning-blueprint.md`
for skills in the expansion and success-plan subgroups). The per-skill blueprint
contains:

| Section | Purpose |
|---------|---------|
| `## Problem Classification Taxonomy` | Input types (A/B/C/D or skill-specific), with characteristics, primary risk, and expert focus per type |
| `## Domain Heuristics` | H1–H7 (or more), skill-specific patterns a veteran CSM would apply — named and numbered for reference in the EXPERT CHECK primer |
| `## Common Failure Modes` | Per-classification-type failures the skill has been observed to produce — source material for the ANTI-PATTERNS primer |
| `## Expert Judgment Patterns` | Scope/Sequencing/Depth/Stakeholder/Confidence decision patterns — how a senior CSM would approach the edge cases this skill encounters |

The per-skill blueprint is **loaded on demand** — referenced from the
`> Blueprint: references/reasoning-blueprint.md` line in the Reasoning Protocol
section. It is not front-loaded into every response. Skills reference it when
applying the expert check and anti-patterns primers, and when the complexity of
an input warrants deeper classification guidance.

---

## Applying the Framework Across Skills

The four primers operate identically across all csm skills. What differs is the
skill-specific content loaded into each primer block. This table maps the
framework elements to their per-skill sources:

| Primer | Framework Element | Per-Skill Source |
|--------|------------------|-----------------|
| CLASSIFY | Input type taxonomy (A/B/C/D) | `## Problem Classification Taxonomy` in per-skill blueprint |
| CONSTRAINTS | Governing limits (G1–G7) | CONSTRAINTS block in SKILL.md (encoded at authoring time) |
| EXPERT CHECK | Domain heuristics (H1–H7) | `## Domain Heuristics` in per-skill blueprint |
| ANTI-PATTERNS | Failure modes by classification type | `## Common Failure Modes` in per-skill blueprint |
| After execution verify | Verification checks + confidence | SKILL.md post-execution block (calibrated at authoring time) |

The constraint codes (G1–G7) and heuristic codes (H1–H7) are skill-specific
numbering schemes within each per-skill blueprint. They are not a shared
cross-skill taxonomy — each skill's blueprint uses its own numbered set.

---

## Confidence Calibration Reference

All csm skills report confidence in the three-band format. The conditions for
each band are skill-specific (encoded in the After execution verify block), but
the band semantics are consistent:

| Band | Meaning | Typical Conditions |
|------|---------|-------------------|
| `[High]` | Live integrations, all components present, data current | CS Platform connected + CRM live + all configured components within freshness threshold |
| `[Medium]` | Partial or mixed data | Some integrations missing, some data stale, or mixed user-provided + live context |
| `[Low]` | User-provided context only | No integrations connected, or critical components unavailable or significantly outdated |

Output always includes the band and the condition that triggered it:
`Confidence: [High] if CS Platform live with all configured components / [Medium] if partial integrations or some stale data / [Low] if user-provided context only — state which.`

---
