# Agent T — Trigger Audit Report

**Date:** 2026-05-18
**Auditor:** Agent T — Trigger Precision Red-Teamer
**Scope:** All SKILL.md files across 5 plugins: csm, renewals, onboarding, cs-ops, rev-ops
**Method:** Adversarial probe of Use When / Do NOT Use For / Typical Activation blocks for FP, FN, and collision risk

---

## Summary

- **Skills audited:** 80
- **Findings:** 6 BLOCK / 19 WARN / 14 NOTE

---

## Findings

---

### [BLOCK] csm/cold-start-interview ↔ csm/customize — Trigger Collision

**Type:** Collision
**Trigger text (cold-start-interview):** "Set up the CSM plugin for my company" / "Configure the plugin from scratch"
**Trigger text (customize):** "Update my churn signal definitions" / `/csm:customize --section escalation-matrix`
**Finding:** Both skills claim ownership of full CSM configuration. `cold-start-interview` owns "first run"; `customize` is supposed to be for targeted updates. But `customize`'s own description says "Alias for cold-start-interview when run fresh." A user invoking "set up my CSM plugin" or "configure the CSM plugin" can reasonably land in either. `customize`'s `Use When` includes "First install: running full configuration" — which directly overlaps with `cold-start-interview`'s explicit purpose. There is no signal in the trigger blocks that distinguishes which skill fires when both are present.
**Adversarial input:** "Configure my CSM plugin for the first time"
**Collides with:** `csm/cold-start-interview`
**Recommendation:** `customize`'s `Use When` must remove "First install" bullet entirely and add an explicit exclusion: "Do NOT use for first-time installation — use `/csm:cold-start-interview` instead." Alternatively, collapse the two skills; the alias relationship without clear disambiguation is a split-brain trigger.

---

### [BLOCK] renewals/churn-analysis ↔ renewals/churn-rca — Trigger Collision

**Type:** Collision
**Trigger text (churn-analysis):** "A renewal has been confirmed lost or contracted and you need to extract root cause while the context is fresh (within 30 days)"
**Trigger text (churn-rca):** "A CSM or RevOps analyst needs to perform root cause analysis on a confirmed full contract cancellation"
**Finding:** Two skills both perform post-churn root cause analysis on closed losses. `churn-analysis` explicitly includes "contraction" events; `churn-rca` explicitly excludes them (redirecting to `downgrade-analysis`). The boundary is the word "contraction" — but a user saying "we lost Acme Corp, help me understand why" will not naturally know whether their loss was "churn" or "contraction" in skill vocabulary. The typical activation examples on both skills are nearly identical in surface form. There is no routing mechanism in the trigger blocks that would prevent dual activation.
**Adversarial input:** "We lost Acme Corp this month. Run a root cause analysis."
**Collides with:** `renewals/churn-analysis`
**Recommendation:** One of these skills must defer to the other. If `churn-rca` is the canonical post-churn RCA (and it has the more precise scope), then `churn-analysis` should be retitled (e.g., `churn-signal-retrospective`) with a `Do NOT use for` that explicitly redirects full-cancellation RCA to `renewals:churn-rca`. The current state will produce user confusion and non-deterministic skill selection.

---

### [BLOCK] csm/success-plan-builder ↔ csm/success-plan-canvas — Trigger Collision

**Type:** Collision
**Trigger text (success-plan-builder):** "Starting a new customer engagement and need to establish a formal success plan"
**Trigger text (success-plan-canvas):** "A CSM needs to generate a structured success plan canvas for a specific account at a lifecycle stage"
**Finding:** Both skills build success plans for new accounts. `success-plan-builder` owns "the co-authored document"; `success-plan-canvas` owns "the structured canvas." These sound different but the user will say "build a success plan for Acme" and have no basis to know which format to use. `success-plan-builder` explicitly says "Do NOT use for the structured success plan canvas format — use success-plan-canvas" — but this assumes the user already knows about the distinction before selecting. At the trigger level, both fire on "build a success plan for [account]."
**Adversarial input:** "Build a success plan for Acme Corp — they just kicked off."
**Collides with:** `csm/success-plan-builder`
**Recommendation:** The `Use When` for each skill must encode the decision criteria: `success-plan-builder` for unstructured narrative/co-authored document; `success-plan-canvas` for OCV-aligned 7-component structured canvas. Add distinguishing language to `Typical Activation` that makes the format difference salient before the user selects. A natural-language trigger of "success plan" will collide without this.

---

