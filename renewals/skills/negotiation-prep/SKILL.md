---
name: negotiation-prep
description: >
  Build a renewal negotiation brief for a specific account — pricing anchor,
  walk-away position, discount authority check, objection handling, and
  competitive counter-positioning. Use before any price conversation, contract
  negotiation, or renewal close call. Pulls commercial context from CRM and
  call recordings when connectors are available. All internal positioning is
  suppressed from customer-facing exports; only clean renewal proposals surface
  in shared outputs. Discount authority is validated against your configured
  ceiling — any offer that requires escalation is flagged before it reaches
  the customer.
argument-hint: "[<account-name-or-ID>] [--brief | --full | --export]"
version: "1.0.0"
---

# /renewals:negotiation-prep

Build a renewal negotiation brief calibrated to your account, authority, and
commercial posture.

---

## Pre-flight

Read both configuration files before preparing any negotiation brief:
1. `~/.claude/plugins/config/claude-for-customer-success/renewals/CLAUDE.md`
2. `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

If either file is missing or contains `[PLACEHOLDER]` markers in the pricing,
discount authority, or escalation fields, stop:

> "Your renewals practice profile isn't configured for negotiation prep — discount
> authority, pricing model, and escalation matrix are required. Run
> `/renewals:cold-start-interview` to configure these fields. Proceeding without
> them means the brief cannot validate whether proposed offers require approval."

Fields read from config:
- Pricing model and tier structure
- Discount authority ceiling (what you can approve without escalation)
- Escalation approval chain (who approves above-authority discounts)
- Standard price increase policy
- Multi-year deal incentive structure
- Negotiation posture (consultative / direct / data-led / segment-dependent)
- AE partner (for expansion or commercial co-ownership)
- Contract terms outside standard (requires Legal/Finance routing)

---


## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of negotiation prep request is this?
   - **Standard Renewal**: Account healthy, no pressure signals, renewal is routine with a possible price-increase conversation. Optimize for completeness over urgency.
   - **Price-Sensitive Renewal**: Budget freeze signals, prior price objections, declining usage, or scope reduction requests. Anchor integrity and concession sequencing are critical.
   - **Competitive Displacement Threat**: Competitor named in calls or CRM, active evaluation or RFP. Hold the anchor — do not panic-discount. Lead with value and switching cost.
   - **Stakeholder Disruption**: Champion departure, exec sponsor change, reorg. Validate the stakeholder map before building the brief — a stale map invalidates the negotiation posture.
   - **Expansion-Attached Renewal**: Renewal coincides with upsell or tier upgrade. Separate the renewal anchor from the expansion proposal — each needs its own walk-away.

2. **CONSTRAINTS**: What limits the solution space?
   - G4: Escalation path must be configured before generating negotiation guidance — no generic "escalate to your manager." Named owner, channel, and SLA required.
   - G5: Internal positioning, walk-away figures, competitive analysis, and discount authority details are confidential — suppressed entirely in `--export` mode. Verify output destination before generating.
   - G7: All data sources must carry a timestamp and staleness flag — CRM >7 days, call recordings >14 days. Never present stale commercial data without flagging it.
   - Discount authority ceiling from config gates every offer scenario — any offer below authority requires pre-call approval from the configured escalation owner.
   - Connected integrations limit what can be retrieved — flag gaps explicitly, never silently omit a data source.

3. **EXPERT CHECK**: What would a veteran renewal negotiator verify first?
   - Has the customer actually raised a price objection, or am I solving a problem that doesn't exist? Preemptive discounting trains customers to expect it.
   - Are the three numbers locked (anchor, first concession, walk-away) before the brief is complete? If any number requires on-call calculation, the brief is incomplete.
   - Is the stakeholder map current? Cross-reference CRM contacts against recent call attendees — a name/title list from CRM is not a verified stakeholder map.

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - Opening below anchor without pre-approved authority — every dollar below anchor in the opening is unrecoverable.
   - Treating the walk-away floor as the opening offer — the floor is the minimum acceptable outcome, not the starting position.
   - Fabricating competitor intelligence — if no competitive data is configured or confirmed from calls, say so. Do not invent competitor weaknesses or pricing.
   - Generating `--export` output before reviewing the internal brief — the export suppresses all strategy; the CSM must see the brief first.
   - Presenting a below-authority offer on a call without prior escalation approval — it sets a precedent and cannot be retracted.
   - Producing a thin brief for a "healthy" account without running the objection scan — latent objections surface on calls, not in CRM status fields.

**After execution**, verify:
- Does the brief give the CSM everything needed to walk into the negotiation prepared — anchor, concession path, floor, objection responses, and escalation routing?
- Are all offer scenarios validated against the configured discount authority ceiling?
- Is internal content fully suppressed if `--export` mode was used?
- Confidence: [High] if CRM + call data corroborate and authority is configured / [Medium] if single-source or partially stale data / [Low] if user-provided context only — state which.

## Mode

`--brief` (default): Core negotiation brief — pricing anchor, walk-away position,
discount authority summary, top 3 objections with responses, and recommended
opening. Most useful 24–48 hours before a renewal call.

`--full`: Expanded brief — all `--brief` content plus full objection bank,
multi-scenario offer modeling, competitive counter-positioning (if competitor
evaluation is confirmed), and stakeholder-by-stakeholder talking points.

`--export`: Clean customer-facing renewal proposal — suppresses all internal
positioning, walk-away notes, competitive analysis, and meta-commentary. Produces
only: proposed renewal terms, value summary, and next steps. Safe to share.

> ⚠️ `--export` mode output does NOT include any internal brief content.
> Review the brief first, then generate the export separately.

---

## Account identification and context pull

Ask: "Which account are you preparing for? Provide the account name, and tell me
the renewal date, ARR, current product tier, and any signals you've seen — objections
raised, price sensitivity, competitor mentions, stakeholder changes."

If a CRM connector is available, pull:
- Current ARR and contract terms (seat count / usage tier)
- Renewal date and days remaining
- Expansion history (prior upsells — indicates willingness to invest)
- Open support tickets or recent escalations (leverage points for the customer)
- Contact map: primary champion, economic buyer, executive sponsor status
- Opportunity stage and any notes from prior renewal conversations

If a call recording connector is available (Gong / Chorus), pull from the last
2–3 calls:
- Price objections raised and their framing
- Competitor mentions (name if captured)
- Budget signals (freeze, reduction, expansion)
- Decision-maker statements about renewal intent
- Unresolved commitments from your side

Confirm the pull before proceeding:
> "[CRM + Gong]: [account name] · $[ARR] ARR · renewal [date] · [N] days out ·
> [N] calls reviewed · last price signal: [summary] · data as of [timestamp]"

---

## Pricing anchor and opening position

Build the anchor from the account's commercial history and your configured pricing model.

### Anchor construction

| Factor | Source | Value |
|--------|--------|-------|
| Current ARR | CRM / user provided | $[amount] |
| Standard renewal (no change) | Config pricing model | $[same] |
| Configured price increase | Config price increase policy | +[%] |
| Full-ask anchor | Configured increase applied | $[amount] |
| Your opening offer | Anchor minus minimum concession room | $[amount] |

> Note: if a price increase applies, this account's anchor is the full
> post-increase figure. Do not open below the anchor unless discount authority
> is deliberately deployed. The anchor is what you ask for; the walk-away is
> what you can accept.

### Opening recommendation

State the opening position clearly:
> "Open at $[anchor amount] — the full renewal amount at [flat rate /
> [X]% increase per config]. This preserves concession room. Your first
> concession, if needed, should be [multi-year term / service credit /
> phased increase] rather than an immediate ARR reduction."

If the account has a confirmed competitor evaluation:
> "Competitive context: opening at full anchor signals confidence. A
> pre-emptive discount can signal weakness before the customer has applied
> pressure. Hold the anchor until they surface an explicit price objection."

---

## Walk-away position

Define the floor before the conversation starts.

| Walk-away element | Value |
|------------------|-------|
| Minimum acceptable ARR | $[current ARR] flat — no contraction without approval |
| Maximum discount within your authority | [configured discount authority %] → $[floor ARR] |
| Below-authority floor | Requires [escalation owner from config] approval |
| Absolute floor (with escalation approval) | [user provided or "not yet defined"] |

> "Walk-away is $[floor ARR]. Any offer below this requires escalation
> to [configured escalation owner] before presenting to the customer. Do not
> present below-authority offers without that approval — it sets a precedent
> and cannot be retracted."

If the customer pushes below the floor:
> "If they push below walk-away, the response is: 'I need to check with my team
> on what's possible — let me come back to you within [N] hours.' Do not
> improvise below-authority offers on the call."

---

## Discount authority check

Validate every offer scenario against the configured ceiling before the call.

| Offer scenario | ARR | Discount from anchor | Within authority? |
|---------------|-----|---------------------|------------------|
| Full anchor | $[amount] | 0% | ✅ |
| First concession | $[amount] | [X]% | ✅ / ⚠️ |
| Walk-away floor | $[amount] | [X]% | ✅ / ⚠️ |
| Below floor (escalation required) | $[amount] | [X]% | ❌ requires [owner] |

> ⚠️ `[review — discount authority]`
> Any offer at or below [X]% discount requires approval from [escalation owner
> from config] per your configured authority ceiling of [configured limit].
> Obtain approval before the call, not after.

If no discount authority is configured:
> "Discount authority is not configured in your practice profile. Run
> `/renewals:cold-start-interview --section pricing` to define it. Until
> configured, this field will not flag authority breaches."

---

## Objection handling

Match objections to the account's observed signals. For `--brief`, surface the
top 3 most likely objections. For `--full`, build the complete bank.

### Objection — Price / "It's too expensive"

**Signal match:** Price sensitivity mentioned in prior calls; competitive evaluation
confirmed; budget freeze signaled; no expansion in prior years.

**Response framework:**
1. Acknowledge: "I understand — budget scrutiny is real, and I want to make
   sure the investment makes sense for you."
2. Reframe to value delivered: Surface specific usage data, outcomes achieved,
   or ROI evidence from the account's own experience. Do not argue about
   price in the abstract.
3. Quantify the cost of switching: Implementation time, migration risk, retraining
   cost, productivity dip — especially if the account has a complex setup.
4. Offer a path: Multi-year discount / phased increase / service credit —
   whichever is within your authority and appropriate.

> Internal note: if they cite a competitor price, ask for the comparison in
> writing before responding. "Apples to apples" requests buy time and expose
> scope gaps in the competitor's offer.

---

### Objection — "We need to reduce scope / seats"

**Signal match:** Active user count significantly below licensed seat count;
department headcount reduction; champion mentions "we're not using everything."

**Response framework:**
1. Validate the usage data: "Let's look at actual usage together — I want to
   make sure you're paying for what you need, but not less than what you're
   using."
2. Distinguish seats from active users: "Your licensed count is [N]; active
   users are [N]. Before reducing, let's understand which teams are inactive
   and whether that's a training gap we could close."
3. Right-size honestly: If genuine over-licensing exists, a right-size to
   actual usage protects the relationship. A forced renewal at the full seat
   count creates a churn risk at the next cycle.
4. Protect ARR floor: Any seat reduction below [floor] requires approval.
   Flag it before agreeing.

---

### Objection — "We're looking at [Competitor]"

**Signal match:** Competitor name mentioned in calls or CRM notes; RFP issued;
champion mentions "evaluation"; procurement involved earlier than usual.

**Response framework:**
1. Clarify the stage: "Are you in an active evaluation, or exploring options?
   Understanding where you are helps me make sure I'm giving you the right
   information."
2. Do not panic and discount: Premature discounting signals weakness. Hold
   the anchor.
3. Ask for the evaluation criteria: "What's important to you in this decision?"
   — this surfaces what's actually driving the evaluation and where you need
   to demonstrate value.
4. Bring in reinforcement: Executive engagement, product roadmap preview, or
   case studies from comparable accounts. For large ARR accounts, route to AE
   partner or Head of CS for executive sponsorship.

> Internal note: [if specific competitor intelligence is configured, reference
> it here. If not: "No competitive intelligence is configured for this competitor
> in your practice profile. Run `/renewals:cold-start-interview --section
> churn-signals` to add competitive displacement patterns."]

---

### Objection — "We're not ready to decide yet"

**Signal match:** Renewal date approaching without champion engagement; executive
sponsor change; internal procurement delays.

**Response framework:**
1. Establish the decision timeline: "Our current contract expires [date]. To
   ensure continuity and avoid a lapse, we need a signed agreement by [N days
   before]. What's standing between you and that decision?"
2. Surface the real blocker: Is this internal budget approval, a stakeholder
   who hasn't signed off, or genuine ambivalence? The response depends on the
   root cause.
3. Offer a mutual action plan: "Let me draft a mutual action plan with the
   steps and owners on both sides — it often helps move things forward."
4. Escalate if inside 30 days with no decision signal: Route to configured
   escalation owner. This is a risk flag, not just a timeline issue.

---

### Additional objections (`--full` mode only)

For `--full` mode, extend the objection bank to cover:
- "We've had too many support issues" → Acknowledge; route to support escalation
  review; bring CSE or dedicated support offer to the table
- "We want to go month-to-month" → Understand the underlying concern; month-to-month
  pricing is typically higher — present the annual commitment advantage; flag
  if a month-to-month offer requires approval
- "We need new features before we renew" → Distinguish features on roadmap
  (shareable with appropriate caveats) from features not committed; never make
  a renewal contingent on undelivered product
- "Our usage is down / ROI isn't clear" → Trigger a success planning session
  before the renewal call; come with data, not with defensiveness

---

## Stakeholder map and talking points (`--full` mode)

For each named stakeholder in the account, surface tailored positioning:

| Stakeholder | Role | Primary concern | Talking point |
|-------------|------|----------------|---------------|
| [Champion name / role] | Day-to-day user | Product value / ROI | [Usage outcomes, efficiency gains, team adoption] |
| [Economic buyer / title] | Budget owner | Cost / business case | [Cost of switching, ROI, risk of disruption] |
| [Executive sponsor / title] | Strategic alignment | Partnership, roadmap | [Strategic direction, executive engagement offer] |
| [Procurement / title] | Contract terms | Standard terms, legal review | [Route to standard terms; flag non-standard asks to Legal] |

If a stakeholder has left or changed roles, flag it:
> "⚠️ [Name] is no longer in the [role] — confirm the replacement before the
> call. An unconfirmed stakeholder map going into a negotiation is a risk."

---

## Multi-scenario offer modeling (`--full` mode)

Build 3 scenarios before the call so you're never constructing offers on the fly:

| Scenario | Terms | ARR | Within authority? | Approval needed? |
|----------|-------|-----|-------------------|-----------------|
| Full anchor — annual | [current terms] | $[anchor] | ✅ | No |
| First concession — multi-year | 2-year + [configured multi-year incentive] | $[amount] | ✅ / ⚠️ | [if above authority] |
| Walk-away floor — annual | [reduced terms if applicable] | $[floor] | ✅ / ❌ | [if applicable] |

> Know your three numbers before the call: anchor, first concession, and floor.
> Never let the customer hear you calculating — it signals room.

---

## Escalation routing

If the negotiation exceeds your authority or requires executive involvement:

> "Escalation needed: [situation] — route to [configured owner] via [method]
> within [SLA from config]. Prepare:
> - Current negotiation position (anchor presented, counter received)
> - Customer's stated objection or demand
> - Your recommended response
> - ARR at stake and renewal date"

Do not present below-authority offers before obtaining approval. If the customer
demands an answer on the call:
> "I want to make sure I get you the right answer — let me confirm with my team
> and come back to you within [N hours]."

---

## Output format — Brief (`--brief` and `--full`)

---

**Negotiation Brief — [Account Name]** *(internal — do not share)*
*ARR: $[amount] · Renewal: [date] · [N] days out*
*Prepared: [date] · Sources: [list]*

**Opening position:** $[anchor] — [flat renewal / [X]% increase per config]
**Walk-away floor:** $[floor] — requires [owner] approval below this figure
**Authority ceiling:** [configured discount %] — $[floor ARR]

**Top objections to prepare for:**
1. [Objection 1] → [Response approach]
2. [Objection 2] → [Response approach]
3. [Objection 3] → [Response approach]

**Recommended opening:**
[2–3 sentences: what to say in the first 60 seconds of the commercial conversation]

**If they push hard:**
[What to do if the first concession isn't enough — and where the escalation
path is if you reach the floor]

**Before the call:**
- [ ] Confirm economic buyer is in the meeting
- [ ] Pull current usage data to have on hand
- [ ] Confirm any open support issues are resolved or have a clear owner
- [ ] Obtain approval if planning to open below anchor

---

> ⚠️ Reviewer note
> - **Sources:** [CRM ✓ verified | Gong ✓ verified | manual input]
> - **Data as of:** [timestamp per source | N/A]
> - **Read:** [account record | last [N] calls | expansion history | open tickets]
> - **Flagged for your judgment:** [N items — discount scenarios requiring
>   escalation | objections without confirmed signal from call data | none]
> - **Before the call:** Validate that no new information has surfaced since
>   this brief was generated — a stakeholder change or support escalation
>   the day of the call changes the posture

---

## Output format — Export (`--export`)

---

**[Company Name] Renewal Proposal**
*Prepared for: [Customer Name / Company]*
*Prepared by: [Your name from config]*
*Date: [date]*

**Your current plan:** [Product tier / seat count / usage tier] at $[ARR]/year,
renewing [date].

**Proposed renewal terms:**

| Option | Terms | Annual investment |
|--------|-------|------------------|
| [Option A — standard annual] | [terms] | $[amount] |
| [Option B — multi-year, if applicable] | [terms] | $[amount] |

**Value delivered this period:**
[2–3 sentences: specific usage data, outcomes, or milestones — pulled from
account context. No generic statements. If data is unavailable, leave this
section for the user to complete before sending.]

**What's next:**
1. Review the options above and let me know which works best for your team
2. I'll send the updated contract for signature by [date]
3. Any questions — I'm available at [contact]

---

*This proposal is valid through [renewal date + 14 days]. Questions about
terms or contract specifics? I'll connect you with the right person.*

---

## Guardrails

**Discount authority check is mandatory.** Every offer scenario is validated
against the configured discount authority ceiling before the brief is complete.
Any offer requiring escalation is flagged before the call. This guardrail
cannot be overridden by conversation.

**Walk-away is not a starting point.** The walk-away floor is the minimum
acceptable outcome — it is not the opening offer. Opening at the floor removes
all concession room and signals desperation.

**No fabricated competitor intelligence.** If competitive positioning is included,
it must reference configured churn signal data or confirmed call recording signals.
Do not invent competitor weaknesses or pricing claims.

**Export suppresses all internal content.** The `--export` output contains no
internal positioning, walk-away figures, competitor notes, or escalation guidance.
Review and generate separately — never share the brief directly.

**Stakeholder maps require verification.** If an executive sponsor or champion
has changed, flag it before the call. A negotiation with an incomplete stakeholder
map is a risk.

**Route contract non-standards to Legal.** If the customer pushes for non-standard
contract terms (IP, liability, indemnification, data residency), route to Legal
before responding. Do not improvise contract language on a renewal call.

**Revenue commitment language.** Any renewal ARR figure in this brief is an
in-negotiation projection, not a closed-won revenue commitment. Flag any scenario
table with `[review — not yet a revenue commitment]` if it will be shared with
leadership before the deal is signed.
