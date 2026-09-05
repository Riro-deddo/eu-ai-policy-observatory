# Data dictionary

Canonical records are UTF-8 JSON objects, one record per file. `Required` means required by `schema/record.schema.json`; optional fields may be omitted unless stated otherwise. `Official` means an EU-supplied fact or provenance link, `Analytical` means researcher classification or interpretation, and `System` means an editorial, identifier, validation or build field. Public repository visibility does not make a draft part of the reviewed corpus: only `published` records enter `public-data.json`.

## Common envelope (every entity)

| Field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| `id` | string | Yes | System | Lowercase hyphenated identifier: `^[a-z0-9]+(?:-[a-z0-9]+)*$`. |
| `entity_type` | string | Yes | System | Entity-specific constant: `policy`, `document`, `event`, `concept`, `institution`, `relationship`, `source`. |
| `publication_status` | string | Yes | System | `draft`, `pending_review`, `verified`, `published`. |
| `created_at` | offset ISO-8601 timestamp | Yes | System | Must not be after `updated_at`. |
| `updated_at` | offset ISO-8601 timestamp | Yes | System | Must not precede `created_at`. |

## Policy

| Field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| `name` | string | Yes | Analytical | Non-empty research-policy name. |
| `short_name` | string | Yes | Analytical | Non-empty abbreviation. |
| `summary` | string | Yes | Analytical | Research description. |
| `policy_family` | string | Yes | Analytical | Research grouping label. |
| `policy_status` | string | Yes | Analytical | `active`, `completed`, `withdrawn`, `superseded`. |
| `scope_note` | string | Yes | Analytical | Scope and classification note. |

## Document

| Field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| `slug` | string | Yes | System | Lowercase hyphenated stable public-route identifier; unique. |
| `official_title` | string | Yes | Official | Non-empty official title. |
| `short_title` | string | Yes | System | Non-empty display abbreviation. |
| `document_type` | string | Yes | Official | `communication`, `coordinated_plan`, `expert_guidelines`, `white_paper`, `legislative_proposal`, `regulation`, `staff_working_document`, `institutional_position`, `opinion`, `resolution`, `decision`, `implementing_regulation`, `guidelines`, `code_of_practice`, `template`, `report`, `standardisation_request`, `study`, `consultation_document`, `declaration`, `recommendation`, `judgment`, `briefing`, `technical_specification`, `work_programme`. |
| `record_level` | string | Yes | Analytical | `principal`, `supporting`, `version`, `attachment`. Principal records are the default public Corpus view; every other value contributes to `supporting_files_and_versions`. |
| `sector_tags` | array of strings | Yes | Analytical | Non-empty, unique researcher classifications from the 20-value sector vocabulary below. These are not official EU metadata. |
| `provenance_tags` | array of strings | Yes | Analytical | Non-empty, unique production-provenance classifications from the seven-value published vocabulary below. |
| `official_reference` | string or `null` | Yes | Official | General official reference, such as a COM or Council document number; `null` only where none is assigned. |
| `procedure_references` | array of strings | Yes | Official | Unique official procedure identifiers, for example `2021/0106(COD)`; may be empty. |
| `oj_reference` | string or `null` | Yes | Official | Official Journal reference where assigned; otherwise `null`. |
| `document_date` | ISO calendar date | Yes | Official | Date of the particular document text or formal version. Generated coverage and chronology use this date. |
| `version_label` | string or `null` | Yes | Official | Human-readable official version or stage label where one exists. Used in the composite identity after whitespace normalisation and case-folding. |
| `version_status` | string | Yes | Analytical | `draft`, `revised`, `final`, `consolidated`, `not_applicable`. This describes the represented text, not its editorial publication state. |
| `publication_date` | ISO calendar date | Yes | Official | Official publication or release date. It may differ from `document_date`; retained for source fidelity and compatibility. |
| `legal_status` | string | Yes | Official | `non_binding`, `proposed`, `adopted`, `in_force`, `withdrawn`, `superseded`. |
| `celex` | string or `null` | No | Official | Unique when non-null; only where assigned. |
| `eli` | string or `null` | No | Official | Unique when non-null; only where assigned. |
| `language` | string | Yes | Official | Exactly `en`. |
| `official_summary` | string or `null` | No | Official | Only an EU-supplied abstract or summary specifically evidenced by a cited source; otherwise `null`. Never full policy text or a researcher paraphrase. |
| `institution_roles` | array of `institution_role` | Yes | Official | Unique items; nested fields below. |
| `policy_ids` | array of string IDs | Yes | Analytical | Unique existing policy IDs. |
| `concept_ids` | array of string IDs | Yes | Analytical | Unique existing concept IDs. |
| `source_ids` | array of string IDs | Yes | Official | Unique existing source IDs; source evidence is required for published/verified documents. |
| `corpus_assessment` | `corpus_assessment` object | Yes | Analytical | Explicitly separate from official metadata; nested fields below. |
| `snapshots` | array of `snapshot` | No | Official | Add only for an actually retrieved official file with a real hash. |

