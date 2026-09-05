# Historical Contract Preflight Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the first independently testable Phase B unit: a strict, read-only historical-document readiness contract and a preservation baseline, without activating partially migrated data.

**Architecture:** Keep the active canonical schema, database builder/exporter and public atlas unchanged. Compose a prospective document schema in memory from the existing schema and a local extension, then check evidence, dates and attribution through a separate read-only preflight API/CLI. A later reviewed migration and atomic schema/SQLite/export/UI activation are required before this contract controls publication or new candidates are imported.

**Tech Stack:** Existing Python 3.12 environment, jsonschema 4.x, pytest 8.x, JSON; no new dependency.

**Spec:** `docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md`, particularly sections 3-6, 9-11.

## Global Constraints

- Keep the seven canonical entities: `policy`, `document`, `event`, `concept`, `institution`, `relationship` and `source`.
- Preserve existing document IDs, slugs and URLs. Correct a record through a documented revision, not deletion and recreation under a new identity.
- Keep one canonical dataset, one generated SQLite database and one public JSON export. Collection labels are fields, not separate databases or an eighth entity.
- Keep the six English pages: Home, Policy Map, Timeline, Corpus, Methodology and About. No unrelated visual redesign is included.
- Keep official facts distinct from researcher classifications, including temporal/relevance groupings, sector tags, corpus tiers and policy membership.
- Do not add LLM experiments, interpretation coding, a backend, accounts, a second-language public site or a new hosting service.
- The current dataset's cutoff remains 4 September 2026 until a separate audit supports a change.
- Do not rerun the old automatic classification migration over reviewed records.
- All new code, docs, report keys and labels are English. Preserve original credited Latin-script names.
- This preparatory contract is NOT an activated publication gate. Do not weaken or modify the current validator, pipeline, schema, SQL, export, web code, canonical data, inventory, source sweep or generated files.
- All Git commands use `git --git-dir=work/sdd-gitmeta --work-tree=.`. Plain `.git` is stale. No reset, cleanup, push, merge or deployment.
- Existing Phase A full-browser release verification is open. This delivery cannot close it or claim whole-Phase-B completion.

## Delivery boundary and later work

This unit intentionally does not backfill the 117 published records, invent citations, reopen the browser troubleshooting loop, register wider source coverage or import the 25 admission-ready candidates. It gives the subsequent reviewed migration a concrete target and reports every missing field without changing a live URL. No optional fields are added to the active schema: that would permit a generator to silently discard newly accepted metadata.

Later Phase B units must:
1. Review all 117 records in explicit batches and freeze a reproducible RP selection without equating every existing core label with the PhD sample.
2. Reconcile the nine disconnected versions/attachments and evidence for all published relationships.
3. Activate required fields atomically in canonical validation, SQL, builder, exporter, TypeScript runtime checks and English atlas display/filtering.
4. Replace inventory year bounds using a separately validated publication cutoff.
5. Verify preservation of all baseline routes, deterministic generation and release/browser checks before any backfill/publication.

## Task 1: Strict read-only contract, preservation baseline and readiness CLI

**Files:**
- Create: `schema/historical-document-extension.schema.json`
- Create: `src/observatory/historical_readiness.py`
- Optional cohesive helper: `src/observatory/historical_relationships.py`, only if the relationship boundary benefits from separate testing/readability. Do not compress code to meet a line-count target.
- Create: `tests/test_historical_readiness.py`
- Create: `research/migrations/2026-09-05-public-document-baseline.json`
- Create: `docs/historical-readiness.md`
- No edits to active production contracts or canonical records.

**Interfaces:**
- Consumes: existing `schema/record.schema.json`; `load_records(Path)` and `LoadedRecord` in `observatory.io`; `ValidationIssue` in `observatory.types`.
- Reuses: the existing official-source predicate `observatory.validate._is_official_source` rather than copying domain trust logic.
- Produces:
```python
def prospective_document_schema(schema_root: Path) -> dict:
    """Return a deep-copied document schema; never mutate or write the base."""

def validate_historical_readiness(
    records: Mapping[str, Sequence[LoadedRecord]],
    schema_root: Path,
    publication_cutoff: str,
) -> list[ValidationIssue]:
    """Assess published documents and their evidence; never infer or modify fields."""

def main(argv: list[str] | None = None) -> int:
    """Print deterministic JSON; 0 means structurally ready, 1 means gaps, 2 means invalid invocation/input."""
```
- CLI: `python -m observatory.historical_readiness --project-root . --publication-cutoff 2026-09-04`.
- CLI JSON keys: `contract_version` = `historical-readiness-1`, `publication_contract_active` = false, `publication_cutoff`, `documents_checked`, `documents_ready`, `issues`. Every issue has the existing four `ValidationIssue` fields. Sort issues by path, field, code, message. No file writes, promotion, network calls, datetime-derived classifications or timestamps pretending to be source verification.
- Invalid exact cutoff syntax/calendar date yields exit 2, an English error and no traceback. Missing/malformed canonical input must fail closed, not become a zero-document success.

