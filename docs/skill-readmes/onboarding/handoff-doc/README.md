# onboarding.handoff-doc

Generate the onboarding graduation handoff document — structured transfer of account context from the onboarding CSM to the post-onboarding team. Reads graduation criteria, escalation contacts, and handoff format from the onboarding profile. Pulls account history from CRM and PM connectors if available.

## Use it for

- Full handoff document for graduation (--draft, default)
- Graduation readiness check before generating the document (--readiness)
- Abbreviated handoff brief for verbal or async transfer (--summary)

## Don't use it for

- Notifying the receiving team (no autonomous messaging)
- Modifying CRM records

## How to trigger it

Say something like:

- "handoff"
- "graduation"
- "transfer account"
- "onboarding complete"
- "handoff doc"

## What you get

- Graduation handoff document (--draft)
- Readiness assessment with gap list (--readiness)
- Abbreviated handoff brief (--summary)

## Prerequisites

- onboarding CLAUDE.md (graduation criteria, handoff format, escalation contacts)

## Governance

- No autonomous outreach to receiving team
- Graduation criteria sourced from profile only

## See also

- onboarding.success-criteria
- onboarding.milestone-tracker

---

*Domain: `onboarding` · Skill ID: `onboarding.handoff-doc`*
