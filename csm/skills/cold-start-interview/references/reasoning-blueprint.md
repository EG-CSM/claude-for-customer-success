---
title: "Reasoning Blueprint: Cold-Start Interview"
type: reasoning-blueprint
skill: cold-start-interview
version: 1.0.0
---

# Reasoning Blueprint: Cold-Start Interview

Load this blueprint when Tier 3 reasoning is activated for cold-start interview work.

## Problem Classification Taxonomy

### Type A — Fresh Install (No Prior Config)
- **Characteristics**: No config file exists at the target path. No shared company profile. User has never run the plugin before.
- **Primary Risk**: Interview fatigue — asking too many questions causes the user to bail before writing a usable profile. Defaults must be strong enough that a partial interview still produces functional output.
- **Expert Focus**: Detecting whether the user has structured artifacts (playbooks, escalation docs, CRM exports) that can replace 80% of the questions. An expert front-loads the "paste or link" prompt before falling back to Q&A.

### Type B — Resume from Pause
- **Characteristics**: Config file exists with `<!-- SETUP PAUSED AT: -->` marker. Some sections populated, others marked `[PENDING]`.
- **Primary Risk**: Context loss — the user forgot what they already answered. Repeating answered questions erodes trust; skipping unanswered ones without acknowledgment feels broken.
- **Expert Focus**: Confirming previously written answers are still accurate before continuing, without re-asking every question. A brief "here's what I have so far — still right?" checkpoint before resuming.

### Type C — Redo (Full or Section)
- **Characteristics**: Populated config exists. User invoked `--redo` or `--redo <section>`. Profile is functional but needs recalibration.
- **Primary Risk**: Overwriting good data. A section redo should not blank adjacent sections. A full redo should confirm before discarding a working profile.
- **Expert Focus**: Showing the current value before asking the replacement question — "Your escalation threshold is currently $50K ARR. What should it be?" preserves context and catches accidental redos.

### Type D — Integration Check Only
- **Characteristics**: User invoked `--check-integrations`. No interview questions needed. Pure connector probe.
- **Primary Risk**: False positives — reporting a connector as connected when it's configured but not actually responding. False negatives — reporting disconnected when there's a transient auth issue.
- **Expert Focus**: Testing with actual read calls, not config file inspection. Distinguishing "not configured" from "configured but auth expired" from "connected and responding."

### Type E — Quick Path (Minimal Setup)
- **Characteristics**: User chose the 2-minute quick path. Only Part 0 and CS motion are asked. Everything else gets `[DEFAULT]` markers.
- **Primary Risk**: Defaults that don't match the user's reality — a tech-touch CSM getting high-touch QBR cadence defaults, or an enterprise CSM getting pooled health thresholds.
- **Expert Focus**: Motion-aware defaults. The quick path answer (high-touch / tech-touch / hybrid / handoff) should drive every default value written, not a single generic default set.

## Domain Heuristics

**The Artifact-First Rule**: If a question is about something that's probably written down (playbook, escalation matrix, health model config, territory sheet), prompt for a paste or link before asking the user to reconstruct it from memory. Documents are more accurate and faster than recall.

**The Two-Question Ceiling Rule**: Never present more than 2-3 answerable prompts per turn. Count subparts. One question with 5 subparts is 5 questions, not 1. Violating this causes users to answer the first two and skip the rest.

**The Motion-Shapes-Everything Rule**: The CS motion answer (high-touch / tech-touch / hybrid / handoff) is the single highest-leverage configuration input. Every default — QBR cadence, health check frequency, engagement depth, escalation urgency — should vary by motion. A motion mismatch downstream is always a cold-start interview failure.

**The Partial-Is-Functional Rule**: A config with `[DEFAULT]` markers is better than no config. A config with `[SKIPPED]` markers is better than a paused interview that never resumes. Always write something usable, even if incomplete.

