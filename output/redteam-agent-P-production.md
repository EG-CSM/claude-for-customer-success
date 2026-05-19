# Agent P — Production Hardness Report
*claude-for-customer-success plugin ecosystem | 2026-05-19*

---

## Summary

- **Skills audited:** 82 across 5 plugins (csm: 16, renewals: 12, cs-ops: 9, onboarding: 9, rev-ops: 36)
- **Findings:** 4 BLOCK / 18 WARN / 11 NOTE
- **Audit scope:** Token economics, observability, fallback handling, error handling, context window assumptions, reference file integrity

The ecosystem is structurally sound in its happy path. Pre-flight gates, G-code guardrails, staleness flags, and reviewer notes are consistently present across all 82 skills — this is not a neglected codebase. The production failures live at the seams: missing reference files that skills declare but cannot load, config-write operations with no failure handling, a test artifact shipped in the skill root, and silent degradation patterns in the onboarding and renewals plugins when live data is unavailable.

---

## Findings

---

### [BLOCK] rev-ops/unit-of-growth-calculator
**Failure mode:** Reference File — Broken Reference at Runtime  
**Finding:** The skill's `## Reference Files` table declares `references/benchmark-library.md` as the source for all benchmark defaults, imbalance signal thresholds, and source-cited comparisons. The file does not exist. The directory contains `references/benchmarking-research.textClipping` — a macOS metadata artifact, not the referenced markdown file. Any operation that requires benchmark defaults (the core function of this skill) cannot load the reference, and Claude will either hallucinate benchmarks or produce output with no citations.  
**Production scenario:** 3am: RevOps director runs unit-of-growth-calculator to prep for board meeting. The skill produces NRR benchmark comparisons without citing sources because the benchmark library cannot be loaded. Output looks authoritative. Director presents fabricated benchmarks to the board.  
**Recommendation:** Rename `benchmarking-research.textClipping` to `benchmark-library.md` or create the missing markdown file. Until the file exists, add a pre-flight guard that halts and alerts: "Benchmark library not found at `references/benchmark-library.md` — install complete to use this skill."

---

### [BLOCK] rev-ops/outcome-statement-builder
**Failure mode:** Observability — Test Artifact Shipped in Production Skill Root  
**Finding:** The skill root contains `gong-outcome-value-registry.md` (276 lines, Gong.io CRO segment data, Status: Draft) and `gong-outcome-review-deck.html` (911 lines, full HTML branded deck). These are live test-run artifacts from skill development. The `## Reference Files` table instructs Claude to use these files as "the visual and structural template for all HTML deck outputs — match the layout, color treatment, card structure, and typography exactly." Every output this skill produces will be templated against Gong.io-specific content: CRO segment framing, Gong product language, and a "TBD magnitude" placeholder convention that may bleed into non-Gong customer deliverables.  
**Production scenario:** Customer Success Manager at a healthcare SaaS company runs outcome-statement-builder. The output inherits structural framing from a Gong.io sales intelligence template: wrong value chain vocabulary, wrong segment framing, wrong review deck layout. If the CSM doesn't catch it, a Gong-flavored outcome registry goes to their customer.  
**Recommendation:** Move `gong-outcome-value-registry.md` and `gong-outcome-review-deck.html` to a `examples/` subdirectory and update Reference Files to label them as examples, not templates. Alternatively, create neutral template files and retire the Gong artifacts from the skill root entirely.

---

### [BLOCK] onboarding/customize
**Failure mode:** Reference File — Path Mismatch, Silent Degradation  
**Finding:** The skill declares `references/skill-impact-map.md` in its `## Reference Files` section and cites it twice in the body for critical output formatting and section-by-section field reference. The file exists at `onboarding/skills/references/skill-impact-map.md` (a shared directory one level up), not at `onboarding/skills/customize/references/skill-impact-map.md` where the skill will look for it. No fallback behavior is specified if the file is absent. When Claude cannot load the skill-impact-map, the downstream skill impact section of `--validate` output will be incomplete — users will see configuration gaps but not which downstream skills those gaps block.  
**Production scenario:** A new CS manager runs `/onboarding:customize --validate` to check their config before going live with the first cohort. The validation output lists `[✗ Missing]` fields but cannot map them to affected skills (graduation missing blocks handoff-doc, escalation matrix missing blocks blocker-review). They proceed without understanding which onboarding skills are non-functional. First customer kickoff fails because handoff-doc can't generate.  
**Recommendation:** Either copy `skill-impact-map.md` into `onboarding/skills/customize/references/`, or update the Reference Files path to `../references/skill-impact-map.md` to resolve to the shared location. Add an explicit fallback: if the file is not found, degrade gracefully and note which sections of validate output are incomplete.

