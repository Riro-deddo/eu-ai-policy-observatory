# Comprehensive Corpus Schema and Interface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement Stage 1 of the approved comprehensive EU AI document corpus: controlled sector and provenance classifications, an auditable coverage contract, deterministic database/public exports, and English browsing interfaces for the existing 117-record corpus.

**Architecture:** Canonical JSON under `data/` remains the research source of truth. Validation enforces controlled multi-value classifications before published records are normalised into SQLite and exported as deterministic public JSON; the research source sweep and candidate inventory are separately validated and reduced to a privacy-safe public coverage summary. Astro consumes only the generated public payload, preserving every existing route while adding classification filters and cutoff-based methodology reporting.

**Tech Stack:** Python 3.11+, JSON Schema 2020-12, SQLite, pytest 8, Astro 5.17.1, TypeScript 5.9.3, Node test runner, Vitest 3.2.4, Playwright 1.55.0, GitHub Actions and GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-09-04-comprehensive-eu-ai-document-corpus-design.md`

## Global Constraints

- Keep repository fields, canonical records, public copy and UI labels in English.
- Preserve all existing canonical IDs, document slugs and public routes.
- Keep the seven top-level entity types unchanged: `policy`, `document`, `event`, `concept`, `institution`, `relationship` and `source`.
- Require non-empty, unique `sector_tags` and `provenance_tags` arrays on every canonical document, including drafts that are not yet public.
- Treat sector tags as researcher classifications; never present them as official EU metadata.
- Keep production provenance, official publisher roles and official hosting sources as separate facts.
- Allow inventory-only provenance values only in `research/corpus-inventory.json`; never allow them on canonical published documents.
- Treat formal official publication as the eligibility threshold; do not reduce the corpus to adopted or in-force law.
- Keep pending or unverified candidates out of SQLite, public JSON and the generated site.
- Publish the exact `coverage_cutoff`; never calculate it from the current clock or infer a future date.
- Use `2026-09-04T00:00:00Z` as the deterministic Stage 1 migration timestamp. Preserve earlier timestamps when a record's substantive data does not change.
- Use only official EU URLs as evidence for published records.
- Add no runtime network dependency to validation, export, tests or the GitHub Pages build.
- Follow test-driven development: run each focused test red, add the minimum implementation, run it green, then commit.

## File and Responsibility Map

- `schema/controlled-vocabularies.json`: canonical sector, provenance, document-type and status values.
- `schema/record.schema.json`: required document arrays and structural constraints.
- `src/observatory/validate.py`: cross-file vocabularies, status combinations and audit integrity.
- `scripts/migrate_document_classifications.py`: one-shot deterministic migration of existing documents.
- `schema/database.sql`: normalised document classification tables.
- `src/observatory/build_db.py`: inserts canonical tags into SQLite.
- `src/observatory/export_public.py`: exports deterministic document arrays and combines document metrics with audit coverage.
- `schema/source-sweep.schema.json`: source-family coverage contract.
- `schema/corpus-inventory.schema.json`: candidate provenance, sector and decision contract.
- `research/source-sweep.json`: exact official entrances and review coverage.
- `research/corpus-inventory.json`: one auditable decision per discovered candidate.
- `src/observatory/coverage.py`: creates a public aggregate from the two research files without exposing candidate details.
- `src/observatory/pipeline.py`: validates, builds and atomically publishes the expanded payload.
- `web/src/lib/types.ts`: public payload types.
- `web/src/lib/filter.ts`: corpus and timeline classification/view filtering.
- `web/src/components/CorpusExplorer.astro`: sector and provenance controls and card labels.
- `web/src/components/Timeline.astro`: principal/all-record view control.
- `web/src/pages/corpus/[slug].astro`: official, analytical and provenance sections.
- `web/src/pages/methodology.astro`: inclusion boundary and auditable coverage reporting.
- `docs/data-dictionary.md` and `README.md`: contributor and public documentation.

---

### Task 1: Add canonical classification and document-type contracts

**Files:**

- Modify: `schema/controlled-vocabularies.json`
- Modify: `schema/record.schema.json`
- Modify: `tests/fixtures/valid/data/documents/example-document.json`
- Modify: `tests/fixtures/invalid/data/documents/broken-document.json`
- Modify: `tests/fixtures/invalid/data/documents/second-document.json`
- Modify: `tests/test_schema_contract.py`

**Interfaces:**

- Consumes: the existing document `$defs` in `schema/record.schema.json`.
- Produces: required `sector_tags: list[str]` and `provenance_tags: list[str]` fields plus the expanded `document_type` vocabulary used by every later task.

- [ ] **Step 1: Write failing schema tests for required, unique, controlled arrays.**

Add this parametrised test to `tests/test_schema_contract.py`, using its existing fixture loader and `_validation_errors` helper:

```python
@pytest.mark.parametrize("field", ["sector_tags", "provenance_tags"])
def test_document_schema_requires_non_empty_unique_classification_arrays(field):
    schema = json.loads(Path("schema/record.schema.json").read_text(encoding="utf-8"))
    document = json.loads(
        Path("tests/fixtures/valid/data/documents/example-document.json")
        .read_text(encoding="utf-8")
    )

    missing = dict(document)
    del missing[field]
    empty = {**document, field: []}
    duplicate = {**document, field: [document[field][0], document[field][0]]}

    validator = Draft202012Validator(schema)
    assert list(validator.iter_errors(missing))
    assert list(validator.iter_errors(empty))
    assert list(validator.iter_errors(duplicate))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("sector_tags", ["not_a_sector"]),
        ("provenance_tags", ["third_party_submission"]),
    ],
)
def test_document_schema_rejects_unknown_or_inventory_only_classifications(field, value):
    schema = json.loads(Path("schema/record.schema.json").read_text(encoding="utf-8"))
    document = json.loads(
        Path("tests/fixtures/valid/data/documents/example-document.json")
        .read_text(encoding="utf-8")
    )
    document[field] = value

    assert list(Draft202012Validator(schema).iter_errors(document))
