# Evidence-backed Relationship Migration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this bounded plan with review checkpoints.

**Goal:** Review fifteen existing relationship-readiness gaps; correct evidenced semantics, explicitly retain unresolved cases, and preserve published identities.

**Architecture:** Data-only corrections using the active contract, a versioned evidence ledger and regression tests. The prospective historical contract remains a read-only assessor. Validate a temporary SQLite/JSON pair; leave existing generated pair unchanged.

**Spec:** docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md; delivery roadmap Phase B.
**Stack:** existing Python, pytest, JSON, SQLite; no dependency changes.
**Base:** f4085fdf6ada9da4954f815738ff2b8bffe81ec0

## Global Constraints

- Preserve all 117 published document IDs, slugs, publication states and routes; add no document.
- Keep the seven canonical entities, English-only project, six pages and publication cutoff 2026-09-04.
- Use evidence for relationships and distinguish editorial judgments from official facts. Do not invent parenthood, lineage, attribution, dates or retained source snapshots.
- Keep prospective historical fields/gate inactive; no schema, production Python, SQL, web, inventory, source-sweep or candidate-admission changes.
- No GitHub push, merge, deployment, package installation, user-run terminal steps, reset or cleanup.
- Use only git --git-dir=work/sdd-gitmeta --work-tree=. in the existing isolated checkout on maintenance/historical-corpus-design. Preserve unrelated untracked work.
- Leave generated/public-data.json and generated/eu-ai-policy-observatory.sqlite unchanged in this bounded migration. Verify an alternate temporary output pair; activation/publication is later work.

## Task 1: Correct evidenced relationships and retain explicit holds

Read this first: these are the task requirements, with exact values to use verbatim.

### Scope and files

Modify exactly these four existing document JSON files under data/documents/:
- gpai-code-model-documentation-form-2025.json: record_level attachment -> supporting.
- gpai-code-signatory-form-2025.json: record_level attachment -> supporting.
- transparency-code-signatory-form-2026.json: record_level attachment -> supporting.
- draft-high-risk-classification-guidelines-2026.json: record_level version -> attachment (this record is the General-principles section, not the entire guidelines).

Only change record_level, updated_at, and append a field-specific English explanation to corpus_assessment.researcher_notes. Credit this narrow editorial correction to AI-assisted reviewer on 2026-09-05, not Yichen; retain existing researcher review fields because other classifications were not re-reviewed. Retain draft/final version_status, dates, titles, IDs/slugs, source/tags/policy memberships.

Modify five existing relationship JSON files under data/relationships/ without renaming their IDs/files or endpoints:
- gpai-code-final-copyright-version-of-final.json
- gpai-code-final-safety-version-of-final.json
- gpai-code-final-transparency-version-of-final.json
For these three, change version_of -> part_of, keep basis official, evidence_source_id gpai-code-final-commission; revise rationale to component/chapter semantics.
- high-risk-annex-i-version-of-draft.json
- high-risk-annex-iii-version-of-draft.json
For these two, change version_of -> related_to, basis official -> analytical. Rationale must say these are sibling sections of one draft guideline, not versions/annexes of the General-principles file; evidence_source_id remains high-risk-guidelines-draft-commission. This records association only, and does NOT satisfy parent readiness.

Create seven published/verified document-to-document relationships under data/relationships/:
- gpai-code-third-draft-commitments-part-of-third-draft: gpai-code-third-draft-commitments -> gpai-code-third-draft, part_of, official, source gpai-code-third-draft-commission.
- gpai-code-third-draft-copyright-part-of-third-draft: gpai-code-third-draft-copyright -> gpai-code-third-draft, part_of, official, same source.
- gpai-code-third-draft-safety-security-part-of-third-draft: gpai-code-third-draft-safety-security -> gpai-code-third-draft, part_of, official, same source.
- gpai-code-third-draft-transparency-part-of-third-draft: gpai-code-third-draft-transparency -> gpai-code-third-draft, part_of, official, same source.
- gpai-code-model-documentation-form-supports-final: gpai-code-model-documentation-form-2025 -> gpai-code-final, related_to, official, source gpai-code-final-commission.
- gpai-code-signatory-form-supports-final: gpai-code-signatory-form-2025 -> gpai-code-final, related_to, official, same source.
- transparency-code-signatory-form-supports-final: transparency-code-signatory-form-2026 -> transparency-code-final-2026, related_to, official, source transparency-code-signatory-commission.