---

### [BLOCK] All config-write skills (5 cold-start-interviews + 5 customize skills)
**Failure mode:** Error Handling — No Filesystem Write Failure Handling  
**Finding:** All 10 config-write skills (cold-start-interview and customize across csm, renewals, cs-ops, onboarding, rev-ops) confirm writes and report timestamps, but none specify what happens when a filesystem write fails. The write protocol in every skill follows the same pattern: (1) display proposed config, (2) get confirmation, (3) write, (4) confirm with timestamp. Step 3 to step 4 has no error branch. If the write fails — permissions denied, disk full, path not found — the skill will either report a successful timestamp against a failed write, or generate a generic error the user cannot act on. The cold-start-interview skills that write two files (plugin CLAUDE.md + shared company-profile.md) have an additional partial-write exposure: if the first file writes successfully and the second fails, the config state is inconsistent across plugins.  
**Production scenario:** 3am: First install on a new machine. The `~/.claude/plugins/config/claude-for-customer-success/` directory doesn't exist yet. csm cold-start-interview writes the csm CLAUDE.md successfully (creating parent dirs) but fails on company-profile.md due to a path resolution edge case. The skill reports success. The next five plugins that run cold-start-interview each read company-profile.md, find it missing, and prompt for a full re-interview — or worse, proceed with placeholder defaults silently.  
**Recommendation:** Add an explicit failure branch to all write operations: "If the write fails, report the error and the exact path that failed — do not report success." For dual-write operations (csm cold-start writes both CLAUDE.md and company-profile.md), add: "If the second write fails, report the partial state explicitly and instruct the user to run the interview again to complete the setup."

---

### [WARN] cs-ops plugin (all 9 skills)
**Failure mode:** Observability — Missing Security & Permissions Section  
**Finding:** All 9 cs-ops skills (capacity-planner, cold-start-interview, customize, data-quality-check, health-model-review, metric-dashboard, playbook-auditor, process-doc, segment-analyzer) have no `## Security & Permissions` section and no `## Trust & Verification` section. The cs-ops plugin is primarily an analysis and configuration plugin with no outbound network calls, but the absence of explicit declarations means: (a) operators cannot confirm network access is restricted, (b) the cold-start-interview and customize skills write to the filesystem without declaring `filesystem_write: config files only`, and (c) cross-plugin security posture is inconsistent — the csm plugin declares full permissions blocks on every skill.  
**Production scenario:** An operator auditing the plugin before enterprise deployment checks all 9 cs-ops skills for network access declarations. Finding none, they cannot confirm the skills are restricted. They either block deployment pending clarification or make incorrect assumptions about network access scope.  
**Recommendation:** Add a `## Security & Permissions` block to all 9 cs-ops SKILL.md files. Minimum required: `network_access: none`, `filesystem_write: false` (or `config files only` for cold-start/customize), `subprocess_execution: false`, `dynamic_code_execution: false`. The cold-start-interview and customize skills that write config files need the explicit write scope declaration.

---

### [WARN] renewals/downgrade-analysis
**Failure mode:** Token Economics — Inline Load Instructions for Three Reference Files During Analysis  
**Finding:** The analyze operation step sequence contains three inline `load` directives:
- Line 113: `Load reference/downgrade-driver-taxonomy.md` for mixed-signal heuristics
- Line 260: `Apply the three-way classification (load reference/value-chain-failure-map.md)`
- Line 275: `Load reference/counter-proposal-framework.md` for the full lever catalog

