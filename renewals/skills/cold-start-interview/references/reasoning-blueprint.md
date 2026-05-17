---
title: "Reasoning Blueprint: Renewals Cold-Start Interview"
type: reasoning-blueprint
skill: cold-start-interview
version: 1.0.0
---

# Reasoning Blueprint: Renewals Cold-Start Interview

Load this blueprint when Tier 3 reasoning is activated for renewals configuration
interview work. It provides the domain-specific taxonomy, heuristics, and expert
judgment patterns that shape expert-level plugin configuration interviews.

---

## Problem Classification Taxonomy

### Type A: First-Run Full Configuration
**Characteristics**: No existing config file; user has never run the interview. All 8 sections needed.
**Primary Risk**: Interview fatigue causing incomplete or rushed answers in later sections.
**Expert Focus**: Pacing and section prioritization — anchor high-impact sections (churn signals, escalation matrix) before fatigue sets in.

### Type B: Targeted Reconfiguration
**Characteristics**: Existing config present; user wants to update one section or re-run after org changes.
**Primary Risk**: Updating one section without propagating dependencies to related sections (e.g., changing pricing model without updating discount authority).
**Expert Focus**: Cross-section dependency detection — flag downstream impacts before writing.

### Type C: Integration Verification
**Characteristics**: Check-integrations mode; no config content changes, only connector status.
**Primary Risk**: Reporting a connector as "connected" when it returns stale or partial data.
**Expert Focus**: Distinguish configured vs. verified vs. live — a connector that responds is not necessarily returning current data.

### Type D: Quick-Start Bootstrap
**Characteristics**: User wants minimum viable config to start using skills immediately.
**Primary Risk**: Placeholder values that never get filled, silently degrading skill output quality indefinitely.
**Expert Focus**: Choose the 8 quick-start questions that maximize skill output quality per question asked.

---

## Domain Heuristics

1. **The Fatigue Cliff Rule**: Interview quality drops sharply after 10 minutes of sequential questions. Front-load the sections that most affect downstream skill output (book, churn signals, escalation) before pricing details and methodology preferences.

2. **The Dependency Chain Rule**: Discount authority, escalation thresholds, and price increase policy form a dependency chain. If one changes, prompt review of the others. Never write one in isolation during `--section` mode without surfacing the chain.

3. **The Placeholder Decay Rule**: Any field written as `[PLACEHOLDER]` has a <20% chance of being updated within 30 days. Quick-start mode must collect the values that cause the worst skill degradation when missing — GRR/NRR targets, churn signals, escalation owner.

4. **The Unbounded Authority Smell**: When a user claims "unlimited" discount authority or "no escalation needed," it almost always means the threshold exists but hasn't been articulated. Probe once; if they insist, log it with an advisory note.

5. **The Connector Trust Hierarchy**: CRM data is the identity anchor (most stable). CS Platform data is the health overlay (moderate churn). Call recording data is the recency signal (most volatile). Verify in that order; never trust a downstream source over an upstream one.

6. **The Company Profile Skip Rule**: If the shared company profile exists and is <30 days old, skip Section 1 entirely. If >30 days, confirm key facts (product description, pricing model) rather than re-asking everything.

---

## Common Failure Modes by Interview Type

### First-Run Full Configuration Failures
- **Section order rigidity**: Running sections in fixed order regardless of user energy or context.
  -> Fix: After Section 3 (book), ask "Want to continue or save progress and finish later?"
- **Accepting vague churn signals**: Recording "low adoption" without asking for the specific metric or threshold.
  -> Fix: For each churn signal, ask: "What does that look like in a number or behavior?"
- **Missing escalation SLAs**: Recording who handles escalation but not response time expectations.
  -> Fix: Always ask the three-part question: who, how notified, expected response time.

### Targeted Reconfiguration Failures
- **Orphaned dependencies**: Updating pricing model without checking if discount authority still makes sense.
  -> Fix: After any section write, scan the dependency chain and flag mismatches.
- **Stale defaults displayed**: Showing current values from a config that was written months ago without flagging the age.
  -> Fix: Always show the config write date alongside current values.

### Integration Verification Failures
- **Configured-vs-verified conflation**: Marking a connector as verified because it's listed, without running a test call.
  -> Fix: Only mark "verified" after a successful test call; otherwise mark "configured (unverified)."

### Quick-Start Bootstrap Failures
- **Too many placeholders**: Collecting role and integrations but skipping GRR/NRR targets and churn signals, which most skills need.
  -> Fix: Quick-start question set must include the 3 values that gate the most skill outputs.

---

## Expert Judgment Patterns

### Pacing Decisions
- If user gives terse answers, they're fatigued or time-pressed — offer to switch to quick mode.
- If user gives elaborate answers with context, they're engaged — probe deeper on churn signals and escalation.

### Validation Decisions
- Always echo back discount authority and escalation thresholds in a confirmation summary — these are the highest-consequence values in the config.
- When GRR target exceeds 95%, probe once: "That's an aggressive target — is that the stretch goal or the operating plan number?" The distinction affects how skills frame risk.

### Scope Decisions
- If user has 3+ connected integrations, recommend full mode even if they asked for quick — the integrations section alone justifies the time.
- If user has zero integrations, quick mode is sufficient — most elaboration in full mode relates to integration-dependent features.

---

*Reasoning Blueprint: Renewals Cold-Start Interview v1.0*
*For use with cold-start-interview when Tier 3 reasoning is activated*
