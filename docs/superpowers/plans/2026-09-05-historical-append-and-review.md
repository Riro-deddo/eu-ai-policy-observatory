# Historical Append and Existing-Record Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox syntax for tracking.

**Goal:** Append the evidence-ready historical batch to the existing database while activating evidence-bearing metadata and explicitly tracking the existing records' outstanding review.

**Architecture:** Keep the canonical seven-entity dataset and generate SQLite and public JSON from it. Compose the existing historical extension into the active document contract; retain only the frozen pre-existing document identities under an explicit compatibility review notice until their evidence upgrade passes. New admissions cannot use that exemption. This is a bounded delivery of the approved historical design, not certification of the entire source universe.

**Tech Stack:** Python, JSON Schema, SQLite, Astro, TypeScript; existing dependencies only.

**Spec:** docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md

## Global Constraints

- Keep the seven canonical entities: `policy`, `document`, `event`, `concept`, `institution`, `relationship` and `source`.
- Preserve existing document IDs, slugs and URLs.
- Keep one canonical dataset, one generated SQLite database and one public JSON export.
- Keep the six English pages: Home, Policy Map, Timeline, Corpus, Methodology and About. No unrelated visual redesign is included.
- Keep official facts distinct from researcher classifications.
- The publication cutoff remains `2026-09-04`; use actual retrieval/review timestamps, never backdate them.
- Unknown classifications must not receive cross-sector or authored-origin defaults.
- No merge, push or deployment in this plan. Preserve the current generated pair; verify with a separate output directory.
- All explicit Git commands use `git --git-dir=work/sdd-gitmeta --work-tree=.` in this existing isolated repository. Do not create another worktree, reset, clean, or stage unrelated untracked files.
- File edits use apply_patch; deterministic bulk mechanical transformations and provided skill scripts are permitted. No child agents from implementers or reviewers.

## Delivery interpretation and boundaries

The user approved doing historical additions and existing-record improvements together in the same database. The prior sequence that required completing all 117 reviews before any historical addition is replaced by an explicit, identity-bounded compatibility transition. Existing unresolved records remain visible with a review notice; the notice is not a verified classification. New records must pass the complete evidence gate. Three existing principal records are being independently checked and can graduate only on complete evidence.

Keep the existing frozen public-document baseline unchanged. Use its exact ID/slug pairs for preservation checks and compatibility eligibility, not its old content hashes as claims of new verification. Do not interpret its 117 records or the mutable `core` tier as an approved RP sample. Preserve the original seed selection as a versioned database seed subset, explicitly distinct from a researcher-approved PhD analytical sample.

Exact source language must survive mapping: add `no_longer_in_force` for an official status that does not itself prove repeal versus expiry; retain approved `repealed` and `expired` with evidence. Add bounded attribution roles `responsible_body`, `requester`, `supervisor`, `cover_note_sender` and additional-date kinds `official_end_of_validity`, `official_dispatch`, `parliament_adopted_text_manifestation` where supported. They must never become authorship by coercion. Hosting services remain source/publisher metadata unless there is an actual institution record.

The initial batch is the 14 `evidence_ready` historical rows in the immutable admission review. Held rows, the separately rechecked EESC opinion, FP7 and older search leads are outside this admission batch. Preserve those leads privately with their unresolved dispositions; no source-completeness claim follows from this batch. The full source matrix and remaining old-record evidence reviews remain separately measurable work, not silently marked complete.

### Task 1: Activate compatible evidence metadata and append the bounded batch

**Files:**
- Modify: `schema/record.schema.json`, `schema/historical-document-extension.schema.json`, `schema/controlled-vocabularies.json`, `schema/corpus-inventory.schema.json`, `schema/database.sql`.
- Modify: `src/observatory/validate.py`, `src/observatory/historical_readiness.py`, `src/observatory/build_db.py`, `src/observatory/export_public.py`, `src/observatory/pipeline.py`, `src/observatory/coverage.py`.
- Create: `src/observatory/historical_publication.py`, `tests/test_historical_publication.py`, `research/migrations/2026-09-05-historical-admissions.json`.
- Modify: `research/corpus-inventory.json`, `research/source-sweep.json`, `docs/historical-readiness.md` and relevant existing Python tests/fixtures where changed public contracts require it.
- Create canonical document/source/institution JSON files using exact proposed IDs in `research/staging/2026-09-05-historical-first-batch-mapping.md`.
- Modify only the evidence-ready members of the three existing documents described by `research/staging/2026-09-05-legacy-three-evidence.json` when that read-only research handoff arrives.

**Inputs:** Read `research/admission/2026-09-05-document-admission-review.json`, the mapping handoff, the existing frozen baseline, and the historical extension. Original admission/discovery snapshots are evidence inputs; do not rewrite their recorded past dispositions. Record current admissions in the new migration ledger and canonical inventory with decision history where applicable.

