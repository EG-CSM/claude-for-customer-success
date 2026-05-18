#!/usr/bin/env bash
# =============================================================================
# review-sweep.sh — Claude for CS Production-Readiness Rubric v1.7
# Automated mechanical sweep: mechanical BLOCK/WARN checks per §1, §2, §3, §5
#
# Usage:
#   bash scripts/review-sweep.sh [--plugin <name>] [--output <path>]
#
# Options:
#   --plugin csm|renewals|onboarding|cs-ops|rev-ops   Limit to one plugin
#   --output <path>    CSV output path (default: output/review-sweep-YYYYMMDD.csv)
#
# Output columns:
#   plugin, skill, check_id, severity, result, detail
#
# Result values: PASS | FAIL | SKIP
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DATE="$(date +%Y%m%d)"
OUTPUT_FILE="$REPO_ROOT/output/review-sweep-${DATE}.csv"
PLUGIN_FILTER=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --plugin) PLUGIN_FILTER="$2"; shift 2 ;;
    --output) OUTPUT_FILE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

mkdir -p "$(dirname "$OUTPUT_FILE")"

# CSV header
echo "plugin,skill,check_id,severity,result,detail" > "$OUTPUT_FILE"

# Counters
total_skills=0
total_checks=0
total_fail=0
total_pass=0

# Helper: emit a CSV row
emit() {
  local plugin="$1" skill="$2" check_id="$3" severity="$4" result="$5" detail="$6"
  # Escape commas in detail field
  detail="${detail//,/;}"
  echo "$plugin,$skill,$check_id,$severity,$result,$detail" >> "$OUTPUT_FILE"
  total_checks=$((total_checks + 1))
  if [[ "$result" == "FAIL" ]]; then
    total_fail=$((total_fail + 1))
  else
    total_pass=$((total_pass + 1))
  fi
}

# Helper: grep_present — returns 0 (true) if pattern found in file
grep_present() {
  local pattern="$1" file="$2"
  grep -qE "$pattern" "$file" 2>/dev/null
}

# Helper: frontmatter_value — extract value from YAML frontmatter
frontmatter_value() {
  local key="$1" file="$2"
  # Extract content between first --- and second ---
  # Use grep -m1 and suppress exit 1 on no-match via || true at pipeline end
  awk '/^---$/{if(found){exit} found=1; next} found{print}' "$file" | \
    grep -m1 -E "^${key}:" | sed "s/^${key}:[[:space:]]*//" | tr -d '"' || true
}

# Determine plugins to scan
if [[ -n "$PLUGIN_FILTER" ]]; then
  PLUGINS=("$PLUGIN_FILTER")
else
  PLUGINS=(csm renewals onboarding cs-ops rev-ops)
fi

echo "=== Claude for CS Production-Readiness Sweep ==="
echo "Date: $DATE"
echo "Repo: $REPO_ROOT"
echo "Output: $OUTPUT_FILE"
echo ""

