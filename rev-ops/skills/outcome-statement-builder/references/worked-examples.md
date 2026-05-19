# Worked Examples
## outcome-statement-builder — Reference File

These two examples trace the full Phase 1 workflow end-to-end for a single product and segment.
They show evaluation diagnosis before transformation, stage classification reasoning, and the
approval gate format. Use them to calibrate what correct skill execution looks like.

**Product:** Meridian Analytics — AI Revenue Intelligence Platform
**Segment:** CRO at mid-market to enterprise B2B SaaS

---

## Example A — OCV-001: Win Rate via Conversation Intelligence

**Demonstrates:** All three evaluation criteria failing on a single input; elevation from Stage 2 to Stage 3; TRIGGER slot distinguishing business context from product activation.

---

### Input

```
Product: Meridian Analytics
Customer Segment: CRO at mid-market B2B SaaS
Capability: "Conversation Intelligence: automatically records, transcribes, and analyzes
customer interactions across all channels. AI detects topics, sentiment, market trends,
and hidden buying signals rather than just keyword tracking."
```

---

### Step 2 — Evaluation

**Capability vs. outcome test: FAIL**
The input describes what Meridian Analytics does — "records, transcribes, analyzes" — not what the CRO achieves. The product is the grammatical subject throughout. A valid outcome statement has the customer role as the subject.

**Measurability test: FAIL**
"Detects buying signals" is a directional signal with no magnitude, metric, or timeframe attached. There is nothing in this input that could be measured before and after implementation to confirm achievement. "Hidden buying signals" is a product marketing phrase, not a change-in-state.

**Usable strength:** The underlying business problem is real and recoverable — reps have inconsistent deal outcomes, and loss reasons come from self-reporting rather than evidence. That problem context is the raw material for the TRIGGER slot.

---

### Step 3 — Transformation

**Madlib slots filled:**

| Slot | Value |
|------|-------|
| TRIGGER | a CRO at a mid-market B2B SaaS company is managing a revenue organization where deal outcomes are inconsistent across reps and loss reasons are based on rep self-reporting rather than evidence |
| ROLE | the CRO |
| CHANGE | reduces revenue lost to undetected deal risk by [TBD% — source required] within [TBD days] of full call capture adoption |
| MECHANISM | identifying which talk tracks, objection responses, and competitive moments correlate with closed-won outcomes across the entire pipeline using Meridian Analytics conversation analysis |
| FUNCTIONAL OUTCOME | identify what actually drives wins and losses at scale — not just the top performers' anecdotes |
| BUSINESS GOAL | win rate as a board-level revenue metric |

**CHANGE slot note:** Magnitude is [TBD]. The direction (reduces revenue lost to undetected deal risk) and metric (revenue lost to undetected deal risk, proxied by win rate delta) are valid. The user must supply the range from customer evidence before this entry is used in a Sales commitment.

**TRIGGER slot note:** "A CRO is managing a revenue organization where..." describes a business context that exists before and without the product. Compare to the failing trigger: "When a customer has activated the Conversation Intelligence feature..." — that describes product activation, not customer situation.

---

### Outcome Statement

> When a CRO at a mid-market B2B SaaS company is managing a revenue organization where deal outcomes are inconsistent across reps and loss reasons are based on rep self-reporting rather than evidence, the CRO reduces revenue lost to undetected deal risk by [TBD% — source required] within [TBD days] of full call capture adoption, enabling the CRO to identify which talk tracks, objection responses, and competitive moments correlate with closed-won outcomes across the entire pipeline — not just the top performers' anecdotes — that advances win rate as a board-level revenue metric.

---

### Step 4 — Stage Classification

**Stage 3 — Desired Outcome.**

The raw capability input was a Stage 2 description (what the product can do: record and analyze calls). The transformation reaches Stage 3 because the CRO's desired outcome is evidence-based visibility into what drives wins and losses at scale — not recorded calls. Win rate improvement is the Stage 4 business goal this desired outcome feeds.

The distinction matters for the renewal conversation: a CS team presenting "you have full call capture and analysis running" is presenting Stage 2 — a feature state. A CS team presenting "your win rate has improved X% and your top-performer talk tracks are now running across all reps" is presenting Stage 3 — a desired outcome achieved. Only Stage 3 and above can anchor a renewal conversation.

---

## Example B — OCV-002: Outbound Pipeline Efficiency

**Demonstrates:** Partial role anchoring failure (correct product area, wrong buyer lens); elevation from rep-level to CRO-level framing; Stage 4 classification when the metric is a CFO/board metric.

---

### Input

