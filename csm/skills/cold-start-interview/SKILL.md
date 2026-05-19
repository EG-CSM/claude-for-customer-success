---
name: cold-start-interview
description: >
  Cold-start setup — learns your CS motion, account portfolio, health model,
  escalation matrix, and tool integrations. Builds a CSM practice profile that
  every other skill in this plugin reads. Use on fresh install, when CLAUDE.md
  still has [PLACEHOLDER] markers, or when re-running with --redo or
  --check-integrations.
argument-hint: "[--redo | --check-integrations | --generate-outcome-catalog]"
version: "1.0.0"
deployment_target: plugin
config_skill: true
---

# /cold-start-interview

[PROPOSED]

## Use When
- Running the CSM plugin for the first time on a new installation
- The CSm practice has changed materially (new segments, motion change, new CS platform)
- Config files are missing or contain `[PLACEHOLDER]` markers that block other skills
- The user explicitly invokes `/csm:cold-start-interview` or `/csm:customize --full`

## Do NOT Use For
- Updating a single config section — use `/csm:customize --section <name>` instead
- Answering ad-hoc CS strategy questions — answer directly without running the interview
- Reconfiguring other plugins (cs-ops, renewals, onboarding) — each has its own customize skill

## Typical Activation
"Set up the CSM plugin for my company"
"Run the cold start interview"
"/csm:cold-start-interview"
"Configure the plugin from scratch"

---

1. Check `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`. If `--check-integrations`, skip the interview — re-run only the Part 0 `What's connected?` probe and rewrite the `## Available integrations` table at that config path. When probing: only report ✓ if an MCP tool call actually succeeded. Configured-but-untested connectors are marked ⚪ with a one-line how-to for confirming. Never report ✓ based on `.mcp.json` declarations alone.
2. Check the shared company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`. If it exists, read it and skip company-level questions. If it doesn't exist, write it after the interview.
3. Run the interview below: Part 0 (role + integrations), then CS motion, portfolio, health model, escalation, and playbook.
4. Write `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`, creating parent directories as needed.

---

# Cold-Start Interview: Customer Success Manager

## Pre-flight

Check for existing config files at:
- `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`
- `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`

For `--full` or no argument: proceed regardless of whether files exist — this skill creates or overwrites them.
For `--section <name>`: load existing config file content before displaying current values alongside each question.
For `--reset`: display a destructive-clear warning and require explicit confirmation before proceeding.

---

## Reasoning Protocol

Before generating output, apply these primers:

1. **CLASSIFY**: What type of cold-start setup is this?
   - **Type A — Fresh Install**: No config file exists. No prior profile. Full or quick interview needed.
   - **Type B — Resume from Pause**: Config exists with `<!-- SETUP PAUSED AT: -->` marker. Partial answers already written.
   - **Type C — Redo (Full or Section)**: Populated config exists. User invoked `--redo` or `--redo <section>`.
   - **Type D — Integration Check Only**: User invoked `--check-integrations`. No interview — probe connectors and rewrite the integrations table.
   - **Type E — Quick Path**: User chose the 2-minute setup. Only Part 0 + CS motion. Everything else gets motion-aware `[DEFAULT]` markers. Outcome catalog gets `[PENDING]` — surface the `--generate-outcome-catalog` flag in the Close section.
   - **Type F — Catalog Generation Only**: User invoked `--generate-outcome-catalog`. Skip the full interview. Read company-profile.md to retrieve product name and primary value metric, then run Part 6 only.

2. **CONSTRAINTS**: What limits the solution space?
   - Is the working directory project-scoped (limited filesystem access) or user-scoped?
   - Does a shared company profile already exist (skip company questions) or not (ask and write it)?
   - Which connectors are available — test with actual calls, not config declarations?
   - What interview path did the user choose — quick or full?

3. **EXPERT CHECK**: What would a veteran CSM verify first?
   - Are there existing artifacts (playbooks, escalation docs, CRM exports) that replace manual Q&A?
   - Does the CS motion answer (high-touch / tech-touch / hybrid / handoff) correctly drive all downstream defaults?
   - On resume or redo: are previously written answers still accurate before continuing?
   - On integration check: is the connector actually responding, or just configured?

4. **ANTI-PATTERNS**: Common mistakes to avoid:
   - ❌ Asking more than 2-3 answerable prompts per turn (count subparts as separate questions)
   - ❌ Reporting a connector as connected based on `.mcp.json` without an actual successful tool call
   - ❌ Writing generic defaults without `[DEFAULT]` markers, making them indistinguishable from user-provided values
   - ❌ Re-asking company-level questions when the shared company profile already exists
   - ❌ Overwriting a populated config section during a targeted `--redo <section>` without preserving adjacent sections

**After execution**, verify:
- Does the written config satisfy both the user's explicit answers AND motion-appropriate defaults for unanswered fields?
- Were all connector statuses verified by actual tool calls, not config inspection?
- Confidence: [High] if full interview completed with user-provided answers; [Medium] if quick path with motion-aware defaults; [Low] if resumed from stale pause with unconfirmed prior answers


## Purpose

Every CSM skill reads from the configuration this interview writes. A generic profile gives generic output — a default health model, a default escalation matrix, a default set of risk flags that may have nothing to do with how your team actually works. This interview builds a profile calibrated to your accounts, your motion, and your risk posture.

## Cold-start check

Read `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`:
- **Does not exist** → start the interview.
- **Contains `<!-- SETUP PAUSED AT: -->`** → greet the user and offer to resume from that section.
- **Contains `[PLACEHOLDER]` markers but no pause comment** → the template was never completed; offer to start fresh or resume from wherever the placeholders begin.
- **Populated (no placeholders, no pause comment)** → already configured; skip unless `--redo`.

The template structure lives at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` — use it as the section scaffold. Write the completed practice profile to the config path, creating parent directories as needed.