These are operational instructions inside the execution steps, not deferred references. The three files total approximately 34KB (downgrade-driver-taxonomy: 8.8KB, value-chain-failure-map: 11.5KB, counter-proposal-framework: 14.3KB). For every `analyze` operation, all three are loaded into context before any output is produced. The skill body itself is 441 lines plus frontmatter. Combined context budget for a single downgrade analysis call is approximately 50-60KB before any account data is injected.  
**Production scenario:** A CSM runs downgrade-analysis on an account with extensive notes. The combined context of skill instructions + three reference files + account context approaches or exceeds available context for lower-tier model configurations, causing truncation of the counter-proposal framework or silent omission of the analysis structure. The output appears complete but is missing retention levers.  
**Recommendation:** The `## Reference Files` table at the bottom already states "loaded on demand during analysis generation — not front-loaded." Reconcile this with the inline `load` instructions by making the heuristics inline (the classification logic is already present in the skill body) and reserving the reference load for the counter-proposal catalog only, which is genuinely too large to inline.

---

### [WARN] renewals/churn-rca and renewals/downgrade-analysis
**Failure mode:** Error Handling — No Filesystem Write Failure Path  
**Finding:** Both skills write structured analysis files to `context/` (churn-rca writes `context/rca-[safe_account]-[YYYY-MM-DD].md`, downgrade-analysis writes `context/downgrade-analysis-[safe_account]-[YYYY-MM-DD].md`). The write protocols include sequence numbering and file derivation logic but no explicit failure handling. Downgrade-analysis Step 8 says "Write complete file to [path]. Confirm write succeeded. Return file path and DGA-ID." — but does not specify what to do if the write fails. churn-rca has no write failure branch at all. Given these are persistent records that downstream operations (update, export) depend on, a silent write failure leaves the skill reporting a DGA-ID that references a file that doesn't exist.  
**Production scenario:** The `context/` directory doesn't exist (first use on a new system). churn-rca attempts to write the RCA file, fails silently, reports a file path. CSM attempts `/renewals:churn-rca` with operation=export and a DGA-ID — the export operation scans `context/rca-*` for the ID and finds nothing. No record of the RCA exists.  
**Recommendation:** Add an explicit failure branch: "If the write fails, report the error and exact path. Do not return a DGA-ID or file path. Do not report success." Add pre-write validation: confirm `context/` directory exists or create it before writing. For the update operation in downgrade-analysis, confirm the source file exists before attempting append.

---

### [WARN] renewals/churn-rca and renewals/downgrade-analysis
**Failure mode:** Fallback — No Recovery Path When No Data Sources Are Available  
**Finding:** Both skills were identified in the "no fallback language" scan. Their Pre-flight sections confirm account context from the user (company name, churn date, ARR) and check company-profile.md for segment context — but neither specifies what happens when the user provides only partial inputs. churn-rca marks `churn_reason` as required but all other inputs as optional. downgrade-analysis marks `downgrade_request` as required. Neither skill has a "minimum viable input" section that defines what quality of analysis is possible with different levels of completeness, nor do they offer a degraded-output path with explicit confidence labeling for sparse inputs.  
**Production scenario:** CSM runs churn-rca with only account name and churn reason. No csm_name, no contract_value, no early_warning_signals. The skill produces a full-looking RCA with missing/defaulted fields but doesn't flag which sections are confidence-degraded vs. supported by data. The RCA is used for a cohort analysis that produces misleading signal patterns.  
**Recommendation:** Add an input completeness assessment at the start of the analyze operation: evaluate which optional fields are present, assign a data completeness tier (Complete / Partial / Minimal), and label the output accordingly. For Minimal inputs, explicitly state: "Analysis confidence is Low — contributing factors and timeline reconstruction are inferred from the churn reason alone."

---

### [WARN] onboarding plugin — blocker-review, handoff-doc, milestone-tracker, ttv-analysis
**Failure mode:** Fallback — Inconsistent "No Connector" Behavior  
**Finding:** These four onboarding skills have partial fallback handling. blocker-review, handoff-doc, and milestone-tracker each have an explicit "If no CRM" or "If no PM connector" prompt asking the user to provide the data manually. ttv-analysis requires "a PM connector with milestone completion data or a CSM-provided list." The gap is consistency: blocker-review says "If no CRM: 'Tell me the account name and which milestone you're currently trying to clear'"; milestone-tracker says "If no PM connector: 'Tell me: which milestone is currently active, what's the status'"; but none of these skills fully enumerate all the connector failure combinations (no CRM AND no PM connector, CRM returns empty, PM connector returns stale data). The reviewer note format handles staleness but not connector partial-failure.  
**Production scenario:** milestone-tracker is called with both CRM and PM connectors configured but the PM connector returns an empty task list (connection succeeded, no tasks found — valid response). The skill has no explicit handling for "connector returned empty results." It may proceed as if no data was retrieved, or it may prompt for manual input with a confusing message that contradicts the user's knowledge that their PM tool has data.  
**Recommendation:** Add a "Connector returned empty results" case to the data pull section of each affected skill: "If connector returned empty results (not an error — zero tasks/records found), prompt: 'Your PM tool returned no records. Confirm the account name is correct, or paste the current milestone status directly.'" This is distinct from "connector not configured" and "connector returned an error."