**The Show-Before-Ask Rule**: On redos and resumes, show the current value before asking for the new one. "Your health model weights are Usage 40% / Support 20% / NPS 20% / Engagement 20%. Change?" is faster and less error-prone than "What are your health model weights?"

**The Probe-Don't-Declare Rule**: For integration checks, only report a connector as connected (checkmark) if an actual tool call succeeded. Config file entries, `.mcp.json` declarations, and "it was working yesterday" are not evidence of current connectivity.

**The Scope-Flag Rule**: If the working directory is project-scoped (not home directory), flag the filesystem access limitation exactly once, early, before the user invests time answering questions about files they can't reach.

## Common Failure Modes by Request Type

### Fresh Install Failures
- **Interview abandonment**: User quits mid-interview because it felt too long. **Fix**: Always offer the quick/full fork upfront. Track completion rates by path length.
- **Generic defaults written as real values**: Default health thresholds written without `[DEFAULT]` markers, making them indistinguishable from user-provided values. **Fix**: Every default must be explicitly marked so downstream skills can flag low-confidence config reads.
- **Company questions re-asked across plugins**: Shared company profile not written or not checked before asking. **Fix**: Always check `company-profile.md` existence before Part 0 company questions.

### Resume Failures
- **Stale context**: User's role, motion, or portfolio changed since the pause. Resumed interview writes outdated answers into new sections. **Fix**: Show a summary of prior answers and ask "still accurate?" before continuing.
- **Marker confusion**: `[PENDING]` markers from a pause mixed with `[PLACEHOLDER]` markers from the template, creating ambiguous config state. **Fix**: Use distinct markers — `[PENDING]` for paused fields, `[PLACEHOLDER]` for never-started fields, `[DEFAULT]` for quick-path defaults, `[SKIPPED]` for deliberate skips.

### Redo Failures
- **Accidental full overwrite**: User meant to redo one section but triggered a full redo, losing a working profile. **Fix**: On `--redo` without a section argument, show the current profile summary and confirm "redo everything?" before proceeding.
- **Section boundary bleed**: Redoing the health model section accidentally clears the escalation matrix because they share a config block. **Fix**: Section writes must be atomic — read the full config, modify only the target section, write back the full config.

### Integration Check Failures
- **False positive on stale auth**: Connector is in `.mcp.json` and the MCP server starts, but the OAuth token expired. Reported as connected. **Fix**: Test with an actual data read, not just a handshake.
- **Missing how-to-connect guidance**: Connector reported as missing but no instructions given for how to add it. **Fix**: Every missing connector report must include the connection path for the user's platform (Cowork vs Claude Code).

## Expert Judgment Patterns

### Sequencing Decisions
- **When to skip company questions**: Company profile exists AND user confirms it's current. Never skip silently — always show and confirm.
- **When to recommend full over quick**: User mentions specific health models, escalation chains, or playbook sources in early answers. They have the structured thinking that makes the full path high-value.
- **When to recommend quick over full**: User is evaluating the plugin, doesn't have CS artifacts to reference, or explicitly asks to "just get started."

### Default Calibration
- **High-touch defaults**: QBR cadence quarterly, health check weekly, escalation SLA 24h, engagement depth deep.
- **Tech-touch defaults**: QBR cadence semi-annual or none, health check monthly (automated), escalation SLA 48h, engagement depth programmatic.
- **Hybrid defaults**: Segment by ARR tier — apply high-touch defaults above the segmentation threshold, tech-touch below.

### Edge Case Handling
- **User pastes a massive document**: Extract relevant fields, confirm extraction accuracy, don't echo the full document back. Write a summary reference, not a copy.
- **User doesn't know their health model weights**: Offer the industry-standard starting point (Usage 40% / Engagement 25% / Support 20% / Relationship 15%) marked as `[DEFAULT]` with a note to calibrate after 30 days.
- **User has multiple roles**: Pick the primary role for config, note the secondary role in the profile so downstream skills can adjust when relevant.