for plugin in "${PLUGINS[@]}"; do
  plugin_dir="$REPO_ROOT/$plugin/skills"
  if [[ ! -d "$plugin_dir" ]]; then
    echo "  [SKIP] Plugin directory not found: $plugin_dir"
    continue
  fi

  echo "Scanning plugin: $plugin"

  for skill_dir in "$plugin_dir"/*/; do
    [[ -d "$skill_dir" ]] || continue
    skill_name="$(basename "$skill_dir")"
    skill_file="$skill_dir/SKILL.md"

    if [[ ! -f "$skill_file" ]]; then
      echo "  [WARN] No SKILL.md in $skill_dir"
      continue
    fi

    total_skills=$((total_skills + 1))

    # ------------------------------------------------------------------
    # SECTION 1 — Frontmatter Compliance
    # ------------------------------------------------------------------

    # 1.1 — deployment_target: plugin (BLOCK)
    dt_value="$(frontmatter_value "deployment_target" "$skill_file")"
    if [[ "$dt_value" == "plugin" ]]; then
      emit "$plugin" "$skill_name" "1.1" "BLOCK" "PASS" "deployment_target=plugin"
    elif [[ -z "$dt_value" ]]; then
      emit "$plugin" "$skill_name" "1.1" "BLOCK" "FAIL" "deployment_target missing"
    else
      emit "$plugin" "$skill_name" "1.1" "BLOCK" "FAIL" "deployment_target=$dt_value (expected: plugin)"
    fi

    # 1.1a — No top-level security: block in frontmatter (BLOCK for plugin target)
    # Extract frontmatter only (between first and second ---)
    frontmatter="$(awk '/^---$/{if(found){exit} found=1; next} found{print}' "$skill_file")"
    if echo "$frontmatter" | grep -qE "^security:"; then
      emit "$plugin" "$skill_name" "1.1a" "BLOCK" "FAIL" "top-level security: block found in frontmatter (plugin loader rejects this)"
    else
      emit "$plugin" "$skill_name" "1.1a" "BLOCK" "PASS" "no top-level security: block in frontmatter"
    fi

    # 1.2 — version field present (WARN)
    ver_value="$(frontmatter_value "version" "$skill_file")"
    if [[ -n "$ver_value" ]]; then
      emit "$plugin" "$skill_name" "1.2" "WARN" "PASS" "version=$ver_value"
    else
      emit "$plugin" "$skill_name" "1.2" "WARN" "FAIL" "version field missing from frontmatter"
    fi

    # 1.3 — name field present (WARN)
    name_value="$(frontmatter_value "name" "$skill_file")"
    if [[ -n "$name_value" ]]; then
      emit "$plugin" "$skill_name" "1.3" "WARN" "PASS" "name=$name_value"
    else
      emit "$plugin" "$skill_name" "1.3" "WARN" "FAIL" "name field missing from frontmatter"
    fi

    # 1.4 — description field present and non-empty (WARN)
    desc_value="$(frontmatter_value "description" "$skill_file")"
    if [[ -n "$desc_value" ]]; then
      emit "$plugin" "$skill_name" "1.4" "WARN" "PASS" "description present"
    else
      emit "$plugin" "$skill_name" "1.4" "WARN" "FAIL" "description field missing or empty"
    fi

    # ------------------------------------------------------------------
    # SECTION 2 — Trigger Precision (structural presence)
    # ------------------------------------------------------------------

    # 2.1 — Use When section present (BLOCK)
    # Accepts: case-insensitive "## Use When" OR "## Trigger Precision" (onboarding convention)
    if grep_present "^## [Uu]se [Ww]hen" "$skill_file" || grep_present "^## Trigger Precision" "$skill_file"; then
      emit "$plugin" "$skill_name" "2.1" "BLOCK" "PASS" "## Use When / Trigger Precision present"
    else
      emit "$plugin" "$skill_name" "2.1" "BLOCK" "FAIL" "## Use When section missing"
    fi

    # 2.2 — Do NOT Use For section present (BLOCK)
    # Accepts: case-insensitive "## Do NOT Use For" OR "## Trigger Precision" (onboarding convention)
    if grep_present "^## [Dd][Oo] [Nn][Oo][Tt] [Uu]se [Ff]or" "$skill_file" || grep_present "^## Trigger Precision" "$skill_file"; then
      emit "$plugin" "$skill_name" "2.2" "BLOCK" "PASS" "## Do NOT Use For / Trigger Precision present"
    else
      emit "$plugin" "$skill_name" "2.2" "BLOCK" "FAIL" "## Do NOT Use For section missing"
    fi

    # 2.3 — Typical Activation section present (WARN)
    if grep_present "^## Typical Activation" "$skill_file"; then
      emit "$plugin" "$skill_name" "2.3" "WARN" "PASS" "## Typical Activation present"
    else
      emit "$plugin" "$skill_name" "2.3" "WARN" "FAIL" "## Typical Activation section missing"
    fi

    # ------------------------------------------------------------------
    # SECTION 3 — Pre-flight / Configuration Gate
    # ------------------------------------------------------------------

    # 3.1 — Pre-flight section present (WARN)
    if grep_present "^## Pre-flight" "$skill_file"; then
      emit "$plugin" "$skill_name" "3.1" "WARN" "PASS" "## Pre-flight present"
    else
      emit "$plugin" "$skill_name" "3.1" "WARN" "FAIL" "## Pre-flight section missing"
    fi

    # 3.2 — References company-profile.md in pre-flight (WARN)
    if grep_present "company-profile\.md" "$skill_file"; then
      emit "$plugin" "$skill_name" "3.2" "WARN" "PASS" "company-profile.md referenced"
    else
      emit "$plugin" "$skill_name" "3.2" "WARN" "FAIL" "company-profile.md not referenced"
    fi

    # ------------------------------------------------------------------
    # SECTION 5 — Reasoning Protocol (structural/mechanical checks)
    # ------------------------------------------------------------------

    # 5.1 — ## Reasoning Protocol section present (WARN)
    if grep_present "^## Reasoning Protocol" "$skill_file"; then
      emit "$plugin" "$skill_name" "5.1" "WARN" "PASS" "## Reasoning Protocol present"
    else
      emit "$plugin" "$skill_name" "5.1" "WARN" "FAIL" "## Reasoning Protocol section missing"
    fi

    # 5.1-D1a — Opening line correct (WARN)
    if grep_present "Before generating output, apply these primers:" "$skill_file"; then
      emit "$plugin" "$skill_name" "5.1-D1a" "WARN" "PASS" "D1 opening line present"
    else
      emit "$plugin" "$skill_name" "5.1-D1a" "WARN" "FAIL" "D1 opening line missing: 'Before generating output, apply these primers:'"
    fi

    # 5.1-D1b — All 4 primer headings present (WARN)
    has_classify=false; has_constraints=false; has_expert=false; has_anti=false
    grep_present "CLASSIFY" "$skill_file" && has_classify=true || true
    grep_present "CONSTRAINTS" "$skill_file" && has_constraints=true || true
    grep_present "EXPERT CHECK" "$skill_file" && has_expert=true || true
    grep_present "ANTI-PATTERNS" "$skill_file" && has_anti=true || true

    missing_primers=""
    [[ "$has_classify" == "true" ]] || missing_primers="${missing_primers}CLASSIFY;"
    [[ "$has_constraints" == "true" ]] || missing_primers="${missing_primers}CONSTRAINTS;"
    [[ "$has_expert" == "true" ]] || missing_primers="${missing_primers}EXPERT CHECK;"
    [[ "$has_anti" == "true" ]] || missing_primers="${missing_primers}ANTI-PATTERNS;"

    if [[ -z "$missing_primers" ]]; then
      emit "$plugin" "$skill_name" "5.1-D1b" "WARN" "PASS" "all 4 primer headings present"
    else
      emit "$plugin" "$skill_name" "5.1-D1b" "WARN" "FAIL" "missing primers: ${missing_primers%?}"
    fi

    # 5.1-D1c — Post-execution verification block present (WARN)
    if grep_present "\*\*After execution\*\*.*verify:" "$skill_file" || \
       grep_present "\*\*After execution\*\*" "$skill_file"; then
      emit "$plugin" "$skill_name" "5.1-D1c" "WARN" "PASS" "post-execution verification block present"
    else
      emit "$plugin" "$skill_name" "5.1-D1c" "WARN" "FAIL" "post-execution verification block missing ('**After execution**, verify:')"
    fi

    # 5.1-D1d — Confidence calibration line present (WARN)
    if grep_present "\[High\].*\[Medium\].*\[Low\]" "$skill_file" || \
       grep_present "Confidence:.*High.*Medium.*Low" "$skill_file"; then
      emit "$plugin" "$skill_name" "5.1-D1d" "WARN" "PASS" "3-band confidence calibration line present"
    else
      emit "$plugin" "$skill_name" "5.1-D1d" "WARN" "FAIL" "3-band confidence calibration missing (High/Medium/Low format)"
    fi

    # 5.1-D4-count — Anti-pattern count in range 4–6 (WARN)
    # Count lines that look like anti-pattern entries (list items under ANTI-PATTERNS)
    # Strategy: count bullet/list items in the ANTI-PATTERNS section
    anti_section=$(awk '/\*\*ANTI-PATTERNS\*\*|^4\.\s+\*\*ANTI-PATTERNS\*\*/,/^[0-9]+\.\s+\*\*/' "$skill_file" 2>/dev/null || true)
    anti_count=0
    if [[ -n "$anti_section" ]]; then
      anti_count=$(echo "$anti_section" | grep -cE "^\s+- " || true)
      anti_count=${anti_count:-0}
    fi
    if [[ "$anti_count" -ge 4 && "$anti_count" -le 6 ]]; then
      emit "$plugin" "$skill_name" "5.1-D4a" "WARN" "PASS" "anti-pattern count=$anti_count (in range 4-6)"
    elif [[ "$anti_count" -eq 0 ]]; then
      emit "$plugin" "$skill_name" "5.1-D4a" "WARN" "SKIP" "anti-pattern count=0 (check 5.1 FAIL may explain; verify manually)"
    elif [[ "$anti_count" -lt 4 ]]; then
      emit "$plugin" "$skill_name" "5.1-D4a" "WARN" "FAIL" "anti-pattern count=$anti_count (below minimum of 4)"
    else
      emit "$plugin" "$skill_name" "5.1-D4a" "WARN" "FAIL" "anti-pattern count=$anti_count (exceeds maximum of 6)"
    fi

    # ------------------------------------------------------------------
    # SECTION 5.1a — Reasoning Blueprint companion file
    # ------------------------------------------------------------------

    # 5.1a — reasoning-blueprint.md file exists (WARN)
    blueprint_path_refs="$skill_dir/references/reasoning-blueprint.md"
    blueprint_path_ref="$skill_dir/reference/reasoning-blueprint.md"
    blueprint_found=false
    blueprint_path_used=""

    if [[ -f "$blueprint_path_refs" ]]; then
      blueprint_found=true
      blueprint_path_used="references/reasoning-blueprint.md"
    elif [[ -f "$blueprint_path_ref" ]]; then
      blueprint_found=true
      blueprint_path_used="reference/reasoning-blueprint.md (NOTE: singular 'reference' — should be 'references')"
    fi

    if [[ "$blueprint_found" == "true" ]]; then
      emit "$plugin" "$skill_name" "5.1a" "WARN" "PASS" "$blueprint_path_used"
    else
      emit "$plugin" "$skill_name" "5.1a" "WARN" "FAIL" "references/reasoning-blueprint.md not found"
    fi

    # 5.1a-path — Flag singular 'reference/' vs 'references/' (NOTE)
    if [[ -f "$blueprint_path_ref" && ! -f "$blueprint_path_refs" ]]; then
      emit "$plugin" "$skill_name" "5.1a-path" "NOTE" "FAIL" "blueprint uses singular 'reference/' directory — should be 'references/'"
    fi

    # ------------------------------------------------------------------
    # SECTION 6 — Reference Files table
    # ------------------------------------------------------------------

    # 6.1 — ## Reference Files section present (WARN)
    if grep_present "^## Reference Files" "$skill_file"; then
      emit "$plugin" "$skill_name" "6.1" "WARN" "PASS" "## Reference Files section present"
    else
      emit "$plugin" "$skill_name" "6.1" "WARN" "FAIL" "## Reference Files section missing"
    fi

    # 6.1a — reasoning-blueprint.md declared in Reference Files table (WARN)
    if grep_present "reasoning-blueprint\.md" "$skill_file"; then
      emit "$plugin" "$skill_name" "6.1a" "WARN" "PASS" "reasoning-blueprint.md referenced in SKILL.md"
    else
      emit "$plugin" "$skill_name" "6.1a" "WARN" "FAIL" "reasoning-blueprint.md not referenced in SKILL.md"
    fi

    # ------------------------------------------------------------------
    # SECTION 9 — G-code Governance
    # ------------------------------------------------------------------

    # 9.1 — At least one G-code referenced in Reasoning Protocol (WARN)
    if grep_present "G[1-9][0-9]?:" "$skill_file" || grep_present "\bG[1-9]\b" "$skill_file"; then
      emit "$plugin" "$skill_name" "9.1" "WARN" "PASS" "G-code governance reference found"
    else
      emit "$plugin" "$skill_name" "9.1" "WARN" "FAIL" "no G-code references found in SKILL.md"
    fi

    # ------------------------------------------------------------------
    # STATUS SIGNAL
    # ------------------------------------------------------------------

    # S1 — Output status signal present (WARN)
    if grep_present "\[PROPOSED\]|\[VALIDATED\]|\[DRAFT\]|\[REQUIRES FOLLOW-UP\]" "$skill_file"; then
      status_signal="$(grep -oE '\[PROPOSED\]|\[VALIDATED\]|\[DRAFT\]|\[REQUIRES FOLLOW-UP\]' "$skill_file" | head -1)"
      emit "$plugin" "$skill_name" "S1" "WARN" "PASS" "status signal=$status_signal"
    else
      emit "$plugin" "$skill_name" "S1" "WARN" "FAIL" "no output status signal found (PROPOSED/VALIDATED/DRAFT)"
    fi

  done

  echo "  Done: $plugin"
done

# ------------------------------------------------------------------
# Summary stats
# ------------------------------------------------------------------

echo ""
echo "=== SWEEP COMPLETE ==="
echo "Skills scanned:  $total_skills"
echo "Checks run:      $total_checks"
echo "  PASS:          $total_pass"
echo "  FAIL:          $total_fail"
echo "Output:          $OUTPUT_FILE"
echo ""

# Per-plugin failure summary
echo "=== FAIL counts by plugin ==="
if [[ -f "$OUTPUT_FILE" ]]; then
  tail -n +2 "$OUTPUT_FILE" | awk -F',' '$5=="FAIL"{count[$1]++} END{for(p in count) print p": "count[p]" failures"}' | sort
fi

echo ""
echo "=== BLOCK failures ==="
if [[ -f "$OUTPUT_FILE" ]]; then
  tail -n +2 "$OUTPUT_FILE" | awk -F',' '$4=="BLOCK" && $5=="FAIL"{print $1"/"$2" — "$3": "$6}' | sort
fi

echo ""
echo "Next step: open $OUTPUT_FILE in a spreadsheet or run:"
echo "  grep FAIL $OUTPUT_FILE | sort -t, -k1,1 -k3,3"
echo "  to sort by plugin and check ID."