### Document levels, versions and identity

`principal` identifies the main independently citable instrument or policy text. `supporting` identifies evidence or institutional material that accompanies the process. `version` preserves a formally distinct draft, revision, signed text or consolidated text. `attachment` is reserved for an independently citable annex or similar separate file. Use `annex_to`, `version_of` and `revises` relationships to make those roles explicit; do not create a second document merely for another file format or manifestation of the same text.

Document identity remains stable across filenames. In addition to unique `slug`, non-null `celex` and non-null `eli` values, validation rejects a duplicate document identity when records share all of the following: a non-null `official_reference`, `language`, a normalised `version_label`, and the same sorted issuing-institution IDs. Normalisation trims and collapses whitespace and compares the version label case-insensitively. Validation reports `duplicate_document_identity` against record paths without echoing the identifying values.

The Corpus and Timeline open in their principal-record views. The Corpus control labelled “All files and versions” and the Timeline control labelled “All documents and versions” deliberately expose all records, including supporting, version and attachment records. This view choice changes presentation only; it does not change publication eligibility.

### Document status dimensions

The three status fields answer different questions and must not be treated as synonyms:

| Field | Question answered | Meaning |
| --- | --- | --- |
| `publication_status` | May this repository entity enter generated public outputs? | Editorial state: `draft`, `pending_review`, `verified` or `published`. Only `published` is exported. |
| `version_status` | What kind of text or manifestation does this document record represent? | `draft`, `revised`, `final`, `consolidated` or `not_applicable`. A formally published draft can therefore have `publication_status: published` and `version_status: draft`. |
| `legal_status` | What is the instrument’s legal or procedural standing? | `non_binding`, `proposed`, `adopted`, `in_force`, `withdrawn` or `superseded`. Adoption or entry into force is not the corpus inclusion threshold. |

Formal publication by an official EU source, rather than adoption or entry into force, is the inclusion threshold. This permits officially published proposals, consultations, drafts and non-binding instruments when they otherwise satisfy the documented scope and evidence requirements.

### Sector tags

Sector tags are researcher classifications of substantive subject matter, not official EU metadata. Every canonical document has at least one value.

| Value | Meaning |
| --- | --- |
| `general_cross_sector` | General or cross-sector AI policy. |
| `health` | Health, medicine or healthcare systems. |
| `employment_and_labour` | Employment, workplace and labour relations. |
| `migration_asylum_and_border_management` | Migration, asylum and border management. |
| `financial_services` | Banking, insurance, payments or other financial services. |
| `transport_and_mobility` | Transport systems, vehicles and mobility. |
| `defence_and_security` | Defence and wider security policy. |
| `law_enforcement` | Policing, criminal investigation and law-enforcement activity. |
| `justice` | Courts, judicial administration and access to justice. |
| `education` | Education, training and learning. |
| `public_administration` | Public-sector administration and delivery of public services. |
| `consumer_protection` | Consumer rights, safety and redress. |
| `media_and_culture` | Media, cultural production and cultural participation. |
| `intellectual_property` | Copyright, patents and other intellectual-property matters. |
| `research_and_innovation` | Research policy, scientific activity and innovation support. |
| `industry_and_manufacturing` | Industrial policy, manufacturing and production. |
| `agriculture_and_environment` | Agriculture, climate and environmental governance. |
| `critical_infrastructure` | Essential infrastructure and essential-service systems. |
| `cybersecurity` | Cybersecurity, network resilience and information security. |
| `competition_and_markets` | Competition policy, market governance and platform markets. |

### Production provenance tags

Production provenance identifies how a document came into being. It remains separate from an institution’s named role and from the official source that hosts the evidence.

| Value | Meaning |
| --- | --- |
| `eu_institution_authored` | Authored by an EU institution. |
| `eu_agency_or_body_authored` | Authored by an EU agency, board, committee or other body. |
| `eu_expert_group_authored` | Authored by a formally constituted EU expert group. |
| `eu_commissioned_external` | Produced externally under a documented EU commission. |
| `joint_institutional` | Produced jointly by more than one named EU institution or body. |
| `official_consultation_material` | Formally published by an EU source as consultation material. |
| `officially_published` | Formally published through an official EU source. |

