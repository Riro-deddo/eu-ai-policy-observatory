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
| `source_ids` | array of string IDs | Yes | Evidence | Unique existing source IDs; official evidence is required for published/verified documents. The bounded Opinion 15 supplement below is explicitly non-official. |
| `retained_route_notice` | object | No | System | Non-null editorial notice for the three reviewed draft-guideline section routes whose whole-work parent relationship remains unresolved. Public document records always expose this property, using `null` when absent. |
| `corpus_assessment` | `corpus_assessment` object | Yes | Analytical | Explicitly separate from official metadata; nested fields below. |
| `snapshots` | array of `snapshot` | No | Evidence | Add only for an actually retrieved file with a real hash; non-official preserved copies require the bounded supplement approval below. |

### Document levels, versions and identity

`principal` identifies the main independently citable instrument or policy text. `supporting` identifies evidence or institutional material that accompanies the process. `version` preserves a formally distinct draft, revision, signed text or consolidated text. `attachment` is reserved for an independently citable annex or similar separate file. Use `annex_to`, `version_of` and `revises` relationships to make those roles explicit; do not create a second document merely for another file format or manifestation of the same text.

Document identity remains stable across filenames. In addition to unique `slug`, non-null `celex` and non-null `eli` values, validation rejects a duplicate document identity when records share all of the following: a non-null `official_reference`, `language`, a normalised `version_label`, and the same sorted issuing-institution IDs. Normalisation trims and collapses whitespace and compares the version label case-insensitively. Validation reports `duplicate_document_identity` against record paths without echoing the identifying values.

The Corpus and Timeline open in their principal-record views. The Corpus control labelled “All files and versions” and the Timeline control labelled “All documents and versions” deliberately expose all records, including supporting, version and attachment records. This view choice changes presentation only; it does not change publication eligibility.

### `retained_route_notice`

A retained-route notice is an attributed editorial disclosure, not official EU metadata, authorship, a relationship, or evidence that lineage has been resolved. The first reviewed contract is limited to the three published draft high-risk-classification guideline sections already present at their stable routes. While their missing whole-work parent condition remains, each must carry the notice; admitting a genuine parent and valid evidenced lineage makes the notice stale and requires its explicit removal. Other records cannot use the field to bypass evidence or relationship gates.

| Field | Type | Required when notice is present | Provenance | Constraint |
| --- | --- | --- | --- | --- |
| `status` | string | Yes | System | Exactly `parent_relationship_under_review`. |
| `reason` | string | Yes | Analytical | Nonblank English explanation that the route is retained while the whole-work parent remains unadmitted; draft status remains unchanged. |
| `reviewed_by` | string | Yes | System | Named editorial reviewer; `Codex` for this reviewed batch, distinct from the original metadata reviewer. |
| `reviewed_at` | offset ISO-8601 timestamp | Yes | System | Must satisfy `created_at <= reviewed_at <= updated_at`. |
| `evidence` | ordered array | Yes | Official | At least the common Commission landing page and the section's own PDF; source IDs must be distinct, declared by the document, and resolve uniquely to published official HTTPS sources. |
| `evidence[].source_id` | string | Yes | Official | Existing canonical source ID. |
| `evidence[].locator` | string | Yes | System | Nonblank bounded locator for the reviewed source passage or pages. |

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
| Source `source_type` | string | Yes | System | `eur_lex`, `eli`, `commission_webpage`, `official_pdf`, `publications_office`, `council_register`, `parliament_register`, `official_register`, `official_consultation`, `institutional_archive`. The last value is not an official EU source type. |
| Source `url` | HTTP(S) URI string | Yes | Evidence | Source location; published evidence requires approved HTTPS sources. |
| Source `publisher` | string | Yes | Evidence | Non-empty publisher or hosting organisation; an academy archive host must not be represented as an EU publisher. |
| Source `retrieved_at` | offset ISO-8601 timestamp | Yes | System | Actual retrieval time. |
| Source `last_verified_at` | offset ISO-8601 timestamp | Yes | System | Last metadata-verification time. |
| Source `verification_note` | string | Yes | System | Human-readable verification record. |

References are validated before SQLite generation. Published records may refer only to published records; published documents, events and relationships require source evidence. SQLite and public JSON are generated outputs, not canonical editing surfaces.

Official metadata, identifiers, document dates, institutional roles and official relationships must be transcribed from an inspectable official English source. Use an official HTTPS EUR-Lex, ELI, EU institution, Publications Office or official register/consultation URL with the matching controlled `source_type`. Record actual retrieval and verification timestamps and a useful verification note. `official_summary` remains `null` unless the cited institution supplies the summary. An analytical relationship still requires an official evidence source plus a researcher-written rationale, but its `basis` remains `analytical`.

### Approved Opinion 15 preserved-original supplement

On 6 September 2026 the maintainer approved one bounded exception to the source-location rule above: the original first edition of Scientific Opinion No. 15 may use the inspected ALLEA and KNAW preserved PDFs together with the independent Commission release announcement. The original and corrected editions remain separate records. This is not a general relaxation for academy-hosted documents.

