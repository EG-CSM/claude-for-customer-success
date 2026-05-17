"""
hooks/auq_hook.py
AUQ Resilience System — Claude Code hook handler.

Implements the three-tier AUQ fallback protocol for ask_user_input_v0:
  T1 — Tool call (mechanical, this file handles it)
  T2 — Prose multiple-choice block injected via PostToolUse block decision
  T3 — Proceed on last-option default (embedded in T2 prose)

Event handlers:
  PreToolUse        — enforce single-question-per-call; write state for PostToolUse;
                       skip T1 when force_prose mode is active
  PostToolUse       — detect T1 failure; inject T2 prose fallback if needed
  UserPromptSubmit  — intercept /auq slash commands; update mode flag
  Notification      — forward FLAG-level notifications as desktop alerts

Claude Code hook I/O contract:
  stdin  → JSON event dict
  stdout → JSON response dict
  exit 0 → always (fail-open; never block Claude on a hook crash)

PreToolUse stdout format (hookSpecificOutput):
  {
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "allow" | "block",
      "permissionDecisionReason": "string"
    }
  }

PostToolUse stdout format (block decision):
  { "decision": "block", "reason": "<T2 prose + instruction>" }
  or null/empty for pass-through.

UserPromptSubmit stdout format:
  {} for passthrough (Claude Code ignores the response body)

State bridge:
  _STATE_FILE   — written by PreToolUse; read by PostToolUse
  _PENDING_FILE — excess questions queued by PreToolUse; read by _pop_pending()
  _MODE_FILE    — written by UserPromptSubmit; read by PreToolUse
                   {"mode": "force_prose"} or {} (cleared)

Usage (invoked by Claude Code automatically per settings.json):
  python hooks/auq_hook.py < event.json > response.json
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from typing import Any

# ── Module-level constants (monkeypatched in tests) ────────────────────────────

_TMPDIR = tempfile.gettempdir()
_STATE_FILE = os.path.join(_TMPDIR, "auq_hook_state.json")
_PENDING_FILE = os.path.join(_TMPDIR, "auq_hook_pending.json")
_MODE_FILE = os.path.join(_TMPDIR, "auq_hook_mode.json")

_AUQ_TOOL = "ask_user_input_v0"

# Null-like values that indicate a failed / empty render response
_NULL_VALUES = frozenset({"", "none", "null", "undefined", "{}"})

# Keys Claude Code / ask_user_input_v0 may use for the user's selection
_RESPONSE_KEYS = ("value", "response", "text", "selected", "answer")

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logger = logging.getLogger("auq_hook")


# ── Data types ─────────────────────────────────────────────────────────────────

@dataclass
class SavedState:
    """State persisted from PreToolUse to PostToolUse via a temp file."""
    last_question_text: str
    last_options: list[str]
    last_default: str


# ── State file helpers ─────────────────────────────────────────────────────────

def _save_state(state: SavedState) -> None:
    try:
        with open(_STATE_FILE, "w") as f:
            json.dump({
                "last_question_text": state.last_question_text,
                "last_options": state.last_options,
                "last_default": state.last_default,
            }, f)
    except OSError as e:
        logger.warning("auq_hook: failed to write state file: %s", e)


def _load_state() -> SavedState | None:
    try:
        with open(_STATE_FILE) as f:
            data = json.load(f)
        return SavedState(
            last_question_text=data.get("last_question_text", ""),
            last_options=data.get("last_options", []),
            last_default=data.get("last_default", ""),
        )
    except (OSError, json.JSONDecodeError, KeyError):
        return None


# ── Pending queue helpers ──────────────────────────────────────────────────────

def _append_pending(questions: list[dict]) -> None:
    """Append excess questions to the pending queue file."""
    if not questions:
        return
    existing: list[dict] = []
    try:
        with open(_PENDING_FILE) as f:
            existing = json.load(f)
        if not isinstance(existing, list):
            existing = []
    except (OSError, json.JSONDecodeError):
        existing = []
    existing.extend(questions)
    try:
        with open(_PENDING_FILE, "w") as f:
            json.dump(existing, f)
    except OSError as e:
        logger.warning("auq_hook: failed to write pending file: %s", e)


def _pop_pending() -> dict | None:
    """Remove and return the first pending question, or None if queue is empty."""
    try:
        with open(_PENDING_FILE) as f:
            queue: list[dict] = json.load(f)
        if not isinstance(queue, list) or not queue:
            return None
        item = queue.pop(0)
        with open(_PENDING_FILE, "w") as f:
            json.dump(queue, f)
        return item
    except (OSError, json.JSONDecodeError):
        return None


# ── Mode file helpers ──────────────────────────────────────────────────────────

def _save_mode(mode: str) -> None:
    """Persist the active AUQ mode (e.g. 'force_prose') to disk."""
    try:
        with open(_MODE_FILE, "w") as f:
            json.dump({"mode": mode}, f)
    except OSError as e:
        logger.warning("auq_hook: failed to write mode file: %s", e)


def _load_mode() -> str:
    """Return the current AUQ mode string, or '' if none is set."""
    try:
        with open(_MODE_FILE) as f:
            data = json.load(f)
        return data.get("mode", "")
    except (OSError, json.JSONDecodeError):
        return ""


def _clear_mode() -> None:
    """Remove the mode file, returning to default (Tier 1) behaviour."""
    try:
        os.remove(_MODE_FILE)
    except OSError:
        pass  # Already absent — no-op


# ── UserPromptSubmit handler ───────────────────────────────────────────────────

# Recognised slash commands and the action each produces.
_AUQ_COMMANDS: dict[str, str] = {
    "/auq force-prose": "force_prose",
    "/auq reset":       "reset",
    "/auq status":      "status",
}


def user_prompt_submit(prompt: str) -> dict[str, Any]:
    """Handle UserPromptSubmit events.

    Detects /auq slash commands in the incoming prompt text and updates the
    mode file accordingly.  Returns a result dict with:
      - "handled":      bool — True when a /auq command was found
      - "command":      str  — matched command name (or "")
      - "inject_output": str — text Claude Code should prepend to the response
                               (used for /auq status; empty otherwise)

    Non-/auq prompts are returned with handled=False and no side effects.
    """
    stripped = prompt.strip()
    matched_cmd = ""
    for cmd in _AUQ_COMMANDS:
        if stripped.lower().startswith(cmd):
            matched_cmd = cmd
            break

    if not matched_cmd:
        return {"handled": False, "command": "", "inject_output": ""}

    action = _AUQ_COMMANDS[matched_cmd]

    if action == "force_prose":
        _save_mode("force_prose")
        return {
            "handled": True,
            "command": matched_cmd,
            "inject_output": (
                "[AUQ] Mode set to **force-prose** — "
                "Tier 1 (ask_user_input_v0) will be skipped for all questions "
                "this session. Use `/auq reset` to return to normal operation."
            ),
        }

    if action == "reset":
        _clear_mode()
        # Also drain the pending queue so stale questions don't linger
        try:
            with open(_PENDING_FILE, "w") as f:
                json.dump([], f)
        except OSError:
            pass
        return {
            "handled": True,
            "command": matched_cmd,
            "inject_output": (
                "[AUQ] Reset — returning to Tier 1 (ask_user_input_v0). "
                "Pending question queue cleared."
            ),
        }

    if action == "status":
        mode = _load_mode()
        mode_label = f"**force-prose** (Tier 2 always)" if mode == "force_prose" else "**normal** (Tier 1 → T2 → T3)"
        # Count pending questions
        pending_count = 0
        try:
            with open(_PENDING_FILE) as f:
                q = json.load(f)
            if isinstance(q, list):
                pending_count = len(q)
        except (OSError, json.JSONDecodeError):
            pass
        return {
            "handled": True,
            "command": matched_cmd,
            "inject_output": (
                f"[AUQ Status]\n"
                f"- Mode: {mode_label}\n"
                f"- Pending queued questions: {pending_count}"
            ),
        }

    return {"handled": False, "command": "", "inject_output": ""}


# ── PreToolUse handler ─────────────────────────────────────────────────────────

def pre_tool_use(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """Handle PreToolUse events.

    Non-AUQ tools: pass through unchanged.
    AUQ tool:
      - If force_prose mode is active: block the tool call immediately and
        inject T2 prose so Claude emits it without the tool running at all.
      - If single question: persist state, allow.
      - If multiple questions: trim to first, persist excess to pending queue,
        persist state for first question, allow with trimmed input.

    Returns a dict in the *internal* format:
      {"action": "allow" | "block", "tool_input": {...}}

    This internal format is consumed by main() which translates it to the
    correct Claude Code hookSpecificOutput schema for stdout.
    """
    if tool_name != _AUQ_TOOL:
        return {"action": "allow", "tool_input": tool_input}

    # ── force_prose mode: skip T1 entirely ────────────────────────────────────
    if _load_mode() == "force_prose":
        questions_raw: list[dict] = list(tool_input.get("questions", []))
        if questions_raw:
            first_q = questions_raw[0]
            excess = questions_raw[1:]
            if excess:
                _append_pending(excess)
            options: list[str] = first_q.get("options", [])
            default = options[-1] if options else ""
            prose = _build_prose_fallback(first_q.get("question", ""), options, default)
            instruction = (
                "Do NOT call ask_user_input_v0 — force-prose mode is active. "
                "Read the options above and respond with a letter (A, B, C, D) "
                "or describe your preference in plain text."
            )
            return {
                "action": "block",
                "reason": f"{prose}\n\n{instruction}",
            }
        return {"action": "allow", "tool_input": tool_input}

    questions: list[dict] = list(tool_input.get("questions", []))

    if not questions:
        return {"action": "allow", "tool_input": tool_input}

    # Trim to one question; queue excess
    first_question = questions[0]
    excess = questions[1:]
    if excess:
        _append_pending(excess)

    # Persist state so PostToolUse can build T2 fallback
    options: list[str] = first_question.get("options", [])
    default = options[-1] if options else ""
    _save_state(SavedState(
        last_question_text=first_question.get("question", ""),
        last_options=options,
        last_default=default,
    ))

    # Return trimmed tool_input (do NOT mutate original)
    new_input = dict(tool_input)
    new_input["questions"] = [first_question]
    return {"action": "allow", "tool_input": new_input}


# ── PostToolUse handler ────────────────────────────────────────────────────────

def post_tool_use(
    tool_name: str,
    tool_input: dict[str, Any],
    tool_result: dict[str, Any],
) -> dict[str, Any]:
    """Handle PostToolUse events.

    Non-AUQ tools: pass result through unchanged.
    AUQ tool:
      - Extract response value from tool_result.
      - Detect T1 failure conditions.
      - On failure: inject auq_fallback dict into tool_result (internal format).
      - On success: return tool_result unchanged.

    Returns a dict in the *internal* format for unit tests.
    main() translates fallback-present results into the Claude Code
    {"decision": "block", "reason": ...} format for stdout.
    """
    if tool_name != _AUQ_TOOL:
        return tool_result

    raw_value = _extract_response_value(tool_result)
    failure_reason = _detect_t1_failure(raw_value, tool_result)

    if failure_reason is None:
        return tool_result

    # T2 fallback — build prose and inject
    state = _load_state()
    if state:
        question_text = state.last_question_text
        options = state.last_options
        default = state.last_default
    else:
        question_text = "Please confirm your choice"
        options = []
        default = ""

    prose = _build_prose_fallback(question_text, options, default)
    instruction = (
        "Do NOT call ask_user_input_v0 again. "
        "Read the options above and respond with a letter (A, B, C, D) "
        "or describe your preference in plain text."
    )

    result = dict(tool_result)
    result["auq_fallback"] = {
        "tier": "T2_PROSE",
        "prose_output": prose,
        "instruction": instruction,
        "failure_reason": failure_reason,
    }
    return result


# ── Notification hook ──────────────────────────────────────────────────────────

def notification_hook(notification: dict[str, Any]) -> dict[str, Any]:
    """Handle Notification events.

    FLAG-level notifications trigger a desktop alert (side effect).
    All notifications are returned unchanged regardless.
    """
    level = notification.get("level", "")
    if level == "FLAG":
        message = notification.get("message", "")
        options = notification.get("options", [])
        body_lines = [message]
        for i, opt in enumerate(options):
            letter = chr(ord("A") + i)
            body_lines.append(f"{letter}) {opt}")
        body = "\n".join(body_lines)
        _emit_desktop_notification(title="Claude for Customer Success needs input", body=body)
    return notification


# ── Helper functions ───────────────────────────────────────────────────────────

def _detect_t1_failure(value: str, tool_result: dict[str, Any]) -> str | None:
    """Identify the failure mode for an AUQ tool response.

    Args:
        value:       Extracted string value from tool_result.
        tool_result: The full tool result dict.

    Returns:
        A failure reason string if a failure is detected, or None on success.
        Failure reasons: "tool_error", "empty_response", "render_failure_echo"
    """
    # Explicit error key in tool_result
    if "error" in tool_result:
        return f"tool_error: {tool_result['error']}"

    # Null-like / empty value
    if value.strip().lower() in _NULL_VALUES:
        return "empty_response"

    # Render failure echo — the tool call itself was echoed back as the value
    # (e.g. the UI failed to render and returned the input JSON)
    if _AUQ_TOOL in value:
        return "render_failure_echo"

    return None


def _extract_response_value(tool_result: Any) -> str:
    """Extract the user's text response from a tool_result dict.

    Checks keys in priority order: value, response, text, selected, answer.
    None values are skipped. Falls back to empty string.
    """
    if not isinstance(tool_result, dict):
        return str(tool_result)

    for key in _RESPONSE_KEYS:
        val = tool_result.get(key)
        if val is not None:
            return str(val)
    return ""


def _build_prose_fallback(
    question_text: str,
    options: list[str],
    default: str,
) -> str:
    """Build the T2 prose multiple-choice block.

    Format:
        **<question_text>**

        **A)** Option 1
        **B)** Option 2 ← proceeding with this if no response
        ...

        *(Type A, B, C, or D — or describe your preference)*
    """
    lines: list[str] = [f"**{question_text}**", ""]
    for i, option in enumerate(options):
        letter = chr(ord("A") + i)
        marker = " ← proceeding with this if no response" if option == default else ""
        lines.append(f"**{letter})** {option}{marker}")
    lines.append("")
    lines.append("*(Type A, B, C, or D — or describe your preference)*")
    return "\n".join(lines)


def _emit_desktop_notification(title: str, body: str) -> None:
    """Emit a desktop notification as a side effect.

    Requires the `desktop-notifier` package. Falls back gracefully if
    unavailable (common in CI environments).
    """
    try:
        from desktop_notifier import DesktopNotifier, Notification  # type: ignore
        import asyncio
        notifier = DesktopNotifier(app_name="Claude for CS")
        notif = Notification(title=title, message=body)
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(notifier.send(notif))
            else:
                loop.run_until_complete(notifier.send(notif))
        except RuntimeError:
            asyncio.run(notifier.send(notif))
    except ImportError:
        # desktop-notifier not installed — log to stderr for CI visibility
        logger.info("auq_hook: desktop-notifier not available; skipping notification")
    except Exception as e:  # noqa: BLE001
        logger.warning("auq_hook: desktop notification failed: %s", e)


# ── Claude Code output serialisation ──────────────────────────────────────────

def _pre_tool_use_to_wire(internal: dict[str, Any]) -> dict[str, Any]:
    """Translate internal PreToolUse result to Claude Code hookSpecificOutput."""
    action = internal.get("action", "allow")
    if action == "block":
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "block",
                "permissionDecisionReason": internal.get("reason", ""),
            }
        }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "",
        }
    }


def _post_tool_use_to_wire(internal: dict[str, Any]) -> dict[str, Any]:
    """Translate internal PostToolUse result to Claude Code wire format.

    If auq_fallback is present → emit {"decision": "block", "reason": ...}
    which causes Claude Code to surface the prose to the model and stop.
    Otherwise → emit empty dict (pass-through; Claude Code ignores it).
    """
    fallback = internal.get("auq_fallback")
    if fallback:
        prose = fallback.get("prose_output", "")
        instruction = fallback.get("instruction", "")
        reason = f"{prose}\n\n{instruction}"
        return {"decision": "block", "reason": reason}
    return {}


def _user_prompt_submit_to_wire(internal: dict[str, Any]) -> dict[str, Any]:
    """Translate internal UserPromptSubmit result to Claude Code wire format.

    When a /auq command was handled, inject the status/confirmation text so
    Claude includes it in its response.  Claude Code treats the "output" key
    as text to prepend to the assistant turn when present.
    Unhandled (non-/auq) prompts return an empty dict — pass-through.
    """
    if internal.get("handled"):
        inject = internal.get("inject_output", "")
        if inject:
            return {"output": inject}
    return {}


# ── CLI entry point ────────────────────────────────────────────────────────────

def main() -> None:
    """Read a Claude Code hook event from stdin, dispatch, write response to stdout."""
    raw = sys.stdin.buffer.read()

    # Fail-open: malformed input must never block Claude
    try:
        event: dict[str, Any] = json.loads(raw)
        if not isinstance(event, dict):
            raise ValueError("Event is not a dict")
    except (json.JSONDecodeError, ValueError) as exc:
        _emit_allow_error(f"parse_error: {exc}")
        return

    hook_type = event.get("hook_type", "")
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    try:
        if hook_type == "PreToolUse":
            internal = pre_tool_use(tool_name, tool_input)
            wire = _pre_tool_use_to_wire(internal)
            _emit(wire)

        elif hook_type == "PostToolUse":
            tool_result = event.get("tool_result", {})
            internal = post_tool_use(tool_name, tool_input, tool_result)
            wire = _post_tool_use_to_wire(internal)
            _emit(wire)

        elif hook_type == "UserPromptSubmit":
            # prompt text is at event["prompt"] in the Claude Code contract
            prompt_text = event.get("prompt", "")
            internal = user_prompt_submit(prompt_text)
            wire = _user_prompt_submit_to_wire(internal)
            _emit(wire)

        elif hook_type == "Notification":
            notification = event.get("notification", event)
            result = notification_hook(notification)
            _emit(result)

        else:
            # Unknown event — allow
            _emit({"hookSpecificOutput": {"hookEventName": hook_type, "permissionDecision": "allow", "permissionDecisionReason": ""}})

    except Exception as exc:  # noqa: BLE001
        logger.error("auq_hook: unhandled exception in %s: %s", hook_type, exc)
        _emit_allow_error(f"handler_error: {exc}")


def _emit(data: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(data))
    sys.stdout.flush()


def _emit_allow_error(reason: str) -> None:
    """Emit a fail-open allow response with an error annotation."""
    _emit({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "",
        },
        "hook_error": reason,
        "action": "allow",  # legacy compat; ignored by Claude Code but useful in error tests
    })


if __name__ == "__main__":
    main()
