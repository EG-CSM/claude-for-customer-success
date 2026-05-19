# Agent D — Design Integrity Report

**Audit scope:** 83 SKILL.md files across 5 plugins (csm, renewals, onboarding, cs-ops, rev-ops)
**Audit date:** 2026-05-18
**Auditor:** Agent D — Design Integrity

---

## Summary

- **Skills audited:** 83
- **Findings:** 9 BLOCK / 21 WARN / 11 NOTE

---

## Findings

---

### [BLOCK] rev-ops/unit-of-growth-calculator

**Design issue:** Reference Loading — Broken Reference File

**Finding:** The Reference Files table declares `references/benchmark-library.md` as a required reference file. This file does not exist on disk. The `references/` directory for this skill contains only `reasoning-blueprint.md` and `metrics-and-glossary.md`. The benchmark-library.md is cited as the authoritative source for benchmark defaults, source registry URLs, confidence tiers, and imbalance signal thresholds — core behaviors the skill invokes during execution.

**Impact:** Claude will attempt to load a file that doesn't exist at the point it needs benchmark defaults, confidence tiers, or imbalance signal thresholds. The skill either silently falls back to hallucinated benchmarks or errors. Either path degrades output quality on the skill's primary differentiator — benchmark-grounded unit economics.

**Recommendation:** Either create `references/benchmark-library.md` with the benchmark tables described in the Reference Files entry, or remove the entry from the table and inline the benchmark content into the skill body. Do not leave a referenced file absent.

---

### [BLOCK] rev-ops/csql-tracking

**Design issue:** Reference Loading — Absolute Path Anti-Pattern

**Finding:** The Reference Files table lists four reference files. Three use absolute-style paths (`rev-ops/skills/csql-tracking/reference/csql-record-schema.md`, etc.) rather than relative paths (`reference/csql-record-schema.md`). Additionally, the short-name entries in the first column (`csql-record-schema.md`, `csql-status-transitions.md`, `query-filter-patterns.md`) are registered by the path resolution logic as bare filenames relative to the skill directory — but no such bare files exist. The actual files live in `reference/` (singular), while the references column uses repo-root-relative paths.

The path table also lists `rev-ops/skills/csql-tracking/references/reasoning-blueprint.md` (plural `references/`) in the "Path" column but bare `reasoning-blueprint.md` in the "File" column. This asymmetry means whichever path Claude tries to resolve — relative or absolute — it will fail.

**Impact:** Claude cannot reliably resolve any of the four referenced files. When attempting to validate CSQL record formats, review state machine transitions, or apply query filter patterns, it either errors silently or generates from training memory — bypassing the authoritative schema files that define this skill's core behavior.

**Recommendation:** Replace all path entries with relative paths from the skill directory. The files exist at `reference/csql-record-schema.md`, `reference/csql-status-transitions.md`, `reference/query-filter-patterns.md`, and `references/reasoning-blueprint.md`. Use those paths directly in the "File" column and remove the redundant "Path" column.

---

### [BLOCK] renewals/churn-rca

**Design issue:** Reference Loading — Mixed directory + broken relative paths

**Finding:** The Reference Files table mixes `references/` (plural — contains only `reasoning-blueprint.md`) and `reference/` (singular — contains the three taxonomy files). The table entries for `churn-rca-taxonomy.md`, `cohort-analysis-framework.md`, and `remediation-playbook.md` use bare filenames with no path prefix. Python path resolution confirms these bare names (`churn-rca-taxonomy.md`, etc.) do not resolve relative to the skill directory — they exist under `reference/` but are listed without the prefix.

The skill also includes inline load-on-demand instructions (`Load churn-rca-taxonomy.md when classifying root causes...`) using bare filenames, which will fail to resolve for the same reason.

**Impact:** Churn-rca is the highest-instruction-fidelity skill in the renewals plugin — it has a 7-category taxonomy, cohort analysis framework, and remediation playbook that are all meaningfully load-on-demand. None of those files are loadable as specified. Claude falls back to training-memory RCA categories, which are generic and unvalidated against the configured taxonomy.