Use valid existing relationship schema fields. Existing created_at stays unchanged; updated_at and all newly created timestamps use 2026-09-05T07:35:00Z (parent review completed this turn). Do not add generic automatic migration code.

Modify four sources under data/sources/: gpai-code-final-commission.json, gpai-code-third-draft-commission.json, high-risk-guidelines-draft-commission.json, transparency-code-signatory-commission.json. Preserve prior retrieved_at and created_at. Set updated_at/last_verified_at to the review timestamp. Append a narrow verification_note: landing-page structure/purpose and download labels checked; linked binary file interiors and retained bytes were NOT verified in this review. Point to the migration ledger.

Create research/migrations/2026-09-05-relationship-evidence-migration.json and a concise companion .md.
The ledger must record actual review date/time, cutoff, reviewer AI-assisted reviewer, base commit, all 15 target document IDs, before/after editorial levels, relationship before/after or new edge IDs, shared source URL/locator evidence, action rationale, resolved/held status and hold reasons. Preserve pre-change values for fields actually changed (nested review notes/source notes may be recorded as before/after in a compact changes array). Do not imply whole-record/every-classification verification. No source snapshots are retained. Generated pair remains pre-migration pending a later controlled rebuild; say so explicitly.

Five holds remain:
- draft-high-risk-classification-guidelines-2026
- draft-high-risk-classification-guidelines-annex-i-2026
- draft-high-risk-classification-guidelines-annex-iii-2026
These need a represented whole-guidelines endpoint; do not add one now, and do not repurpose the General-principles document as that whole.
- draft-guidance-serious-ai-incidents-2025
- draft-serious-ai-incident-report-template-2025
These remain unchanged: co-issued separate consultation documents do not prove same-work version lineage; do not invent a parent or reclassify merely to pass. Review their editorial levels and any genuine predecessor/successor evidence in a later batch.

Ten targets resolve this relationship-readiness issue only, not overall historical readiness. The count of relationships should move from 88 to 95 (7 added; 5 corrected). Document count stays 117. No claims of corpus completeness.

### Evidence verified by parent and parallel read-only researchers

Review timestamp 2026-09-05T07:35:00Z is the parent review cutoff, not a document publication date. The GPAI research agent initially mistyped Sept 3; use actual Sept 5. Primary HTML pages were independently opened by parent.

E1 gpai-code-final-commission:
https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai
Locators: paragraph immediately before "The 3 chapters of the code"; that heading and three chapter rows, especially Transparency.
The code has three chapters. The model-documentation form supports Transparency; the signatory form enables signing. Neither separate form is described as a chapter/annex. Map three chapters to part_of; forms to supporting + related_to. File redirects: transparency 118120, copyright 118115, safety/security 118119, documentation form 118118, signatory form 118312.
Record-level choices are editorial, not official metadata. HTML evidence suffices for this narrow relationship classification; binary redirects failed decoding.

E2 gpai-code-third-draft-commission:
https://digital-strategy.ec.europa.eu/en/library/third-draft-general-purpose-ai-code-practice-published-written-independent-experts
Locators: opening structural paragraph on commitments, "Details of the third draft", and numbered Downloads 1-4.
Commitments plus transparency, copyright, safety/security constitute the draft's structure; this is more than simple co-listing. Use part_of for all four. Redirects respectively 113606, 113607, 113605, 113608. Binary interiors unverified.