---

### [WARN] csm/expansion-business-case and csm/expansion-onboarding
**Failure mode:** Token Economics — Large Pseudocode Blocks in Active Skill Instructions  
**Finding:** Both expansion skills contain substantial Python pseudocode blocks that represent the logic contract. expansion-business-case contains code blocks including injection scanning patterns, safe_account derivation, version resolution, and template loading instructions. expansion-onboarding contains similar pseudocode for plan creation, update, and close operations including file write pseudocode with `open(file_path, 'w')` patterns. These are explicitly labeled "not executed at runtime" — but they still consume context tokens on every invocation. expansion-business-case is 796 lines; expansion-onboarding is 893 lines. These are the two largest skills in the ecosystem.  
**Production scenario:** A CSM runs expansion-business-case immediately after account-research in the same session. The session context already contains the account brief (~300-400 lines) plus the full skill body (796 lines) including all pseudocode. When the skill then loads `reference/expansion-proposal-template.md` or `reference/csql-package-template.md` on demand, the combined context approaches the ceiling of shorter-context model configurations.  
**Recommendation:** Consider extracting the pseudocode logic contracts to `references/logic-contract.md` with explicit "reference only — not executed" labeling, reducing the active instruction body to the operational steps. Alternatively, document the pseudocode in a companion spec file and replace inline pseudocode with concise procedural instructions. The current approach penalizes every invocation with the full logic contract in context.

---

### [WARN] rev-ops/gtm-unified-metrics-pulse and rev-ops/revenue-brief-generation
**Failure mode:** Token Economics — Multi-Connector Aggregation Without Context Budget Ceiling  
**Finding:** Both skills are aggregator patterns that pull from multiple connectors (HubSpot, CS platform, OCV catalog, Slack) and invoke or reference multiple source skills in sequence. revenue-brief-generation references "source skills" across pipeline, handoff quality, CS capacity, early churn, and outcome realization — each of which may in turn pull connector data. Neither skill specifies a context budget ceiling or a maximum data volume per connector pull. The fallback mode (labeled partial output when connectors unavailable) is well-designed, but the happy-path aggregate case has no guard against context overflow from large connector responses.  
**Production scenario:** Weekly pulse run on a portfolio with 200+ active deals in HubSpot and 50+ CS accounts flagged for early churn. HubSpot connector returns the full pipeline record set; CS platform returns all flagged accounts with full health history. The combined response volume exceeds the practical limit for coherent summarization, and the output either gets truncated silently or the model begins omitting sections without the reviewer note reflecting the truncation.  
**Recommendation:** Add explicit data volume guidance to the Pre-flight connector checks: "If HubSpot returns more than [N] records, summarize to top-line counts and flag the volume in the reviewer note rather than processing all records." This is a soft ceiling, not a hard stop, but it creates observable behavior when data volume is the constraint.

---

### [WARN] All cold-start-interview skills — dual-write state consistency
**Failure mode:** Error Handling — Cross-File Write Consistency Not Guaranteed  
**Finding:** csm, renewals, onboarding, and rev-ops cold-start-interview skills write two files: a plugin-specific CLAUDE.md and the shared company-profile.md. The write protocol in each skill confirms write of the plugin CLAUDE.md with a timestamp, then separately writes company-profile.md if it doesn't exist (or skips if it does). The two writes are sequential, not atomic. If the second write fails or is interrupted, the plugin CLAUDE.md exists (with `[PLACEHOLDER]` or default values referencing company-profile.md fields) but company-profile.md is absent or stale. Other plugins that run cold-start-interview next will skip the company questions (seeing company-profile.md exists) but inherit inconsistent data. cs-ops cold-start has a cross-consistency check that explicitly flags divergence from company-profile.md — but this check can only catch post-hoc inconsistency, not prevent it.  
**Production scenario:** User runs onboarding cold-start-interview. onboarding/CLAUDE.md writes successfully. company-profile.md write is interrupted (browser closed, context limit hit). The csm plugin is already configured; its cold-start detects company-profile.md exists, skips company questions. But the company-profile.md is from an older install with a different product name. All csm skills produce output calibrated to the old product until someone notices and re-runs the interview explicitly.  
**Recommendation:** After both writes complete, include a consistency check: "Verify onboarding/CLAUDE.md and company-profile.md agree on segment definitions, product name, and CS team size. If any field diverges, surface it explicitly before closing the interview." For any interrupted session, add: "Setup may be incomplete. Run `/[plugin]:cold-start-interview --check-integrations` to verify config state."

