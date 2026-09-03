# EU AI Policy Observatory — Design Specification

**Date:** 3 September 2026

**Status:** Approved design, pending implementation plan

**Project owner:** Yichen Hao

## 1. Purpose

The EU AI Policy Observatory will be an English-language research database and public browsing interface for a verified corpus of European Union artificial intelligence policy documents. The database is the primary research output. The interface exists to make the database legible, searchable, citable and easy to demonstrate from any device.

The project supports the Year One corpus-building work described in the research proposal *Governing with Generative AI: Large Language Models and the Reinterpretation of EU AI Policy*. It does not yet implement the proposal's LLM experiments. It establishes the policy, document, event, concept, relationship and provenance infrastructure that those experiments may use later.

The project will be hosted in a GitHub repository and its read-only interface will be deployed through GitHub Pages.

## 2. Product Principles

1. **Database first.** The structured corpus is the project; the website is a view of it.
2. **Policy is not document is not event.** A policy process, a text produced within that process and a regulatory milestone are separate entities.
3. **Official is not analytical.** EU-supplied facts and relationships must never merge silently with researcher-authored classifications or interpretations.
4. **Evidence before display.** Public records must have traceable provenance and an explicit publication status.
5. **Stable and reproducible.** Identifiers remain stable, retrieval events are timestamped and historical snapshots are not overwritten.
6. **English by default.** Repository content, data, code, documentation and the public interface are written in British academic English. A Chinese-English glossary may be kept in private working notes but will not be deployed or treated as canonical data.
7. **Static first.** Version 0.1 must run without an application server, hosted database service or paid API.

## 3. Intended Audience

The primary audience is academic supervisors, doctoral reviewers and conference audiences. A secondary audience consists of researchers, policy professionals and members of the public who need a guided introduction to EU AI policy but may not know EUR-Lex conventions.

The public identity is project-led rather than affiliation-led. The interface will use:

> EU AI Policy Observatory
>
> Created and maintained by Yichen Hao.

No university affiliation will be stated unless the project owner later authorises a verified affiliation.

## 4. Scope

### 4.1 Version 0.1 includes

- A normalised, version-controlled research dataset.
- A generated SQLite database that can be downloaded and queried.
- A verified seed corpus of approximately six to ten foundational EU AI policy documents.
- Policies, documents, events, concepts, institutions, sources and explicit relationships.
- Researcher-authored corpus assessments separated from official metadata.
- A static, read-only browsing interface.
- Search, sorting and filters that operate locally in the browser.
- Policy map and timeline views derived from the database.
- Individual, stable document pages.
- Methodology, provenance and authorship documentation.
- Automated validation, database generation, website generation and GitHub Pages deployment.

### 4.2 Version 0.1 excludes

- LLM prompt management or model execution.
- LLM output storage or qualitative coding interfaces.
- A think-tank or media interpretation corpus.
- User accounts, comments or collaborative editing in the website.
- A server-side database or API.
- Automated large-scale EUR-Lex or Cellar ingestion.
- Automatic publication of unreviewed records.
- Payment, analytics, tracking or collection of visitor data.
- Replication of large collections of EU PDFs inside the repository.

## 5. Seed Corpus

The initial candidates are:

1. *Artificial Intelligence for Europe* (2018).
2. *Coordinated Plan on Artificial Intelligence* (2018).
3. *Ethics Guidelines for Trustworthy AI* (2019).
4. *White Paper on Artificial Intelligence: A European Approach to Excellence and Trust* (2020).
5. The European Commission proposal for the Artificial Intelligence Act (2021).
6. The European Commission proposal for an Artificial Intelligence Liability Directive (2022).
7. Regulation (EU) 2024/1689, the Artificial Intelligence Act (2024).

This is a candidate list, not a claim that every record is already verified. Each item must pass the publication workflow before appearing in the public corpus. The empirical timeline for Version 0.1 is 2018–2024, matching the proposal's initial corpus boundary.

## 6. Information Architecture

The public interface contains six top-level pages.

### 6.1 Home

- Project argument.
- Four research lenses: risk, trustworthiness, accountability and compliance.
- Core policy pathway.
- Database-derived summary content only; no manually maintained or speculative metrics.

### 6.2 Policy Map

- Policy families.
- Official and analytical relationships.
- Solid links for official relationships and dashed links for analytical relationships.
- A text-list alternative for accessibility and citation.
- Nodes linking to stable policy or document pages.

### 6.3 Timeline

- Policy documents and regulatory events from 2018 to 2024.
- Filters for institution, document type, policy stage and event type.
- Events generated from database records rather than hard-coded in the page.

### 6.4 Corpus

- Searchable and sortable list of published documents.
- Filters for title, year, institution, document type, legal status, policy stage, concept and corpus tier.
- Individual document pages at stable URLs.

Each document page displays:

- Official title.
- Short title.
- Document type.
- Institution and institutional role.
- Publication date.
- Status.
- CELEX and ELI identifiers when available.
- Language.
- Official source links.
- Policy stage.
- Core concepts.
- Inclusion rationale.
- Relationships.
- Verification status and last verification date.

