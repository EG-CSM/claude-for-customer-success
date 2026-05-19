# renewals.risk-assessment

Assesses renewal risk for a single account or a portfolio batch. Scores across five signal domains, assigns a risk tier (Critical/High/Medium/Low), and triggers mandatory escalation protocols for Critical-tier accounts. Health scores are inputs, not verdicts. Auto-escalate triggers are non-negotiable.

## Use it for

- Pre-renewal risk tier assignment for a single account
- Multi-account triage for pipeline review prep
- Quick 3-domain risk check for time-sensitive situations

## Don't use it for

- Post-churn retrospective (use renewals.churn-rca)
- Expansion opportunity identification (use expansion-signal)
- Forecast construction (use renewal-forecast)

## How to trigger it

Say something like:

- "risk assessment for [account]"
- "how at-risk is [account]"
- "triage my renewal pipeline"
- "risk check before renewal call"
- "--deep"
- "--quick"
- "--triage"

## What you get

- Risk tier assignment (Critical/High/Medium/Low) with evidence
- Signal summary by domain (5 domains assessed)
- Escalation notice with owner, channel, and SLA (if Critical)
- Triage table (--triage mode; all accounts with tier and top signal)

## Prerequisites

- Domain CLAUDE.md
- Account name or ID (or list for --triage)
- Usage data, engagement history, support tickets, commercial signals
- CRM data or manual input

## Governance

- Health scores are inputs not verdicts — tier derives from red flag count and auto-escalate triggers
- {'Auto-escalate triggers are non-negotiable': 'non-renewal notice OR ≥2 auto-escalate signals OR exec sponsor departed + competitor confirmed → always Critical'}
- Escalation always names owner, channel, and SLA — no anonymous escalations
- Discount authority check on every save offer scenario
- Account content confidential — no cross-account data sharing
- CRM data older than 7 days triggers freshness warning

## See also

- renewals.churn-rca (post-churn analog)
- renewals.expansion-signal (expansion only after risk resolved)
- renewals.renewal-forecast (tier imported into forecast)
- renewals.negotiation-prep (risk context required)
- renewals.executive-summary (tier imported; not re-derived)
- renewals.cold-start-interview (domain config pre-flight)

---

*Domain: `renewals` · Skill ID: `renewals.risk-assessment`*