The `institutional_archive` type remains non-official. The gate pins the original document ID, both permitted archive source IDs and URLs, their recorded PDF hashes, and the exact, uniquely resolved, published Commission companion. The preserved originals may support the original issue date, imprint, authorship, non-binding status and substantive classifications. They cannot support a publication-kind primary date, publication dates, `officially_published` provenance, an `official_host` role, events or relationship evidence. The corrected edition's official PDF supports an explicitly analytical `revises` relationship; no official correction schedule is claimed.

Snapshot `archived_path` may be `null`: the offline build checks recorded metadata, not live remote bytes. The hashes describe the files inspected in the dated evidence review. Academy copies are labelled as supplementary preserved originals in the public record. The earlier [research-only memo](../research/verification/2026-09-06-science-opinion-followup.md) remains a historical account of the pre-approval evidence pass; the subsequent [admission record](../research/admission/2026-09-06-science-opinion-admission/report.md) records implementation and verification.

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
| `sources[].covered_document_types` | array of strings | Yes | Controlled document types. In a legacy entry, an empty `covered_document_types` array records no explicit type restriction; it does not prove that all document types were reviewed. |
| `sources[].covered_sector_tags` | array of strings | Yes | Controlled sector tags. In a legacy entry, an empty `covered_sector_tags` array records no explicit named-sector restriction; it does not prove that all sectors were reviewed. Canonical documents still require sector tags. |
| `sources[].discovery_method` | string | Yes | Reproducible register, site or query method used for discovery. |
| `sources[].scan_status` | string | Yes | One of the five source-review states defined below. |
| `sources[].checked_at` | offset ISO-8601 timestamp | Yes | Actual time at which the entrance was checked; this is distinct from the publication cutoff. |
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

Every candidate has `id`, `source_ids`, `official_reference`, `official_title`, `year`, `issuing_institution`, `commissioning_body`, `record_level`, `version_label`, `candidate_provenance`, `provisional_sector_tags`, `official_source_url`, `decision`, `decision_reason`, `document_id`, `merged_into_document_id`, `discovered_at`, `reviewed_at` and `reviewed_by`, plus the file-level `generated_at` timestamp. A candidate may also have a private `decision_history` array. Candidate IDs are unique, source IDs must exist in the source sweep, and the official candidate URL must use HTTPS. The candidate provenance vocabulary consists of the seven published provenance values plus the two inventory-only values defined above.

| Decision | Required linkage | Meaning |
| --- | --- | --- |
| `included` | `document_id` names a matching canonical document; `merged_into_document_id` is `null`. | The candidate is represented as its own canonical document record. |
| `merged` | `merged_into_document_id` names the canonical record; `document_id` is `null`. | Another manifestation or duplicate candidate is represented by an existing record. |
| `excluded` | Both document links are `null`. | A verified failure of the research boundary keeps the candidate outside the corpus. |
| `pending` | Both document links are `null`. | Official availability, identity or metadata remains unresolved. The candidate remains auditable but cannot enter public output. |

Every candidate needs a non-empty decision reason. An `included` or `merged` decision requires a canonical match, reviewed metadata and non-empty provisional sectors. An `excluded` decision requires completed review but no document link. A `pending` decision has no document link, may use `unknown_pending_review`, and may have an empty provisional sector list. The `reviewed_at` value records the actual time of the candidate review; it is not the source sweep publication cutoff.

When a decision is reopened, each optional `decision_history` item snapshots exactly six prior fields: `decision`, `decision_reason`, `document_id`, `merged_into_document_id`, `reviewed_at` and `reviewed_by`. History is private research metadata, not a canonical entity or public field. Pending candidates contribute to aggregate audit decision counts, but their titles, URLs, reasons and history are excluded from public JSON, SQLite, site routes, published record counts and downloads. All canonical records below `publication_status: published` are likewise excluded from public outputs.

## Generated public distribution

The deterministic build writes `generated/public-data.json` and `generated/eu-ai-policy-observatory.sqlite`. They are derived release artefacts and must never be edited directly; canonical JSON, research audit data and source code remain the editing surfaces. The static atlas consumes the public JSON at build time, and the Pages publication artefact carries the SQLite database as a downloadable research artefact.

Only records with `publication_status: published` and their published dependencies enter these generated public outputs. Canonical repository records may legitimately remain in `draft`, `pending_review` or `verified` editorial states, but they are outside the reviewed public corpus until intentional publication.

Every exported document contains `retained_route_notice`. It is `null` for ordinary documents and contains the complete attributed object plus ordered evidence for the three reviewed retained section routes. SQLite stores the same values in `document_retained_route_notices` and `document_retained_route_evidence`; the evidence order is explicit and both document and source references are foreign-key checked.

The public JSON also contains a generated `coverage` object:

| Field | Derivation |
| --- | --- |
| `from_year` / `to_year` | Earliest and latest year among published documents’ `document_date` values; `null` for an empty corpus. |
| `published_documents` | All published canonical document records. |
| `principal_documents` | Published documents whose `record_level` is `principal`. |
| `supporting_files_and_versions` | Published documents whose `record_level` is `supporting`, `version` or `attachment`. |
| `last_verified_date` | Most recent calendar date among exported evidence sources’ `last_verified_at` values; `null` when no source is exported. |
| `coverage_cutoff` | Exact audit cutoff copied from `research/source-sweep.json`; never computed from the current clock. |
| `coverage_statement` | Human-readable statement of expanding scope and documented verification limits. |
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
