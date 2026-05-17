---
title: "Reasoning Blueprint: Stakeholder Map"
type: reasoning-blueprint
skill: stakeholder-map
version: 1.0.0
---

# Reasoning Blueprint: Stakeholder Map

## Problem Classification Taxonomy

### Type A: Coverage Assessment
**Characteristics**: CSM needs a baseline view of who is known, who is missing, and whether role coverage meets the CS motion's requirements.
**Primary Risk**: Incomplete data presented as complete — CSM trusts the map and stops prospecting for contacts.
**Expert Focus**: Verify source freshness; flag roles required by the CS motion that have zero contacts before presenting the map.

### Type B: Engagement Gap Detection
**Characteristics**: Contacts are known but engagement has gone cold or uneven. Request centers on who has dropped off and what that signals.
**Primary Risk**: Conflating silence with disengagement — a contact on parental leave looks identical to a disengaging detractor in CRM data alone.
**Expert Focus**: Cross-reference multiple signals (call attendance, email replies, champion commentary) before labeling a gap as risk.

### Type C: Sponsor Risk Evaluation
**Characteristics**: Executive sponsor stability is the concern — departure signals, tenure, succession gaps, or upcoming renewal with an unengaged sponsor.
**Primary Risk**: Over-relying on LinkedIn signals or single data points to predict sponsor departure.
**Expert Focus**: Triangulate tenure, QBR attendance, champion sentiment, and org-change signals before assigning a risk level.

### Type D: Influence Mapping
**Characteristics**: CSM needs to understand decision dynamics — who blocks, who accelerates, who the real decision-maker is versus the named contact.
**Primary Risk**: Inferring influence from org-chart proximity instead of observed behavior.
**Expert Focus**: Ground every influence claim in direct evidence (call participation, stated authority, observed escalation patterns).

### Type E: Pre-Event Preparation
**Characteristics**: Stakeholder map is being built or refreshed in preparation for a QBR, renewal, or executive meeting.
**Primary Risk**: Stale data presented as current — map was last updated 90 days ago and assumptions have drifted.
**Expert Focus**: Confirm data recency for every contact; flag any contact not verified within the event preparation window.

---

## Domain Heuristics

1. **Single-Thread Alarm**: If only one contact has "Active" engagement health across all roles, the account is single-threaded regardless of how many contacts exist. Flag immediately.

2. **Champion-Sponsor Disconnect**: When the champion reports the sponsor is "fine" but the sponsor hasn't attended a QBR in two cycles, trust the behavioral data over the champion's reassurance.

3. **Title ≠ Role**: A VP of Operations titled "Executive Sponsor" in CRM may have no budget authority. Verify role through observed behavior (signs contracts, attends exec reviews), not CRM fields.

4. **Dormancy Asymmetry**: Apply different dormancy thresholds for executive vs. operational contacts. Executives who engage quarterly are healthy; operational contacts who go 30 days silent in a high-touch motion are declining.

5. **New Stakeholder Window**: A new executive joining the account has a 30-60 day window where they are forming vendor opinions. Missing this window means inheriting whatever internal narrative exists about your product.

6. **Detractor Evidence Standard**: Never label a contact as a detractor based on silence, tone, or title. Require direct evidence: stated opposition, negative survey response, or documented objection.

7. **Departure Signal Triangulation**: No single signal (LinkedIn update, champion mention, missed meeting) confirms sponsor departure. Require 2+ independent signals before escalating.

---

## Common Failure Modes

### Type A (Coverage Assessment)
- **Presenting CRM contacts as stakeholder coverage** — CRM lists everyone who was ever added; many are inactive, departed, or irrelevant. Fix: Filter by last-activity date and verify current role before including.
- **Missing the "unknown unknowns"** — Listing known contacts without flagging roles that should exist but have no contact. Fix: Compare against the CS motion's minimum role coverage template.

### Type B (Engagement Gap Detection)
- **Treating all silence equally** — A 45-day gap for a champion is critical; for a quarterly executive touchpoint it is normal. Fix: Apply role-specific dormancy thresholds from the configured CS motion.
- **Flagging gaps without context** — Reporting "no contact in 60 days" without checking for known reasons (leave, holiday, fiscal year-end). Fix: Cross-reference with champion or known calendar events before labeling as risk.

### Type C (Sponsor Risk Evaluation)
- **Single-signal escalation** — Escalating sponsor risk based on one LinkedIn update or one missed QBR. Fix: Require triangulation (2+ independent signals) before assigning High risk.
- **Ignoring succession** — Flagging sponsor risk without assessing whether a successor exists. Fix: Always include succession path status in sponsor risk output.

### Type D (Influence Mapping)
- **Org-chart inference** — Drawing influence lines from reporting structure instead of observed behavior. Fix: Ground every influence claim in direct evidence with a cited source (call, email, stated authority).
- **Static influence assumptions** — Treating influence dynamics as fixed when they shift with org changes, budget cycles, and project phases. Fix: Date-stamp influence assessments and flag any older than 90 days.

---

## Expert Judgment Patterns

### Data Quality Decisions
- When CRM data conflicts with call-recording data, trust call-recording for attendance and recency; trust CRM for titles and roles only if recently verified.
- When a contact appears in CRM but has never been on a call or email thread, classify as "Unverified" rather than including at face value.

### Risk Calibration Decisions
- Sponsor risk is "High" only when: 2+ departure/disengagement signals AND no identified successor AND renewal is within 6 months.
- A "Medium" risk sponsor with an identified, engaged successor is operationally lower risk than a "Low" risk sponsor with zero succession path.

### Scope Decisions
- For accounts with 20+ contacts in CRM, focus the map on the top 8-10 by influence and recency rather than producing an exhaustive list that buries signal in noise.
- For tech-touch accounts, a single-contact map is acceptable — flag it as single-threaded but do not treat it as a gap requiring the same coverage as high-touch.

### Communication Decisions
- Stakeholder maps with "High" sponsor risk should include a recommended escalation action, not just a risk label — the CSM needs a next step, not a dashboard indicator.
- When influence dynamics are genuinely unknown, say "influence dynamics not yet mapped" rather than inferring from titles. An honest gap is more useful than a confident guess.

---

*Reasoning Blueprint: Stakeholder Map v1.0*
*Domain: Customer Success Management*
