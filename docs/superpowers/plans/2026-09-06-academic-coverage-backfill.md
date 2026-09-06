# Academic Coverage Backfill Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for coordinated execution and dispatching-parallel-agents for independent read-only source investigations. Steps use checkboxes for tracking.

**Goal:** Reassess the published database against its academic evidence contract, document coverage gaps and admit a bounded batch of genuinely omitted, fully evidenced documents.

**Architecture:** Preserve the v0.1.0 tag and existing canonical identities. Separate whole-corpus structural checks from sampled substantive source review; retain reproducible search logs and explicit candidate decisions. Integrate only verified factual corrections and evidence-ready additions.

**Tech Stack:** Canonical JSON, Python/JSON Schema/SQLite, Astro and existing GitHub CI.

**Spec:** User-approved coverage-backfill request in this conversation; CONTRIBUTING.md and docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md.

## Global constraints

- English repository and public site; seven canonical entities and existing UI structure.
- Coverage cutoff remains 2026-09-04. Actual discovery/review timestamps are not backdated.
- Published official drafts may qualify, but must never be described as adopted law.
- Preserve official issue, publication, adoption, registration and retrieval date meanings.
- Retain all 187 existing IDs/routes and prior candidate decisions; substantive corrections require explicit evidence and an audit trail.
- No inferred authorship, automatic cross-sector tags, fabricated human sign-offs, completeness claims or lowered evidence gates.
- Four retained published holds and twelve candidate holds are not reopened without materially new evidence.
- v0.1.0 stays unchanged. No new DOI, licence, LLM experiments or UI redesign.
- Reuse the current checkout as previously authorised, on maintenance/academic-coverage-backfill.

## Task 1: Baseline and scholarly audit

**Files:** Read data/, schema/, research/source-sweep.json, research/corpus-inventory.json, docs/data-dictionary.md and the v0.1.0 disclosures. Create research/audits/2026-09-06-academic-coverage-review.md.

- [x] Verify clean baseline and run the complete existing Python suite.
- [x] Calculate whole-corpus counts by date, institution, level, sector, relevance and source family; distinguish counts from verified search coverage.
- [x] Independently inspect methodological claims, attribution, dates, identities, relationships and annotation limits. Record the exact substantive sample and its selection rule.
- [x] Report concrete defects with sources and severity; distinguish already disclosed limitations from newly discovered problems.

## Task 2: Bounded discovery and admissibility

**Files:** Create research/discovery/2026-09-06-academic-backfill/search-log.json and candidate-evidence.json; update research/source-sweep.json and research/corpus-inventory.json only for actual investigations and decisions.

- [x] Investigate health/finance, employment/migration/transport/defence, and historical/horizontal EU AI sources independently.
- [x] Save exact queries or navigation paths, inspected result URLs, scope, stopping rules, timestamps and access failures. A ranked web search is not an exhaustive institutional catalogue search.
- [x] Deduplicate against canonical records and all inventory decisions before admission.
- [x] Verify exact English originals, identifiers, publication and issue dates, document status, author/commissioner/publisher distinctions and positive sector/relevance evidence.
- [x] Decide included, merged, excluded or pending with a reason. Every proposed admission requires a fully evidenced record and dependencies; unresolved candidates remain unpublished.

## Task 3: Evidence-backed integration

**Files:** Add individually named data/documents/*.json and data/sources/*.json; add institutions/relationships only where evidenced. Create research/migrations/2026-09-06-academic-backfill.json and tests/test_academic_backfill.py.

- [x] Select the evidence-ready batch from Task 2 and record its exact IDs in the migration ledger before editing canonical data.
- [x] Add regression tests that reject loss of old IDs/history, missing required citations, wrong date meanings and accidental promotion of unresolved candidates.
- [x] Make narrowly scoped data additions/corrections and register their source scopes without marking partial searches complete.
- [x] If a code defect is found, reproduce it with a failing test before the minimum fix; do not redesign the schema to fit a difficult record.
- [x] Run inventory, publication-boundary, historical-evidence and full Python tests; build exports to a separate audit directory.

## Task 4: Review and delivery

**Files:** Update the dated audit and migration reports; preserve prior release documentation.

- [x] Obtain independent read-only review of the complete data/code diff and reconcile consequential findings.
- [ ] Verify English text, source/candidate consistency and canonical preservation; obtain passing existing website and browser CI.
- [ ] Publish through a checked PR and confirm deployed commit under the user's standing project authorisation.
- [ ] Report actual additions/corrections, remaining gaps and the limits of this bounded audit. Do not call the EU-wide database complete.
