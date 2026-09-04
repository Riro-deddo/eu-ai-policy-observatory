# Comprehensive EU AI Document Corpus Design

**Date:** 4 September 2026  
**Status:** Approved in conversation; awaiting written-spec review  
**Project:** EU AI Policy Observatory

## 1. Objective

Expand the EU AI Policy Observatory from an AI Act-centred corpus into a comprehensive, auditable, English-language corpus of official European Union documents that substantively concern artificial intelligence between 1 January 2018 and the latest verified date in 2026.

The target is not merely a large collection. The project must be able to show which official source families were reviewed, which candidates were found, why each candidate was included, merged, excluded or left pending, and the date through which the claim was verified.

At the date of this design, the public description must use the following formulation:

> Comprehensive within the documented inclusion boundary, verified through 4 September 2026.

Later audit releases must replace that date with the exact value of the repository's `coverage_cutoff` field; they must never display a future or inferred date.

The project must not claim permanent or theoretical 100 per cent completeness.

## 2. Relationship to the Existing Corpus

This design broadens the research boundary defined in `2026-09-04-ai-act-corpus-expansion-design.md`. The existing AI Act legislative, implementation and amendment corpus remains a central policy pathway, but it becomes one part of a wider EU AI document corpus.

All existing document IDs, public slugs and routes remain stable. Existing official metadata and version relationships are preserved. The current corpus must be migrated to the new sector and provenance fields before new coverage claims are published.

## 3. Inclusion Boundary

An item is eligible when all of the following conditions are satisfied:

1. it was formally issued or published between 1 January 2018 and the current verified cutoff date in 2026;
2. it is publicly accessible and independently citable in English;
3. it was authored, adopted or formally published by an EU institution, body, agency, board or recognised EU expert group, or it was commissioned by the EU and formally published through an official EU source; and
4. artificial intelligence is a substantive subject, regulatory object or material sectoral issue in the document, rather than an incidental mention.

Formal publication, rather than final legal adoption, is the eligibility threshold. Official proposals, drafts, amendments, compromise texts, consultation documents and superseded versions therefore remain eligible when their status is explicit and verifiable.

### 3.1 Included material

Eligible material includes:

- legislation, delegated and implementing acts, consolidated texts and corrigenda;
- legislative proposals, institutional positions, amendments, compromise texts and independently citable procedural versions;
- communications, strategies, coordinated plans, declarations and recommendations;
- opinions and resolutions from EU institutions, bodies and agencies;
- judgments and other independently citable judicial materials substantively concerning AI;
- implementation guidelines, codes of practice, templates, technical specifications, standardisation requests and work programmes;
- consultation questionnaires, official consultation drafts, official summaries and final reports;
- EU-authored studies and reports;
- EU-commissioned external studies formally published through an official EU source; and
- annexes or attachments that are independently citable or contain materially distinct research content.

### 3.2 Sectoral scope

The corpus includes sector-specific EU documents in which AI is a substantive issue, including health, employment, migration, financial services, transport, defence and other fields listed in the controlled sector vocabulary.

### 3.3 Excluded material

The following do not become public document records:

- press releases, ordinary news pages, event announcements and FAQs that do not contain an independently citable document;
- search-result snippets, future publication announcements, rumours and drafts that have not been officially published;
- documents that merely mention AI in passing;
- other-language manifestations of an English record;
- duplicate mirrors of the same official version; and
- individual submissions from companies, citizens, academics, NGOs or other third parties to an EU consultation.

Excluded candidates remain in the research inventory with an explicit reason. Third-party consultation submissions use the inventory-only provenance value `third_party_submission`. Official consultation materials and EU-authored synthesis reports remain eligible.

## 4. Institutional Scope

The source universe covers all relevant EU institutions, bodies, agencies, boards and recognised expert groups, rather than only the Commission, Parliament and Council. It includes, where relevant:

- European Commission and European AI Office;
- European Parliament;
- Council of the European Union and European Council;
- Court of Justice of the European Union;
- European Economic and Social Committee;
- European Committee of the Regions;
- European Central Bank;
- European Data Protection Supervisor and European Data Protection Board;
- European Union Agency for Fundamental Rights;
- European Union Agency for Cybersecurity;
- Europol and other relevant justice and home-affairs bodies;
- European Union Intellectual Property Office;
- European Artificial Intelligence Board and Scientific Panel;
- Commission expert groups, including the High-Level Expert Group on AI; and
- other EU agencies or bodies that formally publish a document meeting the inclusion test.

This list is illustrative rather than a publication cap. Discovery of another EU body triggers a source-registry entry and the same review process.

## 5. Entity Model

The seven existing canonical entity types remain unchanged:

