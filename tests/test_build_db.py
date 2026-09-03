import copy
import sqlite3
from pathlib import Path

import pytest

from observatory.build_db import build_database
from observatory.io import LoadedRecord, load_records


DATA_ROOT = Path("tests/fixtures/valid/data")
SCHEMA_PATH = Path("schema/database.sql")


def test_build_database_normalises_document_links(tmp_path):
    output = tmp_path / "observatory.sqlite"
    build_database(
        load_records(DATA_ROOT),
        SCHEMA_PATH,
        output,
    )
    with sqlite3.connect(output) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert connection.execute("SELECT COUNT(*) FROM documents").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM policy_documents").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM document_concepts").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM document_sources").fetchone() == (1,)


def test_schema_rejects_an_impossible_iso_calendar_date():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO documents "
            "(id, publication_status, created_at, updated_at, slug, official_title, short_title, "
            "document_type, publication_date, legal_status, language) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "invalid-date-document",
                "draft",
                "2026-09-03T12:00:00Z",
                "2026-09-03T12:00:00Z",
                "invalid-date-document",
                "Invalid date document",
                "Invalid date",
                "communication",
                "2026-02-29",
                "non_binding",
                "en",
            ),
        )


def test_build_database_normalises_assessment_institution_and_snapshot_rows(tmp_path):
    records = load_records(DATA_ROOT)
    records["documents"][0].data["snapshots"] = [
        {
            "id": "example-document-html-snapshot",
            "source_id": "example-source",
            "retrieved_at": "2026-09-03T12:00:00Z",
            "format": "text/html",
            "content_hash": "example-content-hash",
            "archived_path": "snapshots/example-document.html",
        }
    ]
    output = tmp_path / "observatory.sqlite"

    build_database(records, SCHEMA_PATH, output)

    with sqlite3.connect(output) as connection:
        assert connection.execute(
            "SELECT corpus_tier, policy_stage, review_status FROM corpus_assessments"
        ).fetchone() == ("core", "proposal", "verified")
        assert connection.execute(
            "SELECT institution_id, role FROM document_institutions"
        ).fetchone() == ("european-commission", "author")
        assert connection.execute(
            "SELECT source_id, format, archived_path FROM document_snapshots"
        ).fetchone() == (
            "example-source",
            "text/html",
            "snapshots/example-document.html",
        )


def test_build_database_rejects_missing_typed_relationship_endpoint(tmp_path):
    records = load_records(DATA_ROOT)
    records["relationships"].append(
        LoadedRecord(
            {
                "id": "missing-endpoint-relationship",
                "entity_type": "relationship",
                "publication_status": "draft",
                "created_at": "2026-09-03T12:00:00Z",
                "updated_at": "2026-09-03T12:00:00Z",
                "source_entity_type": "document",
                "source_entity_id": "missing-document",
                "target_entity_type": "policy",
                "target_entity_id": "example-policy",
                "relationship_type": "related_to",
                "basis": "official",
                "rationale": None,
                "evidence_source_id": "example-source",
                "verification_status": "verified",
            },
            Path("relationships/missing-endpoint-relationship.json"),
        )
    )
    output = tmp_path / "observatory.sqlite"

    with pytest.raises(ValueError, match="missing 'document' endpoint 'missing-document'"):
        build_database(records, SCHEMA_PATH, output)

    assert not output.exists()


def test_build_database_rejects_foreign_keys_without_replacing_prior_output(tmp_path):
    output = tmp_path / "observatory.sqlite"
    build_database(load_records(DATA_ROOT), SCHEMA_PATH, output)
    records = load_records(DATA_ROOT)
    records["documents"][0].data["policy_ids"] = ["missing-policy"]

    with pytest.raises(sqlite3.IntegrityError):
        build_database(records, SCHEMA_PATH, output)

    with sqlite3.connect(output) as connection:
        assert connection.execute("SELECT COUNT(*) FROM documents").fetchone() == (1,)
    assert list(tmp_path.glob(".observatory-*.sqlite")) == []


def test_build_database_has_deterministic_logical_insertion_order(tmp_path):
    first_records = load_records(DATA_ROOT)
    second_policy = copy.deepcopy(first_records["policies"][0])
    second_policy.data["id"] = "second-policy"
    second_policy.data["name"] = "Second policy"
    second_policy.data["short_name"] = "Second"
    second_document = copy.deepcopy(first_records["documents"][0])
    second_document.data["id"] = "second-document"
    second_document.data["slug"] = "second-document"
    second_document.data["official_title"] = "Second document"
    second_document.data["short_title"] = "Second"
    second_document.data["policy_ids"] = ["second-policy"]
    first_records["policies"].append(second_policy)
    first_records["documents"].append(second_document)
    reordered_records = copy.deepcopy(first_records)
    for records in reordered_records.values():
        records.reverse()
    first_output = tmp_path / "first.sqlite"
    second_output = tmp_path / "second.sqlite"

    build_database(first_records, SCHEMA_PATH, first_output)
    build_database(reordered_records, SCHEMA_PATH, second_output)

    assert _logical_rows(first_output) == _logical_rows(second_output)


def test_build_database_rejects_an_invalid_event_date(tmp_path):
    records = load_records(DATA_ROOT)
    records["events"].append(
        LoadedRecord(
            {
                "id": "invalid-date-event",
                "entity_type": "event",
                "publication_status": "draft",
                "created_at": "2026-09-03T12:00:00Z",
                "updated_at": "2026-09-03T12:00:00Z",
                "event_type": "proposal",
                "event_date": "2026-02-29",
                "title": "Invalid date event",
                "description": "An event with an invalid calendar date.",
                "policy_id": "example-policy",
                "document_id": "example-document",
                "source_id": "example-source",
            },
            Path("events/invalid-date-event.json"),
        )
    )

    with pytest.raises(sqlite3.IntegrityError):
        build_database(records, SCHEMA_PATH, tmp_path / "observatory.sqlite")


def _logical_rows(database_path):
    with sqlite3.connect(database_path) as connection:
        tables = [
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            )
        ]
        return {
            table: connection.execute(f"SELECT * FROM {table}").fetchall()
            for table in tables
        }
