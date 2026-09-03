# EU AI Policy Observatory Database Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the validated English JSON corpus pipeline, generated SQLite database and publication-safe JSON export for the EU AI Policy Observatory.

**Architecture:** One-record-per-file JSON is canonical. A Python package validates records against one JSON Schema and controlled vocabularies, performs cross-record checks, builds a normalised SQLite database and exports only records whose `publication_status` is `published`. Generated files are reproducible build output and are not committed.

**Tech Stack:** Python 3.11+, `jsonschema` 4.x, `pytest` 8.x, SQLite 3, JSON Schema Draft 2020-12.

**Spec:** `docs/superpowers/specs/2026-09-03-eu-ai-policy-observatory-design.md`

## Global Constraints

- All canonical data, code, error messages and public documentation use British academic English.
- `Policy`, `Document` and `Event` remain separate entities.
- Official metadata and researcher-authored assessments remain structurally separate.
- Canonical IDs are stable lowercase kebab-case strings.
- Dates use ISO 8601 `YYYY-MM-DD`.
- Only records with `publication_status: published` enter the public export.
- No network retrieval, automatic crawling or LLM functionality is introduced in this plan.
- Generated SQLite and JSON outputs remain under `generated/` and are not committed.
- Each task ends with its own tests and commit.

---

## File Structure

```text
pyproject.toml                         Python metadata and test configuration
src/observatory/__init__.py            Public package version
src/observatory/types.py               Typed record and validation-issue definitions
src/observatory/io.py                  Canonical record discovery and JSON loading
src/observatory/validate.py            Schema, vocabulary and cross-record validation
src/observatory/build_db.py            SQLite schema application and record insertion
src/observatory/export_public.py       Publication-safe JSON export
src/observatory/pipeline.py            End-to-end build orchestration and CLI
schema/record.schema.json              Canonical JSON Schema with entity definitions
schema/controlled-vocabularies.json    Closed vocabulary values
schema/database.sql                    Normalised SQLite schema
data/<entity-type>/*.json              One canonical record per file
tests/fixtures/                         Minimal valid and invalid datasets
tests/test_io.py                        Record loading tests
tests/test_validate.py                  Validation tests
tests/test_build_db.py                  Relational database tests
tests/test_export_public.py             Publication-boundary tests
tests/test_pipeline.py                  Clean-build integration test
docs/data-dictionary.md                English field and vocabulary documentation
```

### Task 1: Establish the Python Package and Canonical Record Contract

**Files:**
- Create: `pyproject.toml`
- Create: `src/observatory/__init__.py`
- Create: `src/observatory/types.py`
- Create: `schema/record.schema.json`
- Create: `schema/controlled-vocabularies.json`
- Create: `tests/test_schema_contract.py`

**Interfaces:**
- Produces: `ValidationIssue(code: str, record_path: str, field: str, message: str)`.
- Produces: `ENTITY_DIRECTORIES: tuple[str, ...]` containing the seven canonical record directories.
- Produces: a Draft 2020-12 schema selected by the `entity_type` discriminator.
- Produces: controlled vocabularies consumed by `validate_records()` in Task 2.

- [ ] **Step 1: Create the Python project configuration**

Create `pyproject.toml` with a Python 3.11 floor, package source under `src`, `jsonschema>=4.23,<5`, and test dependencies `pytest>=8,<9`:

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "eu-ai-policy-observatory"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["jsonschema>=4.23,<5"]

[project.optional-dependencies]
test = ["pytest>=8,<9"]

[project.scripts]
observatory-build = "observatory.pipeline:main"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

- [ ] **Step 2: Write the failing contract test**

Create `tests/test_schema_contract.py`:

```python
from observatory.types import ENTITY_DIRECTORIES, ValidationIssue


def test_entity_directories_are_explicit_and_stable():
    assert ENTITY_DIRECTORIES == (
        "policies",
        "documents",
        "events",
        "concepts",
        "institutions",
        "relationships",
        "sources",
    )


def test_validation_issue_is_immutable():
    issue = ValidationIssue("required", "documents/example.json", "celex", "Missing CELEX")
    assert issue.code == "required"
    assert issue.record_path.endswith("example.json")
```

- [ ] **Step 3: Run the contract test and confirm failure**

Run:

```powershell
python -m pip install -e ".[test]"
python -m pytest tests/test_schema_contract.py -q
```

Expected: collection fails because `observatory.types` does not exist.

- [ ] **Step 4: Implement the package contract**

Create `src/observatory/__init__.py`:

