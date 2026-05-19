# onboarding.cold-start-interview

First-time setup for the onboarding company profile. Collects role, onboarding model, segment configuration, TtV targets, milestone definitions, success criteria model, kickoff and handoff format, escalation matrix, integrations, and CS methodology preferences. Writes to onboarding CLAUDE.md so all other onboarding skills have required context. Run once at setup; use customize for updates.

## Use it for

- Full onboarding profile setup (--full)
- Abbreviated 15-minute setup writing minimum required fields (--quick)
- Full profile redo (--redo)
- Integration check only (--check-integrations)
- Company profile section only (--redo-company-profile)
- Specific section update (--section <name>)

## Don't use it for

- CSM-level account data (use csm.cold-start-interview)
- Rev-ops metric configuration (use rev-ops.cold-start-interview)

## How to trigger it

Say something like:

- "set up onboarding"
- "configure onboarding"
- "onboarding profile"
- "onboarding cold start"

## What you get

- onboarding/CLAUDE.md (complete company profile)

## Prerequisites

- None (generates the profile)

## Governance

- Only writes to onboarding/CLAUDE.md — no other system writes

## See also

- onboarding.customize

---

*Domain: `onboarding` · Skill ID: `onboarding.cold-start-interview`*
