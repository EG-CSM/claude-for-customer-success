#!/usr/bin/env python3
"""
validate-cross-links.py
=======================
Cross-link validator for the claude-for-customer-success plugin suite.

Checks that every file reference inside the cookbook and plugin directories
resolves to a real path on disk. Exits non-zero when broken links are found.

Checks performed
----------------
1. agent.yaml  system.file           → orchestrator .md must exist
2. agent.yaml  callable_agents[].manifest → subagent .yaml must exist
3. agent.yaml  skills[].from_plugin  → plugin directory must exist
4. subagent .yaml  system.file       → subagent .md must exist
5. Markdown [text](path) links       → target file/dir must exist
6. Prose backtick-path references    → .md/.yaml/.json targets must exist

Usage
-----
    python3 scripts/validate-cross-links.py [--root PATH] [--verbose] [--strict]

    --root PATH   Root of the claude-for-customer-success tree.
                  Default: auto-detected relative to this script.
    --verbose     Also print PASS lines.
    --strict      Exit 1 even if only warnings are present.

Output
------
    PASS  <check-type>              <source>
          → <resolved-target>
    FAIL  <check-type>              <source>
          → <resolved-target>   (missing)

Exit codes: 0 = all pass, 1 = any FAIL (or WARN with --strict), 2 = config error.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

try:
    import yaml  # PyYAML
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    status: str          # "PASS" | "FAIL" | "WARN"
    check: str           # short check identifier
    source_file: Path    # file that contains the reference
    reference: str       # the raw reference string extracted
    resolved: Path       # the resolved absolute path being checked
    note: str = ""       # optional extra context


@dataclass
class ValidationResult:
    findings: list[Finding] = field(default_factory=list)

    def add(self, status: str, check: str, source: Path,
            reference: str, resolved: Path, note: str = "") -> None:
        self.findings.append(
            Finding(status, check, source, reference, resolved, note)
        )

    def passes(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "PASS"]

    def fails(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "FAIL"]

    def warns(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "WARN"]


# ---------------------------------------------------------------------------
# YAML helpers (graceful degradation when PyYAML absent)
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict | None:
    """Return parsed YAML dict or None on any error."""
    if not HAVE_YAML:
        return None
    try:
        with path.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception:
        return None


def _yaml_str(obj: object) -> str | None:
    """Return obj as str if it is one, else None."""
    return obj if isinstance(obj, str) else None


# ---------------------------------------------------------------------------
# Check 1 + 2 + 3: agent.yaml references
# ---------------------------------------------------------------------------

def check_agent_yaml(yaml_path: Path, result: ValidationResult) -> None:
    """Validate all cross-file references inside an agent.yaml."""
    data = _load_yaml(yaml_path)
    if data is None:
        result.add("WARN", "yaml-parse", yaml_path, str(yaml_path),
                   yaml_path, "Could not parse YAML — install PyYAML or check syntax")
        return

    base = yaml_path.parent

    # 1. system.file
    system_block = data.get("system") or {}
    system_file = _yaml_str(system_block.get("file") if isinstance(system_block, dict) else None)
    if system_file:
        target = (base / system_file).resolve()
        status = "PASS" if target.is_file() else "FAIL"
        result.add(status, "agent-system-file", yaml_path, system_file, target)

    # 2. callable_agents[].manifest
    for entry in data.get("callable_agents") or []:
        if not isinstance(entry, dict):
            continue
        manifest = _yaml_str(entry.get("manifest"))
        if manifest:
            target = (base / manifest).resolve()
            status = "PASS" if target.is_file() else "FAIL"
            result.add(status, "agent-callable-manifest", yaml_path, manifest, target)

    # 3. skills[].from_plugin
    for entry in data.get("skills") or []:
        if not isinstance(entry, dict):
            continue
        from_plugin = _yaml_str(entry.get("from_plugin"))
        if from_plugin:
            target = (base / from_plugin).resolve()
            status = "PASS" if target.is_dir() else "FAIL"
            result.add(status, "agent-from-plugin", yaml_path, from_plugin, target,
                       note="expected directory")


# ---------------------------------------------------------------------------
# Check 4: subagent .yaml references
# ---------------------------------------------------------------------------

def check_subagent_yaml(yaml_path: Path, result: ValidationResult) -> None:
    """Validate system.file inside a subagent yaml."""
    data = _load_yaml(yaml_path)
    if data is None:
        result.add("WARN", "yaml-parse", yaml_path, str(yaml_path),
                   yaml_path, "Could not parse YAML")
        return

    base = yaml_path.parent
    system_block = data.get("system") or {}
    system_file = _yaml_str(system_block.get("file") if isinstance(system_block, dict) else None)
    if system_file:
        target = (base / system_file).resolve()
        status = "PASS" if target.is_file() else "FAIL"
        result.add(status, "subagent-system-file", yaml_path, system_file, target)


# ---------------------------------------------------------------------------
# Check 5: Markdown [text](path) links
# ---------------------------------------------------------------------------

# Match [any text](./path) or [text](path) — skip http(s):// and anchors
_MD_LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)#]+)\)')


def check_markdown_links(md_path: Path, result: ValidationResult) -> None:
    """Validate all relative markdown links in a .md file."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        result.add("WARN", "md-read", md_path, str(md_path), md_path,
                   "Could not read file")
        return

    base = md_path.parent
    for m in _MD_LINK_RE.finditer(text):
        href = m.group(2).strip()
        # Skip absolute URLs and mailto
        if re.match(r'^(https?://|mailto:|#)', href):
            continue
        # Skip bare words with no path separators or file extensions — these
        # appear in documentation tables as placeholder text, e.g. `[text](url)`
        if '/' not in href and '.' not in href:
            continue
        target = (base / href).resolve()
        exists = target.exists()
        status = "PASS" if exists else "FAIL"
        result.add(status, "md-link", md_path, href, target)


