# Historical document readiness contract

This repository now applies a compatibility-gated historical metadata contract in the production pipeline. New published documents must carry a complete, evidence-backed extension and pass the readiness checks. The 117 routes frozen before activation remain publishable as `legacy_review_pending` until individually reviewed; they do not receive inferred classifications. The initial migration adds 14 reviewed historical documents and upgrades three existing documents, producing 17 `verified` and 114 `legacy_review_pending` documents in a 131-document corpus. A verified status records passage through this evidence gate; it is not a researcher-approved PhD sample or a claim that historical source discovery is complete.

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
- `publication_contract_active`: the standalone diagnostic remains `false`; production activation is enforced separately by `observatory.historical_publication`;
- `publication_cutoff`;
- `documents_checked` and `documents_ready`;
- sorted `issues`, each with `code`, `record_path`, `field`, and `message`.

Exit code `0` means all published documents passed this structural preflight, `1` means readiness gaps were found, and `2` means the invocation or canonical input was invalid. Empty document input and malformed JSON fail closed rather than appearing as a successful zero-document run. Malformed JSON and non-object JSON errors list the affected project-relative source paths in deterministic order without echoing record contents. Wrong-typed fields inside an otherwise valid object remain structured readiness issues in the JSON result; values are never coerced.

The public Python interfaces are:

```python
prospective_document_schema(schema_root: Path) -> dict
validate_historical_readiness(records, schema_root: Path, publication_cutoff: str) -> list[ValidationIssue]
main(argv: list[str] | None = None) -> int
```

`prospective_document_schema` deep-copies the active schema, merges the local extension in memory, retains the base definitions and unknown-property enforcement, and constrains validation to documents. Neither it nor the validator mutates input mappings, schema files, or canonical records.

## Prospective metadata

Every newly admitted or reviewed published document supplies:

- `temporal_collection`: `historical_lineage` or `contemporary_eu_ai_policy`;
- `relevance_class`: `direct_ai_substantive`, `ai_related_precursor`, or `indirect_adm_legal_context`;
- `document_date_kind`: `official_act_date`, `institutional_adoption`, `document_issue`, `publication`, or `consolidation`;
- `date_evidence`, with separate citations for `document_date` and `publication_date`;
- nonempty `classification_evidence` covering the exact relevance class and every sector and provenance tag;
- ordered `bibliographic_authors`, which may be explicitly empty after review;
- `additional_dates`, which may be explicitly empty and preserves day, month, or year precision;
- per-role evidence in each `institution_roles` item.

A citation has an official `source_id`, a nonblank `locator`, and a nonblank explanation of `meaning`. Bibliographic authors and classification items use their corresponding evidence locator and rationale fields. Every evidence reference must be declared by the document and resolve uniquely to a published official HTTPS source. The implementation reuses the active validator's official-source predicate; it does not maintain a second trust list.

The active schema includes the bounded historical document types, legal statuses and attribution roles. `no_longer_in_force`, `repealed`, and `expired` require dedicated official status evidence. Roles such as commissioner, responsible body, requester, supervisor and cover-note sender remain distinct from authorship.
Additional-date kinds include official end-of-validity, official dispatch and Parliament adopted-text manifestation where the cited source supports them.

## What the offline check establishes

The preflight verifies shapes, explicit calendar precision, cutoff boundaries, evidence linkage, reviewed-classification metadata, institution references, attribution requirements, version-aware identities, and relationship evidence. It never infers a missing classification, author, institution, date, source, or relationship.

It does not establish the substantive truth of a quotation or the quality of a research classification. Locators and rationales remain claims requiring human source review. In particular, retrieval timestamps are not document dates, post-cutoff review timestamps do not change historical eligibility, and regulatory application or entry-into-force milestones remain event records rather than additional document dates.

Documents dated before 2018-01-01 are classified by their primary document date as `historical_lineage`; later official publication does not move them into the contemporary collection. Published drafts and proposals remain eligible for checking. External commissioning requires at least one named bibliographic author and an explicit commissioner role; publisher and host roles are not substitutes.

## Preservation baseline and compatibility boundary

`research/migrations/2026-09-05-public-document-baseline.json` freezes the current 117 published route identities as sorted `id`/`slug` pairs and records full file hashes for audit. Route-preservation checks require that set to remain a subset of later published records, so legitimate additions are allowed and later reviewed metadata revisions are not blocked merely because a hash changes.

This all-route baseline is not an analytical sample. Existing `corpus_tier` values are also not a new PhD sample definition. The database's versioned seed subset is limited to the seven original seed IDs and is likewise operational metadata, not a PhD sample.

The compatibility gate never treats field presence as verification: `historical_review_status: verified` is accepted only when the complete date, classification, attribution, source and relationship checks pass. Partial extension blocks fail. Evidence source IDs must resolve to declared, published, verified official sources. The old automatic classification migration must not be rerun over reviewed records. The publication cutoff remains 4 September 2026 unless a separate audit authorizes a change.

The initial admission is deliberately bounded to the 14 `evidence_ready` rows in the private admission review. Three held candidates remain private and were not imported. Four historical source-family scopes are registered as `in_progress`; empty type or sector scopes mean unspecified, not comprehensive coverage. The remaining 114 legacy documents are separately measurable evidence-review work.

On the current corpus, the standalone all-document preflight remains nonzero because 114 retained legacy routes have not been migrated. That does not indicate a production-build regression: the compatibility gate validates the complete extension on reviewed records while preserving only exact ID/slug pairs from the frozen baseline for pending legacy records. Three published draft-guideline section records carry retained-route notices; these explain why their stable routes remain available but do not suppress historical relationship issues or claim a parent relationship.

The inventory's nine “disconnected” records and the preflight's 15 relationship issues were measurements from an earlier 5 September readiness review, not current counts. After the subsequent reviewed identity corrections, the current historical relationship check retains exactly three missing-parent holds, one for each noticed draft-guideline section. The inventory count describes stored parent context under the active model. This prospective preflight accepts an evidenced incoming or outgoing `version_of`/`revises` edge between a version and a published non-attachment peer; a predecessor may therefore be the target of a later revision. An attachment instead needs outgoing `annex_to`/`part_of`, or an outgoing `version_of`/`revises` edge to another published attachment. Generic incoming child-attachment links do not establish the attachment's own lineage. The CLI must not be read as asserting that either earlier number is current or that the two categories are interchangeable.

Every published relationship is checked independently, even when another edge already establishes valid lineage. Both endpoints must use one of the seven canonical entity types, resolve uniquely to a published record in the corresponding canonical directory, and refer to different records; legitimate non-document relationships remain supported. Official evidence is required for every relationship, and an analytical edge also needs a nonblank rationale before it can qualify as lineage. A relationship issue makes both declared document endpoints not ready in CLI counts, including the target of an incoming dependency.