### [BLOCK] rev-ops/deal-to-outcome-tracing ↔ rev-ops/outcome-to-value-tracking — Trigger Collision

**Type:** Collision
**Trigger text (deal-to-outcome):** "Links every closed/won opportunity to its downstream CS trajectory using the OCV Outcome Catalog"
**Trigger text (outcome-to-value):** "Maps each customer to their L0–L3 rubric level on their referenced OCV entries at OCV-defined verification milestones"
**Finding:** Both skills operate on L0–L3 OCV rubric levels for closed customers. `deal-to-outcome-tracing` says it does "30/60/90/180-day checkpoint assessments" and "rubric level assessment." `outcome-to-value-tracking` also does "rubric level tracking per account and per OCV entry." The `Typical Activation` examples are almost indistinguishable: "track outcomes for [account]" vs. "value realization report" and "are customers achieving outcomes." A user asking "how is Acme tracking on their outcomes?" could activate either.
**Adversarial input:** "What rubric level is Acme Corp at on their OCV outcomes? It's been 90 days."
**Collides with:** `rev-ops/deal-to-outcome-tracing`
**Recommendation:** `outcome-to-value-tracking` must explicitly exclude checkpoint rubric assessments and redirect them to `deal-to-outcome-tracing`. Its `Do NOT use for` already mentions "rubric level assessment at checkpoints" but this isn't prominent enough — and both skills' `Use When` blocks independently claim rubric level ownership. Enforce a hard boundary: tracing = per-account checkpoint cadence; value-tracking = portfolio aggregate view only.

---

### [BLOCK] cs-ops/cold-start-interview ↔ cs-ops/customize — Trigger Collision (parallel to csm pattern)

**Type:** Collision
**Trigger text (cold-start):** "Installing the CS-Ops plugin for the first time — no config file exists"
**Trigger text (customize):** "Onboarding to the plugin for the first time (filling placeholder sections)"
**Finding:** `cs-ops/customize`'s `Use When` explicitly includes "onboarding to the plugin for the first time" — which is also the primary purpose of `cold-start-interview`. A new user will receive conflicting signals: both skills claim to handle first-time setup. The distinction (cold-start = blank slate; customize = has existing placeholders) is too fine-grained to reliably disambiguate from user-facing natural language.
**Adversarial input:** "I just installed cs-ops. How do I set it up?"
**Collides with:** `cs-ops/cold-start-interview`
**Recommendation:** Remove "onboarding to the plugin for the first time" from `cs-ops/customize`'s `Use When`. That clause belongs exclusively to `cold-start-interview`. The customize skill should only activate when a config file already exists.

---

### [BLOCK] csm/health-score-review ↔ csm/risk-flag — Trigger Collision on "churn signal detected" scenario

**Type:** Collision
**Trigger text (health-score-review):** "A health signal has triggered (usage drop, NPS decline, support spike, champion departure)"
**Trigger text (risk-flag):** "A churn signal has been detected and you need to determine escalation routing"
**Finding:** The scenarios are identical — "churn signal detected" and "health signal triggered" describe the same event using different vocabulary. Both skills are appropriate responses to the same input. A CSM who sees a usage drop and says "there's a churn signal on Acme" will not know whether to run health-score-review (to understand the signal state) or risk-flag (to determine escalation). The differentiation is in the intended output (narrative vs. escalation memo), but this isn't recoverable from the trigger text alone.
**Adversarial input:** "Acme's usage dropped 40% this week. What should I do?"
**Collides with:** `csm/risk-flag`
**Recommendation:** Establish explicit sequential dependency in both triggers: `health-score-review`'s `Use When` should say "First step when a signal fires — before escalation routing." `risk-flag`'s `Use When` should say "After health-score-review confirms signal aggregate exceeds threshold — for escalation routing decision." The current trigger blocks treat them as alternatives rather than a sequence.

---

### [WARN] csm/account-research ↔ csm/call-prep — Scope Bleed

**Type:** FP / Collision
**Trigger text (account-research):** "Building context before any customer-facing call: kickoff, QBR, health check, renewal, check-in"
**Trigger text (call-prep):** "24-48 hours before any customer call: kickoff, QBR, health check, renewal, escalation, check-in"
**Finding:** Both skills activate on "before a call." `account-research`'s `Do NOT use for` says "Replacing call-prep — account-research provides context; call-prep produces the brief" — but the `Use When` for `account-research` lists the same call types (kickoff, QBR, health check, renewal) that `call-prep` lists. A CSM saying "I have a QBR tomorrow, help me prep" may activate either. The `call-prep` description says "Pairs with account-research for full context" — but this complementary relationship isn't enforced by the trigger; it's documented in the description, which is not the trigger block.
**Adversarial input:** "Prep me for my renewal call with Acme tomorrow."
**Collides with:** `csm/call-prep`
**Recommendation:** `account-research`'s `Use When` should be scoped to "when session context is absent" or "initial account context pull" — not repeated for every call type. Reserve the call-type list for `call-prep`; `account-research` should activate on "no context in session" conditions, not "before any call."