# ---------------------------------------------------------------------------
# Check 6: Prose backtick-path references
# ---------------------------------------------------------------------------

# Match backtick-quoted strings that look like relative paths ending in a
# known extension: subagents/foo.md, ./bar.yaml, path/to/file.json, etc.
_BACKTICK_PATH_RE = re.compile(
    r'`((?:\.{1,2}/)?[\w./\-]+\.(?:md|yaml|yml|json|py|mjs|txt|sh))`'
)


def check_prose_paths(md_path: Path, result: ValidationResult, root: Path) -> None:
    """Validate backtick-quoted path references in a .md file."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return  # already warned in check_markdown_links if called together

    base = md_path.parent
    seen: set[str] = set()

    for m in _BACKTICK_PATH_RE.finditer(text):
        raw = m.group(1)
        # Deduplicate within a single file
        if raw in seen:
            continue
        seen.add(raw)

        # Require a directory separator — bare filenames like `SKILL.md` and
        # bare dotfiles like `.mcp.json` are too ambiguous to validate.
        if "/" not in raw:
            continue

        target = (base / raw).resolve()
        if target.exists():
            result.add("PASS", "prose-path", md_path, raw, target)
        else:
            # Prose paths in documentation are often written from the suite root
            # perspective (e.g. `csm/CLAUDE.md`) rather than relative to the
            # source file's directory. Try root-relative resolution as a fallback
            # and emit WARN rather than FAIL when that succeeds.
            root_target = (root / raw).resolve()
            if root_target.exists():
                result.add("WARN", "prose-path", md_path, raw, root_target,
                           note="resolved root-relative; verify intentional")
            else:
                result.add("FAIL", "prose-path", md_path, raw, target)


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def _is_agent_yaml(path: Path) -> bool:
    """True if this yaml is an orchestrator agent manifest."""
    return (
        path.name == "agent.yaml"
        and path.parent.parent.name == "managed-agent-cookbooks"
    )


def _is_subagent_yaml(path: Path) -> bool:
    """True if this yaml lives in a subagents/ subdirectory."""
    return path.suffix in (".yaml", ".yml") and path.parent.name == "subagents"


def iter_files(root: Path) -> Iterator[tuple[str, Path]]:
    """Yield (kind, path) for every file we want to validate."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        # Skip hidden dirs (.claude-plugin, .git, etc.)
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        if _is_agent_yaml(path):
            yield ("agent_yaml", path)
        elif _is_subagent_yaml(path):
            yield ("subagent_yaml", path)
        elif path.suffix == ".md":
            yield ("markdown", path)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def validate(root: Path) -> ValidationResult:
    result = ValidationResult()

    if not HAVE_YAML:
        print(
            "WARNING: PyYAML not installed — YAML checks disabled. "
            "Run:  pip install pyyaml",
            file=sys.stderr,
        )

    for kind, path in iter_files(root):
        if kind == "agent_yaml":
            check_agent_yaml(path, result)
        elif kind == "subagent_yaml":
            check_subagent_yaml(path, result)
        elif kind == "markdown":
            check_markdown_links(path, result)
            check_prose_paths(path, result, root)

    return result


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


