# Candidate Review and Research Snapshot Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for sequential integration and superpowers:dispatching-parallel-agents for independent source investigations within Task 1. Track each step below.

**Goal:** Adjudicate all 34 current pending candidates, recheck four qualified published records, then preserve a checked citable dataset snapshot.

**Architecture:** Append actual dated decisions and evidence without changing the seven-entity schema, admission rules or public UI. Root integrates separately prepared source investigations; each unresolved item receives a concrete reopening condition. Freeze an unused version at the exact checked source commit after integration.

**Tech Stack:** Canonical JSON, Python validation/SQLite, Astro, GitHub Actions and Releases.

**Spec:** User-approved sequence 1, 2, 3 in this conversation; CONTRIBUTING.md; docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md.

## Global constraints

- English public repository and website; coverage cutoff remains 2026-09-04.
- Baseline commit 39c715948ee67d7071383c02b813d85c13b64c12: 192 published, 188 expanded verified, four qualified published, 34 unpublished pending.
- Keep all existing IDs/routes, prior decisions, evidence actors and timestamps; do not overwrite v0.1.0.
- Published drafts are eligible only with accurate status. Exact issue/publication correspondence and primary-source attribution remain required.
- No automatic concept/policy coding, schema changes, UI redesign, new licence, DOI or external correspondence.
- Work in the existing authorised checkout on maintenance/candidate-review-snapshot.
- A completed review can retain pending decisions; access failure is not grounds for exclusion.

## Task 1: All 34 pending candidates

**Files:** Read research/corpus-inventory.json and prior evidence ledgers. Create research/reviews/2026-09-06-candidate-snapshot/candidate-decisions.json, source-checks.json and report.md. Modify individual data/documents, data/sources and only evidenced dependencies. Test tests/test_candidate_snapshot.py.

- [x] Verify clean source baseline and existing test suite.
- [x] Freeze the exact 34 baseline IDs and before-images before changing inventory.
- [x] Investigate eight health/finance, six sector reports, twelve legacy date holds, and eight horizontal/history candidates in non-overlapping groups; retain actual queries, primary locators, captures/failures and dates.
- [x] Independently check every proposed admission against primary evidence, canonical duplicates, schema and publisher/author distinctions.
- [x] Write failing regression tests for the explicit admitted IDs, preservation of 192 old IDs and all prior candidate decisions, unresolved-candidate exclusion and field-specific corrections. Run them before integration.
- [x] Append prior decisions to history, record included/merged/excluded/pending outcomes for all 34, and integrate only fully evidenced documents and dependencies.
- [x] Run targeted inventory/admission tests and exports. Do not proceed to Task 2 until all 34 have a recorded outcome.

## Task 2: Four qualified published records

**Files:** Read research/reviews/2026-09-06-release-closure/retained-records.json. Create research/reviews/2026-09-06-candidate-snapshot/retained-records.json. Modify canonical records only on materially new positive evidence; extend tests/test_candidate_snapshot.py for any promotion.

- [x] Recheck the standardisation request, two July GPAI records and Council ST 12206/22 INIT against their exact unresolved requirements.
- [x] Preserve dates and prior assessments. Record evidence or no-change disposition plus the concrete reopening trigger for each record.
- [x] Upgrade only when every required fact is resolved; otherwise retain transparent qualifications.
- [x] Run full Python suite and validate generated JSON/SQLite integrity and foreign keys.

## Task 3: Checked research snapshot and publication

**Files:** Create docs/releases/v0.2.0.md after confirming the tag is unused; update CITATION.cff to the new release version/date. Preserve v0.1.0 documentation. Release artefacts are generated outside tracked source.

- [ ] Record exact current counts, cutoff, decisions, qualification and annotation limits in release documentation; do not claim exhaustive EU coverage.
- [ ] Run script-language guard, diff checks, complete tests and independent source/diff review; resolve material findings.
- [ ] Publish through PR, obtain passing website/browser CI, merge and verify deployed commit and live data.
- [ ] Create unused v0.2.0 tag/release at the checked commit; attach JSON, SQLite, manifest and checksums using a declared reproducible build timestamp.
- [ ] Independently download/hash the release assets and verify semantic data counts, tag commit and unchanged v0.1.0.
- [ ] Deliver the three-stage results, snapshot link and any remaining specific evidence gaps.
