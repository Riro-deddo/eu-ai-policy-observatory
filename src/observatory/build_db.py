"""Transactional generation of the Observatory's normalised SQLite database."""

import os
from pathlib import Path
import sqlite3
import tempfile
from typing import Mapping

from observatory.io import LoadedRecord


def build_database(
    records: dict[str, list[LoadedRecord]], schema_path: Path, output_path: Path
) -> Path:
    """Build a verified SQLite database and atomically publish it at output_path."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = _temporary_database_path(destination)
    connection: sqlite3.Connection | None = None

    try:
        _validate_relationship_endpoints(records)
        connection = sqlite3.connect(temporary_path)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(Path(schema_path).read_text(encoding="utf-8"))
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN")
        _insert_records(connection, records)
        _check_integrity(connection)
        connection.commit()
        connection.close()
        connection = None
        os.replace(temporary_path, destination)
        return destination
    except Exception:
        if connection is not None:
            connection.rollback()
            connection.close()
        if temporary_path.exists():
            temporary_path.unlink()
        raise


def _temporary_database_path(destination: Path) -> Path:
    with tempfile.NamedTemporaryFile(
        prefix=f".{destination.stem}-", suffix=".sqlite", dir=destination.parent, delete=False
    ) as temporary_file:
        return Path(temporary_file.name)


def _validate_relationship_endpoints(records: Mapping[str, list[LoadedRecord]]) -> None:
    ids_by_type = {
        entity_type: {
            _text(record.data, "id") for record in entries
        }
        for entity_type, entries in (
            ("policy", records.get("policies", [])),
            ("document", records.get("documents", [])),
            ("event", records.get("events", [])),
            ("concept", records.get("concepts", [])),
            ("institution", records.get("institutions", [])),
            ("relationship", records.get("relationships", [])),
            ("source", records.get("sources", [])),
        )
    }
    for record in _ordered_records(records, "relationships"):
        for side in ("source", "target"):
            entity_type = _text(record.data, f"{side}_entity_type")
            entity_id = _text(record.data, f"{side}_entity_id")
            if entity_id not in ids_by_type.get(entity_type, set()):
                raise ValueError(
                    f"Relationship {_text(record.data, 'id')!r} references missing "
                    f"{entity_type!r} endpoint {entity_id!r}."
                )


def _insert_records(
    connection: sqlite3.Connection, records: Mapping[str, list[LoadedRecord]]
) -> None:
    _insert_policies(connection, _ordered_records(records, "policies"))
    _insert_concepts(connection, _ordered_records(records, "concepts"))
    _insert_institutions(connection, _ordered_records(records, "institutions"))
    _insert_sources(connection, _ordered_records(records, "sources"))
    documents = _ordered_records(records, "documents")
    _insert_documents(connection, documents)
    _insert_events(connection, _ordered_records(records, "events"))
    _insert_relationships(connection, _ordered_records(records, "relationships"))
    _insert_document_supporting_rows(connection, documents)


def _insert_policies(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "policies",
        ("id", "publication_status", "created_at", "updated_at", "name", "short_name", "summary", "policy_family", "policy_status", "scope_note"),
        records,
    )


def _insert_concepts(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "concepts",
        ("id", "publication_status", "created_at", "updated_at", "name", "definition", "research_scope", "eurovoc_uri", "notes"),
        records,
    )


def _insert_institutions(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "institutions",
        ("id", "publication_status", "created_at", "updated_at", "official_name", "short_name", "institution_type", "official_url"),
        records,
    )


def _insert_sources(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "sources",
        ("id", "publication_status", "created_at", "updated_at", "source_type", "url", "publisher", "retrieved_at", "last_verified_at", "verification_note"),
        records,
    )


def _insert_documents(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "documents",
        ("id", "publication_status", "created_at", "updated_at", "slug", "official_title", "short_title", "document_type", "publication_date", "legal_status", "celex", "eli", "language", "official_summary"),
        records,
    )


def _insert_events(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "events",
        ("id", "publication_status", "created_at", "updated_at", "event_type", "event_date", "title", "description", "policy_id", "document_id", "source_id"),
        records,
    )


def _insert_relationships(connection: sqlite3.Connection, records: list[LoadedRecord]) -> None:
    _insert_entity_rows(
        connection,
        "relationships",
        ("id", "publication_status", "created_at", "updated_at", "source_entity_type", "source_entity_id", "target_entity_type", "target_entity_id", "relationship_type", "basis", "rationale", "evidence_source_id", "verification_status"),
        records,
    )


def _insert_entity_rows(
    connection: sqlite3.Connection,
    table: str,
    fields: tuple[str, ...],
    records: list[LoadedRecord],
) -> None:
    placeholders = ", ".join("?" for _ in fields)
    connection.executemany(
        f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})",
        [tuple(record.data.get(field) for field in fields) for record in records],
    )


def _insert_document_supporting_rows(
    connection: sqlite3.Connection, documents: list[LoadedRecord]
) -> None:
    for record in documents:
        data = record.data
        document_id = _text(data, "id")
        assessment = _mapping(data, "corpus_assessment")
        connection.execute(
            "INSERT INTO corpus_assessments "
            "(document_id, corpus_tier, policy_stage, inclusion_rationale, researcher_notes, "
            "review_status, reviewed_by, reviewed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (document_id, *(assessment.get(field) for field in (
                "corpus_tier", "policy_stage", "inclusion_rationale", "researcher_notes",
                "review_status", "reviewed_by", "reviewed_at",
            ))),
        )
        for role in _mappings(data, "institution_roles"):
            connection.execute(
                "INSERT INTO document_institutions (document_id, institution_id, role) VALUES (?, ?, ?)",
                (document_id, role.get("institution_id"), role.get("role")),
            )
        for snapshot in _mappings(data, "snapshots"):
            connection.execute(
                "INSERT INTO document_snapshots "
                "(id, document_id, source_id, retrieved_at, format, content_hash, archived_path) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (snapshot.get("id"), document_id, snapshot.get("source_id"), snapshot.get("retrieved_at"), snapshot.get("format"), snapshot.get("content_hash"), snapshot.get("archived_path")),
            )
        _insert_junction_rows(connection, "policy_documents", "policy_id", data, "policy_ids", document_id)
        _insert_junction_rows(connection, "document_concepts", "concept_id", data, "concept_ids", document_id)
        _insert_junction_rows(connection, "document_sources", "source_id", data, "source_ids", document_id)


def _insert_junction_rows(
    connection: sqlite3.Connection,
    table: str,
    foreign_key: str,
    data: Mapping[str, object],
    source_field: str,
    document_id: str,
) -> None:
    values = data.get(source_field)
    if not isinstance(values, list):
        raise ValueError(f"Document {document_id!r} has no valid {source_field!r} list.")
    connection.executemany(
        f"INSERT INTO {table} (document_id, {foreign_key}) VALUES (?, ?)",
        [(document_id, value) for value in values],
    )


def _check_integrity(connection: sqlite3.Connection) -> None:
    foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
    if foreign_key_errors:
        raise ValueError(f"Foreign-key check failed: {foreign_key_errors!r}")
    integrity = connection.execute("PRAGMA integrity_check").fetchone()
    if integrity != ("ok",):
        raise ValueError(f"Integrity check failed: {integrity!r}")


def _ordered_records(records: Mapping[str, list[LoadedRecord]], directory: str) -> list[LoadedRecord]:
    return sorted(records.get(directory, []), key=lambda record: _text(record.data, "id"))


def _text(data: Mapping[str, object], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str):
        raise ValueError(f"Expected string {field!r} in a validated record.")
    return value


def _mapping(data: Mapping[str, object], field: str) -> Mapping[str, object]:
    value = data.get(field)
    if not isinstance(value, Mapping):
        raise ValueError(f"Expected object {field!r} in a validated record.")
    return value


def _mappings(data: Mapping[str, object], field: str) -> list[Mapping[str, object]]:
    value = data.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, Mapping) for item in value):
        raise ValueError(f"Expected object list {field!r} in a validated record.")
    return value