```python
__version__ = "0.1.0"
```

Create `src/observatory/types.py`:

```python
from dataclasses import dataclass

ENTITY_DIRECTORIES = (
    "policies",
    "documents",
    "events",
    "concepts",
    "institutions",
    "relationships",
    "sources",
)


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    record_path: str
    field: str
    message: str
```

- [ ] **Step 5: Define the controlled vocabularies**

Create `schema/controlled-vocabularies.json` with these exact keys and initial values:

```json
{
  "publication_status": ["draft", "pending_review", "verified", "published"],
  "corpus_tier": ["core", "directly_related", "contextual", "excluded"],
  "relationship_basis": ["official", "analytical"],
  "institution_role": ["author", "proposer", "adopter", "publisher", "contributor"],
  "document_type": ["communication", "coordinated_plan", "expert_guidelines", "white_paper", "legislative_proposal", "regulation"],
  "legal_status": ["non_binding", "proposed", "adopted", "in_force", "withdrawn", "superseded"],
  "policy_status": ["active", "completed", "withdrawn", "superseded"],
  "policy_stage": ["agenda_setting", "coordination", "consultation", "proposal", "negotiation", "adoption", "implementation"],
  "event_type": ["proposal", "publication", "adoption", "entry_into_force", "application", "amendment", "withdrawal", "implementation"],
  "relationship_type": ["part_of", "precedes", "adopted_as", "replaces", "amends", "implements", "based_on", "related_to", "supersedes"],
  "verification_status": ["unverified", "pending", "verified"],
  "source_type": ["eur_lex", "eli", "commission_webpage", "official_pdf", "publications_office"]
}
```

- [ ] **Step 6: Define the discriminated JSON Schema**

Create `schema/record.schema.json` using Draft 2020-12. Define a common envelope requiring `id`, `entity_type`, `publication_status`, `created_at` and `updated_at`; require `id` to match `^[a-z0-9]+(?:-[a-z0-9]+)*$`; use `oneOf` references for all seven entity types and `unevaluatedProperties: false` so misspelled fields fail validation. Define `corpus_assessment`, `institution_roles`, `policy_ids`, `concept_ids`, `source_ids` and `snapshots` as nested properties on document records so the JSON remains one-record-per-file while the SQLite builder normalises them into supporting tables. A snapshot requires `id`, `source_id`, `retrieved_at`, `format`, `content_hash` and nullable `archived_path`.

The document definition must require:

```json
[
  "official_title",
  "short_title",
  "document_type",
  "publication_date",
  "legal_status",
  "language",
  "institution_roles",
  "policy_ids",
  "concept_ids",
  "source_ids",
  "corpus_assessment"
]
```

The `corpus_assessment` definition must require `corpus_tier`, `policy_stage`, `inclusion_rationale`, `researcher_notes`, `review_status`, `reviewed_by` and `reviewed_at`.

- [ ] **Step 7: Run the contract tests**

Run:

```powershell
python -m pytest tests/test_schema_contract.py -q
```

Expected: `2 passed`.

- [ ] **Step 8: Commit the record contract**

```powershell
git add pyproject.toml src/observatory schema tests/test_schema_contract.py
git commit -m "feat: define canonical record contract"
```

### Task 2: Load and Validate Canonical JSON Records

**Files:**
- Create: `src/observatory/io.py`
- Create: `src/observatory/validate.py`
- Create: `tests/fixtures/valid/data/documents/example-document.json`
- Create: `tests/fixtures/valid/data/policies/example-policy.json`
- Create: `tests/fixtures/valid/data/concepts/risk.json`
- Create: `tests/fixtures/valid/data/institutions/european-commission.json`
- Create: `tests/fixtures/valid/data/sources/example-source.json`
- Create: `tests/fixtures/invalid/data/documents/broken-document.json`
- Create: `tests/test_io.py`
- Create: `tests/test_validate.py`

**Interfaces:**
- Consumes: `ENTITY_DIRECTORIES` and `ValidationIssue` from Task 1.
- Produces: `load_records(data_root: Path) -> dict[str, list[LoadedRecord]]`.
- Produces: `validate_records(data_root: Path, schema_path: Path, vocabulary_path: Path) -> list[ValidationIssue]`.
- Produces: `assert_valid(...) -> None`, raising `RecordValidationError` with sorted, actionable messages.

- [ ] **Step 1: Write the failing loader test**

Create `tests/test_io.py`:

