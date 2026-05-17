---
title: "Reasoning Blueprint: CS Ops Process Documentation"
type: reasoning-blueprint
skill: process-doc
version: 1.0.0
---

# Reasoning Blueprint: CS Ops Process Documentation

Load this blueprint when Tier 3 reasoning is activated for CS Ops process
documentation work. It provides the domain-specific taxonomy, heuristics, and
expert judgment patterns that shape expert-level process codification.

---

## Problem Classification Taxonomy

### Type A: Workflow SOP
**Characteristics**: A repeatable operational workflow needs codifying — handoffs, reclassifications, onboarding steps, or recurring CS Ops processes with defined triggers and sequential steps.
**Primary Risk**: Steps are listed without ownership, timing, or exception handling — the SOP describes what happens but not who acts, when, or what to do when it breaks.
**Expert Focus**: Every step has a named role, a timing constraint, and at least one exception path. If a step lacks these, it is incomplete.

### Type B: Governance Record
**Characteristics**: A decision-making process needs a permanent, auditable trail — playbook changes, policy decisions, approval workflows. The output is a framework plus individual change records.
**Primary Risk**: The framework exists but nobody uses it — governance without adoption is worse than no governance because it implies oversight that does not exist.
**Expert Focus**: Enforce that every change type has a named approver and that the record format is concrete enough to fill out in under 5 minutes.

### Type C: Reference Standard
**Characteristics**: A normative document that other tools audit against — data quality definitions, field ownership matrices, threshold configurations. The output is the authoritative source of truth.
**Primary Risk**: The standard drifts from the systems it governs — field names, thresholds, or ownership assignments in the standard no longer match the CRM/CS platform reality.
**Expert Focus**: Include a change process and version log in every standard; without them, the document decays silently.

### Type D: Escalation / Response Protocol
**Characteristics**: A time-sensitive response procedure with severity tiers, SLA commitments, owner assignments, and communication cadences. Urgency is the defining constraint.
**Primary Risk**: Severity definitions are vague or overlapping, causing misclassification under pressure — an S2 treated as S3 misses the response window.
**Expert Focus**: Severity tiers must have mutually exclusive criteria and concrete examples. Response time SLAs must match the configured escalation matrix.

---

## Domain Heuristics

1. **The Ownership Test**: Every step, field, or decision in a process document must name a specific role as owner. If a step says "ensure X is updated" without naming who, it will not be done. No owner = no maintenance.

2. **The Five-Minute Fill Rule**: Any record format (change record, log entry, checklist) must be completable in under 5 minutes. If it takes longer, practitioners will skip fields or avoid the process entirely.

3. **The Exception-First Rule**: Draft the exception handling before the happy path. SOPs that only describe ideal execution fail on first contact with reality. Every step should answer "what if this doesn't work?"

4. **The Placeholder Purge Gate**: A document with `[configured threshold]` or `[N]` markers is a template, not a policy. No process document is publishable until every placeholder references a concrete value from the org's configuration.

5. **The Cross-Reference Anchor**: Escalation SOPs must match the escalation matrix in CLAUDE.md. Data quality standards must match CRM field names. If the process doc references a system value, verify it against the configured source — divergence means the doc is wrong.

6. **The Adoption Proof Rule**: A governance framework without evidence of use (log entries, change records, version increments) is theater. Include a "first use" prompt that forces the first real record to be created during rollout.

7. **The Downward-Change Sensitivity Rule**: Any process that reduces customer engagement (downward reclassification, reduced touch cadence, coverage removal) requires an explicit relationship-risk flag and CS lead sign-off, regardless of commercial justification.

---

## Common Failure Modes by Classification Type

### Workflow SOP Failures
- **Orphaned steps**: Steps listed without role assignment or timing constraint.
  → Fix: Add a RACI or role column to every step table; reject steps without an owner.
- **Missing urgent path**: No fast-track procedure for time-zero scenarios (e.g., unplanned departure).
  → Fix: Add a "skip to Step N for urgent triggers" shortcut at the top of the SOP.
- **Checklist without log**: Completion checklists exist but no audit trail proves execution.
  → Fix: Require a log entry or record alongside checklist completion.

### Governance Record Failures
- **Single-word rationale**: Change records with rationale like "Unused" or "Outdated."
  → Fix: Enforce minimum 2-sentence rationale referencing data (activation rate, audit finding, strategic priority).
- **Approval without authority**: Change records list an approver who does not have configured authority for that change type.
  → Fix: Cross-reference the approver against the change-type authority matrix before accepting.

### Reference Standard Failures
- **Phantom fields**: The standard references CRM fields that do not exist or have been renamed.
  → Fix: Validate field names against the configured CRM schema before publishing.
- **Threshold without rationale**: Staleness thresholds or completeness targets stated without explaining why that number.
  → Fix: Add a "Rationale" column to every threshold table.

### Escalation Protocol Failures
- **Overlapping severity tiers**: S2 and S3 definitions share criteria, causing inconsistent classification under pressure.
  → Fix: Add mutually exclusive decision criteria and worked examples for boundary cases.
- **SLA without routing**: Response time SLAs stated but no named owner or channel for each tier.
  → Fix: Every severity tier row must include primary owner, escalation channel, and executive sponsor.

---

## Expert Judgment Patterns

### Scope Decisions
- If the user asks for "process documentation" without specifying a type, probe for the specific mode — generic SOPs are rarely useful without a concrete process to codify.
- If the request spans two modes (e.g., handoff + escalation), produce separate documents — combined SOPs are harder to maintain and harder to follow under pressure.

### Depth Decisions
- Match document depth to the audience's operational maturity. A team with no existing process needs step-level detail; a team refining an existing SOP needs delta documentation.
- Governance frameworks for teams with fewer than 3 plays do not need the full change-record apparatus — scale the framework to the portfolio size.

### Sequencing Decisions
- Always resolve configuration dependencies before drafting: escalation matrix, segment definitions, CSM roster, and playbook state must be loaded before the document references them.
- For handoff SOPs, build the transfer roster and priority classification before the redistribution plan — the plan depends on the roster.

### Stakeholder Decisions
- Process documents serve operators (CS Ops), not customers. Never include customer-facing language in an SOP without an explicit audience-switch marker.
- Downward reclassification and escalation documents require CS lead review before distribution — flag with `[review]` markers at every approval gate.

---

*Reasoning Blueprint: CS Ops Process Documentation v1.0*
*For use with process-doc when Tier 3 reasoning is activated*
