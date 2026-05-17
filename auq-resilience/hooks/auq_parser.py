"""
hooks/auq_parser.py
AUQ response parser — four-level parse chain.

Converts a free-text user response into a resolved option value from a
known options list.  Designed to run without any model call so it is safe
to use inside a Claude Code PreToolUse hook.

Parse levels (in order, first match wins):
  1. Letter   — leading A/B/C/D (case-insensitive), maps to option by index
  2. Keyword  — bidirectional substring: option text in response OR response
                in option text (case-insensitive); first matching option wins
  3. Semantic — Jaccard token overlap; highest-scoring option above 0.30
  4. Default  — no match; return the stated default value

Usage:
    from auq_parser import parse_response, resolve, ParseResult

    r = parse_response("B", ["Option A", "Option B", "Option C"], "Option C")
    # ParseResult(value="Option B", matched=True, method="letter", confidence=1.0)

    value = resolve("cancel please", options, default=options[-1])
    # "Cancel"
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence


# ── Data contract ──────────────────────────────────────────────────────────────

@dataclass
class ParseResult:
    """Outcome of a single parse_response call.

    Attributes:
        value:      The resolved option string (from options list) or default.
        matched:    True if any parse level succeeded; False for default fallback.
        method:     Which parse level produced the result: "letter" | "keyword"
                    | "semantic" | "default".
        confidence: Numeric confidence [0.0, 1.0].  Letter = 1.0, keyword = 0.85,
                    semantic = Jaccard score, default = 0.0.
    """
    value: str
    matched: bool
    method: str
    confidence: float


# ── Public API ─────────────────────────────────────────────────────────────────

def parse_response(
    response: str,
    options: Sequence[str],
    default: str,
) -> ParseResult:
    """Parse a free-text response against a list of options.

    Args:
        response: The raw user/model response string.
        options:  Ordered list of valid choice strings.
        default:  Value to return when no level matches.

    Returns:
        ParseResult with value, matched, method, and confidence.
    """
    stripped = response.strip()

    # Level 1 — letter match
    result = _match_letter(stripped, options)
    if result is not None:
        return result

    # Level 2 — keyword / substring match
    result = _match_keyword(stripped, options)
    if result is not None:
        return result

    # Level 3 — semantic / Jaccard token overlap
    result = _match_semantic(stripped, options)
    if result is not None:
        return result

    # Level 4 — default fallback
    return ParseResult(value=default, matched=False, method="default", confidence=0.0)


def resolve(
    response: str,
    options: Sequence[str],
    default: str | None = None,
) -> str:
    """Convenience wrapper: return just the resolved value string.

    If default is not supplied, the last option in *options* is used
    (matching the AUQ T3 protocol: "proceed on last-option default").

    Returns:
        The resolved option string, or *default* / last option on no match.
    """
    if not options:
        return default if default is not None else ""
    _default = default if default is not None else options[-1]
    return parse_response(response, options, _default).value


# ── Level 1: letter match ──────────────────────────────────────────────────────

# Accepts: A / B / C / D (case-insensitive) with optional punctuation suffix,
# optionally followed by whitespace and more text (ignored).
# Only A–D are supported (indices 0–3).  Letter must be in range for the
# given options list.
_LETTER_RE = re.compile(r"^([A-Da-d])[.):\s]?", re.IGNORECASE)
_LETTER_MAP = {ch: idx for idx, ch in enumerate("abcd")}


def _match_letter(response: str, options: Sequence[str]) -> ParseResult | None:
    m = _LETTER_RE.match(response)
    if not m:
        return None
    idx = _LETTER_MAP[m.group(1).lower()]
    if idx >= len(options):
        return None
    return ParseResult(
        value=options[idx],
        matched=True,
        method="letter",
        confidence=1.0,
    )


# ── Level 2: keyword / substring match ────────────────────────────────────────

def _match_keyword(response: str, options: Sequence[str]) -> ParseResult | None:
    """Bidirectional case-insensitive substring match.

    Checks:
      a) option text is a substring of response (lowercased)
      b) response is a substring of option text (lowercased)
    First matching option in list order wins.

    Empty response is rejected immediately — an empty string is technically a
    substring of every option, which would produce spurious matches.
    """
    if not response.strip():
        return None
    resp_lower = response.lower()
    for option in options:
        opt_lower = option.lower()
        if opt_lower in resp_lower or resp_lower in opt_lower:
            return ParseResult(
                value=option,
                matched=True,
                method="keyword",
                confidence=0.85,
            )
    return None


# ── Level 3: semantic / Jaccard token overlap ──────────────────────────────────

def _tokenize(text: str) -> set[str]:
    """Split on whitespace and punctuation; return lowercase token set."""
    return set(re.split(r"[\s\W]+", text.lower())) - {""}


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity: |intersection| / |union|.  Returns 0.0 for empty sets."""
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


_SEMANTIC_THRESHOLD = 0.30


def _match_semantic(response: str, options: Sequence[str]) -> ParseResult | None:
    """Highest-Jaccard option above threshold wins."""
    resp_tokens = _tokenize(response)
    if not resp_tokens:
        return None

    best_score = 0.0
    best_option: str | None = None

    for option in options:
        opt_tokens = _tokenize(option)
        score = _jaccard(resp_tokens, opt_tokens)
        if score > best_score:
            best_score = score
            best_option = option

    if best_score >= _SEMANTIC_THRESHOLD and best_option is not None:
        return ParseResult(
            value=best_option,
            matched=True,
            method="semantic",
            confidence=best_score,
        )
    return None
