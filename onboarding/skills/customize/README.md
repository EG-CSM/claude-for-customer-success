# onboarding.customize

View and update the onboarding plugin configuration — milestone targets, TtV benchmarks, success criteria format, escalation contacts, graduation criteria, and CS methodology references. Validates configuration for missing fields and placeholder values before running other onboarding skills.

## Use it for

- Display current configuration with section-by-section status (--view, default)
- Update specific settings by section name (--update <section>)
- Restore a section to template defaults (--reset <section>)
- Validate configuration for completeness and consistency (--validate)

## Don't use it for

- Full profile rebuild (use cold-start-interview --redo)

## How to trigger it

Say something like:

- "update onboarding config"
- "change milestone targets"
- "onboarding settings"
- "view onboarding profile"
- "validate onboarding config"

## What you get

- Updated onboarding/CLAUDE.md
- Validation report (--validate)

## Prerequisites

- onboarding CLAUDE.md (must exist)

## Governance

- Only writes to onboarding/CLAUDE.md — no other system writes

## See also

- onboarding.cold-start-interview

---

*Domain: `onboarding` · Skill ID: `onboarding.customize`*
