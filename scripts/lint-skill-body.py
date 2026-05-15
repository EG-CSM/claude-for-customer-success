#!/usr/bin/env python3
"""
lint-skill-body.py — CS Suite SKILL.md body content linter.

Complements validate-plugin-frontmatter.py (packaging frontmatter only).
This script checks body content and structure for production readiness.

Checks:
  B01 WARN  — version present in frontmatter
  B02 BLOCK — ## Reasoning Protocol section present in body
  B03 BLOCK — Pre-flight section present (## Pre-flight or ## Preflight)
  B04 WARN  — Reviewer note present (line matching ⚠️ or > ⚠️)
  B05 WARN  — Guardrails section present (## Guardrails)
  B06 WARN  — Mode block declared for skills with mode flags (-- in arg hint)
  B07 NOTE  — At least one [review label present in skills with commercial output
  B08 WARN  — Output format section present
  B09 NOTE  — Cross-skill references use /plugin:skill-name format (not bare prose)
  B10 BLOCK — security: block absent from frontmatter (plugin-loader rejects it)

Severity:
  BLOCK — must fix before packaging; exit code 1 if any BLOCK found
  WARN  — should fix; exit code 0 (warning only)
  NOTE  — informational; exit code 0

Usage:
  python3 scripts/lint-skill-body.py claude-for-customer-success/
  python3 scripts/lint-skill-body.py claude-for-customer-success/renewals/skills/renewal-forecast/SKILL.md
  python3 scripts/lint-skill-body.py --plugin csm
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"BLOCK": 0, "WARN": 1, "NOTE": 2}

SEVERITY_COLORS = {
    "BLOCK": "\033[1;31m",  # bold red
    "WARN": "\033[1;33m",   # bold yellow
    "NOTE": "\033[0;36m",   # cyan
    "RESET": "\033[0m",
}


@dataclass
class Finding:
    check_id: str
    severity: str  # BLOCK | WARN | NOTE
    message: str
    line: int | None = None


@dataclass
class SkillReport:
    path: Path
    findings: list[Finding] = field(default_factory=list)

    @property
    def has_blocks(self) -> bool:
        return any(f.severity == "BLOCK" for f in self.findings)

    @property
    def has_warns(self) -> bool:
        return any(f.severity == "WARN" for f in self.findings)

    @property
    def worst_severity(self) -> str | None:
        if not self.findings:
            return None
        return min(self.findings, key=lambda f: SEVERITY_ORDER[f.severity]).severity

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: SEVERITY_ORDER[f.severity])


# ---------------------------------------------------------------------------
# YAML frontmatter parsing (minimal — no dependency on PyYAML)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """
    Extract YAML frontmatter block (between --- delimiters) and return
    (flat_key_value_dict, body_text). Values are raw strings, not parsed.
    Returns ({}, text) if no frontmatter.
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text

    fm_lines: list[str] = []
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
        fm_lines.append(line)

    if end_idx is None:
        return {}, text

    body = "".join(lines[end_idx + 1 :])
    fm: dict[str, str] = {}
    current_key: str | None = None
    for line in fm_lines:
        stripped = line.rstrip()
        # top-level key: value
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_\-]*):\s*(.*)", stripped)
        if m and not stripped.startswith(" "):
            current_key = m.group(1)
            fm[current_key] = m.group(2).strip()
        elif stripped.startswith("  ") and current_key:
            # multi-line continuation — append raw
            fm[current_key] = (fm.get(current_key, "") + " " + stripped.strip()).strip()

    return fm, body


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def _check_b01(fm: dict, body: str, raw: str) -> list[Finding]:
    """B01 WARN — version present in frontmatter."""
    if "version" not in fm or not fm["version"]:
        return [Finding("B01", "WARN", "No `version` field in frontmatter")]
    return []


def _check_b02(fm: dict, body: str, raw: str) -> list[Finding]:
    """B02 BLOCK — ## Reasoning Protocol section present."""
    if not re.search(r"^##\s+Reasoning Protocol", body, re.MULTILINE | re.IGNORECASE):
        return [Finding("B02", "BLOCK", "Missing `## Reasoning Protocol` section")]
    return []


