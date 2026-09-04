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
| `document_type` | string | Yes | Official | `communication`, `coordinated_plan`, `expert_guidelines`, `white_paper`, `legislative_proposal`, `regulation`, `staff_working_document`, `institutional_position`, `opinion`, `resolution`, `decision`, `implementing_regulation`, `guidelines`, `code_of_practice`, `template`, `report`, `standardisation_request`. |
| `record_level` | string | Yes | Analytical | `principal`, `supporting`, `version`, `attachment`. Principal records are the default public Corpus view; every other value contributes to `supporting_files_and_versions`. |
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
| `sources[].id` | string | Yes | Unique lowercase hyphenated entrance ID. |
| `sources[].name` | string | Yes | Human-readable official entrance name. |
| `sources[].institution` | string | Yes | Responsible EU institution or office. |
| `sources[].url` | HTTPS URI string | Yes | Official discovery entrance. |
| `sources[].scope_note` | string | Yes | Bounded search scope used at that entrance. |
| `sources[].scan_status` | string | Yes | `pending`, `in_progress`, `complete`. |
| `sources[].checked_at` | offset ISO-8601 timestamp | Yes | Time at which the entrance was checked. |

### `research/corpus-inventory.json`

Every candidate has `id`, `source_ids`, `official_reference`, `official_title`, `year`, `issuing_institution`, `record_level`, `version_label`, `official_source_url`, `decision`, `decision_reason`, `document_id` and `merged_into_document_id`, plus the file-level `generated_at` timestamp. Candidate IDs are unique, source IDs must exist in the source sweep, and the official candidate URL must use HTTPS.

| Decision | Required linkage | Meaning |
| --- | --- | --- |
| `included` | `document_id` names a matching canonical document; `merged_into_document_id` is `null`. | The candidate is represented as its own canonical document record. |
| `merged` | `merged_into_document_id` names the canonical record; `document_id` is `null`. | Another manifestation or duplicate candidate is represented by an existing record. |
| `excluded` | Both document links are `null`. | A reasoned scope, language, document-status or evidence decision keeps it outside the corpus. |
| `pending` | Both document links are `null`. | Verification is unresolved. The candidate remains auditable but cannot enter public output. |

No source-sweep entrance may remain incomplete when the audit is closed. Every candidate needs a non-empty decision reason. Pending inventory candidates and all canonical records below `publication_status: published` are excluded from public JSON, SQLite, site routes and coverage totals.

## Generated public distribution

The deterministic build writes `generated/public-data.json` and `generated/eu-ai-policy-observatory.sqlite`. These ignored artefacts are derived from canonical JSON and must not be edited or committed. The static atlas consumes the public JSON at build time; the Pages publication artefact also carries the SQLite database as a downloadable research artefact.

Only records with `publication_status: published` and their published dependencies enter these generated public outputs. Canonical repository records may legitimately remain in `draft`, `pending_review` or `verified` editorial states, but they are outside the reviewed public corpus until intentional publication.

The public JSON also contains a generated `coverage` object:

| Field | Derivation |
| --- | --- |
| `from_year` / `to_year` | Earliest and latest year among published documents’ `document_date` values; `null` for an empty corpus. |
| `published_documents` | All published canonical document records. |
| `principal_documents` | Published documents whose `record_level` is `principal`. |
| `supporting_files_and_versions` | Published documents whose `record_level` is `supporting`, `version` or `attachment`. |
| `last_verified_date` | Most recent calendar date among exported official sources’ `last_verified_at` values; `null` when no source is exported. |

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
```

The Python suite checks schema, controlled vocabulary, composite identity, references, provenance, source-sweep and inventory contracts. `observatory-build` validates before atomically replacing generated outputs. Web tests and the public scanner check public-only rendering, routes, downloadable SQLite integrity, common credential markers and local-path leakage.