### Contract shape

The extension is a valid local JSON Schema with `properties`, `required` and `$defs`. Merge these into a deepcopy of the base document definition and definitions; use the base root's oneOf/unevaluatedProperties enforcement to reject unrelated extra properties. Append only `directive` and `conclusions` to document types, `repealed` and `expired` to legal status, and `commissioner`/`official_host` to roles in this prospective copy. No schema file may mutate the active contract.

New required document fields:

| Field | Exact shape |
| --- | --- |
| `temporal_collection` | `historical_lineage` or `contemporary_eu_ai_policy` |
| `relevance_class` | `direct_ai_substantive`, `ai_related_precursor`, `indirect_adm_legal_context` |
| `document_date_kind` | `official_act_date`, `institutional_adoption`, `document_issue`, `publication`, `consolidation` |
| `date_evidence` | Object with exactly `document_date` and `publication_date`, each a citation |
| `classification_evidence` | Nonempty array of objects: `field` (relevance_class/sector_tags/provenance_tags), `value` (nonblank string), `source_id`, `locator`, `rationale` |
| `bibliographic_authors` | Ordered array, possibly explicitly empty after review; each author has `name`, `affiliation` (nonblank string or null), `evidence_source_id`, `evidence_locator` |
| `additional_dates` | Array, possibly empty; each has `kind`, `value`, `precision` (day/month/year), `source_id`, `locator` |

Citation: exactly `source_id` (existing ID format), `locator` (nonblank string), `meaning` (nonblank explanation). Nonblank means at least one non-whitespace character, not merely minLength.

Additional-date kinds: `document_issue`, `institutional_adoption`, `first_official_publication`, `oj_publication`, `manuscript_completion`, `cover_issue`, `consolidation`. Validate real calendar dates at day precision, real year/month at month precision and years 0001-9999. Do not coerce month/year values to exact days. Regulatory application/entry-into-force milestones are not allowed here; they remain events.

Every prospective institution-role object retains `institution_id` and `role` and additionally requires `evidence_source_id` and `evidence_locator`. Reject unknown keys. Named individuals are bibliographic authors, not new institution records. Preserve author order. Do not derive an authored-origin tag from adopter/publisher/host roles.

Optional `legal_status_evidence` is a citation, required for `repealed` or `expired`.

### Semantic rules

1. Assess only published documents, but load source/institution/relationship context. Reject empty or missing published input and malformed JSON with an actionable issue; do not report success on zero records. Preserve source path diagnostics without echoing private field values.
2. Cutoff must be an explicit exact valid date, never current time or maximum record date. Both primary document and publication dates must be on/before it. A review timestamp after the cutoff is valid and retained.
3. Before 2018-01-01 requires historical_lineage; on/after requires contemporary_eu_ai_policy. Check the supplied class; never write/guess it. A 1975 record is eligible. A 2017 adoption plus 2018 OJ publication remains historical.
4. `official_act_date` is valid for regulation/directive/decision/implementing_regulation; `institutional_adoption` for resolution/opinion/conclusions; `consolidation` requires version_status consolidated; a consolidated version requires that date kind. Reports/studies/communications cannot use act/adoption kinds. A publication fallback requires document_date = publication_date. Published official drafts/proposals are not rejected just because version_status is draft or legal_status proposed.
5. Every citation/role/author/classification/additional-date/status evidence source must be declared in the document's source_ids and resolve uniquely to a published official HTTPS source. Reuse the existing source predicate, with separate publication status and unique-ID checks. Blank citations, forged domain suffixes, unpublished/missing references and undeclared evidence fail.
6. Classification evidence must cover the exact relevance value, every sector tag and every provenance tag, with no value absent from the document. Require verified corpus_assessment, nonblank reviewer/inclusion rationale and timezone-aware review timestamp. A title match, old tag or blank evidence is not enough. Offline checks establish evidence shape and linkage, not substantive truth of quotations.
7. Institution roles resolve to actual institution IDs. Each role needs its own source/locator; duplicate institution+role pairs fail even if their evidence differs. External commissioning requires at least one named bibliographic author and a commissioner role. A publisher or host does not satisfy that commissioner requirement. Do not auto-create bodies or bibliographic credits.
8. Repealed/expired require their own official status evidence; programme end dates cannot substitute. Allow a consolidated repealed/expired act when its new status evidence and consolidation date are valid.
9. Every published version needs an evidenced version relationship with another published non-attachment document: outgoing version_of/revises or incoming version_of/revises are accepted because a predecessor may only be the target of a later revision. Every attachment needs outgoing annex_to/part_of to another published document, or outgoing version_of/revises to another published attachment (a separately citable attachment version). Generic incoming attachment links do not establish a version's own lineage. Self-parent, missing/unpublished endpoint and missing official evidence fail. All published relationships, whether official or analytical, require an existing published official evidence source; analytical relations also retain a nonblank rationale. Do not rewrite existing edge types automatically to satisfy this check.
10. Duplicate published IDs/slugs/CELEX/ELI and version-aware identities must fail. Identity uses official_reference, language, normalized version_label and author/proposer/adopter IDs, not publisher/host/commissioner roles; a later OJ manifestation of the same identity is not a second record.
11. Functions do not mutate records, schema inputs or files. They do not fill missing fields, treat a pending record as ready, or turn a structurally ready record into included.