USE_COLOR = sys.stdout.isatty()
_COLORS = {
    "PASS": "\033[0;32m",
    "FAIL": "\033[1;31m",
    "WARN": "\033[1;33m",
    "RESET": "\033[0m",
}


def _c(status: str, text: str) -> str:
    if not USE_COLOR:
        return text
    return f"{_COLORS.get(status, '')}{text}{_COLORS['RESET']}"


def print_report(result: ValidationResult, root: Path, verbose: bool = False) -> None:
    for f in result.findings:
        if f.status == "PASS" and not verbose:
            continue
        src = _rel(f.source_file, root)
        tgt = _rel(f.resolved, root)
        note = f"  ({f.note})" if f.note else ""
        missing = "  [missing]" if f.status == "FAIL" else ""
        print(
            f"{_c(f.status, f.status):<4}  {f.check:<26}  {src}\n"
            f"       → {tgt}{note}{missing}"
        )

    total = len(result.findings)
    n_pass = len(result.passes())
    n_fail = len(result.fails())
    n_warn = len(result.warns())

    print(f"\n{'─' * 64}")
    print(f"Checks  : {total:>5}")
    print(f"  {_c('PASS', 'PASS')} : {n_pass:>5}")
    print(f"  {_c('FAIL', 'FAIL')} : {n_fail:>5}")
    print(f"  {_c('WARN', 'WARN')} : {n_warn:>5}")

    if n_fail == 0 and n_warn == 0:
        print(f"\n{_c('PASS', '✓  All cross-links resolved.')}")
    elif n_fail == 0:
        print(f"\n{_c('WARN', f'⚠  No broken links, but {n_warn} warning(s) need attention.')}")
    else:
        print(f"\n{_c('FAIL', f'✗  {n_fail} broken link(s) found — see FAIL lines above.')}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate cross-file references in claude-for-customer-success/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help=(
            "Root of the claude-for-customer-success tree. "
            "Default: auto-detected relative to this script."
        ),
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Also print PASS lines",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any WARNings are present (in addition to FAILs)",
    )
    args = parser.parse_args(argv)

    # Auto-detect root: script lives in <suite>/scripts/ → suite root is parent
    if args.root is None:
        script_dir = Path(__file__).resolve().parent
        candidate = script_dir.parent
        if candidate.name == "claude-for-customer-success":
            root = candidate
        else:
            root = Path.cwd()
    else:
        root = args.root.resolve()

    if not root.is_dir():
        print(f"ERROR: root directory not found: {root}", file=sys.stderr)
        return 2

    print(f"Validating cross-links under: {root}\n")
    result = validate(root)
    print_report(result, root, verbose=args.verbose)

    if result.fails():
        return 1
    if args.strict and result.warns():
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
