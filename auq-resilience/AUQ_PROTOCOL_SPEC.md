# AUQ Resilience Protocol — Specification

**Version:** 1.1.0  
**Status:** PROPOSED  
**Applies to:** All interactive skills across Claude Cowork and Claude Code

---

## Problem

`ask_user_input_v0` (AUQ) renders as a tappable button card in both Cowork and Claude
Code. When it works, it's the best interaction pattern available — structured, fast,
no typing required. When it doesn't work, Claude has no fallback and the session stalls.

Failure modes that occur in production:

| Failure | Cause | Effect |
|---|---|---|
| Silent non-render | Interface doesn't surface the card | Claude waits indefinitely |
| Empty response | User dismisses without selecting | Tool returns empty string |
| Tool error | `ask_user_input_v0` unavailable in context | Tool call errors |
| Render failure echo | Interface returns raw call syntax | Response value is JSON |

The AUQ Resilience Protocol guarantees that every question resolves — regardless of
which failure mode occurs, or whether no failure occurs at all.

---

## Protocol

Three tiers, each with a defined trigger and a defined output:

```
Tier 1: ask_user_input_v0
    ↓ on: tool error · empty response · null response · render failure echo
Tier 2: Prose multiple choice
    ↓ on: no reply in same session
Tier 3: Proceed on stated default
```

### Tier 1 — ask_user_input_v0

**Always announce before calling:**
```
[AUQ: asking about <specific topic>]
```

The topic names the actual decision — not a generic label:
```
✅ [AUQ: asking about deployment target]
✅ [AUQ: asking about renewal date window]
❌ [AUQ: asking a question]
```

**Call structure:**
```json
{
  "questions": [
    {
      "question": "<question text>",
      "type": "single_select",
      "options": ["<option A>", "<option B>", "<default — last>"]
    }
  ]
}
```

Constraints:
- Exactly **one question** per call — never batch
- **2–4 options** per question
- **Last option is the stated default**
- Use `rank_priorities` only when ranking order is the actual need

**Success condition:** Non-empty response that is not `"None"`, `"null"`, `"{}"`,
or raw tool call syntax (starts with `{` and contains `ask_user_input`).

**Failure → Tier 2:** Any of: tool error present, empty/null response, render echo.

### Tier 2 — Prose Multiple Choice

Output this block verbatim as the next response when Tier 1 fails:

```
**[Question text]**

**A)** [Option 1]
**B)** [Option 2]
**C)** [Option 3]
**D)** [Default option] ← proceeding with this if no response

*(Type A, B, C, or D — or describe your preference)*
```

Format rules — all required:
- Question text is bold
- Each option on its own line, bold letter label
- Default carries the `← proceeding with this if no response` marker
- Prompt line `*(Type A, B, C, or D...)*` always included

**Response parsing** — stop at first match:

| Step | Method | Example | Confidence |
|---|---|---|---|
| 1 | Letter match — leading A/B/C/D, case-insensitive | `"B"` → options[1] | 1.0 |
| 2 | Keyword match — option text substring, bidirectional | `"cancel it"` → "Cancel" | 0.85 |
| 3 | Token overlap — Jaccard ≥ 0.30 | `"deploy to prod"` → "Deploy to production" | variable |
| 4 | Default | no match | 0.0 |

**Failure → Tier 3:** No reply received after Tier 2 in the same session.

### Tier 3 — Proceed on Default

```
[Assumed: <default value> — correct me if wrong]
```

State the default, proceed with the work. Tier 3 is not an error condition — it is
expected behavior for long-running tasks where the user may be away or has implicitly
accepted the default.

---

## Core Invariants

These hold unconditionally — no exception, no override:

1. **One question per exchange.** If multiple clarifications are needed, ask the most
   blocking one first. Queue the rest and ask sequentially after each reply.

2. **Always announce before calling.** The `[AUQ: ...]` announcement precedes
   every `ask_user_input_v0` call in the same turn.

