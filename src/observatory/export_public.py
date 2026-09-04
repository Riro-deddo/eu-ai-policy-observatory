"""Publication-safe, deterministic JSON export for the static Observatory website."""

import json
from pathlib import Path
import sqlite3
from typing import Any


CORE_TABLES = (
    "policies",
    "documents",
    "events",
    "concepts",
    "institutions",
    "relationships",
    "sources",
)
ENDPOINT_TABLES = {
    "policy": "policies",
    "document": "documents",
    "event": "events",
    "concept": "concepts",
    "institution": "institutions",
    "relationship": "relationships",
    "source": "sources",
}


def export_public(database_path: Path, output_path: Path, generated_at: str) -> Path:
    """Export only publishable records and their publishable static-page dependencies."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(Path(database_path))
    try:
        connection.row_factory = sqlite3.Row
        published = {
            table: _published_rows(connection, table) for table in CORE_TABLES
        }
        published_ids = {
            entity_type: {row["id"] for row in published[table]}
            for entity_type, table in ENDPOINT_TABLES.items()
        }
        documents, document_source_ids = _export_documents(connection, published["documents"])
        events, event_source_ids = _export_events(connection, published["events"], published_ids)
        exported_ids = {
            "policy": published_ids["policy"],
            "document": {document["id"] for document in documents},
            "event": {event["id"] for event in events},
            "concept": published_ids["concept"],
            "institution": published_ids["institution"],
            "source": published_ids["source"],
        }
        relationships, source_ids = _export_relationships(
            published["relationships"],
            exported_ids,
            document_source_ids | event_source_ids,
        )
        sources = [
            row for row in published["sources"] if row["id"] in source_ids
        ]
    finally:
        connection.close()

    payload = {
        "coverage": _coverage(documents, sources),
        "generated_at": generated_at,
        "policies": published["policies"],
        "documents": documents,
        "events": events,
        "concepts": published["concepts"],
        "institutions": published["institutions"],
        "relationships": relationships,
        "sources": sources,
    }
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def _published_rows(connection: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in connection.execute(
            f"SELECT * FROM {table} WHERE publication_status = 'published' ORDER BY id"
        )
    ]


def _export_documents(
    connection: sqlite3.Connection, documents: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], set[str]]:
    exported: list[dict[str, Any]] = []
    source_ids: set[str] = set()
    for document in documents:
        document_id = document["id"]
        policies = _document_dependencies(connection, "policy_documents", "policy_id", "policies", document_id)
        concepts = _document_dependencies(connection, "document_concepts", "concept_id", "concepts", document_id)
        institutions = _document_institutions(connection, document_id)
        sources = _document_dependencies(connection, "document_sources", "source_id", "sources", document_id)
        source_ids.update(source["id"] for source in sources)
        exported.append(
            {
                **document,
                "sector_tags": _string_values(
                    connection, "document_sector_tags", "sector_tag", document_id
                ),
                "provenance_tags": _string_values(
                    connection,
                    "document_provenance_tags",
                    "provenance_tag",
                    document_id,
                ),
                "procedure_references": _procedure_references(connection, document_id),
                "policies": policies,
                "concepts": concepts,
                "institutions": institutions,
                "corpus_assessment": _corpus_assessment(connection, document_id),
                "sources": sources,
            }
        )
    return exported, source_ids


def _string_values(
    connection: sqlite3.Connection,
    table: str,
    value_column: str,
    document_id: str,
) -> list[str]:
    query = f"SELECT {value_column} FROM {table} WHERE document_id = ? ORDER BY rowid"
    return [row[0] for row in connection.execute(query, (document_id,)).fetchall()]


def _procedure_references(
    connection: sqlite3.Connection, document_id: str
) -> list[str]:
    return [
        row["procedure_reference"]
        for row in connection.execute(
            "SELECT procedure_reference FROM document_procedure_references "
            "WHERE document_id = ? ORDER BY procedure_reference",
            (document_id,),
        )
    ]


def _coverage(
    documents: list[dict[str, Any]], sources: list[dict[str, Any]]
) -> dict[str, int | str | None]:
    document_years = [int(document["document_date"][:4]) for document in documents]
    verified_dates = [source["last_verified_at"][:10] for source in sources]
    principal_documents = sum(
        document["record_level"] == "principal" for document in documents
    )
    return {
        "from_year": min(document_years) if document_years else None,
        "to_year": max(document_years) if document_years else None,
        "last_verified_date": max(verified_dates) if verified_dates else None,
        "published_documents": len(documents),
        "principal_documents": principal_documents,
        "supporting_files_and_versions": len(documents) - principal_documents,
    }


def _document_dependencies(
    connection: sqlite3.Connection,
    junction_table: str,
    dependency_column: str,
    dependency_table: str,
    document_id: str,
) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in connection.execute(
            f"SELECT dependency.* FROM {junction_table} AS junction "
            f"JOIN {dependency_table} AS dependency "
            f"ON dependency.id = junction.{dependency_column} "
            "WHERE junction.document_id = ? "
            "AND dependency.publication_status = 'published' "
            "ORDER BY dependency.id",
            (document_id,),
        )
    ]


def _document_institutions(
    connection: sqlite3.Connection, document_id: str
) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in connection.execute(
            "SELECT institution.*, junction.role FROM document_institutions AS junction "
            "JOIN institutions AS institution ON institution.id = junction.institution_id "
            "WHERE junction.document_id = ? "
            "AND institution.publication_status = 'published' "
            "ORDER BY institution.id, junction.role",
            (document_id,),
        )
    ]


def _corpus_assessment(
    connection: sqlite3.Connection, document_id: str
) -> dict[str, Any] | None:
    row = connection.execute(
        "SELECT document_id, corpus_tier, policy_stage, inclusion_rationale, researcher_notes, "
        "review_status, reviewed_by, reviewed_at "
        "FROM corpus_assessments WHERE document_id = ?",
        (document_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def _export_events(
    connection: sqlite3.Connection,
    events: list[dict[str, Any]],
    published_ids: dict[str, set[str]],
) -> tuple[list[dict[str, Any]], set[str]]:
    exported = [
        event
        for event in events
        if event["policy_id"] in published_ids["policy"]
        and event["source_id"] in published_ids["source"]
        and (
            event["document_id"] is None
            or event["document_id"] in published_ids["document"]
        )
    ]
    return exported, {event["source_id"] for event in exported}


def _export_relationships(
    relationships: list[dict[str, Any]],
    exported_ids: dict[str, set[str]],
    base_source_ids: set[str],
) -> tuple[list[dict[str, Any]], set[str]]:
    exported = relationships
    while True:
        source_ids = _relationship_source_ids(base_source_ids, exported)
        visible_ids = {
            **exported_ids,
            "source": source_ids & exported_ids["source"],
            "relationship": {relationship["id"] for relationship in exported},
        }
        filtered = [
            relationship
            for relationship in exported
            if _relationship_dependencies_are_exported(relationship, visible_ids)
        ]
        if len(filtered) == len(exported):
            return filtered, visible_ids["source"]
        exported = filtered


def _relationship_source_ids(
    base_source_ids: set[str], relationships: list[dict[str, Any]]
) -> set[str]:
    source_ids = set(base_source_ids)
    for relationship in relationships:
        evidence_source_id = relationship["evidence_source_id"]
        if evidence_source_id is not None:
            source_ids.add(evidence_source_id)
        for side in ("source", "target"):
            if relationship[f"{side}_entity_type"] == "source":
                source_ids.add(relationship[f"{side}_entity_id"])
    return source_ids


def _relationship_dependencies_are_exported(
    relationship: dict[str, Any], exported_ids: dict[str, set[str]]
) -> bool:
    evidence_source_id = relationship["evidence_source_id"]
    return evidence_source_id in exported_ids["source"] and all(
        relationship[f"{side}_entity_id"]
        in exported_ids.get(relationship[f"{side}_entity_type"], set())
        for side in ("source", "target")
    )