`third_party_submission` and `unknown_pending_review` are inventory-only provenance values. They may describe discovered candidates in `research/corpus-inventory.json`, but they are forbidden in canonical documents, SQLite, public JSON and the site.

### `institution_roles[]`

| Field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| `institution_id` | string | Yes | Official | Existing institution ID. |
| `role` | string | Yes | Official | `author`, `proposer`, `adopter`, `publisher`, `contributor`. |

### `corpus_assessment`

| Field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| `corpus_tier` | string | Yes | Analytical | `core`, `directly_related`, `contextual`, `excluded`. |
| `policy_stage` | string | Yes | Analytical | `agenda_setting`, `coordination`, `consultation`, `proposal`, `negotiation`, `adoption`, `implementation`. |
| `inclusion_rationale` | string | Yes | Analytical | Researcher justification. |
| `researcher_notes` | string | Yes | Analytical | Not official metadata. |
| `review_status` | string | Yes | System | `unverified`, `pending`, `verified`. |
| `reviewed_by` | string | Yes | System | Non-empty reviewer name or role. |
| `reviewed_at` | offset ISO-8601 timestamp | Yes | System | Offset required. |

### `snapshots[]`

| Field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| `id` | string | Yes | System | Lowercase hyphenated snapshot identifier. |
| `source_id` | string | Yes | Official | Existing source ID for the retrieved representation. |
| `retrieved_at` | offset ISO-8601 timestamp | Yes | System | Actual retrieval time. |
| `format` | string | Yes | Official | Retrieved representation format, for example `pdf`. |
| `content_hash` | string | Yes | System | Lowercase 64-hex SHA-256 calculated from actual retrieved bytes. |
| `archived_path` | string or `null` | Yes | System | `null` unless a deliberately committed archive exists; when set, a safe repository-relative POSIX path to an existing regular file whose SHA-256 matches `content_hash`. |

## Event, Concept and Institution

| Entity / field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| Event `event_type` | string | Yes | Official | `proposal`, `publication`, `adoption`, `entry_into_force`, `application`, `amendment`, `withdrawal`, `implementation`. |
| Event `event_date` | ISO calendar date | Yes | Official | Valid `YYYY-MM-DD`. |
| Event `title` | string | Yes | Official | Non-empty title. |
| Event `description` | string | Yes | Analytical | Concise editorial description tied to the source. |
| Event `policy_id` | string | Yes | Analytical | Existing policy ID. |
| Event `document_id` | string or `null` | Yes | Official | Existing document ID where applicable. |
| Event `source_id` | string | Yes | Official | Existing source ID; required for published/verified events. |
| Concept `name` | string | Yes | Analytical | Non-empty research-lens name. |
| Concept `definition` | string | Yes | Analytical | Researcher definition. |
| Concept `research_scope` | string | Yes | Analytical | Intended corpus use. |
| Concept `eurovoc_uri` | URI string or `null` | Yes | Official | Official EuroVoc URI where assigned. |
| Concept `notes` | string | Yes | Analytical | Interpretive/use note. |
| Institution `official_name` | string | Yes | Official | Non-empty official name. |
| Institution `short_name` | string | Yes | Official | Non-empty official short name. |
| Institution `institution_type` | string | Yes | Official | Non-empty official organisational type. |
| Institution `official_url` | HTTP(S) URI string | Yes | Official | Official HTTP or HTTPS location. |

## Relationship and Source

| Entity / field | Type | Required | Provenance | Vocabulary / constraint |
| --- | --- | --- | --- | --- |
| Relationship `source_entity_type` | string | Yes | System | `policy`, `document`, `event`, `concept`, `institution`, `relationship`, `source`. |
| Relationship `source_entity_id` | string | Yes | System | Existing typed endpoint ID. |
| Relationship `target_entity_type` | string | Yes | System | Same closed entity-type vocabulary. |
| Relationship `target_entity_id` | string | Yes | System | Existing typed endpoint ID. |
| Relationship `relationship_type` | string | Yes | Analytical | `part_of`, `precedes`, `adopted_as`, `replaces`, `amends`, `implements`, `based_on`, `related_to`, `supersedes`, `version_of`, `annex_to`, `revises`, `endorses`, `procedural_step_for`. |
| Relationship `basis` | string | Yes | Analytical | `official`, `analytical`. |
| Relationship `rationale` | string or `null` | Yes | Analytical | Non-empty when `basis` is `analytical`. |
| Relationship `evidence_source_id` | string or `null` | Yes | Official | Existing official source; analytical links require one. |
| Relationship `verification_status` | string | Yes | System | `unverified`, `pending`, `verified`. |
| Source `source_type` | string | Yes | System | `eur_lex`, `eli`, `commission_webpage`, `official_pdf`, `publications_office`, `council_register`, `parliament_register`, `official_register`, `official_consultation`. |
| Source `url` | HTTP(S) URI string | Yes | Official | Official HTTP or HTTPS source location. |
| Source `publisher` | string | Yes | Official | Non-empty issuing organisation. |
| Source `retrieved_at` | offset ISO-8601 timestamp | Yes | System | Actual retrieval time. |
| Source `last_verified_at` | offset ISO-8601 timestamp | Yes | System | Last metadata-verification time. |
| Source `verification_note` | string | Yes | System | Human-readable verification record. |

