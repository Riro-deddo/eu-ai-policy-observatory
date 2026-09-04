import json
from pathlib import Path
import shutil
import hashlib

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


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("record_level", "unsupported_level"),
        ("version_status", "unsupported_status"),
    ],
)
def test_document_version_metadata_is_checked_against_controlled_vocabularies(
    tmp_path, field, value
):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document[field] = value
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(
        issue.code == "vocabulary"
        and issue.field == field
        and issue.record_path == "documents/example-document.json"
        for issue in issues
    )


def test_duplicate_document_identity_uses_normalised_version_and_institution_ids(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    first_path = data_root / "documents" / "example-document.json"
    first = json.loads(first_path.read_text(encoding="utf-8"))
    first["official_reference"] = "COM(2026) 1 final"
    first["version_label"] = "Final"
    first_path.write_text(json.dumps(first), encoding="utf-8")

    second = dict(first)
    second["id"] = "second-document"
    second["slug"] = "second-document"
    second["version_label"] = "  FINAL  "
    (data_root / "documents" / "second-document.json").write_text(
        json.dumps(second), encoding="utf-8"
    )

    issues = validate_records(data_root, SCHEMA, VOCAB)

    identity_issues = [issue for issue in issues if issue.code == "duplicate_document_identity"]
    assert {issue.record_path for issue in identity_issues} == {
        "documents/example-document.json",
        "documents/second-document.json",
    }
    assert all("COM(2026) 1 final" not in issue.message for issue in identity_issues)


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


def test_schema_errors_name_missing_leaf_without_leaking_researcher_notes(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    del document["slug"]
    document["corpus_assessment"]["researcher_notes"] = ["PRIVATE-RESEARCH-SENTINEL"]
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)
    messages = str(RecordValidationError(issues))

    assert any(issue.field == "slug" for issue in issues)
    assert not any(issue.code == "schema" and issue.field == "$" for issue in issues)
    assert "PRIVATE-RESEARCH-SENTINEL" not in messages
    assert "oneOf" not in messages


def test_unexpected_properties_are_rejected_without_leaking_values(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["unexpected_private_property"] = "PRIVATE-RESEARCH-SENTINEL"
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)
    messages = str(RecordValidationError(issues))

    assert any(
        issue.code == "schema"
        and issue.field == "unexpected_private_property"
        and "unsupported property" in issue.message
        for issue in issues
    )
    assert "PRIVATE-RESEARCH-SENTINEL" not in messages


def test_non_string_entity_type_is_reported_without_crashing(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["entity_type"] = ["document"]
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(issue.code == "schema" for issue in issues)


def test_snapshot_ids_are_unique_within_and_across_documents(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    snapshot = _snapshot("shared-snapshot", None)
    document["snapshots"] = [snapshot, snapshot]
    document_path.write_text(json.dumps(document), encoding="utf-8")

    cross_document = json.loads(document_path.read_text(encoding="utf-8"))
    cross_document["id"] = "second-document"
    cross_document["slug"] = "second-document"
    cross_document["snapshots"] = [_snapshot("shared-snapshot", None)]
    (data_root / "documents" / "second-document.json").write_text(
        json.dumps(cross_document), encoding="utf-8"
    )

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert sum(issue.code == "duplicate_snapshot_id" for issue in issues) == 3


@pytest.mark.parametrize(
    ("directory", "filename", "field", "value"),
    [
        ("sources", "example-source.json", "url", "file:///private.txt"),
        ("sources", "example-source.json", "url", "javascript:alert(1)"),
        ("institutions", "european-commission.json", "official_url", "file:///private.txt"),
        ("institutions", "european-commission.json", "official_url", "javascript:alert(1)"),
    ],
)
def test_source_and_institution_urls_require_http_or_https(tmp_path, directory, filename, field, value):
    data_root = _copy_valid_data(tmp_path)
    record_path = data_root / directory / filename
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record[field] = value
    record_path.write_text(json.dumps(record), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(issue.field == field and issue.code == "schema" for issue in issues)


@pytest.mark.parametrize(
    ("archive_path", "content_hash", "expected_code"),
    [
        ("C:\\private\\snapshot.txt", "a" * 64, "invalid_snapshot_archive"),
        ("/private/snapshot.txt", "a" * 64, "invalid_snapshot_archive"),
        ("../private/snapshot.txt", "a" * 64, "invalid_snapshot_archive"),
        ("https://example.invalid/snapshot.txt", "a" * 64, "invalid_snapshot_archive"),
        ("snapshots/missing.txt", "a" * 64, "invalid_snapshot_archive"),
        ("snapshots/valid.txt", "b" * 64, "snapshot_hash_mismatch"),
        (None, "not-a-sha256", "schema"),
    ],
)
def test_snapshots_require_safe_archives_and_sha256(tmp_path, archive_path, content_hash, expected_code):
    data_root = _copy_valid_data(tmp_path)
    (tmp_path / "snapshots").mkdir()
    (tmp_path / "snapshots" / "valid.txt").write_text("snapshot", encoding="utf-8")
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["snapshots"] = [_snapshot("snapshot-one", archive_path, content_hash)]
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_records(data_root, SCHEMA, VOCAB)

    assert any(issue.code == expected_code for issue in issues)


def test_snapshot_with_repository_relative_archive_and_matching_hash_is_valid(tmp_path):
    data_root = _copy_valid_data(tmp_path)
    archive = tmp_path / "snapshots" / "valid.txt"
    archive.parent.mkdir()
    archive.write_text("snapshot", encoding="utf-8")
    document_path = data_root / "documents" / "example-document.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["snapshots"] = [
        _snapshot("snapshot-one", "snapshots/valid.txt", hashlib.sha256(archive.read_bytes()).hexdigest())
    ]
    document_path.write_text(json.dumps(document), encoding="utf-8")

    assert validate_records(data_root, SCHEMA, VOCAB) == []


def _snapshot(identifier, archived_path, content_hash="a" * 64):
    return {
        "id": identifier,
        "source_id": "example-source",
        "retrieved_at": "2026-09-03T12:00:00Z",
        "format": "text/plain",
        "content_hash": content_hash,
        "archived_path": archived_path,
    }
