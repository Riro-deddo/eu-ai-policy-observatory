# AI Act Corpus Expansion Design

**Date:** 4 September 2026
**Status:** Approved
**Project:** EU AI Policy Observatory

## 1. Objective

Expand the EU AI Policy Observatory from a seven-document seed corpus into a version-aware English-language research corpus covering the development, negotiation, adoption, amendment and implementation of the EU Artificial Intelligence Act from 2018 through 2026.

The expansion is intended to be as complete as practicable within the defined scope. A preliminary review identified approximately 45 principal instruments and an estimated 100–140 separate English-language files or versions, but these figures are discovery estimates rather than publication caps. Every eligible official file found during the sweep must receive an explicit inclusion, merge, exclusion or pending-review decision.

## 2. Research Boundary

The corpus has three inclusion tiers:

- `core`: documents that directly formulate, negotiate, adopt or amend the Artificial Intelligence Act.
- `directly_related`: institutional opinions, impact assessments, implementation acts, guidance, codes, templates and governance documents that directly interpret or operationalise the Act.
- `contextual`: EU artificial-intelligence strategy, coordination, innovation and liability documents needed to understand the Act's policy setting.
- `excluded`: assessed candidates that fall outside the research boundary.

The project does not ingest the whole EU digital acquis. Instruments such as the GDPR, Digital Services Act, Data Act and Cyber Resilience Act may be referenced through evidenced relationships where necessary, but do not enter the corpus merely because the AI Act cites or interacts with them.

The sweep covers:

- EUR-Lex procedure `2021/0106/COD` and its identifiable supporting documents;
- EUR-Lex procedure `2025/0359/COD` and its identifiable supporting documents;
- Commission communications, reports, impact assessments and staff working documents;
- Council general approaches, compromise texts and formal positions;
- Parliament committee reports, amendments, resolutions and adopted positions;
- formal opinions from EU bodies, including the EESC, CoR, ECB, EDPB and EDPS;
- AI Office, AI Board and Scientific Panel instruments;
- implementing regulations, guidelines, codes of practice, templates and standardisation requests; and
- publicly issued consultation drafts, final texts and superseded versions.

Press releases, news articles, FAQs and event pages are not treated as policy documents. They may be retained as sources or evidence for events. Other-language manifestations of an English record are not counted as separate corpus documents.

## 3. Entity Model

The existing seven top-level entity types remain:

1. `policy`
2. `document`
3. `event`
4. `concept`
5. `institution`
6. `relationship`
7. `source`

Snapshots remain nested document data rather than a separate canonical entity type.

### 3.1 Policy records

The current broad policy grouping will be supplemented by narrower policy-process records, including at least:

- the original Artificial Intelligence Act legislative process;
- AI Act implementation and governance;
- the Digital Omnibus on AI amendment process;
- the General-Purpose AI Code of Practice process;
- the Code of Practice on Transparency of AI-generated Content process;
- coordinated European AI strategy; and
- AI liability policy.

A document may belong to more than one policy process where that assignment is analytically justified.

### 3.2 Document records

Each independently citable English official text, attachment or formal version is a separate document record. Existing document identifiers and public slugs remain stable.

The document schema gains:

- `record_level`: `principal`, `supporting`, `version` or `attachment`;
- `official_reference`: a general official identifier for references such as `COM(2021) 206 final`, `SWD(2021) 84 final`, `ST 15698/22` and `P9_TA(2023)0236`;
- `procedure_references`: zero or more procedure identifiers such as `2021/0106(COD)`;
- `oj_reference`: the Official Journal citation where one exists;
- `document_date`: the date stated on, adopted for or formally assigned to the document;
- `version_label`: a concise official or editorial version label where applicable; and
- `version_status`: `draft`, `revised`, `final`, `consolidated` or `not_applicable`.

The controlled document-type vocabulary expands to support at least:

- `staff_working_document`
- `institutional_position`
- `opinion`
- `resolution`
- `decision`
- `implementing_regulation`
- `guidelines`
- `code_of_practice`
- `template`
- `report`
- `standardisation_request`

The existing types remain valid for backward compatibility.

### 3.3 Events

Events represent dated procedural or legal changes, not duplicate document records. Examples include a political agreement, formal adoption, entry into force, the beginning of application of particular obligations, a withdrawal and the launch or close of a consultation.

### 3.4 Relationships

The relationship vocabulary expands with:

- `version_of`
- `annex_to`
- `revises`
- `endorses`
- `procedural_step_for`

