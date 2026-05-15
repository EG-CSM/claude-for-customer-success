---
name: cold-start-interview
description: >
  Cold-start setup — learns your CS motion, account portfolio, health model,
  escalation matrix, and tool integrations. Builds a CSM practice profile that
  every other skill in this plugin reads. Use on fresh install, when CLAUDE.md
  still has [PLACEHOLDER] markers, or when re-running with --redo or
  --check-integrations.
argument-hint: "[--redo | --check-integrations]"
version: "1.0.0"
config_skill: true
---

# /cold-start-interview

1. Check `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`. If `--check-integrations`, skip the interview — re-run only the Part 0 `What's connected?` probe and rewrite the `## Available integrations` table at that config path. When probing: only report ✓ if an MCP tool call actually succeeded. Configured-but-untested connectors are marked ⚪ with a one-line how-to for confirming. Never report ✓ based on `.mcp.json` declarations alone.
2. Check the shared company profile at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`. If it exists, read it and skip company-level questions. If it doesn't exist, write it after the interview.
3. Run the interview below: Part 0 (role + integrations), then CS motion, portfolio, health model, escalation, and playbook.
4. Write `~/.claude/plugins/config/claude-for-customer-success/csm/CLAUDE.md`, creating parent directories as needed.

---

# Cold-Start Interview: Customer Success Manager


## Reasoning Protocol

Before generating output, work through these steps:

1. **Confirm skill activation** — does the request match this skill's intended use? If not, name the better skill.
2. **Identify required connectors** — which integrations are needed? Flag any that are unconfigured or returning stale data.
3. **Check escalation path** — is a named escalation owner configured for this output type? If not, flag before proceeding.
4. **Apply applicable guardrails** — No domain guardrails apply — this skill configures the environment rather than generating outputs.
5. **Assess output destination** — who will see this output? Apply confidentiality check if distributing beyond the CSM.
6. **Confirm mode selection** — is the requested mode (--brief, --deep, etc.) appropriate for the situation?


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