```

Also assert that all eight new document types are accepted by replacing the fixture's `document_type` once per value.

- [ ] **Step 2: Run the schema tests and verify the new tests fail.**

Run: `python -m pytest tests/test_schema_contract.py -q`

Expected: failures because the fixture and document schema do not yet contain the two classification arrays or the eight new document types.

- [ ] **Step 3: Add the exact controlled vocabularies.**

Add these keys to `schema/controlled-vocabularies.json`:

```json
"sector_tag": [
  "general_cross_sector",
  "health",
  "employment_and_labour",
  "migration_asylum_and_border_management",
  "financial_services",
  "transport_and_mobility",
  "defence_and_security",
  "law_enforcement",
  "justice",
  "education",
  "public_administration",
  "consumer_protection",
  "media_and_culture",
  "intellectual_property",
  "research_and_innovation",
  "industry_and_manufacturing",
  "agriculture_and_environment",
  "critical_infrastructure",
  "cybersecurity",
  "competition_and_markets"
],
"provenance_tag": [
  "eu_institution_authored",
  "eu_agency_or_body_authored",
  "eu_expert_group_authored",
  "eu_commissioned_external",
  "joint_institutional",
  "official_consultation_material",
  "officially_published"
]
```

Append `study`, `consultation_document`, `declaration`, `recommendation`, `judgment`, `briefing`, `technical_specification` and `work_programme` to `document_type` without deleting existing values.

- [ ] **Step 4: Require the arrays in the canonical document schema.**

Add these properties to the document definition and include both names in its `required` array:

```json
"sector_tags": {
  "type": "array",
  "minItems": 1,
  "uniqueItems": true,
  "items": {
    "enum": [
      "general_cross_sector", "health", "employment_and_labour",
      "migration_asylum_and_border_management", "financial_services",
      "transport_and_mobility", "defence_and_security", "law_enforcement",
      "justice", "education", "public_administration", "consumer_protection",
      "media_and_culture", "intellectual_property", "research_and_innovation",
      "industry_and_manufacturing", "agriculture_and_environment",
      "critical_infrastructure", "cybersecurity", "competition_and_markets"
    ]
  }
},
"provenance_tags": {
  "type": "array",
  "minItems": 1,
  "uniqueItems": true,
  "items": {
    "enum": [
      "eu_institution_authored", "eu_agency_or_body_authored",
      "eu_expert_group_authored", "eu_commissioned_external",
      "joint_institutional", "official_consultation_material",
      "officially_published"
    ]
  }
}
```

Extend the document-type enum in the schema with the same eight values as the vocabulary file.

- [ ] **Step 5: Migrate the contract fixtures.**

Add this exact pair to the valid example and to invalid documents whose intended failure is unrelated to classification:

```json
"sector_tags": ["general_cross_sector"],
"provenance_tags": ["eu_institution_authored", "officially_published"]
```

- [ ] **Step 6: Run the focused tests.**

Run: `python -m pytest tests/test_schema_contract.py -q`

Expected: all schema-contract tests pass.

- [ ] **Step 7: Commit the canonical contract.**

```powershell
git add schema/controlled-vocabularies.json schema/record.schema.json tests/fixtures tests/test_schema_contract.py
git commit -m "feat: add document sector and provenance contracts"
```

---

### Task 2: Validate classification vocabularies and status combinations

**Files:**

- Modify: `src/observatory/validate.py`
- Modify: `tests/test_validate.py`

**Interfaces:**

- Consumes: `sector_tag` and `provenance_tag` arrays from `schema/controlled-vocabularies.json`.
- Produces: `_validate_vocabulary_list(record, field, vocabulary_key, vocabularies, record_path) -> list[ValidationIssue]` and `_validate_document_status_combination(record, record_path) -> list[ValidationIssue]`.

- [ ] **Step 1: Write failing tests for list vocabularies.**

```python
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("sector_tags", ["general_cross_sector", "invented_sector"]),
        ("provenance_tags", ["officially_published", "third_party_submission"]),
    ],
)
def test_document_classification_arrays_use_controlled_vocabularies(tmp_path, field, value):
    data_root = _copy_valid_data(tmp_path)
    path = data_root / "documents" / "example-document.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document[field] = value
    path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(issue.code == "vocabulary" and issue.field == f"{field}.1" for issue in issues)
```

- [ ] **Step 2: Write failing tests for the minimal cross-status rules.**

Test these exact invalid combinations and one explicitly valid published draft:

```python
@pytest.mark.parametrize(
    ("publication_status", "version_status", "legal_status"),
    [
        ("verified", "final", "in_force"),
        ("published", "draft", "in_force"),
        ("published", "consolidated", "proposed"),
        ("published", "consolidated", "withdrawn"),
    ],
)
def test_invalid_document_status_combinations_are_rejected(
    tmp_path, publication_status, version_status, legal_status
):
    data_root = _copy_valid_data(tmp_path)
    path = data_root / "documents" / "example-document.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document.update(
        publication_status=publication_status,
        version_status=version_status,
        legal_status=legal_status,
    )
    path.write_text(json.dumps(document), encoding="utf-8")

    assert any(
        issue.code == "status_combination"
        for issue in validate_records(data_root, SCHEMA, VOCAB)
    )