### Step 1: Write behavior tests and obtain RED

- [ ] Create a test fixture helper using a deep copy of `tests/fixtures/valid/data/documents/example-document.json`, with explicitly constructed complete new fields. Use real source/institution fixtures and `LoadedRecord`, not mock validator results.
- [ ] Start the prospective validator API with an empty-result stub only after tests exist; this allows the real negative-contract assertions below to fail for missing behavior rather than an import error. Then replace the stub during GREEN.
- [ ] Run the test file before implementing any rule and preserve the expected assertion failures.

The central fixture uses document_date 2017-02-16, publication_date 2018-07-18, resolution/institutional_adoption, historical_lineage, direct_ai_substantive, an official example-source, verified review dated 2026-09-05T06:00:00Z, and cited evidence for its existing tags/roles. This is a synthetic fixture, not a claim of new retrieval.

Actual test patterns:
```python
def test_2017_adoption_with_2018_oj_stays_historical(complete_records):
    assert validate_historical_readiness(complete_records, SCHEMA_ROOT, "2026-09-04") == []

def test_publication_cannot_be_inferred_from_issue_date(complete_records):
    document = complete_records["documents"][0].data
    del document["date_evidence"]["publication_date"]
    issues = validate_historical_readiness(complete_records, SCHEMA_ROOT, "2026-09-04")
    assert any("date_evidence" in issue.field for issue in issues)

def test_retrieval_cannot_be_used_as_document_date_kind(complete_records):
    complete_records["documents"][0].data["document_date_kind"] = "retrieval"
    issues = validate_historical_readiness(complete_records, SCHEMA_ROOT, "2026-09-04")
    assert any(issue.field == "document_date_kind" for issue in issues)

def test_preflight_never_fills_missing_classification(complete_records):
    del complete_records["documents"][0].data["relevance_class"]
    before = deepcopy(complete_records)
    issues = validate_historical_readiness(complete_records, SCHEMA_ROOT, "2026-09-04")
    assert any(issue.field == "relevance_class" for issue in issues)
    assert complete_records == before

def test_undeclared_evidence_is_not_accepted(complete_records):
    document = complete_records["documents"][0].data
    document["date_evidence"]["document_date"]["source_id"] = "unlisted-source"
    issues = validate_historical_readiness(complete_records, SCHEMA_ROOT, "2026-09-04")
    assert any(issue.code == "historical_evidence" for issue in issues)
```

Also cover these exact independent behaviors with literal expected errors or zero issues: 1975 eligible; invalid/leap dates; missing required metadata; wrong temporal label; future publication; published draft eligible; blank/unknown/uncited classification; source http/deceptive host/missing/unpublished/duplicate; unknown institution; externally authored study with commissioner and ordered people; missing commissioner; duplicate role; month-level additional date retained; wrong precision; expiry with/without evidence; 2017/2018 duplicate manifestation rejected; missing version/attachment link; analytical relationship with unofficial evidence; no input mutation; schema file bytes unchanged.

CLI behavior tests must invoke the real module in a subprocess with a temporary fixture tree. Assert JSON/counts/exit code for ready and incomplete records; malformed/empty project and malformed cutoff fail. Snapshot fixture-tree file bytes before/after to prove read-only behavior. Do not test CLI by grepping source.

