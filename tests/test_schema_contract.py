import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

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


def test_schema_requires_a_document_slug_for_stable_public_routes():
    schema_path = Path(__file__).parents[1] / "schema" / "record.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    record_path = Path("tests/fixtures/valid/data/documents/example-document.json")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    del record["slug"]

    errors = list(Draft202012Validator(schema).iter_errors(record))

    assert any(
        error.validator == "required" and "slug" in error.message
        for error in _validation_errors(errors[0])
    )


def test_document_fixture_declares_version_aware_canonical_metadata():
    document_path = Path("tests/fixtures/valid/data/documents/example-document.json")
    document = json.loads(document_path.read_text(encoding="utf-8"))

    assert document["record_level"] in {"principal", "supporting", "version", "attachment"}
    assert document["version_status"] in {
        "draft",
        "revised",
        "final",
        "consolidated",
        "not_applicable",
    }
    assert document["document_date"] == "2026-09-03"
    assert document["procedure_references"] == ["2021/0106(COD)"]


@pytest.mark.parametrize(
    ("field", "value", "validator"),
    [
        ("procedure_references", ["2021/0106(COD)", "2021/0106(COD)"], "uniqueItems"),
        ("record_level", "unsupported_level", "enum"),
        ("version_status", "unsupported_status", "enum"),
        ("document_type", "unsupported_type", "enum"),
    ],
)
def test_document_schema_rejects_unknown_or_duplicate_version_metadata(field, value, validator):
    schema_path = Path(__file__).parents[1] / "schema" / "record.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    record_path = Path("tests/fixtures/valid/data/documents/example-document.json")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record[field] = value

    errors = list(Draft202012Validator(schema).iter_errors(record))

    assert any(error.validator == validator for error in _validation_errors(errors[0]))


def test_document_schema_requires_document_date():
    schema_path = Path(__file__).parents[1] / "schema" / "record.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    record_path = Path("tests/fixtures/valid/data/documents/example-document.json")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    del record["document_date"]

    errors = list(Draft202012Validator(schema).iter_errors(record))

    assert any(
        error.validator == "required" and "document_date" in error.message
        for error in _validation_errors(errors[0])
    )


def _validation_errors(error):
    yield error
    for context_error in error.context:
        yield from _validation_errors(context_error)


@pytest.mark.parametrize(
    ("record", "date_field"),
    [
        (
            {
                "id": "example-document",
                "entity_type": "document",
                "publication_status": "draft",
                "created_at": "2026-09-03T12:00:00Z",
                "updated_at": "2026-09-03T12:00:00Z",
                "official_title": "Example document",
                "short_title": "Example",
                "document_type": "communication",
                "publication_date": "2026-02-28",
                "legal_status": "non_binding",
                "language": "en",
                "institution_roles": [],
                "policy_ids": [],
                "concept_ids": [],
                "source_ids": [],
                "corpus_assessment": {
                    "corpus_tier": "core",
                    "policy_stage": "proposal",
                    "inclusion_rationale": "Example rationale.",
                    "researcher_notes": "Example note.",
                    "review_status": "pending",
                    "reviewed_by": "Researcher",
                    "reviewed_at": "2026-09-03T12:00:00Z",
                },
            },
            "publication_date",
        ),
        (
            {
                "id": "example-event",
                "entity_type": "event",
                "publication_status": "draft",
                "created_at": "2026-09-03T12:00:00Z",
                "updated_at": "2026-09-03T12:00:00Z",
                "event_type": "proposal",
                "event_date": "2026-02-28",
                "title": "Example event",
                "description": "Example description.",
                "policy_id": "example-policy",
                "document_id": None,
                "source_id": "example-source",
            },
            "event_date",
        ),
    ],
)
def test_schema_rejects_invalid_iso_calendar_dates(record, date_field):
    schema_path = Path(__file__).parents[1] / "schema" / "record.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    record[date_field] = "2026-02-29"

    errors = list(Draft202012Validator(schema).iter_errors(record))

    assert errors
    assert any(error.validator == "pattern" for error in _validation_errors(errors[0]))