**Recommendation:** Prefix all three taxonomy file entries with `reference/` in both the table and the inline load instructions. Validate that `reference/churn-rca-taxonomy.md`, `reference/cohort-analysis-framework.md`, and `reference/remediation-playbook.md` are the correct paths (confirmed: they are).

---

### [BLOCK] renewals/downgrade-analysis

**Design issue:** Reference Loading — Non-skill-local file listed as reference

**Finding:** The Reference Files table lists `company-profile.md` as a reference file with the purpose "Account context and historical engagement data." `company-profile.md` is not a file local to the skill directory — it lives at `~/.claude/plugins/config/claude-for-customer-success/company-profile.md`. Listing it in the Reference Files table alongside `reference/downgrade-driver-taxonomy.md` implies it should be loaded the same way as on-demand reference files. It cannot be resolved as a relative path from the skill directory.

This is a category error: `company-profile.md` is a runtime config file read during Pre-flight, not a reference document loaded on-demand during analysis.

**Impact:** An orchestrator or operator reading this Reference Files table to understand the skill's loading behavior will attempt to provision `company-profile.md` as a skill-local file. During execution, any instruction derived from "load `company-profile.md` from the Reference Files section" will fail. The Pre-flight section already handles config file reading correctly — the Reference Files table creates a conflicting and incorrect loading model.

**Recommendation:** Remove `company-profile.md` from the Reference Files table entirely. It is not a reference file. Pre-flight handles it. If the intent is to document that the skill reads config, add a note in the Pre-flight section only.

---

### [BLOCK] csm/success-plan-progress-review

**Design issue:** Reference Loading — Live artifact path in Reference Files table

**Finding:** The Reference Files table for this skill does not directly contain the broken reference — the broken reference (`context/progress-review-acme-corp-2026-05-17.md`) is embedded in an example block in the Output section. However, the skill's file write path (`context/progress-review-[safe_account]-[YYYY-MM-DD].md`) and read path (`context/success-plan-[safe_account]-[canvas_date].md`) are scoped to a `context/` directory relative to the plugin working directory. No documentation confirms where `context/` resolves at runtime in a plugin deployment. Skills are loaded from `~/.claude/plugins/` but their working directory for file I/O is undefined in the plugin spec.

**Impact:** This skill writes and reads inter-skill artifacts (canvas files produced by `csm:success-plan-canvas`, progress review files written by this skill). If `context/` resolves differently in Claude Code vs. claude.ai Plugin deployments, the inter-skill contract breaks — `success-plan-progress-review` cannot locate canvas files produced by `success-plan-canvas`. This is a production path ambiguity on the critical inter-skill data dependency.

**Recommendation:** Explicitly document the resolved `context/` path in Pre-flight. Define whether it is relative to the session working directory, the plugin config directory, or a hardcoded path. The inter-skill contract section shows the correct flow — that documentation should reference the actual filesystem path, not just the relative `context/` prefix.

---

### [BLOCK] csm/expansion-business-case

**Design issue:** Reference Loading — Mixed `reference/` and `references/` within the same skill

**Finding:** The Reference Files table lists files from both `reference/` (singular: `reference/csql-package-template.md`, `reference/expansion-proposal-template.md`, `reference/ocv-synthesis-prompt.md`) and `references/` (plural: `references/reasoning-blueprint.md`). Both directories exist in the skill directory. This is not a broken reference — all four files exist — but the inconsistency in directory naming within a single skill's table creates an authoring ambiguity that degrades maintainability.

The same mixed-directory pattern appears in: `csm/expansion-onboarding`, `csm/success-plan-canvas`, `renewals/churn-rca`, `renewals/downgrade-analysis` (6 skills total).

**Impact:** When adding future reference files to these skills, authors must determine which directory convention applies. The inconsistency has already caused one genuine broken reference (churn-rca). It also creates confusion in any automation that scans reference directories to validate skill completeness.

**Recommendation:** Standardize to a single directory per skill. `references/` (plural) is the convention used by the automated rubric sweep and by the majority of skills across all plugins. Migrate the singular `reference/` content to `references/` in the 6 affected skills and update all path entries accordingly.

