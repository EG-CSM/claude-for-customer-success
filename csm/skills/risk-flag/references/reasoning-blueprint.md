---
title: "Risk Flag Reasoning Blueprint"
type: reasoning-blueprint
skill: risk-flag
version: 1.0.0
---

# Risk Flag — Reasoning Blueprint

## Problem Classification Taxonomy

### 1. Sudden Signal Spike
- **Characteristics:** Single high-weight signal appears abruptly (exec sponsor departure, competitor eval surfaces, P1 escalation filed)
- **Primary Risk:** Rapid churn trajectory — the window to intervene is short and narrows daily
- **Expert Focus:** Validate the signal is real (not data lag), identify who internally already knows, determine if the customer has verbalized intent to leave

### 2. Gradual Decay Pattern
- **Characteristics:** Multiple medium-weight signals accumulating over weeks/months (usage drift, missed QBRs, declining NPS, contact frequency drop)
- **Primary Risk:** Silent churn — no single alarm fires, but the aggregate trend is unmistakable to a trained eye
- **Expert Focus:** Find the inflection point — when did engagement start declining? What changed in the customer's organization or priorities at that time?

### 3. Renewal-Proximity Risk
- **Characteristics:** Renewal within 90 days AND any risk signal present — the time constraint compresses every decision
- **Primary Risk:** Insufficient runway for recovery; leadership needs to be in the loop now, not after the CSM has "tried a few things"
- **Expert Focus:** Is there still a path to renewal, or is this now a save/negotiate scenario? What concessions (if any) are on the table?

### 4. Stakeholder Disruption
- **Characteristics:** Champion departure, sponsor reorg, buyer persona change, or political shift inside the customer org
- **Primary Risk:** Loss of internal advocacy — the product may still deliver value, but nobody inside the customer is positioned to defend the renewal
- **Expert Focus:** Map the new power structure fast. Who inherits the relationship? Is there a detractor now in a decision-making seat?

### 5. Escalation-in-Progress
- **Characteristics:** Customer has already escalated (support ticket, executive complaint, legal mention) — the CSM is responding, not initiating
- **Primary Risk:** Reactive posture limits options; the customer's narrative is already set and may have reached their leadership before yours
- **Expert Focus:** What has the customer already communicated internally? Match your escalation speed to theirs — never be a step behind

## Domain Heuristics

### H1: The 72-Hour Rule
When a high-weight signal fires, the first 72 hours determine whether the account enters recovery or free-fall. Delay past 72h and the customer interprets silence as indifference.

### H2: Signal Clustering Trumps Severity
Two medium signals in the same 30-day window are more dangerous than one high signal in isolation. Clustering indicates systemic disengagement, not an isolated incident.

### H3: Sponsor Silence Is a Signal
If the executive sponsor has not responded to outreach in 2+ attempts over 30 days, treat as a high-weight signal regardless of what the health score says. Health scores lag relationship decay.

### H4: Usage Drop Context Matters
A 20% usage drop in a product with seasonal patterns is noise. The same drop during the customer's peak season is a five-alarm fire. Always normalize against the customer's own usage baseline and business cycle.

### H5: Escalation Routing Must Be Concrete
"Escalate to leadership" is not a routing. A valid routing names the person, the channel, and the SLA. If the configured matrix doesn't cover this scenario, flag the gap — don't improvise a route.

### H6: The Memo Is Not the Intervention
A risk flag memo is a communication artifact, not an action plan. If the CSM reads the memo and doesn't know exactly what to do Monday morning, the intervention plan failed.

### H7: Separate the Audience
The CSM brief and the escalation memo serve different readers with different needs. Never leak health model internals into the escalation memo. Leadership needs the what and the ask, not the scoring methodology.

## Common Failure Modes

### Sudden Signal Spike
1. **False alarm escalation** — Signal is real but caused by a known, benign event (e.g., planned migration caused usage drop). Fix: Cross-reference with CSM notes and recent call transcripts before classifying severity.
2. **Under-scoping the blast radius** — Treating a sponsor departure as a single signal when it actually invalidates the success plan, QBR commitments, and expansion pipeline. Fix: Trace downstream dependencies of the signal before writing the intervention plan.

### Gradual Decay Pattern
1. **Boiling frog memo** — Documenting each signal accurately but failing to convey urgency because no single signal is dramatic. Fix: Lead with the aggregate trend line and time-to-renewal, not the individual signals.
2. **Root cause speculation without evidence** — Inventing a narrative to explain the decay when the real answer is "we don't know yet." Fix: State the hypothesis clearly, name what evidence would confirm or refute it, and make discovery the first action item.

### Renewal-Proximity Risk
1. **Recovery plan with no runway** — Recommending a 90-day intervention when renewal is in 45 days. Fix: Time-box every action against the renewal date. If the plan doesn't fit the window, escalate immediately.
2. **Optimism bias in severity** — Classifying as High when the signal pattern clearly maps to Critical, because the CSM "has a good relationship." Fix: Apply the configured severity matrix mechanically first, then note mitigating factors separately.

### Stakeholder Disruption
1. **Mapping the old org** — Building the memo around the departed sponsor's context instead of the new decision-maker's priorities. Fix: Flag that stakeholder intelligence is stale and make re-mapping the first intervention action.
2. **Assuming continuity** — Treating the new contact as a continuation of the old relationship. Fix: Treat every stakeholder change as a soft reset — re-validate value prop fit with the new audience.

### Escalation-in-Progress
1. **Duplicating the customer's escalation** — Writing a memo that restates what the customer already told your leadership, adding no new information. Fix: The memo must add the CSM's root cause hypothesis, the intervention plan, and the specific ask of leadership — things the customer's complaint doesn't contain.
2. **Tone mismatch** — Using cautious, hedged language in a memo about an account that has already filed a formal complaint. Fix: Match the urgency of your language to the customer's demonstrated urgency.

## Expert Judgment Patterns

### Scope Decisions
- If the account has both risk and expansion signals, exclude expansion from the risk memo entirely — mixing contexts dilutes urgency
- If the CSM provides narrative context but no structured data, build the memo from narrative and flag every signal as "CSM-reported, not independently verified"
- If multiple escalation matrix rows match, show all but name the primary route based on the highest-severity matching condition

### Sequencing Decisions
- Always validate signal evidence before classifying severity — never classify first and justify later
- Root cause hypothesis comes after signal inventory, not before — the hypothesis must be grounded in the signals documented
- Intervention plan is last because it depends on severity classification and escalation routing

### Depth Decisions
- Brief mode: Full signal breakdown, internal health context, detailed intervention plan — this is the CSM's working document
- Escalation memo mode: Stripped to essentials — account facts, signals, root cause, ask. No health model internals, no scoring methodology
- If severity is Critical, both modes should be produced even if only one was requested — flag this as a recommendation

### Stakeholder Decisions
- The CSM brief stays internal. If anyone beyond the CS team will see it, flag for confidentiality review
- The escalation memo assumes the reader has zero account context — every relevant fact must be stated, not referenced
- If the configured escalation contact is no longer in role, flag the gap rather than routing to a guess

### Confidence Decisions
- Signals from live integrations: state as confirmed with timestamp
- Signals from CSM narrative: state as reported, recommend verification
- Signals inferred from absence of data (e.g., "no QBR in 90 days"): state as inferred from data gap, note that the absence could reflect a data sync issue rather than a real miss