```python
from pathlib import Path

from observatory.io import load_records


def test_load_records_preserves_source_path():
    loaded = load_records(Path("tests/fixtures/valid/data"))
    document = loaded["documents"][0]
    assert document.data["id"] == "example-document"
    assert document.path.as_posix().endswith("documents/example-document.json")
```

- [ ] **Step 2: Run the loader test and confirm failure**

Run `python -m pytest tests/test_io.py -q`.

Expected: collection fails because `observatory.io` does not exist.

- [ ] **Step 3: Implement deterministic record discovery**

Create an immutable `LoadedRecord(data: dict[str, object], path: Path)` in `io.py`. Read `*.json` files from every `ENTITY_DIRECTORIES` directory in lexicographic path order, decode as UTF-8 and return empty lists for missing entity directories. Do not follow symlinks.

- [ ] **Step 4: Create minimal valid fixtures**

Create records with these stable IDs and links:

```text
example-policy
example-document → example-policy, risk, european-commission, example-source
risk
european-commission
example-source
```

Use `publication_status: published`, dates `2026-09-03`, language `en`, an official HTTPS URL and a complete corpus assessment.

- [ ] **Step 5: Run the loader test**

Run `python -m pytest tests/test_io.py -q`.

Expected: `1 passed`.

- [ ] **Step 6: Write failing validation tests**

Create `tests/test_validate.py`:

```python
from pathlib import Path

from observatory.validate import validate_records

SCHEMA = Path("schema/record.schema.json")
VOCAB = Path("schema/controlled-vocabularies.json")


def test_valid_fixture_has_no_issues():
    assert validate_records(Path("tests/fixtures/valid/data"), SCHEMA, VOCAB) == []


def test_duplicate_id_and_missing_reference_are_reported():
    issues = validate_records(Path("tests/fixtures/invalid/data"), SCHEMA, VOCAB)
    codes = {issue.code for issue in issues}
    assert "duplicate_id" in codes
    assert "missing_reference" in codes


def test_published_analytical_relationship_requires_rationale_and_evidence():
    issues = validate_records(Path("tests/fixtures/invalid/data"), SCHEMA, VOCAB)
    assert any(issue.code == "analytical_evidence" for issue in issues)


def test_published_records_cannot_reference_unpublished_dependencies():
    issues = validate_records(Path("tests/fixtures/invalid/data"), SCHEMA, VOCAB)
    assert any(issue.code == "publication_boundary" for issue in issues)
```

- [ ] **Step 7: Run the validation tests and confirm failure**

Run `python -m pytest tests/test_validate.py -q`.

Expected: collection fails because `observatory.validate` does not exist.

- [ ] **Step 8: Implement schema and cross-record validation**

Use `jsonschema.Draft202012Validator`. Return issues sorted by `(record_path, field, code)`. Implement exact checks for:

- JSON Schema errors.
- Vocabulary membership.
- A filename that does not equal `<record-id>.json` or a directory that does not match `entity_type`.
- Duplicate IDs across all entity types.
- Duplicate non-null CELEX and ELI values among documents.
- Missing `policy_ids`, `concept_ids`, `source_ids` and institution references.
- Missing source references from nested document snapshots.
- Missing source evidence for `published` or `verified` records.
- References from a `published` record to a non-published policy, concept, institution, source or relationship endpoint.
- Missing rationale or evidence for analytical relationships.
- Non-official evidence sources for official relationships.
- `updated_at` earlier than `created_at`.

Never perform HTTP requests in validation.

- [ ] **Step 9: Run loader and validation tests**

Run:

```powershell
python -m pytest tests/test_io.py tests/test_validate.py -q
```

Expected: all tests pass.

- [ ] **Step 10: Commit the validated loader**

```powershell
git add src/observatory/io.py src/observatory/validate.py tests
git commit -m "feat: validate canonical policy records"
```

### Task 3: Build the Normalised SQLite Database

**Files:**
- Create: `schema/database.sql`
- Create: `src/observatory/build_db.py`
- Create: `tests/test_build_db.py`

**Interfaces:**
- Consumes: validated loaded records from Task 2.
- Produces: `build_database(records: dict[str, list[LoadedRecord]], schema_path: Path, output_path: Path) -> Path`.
- Produces the core tables and supporting tables named in the design specification.

- [ ] **Step 1: Write the failing database test**

Create `tests/test_build_db.py`:

```python
import sqlite3
from pathlib import Path

from observatory.build_db import build_database
from observatory.io import load_records


def test_build_database_normalises_document_links(tmp_path):
    output = tmp_path / "observatory.sqlite"
    build_database(
        load_records(Path("tests/fixtures/valid/data")),
        Path("schema/database.sql"),
        output,
    )
    with sqlite3.connect(output) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert connection.execute("SELECT COUNT(*) FROM documents").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM policy_documents").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM document_concepts").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM document_sources").fetchone() == (1,)
```