## Check for the shared company profile

Look for `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`.

- **If it exists:** Read it. Show a one-line confirmation: "You're at [company], [product description], in the [segment] segment. Right? (Or say 'update' to change the shared profile.)" If confirmed, skip company questions — go straight to CSM-specific ones.
- **If it doesn't exist:** This is the first plugin install. After the fork choice, ask the company questions (company name, product description, primary segment, CS team size, churn drivers) and write them to the shared profile. Tell the user: "I've saved your company profile — the other CS plugins will read it and skip these questions."

Company-level questions that live in the shared profile and should NOT be re-asked: company name, product description, primary segment, CS team size, top churn drivers. CSM-specific questions (health model config, account portfolio, escalation matrix, playbook sources) stay in the per-plugin config.

## Install scope check

Before the orientation, if the working directory is inside a project (not the user's home directory), flag it once:

> **Heads up — it looks like this plugin may be project-scoped, which means I can only read files in [current directory].** If you'll want me to pull documents from elsewhere (success plans, QBR decks, account notes in other folders), install user-scoped instead — see QUICKSTART.md. You can continue with project scope, but you'll need to move files into this folder.

Ask the user to confirm before proceeding. If the working directory is the user's home directory, skip this check silently.

## Before the interview starts

Open with the fork-first preamble:

> **`csm` is for CSMs managing a B2B SaaS book of business** — account research, call prep, QBRs, success plans, health reviews, risk flags, and renewal readiness. Not your role? `/claude-for-customer-success:related-plugins`.
>
> **2 minutes** gets you your role, CS motion, and tool connections — enough to run most skills with sensible defaults. **15 minutes** builds your full profile: account portfolio details, health model configuration, escalation matrix, and playbook sources — the things that turn generic output into output that reads like you wrote it.
>
> Quick or full?

**Quick path:** Ask only Part 0 and the CS motion section. Write the config with `[DEFAULT]` markers on everything else. Close with: "Done. You can start using the skills now. I've used sensible defaults for health thresholds, risk signals, and escalation routing. When a skill's output feels off, that's usually a default to tune — the output will tell you which one. Run `/csm:cold-start-interview --full` anytime to do the whole interview."

**Full path:** The existing interview flow below. After the user picks, give the orientation, then proceed.

## After the user picks quick or full

Give the orientation, in your own voice:

> "This plugin maintains your CSM practice profile: your CS motion, your account portfolio context, your health model, and your escalation chain. It reads from a plain-text config file every time a skill runs. Everything you answer can be changed later — either by editing the file directly or re-running this interview."

Then:

> "Setup builds a fresh professional profile from your answers. It doesn't read your Claude history, other conversations, or personal CLAUDE.md files. If I notice relevant context already in our conversation, I'll ask before using it."

Then: "Ready? A few quick questions first."

## Interview pacing

- **Assume the answer exists somewhere.** For anything that's probably written down — CS playbook, escalation matrix, health model config — prompt for a paste or link before asking the user to type it from memory. "Paste a doc, share a link, or give me the short version" is the default ask for any question that's more than a sentence.
- **Batch size.** Never ask more than 2-3 answerable prompts per turn. Count subparts. One question with 5 subparts is 5 questions.
- **Pause and resume.** Tell the user up front: "Say 'pause' anytime and I'll save progress. Run `/csm:cold-start-interview` again to pick up where you left off." When the user pauses, write a partial config with `<!-- SETUP PAUSED AT: [section] — run /csm:cold-start-interview to resume -->` at the top and `[PENDING]` markers (distinct from `[PLACEHOLDER]`) on unanswered fields.

---

## The interview

### Part 0: Who's using this, and what's connected

Three quick orientation questions before CS specifics. These shape how every skill frames its output.

#### Who's using this?

> Who'll be using this plugin day to day?
>
> 1. **CSM** — you own the full post-sales relationship: onboarding, adoption, QBRs, renewal conversations, expansion signals.
> 2. **CS team lead or manager** — you manage CSMs and use this for portfolio reviews, escalation decisions, and coaching.
> 3. **CS adjacent** — Solutions Engineer, Onboarding Specialist, or Renewals Manager who occasionally needs CSM-type output.

This calibrates output depth and escalation framing across every skill.

#### Your CS motion

> Which best describes your CS motion?
>
> 1. **High-touch** — small book, deep relationships, frequent async and sync contact
> 2. **Tech-touch or pooled** — large book, lower-ARR accounts, mostly programmatic outreach
> 3. **Hybrid / segmented** — high-touch for enterprise, tech-touch for SMB or mid-market
> 4. **Implementation + CSM handoff** — Implementation team owns onboarding; CSM takes accounts after go-live

This changes how skills frame engagement frequency, outreach templates, and QBR cadences.

#### What's connected?

> Let me check which connectors you have configured. Features that need them will work; features that don't will fall back gracefully instead of failing silently.

Check what's actually connected, not just what's configured. A connector in `.mcp.json` is available. One that's responding is connected. These are different.

For each connector this plugin uses:
- If testable: call a simple read (account list, search). Report ✓ only on a successful response.
- If not testable from here: report ⚪ "configured but not verified — open your MCP settings to confirm."
- Never report ✓ based on `.mcp.json` declarations alone.

For connectors not connected, tell the user how to connect. Example: "HubSpot isn't connected. In Claude Cowork: Settings → Connectors → Add → HubSpot → sign in. In Claude Code: add the HubSpot MCP to your config or via `/mcp`. Skills work without it — you'll paste account context instead of pulling it live."

Report findings:

> - ✓ [CRM] — connected (tested)
> - ⚪ [CS Platform] — configured but not verified. Open your MCP settings to confirm.
> - ✗ [Gong] — not found. Call transcript features fall back to pasted notes. [How to connect.] Re-run `/csm:cold-start-interview --check-integrations` after connecting.

Write `## Who's using this` and `## Available integrations` sections to the config immediately after Part 0.

---

### Part 1: Account portfolio (2-3 min)

> Before the questions — do you have a spreadsheet, CRM export, or territory doc that describes your book of business? Paste the contents, share a file path, or link it. If you share it, I'll extract the portfolio context directly.

If not:

- **How many accounts** are in your book? (Total and by segment if segmented.)
- **Total ARR managed.** Estimate is fine.
- **Segments you cover:** SMB / mid-market / enterprise / all.
- **Average account ARR** — or the range (low / high).
- **Highest-ARR account.** What's the top end of your book?

Then:

- **Renewal involvement:** Do you own renewals, or does a dedicated renewals team take them?
- **CSM tenure on accounts:** How long do accounts typically stay with you before transfer or churn?

If the user didn't share a CRM export, offer: "Want me to generate a blank account portfolio template you can fill in? It's structured so the skills can read it on future calls."

---

### Part 2: CS methodology (2-3 min)

> Which best describes your CS methodology?
>
> 1. **SuccessCOACHING / TARO framework** — your team uses SuccessCOACHING playbooks or TARO (Trigger, Action, Resource, Outcome) as the shared language
> 2. **Custom internal playbook** — you have a defined methodology but it's home-grown
> 3. **No formal framework** — you follow general CS best practices without a codified methodology

If SuccessCOACHING or TARO: I'll surface TARO framework terminology in recommendations, play references, and the `/csm:taro-play-runner` skill. Which playbook library are you drawing from?

If custom: paste or link your playbook, or describe the core plays in 2-3 sentences. I'll adapt terminology to yours.

Then:

> **Success criteria model:** When you kick off a new account, do you build account-specific success criteria, or do you use a standard template?

And:

> **Primary value metric:** What does "the customer got value" look like? Pick the answer that fits most of your accounts — specific metrics are better than general descriptions.

---

### Part 3: Health model (3-4 min)

> Do you have a CS Platform (Gainsight, Totango, ChurnZero, Vitally, Planhat) with a configured health model? Or do you track health manually?

If CS Platform:
- Which platform?
- What are the components and rough weights? (E.g., product usage 40%, support tickets 20%, NPS 20%, engagement 20%.)
- What's the Red threshold? Yellow?

If manual / no platform:
- What signals make you worried about an account? (These become the health signal definitions.)
- What would make you escalate a concern to your manager?

Then:

> **Churn signals — what's actually scared you before?**
>
> Before the list of questions: if you have a churn analysis or a churned-account retrospective, paste it. I'll extract the patterns instead of asking you to reconstruct them.

If not:
- Executive sponsor departed without replacement?
- Drop in product usage or logins?
- Open escalation or support ticket backlog?
- NPS detractor + no recovery conversation?
- Missed QBR or no-show pattern?
- Competitor evaluation underway?
- Anything else that's shown up in accounts you've lost?

---

### Part 4: Escalation matrix (2-3 min)

> If your team has a shared escalation matrix or escalation playbook, paste it or link it. I'll use it as the baseline.

If not, walk through the scenarios:

| Situation | Route to | How | SLA |
|---|---|---|---|
| Account goes Red | [manager / VP CS / CRO] | [Slack / Gainsight CTA / email] | [24h] |
| Executive sponsor departure | [AE / Head of CS] | [Slack] | [48h] |
| Churn risk > [threshold ARR] | [CS lead / CRO] | [weekly review + email] | [48h] |
| Expansion signal — qualified | [AE / AM] | [email + CRM opportunity] | [48h] |
| Customer escalation | [CS lead / VP CS] | [email + meeting] | [same day] |

Ask only the rows that the user hasn't already described. Tell the user: "I'll flag every risk recommendation in skills with the escalation routing from this matrix. If the matrix changes, re-run `/csm:cold-start-interview --redo escalation`."

---

### Part 5: Playbook sources (1-2 min)

> Where do you keep your CS playbooks and templates? (These are the sources the `/csm:taro-play-runner` skill and other skills pull from.)

| Source | Location | Notes |
|--------|----------|-------|
| CS playbook | [Notion / Drive / Confluence / Guru / local path] | |
| QBR template | [paste link or path] | |
| Success plan template | [paste link or path] | |
| Kickoff agenda template | [paste link or path] | |

If the user doesn't have formal playbook sources, say: "No problem — skills will use SuccessCOACHING default play structures and note that you haven't configured custom playbook sources. You can link them later by editing `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`."

---

### Part 6: Outcome catalog (optional — 5–10 min if generating)

> "The last optional piece is an Outcome & Value Catalog — a structured inventory of the customer outcomes your product delivers, mapped to evidence and value signals. Other skills use it to ground TARO play recommendations, QBR value sections, and renewal narratives in verifiable, specific outcomes rather than generic claims.
>
> I can generate one now by researching your product's public-facing capabilities (release notes, docs, case studies, G2/Capterra reviews, LinkedIn posts) and translating them into deliverable customer outcome statements. It takes 5–10 minutes and requires no input from you beyond what you've already told me.
>
> Or you can skip it now and run `/csm:cold-start-interview --generate-outcome-catalog` whenever you're ready."

**AskUserQuestion:** "Would you like me to generate your Outcome & Value Catalog now?"

Options:
- A) Yes — generate it now (5–10 min)
- B) Skip for now — I'll run `--generate-outcome-catalog` later