1. `policy`
2. `document`
3. `event`
4. `concept`
5. `institution`
6. `relationship`
7. `source`

Sector and provenance classifications are controlled, multi-valued document fields rather than additional top-level entities. This keeps their purpose distinct from research concepts and policy-process membership.

### 5.1 Sector tags

Every published document must contain a non-empty, unique `sector_tags` array. The initial controlled vocabulary is:

- `general_cross_sector`
- `health`
- `employment_and_labour`
- `migration_asylum_and_border_management`
- `financial_services`
- `transport_and_mobility`
- `defence_and_security`
- `law_enforcement`
- `justice`
- `education`
- `public_administration`
- `consumer_protection`
- `media_and_culture`
- `intellectual_property`
- `research_and_innovation`
- `industry_and_manufacturing`
- `agriculture_and_environment`
- `critical_infrastructure`
- `cybersecurity`
- `competition_and_markets`

Sector tags are researcher classifications. A document may have multiple sector tags. `general_cross_sector` is used when the document is substantively cross-sectoral; it is not a fallback for unreviewed classification.

### 5.2 Provenance tags

Every published document must contain a non-empty, unique `provenance_tags` array. The initial controlled vocabulary is:

- `eu_institution_authored`
- `eu_agency_or_body_authored`
- `eu_expert_group_authored`
- `eu_commissioned_external`
- `joint_institutional`
- `official_consultation_material`
- `officially_published`

These tags describe how the document was produced and entered the official EU publication record. They do not replace `institution_roles`, source records or named attribution. `officially_published` confirms the common eligibility threshold and may coexist with a more specific origin tag.

Candidate inventory records use the same provenance vocabulary plus the inventory-only values `third_party_submission` and `unknown_pending_review`. Neither inventory-only value is valid on a published document.

Document pages must display production provenance, official publisher and official hosting source as separate facts.

### 5.3 Document types

The controlled document-type vocabulary gains:

- `study`
- `consultation_document`
- `declaration`
- `recommendation`
- `judgment`
- `briefing`
- `technical_specification`
- `work_programme`

Existing document types remain valid.

### 5.4 Official issuance and legal status

The public corpus contains only records whose official existence and publication have been verified. Formal issuance must not be conflated with legal adoption or entry into force. Existing `publication_status`, `version_status` and `legal_status` fields continue to express these separate states.

A formally published draft may therefore be `published`, `draft` and `non_binding` at the same time. An adopted regulation may be `published`, `final` and `in_force`. The combination must be validated rather than inferred from a single generic status.

## 6. Identity, Deduplication and Versioning

Candidate identity is resolved using the strongest available combination of:

1. CELEX;
2. ELI;
3. official reference;
4. procedure reference;
5. issuing institution;
6. document date;
7. language;
8. version label; and
9. file-level hash when the official bytes have been retrieved.

Titles alone never establish identity. An official main text and an independently citable annex are separate records. An official draft, revised draft and final document remain separate when each is independently citable. They are connected through verified `version_of`, `revises`, `supersedes`, `adopted_as`, `annex_to` or other appropriate relationships.

Duplicate mirrors and alternative official landing pages are represented as additional source evidence for one document, not duplicate document records.

## 7. Hybrid Source Registry

The project uses a hybrid workflow: structured source discovery plus human verification and classification.

### 7.1 Source families

The source registry covers, at minimum:

- EUR-Lex and Cellar;
- European Parliament Legislative Observatory and document register;
- Council public register and official document repository;
- European Commission policy libraries and departmental publication pages;
- Publications Office catalogues;
- Have Your Say and other official consultation registers;
- CURIA;
- Commission register of expert groups;
- AI Office, AI Board and Scientific Panel publication pages; and
- official publication pages or registers maintained by relevant EU bodies and agencies.

### 7.2 Source-registry fields

Every registered source family records:

- stable source ID;
- institution or body;
- source-family name;
- official entry URL;
- covered date range;
- covered document types;
- covered sectors where the source is sector-specific;
- discovery or query method;
- last scan timestamp;
- coverage cutoff;
- scan status;
- reviewer; and
- a verification note describing limitations or access failures.

Scan status uses `not_started`, `in_progress`, `reviewed`, `gap_found` or `recheck_due`. `reviewed` means the documented method was completed for the stated cutoff, not that the source will never publish another relevant document.

## 8. Candidate Inventory and Decision Workflow

Every discovered candidate enters the inventory before publication. Candidate records gain:

- discovery source IDs;
- official identifier and title where available;
- issuing or commissioning body;
- candidate provenance;
- provisional sector tags;
- discovery timestamp;
- review timestamp and reviewer;
- decision: `included`, `merged`, `excluded` or `pending`;
- decision reason;
- matched document ID or merge target where applicable; and
- official evidence URL.