def _check_b03(fm: dict, body: str, raw: str) -> list[Finding]:
    """B03 BLOCK — Pre-flight section present.

    Suppressed for config skills (config_skill: true) — these skills intentionally
    have no Pre-flight section because they run a guided setup interview rather than
    consuming a pre-configured practice profile.
    """
    if fm.get("config_skill"):
        return []  # config skills intentionally omit ## Pre-flight
    if not re.search(r"^##\s+Pre-?flight", body, re.MULTILINE | re.IGNORECASE):
        return [Finding("B03", "BLOCK", "Missing `## Pre-flight` (or `## Preflight`) section")]
    return []


def _check_b04(fm: dict, body: str, raw: str) -> list[Finding]:
    """B04 WARN — reviewer note present (⚠️ or > ⚠️).

    Suppressed for config skills (config_skill: true) — setup interview skills
    do not produce reviewable output that requires ⚠️ callouts.
    """
    if fm.get("config_skill"):
        return []  # config skills intentionally omit ⚠️ reviewer callouts
    if "⚠️" not in body:
        return [Finding("B04", "WARN", "No reviewer note found (expected line containing `⚠️`)")]
    return []


def _check_b05(fm: dict, body: str, raw: str) -> list[Finding]:
    """B05 WARN — ## Guardrails section present.

    Suppressed for config skills (config_skill: true) — setup interview skills
    configure the environment rather than generating reviewable outputs, so
    domain guardrails are documented in the Reasoning Protocol instead.
    """
    if fm.get("config_skill"):
        return []  # config skills document guardrail intent in Reasoning Protocol
    if not re.search(r"^##\s+Guardrails", body, re.MULTILINE | re.IGNORECASE):
        return [Finding("B05", "WARN", "Missing `## Guardrails` section")]
    return []


def _check_b06(fm: dict, body: str, raw: str) -> list[Finding]:
    """B06 WARN — mode block declared for skills with mode flags (-- in argument-hint).

    Suppressed for config skills (config_skill: true) — setup interview skills
    use -- flags for flow control (--redo, --check-integrations) rather than
    output-mode selection; a formal mode table is not appropriate.
    """
    if fm.get("config_skill"):
        return []  # config skills use -- flags for flow control, not output modes
    # Heuristic: only fire if the argument-hint frontmatter field declares known
    # output-mode flags. Checking body prose is too broad — skills often mention
    # --brief/--deep as examples without actually offering those modes.
    # Input routing flags (--situation, --play, --account, --redo, --check-*) are
    # excluded because they don't imply an output mode block is needed.
    argument_hint = fm.get("argument-hint", "") or ""
    OUTPUT_MODE_FLAGS = r"--(brief|deep|full|detailed|summary|standard|verbose|short|long|export)"
    has_mode_flags = bool(re.search(OUTPUT_MODE_FLAGS, argument_hint, re.IGNORECASE))
    has_mode_block = bool(
        re.search(r"^##\s+Mode", body, re.MULTILINE | re.IGNORECASE)
        or re.search(r"^##\s+\w+\s+[Mm]ode", body, re.MULTILINE)  # "## Output mode", "## Output Mode"
        or re.search(r"\|\s*Mode\s*\|", body, re.IGNORECASE)
        or re.search(r"mode\s*:\s*(brief|detailed|full|summary|standard)", body, re.IGNORECASE)
    )
    if has_mode_flags and not has_mode_block:
        return [Finding("B06", "WARN", "Skill uses `--` mode flags but no mode block/table found")]
    return []


def _check_b07(fm: dict, body: str, raw: str) -> list[Finding]:
    """B07 NOTE — at least one [review label present in commercial output skills."""
    # Heuristic: commercial output = body references draft, email, or report generation
    commercial_indicators = [
        r"\bdraft\b", r"\bemail\b", r"\bproposal\b", r"\breport\b",
        r"\bslide\b", r"\bdeck\b", r"\bexecutive\b",
    ]
    is_commercial = any(
        re.search(pat, body, re.IGNORECASE) for pat in commercial_indicators
    )
    has_review_label = bool(re.search(r"\[review", body, re.IGNORECASE))
    if is_commercial and not has_review_label:
        return [Finding("B07", "NOTE", "Commercial output skill has no `[review` label")]
    return []