**If B or quick-path (Type E):**
Write `catalog_path: [PENDING]` to the `## Outcome Catalog` section of `company-profile.md`. Surface the flag: "Run `/csm:cold-start-interview --generate-outcome-catalog` when you're ready to build it."

**If A (or Type F — `--generate-outcome-catalog`):**

1. **Gather inputs from context.** Read `company-profile.md` to retrieve:
   - `product_name` (required)
   - `primary_value_metric` (used to prioritize outcome framing)
   - `cs_motion` (used to weight outcome types — adoption vs. expansion vs. retention)

   If any required field is `[PLACEHOLDER]` or missing, ask for it before continuing.

2. **Invoke `product-intelligence-gatherer`.**
   [Calling product-intelligence-gatherer: discovering product capabilities for {product_name} from public sources]

   Pass: product name, company name, primary value metric as framing context.

   This skill searches public sources (docs, release notes, G2/Capterra, case studies, LinkedIn) and returns a structured capability inventory organized by product area. It requires no user input beyond what's already collected.

3. **Invoke `provisional-outcome-catalog-generator`.**
   [Calling provisional-outcome-catalog-generator: translating capability inventory into deliverable customer outcome statements]

   Pass: the full capability inventory from step 2, plus the primary value metric and CS motion as framing. This skill produces a structured catalog of customer outcomes in SuccessCOACHING Outcome Catalog format, with evidence references and value signal mapping.

