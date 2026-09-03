from pathlib import Path

import pytest

from observatory.validate import RecordValidationError, assert_valid, validate_records


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
