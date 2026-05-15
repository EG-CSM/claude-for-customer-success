---
name: playbook-auditor
description: >
  Audit the CS playbook for coverage gaps, trigger specificity, outcome
  measurability, play adoption rates, and dead plays. Use quarterly or when
  churn patterns suggest the playbook is missing key scenarios. Produces an
  ops-level playbook assessment with specific gap and improvement recommendations.
  Distinct from /csm:taro-play-runner which executes individual plays; this skill
  evaluates whether the right plays exist and whether they are working.
argument-hint: "[--full | --coverage | --adoption | --dead-plays | --play <play-name>]"
version: "1.0.0"
---

# /cs-ops:playbook-auditor

Is the playbook complete, specific, and actually being used?

---

## Pre-flight

Read `~/.claude/plugins/config/claude-for-customer-success/cs-ops/CLAUDE.md`
and `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

If either is missing or contains `[PLACEHOLDER]` markers, stop and prompt for
`/cs-ops:cold-start-interview`.

Critical configuration to apply:
- Configured playbook list (plays by name, trigger condition, and owner)
- CS motion by segment — determines which plays are expected per segment
- Escalation matrix — confirms plays exist for each escalation scenario
- Standard TARO play library as baseline if no custom playbook is configured

---


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — G6 (playbook audit outputs are leads for CS Ops judgment — not prescriptions for immediate play retirement).
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?

## Mode

`--full`: Complete playbook audit — coverage, adoption, trigger quality,
outcome measurability, and dead plays. **Default.**

`--coverage`: Coverage gap analysis only — which CS scenarios lack a
configured play. Fastest mode; useful when playbook is new.

`--adoption`: Play adoption and activation rate analysis — how often are
plays triggered, which CSMs are using them, which plays are underused.
Requires CS platform data with CTA/play activation history.

`--dead-plays`: Dead play identification — plays in the configured library
that have never been triggered or have not been triggered in the last
[configured period]. Surfacing these avoids playbook bloat.

`--play <play-name>`: Single-play deep audit — trigger specificity,
outcome definition, step completeness, and recent activation history for
one named play.

---

## Data gathering

Pull from connected integrations:
- CS Platform: configured plays, CTA templates, play activation history per account
- CRM: account list with segment, health tier, lifecycle stage
- CS-Ops config: configured playbook, escalation matrix scenarios

If nothing is connected:
> "To audit the playbook, I need: (1) a list of your configured plays with
> their trigger conditions and outcomes, and (2) ideally, activation history
> (how many times each play was triggered in the last [period]).
> Paste your playbook list or describe the plays and I'll run the coverage
> and quality analysis."

Minimum required before proceeding: configured play list with trigger conditions.
Adoption analysis requires activation history data.

---

## Standard scenario coverage baseline

The audit checks the configured playbook against this baseline scenario set.
These are the situations a complete CS playbook should address. Flag any
scenario with no matching play as a **coverage gap**.

**Churn prevention:**
- [ ] Low product usage / adoption decline
- [ ] Executive sponsor departure or disengagement
- [ ] Competitor evaluation underway
- [ ] Open escalation / unresolved P1 ticket
- [ ] NPS detractor with no recovery conversation
- [ ] No CSM contact in >[configured threshold] days
- [ ] Renewal at risk (<90 days, Red health)
- [ ] Budget cut / procurement hold signal

**Expansion:**
- [ ] Power user expansion signal (seat count, feature adoption spike)
- [ ] New use case / department adoption identified
- [ ] Account growth (revenue event — new product line, acquisition)
- [ ] QBR expansion discussion readiness

**Lifecycle management:**
- [ ] New account kickoff / onboarding initiation
- [ ] Onboarding stall or milestone miss
- [ ] First-value milestone achievement
- [ ] Quarterly health check (non-QBR accounts)
- [ ] QBR preparation and delivery
- [ ] Renewal preparation (>90 days out)

**Relationship management:**
- [ ] Executive sponsor introduction / welcome
- [ ] Champion promotion to executive sponsor
- [ ] Contact departure — non-executive
- [ ] Sentiment recovery after escalation closure

---

## Full playbook audit (`--full`)

---

**Playbook Audit Report**
*[Date] · [N] plays configured · INTERNAL — CS-Ops use only*

---

### Playbook inventory

| Play | Trigger condition | Owner | Motion scope | Last updated | Active in period? |
|------|-----------------|-------|-------------|-------------|-----------------|
| [Play 1] | [Trigger] | [CSM / Platform / CS Lead] | [All / HT / TT] | [date] | [Yes / No / Unknown] |
| [Play 2] | | | | | |

**Total configured plays:** [N]
**Plays without documented trigger condition:** [N] — `[review]`
**Plays without documented outcome:** [N] — `[review]`

---

### Coverage gap analysis (`--coverage` content)

---

**Scenario Coverage Assessment — [Date]**

| Scenario | Category | Coverage | Play name | Gap severity |
|----------|---------|---------|----------|-------------|
| Low usage / adoption decline | Churn prevention | ✅ Covered | [Play name] | — |
| Executive sponsor departure | Churn prevention | ⚠️ Gap | — | **High** |
| Competitor evaluation underway | Churn prevention | ✅ Covered | | — |
| [Continue for all baseline scenarios] | | | | |

**Coverage summary:**

| Category | Scenarios in baseline | Covered | Gaps | Coverage % |
|---------|----------------------|---------|------|-----------|
| Churn prevention | 8 | [N] | [N] | [%] |
| Expansion | 4 | [N] | [N] | [%] |
| Lifecycle management | 8 | [N] | [N] | [%] |
| Relationship management | 4 | [N] | [N] | [%] |
| **Total** | 24 | [N] | [N] | **[%]** |

**Gap detail:**

For each uncovered scenario:
> **Gap: [Scenario name]**
> This scenario has no configured play. Given the current portfolio —
> [N] accounts in [relevant segment/tier] — this gap affects an estimated
> [N] accounts that may encounter this scenario in the next 90 days.
> **Recommended play type:** [TARO-structured play or describe play approach]
> **Priority:** [High / Medium / Low — based on ARR concentration and frequency] `[review]`

---

### Trigger specificity audit

A play trigger should be specific enough that two CSMs reading it independently
would activate the play at the same moment for the same account.

| Play | Trigger as configured | Specificity assessment | Issue |
|------|--------------------|----------------------|-------|
| [Play 1] | "[Exact trigger text]" | ✅ Specific | — |
| [Play 2] | "[Vague trigger text]" | ⚠️ Vague | "Usage drop" — no threshold defined |
| [Play 3] | "[Trigger text]" | ❌ Unmeasurable | Cannot confirm without manual CSM judgment |

**Trigger specificity rating:**

| Rating | Count | % of plays |
|--------|-------|-----------|
| ✅ Specific — threshold and condition defined | [N] | [%] |
| ⚠️ Vague — condition named but threshold missing | [N] | [%] |
| ❌ Unmeasurable — subjective or undefined | [N] | [%] |

**Vague trigger detail:**

For each vague or unmeasurable trigger:
> **[Play name] — Trigger:** "[current trigger text]"
> **Issue:** [What is undefined — threshold, time window, signal source]
> **Recommended rewrite:** "[Specific, measurable trigger]"
> Example: "Usage drop" → "Product usage drops >30% week-over-week for 2
> consecutive weeks per [usage source]"

---

### Outcome measurability audit

A play outcome should define a state that is observable at play close —
not a vague intent.

| Play | Outcome as configured | Measurability | Issue |
|------|--------------------|--------------|-------|
| [Play 1] | "[Outcome text]" | ✅ Observable | — |
| [Play 2] | "[Outcome text]" | ⚠️ Vague | "Improve relationship" — no observable state |
| [Play 3] | "[Outcome text]" | ❌ Undefined | No outcome documented |

**Plays without an observable outcome:** [N] — these cannot be evaluated for
effectiveness because there is no definition of "done." `[review]`

**Recommended outcome format:**
"[Observable state] achieved by [date or milestone], confirmed by [evidence]."

Example: "Account health moves from Red to Yellow within 30 days of play close,
confirmed by health score update in [CS platform]."

---

### Play adoption analysis (`--adoption` content)

Requires CS platform activation history.

---

**Play Adoption Report — [Date] — [Period: last N months]**

| Play | Times triggered | Accounts active | Unique CSMs | Avg days to close | Outcome achieved % |
|------|----------------|----------------|------------|------------------|--------------------|
| [Play 1] | [N] | [N] | [N] | [N] | [%] |
| [Play 2] | | | | | |

**Adoption flags:**

| Flag | Count | Detail |
|------|-------|--------|
| High-coverage scenarios with low trigger rate (<[threshold]) | [N] | [list plays] |
| Plays triggered but never closed | [N] | [list plays] |
| CSMs with 0 play activations in period | [N] | [names or count] |
| Plays with outcome achievement <[configured threshold]% | [N] | [list plays] |

**Adoption interpretation:**

[2-3 sentences on the most significant adoption finding. Example: "The
executive-sponsor-departure play has been triggered [N] times but closed
with documented outcome in only [%] of activations — suggesting the close
criteria are not being applied consistently or the outcome is too vague to
confirm. Recommend trigger and outcome review before next QBR cycle."] `[review]`

**CSM adoption distribution:**

| Adoption band | CSMs | % of team |
|--------------|------|----------|
| Heavy users (>[N] plays triggered in period) | [N] | [%] |
| Moderate users ([range] plays) | [N] | [%] |
| Light users (<[N] plays) | [N] | [%] |
| No activations in period | [N] | [%] |

If any CSMs have 0 activations:
> "[N] CSMs triggered no plays in the last [period]. This may indicate:
> (1) tech-touch accounts with no play-eligible scenarios, (2) CSMs not
> using the platform to log play activation, or (3) CSMs managing plays
> outside the system. Recommend reviewing with CS lead before
> drawing conclusions." `[review]`

---

### Dead play identification (`--dead-plays` content)

---

**Dead Play Report — [Date]**
*Plays not triggered in the last [configured period]*

| Play | Last triggered | Times triggered (all time) | Scenario covered | Recommendation |
|------|--------------|--------------------------|-----------------|---------------|
| [Play 1] | [date or Never] | [N] | [Scenario] | [Archive / Update trigger / Retrain] |

**Dead play assessment:**

For each dead play, one of three diagnoses applies:

- **Scenario no longer relevant:** Archive the play. Update the playbook
  index and notify CSMs. Example: "A play for a product feature that was
  deprecated last year."

- **Trigger too narrow:** The scenario exists but the play trigger is so
  specific that it is rarely met. Recommend broadening. Example: "Play
  triggers on 'three consecutive NPS scores below 5' — most detractors
  are caught earlier and the play never fires."

- **Awareness gap:** Play exists and trigger is reasonable, but CSMs are
  not activating it. Recommend retraining. Example: "Competitor evaluation
  play — CSMs are not surfacing competitive signals to activate it."

---

### Single-play deep audit (`--play <play-name>`)

---

**Single Play Audit — [Play name]**
*[Date]*

**Play definition:**

| Field | Value | Quality |
|-------|-------|---------|
| Name | [Play name] | — |
| Trigger condition | [Text] | [✅ Specific / ⚠️ Vague / ❌ Unmeasurable] |
| Trigger source | [Automated / CSM judgment / Health score] | — |
| Owner | [Role or CSM name] | — |
| Steps (count) | [N] | — |
| Documented outcome | [Text] | [✅ Observable / ⚠️ Vague / ❌ Undefined] |
| Motion scope | [All / High-touch / Tech-touch] | — |
| Last updated | [date] | — |
| TARO structure | [Yes — T/A/R/O defined / Partial / No] | — |

**Play step review:**

| Step | Action | Owner | Timing | Completeness |
|------|--------|-------|--------|-------------|
| 1 | [Step text] | [Role] | [Day N / Week N] | [✅ Complete / ⚠️ Vague action] |
| 2 | | | | |

**Missing step types** (check against TARO structure):
- **Trigger (T):** [Present / Missing — play does not define what activates it]
- **Action (A):** [Present / Partial — actions defined but timing missing]
- **Response (R):** [Present / Missing — no customer response anticipated or documented]
- **Outcome (O):** [Present / Missing — no close criteria defined]

**Activation history:**

| Period | Activations | Accounts | Avg days to close | Outcome achieved |
|--------|------------|---------|------------------|-----------------|
| Last 30 days | [N] | [names or count] | [N] | [N] ([%]) |
| Last 90 days | [N] | | | |
| Last 12 months | [N] | | | |

**Single-play recommendation:**

[1-3 specific changes to improve trigger specificity, outcome measurability,
or adoption. If no changes are needed, say so explicitly.]

---

### Playbook health summary

| Dimension | Score | Detail |
|-----------|-------|--------|
| Coverage | [N/24 scenarios covered] ([%]) | [N] gaps — [High / Medium / Low] severity |
| Trigger specificity | [%] specific | [N] vague, [N] unmeasurable |
| Outcome measurability | [%] observable | [N] vague, [N] undefined |
| Adoption (if data available) | [%] of CSMs active | [N] zero-activation CSMs |
| Dead plays | [N] | [Diagnoses: archive [N] / retrain [N] / retrigger [N]] |

**Top 3 recommendations:**

**Priority 1 — [Recommendation headline]:**
[Specific action, why it matters, what improvement to expect. Reference data
from the audit. Example: "Add an executive-sponsor-departure play — this
scenario affects an estimated [N] accounts per year in the Enterprise segment
and there is no configured response. Without a play, response depends on
individual CSM awareness."]

**Priority 2 — [Recommendation headline]:**
[...]

**Priority 3 — [Recommendation headline]:**
[...]

---

## Reviewer note

> **⚠️ Reviewer note**
> - **Sources:** [CS Platform ✓ live | CRM ✓ live | user-provided playbook list — [date] | configured playbook in cs-ops CLAUDE.md | conversation context only]
> - **Playbook baseline applied:** [Custom configured playbook | Standard TARO library | No formal playbook — gap analysis against baseline scenarios only]
> - **Adoption data:** [CS Platform ✓ live — [N] months of history | Not available — adoption analysis skipped]
> - **Coverage baseline:** 24 scenarios across 4 categories — enterprise and SMB scenarios may require different coverage expectations
> - **Data as of:** [timestamp per source]
> - **Flagged for your judgment:** [N items marked `[review]` inline | none]
> - **Before archiving plays:** Confirm with CS lead — dead plays may represent scenarios that haven't occurred recently rather than plays that are no longer needed.

---

## Output

Playbook audit report — format driven by `--standard` (default) or `--full` flag.
Produces a structured markdown report with: scenario coverage matrix, play
effectiveness ratings, gap inventory, and prioritised improvement recommendations.
See **Full playbook audit** section for field-level detail.

## Guardrails

**Coverage gaps are directional, not prescriptive.** The baseline scenario list
represents typical CS situations — some gaps may be intentional (e.g., a
tech-touch segment may not need an executive-sponsor-departure play). Flag gaps
and note the rationale for exclusion; do not recommend plays that don't fit the
configured CS motion.

**Trigger vagueness is a systemic risk.** A vague trigger means different CSMs
will activate the play at different moments — or not at all. Inconsistent
activation means the play cannot be measured for effectiveness. Prioritize
trigger specificity improvements over coverage additions.

**Adoption analysis requires context.** A CSM with zero play activations may
manage a segment where plays are not the primary engagement mechanism. Surface
the data; do not declare the CSM non-compliant without investigation.

**TARO structure is the standard.** When assessing play step completeness,
apply the TARO framework: Trigger → Action → Response → Outcome. A play
without an Outcome definition cannot be closed — it will accumulate in the
system as perpetually open. Flag missing Outcome definitions as high priority.

**Dead plays may represent infrequent scenarios.** A play that has never been
triggered may cover a scenario (e.g., acquisition of a customer by a larger
company) that simply has not occurred in the configured period. Check scenario
frequency before recommending archival.

**No plays should be archived without CS lead sign-off.** Archiving a play
removes it from the library and from CSM visibility. If the scenario reoccurs,
there will be no structured response available. Document the rationale and
get explicit sign-off.

---

## After the audit

- "Coverage gaps confirmed — build the missing plays: `/csm:taro-play-runner --build`"
- "Adoption data shows CSM variance — check capacity context: `/cs-ops:capacity-planner`"
- "Trigger vagueness identified — update playbook config: `/cs-ops:customize --section playbook`"
- "Dead plays confirmed for archival — document the decision: `/cs-ops:process-doc --playbook-governance`"
- "Health distribution patterns suggest new play needed — check the model: `/cs-ops:health-model-review`"