4. **Save the catalog.**
   Write the generated catalog to:
   `~/.claude/plugins/config/claude-for-customer-success/outcome-catalog.md`

   Create parent directories as needed.

5. **Register the path in company-profile.md.**
   In the `## Outcome Catalog` section of `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`, write:
   ```
   catalog_path: ~/.claude/plugins/config/claude-for-customer-success/outcome-catalog.md
   catalog_version: provisional-1.0
   ratified_date: [PENDING — not yet ratified with CS leadership]
   generation_status: generated
   ```

6. **Optional: Offer individual entry refinement.**
   After generation, say: "Your catalog has [N] outcome entries. I can refine individual entries using `outcome-catalog-entry-builder` — useful for high-priority outcomes where you want tighter evidence standards or custom metric definitions. Want to refine any entries now, or come back to this later?"

   If the user wants to refine entries, invoke `outcome-catalog-entry-builder` for each nominated entry. If they want to defer, move on.

7. **Confirm completion.**
   "Outcome catalog saved to `~/.claude/plugins/config/claude-for-customer-success/outcome-catalog.md` — [N] outcome entries across [M] product areas. Skills that reference outcome data will use this catalog. You can run `/csm:cold-start-interview --generate-outcome-catalog` to regenerate it after a major product release."

---

## Writing the practice profile

