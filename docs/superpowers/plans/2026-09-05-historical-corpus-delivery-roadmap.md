# Historical Corpus Delivery Roadmap

**Status:** Planning only; no implementation or deployment has been performed by this document.

**Approved specification:** [Historical Scope and Evidence-Based Coverage Design](../specs/2026-09-05-historical-scope-and-coverage-design.md).

## Delivery boundaries

The approved design contains three independently reviewable deliveries. Implement them sequentially, with a working, tested result and a scope check between phases. Only Phase A has a detailed executable plan in this planning release. Phases B and C below are bounded planning briefs, not executable instructions or claims of completion.

| Phase | Deliverable | Entry and exit conditions |
| --- | --- | --- |
| A — Coverage integrity | Truthful public copy and aggregate states; preserved history when old exclusions are reopened; release regression protection | Start from the existing corpus. Finish with canonical records and URLs unchanged, genuine pending work represented, and no unconditional completeness claim. |
| B — Historical-capable schema and atlas | Evidence-backed temporal/relevance/date and provenance fields, reviewed migration, version integrity, English filtering/display | Begin detailed planning after A's interfaces and review outcomes are checked. Finish only after all migrated public records meet the new rules or have an explicitly reviewed retained-route notice. |
| C — Source matrix and reviewed backfill | Registered source universe, incomplete coverage matrix, individually verified historical and sectoral additions, bounded audit evidence | Begin after B's publication contract works. Finish a named batch without claiming that the wider EU universe has been exhausted. |

The first executable plan is [Phase A: Coverage Integrity](./2026-09-05-coverage-integrity-phase-a.md). There is no permission here to skip directly to a bulk import or merge to the publishing branch.

## Phase B planning brief

The next plan must define concrete field types, evidence references and validators before any migration. Map the work across the existing canonical JSON Schema, controlled vocabularies, Python validator, SQL schema/build/export, TypeScript public types and Astro pages. Do not fork the seven-entity model into separate historical and contemporary databases.

Required independently testable units:

1. Temporal/relevance/date contracts: `temporal_collection`, `relevance_class`, `document_date_kind`, distinct publication dates and source-backed classification review. Cover pre-1984 candidates and the 2017-adoption/2018-publication case without duplicate IDs. Replace the candidate schema's hardcoded 2018 lower bound and 2026 upper bound with historical-capable validation and an explicitly checked publication cutoff; neither year is a permanent eligibility boundary.
2. Attribution contracts: commissioner, bibliographic external author credits, publisher/host distinction, historically correct Community institutions, `directive`/`conclusions` and evidenced repealed/expired statuses.
3. Reviewed migration: freeze the RP-oriented selection, preserve evidence-backed classifications, prohibit the old fallback migration, reconcile nine currently disconnected versions/attachments, and enforce official evidence for all published relationships. Unresolved records need a reviewed transition and a retained-route decision, not silent deletion.
4. Generation and atlas: round-trip the fields through SQLite/public JSON; add collection/relevance filters and counts; move editorial metadata to Research classifications; retain timeline date semantics, the map's recorded-only edges, keyboard behaviour and stable routes.

Before implementation, its detailed plan must include fixtures for every acceptance criterion in specification sections 3–6 and 9, plus tests for migration no-ops, rejected guessed classifications, unknown historical dates and duplicate manifestations. The detailed plan must not imply that reviewing all 117 records is a five-minute automated step: use record batches and an evidence ledger.

## Phase C planning brief

The next source/backfill plan must define source-scope rows and their public matrix projection before registering new apparent coverage. It must distinguish target search intervals, actually reviewed intervals, unstarted work, zero results, access failures and reasoned non-applicability. Empty legacy scope arrays must not become an all-sector census.

Required units:

1. Register EUR-Lex/Cellar, Publications Office catalogues, Parliament studies/registers, Council/European Council, Commission departments/expert groups, CURIA and relevant agency catalogues, including FRA, ENISA and EMA. Verify entry URLs and methods when execution begins.
2. Add the matrix by source family, institution, period, document type and sector, exposing temporal/relevance subsets, denominators and incomplete states. Keep raw pending candidate metadata out of public JSON and downloads.
3. Review the historical candidate set and current-range omissions individually. The audit's 15 AI/precursor candidates and 3 indirect legal-context candidates are leads, not an import whitelist. A five-document contemporary omission sample is not an estimate of the full missing universe.
4. Publish bounded, checked batches with exact dates, institutional names, sources, sector/provenance tags and version relationships. Record actual snapshots only when bytes have been retrieved.
5. Implement a completed-bounded-audit gate only after named source-universe, query, zero-pending, chain/deduplication and reverse-citation evidence can be validated. Until then retain the expanding-corpus statement introduced in A.

Newly discovered pre-1984 evidence is eligible for screening; it does not silently expand a completed audit's date range. No single-record verification advances every source's cutoff.

## Specification coverage map

| Specification section | Owning delivery |
| --- | --- |
| 1–2: decision, model, English scope and non-goals | Constraints in every phase; no phase introduces LLM experiments or a new host |
| 3: temporal collections | B contract and migration; C source/period backfill |
| 4: relevance classes | B evidence contract and filters; C individual assessments |
| 5: dates and identity | B schema/validation/migration; C verified records |
| 6: institutions and provenance | B role/history/type semantics; C historical and commissioned records |
| 7: discovery and candidate decisions | A reopens existing unresolved decisions with history; C registers wider universe and reproducible searches |
| 8.1: matrix | A exposes honest aggregate limitations; C supplies the full matrix |
| 8.2: claims | A removes unconditional claims; C adds the evidence-gated bounded-audit capability |
| 9: atlas and research subsets | A scope/status copy; B controls, classifications and protected RP selection |
| 10: sequence and safe migration | A before B before C; separate authority check before any public deployment |
| 11: acceptance | Each delivery has its own tests; full design acceptance requires B and C as well as A |
| 12: evidence anchors and limits | C re-verifies candidates; no automatic admission based on this roadmap |

## Release and authority checkpoints

- Written-spec approval permits planning; it is not itself a command to publish all changes.
- Execute the selected phase only after the user chooses the execution approach.
- Keep every task's tests, evidence review and local commit distinct. A task's green software tests do not establish academic completeness.
- Preserve user changes and existing public IDs. Never rerun the legacy classifier or silently remove public records to satisfy a new validator.
- An approved preview does not by itself prove deployment. Before a push/PR/merge that can publish, confirm the intended target and existing authorisation; deployment requires the repository's successful Validate-to-Pages chain and live checks.
- Report phase completion narrowly: “Coverage integrity corrected” is not “Historical expansion complete,” and neither is “All EU AI documents collected.”
