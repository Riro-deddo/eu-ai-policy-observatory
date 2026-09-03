import json
from pathlib import Path
import shutil

import pytest

from observatory.validate import RecordValidationError, assert_valid, validate_records


SCHEMA = Path("schema/record.schema.json")
VOCAB = Path("schema/controlled-vocabularies.json")
VALID_DATA = Path("tests/fixtures/valid/data")


def _copy_valid_data(tmp_path: Path) -> Path:
    data_root = tmp_path / "data"
    shutil.copytree(VALID_DATA, data_root)
    return data_root


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


def test_cross_record_issues_cover_canonical_integrity_rules():
    issues = validate_records(Path("tests/fixtures/invalid/data"), SCHEMA, VOCAB)
    codes = {issue.code for issue in issues}
    assert {
        "duplicate_celex",
        "duplicate_eli",
        "filename_mismatch",
        "directory_mismatch",
        "missing_reference",
        "missing_evidence",
        "official_evidence",
        "timestamp_order",
    } <= codes


def test_issues_are_sorted_by_path_field_and_code():
    issues = validate_records(Path("tests/fixtures/invalid/data"), SCHEMA, VOCAB)
    assert issues == sorted(issues, key=lambda issue: (issue.record_path, issue.field, issue.code))


def test_assert_valid_raises_sorted_actionable_messages():
    with pytest.raises(RecordValidationError) as error:
        assert_valid(Path("tests/fixtures/invalid/data"), SCHEMA, VOCAB)

    lines = str(error.value).splitlines()
    assert lines == sorted(lines)
    assert "[duplicate_id]" in str(error.value)


def test_malformed_json_is_a_sorted_issue_without_skipping_other_records(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    (data_root / "documents" / "broken.json").write_text("{", encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(
        issue.code == "json_syntax" and issue.record_path == "documents/broken.json"
        for issue in issues
    )
    assert not any(issue.record_path == "documents/example-document.json" for issue in issues)
    assert issues == sorted(issues, key=lambda issue: (issue.record_path, issue.field, issue.code))


def test_mixed_naive_and_aware_timestamps_report_schema_issue_without_crashing(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["updated_at"] = "2026-09-03T12:00:00"
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(
        issue.code == "schema" and issue.record_path == "documents/example-document.json"
        for issue in issues
    )


def test_duplicate_document_slugs_are_reported(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "second-document.json"
    document = json.loads(
        (data_root / "documents" / "example-document.json").read_text(encoding="utf-8")
    )
    document["id"] = "second-document"
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(issue.code == "duplicate_slug" for issue in issues)


def test_validation_rejects_a_document_without_a_slug(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    del document["slug"]
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(
        issue.code == "schema" and issue.record_path == "documents/example-document.json"
        for issue in issues
    )
