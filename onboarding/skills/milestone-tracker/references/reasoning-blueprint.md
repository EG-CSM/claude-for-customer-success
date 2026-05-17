---
title: "Reasoning Blueprint: Milestone Tracking"
type: reasoning-blueprint
skill: milestone-tracker
version: 1.0.0
---

# Reasoning Blueprint: Milestone Tracking

Load this blueprint when Tier 3 reasoning is activated for onboarding milestone
tracking. It provides the domain-specific taxonomy, heuristics, and expert judgment
patterns that shape expert-level milestone health assessment and portfolio risk triage.

---

## Problem Classification Taxonomy

### Type A: Single-Account Status Check
**Characteristics**: One named account, CSM wants current milestone state before a touchpoint or internal review.
**Primary Risk**: Presenting stale PM data as current — CSM acts on outdated milestone completion status.
**Expert Focus**: Delta since last check matters more than absolute state. Surface what changed, not just what is.

### Type B: Portfolio Health Scan
**Characteristics**: Cross-account view of milestone progress for book-of-business management or 1:1 prep.
**Primary Risk**: Treating all accounts as comparable when segment, model, and duration targets differ.
**Expert Focus**: Normalize by segment target before RAG-coding — a Day-20 M2 delay in enterprise is different from SMB.

### Type C: At-Risk Triage
**Characteristics**: CSM needs to identify which accounts require intervention now — overdue or signal-triggered.
**Primary Risk**: Sorting by days-overdue alone and missing accounts with behavioral at-risk signals that haven't yet breached date thresholds.
**Expert Focus**: Behavioral signals (no login, missing attendees, credentials not received) outweigh calendar math for early intervention.

### Type D: Escalation-Ready Brief
**Characteristics**: A specific account has breached escalation thresholds — output feeds an escalation workflow or leadership review.
**Primary Risk**: Presenting the overdue flag without root-cause context, making the escalation look like a status update instead of an action request.
**Expert Focus**: Pair the flag with owner, recommended action from escalation matrix, and any mitigating context (agreed deferral, dependency block).

---

## Domain Heuristics

1. **The Signal-Over-Calendar Rule**: A milestone with 15 days remaining but a confirmed at-risk signal is more urgent than one 2 days overdue with no signal. Behavioral evidence beats date math.

2. **The Contract-Start Anchor Rule**: Every date calculation flows from contract start date. If that date is missing or estimated, every downstream milestone target is unverified — flag immediately, never silently default.

3. **The Segment Normalization Rule**: Compare milestone pace to segment-specific duration targets, not absolute day counts. Enterprise M3 at Day 30 is on track; SMB M3 at Day 30 may be overdue.

4. **The PM-Trumps-Manual Rule**: When PM connector data conflicts with CSM-reported status, surface the discrepancy rather than choosing one. The conflict itself is a signal worth investigating.

5. **The Overdue-Is-Not-Failed Rule**: An overdue milestone may be legitimately deferred. Before escalating, check for agreed scope changes, customer-requested delays, or technical dependencies. Overdue is a flag, not a verdict.

6. **The Portfolio-Is-Not-Deep-Dive Rule**: Portfolio mode surfaces which accounts need attention. It does not replace per-account investigation. Never escalate from portfolio view alone — run status mode first.

7. **The Escalation-Matrix-Not-Gut Rule**: Escalation routing comes from the configured matrix with named owner, channel, and SLA. Generic "escalate to manager" is never acceptable.

---

## Common Failure Modes by Request Type

### Single-Account Status Failures
- **Stale data presented as current**: PM connector data is days old but displayed without timestamp.
  -> Fix: Always include data-as-of timestamp; flag if PM data >24h old.
- **Missing contract start date silently defaulted**: Date calculations proceed with an estimated start date.
  -> Fix: Hard-stop on missing contract start — request from CSM or CRM before calculating.

### Portfolio Health Failures
- **Cross-segment comparison without normalization**: SMB and enterprise accounts RAG-coded on same absolute day thresholds.
  -> Fix: Apply segment-specific duration targets from config before assigning status.
- **Confidentiality leak in portfolio output**: ARR or internal health details included in output shared beyond CSM.
  -> Fix: Portfolio output is internal-only by default; apply confidentiality check before any distribution.

### At-Risk Triage Failures
- **Calendar-only triage**: Accounts sorted by days-overdue, missing accounts with behavioral signals and days remaining.
  -> Fix: Score by signal severity first, then by date proximity. Behavioral signals rank above calendar math.
- **Recommended actions are generic**: "Follow up with the customer" instead of specific escalation steps.
  -> Fix: Pull recommended action from escalation matrix keyed to days-overdue bracket and milestone type.

### Escalation Brief Failures
- **Flag without context**: Escalation shows "M2 overdue by 5 days" without root cause or mitigating factors.
  -> Fix: Include known blockers, agreed deferrals, and owner assignment alongside the flag.

---

## Expert Judgment Patterns

### Severity Prioritization Decisions
- Behavioral at-risk signals with days remaining > 0 rank above calendar-only overdue with no signal — the former is deteriorating, the latter may be administrative.
- Multiple milestones overdue on one account outranks single-milestone overdue across multiple accounts — concentration of risk matters.

### Data Confidence Decisions
- PM connector data is authoritative over manual input; surface conflicts, don't resolve them silently.
- When contract start date comes from CRM vs. CSM memory, prefer CRM — but flag if CRM field was last updated >30 days ago.
- If no PM connector and no CRM, all milestone dates are [unverified] — state this once at the top, not per row.

### Scope Decisions
- Portfolio mode with >15 accounts: show summary counts and flag only at-risk/overdue accounts individually — don't enumerate all on-track accounts.
- Escalation brief for leadership: strip internal-only TtV projections unless the audience is the CS ops team.

---

*Reasoning Blueprint: Milestone Tracking v1.0*
*For use with milestone-tracker when Tier 3 reasoning is activated*
