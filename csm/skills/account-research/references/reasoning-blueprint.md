---
title: "Reasoning Blueprint: Account Research"
type: reasoning-blueprint
skill: account-research
version: 1.0.0
---

# Reasoning Blueprint: Account Research

Load this blueprint when Tier 3 reasoning is activated for account research work.

## Problem Classification Taxonomy

### Type 1: Pre-Call Snap Brief
- **Characteristics**: Time-pressured, single account, call happening within hours. Needs actionable context fast — not exhaustive history.
- **Primary Risk**: Surfacing stale data without a staleness flag, leading the CSM to reference outdated health or stakeholder info on the call.
- **Expert Focus**: Checks the delta since last contact — what changed since the CSM last spoke to this account? A competent practitioner summarizes the current state; an expert highlights what shifted.

### Type 2: QBR / Executive Meeting Prep
- **Characteristics**: Higher-stakes audience (VP+, economic buyer). Needs polished structure, validated health components, and renewal/expansion context. Longer lead time than a snap brief.
- **Primary Risk**: Health score presented without component decomposition — executive asks "why yellow?" and the CSM has no specifics. Or expansion signals leaked into customer-facing prep.
- **Expert Focus**: Validates that every health component traces to an observable signal, not a composite score alone. Checks whether the stakeholder map includes the actual meeting attendees and flags any unknown or unengaged attendees.

### Type 3: Risk / Escalation Account Review
- **Characteristics**: Account is Red or trending Yellow-to-Red. The brief feeds an escalation workflow or risk memo. Audience is often the CSM's manager or a cross-functional escalation team.
- **Primary Risk**: Treating the health score as a churn verdict instead of decomposing the signals. Or missing the escalation routing — who specifically owns this escalation, per the configured matrix?
- **Expert Focus**: Separates lagging indicators (health score, NPS) from leading indicators (usage trend direction, stakeholder disengagement, support ticket acceleration). Checks whether the escalation path is populated and routable, not generic.

### Type 4: Portfolio Scan / Multi-Account Triage
- **Characteristics**: CSM reviewing multiple accounts before a pipeline review or 1:1. Needs consistent structure across accounts for comparison. Confidentiality risk is higher — portfolio-level financial data in one output.
- **Primary Risk**: Confidentiality failure — ARR, contract terms, and internal health scores for multiple accounts in a single document that could be inadvertently shared. Also: inconsistent data freshness across accounts without per-account staleness flags.
- **Expert Focus**: Applies G5 (confidentiality check) proactively. Ensures each account's data timestamp is independent — one account's CRM data may be 2 days old while another's is 14 days stale.

### Type 5: Stakeholder-Focused Research
- **Characteristics**: The `--stakeholders` flag is active or the request centers on "who matters at this account." Needs contact-level detail, engagement recency, influence mapping, and gap identification.
- **Primary Risk**: Listing contacts without engagement recency or role classification. A name/title list is not a stakeholder map — the value is in identifying gaps (no exec sponsor contact in 60+ days, champion left the company, new decision-maker not yet engaged).
- **Expert Focus**: Cross-references CRM contacts against call recording attendees to find shadow stakeholders (people showing up on calls but not in CRM) and ghost stakeholders (people in CRM who never appear on calls).

## Domain Heuristics

**The Recency-Over-Completeness Rule**: In a pre-call brief, the last 30 days of activity matter more than the full account history. Prioritize recent signals; archive older context. Threshold: if the brief exceeds one page, cut older items first.

**The Delta Rule**: The most valuable insight in an account brief is not the current state — it is what changed since the CSM last engaged. Always surface the delta explicitly: "Usage down 18% since your last call on [date]."

**The Composite Score Decomposition Rule**: Never present a health score without its component signals. A "Yellow" score means nothing actionable; "Yellow because usage dropped 18% and exec sponsor hasn't responded in 45 days" is actionable. Trigger: any time a health color or score appears in output.

**The Staleness Gradient Rule**: Not all stale data is equally dangerous. CRM firmographic data (industry, segment) tolerates weeks of staleness. Usage data older than 3 days may misrepresent the current state. Stakeholder data older than 7 days may miss departures. Apply staleness flags proportional to data volatility.

**The Escalation Specificity Rule**: "Escalate to your manager" is not an escalation path. Every escalation recommendation must name the role, the person (if configured), the channel, and the SLA from the configured matrix. If the matrix is not configured, flag the gap — do not improvise a path.

**The Expansion Signal Quarantine Rule**: Expansion signals are internal-only and tagged as early/unqualified until the AE/AM has evaluated them. Never surface expansion signals in any output that could reach the customer. Trigger: any time `--deep` mode is active or expansion context appears.

