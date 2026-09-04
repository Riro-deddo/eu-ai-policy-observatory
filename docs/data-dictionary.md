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
| `document_type` | string | Yes | Official | `communication`, `coordinated_plan`, `expert_guidelines`, `white_paper`, `legislative_proposal`, `regulation`. |
| `publication_date` | ISO calendar date | Yes | Official | Valid `YYYY-MM-DD`. |
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
| Relationship `relationship_type` | string | Yes | Analytical | `part_of`, `precedes`, `adopted_as`, `replaces`, `amends`, `implements`, `based_on`, `related_to`, `supersedes`. |
| Relationship `basis` | string | Yes | Analytical | `official`, `analytical`. |
| Relationship `rationale` | string or `null` | Yes | Analytical | Non-empty when `basis` is `analytical`. |
| Relationship `evidence_source_id` | string or `null` | Yes | Official | Existing official source; analytical links require one. |
| Relationship `verification_status` | string | Yes | System | `unverified`, `pending`, `verified`. |
| Source `source_type` | string | Yes | System | `eur_lex`, `eli`, `commission_webpage`, `official_pdf`, `publications_office`. |
| Source `url` | HTTP(S) URI string | Yes | Official | Official HTTP or HTTPS source location. |
| Source `publisher` | string | Yes | Official | Non-empty issuing organisation. |
| Source `retrieved_at` | offset ISO-8601 timestamp | Yes | System | Actual retrieval time. |
| Source `last_verified_at` | offset ISO-8601 timestamp | Yes | System | Last metadata-verification time. |
| Source `verification_note` | string | Yes | System | Human-readable verification record. |

References are validated before SQLite generation. Published records may refer only to published records; published documents, events and relationships require source evidence. SQLite and public JSON are generated outputs, not canonical editing surfaces.

## Generated public distribution

The deterministic build writes `generated/public-data.json` and `generated/eu-ai-policy-observatory.sqlite`. These ignored artefacts are derived from canonical JSON and must not be edited or committed. The static atlas consumes the public JSON at build time; the Pages publication artefact also carries the SQLite database as a downloadable research artefact.

Only records with `publication_status: published` and their published dependencies enter these generated public outputs. Canonical repository records may legitimately remain in `draft`, `pending_review` or `verified` editorial states, but they are outside the reviewed public corpus until intentional publication.
