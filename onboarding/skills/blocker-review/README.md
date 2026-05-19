# onboarding.blocker-review

Diagnose and resolve onboarding blockers — anything preventing a customer from reaching their next milestone on time. Classifies blockers by type and severity, routes to the correct resolution path per the escalation matrix, and produces an action plan with named owners and deadlines.

## Use it for

- Guided diagnostic for a current blocker (--diagnose, default)
- Formatted escalation brief for a named escalation contact (--escalate)
- Logging a resolved blocker to account history (--log)

## Don't use it for

- Autonomously contacting escalation contacts
- Modifying PM connector tasks directly

## How to trigger it

Say something like:

- "blocker"
- "stuck"
- "milestone delayed"
- "escalate"
- "not progressing"

## What you get

- Blocker diagnostic with classification and severity
- Escalation brief (--escalate)
- Resolved blocker log entry (--log)

## Prerequisites

- onboarding CLAUDE.md (escalation matrix, thresholds, escalation contacts)

## Governance

- Escalation contacts sourced from profile only; no autonomous outreach
- Severity classification uses profile escalation thresholds

## See also

- onboarding.milestone-tracker
- onboarding.handoff-doc

---

*Domain: `onboarding` · Skill ID: `onboarding.blocker-review`*
