#!/usr/bin/env python3
"""
Rev-ops eval benchmark aggregator.
Reads grading.json files from a completed iteration directory and produces
benchmark.json + benchmark.md summary.

Usage:
  python aggregate_benchmark.py <workspace_path> --skill-name <name>

Example:
  python aggregate_benchmark.py ./deal-to-outcome-tracing-workspace/iteration-1 \
    --skill-name deal-to-outcome-tracing
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


def load_grading_results(workspace_path: Path) -> list[dict]:
    """Load all grading.json files from eval subdirectories."""
    results = []
    for eval_dir in sorted(workspace_path.iterdir()):
        if not eval_dir.is_dir():
            continue
        grading_file = eval_dir / "with_skill" / "grading.json"
        if grading_file.exists():
            with open(grading_file) as f:
                results.append(json.load(f))
    return results


def load_eval_metadata(workspace_path: Path) -> dict[int, dict]:
    """Load eval_metadata.json files keyed by eval_id."""
    metadata = {}
    for eval_dir in sorted(workspace_path.iterdir()):
        if not eval_dir.is_dir():
            continue
        meta_file = eval_dir / "eval_metadata.json"
        if meta_file.exists():
            with open(meta_file) as f:
                m = json.load(f)
                metadata[m["eval_id"]] = m
    return metadata


def aggregate(workspace_path: Path, skill_name: str) -> dict:
    """Compute benchmark statistics from grading results."""
    results = load_grading_results(workspace_path)
    metadata = load_eval_metadata(workspace_path)

    if not results:
        print(f"No grading.json files found in {workspace_path}", file=sys.stderr)
        sys.exit(1)

    # Load evals.json to get category per eval
    evals_file = workspace_path.parent.parent / "evals" / skill_name / "evals.json"
    category_map: dict[int, str] = {}
    if evals_file.exists():
        with open(evals_file) as f:
            evals_data = json.load(f)
            for e in evals_data.get("evals", []):
                category_map[e["id"]] = e.get("category", "unknown")

    total = len(results)
    passed = sum(1 for r in results if r.get("overall_passed", False))
    pass_rate = passed / total if total > 0 else 0.0

    # By category
    category_results: dict[str, list[bool]] = defaultdict(list)
    for r in results:
        cat = category_map.get(r.get("eval_id", -1), "unknown")
        category_results[cat].append(r.get("overall_passed", False))

    by_category = {}
    for cat, outcomes in category_results.items():
        n = len(outcomes)
        cat_pass = sum(outcomes)
        by_category[cat] = {
            "pass_rate": round(cat_pass / n, 3),
            "passed": cat_pass,
            "n": n,
        }

    # By assertion type
    type_results: dict[str, list[bool]] = defaultdict(list)
    for r in results:
        for exp in r.get("expectations", []):
            # Match assertion type from eval metadata
            eval_id = r.get("eval_id", -1)
            if eval_id in metadata:
                for assertion in metadata[eval_id].get("assertions", []):
                    if assertion.get("text") == exp.get("text"):
                        atype = assertion.get("type", "unknown")
                        type_results[atype].append(exp.get("passed", False))
                        break

    assertion_breakdown = {}
    for atype, outcomes in type_results.items():
        n = len(outcomes)
        assertion_breakdown[atype] = {
            "pass_rate": round(sum(outcomes) / n, 3) if n > 0 else 0.0,
            "n": n,
        }

    # Failure patterns
    failure_map: dict[str, list] = defaultdict(list)
    for r in results:
        cat = category_map.get(r.get("eval_id", -1), "unknown")
        for exp in r.get("expectations", []):
            if not exp.get("passed", True):
                failure_map[cat].append({
                    "eval_id": r.get("eval_id"),
                    "eval_name": r.get("eval_name"),
                    "assertion": exp.get("text"),
                    "evidence": exp.get("evidence", ""),
                })

    failure_patterns = []
    for cat, failures in failure_map.items():
        if failures:
            failure_patterns.append({
                "category": cat,
                "count": len(failures),
                "affected_evals": list({f["eval_name"] for f in failures}),
                "sample_assertions": [f["assertion"] for f in failures[:3]],
            })

    return {
        "skill_name": skill_name,
        "workspace": str(workspace_path),
        "total_evals": total,
        "passed": passed,
        "pass_rate": round(pass_rate, 3),
        "by_category": by_category,
        "assertion_breakdown": assertion_breakdown,
        "failure_patterns": failure_patterns,
    }


def to_markdown(benchmark: dict) -> str:
    """Produce a readable benchmark.md from benchmark dict."""
    lines = [
        f"# Benchmark: {benchmark['skill_name']}",
        "",
        f"**Total evals:** {benchmark['total_evals']}  "
        f"**Passed:** {benchmark['passed']}  "
        f"**Pass rate:** {benchmark['pass_rate']:.1%}",
        "",
        "## By Category",
        "",
        "| Category | Pass rate | n |",
        "|----------|-----------|---|",
    ]
    for cat, stats in benchmark["by_category"].items():
        lines.append(
            f"| {cat} | {stats['pass_rate']:.1%} | {stats['n']} |"
        )

    lines += [
        "",
        "## By Assertion Type",
        "",
        "| Type | Pass rate | n |",
        "|------|-----------|---|",
    ]
    for atype, stats in benchmark["assertion_breakdown"].items():
        lines.append(
            f"| {atype} | {stats['pass_rate']:.1%} | {stats['n']} |"
        )

    if benchmark["failure_patterns"]:
        lines += [
            "",
            "## Failure Patterns",
            "",
        ]
        for fp in benchmark["failure_patterns"]:
            lines.append(
                f"**{fp['category']}** — {fp['count']} failure(s) "
                f"in: {', '.join(fp['affected_evals'])}"
            )
            for sa in fp.get("sample_assertions", []):
                lines.append(f"  - {sa}")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate rev-ops eval benchmark")
    parser.add_argument("workspace", help="Path to iteration directory")
    parser.add_argument("--skill-name", required=True, help="Skill name")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    benchmark = aggregate(workspace, args.skill_name)

    # Write benchmark.json
    json_out = workspace / "benchmark.json"
    with open(json_out, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"Written: {json_out}")

    # Write benchmark.md
    md_out = workspace / "benchmark.md"
    with open(md_out, "w") as f:
        f.write(to_markdown(benchmark))
    print(f"Written: {md_out}")

    # Print summary
    print(f"\nPass rate: {benchmark['pass_rate']:.1%} ({benchmark['passed']}/{benchmark['total_evals']})")
    if benchmark["failure_patterns"]:
        print(f"Failure patterns: {len(benchmark['failure_patterns'])}")
        for fp in benchmark["failure_patterns"]:
            print(f"  [{fp['category']}] {fp['count']} failure(s)")


if __name__ == "__main__":
    main()