---

### [WARN] csm/renewal-readiness ↔ csm/risk-flag — 90-Day Window Overlap

**Type:** Collision
**Trigger text (renewal-readiness):** "Renewal is approaching and you need to surface known objections and risks"
**Trigger text (risk-flag):** "Renewal is approaching and you need a structured risk assessment before the commercial conversation"
**Finding:** Both skills share the identical trigger condition: "renewal approaching + risk assessment needed." `renewal-readiness` owns the 90-day-out readiness picture for all accounts; `risk-flag` owns at-risk signal assessment. But a CSM with a renewal in 60 days who spots concerning signals will rationally activate both. The trigger blocks do not distinguish "all-accounts renewal prep" (renewal-readiness) from "at-risk renewal prep" (risk-flag).
**Adversarial input:** "Acme's renewal is in 60 days and they've gone quiet. What do I do?"
**Collides with:** `csm/risk-flag`
**Recommendation:** `risk-flag`'s `Use When` should remove the renewal-proximity trigger. Risk-flag fires on signal presence, not calendar proximity. `renewal-readiness` owns the calendar-based trigger. Add to `risk-flag`'s `Do NOT use for`: "Renewal prep without active risk signals — use /csm:renewal-readiness."

---

### [WARN] csm/qbr-builder ↔ csm/value-statement — Pre-QBR Scope Bleed

**Type:** FP
**Trigger text (qbr-builder):** "Preparing a Quarterly Business Review or Executive Business Review for a customer"
**Trigger text (value-statement):** "Drafting value messaging for a QBR, renewal, or business review"
**Finding:** `value-statement` explicitly activates on QBR prep. `qbr-builder` owns QBR construction. A user saying "I need value content for my QBR" will activate `value-statement`; a user saying "build my QBR" will activate `qbr-builder` — but those two inputs are often interchangeable in practice. The `Do NOT use for` on `value-statement` references `qbr-builder` for "full QBR deck construction" but doesn't clarify when the value statement is the right smaller-scope tool vs. when to go straight to QBR.
**Adversarial input:** "I need to show value for my Acme QBR next week."
**Collides with:** `csm/qbr-builder`
**Recommendation:** `value-statement`'s `Use When` should specify the scope condition: "when the value narrative is the only output needed, not a full QBR deck." Add a decision criterion: "If you need the full QBR structure, use /csm:qbr-builder; if you need the value story as a standalone section or document, use this skill."

---

### [WARN] renewals/risk-assessment ↔ csm/risk-flag — Cross-Plugin Collision

**Type:** Collision
**Trigger text (renewals/risk-assessment):** "A churn signal has been detected and the account needs immediate triage"
**Trigger text (csm/risk-flag):** "A churn signal has been detected and you need to determine escalation routing"
**Finding:** These are nearly identical trigger conditions across two plugins. A CSM who detects a churn signal does not know whether to use `csm:risk-flag` (their own plugin) or `renewals:risk-assessment` (the renewals plugin). The scoping distinction — renewals is for the 90/60/30-day window; csm is for day-to-day signal response — is not reflected in the trigger blocks.
**Adversarial input:** "I just got alerted that Acme's NPS dropped to 3. What's their risk?"
**Collides with:** `csm/risk-flag`
**Recommendation:** `renewals/risk-assessment`'s trigger should require explicit renewal-window context: "Use when a churn signal appears within the 90-day renewal window." `csm/risk-flag` should own all signal-triggered risk assessment outside the renewal window. Add mutual exclusion language to each `Do NOT use for`.

---

### [WARN] rev-ops/crm-hygiene-audit ↔ rev-ops/data-quality-check (cs-ops) — Cross-Plugin Collision

