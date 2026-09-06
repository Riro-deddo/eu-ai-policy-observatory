# Three-record admission implementation plan

> **For agentic workers:** Use superpowers:subagent-driven-development for the bounded data task and its independent review. Do not commit, push, merge or deploy: the user requested local admission first.

**Goal:** Admit the evidence-ready JURI report and NDSG v2.0 together with its v1.4 predecessor, while retaining the scientific-opinion hold.

**Architecture:** Append English canonical JSON records and update the live inventory with preserved decision history. Keep all previous audit bundles as historical records; generate SQLite and JSON using the unchanged validated pipeline.

**Tech Stack:** Canonical JSON, JSON Schema, Python pipeline, SQLite and existing Node tests.

**Spec:** `docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md`; `docs/superpowers/specs/2026-09-04-comprehensive-eu-ai-document-corpus-design.md`; `research/verification/2026-09-06-remaining-three/README.md` and the three linked memos.

## Global constraints

- Keep the seven canonical entities and all existing document IDs, slugs and URLs.
- All repository and public content remains English. Official metadata and editorial classifications remain distinct.
- Cutoff remains `2026-09-04`; use actual review timestamps. Keep the previous 181 documents and their existing review states unchanged.
- Preserve `chief-scientific-advisors-ai-science-opinion-2024` as pending and absent from published documents. Do not alter the 26 legacy holds or unrelated candidates.
- No schema, UI, application code or source-family completeness expansion. No installation, Git-state change, push, merge or deployment.
- Work in the existing user-scoped isolated directory. Its custom local Git metadata trails the deployed release; preserve the working files and do not reset, rebase or recreate the worktree.
- Use `apply_patch` for authored file changes. Existing generated outputs may be protected; a fresh explicitly named output directory is an acceptable delivery location.

## Task 1: Admit the three records and reconcile the inventory

**Files:**
- Create `data/documents/historical-juri-robotics-report-2017.json`.
- Create `data/documents/hma-ema-ndsg-workplan-2025-2028-v1-4.json`.
- Create `data/documents/hma-ema-ndsg-workplan-2026-2028-v2.json`.
- Create only necessary evidence sources/institutions/relationships in their existing `data/` directories. Reuse matching existing identities. Existing NDSG v2 source records may receive a documented verification-note/timestamp update; preserve prior retrieval facts.
- Modify `research/corpus-inventory.json`: reopen the two resolved candidates with their previous decision fields appended to `decision_history`; add the independently identified v1.4 candidate. Record the new metadata and linked canonical IDs.
- Modify `research/source-sweep.json` only to record the bounded follow-up and v1.4 scope; retain source statuses as incomplete and preserve the cutoff. Do not relabel the old frozen 53-candidate scope to silently include the predecessor.
- Create `research/admission/2026-09-06-three-record-admission/result.json` and `report.md` with the exact file manifest, changes, decisions, limitations and validation results. Preserve the earlier 53-candidate result and verification memos unchanged.

**Interfaces:** consumes the three evidence memos and current canonical 181-document baseline; produces 184 canonical published documents, including 158 expanded-verified and 26 unchanged legacy holds. The former three-candidate remainder resolves two IDs, retains one; v1.4 is one newly admitted dependency, not the third formerly pending candidate.

- [x] Capture a before-state file/hash manifest for canonical data, inventory and sweep before editing.
- [x] Review the evidence memos and comparable current records, including the date/provenance extension and controlled vocabulary.
- [x] Create the JURI record using `report`, `principal`, exact reference `A8-0005/2017`, procedure `2015/2103(INL)`, version `PE582.443v03-00`, issue `2017-01-27`, and publication `2017-01-27` explicitly meaning official parliamentary tabling. Preserve committee adoption `2017-01-12` separately. Keep resolution CELEX/OJ identifiers off this report. Add an evidenced procedural relationship to `civil-law-rules-on-robotics-resolution-2017` using a suitable existing type, and evidence-backed sectors/provenance. Do not split its six embedded opinions into records.
- [x] Create NDSG v1.4 and v2.0 as `work_programme`, `version`, non-binding institutional workplans. Use publication fallback `2025-07-22` for v1.4, with cover issue `2025-07` at month precision; do not give v1.4 the lineage's May first-publication date or March original-adoption date. Use publication fallback `2026-03-09` for v2.0, with cover issue and NDSG adoption `2026-02` at month precision. Do not invent an 11 February final-adoption day. Preserve correct joint NDSG authorship and EMA hosting/publishing roles, and health/public-administration/research tags with specific locators. Add `v2.0 revises v1.4`, supported by the official catalogue and introduction. Document unrecovered earlier manifestations without inventing canonical parents.
- [x] Reconcile inventory/history and bounded source coverage using the same three IDs and evidence-backed metadata. Scientific opinion stays pending; a new dated follow-up report records the improved evidence without erasing its old decision.
- [x] Run existing structural, reference, inventory and historical-publication validation. Generate fresh output with `observatory.pipeline.run_pipeline(Path('.'), timestamp, output_root=...)`.
- [x] Verify exported document IDs exactly equal all 184 canonical published IDs; check the three new IDs, scientific-opinion absence, unchanged old documents/hold cohort, 158/26 review partition, cutoff, and SQLite `PRAGMA integrity_check` / `PRAGMA foreign_key_check`.
- [x] Run the complete existing Python suite once and Node source/unit tests against the fresh JSON where supported. Record any environment-blocked checks accurately; do not weaken assertions or change code to hide failures.
- [x] Generate the pair twice at the same timestamp and compare checksums. Have an independent reviewer inspect the task diff against the evidence and constraints before declaring local admission complete.

No new runtime feature or bugfix is planned, so this uses existing validation coverage rather than adding artificial failing tests. Any discovered code defect is a separate escalation, not authorization to redesign the application.

## Preflight review

One data task owns all canonical and inventory writes; the controller performs read-only evidence checks and validation coordination concurrently. No two implementers share file ownership. Exact dates are already resolved by the evidence memos and existing schema; no guessed field or pending scientific-opinion admission is required. Baseline files are preserved independently of the stale local Git index.
