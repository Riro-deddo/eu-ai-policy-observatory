# Fifty-three candidate verification and admission plan

> **For agentic workers:** Use superpowers:subagent-driven-development for bounded research handoffs and review; use superpowers:dispatching-parallel-agents for independent evidence groups. Root alone integrates shared canonical data. Steps use checkbox syntax.

**Goal:** Account for all 53 identities in the 6 September gap audit and append only candidates satisfying the existing publication/evidence gate.

**Architecture:** Keep the seven-entity canonical JSON database, existing schemas and atlas. Three independent research groups produce isolated admission bundles; root verifies the Commission group, reviews bundles, updates the inventory/source registry and applies ready records. Pending or excluded identities receive reasoned inventory decisions, never fabricated verification.

**Tech Stack:** Existing Python/jsonschema/SQLite pipeline, JSON research notes, Astro frontend verification; no new dependencies.

**Spec:** docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md and docs/superpowers/specs/2026-09-04-comprehensive-eu-ai-document-corpus-design.md.

## Global Constraints

- Keep the seven canonical entities: policy, document, event, concept, institution, relationship and source.
- Preserve existing document IDs, slugs and URLs.
- Keep one canonical dataset, one generated SQLite database and one public JSON export.
- Keep the six English pages. No unrelated visual redesign is included.
- Keep official facts distinct from researcher classifications.
- Publication cutoff remains 2026-09-04. Use actual retrieval/review timestamps, never backdate.
- Unknown classifications must not receive cross-sector or authored-origin defaults.
- Official publication, not final adoption, is the eligibility threshold. Drafts need explicit version status and evidenced relationships.
- No merge, push or deployment in this request. Use the already approved isolated repository and explicit Git metadata work/sdd-gitmeta. Do not create another worktree or overwrite unrelated work.
- Preserve protected generated artifacts; generate the authoritative verified pair into work/gap-admission-20260906/final and supply it to the existing web loader override. Earlier output/repeat directories are retained scratch results only.
- All edits use apply_patch. Research agents may write only their own bundle/report, never shared canonical files, and may not spawn agents.
- AI-assisted checks remain truthfully recorded in research provenance; preserve existing public display attribution behavior.

## Task 1: Freeze queue and verify baseline

Files: research/discovery/2026-09-06-gap-scan/audit.json (read-only); research/admission/2026-09-06-gap-admissions/progress.md (create).
- [x] Confirm canonical baseline 131 and prior review states 105 verified / 26 pending.
- [x] Resolve 33 new main candidates plus 20 old backlog; exclude all uncounted follow-up arrays and unrelated 12 inventory holds.
- [x] Run existing Python baseline suite in a new task-owned temporary directory: 404 passed, 1 skipped.
- [x] Record all 53 stable input IDs and worker allocation in the progress/result ledgers.

## Task 2: Independent evidence review and admission bundles

Create research/admission/2026-09-06-gap-admissions/{historical,rights,sectoral,commission-base,commission-experts}.json. A separate recovered.json records the later successful FP5 and Frontex recoveries without rewriting the original handoffs.
Consume current gap handoffs and previous discovery file. Produce JSON with records, sources, institutions, relationships, decisions and evidence_log arrays.
- [x] Historical: six new historical plus three outstanding historical candidates.
- [x] Rights: eleven new rights candidates plus prior EP military/international-law, Frontex AI capabilities, EPRS borders and EU-OSHA worker-management reports.
- [x] Sectoral: eight new sectoral plus thirteen remaining prior agency candidates.
- [x] Commission: eight new Commission/research/infrastructure candidates.
- [x] Retrieve primary official English texts and date/attribution metadata. Seek equivalent official manifestations for failed URLs; never bypass access restrictions. Unresolved retrievals are explicitly pending.
- [x] Verify exact identity, dates, publication before cutoff, institutional/bibliographic attribution, substantive relevance, each sector/provenance tag and required parent/version links for admissions. Preserve three unresolved candidates outside canonical data.
- [x] For ready candidates construct existing-schema records with fully specific citations. For every other candidate record pending/excluded and exact reason. Do not broaden the schema.
- [x] Review the insurance factsheet under existing substantive-document criteria; no automatic inclusion or exclusion merely from its length.
- [x] Each group self-checks bundle JSON, exact allocation count, IDs and evidence completeness, then returns its report for independent review.

## Task 3: Reviewed canonical integration

Create data/documents/<ready-id>.json, data/sources/<evidence-id>.json and required institution/relationship records. Modify research/corpus-inventory.json and research/source-sweep.json only for this bounded batch. Create research/admission/2026-09-06-gap-admissions/result.json and report.md.
- [x] Root reviews candidate decisions and evidence, not merely schema acceptance. Resolve disputed dates conservatively.
- [x] Merge isolated bundles, reject collisions and preserve existing records byte-for-byte.
- [x] Register missing source families with honest in_progress/gap_found/recheck_due states; do not certify a completed source census.
- [x] Add an inventory disposition for every 53 identity, including explicit pending/excluded decisions.
- [x] Run existing schema/cross-record/historical-publication/inventory gates and fix data defects without weakening validators.
- [x] Obtain independent batch review; resolve important issues before generating final artifacts.

## Task 4: Generate and verify

No frontend behavior changes are planned.
- [x] Run pipeline twice with the same build timestamp into separate new output directories; compare JSON/SQLite bytes and inspect SQLite integrity/foreign keys.
- [x] Run full Python suite and relevant web unit/source tests. Worker Python: 404 passed, 1 skipped; root Python: 402 passed, 1 skipped, 2 protected-file access failures. Node: 65 passed.
- [ ] Production build, Vitest and fresh public-build scanner: blocked by Windows directory permissions; no rendered-site or browser end-to-end success claimed.
- [x] Run English guard and document environmental limitations. Final documentation is included in the delivery recheck.
- [x] Final report reconciles all 53 as included/merged/excluded/pending, gives resulting local export count and paths, and states no deployment occurred.

## Preflight

The research groups share read-only schemas and input discovery notes but write disjoint bundles. Root exclusively writes inventory, source registry and canonical records. Existing26 review holds are outside this task. No new research-core membership, synthetic policy relations or future events are introduced.
