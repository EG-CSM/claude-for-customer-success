# onboarding.milestone-tracker

Track milestone progress across one account or the full onboarding portfolio. Reads milestone framework, at-risk signals, and escalation thresholds from the onboarding profile. Pulls current milestone status from PM connector (Asana, Linear, Jira, or Monday) if configured.

## Use it for

- Current-state milestone view for one account (--status, default)
- Milestone health summary across all active onboarding accounts (--portfolio)
- At-risk and overdue milestones with recommended actions (--flag)

## Don't use it for

- Modifying milestones or task assignments in PM connector
- TtV performance analysis (use ttv-analysis)

## How to trigger it

Say something like:

- "milestone status"
- "milestone health"
- "track onboarding"
- "at-risk milestones"
- "overdue milestones"

## What you get

- Milestone health snapshot (--status or --portfolio)
- At-risk account list with recommended actions (--flag)

## Prerequisites

- onboarding CLAUDE.md (milestone framework, at-risk signals, escalation thresholds)

## Governance

- Read-only — no PM connector writes
- At-risk thresholds sourced from profile

## See also

- onboarding.blocker-review
- onboarding.ttv-analysis
- onboarding.onboarding-plan

---

*Domain: `onboarding` · Skill ID: `onboarding.milestone-tracker`*