**Type:** Collision
**Trigger text (rev-ops/crm-hygiene-audit):** "CRM data quality needs a structured audit across key pipeline fields"
**Trigger text (cs-ops/data-quality-check):** "Audit CRM and CS platform data quality against configured field requirements"
**Finding:** Both skills audit CRM data quality. `rev-ops/crm-hygiene-audit` is scoped to pipeline fields; `cs-ops/data-quality-check` is scoped to CS platform fields. But CRM is shared infrastructure. A user asking "audit our CRM data quality" will not know which plugin to use, and neither `Do NOT use for` block explicitly names the other.
**Adversarial input:** "Our CRM data quality is unreliable. Run an audit."
**Collides with:** `cs-ops/data-quality-check`
**Recommendation:** Add explicit cross-plugin exclusion to both `Do NOT use for` blocks: `rev-ops/crm-hygiene-audit` → "CS platform data quality — use `/cs-ops:data-quality-check`"; `cs-ops/data-quality-check` → "Sales pipeline field hygiene — use `/rev-ops:crm-hygiene-audit`."

---

### [WARN] rev-ops/field-completion-monitoring ↔ rev-ops/crm-hygiene-audit ↔ rev-ops/data-decay-tracking — Three-Way Collision Cluster

**Type:** Collision
**Trigger text (field-completion):** "Required CRM field completion rates need to be tracked over time"
**Trigger text (crm-hygiene):** "CRM data quality needs a structured audit across key pipeline fields"
**Trigger text (data-decay):** "CRM record staleness needs to be quantified and trended"
**Finding:** Three rev-ops skills all fire on "CRM data is bad / incomplete / stale." The `Do NOT use for` on each skill redirects to the others, but the top-level `Use When` conditions are too similar for reliable disambiguation. A user with a CRM data problem does not have enough signal to route correctly without already knowing the taxonomy (completeness vs. hygiene vs. decay).
**Adversarial input:** "Our CRM data is a mess. Help me understand what's wrong."
**Collides with:** `rev-ops/crm-hygiene-audit`, `rev-ops/data-decay-tracking`
**Recommendation:** The trio needs a routing primer in each `Use When` block: field-completion = "when tracking fill rate over time"; crm-hygiene = "when needing a point-in-time overall health score"; data-decay = "when contact/company record age is the specific concern." The `Typical Activation` examples do not currently disambiguate these.

---

### [WARN] rev-ops/pipeline-coverage-analysis ↔ rev-ops/pipeline-velocity-tracking — Shared "Pipeline Health" Trigger Space

**Type:** Collision
**Trigger text (coverage):** "Assess pipeline health before a forecast call"
**Trigger text (velocity):** "Understand how fast deals move through pipeline stages"
**Finding:** Both are "pipeline health" skills. "Pipeline health" is one of the most common RevOps phrases. Coverage fires on "do we have enough?"; velocity fires on "are deals moving?". But in practice, these are often asked together. The `Typical Activation` for coverage includes "pipeline health check" and velocity includes "health check on my pipeline" — identical surface-form activation phrases pointing to different skills.
**Adversarial input:** "Run a pipeline health check for Q2."
**Collides with:** `rev-ops/pipeline-velocity-tracking`
**Recommendation:** Remove "pipeline health check" from `Typical Activation` on both. Reserve "coverage" language for `pipeline-coverage-analysis`; reserve "velocity," "cycle time," and "aging" language for `pipeline-velocity-tracking`. The generic "health check" phrase must not appear in either trigger block.

---

### [WARN] onboarding/kickoff-prep ↔ csm/call-prep — Cross-Plugin Overlap

**Type:** Collision
**Trigger text (kickoff-prep):** "Prep me for my kickoff with [Account] on [date]"
**Trigger text (csm/call-prep):** "Prep me for my call with [customer] tomorrow" / "call-prep Acme Corp kickoff"
**Finding:** `csm/call-prep` explicitly lists "kickoff" as a call type it handles. `onboarding/kickoff-prep` is a dedicated skill for kickoff preparation. A CSM using the csm plugin (not onboarding) who has a kickoff will use `csm:call-prep kickoff` — and that may produce a generic call brief rather than the onboarding-model-specific agenda. But a user who says "prep my kickoff call" without a namespace could activate either.
**Adversarial input:** "Prep me for my onboarding kickoff with Acme tomorrow."
**Collides with:** `csm/call-prep`
**Recommendation:** `csm/call-prep`'s `Use When` should note: "For onboarding kickoffs, prefer `/onboarding:kickoff-prep` for agenda and checklist — this skill provides a lighter pre-call brief." Add this as a cross-plugin routing note, not a hard exclusion.

---

### [WARN] renewals/negotiation-prep ↔ csm/renewal-readiness — Renewal Conversation Ownership Ambiguity