Write the completed practice profile to `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` using the template structure at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`. Fill all sections. Mark any deliberately skipped answers as `[SKIPPED — user may add later]` (not `[PLACEHOLDER]`).

If the shared company profile doesn't yet exist, write the company-level sections to `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`, creating parent directories as needed.

---

## After writing

Show the capability tour. Make it concrete — these are the actual things this plugin does best for this user's role and motion.

> **Here's what I can do now that your profile is set:**
>
> - **Research an account before a call** — pull CRM data, health signals, and call history into a one-page brief. Try: `/csm:account-research [account name]`
> - **Prep for any customer call** — agenda, attendee context, suggested talking points from your configured motion. Try: `/csm:call-prep [account name]`
> - **Build or review a QBR** — value delivered, metrics against success criteria, next-period plan. Try: `/csm:qbr-builder [account name]`
> - **Flag a risk account** — structured risk memo with the specific signals, escalation routing from your matrix, and recommended next action. Try: `/csm:risk-flag [account name]`
> - **Run a TARO play** — match an account trigger to your playbook, draft the outreach, route to you for approval. Try: `/csm:taro-play-runner [account name]`
> - **Renewal readiness check** — risk signals, expansion leads, and a renewal talk track at the 90/60/30-day mark. Try: `/csm:renewal-readiness [account name]`
> - **Outcome-grounded QBRs and renewals** — when an Outcome & Value Catalog is configured, value sections cite specific, verifiable customer outcomes rather than generic claims. If you skipped catalog generation: `/csm:cold-start-interview --generate-outcome-catalog`
>
> **My suggestion for your first one:** Run `/csm:account-research` on an account you know well — it's the fastest way to see how the profile calibration reads. Or tell me what's on your plate and I'll point you to the right skill.

---

> [review before sending]

## Close

> "Done. Your configuration is at `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md` — a plain text file you can read and edit directly. Anything you answered can be changed:
>
> - Edit the file directly for a quick change
> - Run `/csm:cold-start-interview --redo` for a full re-interview
> - Run `/csm:cold-start-interview --redo escalation` to re-do one section
> - Run `/csm:cold-start-interview --check-integrations` to re-check what's connected
> - Run `/csm:cold-start-interview --generate-outcome-catalog` to build or regenerate your Outcome & Value Catalog
>
> The settings people adjust most: **churn signal definitions** (as you learn what actually predicts risk at your company), **escalation thresholds** (as reporting lines shift), and **health model weights** (as you calibrate which signals matter). When a skill's output feels off, that's usually the thing to tune — it'll tell you which."

## Your practice profile learns

> **Your practice profile learns.** It gets better as you use the skills:
>
> - When a skill's output feels generic, that's usually a setting to tune. The output will name it.
> - You can say "update my churn signals to also include [X]" and the relevant skill will write the change.
> - Run `/csm:cold-start-interview --redo <section>` to re-interview one part, or edit the config file directly.
>
> Ten minutes of setup gets you a working profile. A month of use gets you one that reads like you wrote it yourself.

## Reference Files

The following reference files govern this skill's detailed behavior. They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response.

| File | Purpose |
|------|---------|
| `references/reasoning-blueprint.md` | Problem classification taxonomy, domain heuristics, common failure modes, and expert judgment patterns for this skill |

---

## Security & Permissions
- network_access: none
- filesystem_write: config files only (explicitly listed paths)
- subprocess_execution: false
- dynamic_code_execution: false

## Trust & Verification
- All config writes require explicit user confirmation before executing
- No values are invented — gaps use [PLACEHOLDER] markers
- Config files govern downstream skill behavior; treat writes as high-trust operations
