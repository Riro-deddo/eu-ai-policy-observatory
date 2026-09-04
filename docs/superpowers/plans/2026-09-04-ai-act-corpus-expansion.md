# AI Act Corpus Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the English-only EU AI Policy Observatory from seven seed documents into an auditable, version-aware 2018–2026 EU AI Act corpus, then publish the enlarged database and usable principal-versus-all-files views on GitHub Pages.

**Architecture:** Keep JSON records under `data/` as canonical research data, validate them offline, normalise published records into SQLite, export a deterministic public JSON payload, and render the static Astro atlas from that payload. Add a checked-in research inventory and source-sweep register so completeness claims are reproducible without making CI depend on live EU websites.

**Tech Stack:** Python 3.11+, JSON Schema 2020-12, SQLite, pytest, Astro 5, TypeScript, Node test runner, Vitest, Playwright, GitHub Actions and GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-04-ai-act-corpus-expansion-design.md`

## Global Constraints

- Keep every repository field, record, page and user-facing label in English.
- Preserve the IDs and slugs of all seven existing documents.
- Use only official EU sources for public metadata and relationship evidence.
- Keep `official_summary` null unless an attributable official summary is copied or closely represented.
- Do not count press releases, news, FAQs or event pages as policy documents; they may support source or event records.
- Do not create snapshots unless actual file bytes have been retrieved and hashed.
- Do not place pending-review records in SQLite, public JSON or the built site.
- Use `2026-09-04T00:00:00Z` as the canonical migration timestamp for records added or materially changed by this expansion. Use the real verification time for `retrieved_at` and `last_verified_at` when official sources are checked.
- Run the narrow failing test before each implementation step, then the narrow passing test after it.
- Commit only after the task's tests pass; suggested commit messages below may be combined only when a task is too small to justify a separate commit.

## File and Responsibility Map

- `schema/record.schema.json`: canonical entity contract.
- `schema/controlled-vocabularies.json`: allowed research and legal classifications.
- `schema/database.sql`: public SQLite schema.
- `src/observatory/validate.py`: cross-record, identity, provenance and inventory validation.
- `src/observatory/build_db.py`: normalised SQLite insertion.
- `src/observatory/export_public.py`: deterministic public payload and coverage metrics.
- `src/observatory/pipeline.py`: atomic validation/build/export orchestration.
- `research/source-sweep.json`: official discovery entrances and scan status.
- `research/corpus-inventory.json`: one decision for every discovered candidate.
- `schema/source-sweep.schema.json` and `schema/corpus-inventory.schema.json`: audit-file contracts.
- `data/{policies,institutions,sources,documents,events,relationships}/*.json`: canonical corpus records.
- `web/src/lib/{types,filter}.ts`: public-data types and browsing rules.
- `web/src/components/{CorpusExplorer,Timeline,PolicyMap}.astro`: interactive public views.
- `web/src/pages/corpus/[slug].astro`: record metadata and relationship navigation.
- `web/src/pages/{index,methodology,about}.astro`: coverage and methods copy.
- `docs/data-dictionary.md` and `README.md`: contributor-facing data documentation.
- `tests/` and `web/tests/`: regression, contract, rendering, accessibility and route checks.

---

## Task 1: Evolve the canonical document contract

**Files:**

- Modify: `schema/controlled-vocabularies.json`
- Modify: `schema/record.schema.json`
- Modify: `src/observatory/validate.py`
- Modify: `tests/fixtures/valid/data/documents/example-document.json`
- Modify: `tests/fixtures/invalid/data/documents/broken-document.json`
- Modify: `tests/fixtures/invalid/data/documents/second-document.json`
- Modify: `tests/test_schema_contract.py`
- Modify: `tests/test_validate.py`

- [ ] **Step 1: Add failing schema tests for the new fields and vocabularies.**

Add assertions equivalent to:

```python
assert document["record_level"] in {"principal", "supporting", "version", "attachment"}
assert document["version_status"] in {"draft", "revised", "final", "consolidated", "not_applicable"}
assert document["document_date"] == "2026-09-03"
assert document["procedure_references"] == ["2021/0106(COD)"]
```

Also test that duplicate `procedure_references`, missing `document_date`, an unknown `record_level`, an unknown `version_status`, and an unknown expanded `document_type` are rejected.

- [ ] **Step 2: Run the focused tests and confirm the new assertions fail.**

Run: `python -m pytest tests/test_schema_contract.py tests/test_validate.py -q`

Expected: failures naming the unsupported or missing new document fields.

- [ ] **Step 3: Expand the controlled vocabularies.**

Add:

```json
"record_level": ["principal", "supporting", "version", "attachment"],
"version_status": ["draft", "revised", "final", "consolidated", "not_applicable"]
```

Extend `document_type` with `staff_working_document`, `institutional_position`, `opinion`, `resolution`, `decision`, `implementing_regulation`, `guidelines`, `code_of_practice`, `template`, `report`, and `standardisation_request`. Extend `relationship_type` with `version_of`, `annex_to`, `revises`, `endorses`, and `procedural_step_for`. Extend `source_type` with `council_register`, `parliament_register`, `official_register`, and `official_consultation`.

- [ ] **Step 4: Add required fields to the document schema.**

Use this shape:

```json
"record_level": {"enum": ["principal", "supporting", "version", "attachment"]},
"official_reference": {"$ref": "#/$defs/nullable_string"},
"procedure_references": {
  "type": "array",
  "items": {"type": "string", "minLength": 1},
  "uniqueItems": true
},
"oj_reference": {"$ref": "#/$defs/nullable_string"},
"document_date": {"$ref": "#/$defs/date"},
"version_label": {"$ref": "#/$defs/nullable_string"},
"version_status": {"enum": ["draft", "revised", "final", "consolidated", "not_applicable"]}
```

Require all seven keys so null and empty-list values are explicit research decisions.

- [ ] **Step 5: Teach vocabulary validation about `record_level` and `version_status`, then migrate fixtures.**

The valid fixture uses `principal`, `COM(2026) 1 final`, `["2021/0106(COD)"]`, a null OJ reference, matching document/publication dates, `Final`, and `final`. Invalid fixtures receive syntactically valid migrated defaults unless their purpose is to test one of these fields.

- [ ] **Step 6: Add and test the composite identity check.**

In `validate.py`, reject duplicate document identity when two records share a non-null `official_reference`, `language`, normalised `version_label`, and the same sorted issuing-institution IDs. Keep the existing CELEX, ELI and slug checks. The issue code is `duplicate_document_identity` and must name record paths without echoing private data.

- [ ] **Step 7: Run the focused tests.**

Run: `python -m pytest tests/test_schema_contract.py tests/test_validate.py -q`

Expected: all pass.

- [ ] **Step 8: Commit.**

Suggested commit: `feat: add version-aware document schema`

---

## Task 2: Normalise and export the new metadata

**Files:**

- Modify: `schema/database.sql`
- Modify: `src/observatory/build_db.py`
- Modify: `src/observatory/export_public.py`
- Modify: `tests/test_build_db.py`
- Modify: `tests/test_export_public.py`
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add failing database and export tests.**

Assert that `documents` contains the six scalar additions, that `document_procedure_references` contains one row per reference, and that public JSON embeds a sorted `procedure_references` array. Add a deterministic coverage assertion:

```python
assert payload["coverage"] == {
    "from_year": 2026,
    "to_year": 2026,
    "last_verified_date": "2026-09-03",
    "published_documents": 1,
    "principal_documents": 1,
    "supporting_files_and_versions": 0,
}
```

- [ ] **Step 2: Run the focused tests and confirm failure.**

Run: `python -m pytest tests/test_build_db.py tests/test_export_public.py tests/test_pipeline.py -q`

- [ ] **Step 3: Alter the SQLite schema.**

Add `record_level`, `official_reference`, `oj_reference`, `document_date`, `version_label`, and `version_status` to `documents`. Apply the same strict calendar check to `document_date` as to `publication_date`. Add:

```sql
CREATE TABLE document_procedure_references (
    document_id TEXT NOT NULL REFERENCES documents(id),
    procedure_reference TEXT NOT NULL,
    PRIMARY KEY (document_id, procedure_reference)
);
```

Do not make `official_reference` globally unique because independently citable attachments may share a parent reference.

- [ ] **Step 4: Insert and export the new fields.**

Extend `_insert_documents`, add insertion of `procedure_references`, and add an export helper that selects them ordered by value. Include `coverage` in the public payload. Define `supporting_files_and_versions` as every published document whose `record_level != 'principal'`; derive the date range from `document_date` and `last_verified_date` from exported official sources.

- [ ] **Step 5: Run the focused tests.**

Run: `python -m pytest tests/test_build_db.py tests/test_export_public.py tests/test_pipeline.py -q`

Expected: all pass and the generated artefacts remain atomic and deterministic.

- [ ] **Step 6: Commit.**

Suggested commit: `feat: export version metadata and coverage counts`

---

## Task 3: Migrate the seven stable seed records

**Files:**

- Modify: all seven existing files in `data/documents/`
- Modify: `tests/test_seed_corpus.py`
- Modify: `web/tests/site.spec.ts`

- [ ] **Step 1: Add failing migration assertions.**

Assert that the original seven ID/slug pairs are unchanged, every record has the new explicit fields, the final AI Act has `document_date: 2024-06-13` and `publication_date: 2024-07-12`, and the proposal carries `official_reference: COM(2021) 206 final` plus `procedure_references: ["2021/0106(COD)"]`.

- [ ] **Step 2: Run the focused tests and confirm failure.**

Run: `python -m pytest tests/test_seed_corpus.py -q`

- [ ] **Step 3: Migrate each record from official evidence.**

Use `principal` for the seven existing records. Use `final` when the record is a final issued text, `draft` for the legislative proposals, and `not_applicable` only when version language would be misleading. Populate official references, procedures and OJ citations where available; use null or an empty list explicitly where unavailable.

- [ ] **Step 4: Run seed and route tests.**

Run: `python -m pytest tests/test_seed_corpus.py -q`

Run: `pnpm --dir web test -- --run`

Expected: every original corpus URL still resolves.

- [ ] **Step 5: Commit.**

Suggested commit: `data: migrate seed corpus to version-aware records`

---

## Task 4: Add the auditable source sweep and corpus inventory

**Files:**

- Create: `schema/source-sweep.schema.json`
- Create: `schema/corpus-inventory.schema.json`
- Create: `research/source-sweep.json`
- Create: `research/corpus-inventory.json`
- Modify: `src/observatory/validate.py`
- Modify: `src/observatory/pipeline.py`
- Create: `tests/test_research_inventory.py`
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Write failing inventory contract tests.**

Test these invariants:

```python
assert {entry["decision"] for entry in inventory["candidates"]} <= {
    "included", "merged", "excluded", "pending"
}
assert all(entry["decision_reason"].strip() for entry in inventory["candidates"])
assert all(entry["document_id"] for entry in inventory["candidates"] if entry["decision"] == "included")
assert all(source["scan_status"] == "complete" for source in sweep["sources"])
```

Also require unique candidate IDs, unique source IDs, a valid official HTTPS URL, `checked_at`, and a matching canonical document for every `included` candidate. A `merged` candidate must name `merged_into_document_id`; an `excluded` candidate must not name a document; a `pending` candidate must remain absent from public data.

- [ ] **Step 2: Run the tests and confirm the inventory files or validators are missing.**

Run: `python -m pytest tests/test_research_inventory.py tests/test_pipeline.py -q`

- [ ] **Step 3: Define the audit schemas.**

The source-sweep file has `generated_at` and `sources[]` with `id`, `name`, `institution`, `url`, `scope_note`, `scan_status`, and `checked_at`. The corpus inventory has `generated_at` and `candidates[]` with `id`, `source_ids`, `official_reference`, `official_title`, `year`, `issuing_institution`, `record_level`, `version_label`, `official_source_url`, `decision`, `decision_reason`, `document_id`, and `merged_into_document_id`.

- [ ] **Step 4: Register the required official discovery entrances.**

The initial `research/source-sweep.json` must include at least:

1. EUR-Lex procedure `2021/0106/COD`.
2. EUR-Lex procedure `2025/0359/COD`.
3. EUR-Lex searches for Commission AI communications, staff working documents, decisions, regulations and implementing regulations, 2018–2026.
4. European Parliament Legislative Observatory and adopted-text records for `2021/0106(COD)`.
5. Council public-register records for `2021/0106(COD)` and `2025/0359(COD)`.
6. EESC, Committee of the Regions and ECB opinion registers.
7. EDPB and EDPS legislative-opinion registers.
8. Commission AI Act implementation and regulatory-framework pages.
9. AI Office pages for GPAI guidance, codes, templates and opinions.
10. European AI Board document page.
11. Commission consultation pages for high-risk, incident-reporting and transparency instruments.
12. Commission standardisation-request records, including C(2023) 3215 and C(2025) 3871.

- [ ] **Step 5: Integrate offline inventory validation before output mutation.**

Add a dedicated validation function invoked by `run_pipeline` after canonical record validation and before loading or publishing outputs. Return actionable paths such as `research/corpus-inventory.json: candidates.12.document_id`.

- [ ] **Step 6: Run the focused tests.**

Run: `python -m pytest tests/test_research_inventory.py tests/test_pipeline.py -q`

- [ ] **Step 7: Commit.**

Suggested commit: `feat: add auditable corpus inventory`

---

## Task 5: Complete the official 2018–2021 discovery and ingestion batch

**Files:**

- Modify: `research/source-sweep.json`
- Modify: `research/corpus-inventory.json`
- Create/modify: `data/policies/*.json`
- Create/modify: `data/institutions/*.json`
- Create: `data/sources/*.json`
- Create: `data/documents/*.json`
- Create: `data/events/*.json`
- Create: `data/relationships/*.json`
- Modify: `tests/test_seed_corpus.py`
- Modify: `tests/test_research_inventory.py`

- [ ] **Step 1: Add failing assertions for the required anchor instruments.**

At minimum, assert included and published records for:

- COM(2018) 237, *Artificial Intelligence for Europe*;
- COM(2018) 795 and its coordinated-plan attachment(s);
- the 2019 Ethics Guidelines for Trustworthy AI;
- COM(2019) 168, *Building Trust in Human-Centric Artificial Intelligence*;
- COM(2020) 65, the AI White Paper;
- COM(2020) 64, the safety and liability report;
- the 2020 Assessment List for Trustworthy AI;
- COM(2021) 205 and the 2021 Coordinated Plan review;
- COM(2021) 206, the AI Act proposal;
- SWD(2021) 84 and SWD(2021) 85, including independently citable annex or part files;
- EESC opinion `2021/C 517/08` / CELEX `52021AE2482`;
- Committee of the Regions opinion CELEX `52021AR2682`;
- ECB opinion CELEX `52021AB0040`; and
- EDPB–EDPS Joint Opinion 5/2021.

- [ ] **Step 2: Run the anchor tests and confirm missing records.**

Run: `python -m pytest tests/test_seed_corpus.py tests/test_research_inventory.py -q`

- [ ] **Step 3: Sweep every linked official file, not only the anchor pages.**

For each source entrance, enumerate English main texts, annexes, corrections and formal versions. Add one inventory row per candidate before deciding it. Use `attachment` plus `annex_to` for independently citable annexes; use `merged` when a PDF is merely another manifestation of the same English record; use `excluded` for explanatory news/FAQ content; use `pending` when metadata cannot yet be verified.

- [ ] **Step 4: Create narrower policy and institution records needed by the batch.**

Add policy records for the AI Act legislative process and coordinated European AI strategy. Add missing issuers such as the EESC, Committee of the Regions, ECB, EDPB and EDPS. Keep researcher classifications in corpus assessments and relationship rationales, never in official-title fields.

- [ ] **Step 5: Add official sources, documents, events and relationships.**

Use EUR-Lex or ELI as the first evidence source whenever available. Model the proposal package with `annex_to`, `procedural_step_for`, `part_of`, `precedes` and `based_on` relations as supported by the sources. Every published relationship must have a verified official evidence source.

- [ ] **Step 6: Mark all 2018–2021 sweep entrances complete and run tests.**

Run: `python -m pytest tests/test_seed_corpus.py tests/test_research_inventory.py tests/test_validate.py -q`

Run: `observatory-build --project-root . --timestamp 2026-09-04T00:00:00Z`

- [ ] **Step 7: Commit.**

Suggested commit: `data: add 2018 to 2021 AI Act corpus`

---

## Task 6: Complete the 2022–2024 negotiation, adoption and early implementation batch

**Files:**

- Modify: `research/source-sweep.json`
- Modify: `research/corpus-inventory.json`
- Create/modify: canonical records under `data/`
- Modify: `tests/test_seed_corpus.py`
- Modify: `tests/test_research_inventory.py`

- [ ] **Step 1: Add failing anchor assertions.**

Require at least:

- Council General Approach ST 15698/22 and all formally published compromise-text versions found in the Council register;
- European Parliament committee-report material and P9_TA(2023)0236 / CELEX `52023AP0236`;
- Parliament first-reading position P9_TA(2024)0138 / CELEX `52024AP0138`;
- final Regulation (EU) 2024/1689 / CELEX `32024R1689`;
- corrigenda or consolidated versions that meet the independent-record rule;
- Commission Decision C(2024) 390 / ELI `C/2024/1459` establishing the European AI Office;
- COM(2024) 28 on AI startups and innovation;
- the original standardisation request C(2023) 3215; and
- COM(2022) 496, the AI Liability Directive proposal, with its later withdrawal represented as an event rather than a rewritten publication date.

- [ ] **Step 2: Run the anchor tests and confirm failure.**

Run: `python -m pytest tests/test_seed_corpus.py tests/test_research_inventory.py -q`

- [ ] **Step 3: Sweep the complete procedure histories and linked registers.**

Capture Council document revisions, Parliament reports/annexes/amendments/positions, committee opinions, adopted text, final OJ record and corrigenda. Apply the same one-candidate-one-decision rule before canonical ingestion.

- [ ] **Step 4: Create records and version relationships.**

Use `version_of` for historical states of the same text, `revises` for a text that explicitly revises another, `adopted_as` between proposal and final legislation, `annex_to` for attachments, and `procedural_step_for` for formal positions. Record the AI Act's 13 June 2024 document date, 12 July 2024 OJ publication date and 1 August 2024 entry-into-force event separately.

- [ ] **Step 5: Run validation and build checks.**

Run: `python -m pytest tests/test_seed_corpus.py tests/test_research_inventory.py tests/test_validate.py tests/test_pipeline.py -q`

Run: `observatory-build --project-root . --timestamp 2026-09-04T00:00:00Z`

- [ ] **Step 6: Commit.**

Suggested commit: `data: add AI Act negotiation and adoption records`

---

## Task 7: Complete the 2025–2026 implementation and amendment batch

**Files:**

- Modify: `research/source-sweep.json`
- Modify: `research/corpus-inventory.json`
- Create/modify: canonical records under `data/`
- Modify: `tests/test_seed_corpus.py`
- Modify: `tests/test_research_inventory.py`

- [ ] **Step 1: Add failing anchor assertions.**

Require verified records for every available draft/final/component file in these official families:

- the AI system definition guidelines, C(2025) 5053 final;
- prohibited-practices guidelines, C(2025) 5052 final;
- general-purpose AI model guidelines, C(2025) 5045 final;
- the GPAI Code of Practice and its independently issued chapters, annexes, signatory forms and Commission assessment opinion;
- the public training-content summary template and explanatory notice;
- GPAI serious-incident reporting template and explanatory material that qualifies as a document;
- high-risk AI serious-incident draft guidance and reporting template;
- the Code of Practice on Transparency of AI-generated Content, its components and Commission assessment opinion;
- transparency-obligations guidelines;
- high-risk AI-system guidelines and their consultation versions;
- the Article 6(3) adequacy assessment, Article 70(9) adequacy assessment and successor versions listed by the AI Board;
- Commission Implementing Regulation (EU) 2025/454 / CELEX `32025R0454`;
- Commission Implementing Regulation (EU) 2026/1755 / CELEX `32026R1755`;
- C(2025) 3871, the updated standardisation request, related to and superseding C(2023) 3215;
- COM(2025) 165, the AI Continent Action Plan;
- COM(2025) 723, the Apply AI Strategy;
- COM(2025) 836 and every official supporting file in procedure `2025/0359(COD)`;
- Regulation (EU) 2026/1744 / CELEX `32026R1744`; and
- the 2026 Commission review report on prohibitions and high-risk AI.

- [ ] **Step 2: Run the anchor tests and confirm failure.**

Run: `python -m pytest tests/test_seed_corpus.py tests/test_research_inventory.py -q`

- [ ] **Step 3: Sweep the implementation pages, downloads and amendment procedure.**

Open every official download and version link, record the English title/date/reference and decide the candidate. Treat a consultation webpage as a source; treat its downloadable draft guidance or template as a document. Keep page-only announcements as sources unless they contain an independently citable formal instrument.

- [ ] **Step 4: Add policy-process records and canonical data.**

Add policies for AI Act implementation and governance, the Digital Omnibus amendment process, the GPAI Code process and the AI-generated-content transparency code process. Add AI Office, AI Board and Scientific Panel institution/body records only where they act as issuer or formal contributor; otherwise retain the European Commission institution with a precise role.

- [ ] **Step 5: Model revisions and legal changes.**

Connect draft-to-final records with `version_of` or `revises`, codes to Commission opinions with `endorses`, implementation instruments to the AI Act with `implements`, and the Digital Omnibus legislation to the AI Act with `amends`. Preserve exact proposal, adoption, OJ publication, entry-into-force and application dates as separate document/event facts.

- [ ] **Step 6: Close the inventory audit.**

No source-sweep entrance may remain incomplete. Every discovered candidate must have `included`, `merged`, `excluded` or a reasoned `pending` decision. `pending` is allowed in the repository but must fail any assertion that it leaks into public outputs.

- [ ] **Step 7: Run validation and build checks.**

Run: `python -m pytest tests/test_seed_corpus.py tests/test_research_inventory.py tests/test_validate.py tests/test_pipeline.py -q`

Run: `observatory-build --project-root . --timestamp 2026-09-04T00:00:00Z`

- [ ] **Step 8: Commit.**

Suggested commit: `data: add AI Act implementation and amendment corpus`

---

## Task 8: Add principal-versus-all corpus browsing

**Files:**

- Modify: `web/src/lib/types.ts`
- Modify: `web/src/lib/filter.ts`
- Modify: `web/src/components/CorpusExplorer.astro`
- Modify: `web/tests/fixtures/documents.ts`
- Modify: `web/tests/filter.node.test.mjs`
- Modify: `web/tests/filter.test.ts`
- Modify: `web/tests/corpus.source.test.mjs`

- [ ] **Step 1: Add failing TypeScript and filter tests.**

The default criteria must return only `record_level === 'principal'`; `view=all` must return all published records. Add AND-semantics tests for `recordLevel`, `versionStatus`, and `policy` as well as parsing tests that reject unknown query keys.

```ts
filterDocuments(documents, {}).map(({ id }) => id)
// principal records only

filterDocuments(documents, { view: 'all', versionStatus: 'draft' })
// all matching drafts, including version and attachment records
```

- [ ] **Step 2: Run the focused tests and confirm failure.**

Run: `pnpm --dir web test -- --run`

- [ ] **Step 3: Expand public TypeScript types and filter criteria.**

Add the seven new document fields and the `coverage` object. Extend `CorpusCriteria` with `view`, `recordLevel`, `versionStatus`, and `policy`. Keep search over official title, short title, CELEX, ELI and add `official_reference`.

- [ ] **Step 4: Update the Corpus explorer.**

Add an accessible two-choice view control labelled `Principal documents` and `All files and versions`. Add filters for record level, version status and policy process. Show both counts above the list, make the active count clear, retain the noscript complete list, and render human-readable labels rather than raw underscores.

- [ ] **Step 5: Run tests.**

Run: `pnpm --dir web test -- --run`

- [ ] **Step 6: Commit.**

Suggested commit: `feat: browse principal documents and all versions`

---

## Task 9: Expose version context on record, timeline and policy-map pages

**Files:**

- Modify: `web/src/pages/corpus/[slug].astro`
- Modify: `web/src/components/Timeline.astro`
- Modify: `web/src/lib/filter.ts`
- Modify: `web/src/components/PolicyMap.astro`
- Modify: `web/src/lib/policy-map.ts`
- Modify: `web/tests/site.spec.ts`
- Modify: `web/tests/timeline.node.test.mjs`
- Modify: `web/tests/policy-map.node.test.mjs`
- Modify: `web/tests/timeline-policy-map.source.test.mjs`

- [ ] **Step 1: Add failing record-page and graph tests.**

Assert that a version record renders official reference, document date, publication date, record level, version label, version status and procedures. Assert that relevant incoming/outgoing relations produce sections for `Parent or principal record`, `Attachments`, `Previous and next versions`, and `Formal procedure`. Add tests that timeline entries use `document_date` for the text's date while separate publication/adoption/entry events retain their own dates.

- [ ] **Step 2: Run the focused tests and confirm failure.**

Run: `pnpm --dir web test -- --run`

- [ ] **Step 3: Render document metadata and relationship navigation.**

Derive relationship groups from public `relationships` without duplicating data in document JSON. Render missing optional identifiers as absent sections, not `null`. Make all related document titles clickable and keep official versus analytical bases visible.

- [ ] **Step 4: Extend timeline and policy-map labels.**

Add readable labels for the expanded relationship and document vocabularies. Preserve the policy map's text alternative. Avoid showing identical same-day document and event entries when an event does not add a distinct procedural fact.

- [ ] **Step 5: Run tests.**

Run: `pnpm --dir web test -- --run`

- [ ] **Step 6: Commit.**

Suggested commit: `feat: show document versions and procedure context`

---

## Task 10: Publish honest coverage and methodology copy

**Files:**

- Modify: `web/src/pages/index.astro`
- Modify: `web/src/pages/methodology.astro`
- Modify: `web/src/pages/about.astro`
- Modify: `web/src/components/PolicyPathway.astro`
- Modify: `README.md`
- Modify: `docs/data-dictionary.md`
- Modify: `web/tests/final-review.source.test.mjs`
- Modify: `web/tests/accessibility.source.test.mjs`
- Modify: `tests/test_public_build.py`

- [ ] **Step 1: Add failing coverage-copy tests.**

Require the built site to contain `Coverage: 2018–2026`, the generated principal/supporting counts, the most recent verification date, and the sentence `Pending-review records are excluded from public totals.` Remove every remaining claim that the active corpus ends in 2024 or contains only seven documents.

- [ ] **Step 2: Run the focused tests and confirm failure.**

Run: `python -m pytest tests/test_public_build.py -q`

Run: `pnpm --dir web test -- --run`

- [ ] **Step 3: Update public copy from generated data.**

Do not hard-code document counts. Render them from `data.coverage`. Explain the three corpus tiers, inventory-decision model, official-versus-analytical distinction, version handling and date semantics in Methodology. State that the corpus is bounded to the AI Act policy process and directly relevant implementation, not all EU digital law.

- [ ] **Step 4: Update contributor documentation.**

Document every new field, vocabulary, identity rule, inventory decision and validation command. Include the database download and official-source requirements. Keep the public authorship line `Created and maintained by Yichen Hao`.

- [ ] **Step 5: Run tests.**

Run: `python -m pytest tests/test_public_build.py -q`

Run: `pnpm --dir web test -- --run`

- [ ] **Step 6: Commit.**

Suggested commit: `docs: publish corpus coverage and methods`

---

## Task 11: Full local verification and responsive browser review

**Files:**

- Modify if failures reveal defects: files owned by Tasks 1–10 only

- [ ] **Step 1: Run the complete Python suite.**

Run: `python -m pytest -q`

Expected: exit code 0.

- [ ] **Step 2: Rebuild canonical public artefacts.**

Run: `observatory-build --project-root . --timestamp 2026-09-04T00:00:00Z`

Expected: SQLite integrity `ok`; public JSON contains no pending-review records or local filesystem paths.

- [ ] **Step 3: Run complete web tests and production build.**

Run: `pnpm --dir web test`

Run: `pnpm --dir web build`

Expected: unit/source tests, Astro checks and Playwright tests pass.

- [ ] **Step 4: Run the public artefact scanner.**

Run: `python scripts/check_public_build.py --site web/dist --data generated/public-data.json`

Expected: exit code 0, with no unpublished entities, credentials or local paths.

- [ ] **Step 5: Review the rendered site at desktop and mobile widths.**

Check Home, Corpus default view, Corpus all-files view, a principal record, an attachment/version record, Timeline, Policy Map, Methodology and About at approximately 1440×900 and 390×844. Verify keyboard operation, visible focus, no horizontal overflow, readable long official titles and correct browser back/forward behaviour for query parameters.

- [ ] **Step 6: Inspect the final diff and repository status.**

Run: `git diff --check`

Run: `git status --short`

Run: `git diff --stat`

Expected: only intentional project files are changed; no generated caches, secrets or unrelated user work are included.

- [ ] **Step 7: Commit any verification fixes.**

Suggested commit: `test: verify expanded observatory corpus`

---

## Task 12: Push, monitor CI and verify GitHub Pages

**Files:**

- No planned source changes; fix only evidence-backed CI or deployment defects.

- [ ] **Step 1: Confirm the exact branch and remote.**

Run: `git branch --show-current`

Run: `git remote -v`

Expected: the intended branch and `Riro-deddo/eu-ai-policy-observatory` remote.

- [ ] **Step 2: Push the verified commits.**

Run in PowerShell: `$observatoryBranch = git branch --show-current; git push origin $observatoryBranch`

- [ ] **Step 3: Monitor the `Validate` and `Deploy GitHub Pages` workflows.**

Wait for both workflow runs associated with the pushed commit. If either fails, read the failing log, write a regression test where appropriate, fix only the failure, rerun all relevant local checks and push the repair.

- [ ] **Step 4: Verify the live site.**

Open `https://riro-deddo.github.io/eu-ai-policy-observatory/` and confirm the deployed commit exposes 2018–2026 coverage, dynamic counts, principal/all views and at least one new version-aware record. Confirm all seven legacy document URLs still return their record pages.

- [ ] **Step 5: Report the evidence.**

Report the final published document count, principal count, supporting/version/attachment count, pending inventory count, last verification date, commit hash, workflow conclusions and live URL. Do not describe the corpus as complete without also naming the bounded source-sweep method and any pending candidates.