```
Product: Meridian Analytics
Customer Segment: CRO at mid-market B2B SaaS
Capability: "AI Sales Engagement & Outreach: AI Composer drafts highly personalized
prospecting emails and follow-ups based on real conversational context. Provides tools
to prioritize and automate account-based outreach."
```

---

### Step 2 — Evaluation

**Capability vs. outcome test: FAIL**
"Drafts emails" and "automates outreach" describe product actions. No customer role achieves anything in this statement.

**Measurability test: FAIL**
"Highly personalized" is a product quality claim. "Prioritize and automate" describes process activity. Neither contains a direction, magnitude, metric, or timeframe.

**Role anchoring test: PARTIAL FAIL**
The input implies sales reps and SDRs as the direct users — correct product area — but the stated segment is the CRO. The CRO does not write prospecting emails. The CRO cares about what AI-assisted outreach produces at the org level: pipeline generation efficiency and coverage ratio. The transformation must elevate the lens from rep activity to CRO accountability.

**Usable strength:** The underlying efficiency problem is recoverable — outbound productivity per rep is inconsistent, and follow-up execution degrades beyond three contacts. That's the CRO's constraint, not the rep's task.

---

### Step 3 — Transformation

**Madlib slots filled:**

| Slot | Value |
|------|-------|
| TRIGGER | a CRO is accountable for pipeline generation targets but outbound productivity per rep is inconsistent and follow-up execution degrades after multi-touch sequences beyond three contacts |
| ROLE | the CRO |
| CHANGE | increases outbound pipeline generated per rep per quarter by [TBD% — source required] within [TBD days] of full AI Composer adoption across the SDR and AE teams |
| MECHANISM | AI Composer-assisted outbound sequences with personalization drawn from Meridian Analytics conversational context |
| FUNCTIONAL OUTCOME | hold the pipeline coverage ratio without headcount increases |
| BUSINESS GOAL | sales efficiency (pipeline generated per fully-loaded rep cost) as an operating metric reported to the CFO |

**Role elevation note:** The transformation shifted from "SDRs send better emails" (rep activity) to "the CRO increases pipeline per rep while holding headcount flat" (CRO accountability). Same product capability; completely different outcome frame. The test: would the CRO present this outcome to the CFO? Yes — pipeline per rep cost is a CFO metric. Would a rep present "I wrote better emails"? No. The CRO frame is correct for the stated segment.

---

### Outcome Statement

> When a CRO is accountable for pipeline generation targets but outbound productivity per rep is inconsistent and follow-up execution degrades after multi-touch sequences beyond three contacts, the CRO increases outbound pipeline generated per rep per quarter by [TBD% — source required] within [TBD days] of full AI Composer adoption across the SDR and AE teams, enabling the CRO to hold the pipeline coverage ratio without headcount increases that advances sales efficiency (pipeline generated per fully-loaded rep cost) as an operating metric reported to the CFO.

---

### Step 4 — Stage Classification

**Stage 4 — Business Goal.**

This is the only entry in the Meridian Analytics CRO set that reaches Stage 4 directly from the capability input. The reason: "pipeline generated per fully-loaded rep cost" is a metric the CFO and board track, not just the sales org. The CRO's mandate to hold pipeline coverage without headcount increases is an operating efficiency objective, not a desired sales outcome.

Stage 4 classification changes the renewal conversation posture. A Stage 4 outcome is presented to the CFO alongside the CS leader, not just to the CRO. It requires a calculation: if pipeline per rep increased X% and headcount held flat, what is the dollar value of the efficiency gain? That calculation belongs in the Business Impact Statement, which is the next layer of the full catalog entry beyond this skill's scope.

---

## What These Examples Illustrate Together

| Dimension | Example A (OCV-001) | Example B (OCV-002) |
|-----------|---------------------|---------------------|
| Primary failure mode | Product as subject; no customer role | Correct product area, wrong buyer lens |
| Recovery move | Reframe from product action to CRO visibility problem | Elevate from rep activity to CRO accountability metric |
| Stage reached | Stage 3 — Desired Outcome | Stage 4 — Business Goal |
| TRIGGER distinction | Business context vs. product activation | CRO constraint vs. rep task |
| Renewal conversation implication | CS presents to CRO with win rate evidence | CS presents to CRO + CFO with efficiency calculation |
| Magnitude status | [TBD] — direction and metric valid, range pending | [TBD] — direction and metric valid, range pending |

The pattern across both: the raw capability inputs described the product. The transformations describe what the CRO achieves. That shift — from product subject to customer subject — is the single most important move the skill makes.

---

*outcome-statement-builder v1.0.0 | References: Worked Examples | Meridian Analytics CRO Segment*