E3 high-risk-guidelines-draft-commission:
https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems
Locators: paragraph immediately before Downloads (separately downloadable sections), Downloads 1-3, and section III/IV explanation.
General principles and the two sector sections are siblings. Annex I/III name AI Act annexes covered, not annexes attached to General principles. Redirects 128559, 128560, 128561. Whole-work endpoint absent. Binary interiors unverified.

E4 transparency-code-signatory-commission:
https://digital-strategy.ec.europa.eu/en/library/how-sign-code-practice-transparency-ai-generated-content
Locator: signing instructions and "Signatory form (DOCX)" download (129548).
The form is administrative signing material for the final transparency code; supporting/related_to is an editorial representation of the stated purpose.
Corroboration: https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content (two sections vs separate signature instructions).
Binary interiors unverified.

E5 high-risk-incident-consultation-commission (read-only; do not update canonical source this task):
https://digital-strategy.ec.europa.eu/en/consultations/ai-act-commission-issues-draft-guidance-and-reporting-template-serious-ai-incidents-and-seeks
Locators: explanatory paragraph before Downloads; two separately titled Downloads.
Two companion drafts with distinct functions. Neither parenthood nor a represented version endpoint was verified. Redirects guidance 119624/template 119623 returned decoding errors. No final successor verified.

### TDD and verification

Controller integration addendum: update tests/test_seed_corpus.py to match the verified final Transparency chapter relationship (part_of, not version_of). Also use pytest's tmp_path fixture for test_classification_migration_preserves_ordered_document_ids_and_slugs instead of TemporaryDirectory(dir="."). The latter reproducibly stalls in Windows tempfile.mkdtemp before any migration runs; retain all migration/identity assertions and do not skip the test. These are test-harness corrections only, not production changes. Run the full Python suite with PYTHONPATH set to the absolute src directory and a system Temp basetemp.

Create tests/test_relationship_evidence_migration.py. Write meaningful failing regression tests FIRST and run them before canonical edits:
- Assert exact directed, typed edges for the seven component links and three supporting-form associations.
- Assert the three forms are supporting while draft/final statuses and the frozen 117 identity/route baseline in research/migrations/2026-09-05-public-document-baseline.json are preserved. Do not use mutable generated output as the identity authority.
- Assert General principles is attachment, sibling edges related_to/analytical, and all five held targets retain relationship readiness issues while the other ten no longer do.
- Run real existing load_records + validate_historical_readiness for this relationship subset; do not mock away validation or activate the schema.
- Verify the evidence ledger covers exactly 15 unique targets with 10 resolved/5 held and concrete source references; avoid tests asserting vacuous strings.
- Run the real run_pipeline(project_root, timestamp, output_root=tmp_path / "output") and inspect both temporary public JSON and SQLite for changed record levels, directed edges and full published ID/slug preservation. Reuse unchanged pipeline's actual signatures/table columns; do not invent API flags.
- Keep these as compact focused data regression/integration tests, not a new migration subsystem.

After edits run:
.venv/Scripts/python.exe -m pytest tests/test_relationship_evidence_migration.py tests/test_historical_readiness.py tests/test_schema_contract.py tests/test_validate.py tests/test_research_inventory.py -q -p no:cacheprovider --basetemp <fresh absolute system Temp directory> --tb=short
Current baseline for the four pre-existing suites: 179 passed. Use system Temp, not repo scratch.
PYTHONPATH=src for Python module CLI if needed. Verify git diff --check and protected generated pair hashes unchanged. Do not run frontend/browser tasks.

Report exact RED/GREEN commands/output, tested export counts, remaining issue counts, before/after audit and any concerns to the report path supplied by controller. Do not overwrite the prior Phase B1 readiness report. No subagents. Controller will review, verify and commit the completed task; do not stage/commit yourself.


### Delivery checklist

- [x] Evidence-led TDD and data corrections.
- [x] Task review (specification and quality).
- [x] Fresh controller verification and final broader review.
- [x] Local commit and explicit held-work handoff; no publication.