### Step 2: Implement the local extension and in-memory prospective schema

- [ ] Create the extension and compose it with a deepcopy of the existing schema. In `prospective_document_schema`, retain all seven base branches/definitions and base format/unknown-property validation, then constrain entity_type to document.
- [ ] Reuse `Draft202012Validator(..., format_checker=FormatChecker())`; do not write custom regex-only calendar validation.
- [ ] Keep all new roles/types/statuses confined to the prospective schema. Assert the active schema still rejects a record containing these new fields until later activation.

Core date helper implementation:
```python
def _exact_date(value: object) -> date | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None
```

### Step 3: Implement semantics and the read-only CLI

- [ ] Implement the eleven semantic rules with stable codes: `historical_schema`, `historical_date`, `historical_collection`, `historical_evidence`, `historical_classification`, `historical_attribution`, `historical_identity`, `historical_relationship`, `historical_input`.
- [ ] Avoid cascading crashes on malformed inputs: add shape issues and guard accesses, rather than calling string/date methods on unknown values.
- [ ] Reuse official-source trust logic without weakening it. Do not duplicate the entire existing validator; only this prospective readiness boundary is new.
- [ ] CLI reads `load_records(root / "data")`, calls the API and serializes `dataclasses.asdict(issue)`. A record is counted ready only when no issue applies to it or its required relationship/source context.
- [ ] CLI exit 0 means structurally ready under this preflight only, not academically verified, canonically included or release-ready. State that in docs/output.

### Step 4: Freeze the current route preservation baseline

- [ ] Create the baseline JSON from the actual 117 published document files with `baseline_date`, `publication_cutoff`, `baseline_head`, `documents` containing sorted `id`, `slug`, `record_sha256`. Store exactly this existing set, not an invented RP analytical sample.
- [ ] Add a test comparing baseline id/slug pairs as a subset of current published records. Add/remove a temporary fixture record to show legitimate additions are allowed and baseline loss/slug changes rejected by a small pure comparison helper in test utilities (not production).
- [ ] Preserve full hashes for audit, but do not lock legitimate future metadata revisions to those hashes in the route-preservation test.
- [ ] Document that current corpus_tier labels and this all-route baseline are not a new PhD sample definition.

### Step 5: GREEN, documentation and scoped commit

- [ ] Run focused tests through `.venv/Scripts/python.exe -m pytest tests/test_historical_readiness.py -q -p no:cacheprovider --basetemp C:/Users/ROG/AppData/Local/Temp/eu-ai-b1-green-20260905-01`.
- [ ] Run the existing contract/validator/inventory tests together with the new file using a fresh Temp path; baseline was 101 passed before changes.
- [ ] Run the read-only CLI on the real repository. A nonzero result for the unchanged 117 records is the expected migration-readiness result, not a failed existing build.
- [ ] Document the concrete fields/API, distinction between structural and substantive evidence, no-mutation behavior, legacy gaps and subsequent activation work in `docs/historical-readiness.md`.
- [ ] Verify `generated/public-data.json` SHA-256 remains `067B839BA54DA091D8B6BA7F743D660826865221F4587C647379D7C8F71FC4EB`; protected active/data/generated paths have no diff.
- [ ] Commit only the Task 1 deliverable paths listed above and this plan using the alternate metadata command. If staging is denied, stop retrying and report the completed tests/diff; the controller handles the exact permission issue.
- [ ] Write RED/GREEN commands and output, file list and limitations to the task report; return the short completion contract.

## Self-review coverage

| Requirement | This unit | Later activation/migration |
| --- | --- | --- |
| Sections 3-5 temporal/relevance/date evidence | Strict prospective checks and adversarial fixtures | Reviewed values on all public records |
| Section 6 authors/commissioner/historical types/status | Prospective model, official reference checks, ordered author fixture | SQL/export/UI and real credit review |
| Section 5.2 identity and version integrity | Readiness diagnostics and synthetic regressions | Nine real link reconciliations |
| Section 9 stable routes/RP separation | All-117 id/slug baseline; do not redefine RP subset | Full route generation and explicit RP selection |
| Section 9 atlas filters and display | Deliberately inactive; no misleading new controls | Atomic runtime types/filter/display activation |
| Section 10 reviewed migration | Missing fields are reported, never guessed | Explicit evidence batches and activation |
| Release gate | No release claims or external writes | Existing Phase A/E2E and full B checks remain required |