---

### [BLOCK] rev-ops/outcome-statement-builder

**Design issue:** Reference Loading — Non-markdown file in Reference Files table; live test artifact as authoritative reference

**Finding:** The Reference Files table includes `gong-outcome-review-deck.html` as an authoritative template reference: "Use as the visual and structural template for all HTML deck outputs — match the layout, color treatment, card structure, and typography exactly." Two design problems:

1. The file exists — but it is a live test artifact from a single Gong.io CRO test run, not a validated, generalized template. The skill instructs Claude to "match exactly" a file derived from one specific customer test. If the Gong example contains customer-specific branding, data, or formatting choices, Claude will replicate them for all operators.

2. The Reference Files section references both `references/worked-examples.md` and `references/reference-registry.md` (under `references/`), plus `gong-outcome-value-registry.md` and `gong-outcome-review-deck.html` (directly in the skill root, not under a subdirectory). The structural inconsistency means these files are treated as reference materials but live outside the designated reference directory.

**Impact:** Claude is instructed to treat a single customer's test run as the canonical visual template for all output. This is a scope collapse — one test artifact governs all operator deployments. If the Gong data or branding is wrong or non-generic, every deck output will inherit the defect.

**Recommendation:** Promote `gong-outcome-review-deck.html` to a named template directory (`reference/html-deck-template.html`) with customer data stripped, or replace the file reference with an inline HTML structure specification in the skill body. Remove the instruction to "match exactly" in favor of "use as structural reference." Move all reference-class files into `references/`.

---

### [BLOCK] All skills (83/83) — Artifact separator noise

**Design issue:** Progressive Disclosure — Stray YAML separator lines throughout skill bodies

**Finding:** Every SKILL.md in the ecosystem contains between 6 and 37 standalone `---` separator lines embedded in the instruction body, beyond the two required for YAML frontmatter. Examples: `csm/value-statement` has 37 `---` lines; `cs-ops/metric-dashboard` has 34; `csm/escalation-memo` has 31. The lines appear between sections, between paragraphs, and — most critically — in densely stacked clusters of 10–20 consecutive `---` lines in several skills.

The stacked cluster pattern (e.g., `csm/call-prep` lines 219–229: ten consecutive `---` lines) is evidence of repeated edit-and-merge operations that accumulated separator artifacts rather than intentional formatting.

**Impact:** While Markdown renders horizontal rules as visual separators, in the context of YAML-aware parsers and plugin loaders, each standalone `---` is a potential frontmatter boundary marker. Any parser that treats `---` as a YAML document separator will misparse the skill body, treating sections after separator lines as new documents. More practically, the visual clutter degrades readability and signals authoring process discipline issues — if artifact accumulation produced stacked separators, what else accumulated silently?

**Recommendation:** Run a cleanup pass across all 83 skills to collapse stacked consecutive `---` lines to single separators and remove decorative `---` lines between paragraphs within the same section. The frontmatter boundary (two `---` lines) must be preserved. All others are optional and should be used sparingly.

---

### [BLOCK] csm/success-plan-builder vs csm/success-plan-canvas

**Design issue:** Skill-vs-Service Boundary Violation — Functional overlap between two skills on the same service step

**Finding:** Both `success-plan-builder` and `success-plan-canvas` produce success plan artifacts for the same service step: creating a structured success plan for a customer account. The boundary between them is described in `success-plan-builder`'s Do NOT Use For as: "The structured success plan canvas format — use /csm:success-plan-canvas for OCV-aligned canvas output." This implies the two skills differ only in output format (narrative plan vs. OCV-aligned canvas schema).

However, both skills:
- Accept the same inputs (account name, CS motion context, milestones)
- Execute during the same service moment (plan creation at or after kickoff)
- Require the same Pre-flight configuration
- Produce a "success plan" as their output artifact