**Type:** FP / FN
**Trigger text (negotiation-prep):** "You are preparing for a renewal call, contract negotiation, or price conversation"
**Trigger text (renewal-readiness):** "Preparing for the renewal conversation and need to surface known objections and risks"
**Finding:** Both skills prepare the CSM for the renewal conversation. The distinction is: `renewal-readiness` owns pre-conversation readiness assessment 90 days out; `negotiation-prep` owns the call-ready brief. But "preparing for the renewal conversation" is in both `Use When` blocks with no timing cue. A CSM who is 60 days from renewal and wants renewal call prep could reasonably invoke either.
**Adversarial input:** "Acme's renewal is in 60 days. Help me prep for the renewal conversation."
**Collides with:** `csm/renewal-readiness`
**Recommendation:** `renewals/negotiation-prep` should require an explicit commercial context signal: "Use when pricing, discounting, or contract terms are on the table." `csm/renewal-readiness` owns anything that isn't yet commercial. Add timing language: "Use negotiation-prep when the commercial conversation is imminent (within 30 days or already scheduled)."

---

### [WARN] rev-ops/revenue-brief-generation ↔ cs-ops/metric-dashboard — Executive Report Collision

**Type:** Collision
**Trigger text (revenue-brief):** "Leadership or board review requires a structured revenue performance brief"
**Trigger text (metric-dashboard):** "Building the monthly CS performance summary for the executive team" / "Preparing the quarterly CS section of a board or investor presentation"
**Finding:** Both produce executive-facing revenue/CS metrics content. `metric-dashboard` is explicitly positioned for board and executive presentations. `revenue-brief-generation` is also positioned for board and executive content. A Head of CS preparing for a board review has no basis to choose between them from the trigger blocks alone.
**Adversarial input:** "I need a board-ready summary of CS performance this quarter."
**Collides with:** `rev-ops/revenue-brief-generation`
**Recommendation:** `cs-ops/metric-dashboard` should own CS-specific metrics (GRR, NRR, health distribution, CSM performance). `rev-ops/revenue-brief-generation` should own the cross-functional revenue narrative (Sales + CS combined). Add explicit scope statement to each: "This skill covers CS-function metrics only" vs. "This skill covers full revenue system across Sales and CS."

---

### [WARN] rev-ops/early-churn-downgrade-signal-detection ↔ renewals/risk-assessment — Churn Signal Ownership

**Type:** Collision
**Trigger text (early-churn):** "Account shows structural signals suggesting churn or downgrade risk"
**Trigger text (renewals/risk-assessment):** "A churn signal has been detected (login drop, NPS decline, executive sponsor departure)"
**Finding:** Both skills detect and respond to churn signals on active accounts. `early-churn` claims to start at deal close (earlier in lifecycle); `renewals/risk-assessment` claims to act at 90/60/30-day renewal windows. But both can be activated by "churn signal detected on account" — and neither `Do NOT use for` explicitly names the other.
**Adversarial input:** "We're seeing warning signs on Acme. Assess the churn risk."
**Collides with:** `renewals/risk-assessment`
**Recommendation:** Add explicit lifecycle-stage exclusions. `early-churn`'s `Do NOT use for` should include: "90-day renewal window risk triage — use `renewals:risk-assessment`." `renewals/risk-assessment`'s `Do NOT use for` should include: "Structural deal-close signals — use `rev-ops:early-churn-downgrade-signal-detection`."

---

### [WARN] csm/taro-play-runner ↔ cs-ops/playbook-auditor — "What play applies?" Ambiguity

**Type:** FP
**Trigger text (taro-play-runner):** "What play applies to [account]?"
**Trigger text (playbook-auditor):** Not a direct collision — but `Do NOT use for` on `playbook-auditor` redirects individual play execution to `/csm:play-runner` (incorrect skill name: should be `taro-play-runner`)
**Finding:** The `Do NOT use for` in `cs-ops/playbook-auditor` references `/csm:play-runner` which is not the actual skill name. The correct name is `csm:taro-play-runner`. This is a broken cross-reference in the exclusion block that will route users to a non-existent skill. Additionally, a question like "What plays do I have for this situation?" could fire the auditor (which catalogs plays) rather than the runner (which executes them).
**Adversarial input:** "What play should I run for an at-risk account?"
**Collides with:** `cs-ops/playbook-auditor` (coverage mode)
**Recommendation:** Fix `cs-ops/playbook-auditor`'s `Do NOT use for` to reference `csm:taro-play-runner` by correct name. Add to `taro-play-runner`'s `Do NOT use for`: "Assessing whether the right plays exist in your playbook — use `/cs-ops:playbook-auditor`."