References are validated before SQLite generation. Published records may refer only to published records; published documents, events and relationships require source evidence. SQLite and public JSON are generated outputs, not canonical editing surfaces.

Official metadata, identifiers, document dates, institutional roles and official relationships must be transcribed from an inspectable official English source. Use an official HTTPS EUR-Lex, ELI, EU institution, Publications Office or official register/consultation URL with the matching controlled `source_type`. Record actual retrieval and verification timestamps and a useful verification note. `official_summary` remains `null` unless the cited institution supplies the summary. An analytical relationship still requires an official evidence source plus a researcher-written rationale, but its `basis` remains `analytical`.

## Source sweep and corpus inventory

The source sweep and inventory are checked-in audit records, not public entities. They make the bounded discovery method reviewable without querying live EU websites during a build.

### `research/source-sweep.json`

| Field | Type | Required | Constraint |
| --- | --- | --- | --- |
| `generated_at` | offset ISO-8601 timestamp | Yes | Timestamp for the audit-file revision. |
| `coverage_cutoff` | ISO calendar date | Yes | Exact last date covered by this audit revision; supplied by the audit, not inferred from the current clock or source-verification dates. |
| `sources[].id` | string | Yes | Unique lowercase hyphenated entrance ID. |
| `sources[].name` | string | Yes | Human-readable official entrance name. |
| `sources[].institution` | string | Yes | Responsible EU institution or office. |
| `sources[].source_family` | string | Yes | Stable human-readable grouping used for aggregate public coverage. |
| `sources[].url` | HTTPS URI string | Yes | Official discovery entrance. |
| `sources[].scope_note` | string | Yes | Bounded search scope used at that entrance. |
| `sources[].covered_from` / `covered_through` | ISO calendar dates | Yes | Bounded interval reviewed at the entrance; `covered_through` cannot exceed the cutoff. |
| `sources[].covered_document_types` | array of strings | Yes | Controlled document types. An empty `covered_document_types` array means the source review was not restricted by document type. |
| `sources[].covered_sector_tags` | array of strings | Yes | Controlled sector tags. An empty `covered_sector_tags` array means the source review was not restricted to a named sector; canonical documents still require sector tags. |
| `sources[].discovery_method` | string | Yes | Reproducible register, site or query method used for discovery. |
| `sources[].scan_status` | string | Yes | One of the five source-review states defined below. |
| `sources[].checked_at` | offset ISO-8601 timestamp | Yes | Time at which the entrance was checked. |
| `sources[].coverage_cutoff` | ISO calendar date | Yes | Per-entrance cutoff, no later than the file-level cutoff. |
| `sources[].reviewer` | string | Yes | Named reviewer. |
| `sources[].verification_note` | string | Yes | Human-readable evidence and limitations of the review. |

Source-review states have these meanings:

- `not_started`: the registered source family has not yet been reviewed through the cutoff.
- `in_progress`: review has begun but is not complete through the cutoff.
- `reviewed`: the documented bounded review completed through the stated cutoff.
- `gap_found`: review identified an unresolved coverage gap requiring follow-up.
- `recheck_due`: an earlier review exists but needs another bounded check.

A public source-family status is an aggregate. A family is `reviewed` only when every registered entrance in that family is reviewed; otherwise the aggregate uses the documented priority order `gap_found`, `recheck_due`, `in_progress`, then `not_started`.

### `research/corpus-inventory.json`