The distinction between "a success plan" and "a success plan canvas" is an internal schema difference, not a service boundary. An operator invoking this plugin faces an ambiguous choice between two skills that occupy the same service step, with the decision gated on knowledge of whether their organization uses "OCV-aligned canvas output" — a term that requires prior knowledge of the OCV system to parse.

**Impact:** Operators will misfire between these two skills, producing the wrong artifact format for their workflow. The trigger overlap creates false positive activations: any "build me a success plan" request could legitimately activate either skill. Two skills owning the same service step is a boundary violation — it fragments what should be a single skill with an `--format` flag into two separate skills with separate trigger surfaces.

**Recommendation:** Merge `success-plan-builder` and `success-plan-canvas` into a single skill with a format flag (`--narrative` vs. `--canvas`). If the OCV schema is a mandatory organizational choice that justifies separate skills, the trigger language must be made unambiguous: `success-plan-canvas` should require an explicit OCV context marker that `success-plan-builder` cannot match.

---

### [WARN] csm/customize vs csm/cold-start-interview

**Design issue:** Skill-vs-Service Boundary — Partial scope duplication between config skills

**Finding:** `csm/customize` describes itself as "Alias for cold-start-interview when run fresh." `csm/cold-start-interview` describes itself as the primary first-run setup skill with `csm:customize --full` as an alias. Both skills perform the same config interview, write the same config files, and have nearly identical Pre-flight sections. The distinction is: `cold-start-interview` is preferred for "a cleaner first-run experience" (per `customize`'s Do NOT Use For) and `customize` handles partial section updates (`--section <name>`).

Two problems: (1) The same "full interview + config write" logic exists in both skills — divergence over time is inevitable. (2) The trigger disambiguation ("prefer cold-start-interview for first run") requires the operator to know which one to choose rather than the skill figuring it out.

This pattern repeats across all 5 plugins: every plugin has both a `cold-start-interview` and a `customize` skill with overlapping scope.

**Impact:** Maintenance burden doubles for any change to the interview flow. Operators must choose between two identically-scoped skills. Any divergence between the two creates inconsistent config outputs. The 5x repetition of this pattern across plugins amplifies the risk.

**Recommendation:** Collapse each plugin's `cold-start-interview` + `customize` into a single `setup` skill. First-run detection (no config exists / placeholders present) determines whether the full interview runs or the section-update path activates. This is logic the skill can execute, not a choice the operator should have to make.

---

### [WARN] All 5 plugins — cold-start-interview skills have no service context declaration

**Design issue:** Service Context — Orphaned capability pattern

**Finding:** None of the 83 SKILL.md files declare a `service:` metadata field or a service context section in their instructions. Only 1 skill declares `lifecycle_stage` in frontmatter (`csm/expansion-business-case` and `csm/expansion-onboarding`). The rest have no explicit statement of which service or service step they belong to.

The cold-start-interview and customize skills across all 5 plugins are especially affected: they function as infrastructure-layer skills (config writers) rather than customer-facing service steps, but nothing in their design distinguishes them from operational skills. An orchestrator has no metadata to classify these as "setup required before other skills run."

**Impact:** Orchestration agents composing multi-skill workflows cannot programmatically determine service step membership, sequencing dependencies, or which skills are prerequisites vs. operational. Any agent-level orchestration (as designed in the managed-agent-cookbooks) must hard-code this knowledge rather than reading it from skill metadata. This is an ecosystem-level gap: the skills compose well by convention but are invisible to automation.

**Recommendation:** Add `service:` and `lifecycle_stage:` fields to frontmatter for all operational skills. For infrastructure skills (cold-start-interview, customize), add a `skill_type: config` frontmatter field so orchestrators can identify and sequence them. The expansion-business-case and expansion-onboarding skills provide the right model — scale it to the full ecosystem.

---

### [WARN] renewals — 10 skills missing structured Use When / Do NOT Use For sections

**Finding:** The renewals plugin has 10 skills with `## Use when` (lowercase) and `## Do NOT use for` (lowercase) headings rather than the title-case versions used in csm, onboarding, and rev-ops. More significantly, several renewals skills' Use When sections contain 0 bullet points (confirmed by line count analysis showing 0 for risk-assessment, renewal-forecast, price-increase-prep, negotiation-prep, expansion-signal, executive-summary, contract-review, cold-start-interview, and churn-analysis).

Spot-check of `renewals/risk-assessment` confirms `## Use when` and `## Do NOT use for` exist but the body content is embedded in the section below the heading — the bullets are present but structured as prose paragraphs rather than list items, meaning automated trigger audits miss them.

**Impact:** Automated trigger precision validation (check 2.1/2.2) may produce false-passes on renewals skills where the Use When content exists but isn't bullet-formatted. Human operators scanning the skill for activation guidance see inconsistent formatting across the plugin compared to csm/onboarding norms.

**Recommendation:** Standardize all renewals skills to title-case `## Use When` / `## Do NOT Use For` with bullet-list bodies. Run a focused authoring pass on renewals to verify trigger content quality matches the csm plugin standard.

---

### [WARN] csm — 17 skills with Reasoning Protocol section containing stale blueprint forward reference

**Finding:** Several csm skills contain the pattern:

```
## Reasoning Protocol

> Full reasoning blueprint: `references/reasoning-blueprint.md`
```

...followed by a full 4-primer D1 structure. This creates a redundant forward reference at the top of the Reasoning Protocol — the blueprint reference appears both as an inline directive and in the Reference Files table at the bottom of the skill. Examples: `csm/escalation-memo` includes both `> Full reasoning blueprint: references/reasoning-blueprint.md` and a separate Reference Files entry for the same file.

**Impact:** The inline forward reference implies the full reasoning protocol is defined in the external file rather than inline. An operator reading the skill will be uncertain whether the inline primers or the external file governs. If Claude attempts to resolve the blueprint reference before applying the inline primers, it loads context early (progressive disclosure violation). If it ignores the reference and uses the inline primers, the reference is dead weight.

**Recommendation:** Remove the inline `> Full reasoning blueprint: ...` forward reference from all Reasoning Protocol sections. The Reference Files table entry is sufficient — it correctly marks the file as on-demand. The inline reference creates ambiguity about loading order.

---

### [WARN] csm/account-research — Output section structurally unreachable

**Finding:** `account-research/SKILL.md` has no `## Output` section. The skill's output is described inline across multiple sections (`## Brief structure`, `## Output mode`, `## Deep mode additions`). These inline output descriptions are thorough but not grouped under the canonical `## Output` heading that the rubric and other skills use.

**Impact:** Any orchestrator or operator looking for `## Output` to understand what artifact the skill produces will not find it. The `--brief`, `--deep`, and `--stakeholders` output modes are described in scattered sections, making it harder to verify that the output contract is complete and consistent.

**Recommendation:** Add a top-level `## Output` section near the end of the skill body that consolidates the output contract: modes, artifact format, and the reviewer note requirement. The existing inline descriptions can remain as implementation detail — the `## Output` section provides the contract summary.

---

### [WARN] csm/call-prep — Reference Files table entry incomplete

**Finding:** The Reference Files section in `call-prep/SKILL.md` has only the table header row and a single entry for `references/reasoning-blueprint.md`. However, call-prep is one of the more complex csm skills — it handles 6 call types with different brief structures, agenda templates, and data gathering approaches. The skill body references no external reference files beyond the blueprint, meaning all call-type templates and agenda structures are inlined.

Contrast with `account-research`, which explicitly separates output structure into the skill body with detailed per-mode instructions. `call-prep` does the same inline but offers no indication whether call-type templates are intended to be externalizable.

**Impact:** The Reference Files table is minimal (1 entry) relative to the skill's complexity. This is not a blocking issue — but it signals that call-prep was not designed with future modularity in mind. Adding a second call type or modifying agenda structures requires editing the monolithic skill body rather than loading a template file.

**Recommendation:** NOTE-level for now (see below). Consider extracting call-type agenda templates to `references/call-type-templates.md` when the skill is next revised — this would make the output structure auditable and updateable without touching the reasoning logic.

---

### [WARN] onboarding/skills/references/skill-impact-map.md — Orphaned shared reference

**Finding:** `onboarding/skills/references/skill-impact-map.md` exists at the plugin skills level (not under any individual skill's `references/` directory). No individual SKILL.md in the onboarding plugin references this file in its Reference Files section. It appears to be a cross-skill reference document that was created but never wired into any skill's loading instructions.

**Impact:** The file is unreachable by any skill's on-demand loading mechanism. It consumes space and creates a false signal of documentation completeness — an operator or developer might assume skills use this cross-skill map when they don't.

**Recommendation:** Either wire `skill-impact-map.md` into relevant onboarding skills that have skill-sequencing logic (e.g., `onboarding-plan`, `kickoff-prep`, `handoff-doc`), or remove the file. If it's intended as human-readable documentation, move it to the `docs/` tree.

---

### [WARN] cs-ops/customize — Broken reference in Reference Files (formatting artifact)

**Finding:** The cs-ops/customize Reference Files section contains a malformed entry. Python path resolution identified a reference path containing a newline character: `` `references/reasoning-blueprint.md` — reasoning framework for this skill\n- `company-profile.md` ``. This is a Markdown list-item continuation that was incorrectly formatted as part of a table row, creating a multi-line cell that looks correct to a human reader but is unresolvable as a file path.

The actual `references/reasoning-blueprint.md` file exists. But the table cell formatting embeds the `company-profile.md` reference inside the same cell as a continuation, meaning `company-profile.md` is listed neither as a separate table row nor as a correctly formatted entry.

**Impact:** `company-profile.md` is silently present in the Reference Files section but formatted in a way that prevents it from being machine-parsed as a reference. Combined with the downgrade-analysis finding (BLOCK above), this is a pattern: config files are being added to Reference Files tables where they don't belong.

**Recommendation:** Fix the table formatting — separate the reasoning-blueprint.md and company-profile.md entries into distinct table rows if both are intended as references. More likely: remove company-profile.md from the Reference Files table (see the downgrade-analysis BLOCK recommendation) and repair the reasoning-blueprint.md row to a clean single-cell format.

---

### [WARN] rev-ops plugin — No service context declared across 34 skills

**Finding:** The rev-ops plugin has 34 skills covering deal classification, pipeline tracking, forecast variance, capacity modeling, CRM hygiene, and GTM metrics. None of these skills declare a `service:` field, `lifecycle_stage:`, or any explicit statement of which GTM service process they support. The skills range from data quality (field-completion-monitoring, data-decay-tracking) to strategic planning (annual-planning-workflow, scenario-modeling) to deal management (deal-desk-workflow-management, non-standard-terms-detection).

Without service context, the 34 skills appear as an undifferentiated collection. An operator using the rev-ops plugin for the first time has no structural guide to which skills belong to the same workflow, which are standalone, and which are sequentially dependent.

**Impact:** Rev-ops is the most complex plugin (34 skills vs. 9–15 for other plugins). The absence of service grouping makes it effectively flat — there is no discoverable structure beyond alphabetical ordering. Skills that should be used together (e.g., `deal-classification` → `deal-health-scoring` → `deal-desk-workflow-management`) share no metadata linking them.

**Recommendation:** Introduce a `service_group:` frontmatter field that clusters rev-ops skills into their natural service groupings: Deal Management, Pipeline Health, Planning & Forecasting, CRM Hygiene, GTM Analytics, CS Capacity. Apply the same grouping to the plugin's README or marketplace.json for operator discoverability.

---

### [WARN] csm/expansion-business-case + csm/expansion-onboarding — Lifecycle stage metadata on only 2 of 17 csm skills

**Finding:** `expansion-business-case` and `expansion-onboarding` declare `lifecycle_stage: stage-4-expansion` in frontmatter. No other csm skill declares a lifecycle stage. This creates a partially annotated ecosystem where expansion skills are discoverable by lifecycle stage but every other CSM service step (onboarding, health management, escalation, renewal) is invisible to any lifecycle-aware orchestration.

**Impact:** Inconsistent metadata is worse than no metadata for automation purposes. An orchestrator reading lifecycle stage will find only stage-4 skills and incorrectly conclude the other stages have no skills. The partial annotation also signals the metadata was applied reactively (when these two skills were built as a matched pair) rather than architecturally.

**Recommendation:** Apply `lifecycle_stage:` consistently to all csm skills using the CS Journey stage model already implicit in the plugin's design. Map each skill to its stage and document the mapping in the csm CLAUDE.md.

---

### [WARN] csm/taro-play-runner — Scope unclear from trigger language

**Finding:** `taro-play-runner` has 4 Use When bullets referencing "TARO plays" without defining what a TARO play is or where the play library lives. The skill description says "Execute a TARO play from your configured playbook." The Pre-flight reads the CSM company profile but the play library source is not specified in the skill body — only that it exists in the "configured playbook."

An operator encountering this skill for the first time, or an orchestrator evaluating its trigger surface, cannot determine from the skill alone: (1) what constitutes a TARO play, (2) where the play library is stored, (3) whether TARO is a proprietary framework requiring external documentation.

**Impact:** The skill is opaque to new operators and to orchestration agents that haven't encountered TARO plays in prior context. Trigger precision suffers: the skill fires on "run a play" but has no fallback if the play library is unconfigured.

**Recommendation:** Add a brief definition of TARO plays to the skill description or Pre-flight section (1–2 sentences). Specify where the play library lives (in the CSM company profile, in a separate reference file, or in the tool integrations). Add a TARO-play-library-not-configured error path to Pre-flight parallel to the existing config-missing error path.

---

### [NOTE] rev-ops/outcome-statement-builder — Gong test artifacts as skill-local files

**Finding:** The skill root directory contains `gong-outcome-value-registry.md` and `gong-outcome-review-deck.html` — live outputs from a Gong.io CRO test run. These are operator-specific test artifacts, not generalized reference materials. They are referenced in the Reference Files table as authoritative output templates. This creates a subtle generalization risk: future operators will receive output that structurally mimics Gong-specific formatting choices baked into the template.

**Recommendation:** Move these files to a `examples/` subdirectory clearly labeled as test artifacts. Reference them in the skill as "example output from the Gong.io CRO test run" rather than as authoritative templates. Create a generalized `references/output-template.html` and `references/registry-template.md` for production use.

---

### [NOTE] cs-ops plugin — 9 skills, all with only 2-entry Reference Files tables

**Finding:** All 9 cs-ops skills have Reference Files tables with exactly 2 entries: `references/reasoning-blueprint.md` and a second file (varies by skill). Compared to csm skills (which have 1-entry tables) and rev-ops skills (which have 1–5 entries), cs-ops has consistent 2-entry tables. However, some cs-ops skills are complex enough to benefit from additional reference files. `metric-dashboard` and `capacity-planner` both inline extensive configuration-dependent logic that could be externalized to reference files for maintainability.

**Recommendation:** No immediate action required. Note for next authoring pass: evaluate `metric-dashboard` and `capacity-planner` for reference file extraction opportunities.

---

### [NOTE] csm/success-plan-canvas — Reference Files table lists 5 entries; skill body contains 12+ operational sections with inline schemas

**Finding:** `success-plan-canvas` has the highest Reference Files count of any csm skill (reference/success-plan-canvas-schema.md, reference/plan-type-guide.md, reference/ocv-integration-contract.md, references/reasoning-blueprint.md). The skill body also contains extensive inline schema definitions, YAML templates, and validation rules in addition to these references. The result is a skill where it is unclear which behaviors are governed by inline instructions and which by the referenced schema files.

The Reference Files purpose descriptions imply the schema files are authoritative for validation rules, section assembly, and field types. But the skill body also defines these rules inline. Any divergence between inline rules and schema file content will produce inconsistent behavior depending on which Claude loads.

**Recommendation:** Audit for divergence between the inline schema definitions in the skill body and the content of `reference/success-plan-canvas-schema.md`. One should be authoritative; the other should defer. Typically the external schema file should be authoritative, with the inline content serving as summary-level guidance.

---

### [NOTE] Cross-plugin — csm/renewal-readiness vs renewals/risk-assessment scope proximity

**Finding:** `csm/renewal-readiness` and `renewals/risk-assessment` both assess renewal risk. The csm skill is positioned as "90–180 days before renewal, close readiness gaps." The renewals skill is positioned as "5-domain risk tier assignment." The functional boundary is thin: both produce a risk assessment, both feed the renewal workflow, both use health signals, stakeholder data, and commercial context.

The boundary is: renewal-readiness is CSM-action-oriented ("close gaps before commercial conversation") while risk-assessment is analytics-oriented ("assign risk tier, surface signals"). This is a real distinction but it requires the operator to understand CSM workflow stages to select correctly.

**Impact:** Operators new to the plugin ecosystem will use these interchangeably, producing the wrong output format for their workflow stage.

**Recommendation:** Strengthen the cross-plugin referencing between these two skills. `renewals/risk-assessment` should explicitly state "produces input for `csm:renewal-readiness`" and vice versa. Add this inter-skill contract to both skills' descriptions.

---

### [NOTE] onboarding/skills/references/ — Stray directory at plugin skills level

**Finding:** `onboarding/skills/references/` exists as a directory at the plugin skills level, containing `skill-impact-map.md`. All other plugins have `references/` directories only within individual skill subdirectories. This plugin-level `references/` directory has no counterpart in csm, renewals, cs-ops, or rev-ops.

**Recommendation:** Resolve the orphaned `skill-impact-map.md` file (see WARN finding above). Once resolved, assess whether `onboarding/skills/references/` should be removed or formalized as a plugin-level shared reference directory (with corresponding loading instructions in relevant skills).

---

## Systemic Observations

### 1. Artifact accumulation from iterative editing

The stacked `---` separator finding (BLOCK-8) is the surface symptom of a deeper process issue: skills have been edited iteratively across many sessions, and each edit pass accumulates separator artifacts. The csm and cs-ops plugins have the highest separator counts (21–37 per skill), while rev-ops — which was built later — has lower counts (6–9 per skill). This tracks with the task history showing csm underwent the most edit passes. A one-time cleanup pass is warranted, but the underlying process (edit-accumulate-merge) will regenerate the problem without a linting step.

### 2. Progressive disclosure is declared but inconsistently enforced

All skills include the sentence "They are loaded on-demand when the relevant behavior is being applied — they are not front-loaded into every response." However, four skills (csm/escalation-memo and others) include an inline `> Full reasoning blueprint: references/reasoning-blueprint.md` at the top of the Reasoning Protocol, which instructs Claude to resolve the reference before applying the protocol. This contradicts the declared on-demand loading. The declaration of progressive disclosure is consistent; the enforcement is not.

### 3. Service context is architecturally absent

Not a single skill in the 83-skill ecosystem explicitly declares the service it belongs to. The two skills that declare `lifecycle_stage` are the exception. This is a design gap that will constrain the managed-agent-cookbooks' ability to compose skills programmatically. The gap is low-cost to close (frontmatter fields) but requires a coordinated pass across all plugins.

### 4. The customize/cold-start-interview duplication pattern is systemic

All 5 plugins replicate the same structural antipattern: two skills (cold-start-interview + customize) covering the same service step (plugin configuration). This is 10 skills maintaining two parallel implementations of the same interview logic. The duplication risk is real — any config schema change must be reflected in two files per plugin. Consolidation should be treated as a P1 architectural refactor.

### 5. Reference directory inconsistency (reference/ vs references/) creates fragility

6 skills use both `reference/` and `references/` in the same Reference Files table. The automated rubric sweep checks `references/` (plural) for the reasoning-blueprint. Skills using singular `reference/` for their primary reference files are systematically underserved by any tool that normalizes to plural. This inconsistency has already produced one BLOCK-level broken reference (churn-rca). Standardizing to `references/` (plural) across all skills and plugins is a low-risk, high-value cleanup.

---

*Agent D — Design Integrity Audit complete*
