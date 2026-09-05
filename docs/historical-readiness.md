# Historical document readiness contract

This repository contains an **inactive**, read-only preflight contract for historical document metadata. It describes and checks a prospective document shape without changing the active canonical schema, publication pipeline, database, public export, or any of the 117 published document records. A zero-exit result means only that the supplied records are structurally ready for a later reviewed migration. It does not mean that the evidence is academically verified, that a record is included in a PhD sample, or that the site is release-ready.

## Command and API

Run the preflight with an explicit cutoff:

```text
python -m observatory.historical_readiness --project-root . --publication-cutoff 2026-09-04
```

That command assumes the package is installed. From an uninstalled source checkout, expose `src` first—for example, in PowerShell:

```powershell
$env:PYTHONPATH = "src"
.venv/Scripts/python.exe -m observatory.historical_readiness --project-root . --publication-cutoff 2026-09-04
```

The cutoff must be a real calendar date in exact `YYYY-MM-DD` form. The command never substitutes the current date or a maximum record date. It reads `data/` through `observatory.io.load_records`, prints deterministic JSON, and writes no files.

The output contains:

- `contract_version`: always `historical-readiness-1`;
- `publication_contract_active`: always `false`;
- `publication_cutoff`;
- `documents_checked` and `documents_ready`;
- sorted `issues`, each with `code`, `record_path`, `field`, and `message`.

Exit code `0` means all published documents passed this structural preflight, `1` means readiness gaps were found, and `2` means the invocation or canonical input was invalid. Empty document input and malformed JSON fail closed rather than appearing as a successful zero-document run.

The public Python interfaces are:

```python
prospective_document_schema(schema_root: Path) -> dict
validate_historical_readiness(records, schema_root: Path, publication_cutoff: str) -> list[ValidationIssue]
main(argv: list[str] | None = None) -> int
```

`prospective_document_schema` deep-copies the active schema, merges the local extension in memory, retains the base definitions and unknown-property enforcement, and constrains validation to documents. Neither it nor the validator mutates input mappings, schema files, or canonical records.

## Prospective metadata

Every published document is expected to supply:

- `temporal_collection`: `historical_lineage` or `contemporary_eu_ai_policy`;
- `relevance_class`: `direct_ai_substantive`, `ai_related_precursor`, or `indirect_adm_legal_context`;
- `document_date_kind`: `official_act_date`, `institutional_adoption`, `document_issue`, `publication`, or `consolidation`;
- `date_evidence`, with separate citations for `document_date` and `publication_date`;
- nonempty `classification_evidence` covering the exact relevance class and every sector and provenance tag;
- ordered `bibliographic_authors`, which may be explicitly empty after review;
- `additional_dates`, which may be explicitly empty and preserves day, month, or year precision;
- per-role evidence in each `institution_roles` item.

A citation has an official `source_id`, a nonblank `locator`, and a nonblank explanation of `meaning`. Bibliographic authors and classification items use their corresponding evidence locator and rationale fields. Every evidence reference must be declared by the document and resolve uniquely to a published official HTTPS source. The implementation reuses the active validator's official-source predicate; it does not maintain a second trust list.

The prospective copy alone adds document types `directive` and `conclusions`, legal statuses `repealed` and `expired`, and institution roles `commissioner` and `official_host`. Repealed and expired documents require a dedicated `legal_status_evidence` citation. These additions remain invalid under the active schema until a separate reviewed activation.

## What the offline check establishes

The preflight verifies shapes, explicit calendar precision, cutoff boundaries, evidence linkage, reviewed-classification metadata, institution references, attribution requirements, version-aware identities, and relationship evidence. It never infers a missing classification, author, institution, date, source, or relationship.

It does not establish the substantive truth of a quotation or the quality of a research classification. Locators and rationales remain claims requiring human source review. In particular, retrieval timestamps are not document dates, post-cutoff review timestamps do not change historical eligibility, and regulatory application or entry-into-force milestones remain event records rather than additional document dates.

Documents dated before 2018-01-01 are classified by their primary document date as `historical_lineage`; later official publication does not move them into the contemporary collection. Published drafts and proposals remain eligible for checking. External commissioning requires at least one named bibliographic author and an explicit commissioner role; publisher and host roles are not substitutes.

## Preservation baseline and activation boundary

`research/migrations/2026-09-05-public-document-baseline.json` freezes the current 117 published route identities as sorted `id`/`slug` pairs and records full file hashes for audit. Route-preservation checks require that set to remain a subset of later published records, so legitimate additions are allowed and later reviewed metadata revisions are not blocked merely because a hash changes.

This all-route baseline is not an analytical sample. Existing `corpus_tier` values are also not a new PhD sample definition. They remain researcher classifications distinct from official source facts.

Before activation, a separate reviewed migration must supply evidence-backed metadata for the current records, audit every reported gap, review any canonical revisions, and then deliberately update the active schema and pipeline contracts. The old automatic classification migration must not be rerun over reviewed records. The publication cutoff remains 4 September 2026 unless a separate audit authorizes a change.

On the unchanged corpus, a nonzero preflight result is expected because the prospective fields have not been migrated. That result does not indicate a regression in the currently active build.

The current inventory's nine “disconnected” records and the preflight's 15 remaining relationship issues are different measurements. The inventory count describes stored parent context under the active model. This prospective preflight accepts an evidenced incoming or outgoing `version_of`/`revises` edge between a version and a published non-attachment peer; a predecessor may therefore be the target of a later revision. An attachment instead needs outgoing `annex_to`/`part_of`, or an outgoing `version_of`/`revises` edge to another published attachment. Generic incoming child-attachment links do not establish the attachment's own lineage. The CLI must not be read as asserting that the inventory count is 15 or that the two categories are interchangeable.

Every published relationship is checked independently, even when another edge already establishes valid lineage. Both endpoints must use one of the seven canonical entity types, resolve uniquely to a published record in the corresponding canonical directory, and refer to different records; legitimate non-document relationships remain supported. Official evidence is required for every relationship, and an analytical edge also needs a nonblank rationale before it can qualify as lineage. A relationship issue makes both declared document endpoints not ready in CLI counts, including the target of an incoming dependency.