**Interfaces:**
- Existing `validate_records(data_root, schema_path, vocabulary_path)` continues to reject unknown properties and invalid base metadata.
- Add `validate_historical_publication(records, schema_root, publication_cutoff, baseline_path) -> list[ValidationIssue]` in the new module. Call it before generation. It validates every extended record using the evidence logic in `validate_historical_readiness`; non-extended published records are allowed only if their exact ID/slug appears in the frozen baseline. An extended record cannot silently fall back after a failure. Reject partial extension blocks. Avoid circular imports by moving or locally importing shared helpers deliberately.
- Public documents contain `historical_review_status: "verified" | "legacy_review_pending"`, nullable `temporal_collection`, `relevance_class`, `document_date_kind`, `date_evidence`, `legal_status_evidence`, plus `classification_evidence`, `bibliographic_authors`, `additional_dates`. Evidence-bearing institution role fields survive export. Missing legacy evidence remains null/empty, not invented.
- Store the scalar classifications in document SQLite columns and structured evidence in normalized supporting tables or a document-owned serialized metadata column; never create an eighth canonical entity. Every source ID embedded in evidence must resolve to a declared, published, verified official source before public export.
- Export `coverage.historical_review` counts keyed by `verified` and `legacy_review_pending`. Export a safe `coverage.source_scopes` array containing registered source ID/name/family/institution, bounded interval, type/sector scopes, scan status, cutoff and pending-candidate count. Empty scopes must mean unspecified, never all sectors.

- [ ] Write failing behavioral tests before implementation. Use the existing production pipeline, not a mock. Initial repository test:

```python
def test_historical_batch_round_trips_without_losing_old_routes(tmp_path):
    import json
    from pathlib import Path
    from observatory.pipeline import run_pipeline
    payload = json.loads(run_pipeline(Path.cwd(), "2026-09-05T12:00:00Z", output_root=tmp_path).public_json.read_text(encoding="utf-8"))
    docs = {row["id"]: row for row in payload["documents"]}
    baseline = json.loads(Path("research/migrations/2026-09-05-public-document-baseline.json").read_text(encoding="utf-8"))
    assert all(docs[row["id"]]["slug"] == row["slug"] for row in baseline["documents"])
    esprit = docs["council-decision-84-130-eec-esprit"]
    assert esprit["document_date"] == "1984-02-28"
    assert esprit["temporal_collection"] == "historical_lineage"
    assert esprit["relevance_class"] == "ai_related_precursor"
    assert esprit["date_evidence"]["publication_date"]["locator"]
    robotics = docs["civil-law-rules-on-robotics-resolution-2017"]
    assert robotics["document_date"] == "2017-02-16"
    assert robotics["publication_date"] == "2018-07-18"
    assert robotics["temporal_collection"] == "historical_lineage"
    assert sum(row["celex"] == "52017IP0051" for row in docs.values()) == 1
```

- [ ] Run the focused test with `.venv/Scripts/python.exe -m pytest tests/test_historical_publication.py -q`; record the expected missing-admission failure. Add gate mutations testing: unknown new legacy-like document rejected; partial extension rejected; evidence on pending/unverified/undeclared sources rejected; missing tag/date/role citations rejected; future publication rejected; historical identity duplicate rejected. A pre-1984 fully valid fixture must pass.
- [ ] Compose the schema rather than duplicating divergent rules. Remove the inventory's 2018 minimum without imposing a new historical anchor minimum; retain valid calendar/year and release-cutoff checks. Enforce the new evidence gate only after ordinary validation and before atomic generation. Existing fixture-only tests must use a deliberate fixture baseline or fully evidenced fixture; do not bypass the gate in tests.
- [ ] Append exactly the eligible historical rows from the evidence mapping, with canonical sources and period-correct bodies. Use only reviewed evidence URLs/locators and actual timestamps. Do not turn the staged summary into invented quotations. All new reviews identify `Codex (AI-assisted evidence review)`, not an unperformed personal review by Yichen Hao. Use full official identity/date/status evidence and per-tag citations. For truly unresolved contradictions keep a named hold and report fewer actual admissions rather than fabricate data.
- [ ] Register bounded historical source scopes as `in_progress` or `gap_found`, with explicit method and limits. Deduplicate against existing inventory rows by identifier/manifestation; update decisions with history or append where absent. Keep held candidate titles out of public exports. Finish the three existing-record upgrades only for entries marked fully evidence-ready; the remainder retain pending review notices.
- [ ] Generate twice into two unique scratch directories via `run_pipeline(..., output_root=...)`; compare bytes, inspect SQLite foreign-key/integrity checks and public JSON. Preserve the original generated pair. Update existing hardcoded inventory/corpus tests only to genuine new expected counts or meaningful derivations retaining the behavioral assertions.
- [ ] Run focused historical, validation, database, export, inventory and pipeline tests, then one full Python suite. Run the English production guard if available. Stage only task files and evidence inputs actually needed for reproducible admissions; commit locally with an English message. Write the report with exact counts, test commands/results, holds, generated paths and any concerns.

