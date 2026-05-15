#!/usr/bin/env python3
"""
check-config-completeness.py — CS Suite installed plugin config completeness checker.

Reads installed plugin CLAUDE.md config files from:
  ~/.claude/plugins/config/claude-for-customer-success/<plugin>/CLAUDE.md

Reports:
  - PLACEHOLDER fields: lines or values containing literal "PLACEHOLDER" text
  - Blocked/disabled skills: skills declared as blocked, disabled, or commented-out
    in the CLAUDE.md config

This script targets INSTALLED configs, not source-repo CLAUDE.md files.
Run after plugin installation to verify configuration is complete.

Usage:
  python3 scripts/check-config-completeness.py
  python3 scripts/check-config-completeness.py --plugin csm
  python3 scripts/check-config-completeness.py --all
  python3 scripts/check-config-completeness.py --plugin renewals --verbose
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PLUGINS: list[str] = ["csm", "renewals", "onboarding", "cs-ops"]

CONFIG_BASE = Path.home() / ".claude" / "plugins" / "config" / "claude-for-customer-success"

# Patterns that indicate a PLACEHOLDER value
PLACEHOLDER_RE = re.compile(r"PLACEHOLDER", re.IGNORECASE)

# Patterns that indicate a skill is blocked or disabled in config
# Matches lines like:
#   blocked_skills: [skill-name]
#   disabled_skills: [skill-name]
#   # skill-name (commented-out skill in a list)
#   blocked: true  (on a skill entry)
BLOCKED_SKILLS_KEY_RE = re.compile(
    r"^\s*(blocked_skills|disabled_skills|blocked|disabled)\s*:", re.IGNORECASE
)
# A skill name in a YAML list item that is commented out
COMMENTED_SKILL_RE = re.compile(r"^\s*#\s*-\s+([a-z][a-z0-9\-]+)\s*$")
# A block/disabled key set to a non-empty, non-false value
BLOCKED_VALUE_RE = re.compile(r"^\s*(blocked|disabled)\s*:\s*(true|yes|1)\s*$", re.IGNORECASE)

# ---------------------------------------------------------------------------
# ANSI colours
# ---------------------------------------------------------------------------

COLORS = {
    "RED":    "\033[1;31m",
    "YELLOW": "\033[1;33m",
    "CYAN":   "\033[0;36m",
    "GREEN":  "\033[0;32m",
    "BOLD":   "\033[1m",
    "DIM":    "\033[2m",
    "RESET":  "\033[0m",
}


def _c(color: str, text: str) -> str:
    """Wrap text in ANSI colour if stdout is a TTY."""
    if not sys.stdout.isatty():
        return text
    return f"{COLORS[color]}{text}{COLORS['RESET']}"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class PlaceholderFinding:
    line_number: int
    line_text: str
    key: str  # The config key on that line, or "" if continuation


@dataclass
class BlockedSkillFinding:
    line_number: int
    line_text: str
    skill_name: str
    reason: str  # "blocked_skills key", "disabled_skills key", "commented-out", "blocked: true"


@dataclass
class ConfigReport:
    plugin: str
    config_path: Path
    exists: bool
    placeholders: list[PlaceholderFinding] = field(default_factory=list)
    blocked_skills: list[BlockedSkillFinding] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return self.exists and len(self.placeholders) == 0

    @property
    def has_blocked_skills(self) -> bool:
        return len(self.blocked_skills) > 0

    @property
    def issue_count(self) -> int:
        return len(self.placeholders) + len(self.blocked_skills)


# ---------------------------------------------------------------------------
# Config file resolution
# ---------------------------------------------------------------------------

def _config_path(plugin: str) -> Path:
    """Return the installed config path for a given plugin."""
    return CONFIG_BASE / plugin / "CLAUDE.md"


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _extract_key(line: str) -> str:
    """Extract the YAML key from a line like '  my_key: value'."""
    m = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_\-]*)\s*:", line)
    return m.group(1) if m else ""


def _find_placeholders(lines: list[str]) -> list[PlaceholderFinding]:
    """Find all lines containing PLACEHOLDER text."""
    findings: list[PlaceholderFinding] = []
    for i, line in enumerate(lines, start=1):
        if PLACEHOLDER_RE.search(line):
            key = _extract_key(line)
            findings.append(PlaceholderFinding(
                line_number=i,
                line_text=line.rstrip(),
                key=key,
            ))
    return findings


def _find_blocked_skills(lines: list[str]) -> list[BlockedSkillFinding]:
    """
    Find skills that are explicitly blocked, disabled, or commented out.

    Handles patterns:
      1. blocked_skills: [skill-a, skill-b]
      2. disabled_skills:
           - skill-a
           - skill-b
      3. # - skill-name   (commented-out list item, likely inside a skills list)
      4. blocked: true / disabled: true  (inline on a skill entry)
    """
    findings: list[BlockedSkillFinding] = []
    in_block_list = False  # True when we're inside a blocked/disabled_skills list
    block_list_key = ""

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip()

        # Pattern 3: commented-out skill list item
        m = COMMENTED_SKILL_RE.match(line)
        if m:
            findings.append(BlockedSkillFinding(
                line_number=i,
                line_text=line,
                skill_name=m.group(1),
                reason="commented-out in skills list",
            ))
            continue

        # Pattern 4: blocked: true / disabled: true
        if BLOCKED_VALUE_RE.match(line):
            # Try to extract context from the surrounding line
            key = _extract_key(line)
            findings.append(BlockedSkillFinding(
                line_number=i,
                line_text=line,
                skill_name="(inline on containing entry)",
                reason=f"{key}: true",
            ))
            continue

        # Pattern 1/2: blocked_skills: or disabled_skills: key
        if BLOCKED_SKILLS_KEY_RE.match(line):
            block_list_key = _extract_key(line)
            in_block_list = True

            # Inline list: blocked_skills: [skill-a, skill-b]
            inline_m = re.search(r"\[([^\]]+)\]", line)
            if inline_m:
                in_block_list = False
                skill_names = [s.strip().strip("\"'") for s in inline_m.group(1).split(",")]
                for skill_name in skill_names:
                    if skill_name:
                        findings.append(BlockedSkillFinding(
                            line_number=i,
                            line_text=line,
                            skill_name=skill_name,
                            reason=f"{block_list_key} (inline list)",
                        ))
            continue

        # If we're inside a block list, collect list items
        if in_block_list:
            item_m = re.match(r"^\s+-\s+(['\"]?)([a-z][a-z0-9\-]+)\1\s*$", line)
            if item_m:
                findings.append(BlockedSkillFinding(
                    line_number=i,
                    line_text=line,
                    skill_name=item_m.group(2),
                    reason=f"{block_list_key}",
                ))
                continue
            # Non-list line ends the block list (unless blank)
            if line.strip():
                in_block_list = False

    return findings


def _analyze_config(plugin: str) -> ConfigReport:
    """Load and analyze the installed config for a plugin."""
    path = _config_path(plugin)
    report = ConfigReport(plugin=plugin, config_path=path, exists=path.exists())

    if not report.exists:
        return report

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    report.placeholders = _find_placeholders(lines)
    report.blocked_skills = _find_blocked_skills(lines)
    return report


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _print_report(report: ConfigReport, verbose: bool) -> None:
    """Print the report for a single plugin."""
    plugin_label = _c("BOLD", f"[{report.plugin}]")

    if not report.exists:
        print(f"{plugin_label}  {_c('YELLOW', 'NOT INSTALLED')}  {_c('DIM', str(report.config_path))}")
        return

    status_parts: list[str] = []

    if not report.placeholders and not report.blocked_skills:
        status_parts.append(_c("GREEN", "✓ complete"))
    else:
        if report.placeholders:
            n = len(report.placeholders)
            status_parts.append(_c("RED", f"{n} placeholder{'s' if n != 1 else ''}"))
        if report.blocked_skills:
            n = len(report.blocked_skills)
            status_parts.append(_c("YELLOW", f"{n} blocked skill{'s' if n != 1 else ''}"))

    status_str = "  ".join(status_parts)
    print(f"{plugin_label}  {status_str}")

    if verbose:
        print(f"  {_c('DIM', str(report.config_path))}")

    # Print placeholder details
    if report.placeholders:
        print(f"  {_c('RED', 'PLACEHOLDER fields:')}")
        for p in report.placeholders:
            key_part = f"  [{p.key}]" if p.key else ""
            print(f"    line {p.line_number:4d}{key_part}  {_c('DIM', p.line_text[:100])}")

    # Print blocked skill details
    if report.blocked_skills:
        print(f"  {_c('YELLOW', 'Blocked/disabled skills:')}")
        for b in report.blocked_skills:
            print(
                f"    line {b.line_number:4d}  "
                f"{_c('BOLD', b.skill_name):30s}  "
                f"({b.reason})"
            )

    if (report.placeholders or report.blocked_skills) and verbose:
        print()


def _print_summary(reports: list[ConfigReport]) -> None:
    """Print a one-line summary across all checked plugins."""
    installed = [r for r in reports if r.exists]
    missing = [r for r in reports if not r.exists]
    incomplete = [r for r in installed if not r.is_complete]
    with_blocked = [r for r in installed if r.has_blocked_skills]

    total_placeholders = sum(len(r.placeholders) for r in installed)
    total_blocked = sum(len(r.blocked_skills) for r in installed)

    print()
    print(_c("BOLD", "Summary"))
    print(f"  Plugins checked   : {len(reports)}")
    print(f"  Installed         : {len(installed)}")

    if missing:
        print(f"  Not installed     : {_c('YELLOW', str(len(missing)))} ({', '.join(r.plugin for r in missing)})")
    else:
        print(f"  Not installed     : 0")

    if total_placeholders:
        print(f"  Placeholder fields: {_c('RED', str(total_placeholders))} across {len(incomplete)} plugin(s)")
    else:
        print(f"  Placeholder fields: {_c('GREEN', '0')}")

    if total_blocked:
        print(f"  Blocked skills    : {_c('YELLOW', str(total_blocked))} across {len(with_blocked)} plugin(s)")
    else:
        print(f"  Blocked skills    : {_c('GREEN', '0')}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check CS Suite installed plugin configs for PLACEHOLDER fields "
            "and blocked/disabled skills.\n\n"
            "Reads: ~/.claude/plugins/config/claude-for-customer-success/<plugin>/CLAUDE.md"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    target = parser.add_mutually_exclusive_group()
    target.add_argument(
        "--plugin",
        metavar="PLUGIN",
        choices=PLUGINS,
        help=f"Check a single plugin. One of: {', '.join(PLUGINS)}",
    )
    target.add_argument(
        "--all",
        action="store_true",
        default=False,
        help="Explicitly check all plugins (default behaviour when no flag given).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Show config file path and blank lines between plugins.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    plugins_to_check = [args.plugin] if args.plugin else PLUGINS

    reports: list[ConfigReport] = []
    for plugin in plugins_to_check:
        report = _analyze_config(plugin)
        reports.append(report)
        _print_report(report, verbose=args.verbose)

    if len(reports) > 1:
        _print_summary(reports)

    # Exit 1 if any installed config has PLACEHOLDER fields (incomplete config)
    # Exit 0 if all installed configs are complete (blocked skills are informational)
    has_placeholders = any(r.placeholders for r in reports if r.exists)
    return 1 if has_placeholders else 0


if __name__ == "__main__":
    sys.exit(main())