---

### [WARN] renewals/customize and renewals/cold-start-interview
**Failure mode:** Observability — GRR/NRR Targets Written Without Version or Effective Date  
**Finding:** renewals cold-start collects GRR/NRR targets and ARR figures with a requirement to flag Finance/RevOps review (G5). However, the configuration write protocol does not require an `effective_date` or `config_version` field on financial targets. When these values are updated via customize later, there is no audit trail of what the previous value was or when it changed. The current value in the config file at any point in time is the only source of truth.  
**Production scenario:** Renewals manager updates GRR target from 90% to 87% in October using customize. In December, the team reviews churn analysis outputs from August that referenced "configured GRR target" — but there is no record of what that target was in August. The retrospective analysis is anchored to the wrong baseline.  
**Recommendation:** Add `config_last_updated: [timestamp]` and `config_version: [N]` fields to the renewals CLAUDE.md template. When customize writes a financial target change, append the old value and timestamp to a `## Change Log` section before overwriting the active value.

---

### [WARN] onboarding plugin — 9 skills without security declarations
**Failure mode:** Observability — Inconsistent Security Posture Across Plugins  
**Finding:** The onboarding plugin's skill-level security declarations are non-uniform. blocker-review, handoff-doc, milestone-tracker, success-criteria, ttv-analysis, kickoff-prep, onboarding-plan, and cold-start-interview each have a `## Security & Permissions` section with a brief natural-language declaration ("No filesystem writes, no subprocess execution, no dynamic code execution"). However, this format differs from the structured key-value format used in the csm and renewals plugins (`filesystem_write: false`, `subprocess_execution: false`). onboarding/customize, which does write config files, has a structured format but cold-start-interview uses prose. The inconsistency makes automated security posture auditing unreliable.  
**Production scenario:** An operator scanning all 82 skills with a script looking for `filesystem_write: true` will miss any write capability declared in prose format only.  
**Recommendation:** Standardize all onboarding skill security declarations to the structured key-value format: `network_access:`, `filesystem_write:`, `subprocess_execution:`, `dynamic_code_execution:`. Align with the format used in csm and renewals plugins.

---

### [WARN] renewals/churn-rca — VALIDATE step not defined for required fields
**Failure mode:** Error Handling — Validation Gate Before Write Only Partially Specified  
**Finding:** churn-rca includes "Validation — enforce before any analysis or file write" at line 178, but the validation checks are not fully listed for the analyze operation. The operation table marks `account_name` and `csm_name` and `churn_reason` as `Required: Yes` — but the validation section doesn't explicitly state what error is returned for each missing required field, and doesn't specify whether the skill stops immediately on first missing field or accumulates all errors before stopping. For a skill that writes to the filesystem, unclear validation sequencing creates a risk of partial output being written before a late-discovered validation failure.  
**Production scenario:** User calls churn-rca with account_name and csm_name but omits churn_reason (accidentally). The skill begins constructing the RCA document — possibly even writing the file with partial content — before discovering that churn_reason is missing from a step that requires it mid-analysis.  
**Recommendation:** Add a pre-write validation gate that checks all required fields at the start of the operation, before any file path construction or analysis generation. Specify the error format explicitly: "Missing required field: [field_name]. Provide [description] to proceed."

---