Existing relationship types remain valid. Official and analytical relationship bases continue to be distinguished, and every published relationship requires an official evidence source.

### 3.5 Sources and snapshots

Source records identify the official evidence used for metadata and relationship verification. The source vocabulary will accommodate official institutional registers and webpages without treating a press page as the underlying policy text.

A snapshot is created only when the actual bytes of a file have been retrieved and hashed. Historical versions must be represented as document records and relationships, not simulated by snapshot metadata.

## 4. Identity, Deduplication and Versioning

Deduplication uses the strongest available combination of:

1. CELEX;
2. ELI;
3. official reference;
4. language;
5. version label; and
6. issuing institution.

Titles alone are not sufficient for identity. A main document and its annex are distinct when they are independently citable or contain materially distinct research content. A single instrument delivered as several complementary chapters may be represented by one principal record plus component document records.

Final documents do not overwrite draft or superseded records. Version relationships preserve the sequence and make status differences visible.

`document_date` and `publication_date` must not be conflated. `document_date` records the date printed on or formally assigned to the instrument, while `publication_date` records its first official publication or public release. For Official Journal acts, `publication_date` is the Official Journal date. Adoption, entry into force and application dates remain separate events. For example, Regulation (EU) 2024/1689 has a document date of 13 June 2024, an Official Journal publication date of 12 July 2024 and an entry-into-force event on 1 August 2024.

## 5. Verification and Publication

The evidence hierarchy is:

1. EUR-Lex or ELI;
2. an official register or publication page of the issuing EU institution or body;
3. an official EU-hosted PDF or downloadable file; and
4. an official EU explanatory page used only for facts it directly supports.

A record may enter the public corpus only when its title, date, institution, identifier where available, status and official source have been verified. Public consultation drafts may be published as corpus records when their draft status is explicit and verified. Unresolved records remain `pending_review` and do not enter generated public JSON, SQLite or site output.

Researcher-authored fields remain separate from official metadata. Official summaries stay `null` unless a source provides a clearly attributable official abstract or summary.

## 6. Corpus Inventory

The repository will include an English-language corpus inventory covering every candidate identified by the source sweep. Each inventory entry records:

- official reference;
- official title;
- year;
- issuing institution;
- record level;
- version;
- official source URL;
- decision: `included`, `merged`, `excluded` or `pending`; and
- a concise reason.

The inventory provides an auditable account of completeness even when a candidate does not enter the published corpus.

## 7. Public Atlas Behaviour

The atlas retains its established visual language and existing routes. All seven existing document URLs must continue to resolve.

The Corpus page will add:

- a default `Principal documents` view;
- an `All files and versions` view;
- filters for record level, version status and policy process; and
- coverage counts that distinguish principal documents from supporting files and versions.

Document pages will expose parent or principal document, annex relationships, previous and next versions, official reference, version label and record level where applicable.

The Timeline continues to combine documents and events without representing the same procedural fact twice. The Policy Map uses the expanded relationship vocabulary and retains a readable text alternative.

Coverage copy will state:

- `Coverage: 2018–2026`;
- the most recent verification date;
- counts for principal instruments and supporting files or versions; and
- that pending-review records are excluded from public totals.

## 8. Migration and Compatibility

The seven existing documents retain their IDs and slugs. New required document fields receive explicit migrated values in the existing records. Generated outputs remain deterministic.

Schema, SQL generation, public export, TypeScript types, filters and pages must be updated together. The migration must not introduce local paths, credentials or unpublished records into public artefacts.

## 9. Verification Strategy

Implementation follows test-driven development. Tests must first describe:

- the expanded controlled vocabularies;
- the new required document fields;
- identity and version constraints;
- relationship validation;
- preservation of all existing routes;
- principal-versus-all filtering;
- coverage counts and date copy;
- exclusion of pending records from public output; and
- deterministic JSON and SQLite generation.

Verification includes Python tests, web unit tests, a production build, the public-build scanner, responsive browser checks, accessibility checks and the GitHub Actions/Pages result after publication.

## 10. Completion Criteria

The expansion is complete when:

- every scoped official source family has been swept;
- every discovered candidate has an inventory decision;
- all included records have verified official evidence;
- the database and atlas expose the expanded corpus without overwhelming the default view;
- no previously published route regresses;
- all local checks and remote workflows pass; and
- the live GitHub Pages site reflects the verified 2018–2026 corpus.