- [ ] **Step 2: Run the database test and confirm failure**

Run `python -m pytest tests/test_build_db.py -q`.

Expected: collection fails because `observatory.build_db` does not exist.

- [ ] **Step 3: Define the SQLite schema**

Create `schema/database.sql` with `PRAGMA foreign_keys = ON`, text primary keys, ISO date checks and these tables:

```text
policies
documents
events
concepts
institutions
relationships
sources
corpus_assessments
document_institutions
document_snapshots
policy_documents
document_concepts
document_sources
```

Add unique partial indexes for non-null `documents.celex` and `documents.eli`, unique `documents.slug`, and composite primary keys on junction tables. Separate `documents.legal_status` from the common `publication_status`.

- [ ] **Step 4: Implement transactional database generation**

`build_database()` must:

1. Create the parent directory.
2. Build into a sibling temporary file.
3. Apply `database.sql`.
4. Insert parent entities before junction rows.
5. Store relationship endpoints as typed IDs after validation.
6. Run `PRAGMA foreign_key_check` and `PRAGMA integrity_check`.
7. Commit and atomically replace the requested output.
8. Delete the temporary file after failure.

Use only Python's standard `sqlite3`, `tempfile` and `os.replace` modules.

- [ ] **Step 5: Run the database tests**

Run `python -m pytest tests/test_build_db.py -q`.

Expected: all tests pass and integrity is `ok`.

- [ ] **Step 6: Commit the SQLite builder**

```powershell
git add schema/database.sql src/observatory/build_db.py tests/test_build_db.py
git commit -m "feat: build normalised SQLite database"
```

### Task 4: Export Publication-Safe Website Data

**Files:**
- Create: `src/observatory/export_public.py`
- Create: `tests/test_export_public.py`

**Interfaces:**
- Consumes: a generated SQLite database.
- Produces: `export_public(database_path: Path, output_path: Path, generated_at: str) -> Path`.
- Produces a stable JSON object with keys `policies`, `documents`, `events`, `concepts`, `institutions`, `relationships`, `sources` and `generated_at`.

- [ ] **Step 1: Write the failing publication-boundary test**

Create `tests/test_export_public.py`:

```python
import json
from pathlib import Path

from observatory.export_public import export_public


def test_export_excludes_every_non_published_record(built_mixed_status_database, tmp_path):
    output = tmp_path / "public-data.json"
    export_public(built_mixed_status_database, output, "2026-09-03T00:00:00Z")
    payload = json.loads(output.read_text(encoding="utf-8"))
    for collection in (
        "policies",
        "documents",
        "events",
        "concepts",
        "institutions",
        "relationships",
        "sources",
    ):
        assert {item["publication_status"] for item in payload[collection]} <= {"published"}
    assert "draft-document" not in {item["id"] for item in payload["documents"]}
```

Add a pytest fixture that builds one published and one draft document with valid referenced entities.

- [ ] **Step 2: Run the export test and confirm failure**

Run `python -m pytest tests/test_export_public.py -q`.

Expected: collection fails because `observatory.export_public` does not exist.

- [ ] **Step 3: Implement the public export**

Query only `publication_status = 'published'`. Exclude relationships if either endpoint is not published. Exclude sources not referenced by a published exported entity. Embed each document's institutions with roles, policies, concepts, corpus assessment and sources to support static page generation without further database queries.

Serialise with UTF-8, `ensure_ascii=False`, two-space indentation, alphabetically sorted object keys and deterministic array ordering by stable ID. Set `generated_at` from the build invocation parameter rather than the current clock so deterministic tests remain possible.

- [ ] **Step 4: Run the export tests**

Run `python -m pytest tests/test_export_public.py -q`.

Expected: all tests pass.

- [ ] **Step 5: Commit the public exporter**

```powershell
git add src/observatory/export_public.py tests/test_export_public.py
git commit -m "feat: export publication-safe web data"
```

### Task 5: Add the Verified Seed Corpus and End-to-End Build

