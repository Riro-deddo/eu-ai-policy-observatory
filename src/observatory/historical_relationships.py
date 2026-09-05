"""Relationship checks for the inactive historical readiness contract."""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping, Sequence

from observatory.io import LoadedRecord
from observatory.types import ValidationIssue
from observatory.validate import _is_official_source


_VERSION_RELATIONSHIPS = {"version_of", "revises"}
_ATTACHMENT_PARENT_RELATIONSHIPS = {"annex_to", "part_of"}


def _issue(record: LoadedRecord, field: str, message: str) -> ValidationIssue:
    return ValidationIssue(
        code="historical_relationship",
        record_path=record.path.as_posix(),
        field=field,
        message=message,
    )


def _official_evidence(
    relationship: Mapping[str, object],
    sources: Mapping[str, Sequence[LoadedRecord]],
) -> bool:
    evidence_id = relationship.get("evidence_source_id")
    matches = sources.get(evidence_id, ()) if isinstance(evidence_id, str) else ()
    return (
        len(matches) == 1
        and matches[0].data.get("publication_status") == "published"
        and _is_official_source(matches[0].data)
    )


def validate_historical_relationships(
    records: Mapping[str, Sequence[LoadedRecord]],
    documents: Sequence[LoadedRecord],
    sources: Mapping[str, Sequence[LoadedRecord]],
) -> list[ValidationIssue]:
    """Validate published evidence edges and each document's lineage shape."""
    issues: list[ValidationIssue] = []
    documents_by_id: dict[str, list[LoadedRecord]] = defaultdict(list)
    for document in documents:
        document_id = document.data.get("id")
        if isinstance(document_id, str):
            documents_by_id[document_id].append(document)

    outgoing: dict[str, list[LoadedRecord]] = defaultdict(list)
    incoming: dict[str, list[LoadedRecord]] = defaultdict(list)
    for relationship in records.get("relationships", ()):
        if not isinstance(relationship.data, Mapping):
            continue
        data = relationship.data
        if data.get("publication_status") != "published":
            continue
        source_id, target_id = data.get("source_entity_id"), data.get("target_entity_id")
        if data.get("source_entity_type") == "document" and isinstance(source_id, str):
            outgoing[source_id].append(relationship)
        if data.get("target_entity_type") == "document" and isinstance(target_id, str):
            incoming[target_id].append(relationship)
        if not _official_evidence(data, sources):
            issues.append(_issue(relationship, "evidence_source_id", "Published relationships require one published official HTTPS evidence source."))
        if data.get("basis") == "analytical":
            rationale = data.get("rationale")
            if not isinstance(rationale, str) or not rationale.strip():
                issues.append(_issue(relationship, "rationale", "Analytical relationships require a nonblank rationale."))

    def valid_edge(relationship: LoadedRecord, document_id: str, *, incoming_edge: bool) -> bool:
        data = relationship.data
        other_id = data.get("source_entity_id" if incoming_edge else "target_entity_id")
        return (
            isinstance(other_id, str)
            and other_id != document_id
            and other_id in documents_by_id
            and _official_evidence(data, sources)
        )

    for document in documents:
        data = document.data
        level, document_id = data.get("record_level"), data.get("id")
        if not isinstance(document_id, str) or level not in {"version", "attachment"}:
            continue
        valid = False
        if level == "version":
            candidates = [
                (edge, False)
                for edge in outgoing.get(document_id, ())
                if edge.data.get("relationship_type") in _VERSION_RELATIONSHIPS
            ] + [
                (edge, True)
                for edge in incoming.get(document_id, ())
                if edge.data.get("relationship_type") in _VERSION_RELATIONSHIPS
            ]
            valid = any(
                valid_edge(edge, document_id, incoming_edge=is_incoming)
                and all(peer.data.get("record_level") != "attachment" for peer in documents_by_id[edge.data.get("source_entity_id" if is_incoming else "target_entity_id")])
                for edge, is_incoming in candidates
            )
        else:
            for edge in outgoing.get(document_id, ()):
                relation_type = edge.data.get("relationship_type")
                if not valid_edge(edge, document_id, incoming_edge=False):
                    continue
                target_id = edge.data.get("target_entity_id")
                if relation_type in _ATTACHMENT_PARENT_RELATIONSHIPS:
                    valid = True
                elif relation_type in _VERSION_RELATIONSHIPS and all(
                    peer.data.get("record_level") == "attachment"
                    for peer in documents_by_id[target_id]
                ):
                    valid = True
        if not valid:
            issues.append(_issue(document, "record_level", "Published version or attachment lacks a valid evidenced lineage relationship."))
    return issues