Every candidate has `id`, `source_ids`, `official_reference`, `official_title`, `year`, `issuing_institution`, `commissioning_body`, `record_level`, `version_label`, `candidate_provenance`, `provisional_sector_tags`, `official_source_url`, `decision`, `decision_reason`, `document_id`, `merged_into_document_id`, `discovered_at`, `reviewed_at` and `reviewed_by`, plus the file-level `generated_at` timestamp. Candidate IDs are unique, source IDs must exist in the source sweep, and the official candidate URL must use HTTPS. The candidate provenance vocabulary consists of the seven published provenance values plus the two inventory-only values defined above.

| Decision | Required linkage | Meaning |
| --- | --- | --- |
| `included` | `document_id` names a matching canonical document; `merged_into_document_id` is `null`. | The candidate is represented as its own canonical document record. |
| `merged` | `merged_into_document_id` names the canonical record; `document_id` is `null`. | Another manifestation or duplicate candidate is represented by an existing record. |
| `excluded` | Both document links are `null`. | A reasoned scope, language, document-status or evidence decision keeps it outside the corpus. |
| `pending` | Both document links are `null`. | Verification is unresolved. The candidate remains auditable but cannot enter public output. |

Every candidate needs a non-empty decision reason. An `included` or `merged` decision requires a canonical match, reviewed metadata and non-empty provisional sectors. An `excluded` decision requires completed review but no document link. A `pending` decision has no document link, may use `unknown_pending_review`, and may have an empty provisional sector list. Pending inventory candidates and all canonical records below `publication_status: published` are excluded from public JSON, SQLite, site routes and coverage totals.

## Generated public distribution

The deterministic build writes `generated/public-data.json` and `generated/eu-ai-policy-observatory.sqlite`. They are derived release artefacts and must never be edited directly; canonical JSON, research audit data and source code remain the editing surfaces. The static atlas consumes the public JSON at build time, and the Pages publication artefact carries the SQLite database as a downloadable research artefact.

Only records with `publication_status: published` and their published dependencies enter these generated public outputs. Canonical repository records may legitimately remain in `draft`, `pending_review` or `verified` editorial states, but they are outside the reviewed public corpus until intentional publication.

The public JSON also contains a generated `coverage` object:

| Field | Derivation |
| --- | --- |
| `from_year` / `to_year` | Earliest and latest year among published documents’ `document_date` values; `null` for an empty corpus. |
| `published_documents` | All published canonical document records. |
| `principal_documents` | Published documents whose `record_level` is `principal`. |
| `supporting_files_and_versions` | Published documents whose `record_level` is `supporting`, `version` or `attachment`. |
| `last_verified_date` | Most recent calendar date among exported official sources’ `last_verified_at` values; `null` when no source is exported. |
| `coverage_cutoff` | Exact audit cutoff copied from `research/source-sweep.json`; never computed from the current clock. |
| `coverage_statement` | Human-readable bounded-completeness statement generated from the exact cutoff. |
| `source_families.total` / `source_families.by_status` | Aggregate registered family count and zero-filled counts for the five source-review states. These counts do not prove record-level completeness. |
| `inventory` | Aggregate candidate decision counts for `included`, `merged`, `excluded` and `pending`; no candidate details are exposed. |
| `unresolved_candidates` | Number of inventory candidates whose decision remains `pending`. |

The Pages artefact exposes the generated SQLite database at [`downloads/eu-ai-policy-observatory.sqlite`](https://riro-deddo.github.io/eu-ai-policy-observatory/downloads/eu-ai-policy-observatory.sqlite). The file must be copied into `web/dist/downloads/` after the web build and before the public scanner runs with `--require-database`.

## Validation commands

Run from the repository root after installing the Python and web dependencies:

```powershell
python -m pytest -q
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
pnpm --dir web test
pnpm --dir web build
New-Item -ItemType Directory -Force web/dist/downloads
Copy-Item generated/eu-ai-policy-observatory.sqlite web/dist/downloads/eu-ai-policy-observatory.sqlite
python scripts/check_public_build.py --site web/dist --data generated/public-data.json --require-database
python scripts/check_repository_english.py --root .
```

The Python suite checks schema, controlled vocabulary, composite identity, references, provenance, source-sweep and inventory contracts. `observatory-build` validates before atomically replacing generated outputs. Web tests and the public scanner check public-only rendering, routes, downloadable SQLite integrity, common credential markers and local-path leakage. The repository script guard scans Git-tracked UTF-8 text, decoded JSON strings and path names for letters from non-Latin scripts while allowing accented Latin names, digits, punctuation, symbols and machine identifiers. This automated script-policy check is enforced by validation and deployment workflows; it cannot semantically identify English among Latin-script languages, so human English copy review remains required.