The processing pipeline is:

```text
Discovered
-> official existence verified
-> identity and version checked
-> inclusion decision recorded
-> sector and provenance classified
-> relationships validated
-> published
```

Unverified and pending candidates are excluded from generated public JSON, SQLite and website output. A source failure or ambiguous identity produces a pending decision with a concrete explanation; it does not permit guessed metadata.

## 9. Coverage Matrix and Completeness Claim

Coverage is reported across source family, institution or body, date range, document type and sector. The matrix is generated from the source registry and candidate inventory rather than maintained as an unsupported percentage.

An audit cycle may be described as reviewed through its cutoff only when:

- every in-scope source family has a completed documented query or review;
- every discovered candidate has an inclusion, merge, exclusion or explicit pending decision;
- pending candidates are counted and publicly disclosed;
- legislative procedures and cited document chains have been reconciled against their official registers;
- cross-source duplicate and version checks have been run; and
- reverse searches and citation-chain spot checks have not found unregistered eligible documents.

The public coverage statement must include the exact cutoff date and unresolved-candidate count. A source-level status such as `30/30 reviewed` must not be presented as proof of record-level completeness.

## 10. Public Atlas Behaviour

The existing six-page information architecture and visual language remain. No unrelated redesign is part of this work.

### 10.1 Corpus page

The Corpus page gains filters for:

- sector;
- provenance;
- institution;
- document type;
- policy process;
- year;
- legal or version status; and
- record level.

The default view remains `Principal documents`, with a prominent `All documents and versions` control. Document cards display concise sector and provenance labels.

### 10.2 Document pages

Every document page displays:

- sector tags;
- research concepts;
- policy-process membership;
- document provenance;
- official author, adopter, commissioner or publisher roles;
- official source;
- record and version status;
- previous, next, parent, annex and related records where applicable; and
- last verification date.

Researcher classification and official metadata remain visually and semantically distinct.

### 10.3 Timeline and methodology

The Timeline continues to prioritise principal records while allowing visitors to reveal all official versions. The Methodology page exposes the documented boundary, coverage cutoff, source-family status, included and excluded counts, and unresolved-candidate count.

All existing public routes must continue to resolve.

## 11. Implementation Sequence

Implementation is divided into three independently verifiable stages.

### Stage 1: Schema and interface

- add sector and provenance vocabularies and required document fields;
- extend document types;
- extend source-registry and candidate-inventory structures;
- migrate and classify all existing published records;
- update SQLite generation, public export and TypeScript types;
- add filters and document-page presentation; and
- replace ambiguous coverage copy with cutoff-based reporting.

### Stage 2: Priority backfill

- add the already confirmed missing AI Act and Digital Omnibus procedural versions;
- add directly related AI liability, implementation and governance materials;
- add confirmed Commission studies and formal institutional opinions; and
- reconsider previously excluded independently citable parliamentary amendments under the broadened boundary.

### Stage 3: EU-wide sweep

- register and review all relevant EU institutions, bodies, agencies and expert groups;
- sweep every year from 2018 through the cutoff;
- sweep both cross-sector and sector-specific AI material;
- resolve every discovered candidate; and
- publish an updated coverage matrix only after the audit criteria are met.

## 12. Verification Strategy

Implementation follows test-driven development. Tests must cover:

- the controlled sector and provenance vocabularies;
- required non-empty tags on every published document;
- expanded document types;
- valid combinations of publication, version and legal status;
- official-host and verification requirements;
- identity, deduplication and version relationships;
- inventory decision integrity;
- exclusion of pending and unverified candidates from public output;
- source-registry cutoff and scan-state validation;
- coverage-matrix generation;
- all new filters;
- preservation of existing routes;
- deterministic JSON and SQLite generation;
- responsive rendering, keyboard use and accessibility; and
- GitHub Pages production output.

Before publication, verification includes the complete Python test suite, web unit tests, production build, public-build scanner, browser checks at desktop and mobile widths, and remote GitHub Actions/Pages status.

## 13. Completion Criteria

The expansion is complete for the stated coverage cutoff when:

- the schema, source registry, inventory, SQLite database and public JSON agree;
- every published document has verified official evidence, sector tags, provenance tags and a verification date;
- all existing corpus records have been migrated;
- every registered official source family has been reviewed through the cutoff;
- every discovered candidate has a recorded decision;
- unresolved candidates are absent from public records and disclosed in coverage reporting;
- duplicate identities and unexplained version gaps have been eliminated;
- existing public routes remain valid;
- all local and remote verification checks pass; and
- the live GitHub Pages site shows the exact coverage cutoff and auditable scope statement.