### Task 2: Display evidence review and historical collection in the existing atlas

**Files:**
- Modify: `web/src/lib/types.ts`, `web/src/lib/data.ts`, `web/src/lib/filter.ts`, `web/src/components/CorpusExplorer.astro`, `web/src/components/Timeline.astro`, `web/src/pages/corpus/[slug].astro`, `web/src/pages/methodology.astro`, and existing Home/About copy only where temporal claims need updating.
- Test: relevant existing `web/tests` unit/browser tests; create `web/tests/historical-metadata.test.mjs` for static rendered-contract assertions if needed.
- Modify documentation: this plan's completion notes and `docs/historical-readiness.md` to distinguish active new-admission validation from remaining legacy review and release gates.

**Interfaces:** Consume the exact Task 1 public document fields and `coverage.historical_review` / `coverage.source_scopes`. Do not rename these fields. Existing principal/all, sector/provenance, institution, concept, query and date controls keep their behavior.

- [ ] Read frontend-testing-debugging skill before frontend work. Add failing tests for collection/relevance filter combinations and clear missing-review behavior. An unreviewed legacy record is not counted as reviewed contemporary or direct-AI evidence. Default Principal view includes both collections and legacy pending records with an explicit pending denominator.

Use `CorpusCriteria.collection` and `CorpusCriteria.relevance` as the URL/form keys. Both accept `legacy_review_pending` as an explicit review-pending option. Add the following behavioral test alongside the existing filter fixtures before changing the filter implementation; complete the typed fixture with the Task 1 evidence fields already required by the type:

```typescript
it('separates a historical collection from publication year and pending review', () => {
  const historical = {
    ...act,
    id: 'historical-test-resolution',
    historical_review_status: 'verified' as const,
    temporal_collection: 'historical_lineage' as const,
    relevance_class: 'direct_ai_substantive' as const,
    document_date: '2017-02-16',
    publication_date: '2018-07-18',
    record_level: 'principal' as const,
  };
  const pending = {
    ...act,
    id: 'legacy-test-record',
    historical_review_status: 'legacy_review_pending' as const,
    temporal_collection: null,
    relevance_class: null,
    record_level: 'principal' as const,
  };
  const rows = [historical, pending];
  expect(filterDocuments(rows, { collection: 'historical_lineage', relevance: 'direct_ai_substantive', year: '2018' }).map(row => row.id)).toEqual(['historical-test-resolution']);
  expect(filterDocuments(rows, { collection: 'historical_lineage', year: '2017' })).toEqual([]);
  expect(filterDocuments(rows, { relevance: 'legacy_review_pending' }).map(row => row.id)).toEqual(['legacy-test-record']);
  expect(filterDocuments(rows, {}).map(row => row.id).sort()).toEqual(['historical-test-resolution', 'legacy-test-record']);
});
```

Run `node.exe node_modules/vitest/vitest.mjs run tests/filter.test.ts` for RED/GREEN, using the known absolute Node runtime. Preserve the existing explicitly labelled Publication year control; Timeline remains based on document_date. Test URL parse/serialize for the two new criteria using the existing helper signatures.
- [ ] Add compact English Collection and Relevance controls, including an explicit pending-review option. Render date kind and publication-date evidence with official metadata; render temporal/relevance and their evidence under Research classifications. Named external authors, commissioner, publisher, host/source and evidence-bearing roles stay distinct. Keep existing short-title typography and routes.
- [ ] Show a plain legacy expanded-review notice on old unupgraded record pages. Do not conflate it with existing retained-route notices that address different evidence defects. Timeline accepts historical years, labels the plotted document date, and still separates events. No synthetic Policy Map edges or forced AI Act membership.
- [ ] Display the bounded source-scope matrix/list on Methodology with explicit partial/unspecified status, cutoff, interval and pending counts. Retain the expanding-corpus statement and distinguish the database seed subset from an approved PhD sample. Update count expectations that genuinely changed; do not weaken unrelated tests.
- [ ] Use Task 1's verified scratch public JSON for the local build without overwriting protected generated artifacts; use existing loader override if present or a narrowly scoped environment override with tests. Run relevant web tests and production build; inspect browser desktop/mobile Corpus, one historical record, one pending legacy record, Timeline and Methodology using the available browser plugin first. Report unavailable checks honestly rather than moving the user into repeated manual command loops.
- [ ] Commit only task files locally, write the report, and hand off without pushing or claiming deployment. Final report separates historical additions, existing records fully reviewed, remaining reviews, software validation, and publication status.

## Self-review and explicit remaining scope

Task 1 implements the historical inclusion gate, compatible old-record handling, evidence/attribution/date persistence, bounded source scopes, and actual additions. Task 2 makes these semantics visible and filterable without redesign. The following are not claimed complete: all 117 evidence reviews, all EU source/year searches, a fully populated source/type/sector cross-product, adjudication of held leads, a researcher-approved RP analytical sample, or remote release checks. These remain visibly incomplete rather than blocking truthful partial publication semantics.