### [NOTE] Ecosystem-wide — reasoning-blueprint.md physical files exist but are stubs
**Failure mode:** Token Economics — Reference File Content vs. Stub Risk  
**Finding:** The `references/reasoning-blueprint.md` files added across all 82 skills during the P1 authoring pass are physically present (verified). However, the file content for all recently-added skills (cs-ops, onboarding, renewals, rev-ops) was created as part of a batch scaffolding operation. The cs-ops skill blueprints are 611 bytes (stub size), while the csm expansion-business-case reasoning-blueprint is 14,174 bytes (substantive content). Skills that reference a reasoning-blueprint.md but find only a stub will derive no reasoning guidance from it — the reference label passes the rubric check but provides no production value.  
**Production scenario:** cs-ops/capacity-planner invokes its reasoning-blueprint.md during a complex portfolio capacity analysis. The blueprint is a stub. The skill produces generic reasoning without the domain heuristics and failure modes that a real blueprint would provide.  
**Recommendation:** Audit the reasoning-blueprint.md files added during the P1 pass for content adequacy. Any file under ~2KB is almost certainly a stub. Prioritize populating blueprints for skills with complex multi-step analysis (capacity-planner, metric-dashboard, playbook-auditor, data-quality-check).

---

### [NOTE] rev-ops/downgrade-analysis — reference/ vs references/ inconsistency
**Failure mode:** Reference File — Path Convention Inconsistency  
**Finding:** downgrade-analysis uses two different directory names for reference files: the analysis operation references `reference/value-chain-failure-map.md`, `reference/downgrade-driver-taxonomy.md`, and `reference/counter-proposal-framework.md` (singular), while the `## Reference Files` table at the bottom also lists `references/reasoning-blueprint.md` (plural). The actual files are split correctly across both directories (`reference/` has the three analysis files; `references/` has the reasoning-blueprint). The inconsistency doesn't cause a runtime failure because both directories exist with the correct files — but it creates maintenance confusion and any automated path-consistency tooling will flag this skill.  
**Recommendation:** Consolidate all reference files into one directory (`references/` preferred, matching ecosystem convention) and update all inline references from `reference/` to `references/`.

---

### [NOTE] onboarding/ttv-analysis — minimum sample size declared but not enforced pre-write
**Failure mode:** Error Handling — Soft Constraint Not Enforced  
**Finding:** ttv-analysis declares "Requires minimum 5 accounts with complete milestone data for meaningful analysis" for the `--patterns` mode. This is stated in the Use When section and again in the data pull section. However, there is no explicit Pre-flight or validation step that checks account count before running the pattern analysis. If a user runs `--patterns` with 2 accounts, the skill will proceed and produce pattern findings from a statistically meaningless sample, with no flag.  
**Production scenario:** New CSM runs `--patterns` on their 3-account book of business one month after joining. The skill produces "customers in the mid-market segment take 18% longer to complete M3" from three data points, presented without a statistical validity warning. This gets reported upward as a finding.  
**Recommendation:** Add a pre-flight check for `--patterns` mode: "Count accounts with complete milestone data before proceeding. If fewer than 5, stop and report: 'Pattern analysis requires at least 5 accounts with complete milestone data. Found [N]. Add more accounts or run single-account analysis instead.'"

---

### [NOTE] Ecosystem-wide — no rate limiting or retry guidance for MCP connector calls
**Failure mode:** Token Economics / Error Handling — No Guidance on Connector Failures vs. Rate Limits  
**Finding:** Skills that declare connector dependencies (CRM, CS Platform, call recording) have fallback behavior for "connector not configured" and "no data returned" cases. None specify behavior for rate limit responses (HTTP 429) or transient connector failures (HTTP 503). The fallback in most skills is "proceed with available data and flag the gap" — which is appropriate for missing connectors but conflates "connector unavailable" (permanent) with "connector temporarily rate-limited" (transient). A CSM who hits a rate limit will receive a brief labeled "CRM unavailable" that is stale, but the skill will not suggest retrying.  
**Recommendation:** Add a connector error categorization note to the data gathering section of connector-dependent skills: "If the connector returns a rate-limit error, note it explicitly and recommend retrying in 60 seconds rather than proceeding with degraded output." This is a NOTE rather than WARN because the current fallback still produces usable output — it just misses the retry opportunity.

---