3. **Always state the default.** Every question — Tier 1 or Tier 2 — includes an
   explicit default. Never ask without one.

4. **Never hang silently.** Tier 1 failure → Tier 2 immediately. No retry of the
   tool call.

5. **Never call AUQ twice before a response.** Once Tier 2 prose has been output,
   wait for a reply before calling `ask_user_input_v0` again.

---

## Enforcement by Environment

The protocol is identical in both environments. Enforcement differs.

### Claude Code

**Mechanical enforcement** via hooks:

- `PreToolUse` hook fires before every `ask_user_input_v0` call: enforces
  one-question rule, queues excess, persists question state to temp file
- `PostToolUse` hook fires after: reads temp file, checks response, injects
  `auq_fallback` directive when Tier 1 failure detected
- Claude reads `auq_fallback.prose_output` and emits it verbatim
- `Notification` hook fires on FLAG-level questions: surfaces desktop notification
  via `desktop-notifier` v6.x

The fallback fires automatically. Claude doesn't need to evaluate failure conditions
— the hook does it and instructs Claude what to output.

**Why hooks need file-based state:** Claude Code spawns a new OS process per hook
event. A module-level variable set in `PreToolUse` doesn't survive to `PostToolUse`.
State persists to `/tmp/auq_hook_state.json`, overwritten per question.

### Claude Cowork

**Behavioral enforcement** via `CLAUDE.md` project instructions:

- No hook system is available in Cowork
- The `CLAUDE.md` ALWAYS rule mandates the protocol: check response value, fall
  through to Tier 2 on failure
- The `CLAUDE.md` NEVER rule prohibits silent hanging
- Cowork's "Ask before acting" mode creates natural pause points where AUQ fires

The fallback fires because the instructions say to. Same output as Claude Code;
different enforcement mechanism.

### Managed Agent Contexts

**No hook inheritance — behavioral enforcement only:**

When a managed agent is spawned via `callable_agents`, it runs in a child
process that does **not** inherit the parent session's hooks. This means:

- `PreToolUse` and `PostToolUse` AUQ hooks registered in the parent do not fire
  for tool calls made inside subagents
- Tier 1 mechanical enforcement (hook-injected fallback) is unavailable inside
  the subagent
- Tier 2 and Tier 3 must be enforced behaviorally via the subagent's own
  instructions

**Required:** Any subagent that may call `ask_user_input_v0` must include the
AUQ behavioral rules (ALWAYS/NEVER block) in its own system prompt or `CLAUDE.md`.
The parent session's `CLAUDE.md` rules do not propagate into subagent contexts.

---

## Question Queue

When multiple clarifications are needed, queue them:

1. Rank by blocking order — which question prevents progress if unanswered?
2. Ask the highest-ranked blocker via Tier 1/2
3. Store remaining questions in order
4. After each response, ask the next queued question using the full T1→T2→T3 protocol

**Claude Code:** Queue persists to `/tmp/auq_hook_pending.json`, survives across
tool calls within the session.

**Cowork:** Queue is session-scoped in-context only. Lost if the session ends.

---

## Slash Commands

| Command | Effect |
|---|---|
| `/auq force-prose` | Skip Tier 1; use Tier 2 prose for all questions this session. Use when the card is confirmed not rendering. |
| `/auq status` | Report current tier; list pending queued questions. |
| `/auq reset` | Clear pending queue; return to Tier 1. |

---

## Implementation Files

| File | Purpose | Environment |
|---|---|---|
| `hooks/auq_hook.py` | PreToolUse + PostToolUse + UserPromptSubmit + Notification handlers | Claude Code |
| `hooks/auq_parser.py` | Tier 2 response parser — letter/keyword/semantic/default | Both |
| `.claude/CLAUDE.md` | Session-level behavioral rules | Claude Code |
| `.claude/settings.json` | Hook registration | Claude Code |
| `CLAUDE.md` (per plugin) | Universal behavioral floor | Both |