Official metadata and the researcher-authored corpus assessment must appear as visibly separate sections.

### 6.5 Methodology

- Corpus inclusion criteria.
- Verification and provenance rules.
- Distinction between official metadata and analytical judgement.
- Planned LLM comparison protocol, described as future research rather than implemented functionality.

### 6.6 About

- Project purpose.
- Scope and limitations.
- “Created and maintained by Yichen Hao.”
- No unverified institutional affiliation.

## 7. Technical Architecture

The canonical source is a collection of one-record-per-file JSON documents. JSON is chosen because it is machine-validatable, directly inspectable on GitHub and produces meaningful version-control diffs. The SQLite file is generated rather than manually edited.

```text
English JSON records
        ↓
JSON Schema and controlled-vocabulary validation
        ↓
Relational and provenance checks
        ↓
Generated SQLite database
        ↓
Published-data JSON export
        ↓
Astro static-site build with lightweight TypeScript enhancements
        ↓
GitHub Pages deployment
```

The website must not query SQLite at runtime. Static document pages are generated during the build, while browser-side search and filters use a published JSON export. The generated SQLite database remains available as a downloadable research artefact.

## 8. Repository Structure

```text
eu-ai-policy-observatory/
├── data/
│   ├── policies/
│   ├── documents/
│   ├── events/
│   ├── concepts/
│   ├── institutions/
│   ├── relationships/
│   └── sources/
├── schema/
│   ├── database.sql
│   ├── record.schema.json
│   └── controlled-vocabularies.json
├── generated/                 # build output; not committed
│   ├── eu-ai-policy-observatory.sqlite
│   └── public-data.json
├── web/
├── scripts/
├── tests/
├── docs/
│   ├── methodology.md
│   └── data-dictionary.md
└── .github/workflows/
```

The generated files are not committed. Local builds place them in `generated/`. GitHub Actions uploads them as workflow artefacts, and the deployment copies the SQLite database to the Pages output as `/downloads/eu-ai-policy-observatory.sqlite`. A tagged release may attach the same generated database without changing the canonical-data rule.

## 9. Data Model

Every canonical record uses a common editorial envelope:

- `id`
- `publication_status`: `draft`, `pending_review`, `verified` or `published`
- `created_at`
- `updated_at`

Entity-specific legal or policy status fields are named explicitly and must not be confused with `publication_status`.

### 9.1 Core entities

#### Policy (`policies`)

- `id`
- `name`
- `short_name`
- `summary`
- `policy_family`
- `policy_status`
- `scope_note`

#### Document (`documents`)

The table contains objectively verifiable document data only.

- `id`
- `slug`
- `official_title`
- `short_title`
- `document_type`
- `publication_date`
- `legal_status`
- `celex`
- `eli`
- `language`
- `official_summary`

#### Event (`events`)

- `id`
- `event_type`
- `event_date`
- `title`
- `description`
- `policy_id`
- `document_id`, nullable
- `source_id`

#### Concept (`concepts`)

- `id`
- `name`
- `definition`
- `research_scope`
- `eurovoc_uri`, nullable
- `notes`

#### Relationship (`relationships`)

- `id`
- `source_entity_type`
- `source_entity_id`
- `target_entity_type`
- `target_entity_id`
- `relationship_type`
- `basis`: `official` or `analytical`
- `rationale`
- `evidence_source_id`
- `verification_status`

Entity references in the polymorphic relationship table are checked by the build validator before SQLite generation.

#### Source (`sources`)

- `id`
- `source_type`
- `url`
- `publisher`
- `retrieved_at`
- `last_verified_at`
- `verification_note`

### 9.2 Supporting entities

#### Corpus assessment (`corpus_assessments`)

- `document_id`
- `corpus_tier`
- `policy_stage`
- `inclusion_rationale`
- `researcher_notes`
- `review_status`
- `reviewed_by`
- `reviewed_at`

This table prevents researcher judgement from being presented as official metadata.

#### Institution (`institutions`)

- `id`
- `official_name`
- `short_name`
- `institution_type`
- `official_url`

#### Document–institution (`document_institutions`)

- `document_id`
- `institution_id`
- `role`

#### Document snapshot (`document_snapshots`)

- `id`
- `document_id`
- `source_id`
- `retrieved_at`
- `format`
- `content_hash`
- `archived_path`, nullable

A proposal, parliamentary position and final regulation remain separate documents. A snapshot records a retrieved representation of one document and must not be used to collapse distinct legal documents into “versions” of one record.

#### Junction tables

- `policy_documents`: policy to document.
- `document_concepts`: document to concept.
- `document_sources`: document to source.

### 9.3 Reserved extensions

The identifiers and relationships must allow later addition of `passages`, `llm_experiments`, `model_runs` and `qualitative_codings`, but those tables are not part of Version 0.1.

## 10. Controlled Vocabularies