---

### [NOTE] csm/expansion-business-case ↔ csm/value-statement — CSQL Expansion Brief Overlap

**Type:** FP
**Trigger text (expansion-business-case):** "Build a business case for expanding to the enterprise tier with Acme Corp"
**Trigger text (value-statement):** "Generating internal expansion signal documentation (expansion mode — never customer-facing)"
**Finding:** `value-statement` has an `--ae-handoff` mode that produces "internal expansion signal documentation." `expansion-business-case` has a `csql` mode that produces a "CSQL Qualification Package for Sales handoff." Both produce internal expansion-to-AE handoff documents. The trigger surface overlap is narrow but present: a CSM preparing to hand off an expansion to the AE could land in either.
**Adversarial input:** "I want to document the expansion signal for Acme to hand off to the AE."
**Collides with:** `csm/expansion-business-case` (csql mode)
**Recommendation:** `value-statement`'s `Do NOT use for` should explicitly redirect AE-handoff expansion packages to `csm:expansion-business-case [mode=csql]`.

---

### [NOTE] onboarding/success-criteria ↔ csm/success-plan-builder — Success Criteria Ownership

**Type:** FP
**Trigger text (onboarding/success-criteria):** "Define success criteria for [Account]" / "We need to refine the success criteria after the kickoff call"
**Trigger text (csm/success-plan-builder):** "Starting a new customer engagement and need to establish a formal success plan" (which includes success criteria)
**Finding:** `success-plan-builder` is explicitly the co-authored document that includes success criteria. `onboarding/success-criteria` defines and tracks onboarding-specific criteria. A CSM onboarding a new account who wants to establish success criteria could use either. The boundary (onboarding-scoped vs. full lifecycle) is meaningful but not surfaced in the trigger language.
**Adversarial input:** "Define success criteria for TechCo — they just had their kickoff."
**Collides with:** `csm/success-plan-builder`
**Recommendation:** `onboarding/success-criteria`'s `Use When` should explicitly scope to the onboarding period: "Use when defining success criteria within the onboarding lifecycle stage." Add cross-reference: "For post-onboarding success criteria as part of an ongoing success plan, use `/csm:success-plan-builder`."

---

### [NOTE] rev-ops/deal-classification ↔ rev-ops/deal-health-scoring — "Is this deal ok?" Overlap

**Type:** FP
**Trigger text (classification):** "ARR classification is disputed or ambiguous for a specific opportunity"
**Trigger text (health-scoring):** "Deal review requires objective signal aggregation"
**Finding:** "Classify this deal" (what type is it?) and "score this deal" (how healthy is it?) are adjacent but distinct. The trigger blocks are clean enough — but the `Typical Activation` examples on health-scoring include "CS pipeline health" and "flag unhealthy expansion deals" without specifying the health score is the output, not a classification. Minor disambiguation needed.
**Adversarial input:** "Is this expansion deal in good shape?"
**Collides with:** `rev-ops/deal-classification` (minor)
**Recommendation:** `deal-health-scoring`'s `Typical Activation` should not use "classify" or "classification" language. Ensure all examples use "score," "health," or "risk" framing.

---

### [NOTE] rev-ops/annual-planning-workflow — FN Risk on "Mid-Year" Input

**Type:** FN
**Trigger text:** "Mid-year replanning triggered by miss (use mid-year-replan-triggering)"
**Finding:** The `Do NOT use for` correctly excludes mid-year replanning. But the `Use When` block says "Annual planning workflow orchestration is needed across multiple RevOps domains" and `Typical Activation` doesn't include any examples that would clearly fire for "we missed H1, do we need to replan?" — this input correctly routes to `mid-year-replan-triggering`. But a user saying "we need to re-do our plan" mid-year is ambiguous. The skill's `Do NOT use for` handles this correctly, but `mid-year-replan-triggering`'s own trigger should be primary.
**Adversarial input:** "We're halfway through the year and we've missed by 20%. Do we need to update our plan?"
**Recommendation:** Minor: Add "plan adjustment triggered by actuals" to `annual-planning-workflow`'s `Do NOT use for`. Currently the block excludes "Mid-year replanning triggered by miss" — sufficient but could be stated more explicitly.

---

### [NOTE] onboarding/handoff-doc ↔ rev-ops/sales-cs-handoff-quality-scoring — Handoff Direction Ambiguity