**The Audience-Aware Framing Rule**: The same account data requires different framing for different audiences. A brief for the CSM's own prep includes internal health scores and ARR; a brief that might reach the customer must strip these. Always confirm the destination before generating. Trigger: any request that mentions "share with customer" or "send to."

## Common Failure Modes by Request Type

### Pre-Call Snap Brief
- **Stale data presented as current**: CRM last synced 10 days ago but the brief shows data without a timestamp. Fix: enforce per-source timestamps in every brief; flag any source >3 days old for usage data, >7 days for CRM.
- **Missing delta context**: Brief shows current state but not what changed since the last touchpoint. Fix: always pull last contact date and compare current signals against that baseline.
- **Wrong mode selection**: CSM asks for quick prep but gets a deep-mode output that takes 5 minutes to read before a call starting in 10. Fix: default to `--brief` unless explicitly requested otherwise; confirm mode if the request is ambiguous.

### QBR / Executive Meeting Prep
- **Health score without decomposition**: Output says "Yellow" without explaining which components are driving it. Fix: always show component-level signals with configured thresholds.
- **Stakeholder map missing meeting attendees**: Brief lists CRM contacts but doesn't cross-reference against the actual meeting invite or recent call attendees. Fix: when call recording data is available, cross-reference attendees.
- **Expansion signals in customer-facing prep**: Deep mode expansion signals leak into a QBR deck draft. Fix: apply G2 quarantine — expansion signals never appear in customer-facing output.

### Risk / Escalation Account Review
- **Health score treated as churn prediction**: "This account will churn" instead of "these signals indicate elevated risk." Fix: enforce G1 — health scores are heuristics, not verdicts.
- **Generic escalation path**: "Escalate immediately" without naming who, how, or what SLA. Fix: enforce G4 — route through configured matrix or flag the gap.
- **Lagging-only analysis**: Brief reports NPS dropped and health is Red but doesn't surface leading indicators (usage trend direction, engagement velocity). Fix: always separate leading from lagging indicators in risk context.

### Portfolio Scan / Multi-Account
- **Confidentiality breach risk**: Multiple accounts' ARR, contract terms, and health scores in a single document. Fix: enforce G5 — flag confidentiality risk; recommend per-account briefs for external distribution.
- **Inconsistent staleness across accounts**: One account has fresh data, another's is 2 weeks old, but no per-account timestamps. Fix: per-account data freshness in the reviewer note.

### Stakeholder-Focused Research
- **Contact list without engagement context**: Names and titles without last-contact dates, engagement quality, or role classification. Fix: always include last contact date and flag gaps per CS motion thresholds.
- **Missing shadow stakeholders**: People appearing on recent calls but absent from CRM contacts. Fix: cross-reference call recording attendees against CRM contact list.

## Expert Judgment Patterns

### Scope Decisions
- **Brief vs. Deep**: Default to brief unless the CSM explicitly requests deep or the account is Red/Yellow with renewal <90 days — in that case, recommend deep mode proactively.
- **Single vs. Multi-account**: If the request names 3+ accounts, switch to portfolio scan mode with per-account staleness tracking and a confidentiality warning.
- **Stakeholder inclusion**: Include the stakeholder section in the standard brief only when there is a flaggable gap (exec sponsor >60 days, champion departed). Otherwise, keep it in `--stakeholders` mode to avoid brief bloat.

### Sequencing Decisions
- **Data source priority**: CRM first (identity anchor), then CS Platform (health overlay), then call recording (recency context), then documents (open items). Never skip CRM — it anchors everything else.
- **Gap handling**: When a data source fails or returns nothing, note the gap and proceed — never block the brief on a single source. But adjust confidence downward and flag it in the reviewer note.

### Depth Decisions
- **Health decomposition depth**: Always show components. Show threshold comparison only when the account is Yellow or Red — Green accounts don't need threshold math cluttering the brief.
- **Call history depth**: Last 2 calls for brief mode; last 90 days thematic for deep mode. Never summarize more than 90 days of calls — diminishing returns and token cost.

### Confidence Decisions
- **Single-source health**: If health signals come from only one source (e.g., CS Platform but no call or CRM corroboration), tag as [Moderate | single-source] — not [High Confidence].
- **User-provided context only**: When no integrations are connected and the CSM pastes context, tag the entire brief as [Moderate — user-provided context only; not independently verified].
- **Stale + single-source**: If data is both stale (>7 days) and single-source, downgrade to [Low Confidence] and recommend the CSM verify before acting on the signal.