**Files:**
- Create: `data/policies/*.json`
- Create: `data/documents/*.json`
- Create: `data/events/*.json`
- Create: `data/concepts/{risk,trustworthiness,accountability,compliance}.json`
- Create: `data/institutions/*.json`
- Create: `data/relationships/*.json`
- Create: `data/sources/*.json`
- Create: `src/observatory/pipeline.py`
- Create: `tests/test_pipeline.py`
- Create: `docs/data-dictionary.md`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: `validate_records()`, `build_database()` and `export_public()`.
- Produces: `run_pipeline(project_root: Path, build_timestamp: str, output_root: Path | None = None) -> BuildOutputs`.
- Produces: CLI command `observatory-build --project-root . --timestamp <ISO-8601>`.
- Produces: `generated/eu-ai-policy-observatory.sqlite` and `generated/public-data.json`.

- [ ] **Step 1: Write the failing pipeline test**

Create `tests/test_pipeline.py`:

```python
import json
import sqlite3
from pathlib import Path

from observatory.pipeline import run_pipeline


def test_repository_build_produces_database_and_public_export(tmp_path):
    outputs = run_pipeline(Path.cwd(), "2026-09-03T00:00:00Z", output_root=tmp_path)
    assert outputs.database.exists()
    assert outputs.public_json.exists()
    with sqlite3.connect(outputs.database) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    payload = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    assert len(payload["documents"]) >= 6
    assert all(item["publication_status"] == "published" for item in payload["documents"])
```

- [ ] **Step 2: Run the pipeline test and confirm failure**

Run `python -m pytest tests/test_pipeline.py -q`.

Expected: collection fails because `observatory.pipeline` does not exist.

- [ ] **Step 3: Research and enter each seed document from official sources**

For each candidate in the design specification, verify the official title, publication date, institution roles, legal status, CELEX or ELI when assigned, and official URL. Create one document JSON file and at least one source JSON file. Use these expected stable identifiers where applicable and reject any mismatch found in the official record rather than forcing the expected value:

```text
Artificial Intelligence for Europe       CELEX 52018DC0237
Coordinated Plan on Artificial Intelligence CELEX 52018DC0795
White Paper on Artificial Intelligence   CELEX 52020DC0065
AI Act proposal                          CELEX 52021PC0206
AI Liability Directive proposal          CELEX 52022PC0496
Artificial Intelligence Act              CELEX 32024R1689; ELI /eli/reg/2024/1689/oj
```

The Ethics Guidelines record uses the official European Commission page and official PDF because it has no assumed CELEX value. Every source must record the actual retrieval and verification date. For every official file actually retrieved, add a document snapshot containing the retrieval date, media format and SHA-256 content hash; leave `archived_path` null unless an archival file is deliberately committed later. Do not fabricate a snapshot for an unarchived web page, and do not copy full copyrighted or official document text into JSON.

- [ ] **Step 4: Add policies, institutions, concepts, events and relationships**

Create the four concept records required by the proposal. Create only policies and relationships needed to place the seed documents into the 2018–2024 core pathway. For every relationship, set `basis` explicitly and provide official evidence or an English analytical rationale. Create events only for dates supported by an official source.

- [ ] **Step 5: Implement the pipeline and CLI**

`run_pipeline()` must validate first and stop without touching prior outputs on error. On success, build the database and export JSON into a temporary output directory, then atomically replace the requested `generated/` outputs. The CLI prints the two output paths and record counts; validation failure prints sorted issues and exits with status 1.

- [ ] **Step 6: Document the English data dictionary**

Create `docs/data-dictionary.md` with every canonical field, its type, whether it is required, its official or analytical provenance class, and allowed vocabulary where applicable. State that public repository visibility does not make drafts part of the reviewed corpus.

- [ ] **Step 7: Run the complete data test suite**

Run:

```powershell
python -m pytest -q
observatory-build --project-root . --timestamp 2026-09-03T00:00:00Z
```

Expected: all tests pass; both generated files exist; the public export contains at least six published documents and four concepts.

- [ ] **Step 8: Confirm deterministic logical output**

Run the build twice with the same timestamp and compare SHA-256 hashes of `generated/public-data.json`. Query both logical SQLite dumps ordered by table and primary key; the dumps must match even if the raw SQLite file bytes differ.

- [ ] **Step 9: Commit the database foundation**

```powershell
git add data src/observatory/pipeline.py tests/test_pipeline.py docs/data-dictionary.md .gitignore
git commit -m "feat: add verified EU AI policy seed corpus"
```

## Plan 1 Completion Gate

Do not begin the website plan until:

- `python -m pytest -q` passes.
- A clean checkout can generate both outputs with one command.
- The SQLite integrity check returns `ok`.
- At least six records have official provenance and intentional `published` status.
- No draft, pending-review or merely verified record appears in `public-data.json`.