```

Add a separate test that `published + draft + non_binding` produces no `status_combination` issue.

- [ ] **Step 3: Run the focused validation tests and verify failure.**

Run: `python -m pytest tests/test_validate.py -q`

Expected: the new tests fail because list entries and cross-status combinations are not checked by the Python validator.

- [ ] **Step 4: Implement list vocabulary validation.**

Add a list-field map next to `_VOCABULARY_FIELDS`:

```python
_VOCABULARY_LIST_FIELDS = {
    "sector_tags": "sector_tag",
    "provenance_tags": "provenance_tag",
}
```

For each string item, emit a `ValidationIssue` with code `vocabulary`, field `<field>.<zero-based-index>`, and a message that names the unknown vocabulary value but does not echo unrelated record content.

- [ ] **Step 5: Implement the exact status-combination rules.**

Apply these predicates only to document records:

```python
if legal_status == "in_force" and publication_status != "published":
    invalid = True
elif legal_status == "in_force" and version_status not in {"final", "consolidated"}:
    invalid = True
elif version_status == "consolidated" and legal_status not in {"adopted", "in_force", "superseded"}:
    invalid = True
else:
    invalid = False
```

Emit one `status_combination` issue on `publication_status/version_status/legal_status`. These rules intentionally allow a formally published draft, revised proposal or non-binding final document.

- [ ] **Step 6: Run the focused tests.**

Run: `python -m pytest tests/test_validate.py -q`

Expected: all validation tests pass.

- [ ] **Step 7: Commit validation.**

```powershell
git add src/observatory/validate.py tests/test_validate.py
git commit -m "feat: validate classification and document statuses"
```

---

### Task 3: Deterministically classify all existing document records

**Files:**

- Create: `scripts/migrate_document_classifications.py`
- Create: `tests/test_migrate_document_classifications.py`
- Modify: all existing `data/documents/*.json`
- Modify: `tests/test_seed_corpus.py`

**Interfaces:**

- Consumes: canonical document IDs and `institution_roles`.
- Produces: `sector_tags_for(document_id: str) -> list[str]`, `provenance_tags_for(document_id: str, institution_ids: set[str]) -> list[str]`, and `migrate_document(path: Path) -> bool`.

- [ ] **Step 1: Write failing tests for complete deterministic migration.**

```python
def test_every_existing_document_receives_required_classifications():
    for path in sorted(Path("data/documents").glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        assert document["sector_tags"]
        assert len(document["sector_tags"]) == len(set(document["sector_tags"]))
        assert document["provenance_tags"]
        assert "officially_published" in document["provenance_tags"]


def test_migration_is_idempotent(tmp_path):
    copied = tmp_path / "document.json"
    copied.write_bytes(Path("data/documents/artificial-intelligence-act.json").read_bytes())
    migrate_document(copied)
    before = copied.read_bytes()
    assert migrate_document(copied) is False
    assert copied.read_bytes() == before
```

Also assert that the number and ordered list of `(id, slug)` pairs is unchanged before and after the migration script.

- [ ] **Step 2: Run the migration tests and verify failure.**

Run: `python -m pytest tests/test_migrate_document_classifications.py tests/test_seed_corpus.py -q`

Expected: failure because existing documents do not contain the required fields and the migration module does not exist.

- [ ] **Step 3: Implement explicit classification rules.**

Use `general_cross_sector` as the reviewed classification for the present AI Act-centred corpus, then add evidence-backed sector tags through this explicit override map:

```python
SECTOR_OVERRIDES = {
    "ecb-opinion-con-2021-40": ["general_cross_sector", "financial_services"],
    "ecb-opinion-con-2026-10": ["general_cross_sector", "financial_services"],
    "ecb-technical-working-document-con-2026-10": ["general_cross_sector", "financial_services"],
    "ep-ai-act-cult-opinion-pe-719637": ["education", "media_and_culture"],
    "ep-ai-omnibus-cult-opinion-pe-784261": ["education", "media_and_culture"],
    "ep-ai-act-envi-opinion-pe-699056": ["agriculture_and_environment", "health"],
    "ep-ai-act-itre-opinion-pe-719801": ["industry_and_manufacturing", "research_and_innovation"],
    "ep-ai-act-juri-opinion-pe-719827": ["intellectual_property", "justice"],
    "ep-ai-omnibus-juri-opinion-pe-784179": ["intellectual_property", "justice"],
    "ep-ai-act-tran-opinion-pe-730085": ["transport_and_mobility"],
}
```

Map institutions exactly:

```python
EU_INSTITUTIONS = {
    "european-commission", "european-parliament",
    "council-of-the-european-union", "european-central-bank",
}
EU_BODIES = {
    "european-economic-and-social-committee",
    "european-data-protection-supervisor", "european-data-protection-board",
    "european-committee-of-the-regions",
    "european-artificial-intelligence-board",
}
EU_EXPERT_GROUPS = {"high-level-expert-group-on-ai"}
EU_INSTITUTION_SERVICES = {"european-ai-office"}

OFFICIAL_CONSULTATION_DOCUMENTS = {
    "draft-guidance-serious-ai-incidents-2025",
    "draft-serious-ai-incident-report-template-2025",
    "draft-high-risk-classification-guidelines-2026",
    "draft-high-risk-classification-guidelines-annex-i-2026",
    "draft-high-risk-classification-guidelines-annex-iii-2026",
    "draft-transparency-guidelines-2026",
}
```

Always include `officially_published`. Add `official_consultation_material` for the explicit set above and `joint_institutional` when more than one distinct institution is named in `institution_roles`. Sort both arrays according to their controlled-vocabulary order, not alphabetically. Fail with a clear document ID when no authoring-origin tag can be derived; do not silently label an unknown origin. Before executing the migration, verify each consultation override against its existing official source link; remove an ID from the set if that official evidence does not identify the text as consultation material.

- [ ] **Step 4: Implement stable file rewriting.**

`migrate_document` must load UTF-8 JSON, set only `sector_tags`, `provenance_tags` and `updated_at` when classifications change, and write `json.dumps(record, indent=2, ensure_ascii=False) + "\n"`. It returns `True` only when bytes change. The CLI accepts `--data-root`, defaulting to `data/documents`, and prints changed record IDs in sorted order.

- [ ] **Step 5: Run the migration once and inspect its bounded diff.**

Run: `python scripts/migrate_document_classifications.py --data-root data/documents`

Run: `git diff --stat -- data/documents`

Expected: exactly the existing document files change; no IDs, slugs, official metadata, relationships or source links change.

- [ ] **Step 6: Run migration and full canonical validation again.**

Run: `python scripts/migrate_document_classifications.py --data-root data/documents`

Expected: no changed IDs are printed.

Run: `python -m pytest tests/test_migrate_document_classifications.py tests/test_seed_corpus.py tests/test_validate.py -q`

Expected: all tests pass and every canonical document validates.

- [ ] **Step 7: Commit the migration.**

```powershell
git add scripts/migrate_document_classifications.py tests/test_migrate_document_classifications.py tests/test_seed_corpus.py data/documents
git commit -m "data: classify existing EU AI documents"
```

---

### Task 4: Normalise and export document classifications

**Files:**

- Modify: `schema/database.sql`
- Modify: `src/observatory/build_db.py`
- Modify: `src/observatory/export_public.py`
- Modify: `tests/test_build_db.py`
- Modify: `tests/test_export_public.py`

**Interfaces:**

- Consumes: canonical `sector_tags` and `provenance_tags` arrays.
- Produces: `document_sector_tags(document_id, sector_tag)`, `document_provenance_tags(document_id, provenance_tag)` and public `DocumentRecord` arrays ordered by controlled-vocabulary order.

- [ ] **Step 1: Add failing SQLite and export tests.**

Extend the existing one-document assertions:

```python
assert connection.execute(
    "SELECT document_id, sector_tag FROM document_sector_tags ORDER BY sector_tag"
).fetchall() == [("example-document", "general_cross_sector")]

assert connection.execute(
    "SELECT document_id, provenance_tag FROM document_provenance_tags ORDER BY provenance_tag"
).fetchall() == [
    ("example-document", "eu_institution_authored"),
    ("example-document", "officially_published"),
]

document = payload["documents"][0]
assert document["sector_tags"] == ["general_cross_sector"]
assert document["provenance_tags"] == [
    "eu_institution_authored", "officially_published"
]
```

- [ ] **Step 2: Run the focused tests and verify failure.**

Run: `python -m pytest tests/test_build_db.py tests/test_export_public.py -q`

Expected: missing-table or missing-key failures.

- [ ] **Step 3: Add normalised junction tables.**

Append to `schema/database.sql`:

```sql
CREATE TABLE document_sector_tags (
    document_id TEXT NOT NULL REFERENCES documents(id),
    sector_tag TEXT NOT NULL,
    PRIMARY KEY (document_id, sector_tag)
);

CREATE TABLE document_provenance_tags (
    document_id TEXT NOT NULL REFERENCES documents(id),
    provenance_tag TEXT NOT NULL,
    PRIMARY KEY (document_id, provenance_tag)
);
```

- [ ] **Step 4: Insert and export the arrays.**

In `_insert_document_supporting_rows`, call the existing junction-row helper once per new array. In `export_public.py`, add:

```python
def _string_values(
    connection: sqlite3.Connection,
    table: str,
    value_column: str,
    document_id: str,
) -> list[str]:
    query = f"SELECT {value_column} FROM {table} WHERE document_id = ? ORDER BY rowid"
    return [row[0] for row in connection.execute(query, (document_id,)).fetchall()]
```

Call the helper only with the two module-owned constant table/column pairs; never pass request or record data into its identifiers. Preserve canonical order by inserting arrays in canonical order and selecting by `rowid`.

- [ ] **Step 5: Run deterministic export tests.**

Run: `python -m pytest tests/test_build_db.py tests/test_export_public.py -q`

Expected: all tests pass and two exports from the same input are byte-identical.

- [ ] **Step 6: Commit database support.**

```powershell
git add schema/database.sql src/observatory/build_db.py src/observatory/export_public.py tests/test_build_db.py tests/test_export_public.py
git commit -m "feat: export document classifications"
```

---

### Task 5: Expand the source registry and candidate inventory contracts

**Files:**

- Modify: `schema/source-sweep.schema.json`
- Modify: `schema/corpus-inventory.schema.json`
- Modify: `research/source-sweep.json`
- Modify: `research/corpus-inventory.json`
- Modify: `src/observatory/validate.py`
- Modify: `tests/test_research_inventory.py`

**Interfaces:**

- Consumes: canonical document and source IDs plus the controlled document-type, sector and provenance vocabularies.
- Produces: validated `coverage_cutoff`, source status and candidate classification fields consumed by `build_public_coverage_summary` in Task 6.

- [ ] **Step 1: Write failing contract tests for the source registry.**

Assert this exact required shape for every source entry:

```python
assert sweep["coverage_cutoff"] == "2026-09-04"
for source in sweep["sources"]:
    assert source["source_family"].strip()
    assert source["covered_from"] <= source["covered_through"]
    assert source["covered_through"] <= source["coverage_cutoff"]
    assert len(source["covered_document_types"]) == len(set(source["covered_document_types"]))
    assert len(source["covered_sector_tags"]) == len(set(source["covered_sector_tags"]))
    assert source["discovery_method"].strip()
    assert source["scan_status"] in {
        "not_started", "in_progress", "reviewed", "gap_found", "recheck_due"
    }
    assert source["reviewer"].strip()
    assert source["verification_note"].strip()
```

An empty `covered_document_types` means the source is not restricted by document type. An empty `covered_sector_tags` means it is not restricted to a named sector; document records still require a non-empty sector classification.

- [ ] **Step 2: Write failing candidate-decision tests.**

Require these new fields: `commissioning_body`, `candidate_provenance`, `provisional_sector_tags`, `discovered_at`, `reviewed_at` and `reviewed_by`. Add tests that:

```python
assert candidate["candidate_provenance"] in {
    "eu_institution_authored", "eu_agency_or_body_authored",
    "eu_expert_group_authored", "eu_commissioned_external",
    "joint_institutional", "official_consultation_material",
    "officially_published", "third_party_submission", "unknown_pending_review"
}
```

For `included` and `merged`, require a non-empty provisional sector list, non-null review timestamp/reviewer, and a matched canonical document. For `excluded`, require non-null review timestamp/reviewer but no document ID. For `pending`, require `document_id` and `merged_into_document_id` to be null; allow an empty provisional sector list and `unknown_pending_review`.

- [ ] **Step 3: Run the focused audit tests and verify failure.**

Run: `python -m pytest tests/test_research_inventory.py -q`

Expected: the existing three-state source statuses and old candidate shape fail the new assertions.

- [ ] **Step 4: Replace the source-sweep schema.**

At top level require `generated_at`, `coverage_cutoff` and `sources`. Require every source to contain:

```json
{
  "id": "stable-source-id",
  "name": "Human-readable official entrance",
  "institution": "European Commission",
  "source_family": "European Commission policy libraries",
  "url": "https://commission.europa.eu/",
  "scope_note": "Bounded scope statement.",
  "covered_from": "2018-01-01",
  "covered_through": "2026-09-04",
  "covered_document_types": [],
  "covered_sector_tags": [],
  "discovery_method": "Documented site or register query.",
  "scan_status": "reviewed",
  "checked_at": "2026-09-04T00:00:00Z",
  "coverage_cutoff": "2026-09-04",
  "reviewer": "Yichen Hao",
  "verification_note": "The documented query completed without an unresolved access failure."
}
```

Apply ISO date/date-time patterns and disallow additional properties. Vocabulary membership is enforced in Python so both audit schemas share the canonical vocabulary file.

- [ ] **Step 5: Replace the candidate-inventory schema.**

Keep every existing candidate field and add:

```json
"commissioning_body": {"type": ["string", "null"]},
"candidate_provenance": {"type": "string", "minLength": 1},
"provisional_sector_tags": {
  "type": "array", "uniqueItems": true, "items": {"type": "string", "minLength": 1}
},
"discovered_at": {"type": "string", "format": "date-time"},
"reviewed_at": {"type": ["string", "null"], "format": "date-time"},
"reviewed_by": {"type": ["string", "null"]}
```

- [ ] **Step 6: Extend cross-file audit validation.**

Reject:

- a source `covered_document_types` value absent from `document_type`;
- a source or candidate sector value absent from `sector_tag`;
- a candidate provenance value absent from public `provenance_tag` plus the two inventory-only values;
- an included candidate whose classifications do not equal its canonical document classifications;
- `third_party_submission` or `unknown_pending_review` on an included candidate;
- per-source `coverage_cutoff` later than the top-level cutoff; and
- a non-pending decision without `reviewed_at` and `reviewed_by`.

Use issue codes `audit_vocabulary`, `audit_classification_mismatch`, `audit_cutoff` and `audit_decision` with paths rooted at `research/source-sweep.json` or `research/corpus-inventory.json`.

- [ ] **Step 7: Migrate the two research files deliberately.**

Map old statuses as follows: `complete -> reviewed`, `in_progress -> in_progress`, `pending -> not_started`. Set the top-level and per-source cutoff to `2026-09-04`; use each source's existing `checked_at` date as `covered_through` when earlier, otherwise `2026-09-04`. Populate `source_family` and `discovery_method` from the existing registered entrance, not from a generic site-wide claim. Use empty coverage arrays only under the explicit unrestricted meaning defined above.

For included candidates, copy `sector_tags` and the most specific non-`officially_published` provenance value from the matched canonical document, then add `officially_published` when present there. Use `commissioning_body` only for a formally commissioned study. Set `discovered_at` to the existing audit generation timestamp when no more precise timestamp is recorded; set `reviewed_at` and `reviewed_by` for every decided row.

- [ ] **Step 8: Run audit validation tests.**

Run: `python -m pytest tests/test_research_inventory.py tests/test_validate.py -q`

Expected: all tests pass with zero pending candidate leaking into canonical publication.

- [ ] **Step 9: Commit audit contracts and data.**

```powershell
git add schema/source-sweep.schema.json schema/corpus-inventory.schema.json research/source-sweep.json research/corpus-inventory.json src/observatory/validate.py tests/test_research_inventory.py
git commit -m "feat: expand corpus audit metadata"
```

---

### Task 6: Generate a public cutoff and audit summary

**Files:**

- Create: `src/observatory/coverage.py`
- Create: `tests/test_coverage.py`
- Modify: `src/observatory/export_public.py`
- Modify: `src/observatory/pipeline.py`
- Modify: `tests/test_export_public.py`
- Modify: `tests/test_pipeline.py`

**Interfaces:**

- Consumes: `build_public_coverage_summary(research_root: Path) -> dict[str, object]` output in the pipeline.
- Produces: `export_public(database_path: Path, output_path: Path, generated_at: str, audit_summary: Mapping[str, object]) -> None` and an expanded public `coverage` object.

- [ ] **Step 1: Write failing aggregate tests.**

Create a temporary source sweep with five statuses and an inventory with one row per decision, then assert:

```python
assert build_public_coverage_summary(research_root) == {
    "coverage_cutoff": "2026-09-04",
    "coverage_statement": (
        "Comprehensive within the documented inclusion boundary, "
        "verified through 4 September 2026."
    ),
    "source_families": {
        "total": 5,
        "by_status": {
            "not_started": 1,
            "in_progress": 1,
            "reviewed": 1,
            "gap_found": 1,
            "recheck_due": 1,
        },
    },
    "inventory": {"included": 1, "merged": 1, "excluded": 1, "pending": 1},
    "unresolved_candidates": 1,
}
```

Also assert that candidate titles, URLs and decision reasons are absent from the returned object.

- [ ] **Step 2: Run the coverage tests and verify failure.**

Run: `python -m pytest tests/test_coverage.py -q`

Expected: import failure because `observatory.coverage` does not exist.

- [ ] **Step 3: Implement the aggregate module.**

Load both UTF-8 JSON files. Group registry rows by exact `source_family`; a family is `reviewed` only when every row in that family is reviewed, otherwise choose the first present state in this priority order: `gap_found`, `recheck_due`, `in_progress`, `not_started`. Count the resulting family states with a zero-filled dictionary in the vocabulary order above. Format the cutoff with `date.fromisoformat` and, on Windows, avoid `%-d` by formatting the numeric day directly:

```python
cutoff = date.fromisoformat(source_sweep["coverage_cutoff"])
human_cutoff = f"{cutoff.day} {cutoff.strftime('%B %Y')}"
```

The function performs no network access and exposes aggregates only.

- [ ] **Step 4: Pass the aggregate through the atomic pipeline.**

After both validation calls succeed, build the summary and pass it to `export_public`. Extend `_coverage` by merging the existing document date/count metrics with the supplied audit keys. Do not recalculate `coverage_cutoff` from source `last_verified_at` dates.

- [ ] **Step 5: Add pipeline regression tests.**

Assert the generated public JSON contains the exact cutoff statement and decision counts, and that a malformed cutoff fails before an existing output pair is touched. Retain the existing assertion that a pending candidate's title does not appear anywhere in public JSON.

- [ ] **Step 6: Run focused backend tests.**

Run: `python -m pytest tests/test_coverage.py tests/test_export_public.py tests/test_pipeline.py -q`

Expected: all tests pass and failed audit validation leaves prior SQLite and JSON bytes unchanged.

- [ ] **Step 7: Commit coverage export.**

```powershell
git add src/observatory/coverage.py src/observatory/export_public.py src/observatory/pipeline.py tests/test_coverage.py tests/test_export_public.py tests/test_pipeline.py
git commit -m "feat: publish auditable corpus coverage"
```

---

### Task 7: Extend browser types and pure filtering logic

**Files:**

- Modify: `web/src/lib/types.ts`
- Modify: `web/src/lib/filter.ts`
- Modify: `web/tests/fixtures/documents.ts`
- Modify: `web/tests/filter.test.ts`
- Modify: `web/tests/filter.node.test.mjs`
- Modify: `web/tests/data.test.ts`
- Modify: `web/tests/timeline.node.test.mjs`

**Interfaces:**

- Consumes: public JSON arrays and coverage shape from Tasks 4 and 6.
- Produces: `CorpusCriteria.sector`, `CorpusCriteria.provenance`, `TimelineCriteria.view` and `TimelineEntry.recordLevel` used by Astro components.

- [ ] **Step 1: Add failing TypeScript filter tests.**

Give the two existing document fixtures distinct arrays, then assert:

```typescript
expect(filterDocuments(publishedDocuments, {
  sector: 'financial_services',
  provenance: 'eu_institution_authored',
}).map((document) => document.id)).toEqual(['artificial-intelligence-act-2024']);

expect(buildCorpusSearchParams(new URLSearchParams('ref=phd'), {
  sector: 'health',
  provenance: 'eu_agency_or_body_authored',
}).toString()).toBe(
  'ref=phd&sector=health&provenance=eu_agency_or_body_authored'
);
```

Add a timeline fixture with `record_level: 'version'`; assert the default timeline excludes it and `{view: 'all'}` includes it. Unlinked policy events with `recordLevel: null` remain visible in the principal view.

- [ ] **Step 2: Run web unit tests and verify failure.**

Run: `npm --prefix web test`

Expected: missing property/type assertions and incorrect timeline default.

- [ ] **Step 3: Extend public TypeScript types.**

Add to `DocumentRecord`:

```typescript
sector_tags: string[];
provenance_tags: string[];
```

Add to `CorpusCoverage`:

```typescript
coverage_cutoff: string;
coverage_statement: string;
source_families: {
  total: number;
  by_status: Record<'not_started' | 'in_progress' | 'reviewed' | 'gap_found' | 'recheck_due', number>;
};
inventory: Record<'included' | 'merged' | 'excluded' | 'pending', number>;
unresolved_candidates: number;
```

- [ ] **Step 4: Extend corpus parsing, serialisation and filtering.**

Add `sector` and `provenance` to `CorpusCriteria` and `corpusStringCriteriaKeys`. Match each criterion using `document.sector_tags.some(...)` and `document.provenance_tags.some(...)`; preserve logical AND with every existing criterion.

- [ ] **Step 5: Add the timeline principal/all rule.**

Add:

```typescript
export interface TimelineCriteria {
  view?: 'principal' | 'all';
  // existing scalar fields remain
}

export interface TimelineEntry {
  // existing fields remain
  recordLevel: DocumentRecord['record_level'] | null;
}
```

Documents inherit their record level; linked events inherit the linked document's level; unlinked events use null. In `filterTimeline`, require `criteria.view === 'all' || entry.recordLevel === null || entry.recordLevel === 'principal'`.

- [ ] **Step 6: Update every fixture coverage object and run unit tests.**

Use a small deterministic audit object with cutoff `2026-09-04`. Run: `npm --prefix web test`

Expected: all Node and Vitest tests pass.

- [ ] **Step 7: Commit web data contracts.**

```powershell
git add web/src/lib/types.ts web/src/lib/filter.ts web/tests
git commit -m "feat: filter corpus by sector and provenance"
```

---

### Task 8: Add classification, timeline and coverage UI

**Files:**

- Modify: `web/src/components/CorpusExplorer.astro`
- Modify: `web/src/components/Timeline.astro`
- Modify: `web/src/pages/corpus/[slug].astro`
- Modify: `web/src/pages/methodology.astro`
- Modify: `web/src/styles/global.css`
- Modify: `web/tests/corpus.source.test.mjs`
- Modify: `web/tests/timeline-policy-map.source.test.mjs`
- Modify: `web/tests/accessibility.source.test.mjs`
- Modify: `web/tests/touch-layout.source.test.mjs`
- Modify: `web/tests/site.spec.ts`
- Modify: `web/tests/no-js.spec.ts`

**Interfaces:**

- Consumes: the `DocumentRecord`, `CorpusCoverage`, `CorpusCriteria` and `TimelineCriteria` shapes from Task 7.
- Produces: accessible English controls and record classifications without changing any route.

- [ ] **Step 1: Add failing source and browser assertions.**

Require:

- labelled Corpus selects named `sector` and `provenance`;
- card text headed `Sectors` and `Provenance`;
- a Timeline control named `view` with `principal` and `all` values;
- document detail headings `Research classifications` and `Production provenance`;
- Methodology text containing the exact public coverage statement and unresolved-candidate count;
- keyboard-reachable native controls with visible focus; and
- no horizontal overflow at 375 px.

In Playwright, select `financial_services` and assert every visible result card contains the human-readable label `Financial services`; then select `All documents and versions` on Timeline and assert its count does not decrease.

- [ ] **Step 2: Run focused frontend tests and verify failure.**

Run: `npm --prefix web test`

Run: `npm --prefix web run build`

Expected: source assertions fail first; the production build remains useful for catching Astro/TypeScript errors after implementation begins.

- [ ] **Step 3: Add Corpus controls and labels.**

Build sorted unique option lists from all documents. Use `vocabularyLabel` for display, raw controlled values for `<option value>`, and these exact labels:

```html
<label>Sector <select name="sector">...</select></label>
<label>Provenance <select name="provenance">...</select></label>
```

Render tags on every result card under separate `Sectors` and `Provenance` labels. Update the existing client script to read/write the new criteria through the pure helpers; do not duplicate filtering logic in the component.

- [ ] **Step 4: Add the Timeline view control.**

Make `Principal documents` the checked default and `All documents and versions` the alternate value. Pass the selected view into `filterTimeline`; keep year headings hidden when all their items are filtered out. The reset action returns to principal view.

- [ ] **Step 5: Separate document-page facts.**

Create a `Research classifications` section containing sector tags, research concepts, policy membership, policy stage and corpus tier. Its introductory sentence must state that these are researcher classifications.

Create a separate `Production provenance` section containing provenance tags and named institution roles. Keep `Official sources and identifiers` unchanged as a third section so authoring, publishing and hosting are not conflated.

- [ ] **Step 6: Replace the Methodology scope and coverage copy.**

State that the corpus covers official EU documents substantively concerning AI from 1 January 2018 through the displayed cutoff, including formally published drafts and sector-specific materials. Render:

```astro
<p>{data.coverage.coverage_statement}</p>
<dl>
  <dt>Registered source families</dt><dd>{data.coverage.source_families.total}</dd>
  <dt>Reviewed through cutoff</dt><dd>{data.coverage.source_families.by_status.reviewed}</dd>
  <dt>Included candidates</dt><dd>{data.coverage.inventory.included}</dd>
  <dt>Excluded candidates</dt><dd>{data.coverage.inventory.excluded}</dd>
  <dt>Unresolved candidates</dt><dd>{data.coverage.unresolved_candidates}</dd>
</dl>
```

Do not describe a source count as proof of record-level completeness.

- [ ] **Step 7: Add responsive styling without redesigning the site.**

Reuse existing form, pill and metadata styles. Permit filter rows and tag lists to wrap; set controls to `min-width: 0` inside the grid; retain the existing focus outline; keep the established typography and colour tokens.

- [ ] **Step 8: Run frontend verification.**

Run: `npm --prefix web test`

Run: `npm --prefix web run build`

Run: `npm --prefix web run test:e2e`

Expected: all unit/source tests pass, Astro reports no type errors, existing routes resolve, filters work without JavaScript regressions, and desktop/mobile browser tests pass.

- [ ] **Step 9: Commit the interface.**

```powershell
git add web/src web/tests
git commit -m "feat: expose comprehensive corpus classifications"
```

---

### Task 9: Document the contract and verify the complete Stage 1 build

**Files:**

- Modify: `docs/data-dictionary.md`
- Modify: `README.md`
- Modify: `tests/test_public_build.py`
- Modify: `web/tests/final-review.source.test.mjs`

**Interfaces:**

- Consumes: all Stage 1 schema, audit, export and UI behaviour.
- Produces: contributor documentation and a verified production artefact ready for the priority-backfill plan.

- [ ] **Step 1: Add failing documentation and public-build assertions.**

Require the data dictionary to define every sector and provenance value, the audit-only values, empty coverage-array semantics, and the distinction among `publication_status`, `version_status` and `legal_status`. Require README to use this exact sentence:

> Comprehensive within the documented inclusion boundary, verified through 4 September 2026.

Extend the public-build test to require both classification arrays on every public document and verify `coverage.coverage_cutoff == "2026-09-04"`.

- [ ] **Step 2: Run focused documentation/public-build tests and verify failure.**

Run: `python -m pytest tests/test_public_build.py -q`

Run: `node --test web/tests/final-review.source.test.mjs`

- [ ] **Step 3: Update the data dictionary and README.**

Document:

- all 20 sector tags and seven published provenance tags;
- `third_party_submission` and `unknown_pending_review` as inventory-only;
- formal publication rather than adoption as the inclusion threshold;
- source status meanings;
- candidate decision meanings;
- cutoff semantics;
- principal/all-record view behaviour; and
- the three-stage expansion sequence, identifying Stage 1 as schema/interface rather than a completed EU-wide sweep.

- [ ] **Step 4: Run the full backend suite and build canonical artefacts.**

Run: `python -m pytest -q`

Run: `python -m observatory.pipeline --project-root . --timestamp 2026-09-04T00:00:00Z`

Run:

```powershell
$databaseHash = (Get-FileHash generated/observatory.sqlite -Algorithm SHA256).Hash
$jsonHash = (Get-FileHash generated/public-data.json -Algorithm SHA256).Hash
python -m observatory.pipeline --project-root . --timestamp 2026-09-04T00:00:00Z
if ((Get-FileHash generated/observatory.sqlite -Algorithm SHA256).Hash -ne $databaseHash) { throw "SQLite output is not deterministic" }
if ((Get-FileHash generated/public-data.json -Algorithm SHA256).Hash -ne $jsonHash) { throw "Public JSON output is not deterministic" }
```

Expected: all tests pass and both SHA-256 comparisons succeed after a same-timestamp rebuild.

- [ ] **Step 5: Run the full production-site suite.**

Run: `npm --prefix web test`

Run: `npm --prefix web run build`

Run: `npm --prefix web run check:public`

Run: `npm --prefix web run test:e2e`

Expected: every command exits zero; the public scanner finds no draft, pending-review, local-path or unsafe-link leakage.

- [ ] **Step 6: Inspect the final repository delta.**

Run: `git status --short`

Run: `git diff --check`

Run: `git diff --name-only origin/main...HEAD`

Expected: only Stage 1 schema, migration, audit, backend, generated-data, web, test and documentation files appear; no existing slug or route is removed.

- [ ] **Step 7: Commit final documentation and generated outputs.**

```powershell
git add README.md docs/data-dictionary.md tests/test_public_build.py web/tests/final-review.source.test.mjs generated/public-data.json generated/observatory.sqlite
git commit -m "docs: describe comprehensive corpus coverage"
```

---

## Stage 1 Exit Gate

Stage 1 is complete only when all of the following are true:

- every canonical document has valid non-empty sector and provenance arrays;
- SQLite and public JSON reproduce those classifications deterministically;
- inventory-only provenance values cannot enter canonical or public records;
- source/candidate audit files validate against the cutoff and decision rules;
- the public payload exposes aggregate audit status without candidate-level leakage;
- Corpus and Timeline preserve principal defaults and expose all records deliberately;
- document pages visually separate research classification, production provenance and official source evidence;
- Methodology reports the exact cutoff and unresolved count without claiming permanent completeness;
- every prior public route still resolves; and
- all backend, frontend, accessibility, responsive, production-build and public-leakage checks pass.

Only after this gate passes should the project execute the separate priority-backfill plan and then the EU-wide source-sweep plan.