The following fields use closed vocabularies validated during the build:

- `document_type`
- `legal_status`
- `policy_status`
- `policy_stage`
- `corpus_tier`
- `event_type`
- `relationship_type`
- `verification_status`
- `institution_role`
- `source_type`

The initial corpus tiers are:

- `core`
- `directly_related`
- `contextual`
- `excluded`

The initial institutional roles are:

- `author`
- `proposer`
- `adopter`
- `publisher`
- `contributor`

The initial event types are:

- `proposal`
- `publication`
- `adoption`
- `entry_into_force`
- `application`
- `amendment`
- `withdrawal`
- `implementation`

The initial relationship types are:

- `part_of`
- `precedes`
- `adopted_as`
- `replaces`
- `amends`
- `implements`
- `based_on`
- `related_to`
- `supersedes`

Vocabulary additions require a reviewed change to the canonical vocabulary file rather than ad hoc values in records.

## 11. Verification and Publication Workflow

Records move through four states:

```text
draft → pending_review → verified → published
```

- New records default to `draft` and are excluded from website exports.
- `pending_review` records may be committed to the repository but are not public website claims.
- `verified` records have the required official source, stable identifier or documented verification basis.
- `published` records are verified and intentionally approved for inclusion in GitHub Pages.
- An analytical relationship must have an English rationale.
- An official relationship must cite evidence from an official source.
- Earlier snapshots are retained when an official source changes.
- Dates use ISO 8601 `YYYY-MM-DD` format.
- Internal IDs remain unchanged if display titles change.

The public repository may expose draft JSON to technically sophisticated visitors. Every non-published record must therefore carry an unmistakable status, and the README must state that only records exported to the public site constitute the reviewed public corpus.

## 12. Validation and Error Handling

Every proposed change runs the following checks:

1. JSON syntax and JSON Schema validity.
2. Required fields.
3. Controlled-vocabulary values.
4. Unique internal IDs and slugs.
5. Duplicate CELEX and ELI identifiers when uniqueness is expected.
6. Existence of referenced policies, documents, sources, concepts and institutions.
7. Required provenance for verified and published records.
8. Required rationale and evidence rules for relationships.
9. SQLite foreign-key and integrity checks.
10. Successful public-data export.
11. Successful static-site build.

A failed check blocks deployment. The previously deployed website remains available. Error messages must identify the record, field and violated rule. Missing optional identifiers are displayed as “Not assigned” rather than guessed. An empty search result displays a clear English message and a reset action.

External URL syntax is validated on each change. Live URL availability is not a blocking commit check in Version 0.1 because official services may be temporarily unavailable or rate-limited.

## 13. Testing Strategy

### Data and database tests

- Unit tests for parsing and normalisation.
- Schema-validation fixtures for accepted and rejected records.
- Controlled-vocabulary tests.
- Duplicate and broken-reference tests.
- SQLite build and integrity tests.
- Tests that unpublished records never enter the public export.
- Deterministic-build test: identical source records produce identical logical database content.

### Website tests

- Static build smoke test.
- Navigation and stable-route tests.
- Corpus search, sorting and filter tests.
- Document-page rendering tests.
- Policy-map legend and text-alternative tests.
- Timeline filter tests.
- No-JavaScript readability check for core content.
- Keyboard navigation and basic automated accessibility checks.
- Responsive checks at narrow mobile, tablet and desktop widths.

## 14. Deployment and Security

GitHub Actions will use separate validation and deployment workflows. Deployment runs only after all checks pass and only exports records with `publication_status: published`.

The Pages deployment receives only the minimum permissions required to read repository contents and publish the static artefact. No credentials, model API keys or private research data are stored in the repository or browser bundle.

The default site address will be:

```text
https://<github-username>.github.io/eu-ai-policy-observatory/
```

A custom domain is outside Version 0.1. The repository and site will not include a reuse licence in Version 0.1; public visibility alone does not grant reuse rights. Licensing can be addressed in a separate, explicit decision.

## 15. Success Criteria

Version 0.1 is complete when:

1. The canonical English JSON records validate successfully.
2. The schema generates a valid SQLite database from a clean checkout.
3. The seed corpus contains at least six verified and intentionally published documents.
4. Every published document has provenance, verification metadata and a stable page.
5. Official metadata and corpus assessments are structurally and visually distinct.
6. Policy Map, Timeline and Corpus views are generated from the same canonical data.
7. Search and filters work without a server.
8. The website is usable on mobile and desktop.
9. GitHub Actions blocks invalid data and deploys valid published data to GitHub Pages.
10. A visitor can understand the project, inspect its methodology, browse the corpus and follow every published record back to an official source.

## 16. Approved Design Summary

Version 0.1 is a public, English-only, static research atlas backed by a generated relational database. It prioritises corpus integrity, provenance and the separation of official evidence from researcher judgement. It makes a small, verified 2018–2024 EU AI policy corpus available through six public views while avoiding premature LLM infrastructure, large-scale ingestion and server-side complexity.