### [NOTE] csm plugin — PROPOSED status on 14 of 16 skills
**Failure mode:** Observability — Status Signal Accuracy  
**Finding:** Of the 16 csm skills, 14 carry `[PROPOSED]` status and 2 carry `[VALIDATED]` (expansion-business-case and expansion-onboarding show `[VALIDATED]` after documented CSE runs). The `[PROPOSED]` status is accurate — these skills are complete and reasoned but have not been through a full runtime validation pass. This is not a defect; it correctly signals pre-VALIDATED state. Noted here for the synthesis report: the csm plugin should not be marked production-ready at the ecosystem level until the PROPOSED skills are promoted or explicitly accepted as deployment-grade PROPOSED.  
**Recommendation:** No immediate action required. Track PROPOSED-to-VALIDATED promotion as a separate quality gate milestone before enterprise deployment.

---

### [NOTE] rev-ops/outcome-statement-builder — gong HTML deck is 911 lines front-loaded as a template
**Failure mode:** Token Economics — Large Static Template in Skill Reference  
**Finding:** `gong-outcome-review-deck.html` is 911 lines of HTML. The skill instructs Claude to "match the layout, color treatment, card structure, and typography exactly" when generating HTML review decks. This file is loaded as a template reference — meaning its content enters context whenever an HTML deck output is requested. For every HTML deck generation call, approximately 15-20K tokens of HTML template are loaded before any analysis content. This compounds the BLOCK finding about the file being Gong-branded.  
**Recommendation:** Replace the 911-line branded HTML template with a minimal structural template (~50 lines) that defines the layout contract without Gong-specific content. The branded version can live in `examples/gong/` for reference.

---

### [NOTE] Ecosystem-wide — G-code references not cross-validated against plugin config
**Failure mode:** Observability — G-code Guardrails Not Verified Against Configuration  
**Finding:** G-codes (G1–G9) are referenced across 82 skills. The most-referenced are G5 (57 references — confidentiality), G7 (46 references — staleness), G1 (39 references — health as heuristic), G4 (34 references — expansion stays internal), G2 (33 references). These G-codes are defined in the CLAUDE.md config files per plugin, not in a shared registry. Skills in the cs-ops plugin reference G-codes (G1, G4, G7) without a security section — confirming the skills assume the CLAUDE.md config loads and provides the G-code definitions. If a CLAUDE.md config is absent or has `[PLACEHOLDER]` markers, the Pre-flight gate fires correctly, but the G-code guardrail definitions are never loaded. Skills that reference G-codes in their Reasoning Protocol and Guardrails sections are depending on the Pre-flight gate working correctly to ensure those definitions are present.  
**Recommendation:** Document the dependency explicitly: "All G-code guardrails in this skill depend on the config being loaded at Pre-flight. If Pre-flight halts, G-codes are undefined. Do not proceed with partial config." This is currently implicit; making it explicit improves debuggability.

---

## Production Hardness Assessment by Plugin

| Plugin | BLOCK | WARN | NOTE | Overall Hardness |
|--------|-------|------|------|-----------------|
| csm | 0 | 2 | 2 | Solid — happy path well-covered; gaps at edge cases only |
| renewals | 0 | 4 | 1 | Moderate — churn-rca and downgrade-analysis need write failure handling |
| cs-ops | 0 | 1 | 2 | Moderate — no security declarations; otherwise structurally sound |
| onboarding | 1 | 2 | 1 | Moderate — skill-impact-map path mismatch is a real user failure; connector edge cases incomplete |
| rev-ops | 3 | 9 | 5 | Needs attention — two BLOCK findings in production artifacts; downgrade-analysis token load; write handling gaps throughout |

---

## Top 5 Fix Priority

1. **[BLOCK] rev-ops/unit-of-growth-calculator** — rename `benchmarking-research.textClipping` to `benchmark-library.md`. 5-minute fix; eliminates a skill that currently cannot load its core reference.
2. **[BLOCK] rev-ops/outcome-statement-builder** — move Gong artifacts to `examples/` and create a neutral template. Prevents brand contamination in every customer-facing deck this skill produces.
3. **[BLOCK] onboarding/customize** — copy `skill-impact-map.md` into `onboarding/skills/customize/references/`. 1-minute fix; eliminates silent degradation in the validate operation.
4. **[BLOCK] All cold-start-interview / customize skills** — add explicit write failure branches. Prevents phantom config states that silently degrade all downstream skills.
5. **[WARN] renewals/downgrade-analysis** — resolve the inline load instruction vs. on-demand reference inconsistency. The three reference files (34KB combined) are loaded on every analyze call regardless of the "loaded on demand" footer claim.