**Type:** FP
**Trigger text (handoff-doc):** "Generate the onboarding graduation handoff document"
**Trigger text (sales-cs-handoff-quality-scoring):** "Closed deal is entering CS onboarding and handoff quality needs assessment"
**Finding:** Both skills operate at the Sales→CS handoff point, but in opposite directions: `handoff-doc` generates the CS→post-onboarding graduation document; `sales-cs-handoff-quality-scoring` scores the Sales→CS handoff. The vocabulary is confusing: "handoff document" and "handoff quality scoring" could both activate on "I need to document this handoff." The distinction between Sales-to-CS and CS-to-postCS is not prominent in either trigger block.
**Adversarial input:** "We need a handoff document for Acme Corp."
**Collides with:** `rev-ops/sales-cs-handoff-quality-scoring`
**Recommendation:** Both skills should explicitly state directionality in their first trigger line. `handoff-doc`: "Onboarding-to-post-onboarding graduation handoff (CS team internal)." `sales-cs-handoff-quality-scoring`: "Sales-to-CS handoff quality scoring at deal close."

---

### [NOTE] cs-ops/capacity-planner ↔ rev-ops/closed-won-to-cs-capacity-modeling — CS Capacity Ownership

**Type:** Collision
**Trigger text (cs-ops/capacity-planner):** "Quarterly planning requires current CSM load vs. target ratio analysis" / "A CSM is departing"
**Trigger text (rev-ops/closed-won):** "CS team capacity needs to be assessed against incoming closed-won volume"
**Finding:** Both address CS capacity. `cs-ops/capacity-planner` owns current-state CSM load analysis; `rev-ops/closed-won` owns demand-driven CS capacity modeling (forward-looking). The trigger boundary is "current state" vs. "projected demand from pipeline." The `Do NOT use for` on `rev-ops/closed-won` does redirect "individual CS assignment decisions" but does not explicitly exclude current-state headcount reviews. A manager asking "do we have enough CSMs?" could activate either.
**Adversarial input:** "Do we have enough CSMs to handle our current pipeline?"
**Collides with:** `cs-ops/capacity-planner`
**Recommendation:** `rev-ops/closed-won` should add to `Do NOT use for`: "Current-state CSM load analysis without a pipeline forecast — use `/cs-ops:capacity-planner`." The forward/backward temporal dimension is the critical differentiator and should be explicit.

---

### [NOTE] renewals/expansion-signal ↔ csm/expansion-business-case — Pre-CSQL Signal vs. CSQL Package Ambiguity

**Type:** FP
**Trigger text (expansion-signal):** "You need to identify and qualify seat growth, usage expansion, product tier upsell, or cross-sell signals in a specific account"
**Trigger text (expansion-business-case):** "Build a business case for expanding to the enterprise tier with Acme Corp"
**Finding:** `expansion-signal` identifies and qualifies signals; `expansion-business-case` builds the case once signals are confirmed. These should be sequential. But a user saying "I want to pursue expansion with Acme" may skip `expansion-signal` and go straight to `expansion-business-case` — or vice versa if they already know the signal. The skills don't explicitly reference each other in their trigger blocks.
**Adversarial input:** "I think Acme is ready for an expansion. How do I move forward?"
**Recommendation:** Add a dependency note to `expansion-business-case`'s `Use When`: "After expansion signals have been identified and qualified via `/renewals:expansion-signal`." `expansion-signal`'s `Use When` should add: "Before building a business case — use `/csm:expansion-business-case` once signals are at pipeline-ready or qualified tier."

---

### [NOTE] rev-ops/gtm-unified-metrics-pulse ↔ rev-ops/revenue-brief-generation — "Weekly Executive Summary" Collision

**Type:** FP
**Trigger text (gtm-pulse):** "Weekly or monthly GTM metrics brief required across functions" / "GTM health snapshot"
**Trigger text (revenue-brief):** "Weekly or monthly revenue status needs synthesis across pipeline, forecast, and actuals" / "Revenue brief for leadership"
**Finding:** Both skills produce weekly executive revenue summaries. The difference is subtle: `gtm-pulse` is multi-function (Sales + CS combined metrics); `revenue-brief` is a narrative synthesis. But the `Typical Activation` examples are functionally identical for a RevOps person tasked with "the weekly leadership update." Neither `Do NOT use for` block cross-references the other.
**Adversarial input:** "Run the weekly leadership revenue update."
**Collides with:** `rev-ops/revenue-brief-generation`
**Recommendation:** Both `Do NOT use for` blocks should reference the other. `gtm-pulse` → "Narrative revenue brief — use `revenue-brief-generation`." `revenue-brief` → "Cross-functional metrics dashboard — use `gtm-unified-metrics-pulse`." Establish that pulse = metrics/data; brief = narrative/story.