def _check_b08(fm: dict, body: str, raw: str) -> list[Finding]:
    """B08 WARN — output format section present.

    Suppressed for config skills (config_skill: true) — setup interview skills
    write directly to CLAUDE.md config files; they have no discrete output section.
    """
    if fm.get("config_skill"):
        return []  # config skills intentionally omit ## Output section
    if not re.search(
        r"^##\s+(Output|Output Format|Outputs)",
        body,
        re.MULTILINE | re.IGNORECASE,
    ):
        return [Finding("B08", "WARN", "Missing output format section (`## Output` or `## Output Format`)")]
    return []


def _check_b09(fm: dict, body: str, raw: str) -> list[Finding]:
    """B09 NOTE — cross-skill references use /plugin:skill-name format."""
    # Flag bare skill-name references that look like cross-plugin calls but lack /plugin: prefix
    # Look for patterns like: "renewal-forecast skill", "the account-health skill", etc.
    bare_refs = re.findall(
        r"\b([a-z][a-z0-9]+-[a-z][a-z0-9]+(?:-[a-z][a-z0-9]+)*)\s+skill\b",
        body,
        re.IGNORECASE,
    )
    # Exclude self-references and known non-skill patterns
    skill_name = fm.get("name", "").lower().replace(" ", "-")
    # Exclude known plugin/suite names used as adjectives (e.g. "any cs-ops skill" is
    # describing the plugin family, not invoking a bare skill).
    # Also exclude tokens that appear in the file only inside /plugin:skill-name paths.
    _KNOWN_PLUGIN_NAMES = {
        "cs-ops", "csm", "renewals", "onboarding",
        "claude-for-customer-success", "customer-success",
    }
    external = [
        r for r in bare_refs
        if r.lower() != skill_name and r.lower() not in _KNOWN_PLUGIN_NAMES
    ]
    if external:
        unique = sorted(set(r.lower() for r in external))
        return [Finding(
            "B09", "NOTE",
            f"Possible bare cross-skill reference(s): {', '.join(unique)} — use `/plugin:skill-name` format",
        )]
    return []


def _check_b10(fm: dict, body: str, raw: str) -> list[Finding]:
    """B10 BLOCK — security: block absent from frontmatter (plugin-loader rejects it).

    NON-SUPPRESSIBLE: This check cannot be suppressed by config_skill or any other
    frontmatter flag. A `security:` block in frontmatter causes the plugin-loader to
    reject the entire plugin at install time, regardless of skill type. All skills —
    including config skills — must omit this from frontmatter.
    """
    # Check raw text — the security: key at top-level frontmatter indentation
    lines = raw.splitlines()
    in_fm = False
    found_security = False
    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break  # end of frontmatter
        if in_fm and re.match(r"^security\s*:", line):
            found_security = True
            break
    if found_security:
        return [Finding(
            "B10", "BLOCK",
            "`security:` block present in frontmatter — plugin-loader rejects this; "
            "move security contract to body sections `## Security & Permissions` + `## Trust & Verification`",
        )]
    return []


# ---------------------------------------------------------------------------
# Check registry
# ---------------------------------------------------------------------------

CHECKS = [
    _check_b01,
    _check_b02,
    _check_b03,
    _check_b04,
    _check_b05,
    _check_b06,
    _check_b07,
    _check_b08,
    _check_b09,
    _check_b10,
]


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def _find_skill_files(path: Path) -> Generator[Path, None, None]:
    """Yield all SKILL.md files under path (or path itself if it is one)."""
    if path.is_file():
        if path.name == "SKILL.md":
            yield path
        return
    yield from path.rglob("SKILL.md")


# ---------------------------------------------------------------------------
# Linting a single file
# ---------------------------------------------------------------------------

def lint_file(skill_path: Path) -> SkillReport:
    report = SkillReport(path=skill_path)
    try:
        raw = skill_path.read_text(encoding="utf-8")
    except OSError as e:
        report.findings.append(Finding("IO", "BLOCK", f"Cannot read file: {e}"))
        return report

    fm, body = _parse_frontmatter(raw)

    for check_fn in CHECKS:
        try:
            findings = check_fn(fm, body, raw)
            report.findings.extend(findings)
        except Exception as e:  # noqa: BLE001
            report.findings.append(
                Finding(check_fn.__name__, "WARN", f"Check raised exception: {e}")
            )

    return report


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

USE_COLOR = sys.stdout.isatty()


