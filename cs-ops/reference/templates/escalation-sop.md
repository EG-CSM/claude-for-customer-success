# CS Escalation Standard Operating Procedure

**CS Escalation Standard Operating Procedure**
*[Version] · [Date] · INTERNAL — CS and CS-Ops use*
*Applies to: customer escalations · product escalations · executive escalations*

---

## Purpose and scope

This SOP governs how escalations are opened, triaged, owned, communicated, and resolved
across the CS team. It applies to all accounts regardless of segment. An escalation is
any situation where standard CS engagement cannot resolve the customer issue within the
normal cadence — requiring cross-functional ownership, executive involvement, or
expedited response.

**This SOP does not apply to:** routine support tickets handled by the support team
without CSM involvement; internal process issues without customer impact.

---

## Escalation severity tiers

| Severity | Label | Response SLA | Examples |
|---------|-------|-------------|---------|
| S1 | Critical | <2 hours | Production outage with business impact; customer threatening immediate churn; executive-level demand for resolution |
| S2 | High | <24 hours | Significant product failure without workaround; renewal at risk due to unresolved issue; VP-level customer concern |
| S3 | Standard | <48 hours | Feature gap blocking workflow; persistent support ticket unresolved past SLA; health score drop to Red without active CTA |

**Severity is set by the CS Lead at triage.** The opening CSM proposes a severity;
the CS Lead confirms or adjusts. For S1 escalations, CS Lead can escalate to VP CS.

---

## Escalation workflow

### Step 1 — Trigger

A CSM opens an escalation when:
- A customer issue cannot be resolved within the standard engagement model
- A customer communicates dissatisfaction at a severity level above routine feedback
- A product or service failure is creating measurable business impact for the customer
- A renewal is at risk due to an unresolved issue

**Open the escalation immediately — do not wait for resolution attempts to exhaust.**

### Step 2 — Triage

Within the severity SLA:

| Action | Owner |
|--------|-------|
| Review escalation details submitted by CSM | CS Lead |
| Confirm or adjust severity tier | CS Lead |
| Assign escalation owner | CS Lead |
| Notify cross-functional stakeholders (Support, Engineering, Product) as appropriate | CS Lead / Escalation Owner |

### Step 3 — Owner assignment

| Severity | Escalation owner | Backup |
|---------|-----------------|--------|
| S1 | CS Lead | VP CS |
| S2 | CSM + CS Lead co-own | CS Lead escalates to VP CS if unresolved >12 hours |
| S3 | CSM | CS Lead reviews at 48 hours if unresolved |

### Step 4 — Customer communication

| Severity | First response | Cadence | From |
|---------|---------------|---------|------|
| S1 | <2 hours | Every 2 hours until resolved | CS Lead (or VP CS) |
| S2 | <4 hours | Daily update until resolved | CSM + CS Lead |
| S3 | <24 hours | Every 2 business days | CSM |

**S1 customer communication must acknowledge the issue and state the next update time.**
Do not communicate resolution timelines unless Engineering has confirmed the estimate.

### Step 5 — Resolution

Resolution is confirmed when:
- The root cause has been identified and addressed (or a workaround is in place)
- The customer has acknowledged the resolution
- Any product or service fix is validated in the customer's environment

### Step 6 — Post-escalation follow-up

Within 5 business days of resolution:
- CSM conducts a follow-up call or sends a written summary to the customer
- CS Lead reviews whether the escalation reveals a product gap, process gap, or
  isolated incident
- Escalation log entry marked resolved with root cause and resolution summary
- If escalation reveals systemic issue: CS Ops opens a process improvement record

---

## Escalation log entry format

Open one entry per escalation. Archive in escalation log.

| Field | Value |
|-------|-------|
| Escalation ID | [ESC-YYYY-NNN] |
| Account | [Account name] |
| ARR | $[amount] |
| Severity | [S1 / S2 / S3] |
| Opened by | [CSM name] |
| Opened date | [Date] |
| Escalation owner | [Name] |
| Status | [Open / In progress / Resolved] |
| Root cause | [Summary — complete at resolution] |
| Resolution summary | [What resolved it — complete at close] |
| Resolved date | [Date] |
| Follow-up completed | [Yes / No / Date scheduled] |

**Issue description:**
[What is happening, what the customer communicated, what has been tried]

**Customer impact:**
[Business impact on the customer — not just the technical issue]

**Internal stakeholders notified:**
[Names and roles]