---

### [NOTE] renewals/price-increase-prep — FN on "CPI Clause" Renewal Trigger

**Type:** FN
**Trigger text:** "An account is approaching renewal with a contractual CPI or escalation clause and you need to confirm what applies and draft compliant notification"
**Finding:** This is a legitimate `Use When` but it will not activate naturally. A user managing renewal timelines is unlikely to say "I have a CPI clause renewal" — they will say "Acme's renewal is next month, do I need to send a price notice?" The `Typical Activation` block does not contain examples that surface this scenario. The CPI/escalation clause use case is buried in `Use When` text that users won't search against.
**Adversarial input:** "Acme's contract has a 3% annual increase. Their renewal is in 45 days. What do I do?"
**Recommendation:** Add a `Typical Activation` example that surfaces the CPI scenario: "Acme has a CPI escalation clause — what notice do I need to send before renewal?"

---

### [NOTE] onboarding/ttv-analysis — FP Risk on "Is this account on track?" Input

**Type:** FP
**Trigger text:** "Is [Account] on track for TtV?"
**Finding:** "Is Acme on track?" is also a natural trigger for `onboarding/milestone-tracker` ("Where are we on milestones for [Account]?"). The two skills overlap on the "single account progress check" use case. `ttv-analysis` is an internal planning tool; `milestone-tracker` is the execution-layer status view. But both answer "is this account on track?" and neither `Do NOT use for` explicitly names the other.
**Adversarial input:** "Is TechCo on track with their onboarding?"
**Collides with:** `onboarding/milestone-tracker`
**Recommendation:** `ttv-analysis`'s `Use When` should clarify this is for "TtV pace assessment against segment benchmarks" not milestone status. `milestone-tracker` owns "status of this account." Add to `ttv-analysis`'s `Do NOT use for`: "Current milestone status view — use `/onboarding:milestone-tracker`."

---

## High-Collision Clusters

Three structural collision clusters warrant architectural attention beyond individual fixes:

**Cluster A — Success Planning (csm plugin):** `success-plan-builder`, `success-plan-canvas`, `success-plan-progress-review` form a three-skill chain with ambiguous entry point. Natural-language success plan requests don't route cleanly to any one skill. Requires explicit `Use When` scoping that encodes document format (builder = narrative, canvas = OCV-structured, progress-review = downstream of canvas only).

**Cluster B — CRM Data Quality (rev-ops plugin):** `crm-hygiene-audit`, `field-completion-monitoring`, `data-decay-tracking` share overlapping trigger vocabulary around "CRM data problems." A triage primer or decision tree in each `Use When` block would reduce misfires. No single entry point skill exists to route these.

**Cluster C — Post-Churn Analysis (renewals plugin):** `churn-analysis` and `churn-rca` are functionally near-duplicate for the most common use case (we lost an account, understand why). The contraction/cancellation boundary is meaningful but not user-visible at trigger time. Requires either consolidation or a prominent disambiguation criterion in both trigger blocks.

---

## Airtight Triggers (no significant issues)

The following skills have tight, well-differentiated trigger blocks that do not require remediation:

- `csm/stakeholder-map` — narrow scope, unique trigger vocabulary
- `csm/escalation-memo` — correctly deferred behind risk-flag
- `renewals/contract-review` — clear commercial-constraints framing with good exclusions
- `renewals/renewal-forecast` — portfolio-level with clear exclusion of per-account work
- `renewals/executive-summary` — strategic account scope gates activation effectively
- `rev-ops/comp-simulation` — narrow trigger, G3 governance label pre-empts misuse
- `rev-ops/deal-desk-workflow-management` — routes/approves distinction is clean
- `rev-ops/duplicate-detection` — unambiguous deduplication scope
- `rev-ops/non-standard-terms-detection` — specific enough to avoid collision
- `rev-ops/stage-integrity-audit` — distinct from pipeline-velocity-tracking with good exclusions
- `rev-ops/sales-cs-handoff-quality-scoring` — scoring framing avoids confusion with handoff-doc
- `onboarding/blocker-review` — operational scope is narrow and specific
- `onboarding/handoff-doc` — graduation framing anchors trigger precisely
- `csm/taro-play-runner` — play execution framing is distinct enough (except broken cross-reference in playbook-auditor)
- `rev-ops/csql-tracking` — inter-skill contract dependency is explicit and enforced

---

*Report generated by Agent T — Trigger Precision Red-Teamer, 2026-05-18*
