---
title: Escalation Memo Reasoning Blueprint
type: reasoning-blueprint
skill: escalation-memo
version: 1.0.0
---

# Escalation Memo — Reasoning Blueprint

## Problem Classification Taxonomy

### Type A: Technical Escalation (P1/P2)
**Characteristics**: Unresolved support ticket at P1/P2 severity, SLA breach or approaching breach, product bug with measurable customer impact, engineering involvement required.
**Primary Risk**: SLA clock is already running — delay compounds both the customer impact and the internal accountability gap. Missed SLA windows turn technical issues into relationship issues.
**Expert Focus**: Validate SLA status against the configured matrix first. Confirm whether the customer has been told a timeline — broken commitments escalate faster than broken products.

### Type B: Customer Complaint
**Characteristics**: Formal expression of dissatisfaction — NPS detractor follow-up unresolved, written complaint, executive-level frustration, or public-facing concern (review, social). Emotion is high; facts may be incomplete.
**Primary Risk**: Complaint language gets mirrored into internal communications without separating customer perception from verified facts. The memo becomes an amplifier rather than a diagnostic tool.
**Expert Focus**: Separate what the customer said (quote it) from what the data shows. Name the gap. Complaints without root cause investigation get resolved symptomatically and recur.

### Type C: Executive Escalation
**Characteristics**: A named executive at the customer has requested senior involvement — VP or C-level. Triggered by relationship posture, not necessarily health score. May overlap with churn risk but is fundamentally a power-dynamics event.
**Primary Risk**: Under-routing. If the configured matrix says VP CS and you route to a Support Manager, the executive perceives the escalation as ignored. Over-routing wastes leadership bandwidth on issues that don't warrant it.
**Expert Focus**: Match the seniority of the response to the seniority of the request. Confirm ARR threshold — high-ARR executive escalations have different routing and SLA in most matrices.

### Type D: Internal Process Failure
**Characteristics**: The customer was harmed by an internal miss — dropped handoff, broken commitment, SLA breach caused by internal team rather than product. The customer may or may not know the root cause is internal.
**Primary Risk**: Deflection. Internal failures get framed as "miscommunication" in customer-facing language when the honest framing is "we missed it." Deflection erodes trust faster than the original failure.
**Expert Focus**: Name the internal failure clearly in the internal brief. The customer draft should acknowledge the miss without exposing internal blame chains. Lessons-learned must name the process gap, not the person.

## Domain Heuristics

### H1: SLA Clock Awareness
If the SLA clock is already running, the memo is urgent — not important, urgent. Check SLA status before composing the narrative. A beautifully written memo delivered after the SLA window closes is a failure document.

### H2: The Commitment Audit
Before writing recommended actions, audit what has already been promised to the customer. Broken commitments in the escalation brief destroy credibility. Search call recordings, ticket notes, and CSM context for any "we will" or "by [date]" language.

### H3: Repeat Escalation Detection
If CRM shows a prior escalation of the same type for this account, the memo must flag the pattern explicitly. A second technical escalation is not a new issue — it is evidence that the first resolution was incomplete. Systemic, not episodic.

### H4: ARR Threshold Gate
Check ARR against the configured escalation threshold before routing. Above-threshold accounts automatically include VP CS / CRO in communications. Missing this step means leadership learns about a high-value escalation after the customer has already lost patience.

### H5: Customer Language Firewall
Internal language (health scores, escalation IDs, ARR, routing names, revenue-at-risk) never appears in customer-facing drafts. Review the customer acknowledgment draft as if the customer's CEO will read it — because they might forward it.

### H6: Specificity Over Empathy
"I understand your frustration" is filler. "I know that [specific impact] is affecting [specific business outcome]" is acknowledgment. Every customer-facing sentence must reference the specific issue, not generic empathy templates.

### H7: Close-Out Requires Root Cause
Never close an escalation without a root cause hypothesis, even if preliminary. "We resolved it" without "here's why it happened" guarantees recurrence. The lessons-learned section is not optional — it is the highest-value part of the close-out.

## Common Failure Modes

### Type A (Technical) Failures
- **Stale SLA data**: Memo cites an SLA window that has already passed without flagging the breach. **Fix**: Pull SLA status live from support platform; if unavailable, flag "SLA status unverified — confirm before routing."
- **Missing engineering context**: Escalation brief lacks what engineering has already tried. **Fix**: Include "attempted resolutions" in the issue narrative — the escalation owner should not re-request diagnostics already performed.
- **Vague ETA in customer draft**: "We're working on it" instead of a specific next-update time. **Fix**: If no ETA is available, commit to a status update time, not a resolution time: "I'll update you by [specific date/time]."

### Type B (Complaint) Failures
- **Emotional mirroring**: Internal brief adopts the customer's emotional framing instead of separating perception from facts. **Fix**: Quote the customer's words, then state the verified facts separately. Let the escalation owner assess the gap.
- **Missing triggering event**: Complaint memos that describe ongoing dissatisfaction without naming the specific event that triggered formal escalation. **Fix**: Always answer "what happened on [date] that made this a formal escalation?"

### Type C (Executive) Failures
- **Under-routing**: Executive requests VP involvement; memo routes to a manager. **Fix**: Match response seniority to request seniority. When in doubt, route up — leadership can delegate down, but a manager cannot escalate themselves.
- **Missing relationship context**: Brief lacks information about the executive's history, influence, and what they specifically asked for. **Fix**: Include "what the executive said they need" as a direct quote or close paraphrase.

### Type D (Internal) Failures
- **Blame deflection in customer draft**: Customer communication uses passive voice to hide internal accountability ("there was a miscommunication" vs. "we missed the handoff"). **Fix**: Use active voice acknowledging the miss without naming internal individuals.
- **No process fix in lessons-learned**: Close-out names what happened but not what changes prevent recurrence. **Fix**: Every lessons-learned entry must include a specific process or communication change, not just a description of the failure.

## Expert Judgment Patterns

### Scope Decisions
- **Single-type vs. compound**: If an escalation spans two types (e.g., technical failure that triggered an executive complaint), open it under the type that determines routing, and note the secondary type. Do not open two parallel escalations for the same event.
- **Escalation vs. risk flag**: If the issue is a pattern of concern without a specific triggering event, it is a risk flag, not an escalation. Redirect to `/csm:risk-flag`.

### Sequencing Decisions
- **SLA-first**: Always check SLA status before narrative composition. The SLA clock determines urgency, which determines how much detail the first communication needs vs. how much can follow in an update.
- **Routing before drafting**: Confirm the escalation owner from the matrix before writing recommended actions. Actions written for the wrong audience waste the CSM's editing time.

### Depth Decisions
- **Open memos need full context**: The escalation owner is seeing this account for the first time in this context. Include relationship history, prior escalations, and renewal timeline.
- **Update memos need delta only**: Do not re-state the full context. State what changed, what was done, and what is next.
- **Close memos need root cause depth**: The resolution summary can be brief; the lessons-learned section should be substantive.

### Stakeholder Decisions
- **Internal vs. customer draft tone**: Internal brief is diagnostic and complete. Customer draft is empathetic, specific, and commitment-oriented. Never merge the two audiences.
- **Leadership inclusion**: ARR above threshold or repeat escalation pattern = automatic leadership inclusion. Do not wait for the CSM to request it.

### Confidence Decisions
- **Data-backed vs. CSM-reported**: When data sources conflict with CSM-provided context, present both and flag the discrepancy. Do not silently prefer one over the other.
- **Preliminary root cause**: Label root cause as "preliminary" or "confirmed" based on whether engineering or process review has validated it. Never present a hypothesis as confirmed.