def _color(severity: str, text: str) -> str:
    if not USE_COLOR:
        return text
    c = SEVERITY_COLORS.get(severity, "")
    reset = SEVERITY_COLORS["RESET"]
    return f"{c}{text}{reset}"


def _print_report(reports: list[SkillReport], verbose: bool = False) -> None:
    total_blocks = 0
    total_warns = 0
    total_notes = 0
    files_with_issues = 0

    for report in reports:
        if not report.findings and not verbose:
            continue

        files_with_issues += 1
        findings = report.sorted_findings()

        print(f"\n{report.path}")
        for f in findings:
            tag = _color(f.severity, f"[{f.severity}]")
            loc = f" (line {f.line})" if f.line else ""
            print(f"  {tag} {f.check_id}{loc}: {f.message}")

        block_count = sum(1 for f in findings if f.severity == "BLOCK")
        warn_count = sum(1 for f in findings if f.severity == "WARN")
        note_count = sum(1 for f in findings if f.severity == "NOTE")

        total_blocks += block_count
        total_warns += warn_count
        total_notes += note_count

    total_files = len(reports)
    clean_files = total_files - files_with_issues

    print("\n" + "─" * 60)
    print(f"Scanned {total_files} SKILL.md file(s)")
    print(f"  Clean:    {clean_files}")
    print(f"  {_color('BLOCK', 'BLOCK')}:    {total_blocks}")
    print(f"  {_color('WARN', 'WARN')}:     {total_warns}")
    print(f"  {_color('NOTE', 'NOTE')}:     {total_notes}")

    if total_blocks > 0:
        print(
            f"\n{_color('BLOCK', 'FAIL')}: {total_blocks} BLOCK finding(s) must be resolved before packaging."
        )
    elif total_warns > 0:
        print(f"\n{_color('WARN', 'PASS (with warnings)')}: No BLOCK findings. {total_warns} WARN(s) should be reviewed.")
    else:
        print(f"\n{_color('NOTE', 'PASS')}: No BLOCK or WARN findings.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _resolve_paths(args: argparse.Namespace) -> list[Path]:
    """Resolve all target paths from args."""
    paths: list[Path] = []

    if args.plugin:
        # --plugin csm → look for claude-for-customer-success/csm/ relative to cwd
        # or relative to a common repo root heuristic
        candidates = [
            Path(f"claude-for-customer-success/{args.plugin}"),
            Path(args.plugin),
        ]
        for c in candidates:
            if c.exists():
                paths.append(c)
                break
        else:
            print(f"ERROR: Could not locate plugin directory for '{args.plugin}'", file=sys.stderr)
            sys.exit(2)
    elif args.targets:
        for t in args.targets:
            p = Path(t)
            if not p.exists():
                print(f"ERROR: Path does not exist: {t}", file=sys.stderr)
                sys.exit(2)
            paths.append(p)
    else:
        # Default: look for claude-for-customer-success/ in cwd
        default = Path("claude-for-customer-success")
        if default.exists():
            paths.append(default)
        else:
            print("ERROR: No target specified and claude-for-customer-success/ not found in cwd.", file=sys.stderr)
            print("Usage: python3 scripts/lint-skill-body.py <path> [...]", file=sys.stderr)
            sys.exit(2)

    return paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint SKILL.md body content for CS suite production readiness.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "targets",
        nargs="*",
        metavar="PATH",
        help="SKILL.md file(s) or directory/directories to scan",
    )
    parser.add_argument(
        "--plugin",
        metavar="PLUGIN",
        help="Scan a specific plugin by name (csm|renewals|onboarding|cs-ops)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all files, including those with no findings",
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Exit 1 on WARN findings in addition to BLOCK",
    )

    args = parser.parse_args()
    paths = _resolve_paths(args)

    # Collect all SKILL.md files
    skill_files: list[Path] = []
    for p in paths:
        skill_files.extend(_find_skill_files(p))

    if not skill_files:
        print("No SKILL.md files found.", file=sys.stderr)
        sys.exit(2)

    # Sort for deterministic output
    skill_files.sort()

    # Lint each file
    reports = [lint_file(sf) for sf in skill_files]

    # Print results
    _print_report(reports, verbose=args.verbose)

    # Exit code
    has_blocks = any(r.has_blocks for r in reports)
    has_warns = any(r.has_warns for r in reports)

    if has_blocks:
        sys.exit(1)
    if args.fail_on_warn and has_warns:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
