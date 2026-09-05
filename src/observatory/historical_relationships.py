"""Relationship checks for the inactive historical readiness contract."""

from __future__ import annotations

from collections import defaultdict
from typing import Mapping, Sequence

from observatory.io import LoadedRecord
from observatory.types import ValidationIssue
from observatory.validate import _is_official_source


_VERSION_RELATIONSHIPS = {"version_of", "revises"}
_ATTACHMENT_PARENT_RELATIONSHIPS = {"annex_to", "part_of"}
_ENTITY_DIRECTORIES = {
    "policy": "policies",
    "document": "documents",
    "event": "events",
    "concept": "concepts",
    "institution": "institutions",
    "relationship": "relationships",
    "source": "sources",
}


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

    endpoints: dict[tuple[str, str], list[LoadedRecord]] = defaultdict(list)
    for entity_type, directory in _ENTITY_DIRECTORIES.items():
        for record in records.get(directory, ()):
            data = record.data
            if not isinstance(data, Mapping) or data.get("publication_status") != "published":
                continue
            record_id = data.get("id")
            if data.get("entity_type") == entity_type and isinstance(record_id, str):
                endpoints[(entity_type, record_id)].append(record)

    outgoing: dict[str, list[LoadedRecord]] = defaultdict(list)
    incoming: dict[str, list[LoadedRecord]] = defaultdict(list)
    eligible: dict[str, bool] = {}
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
        endpoint_keys: list[tuple[str, str] | None] = []
        endpoints_valid = True
        for side in ("source", "target"):
            entity_type, entity_id = data.get(f"{side}_entity_type"), data.get(f"{side}_entity_id")
            if not isinstance(entity_type, str) or entity_type not in _ENTITY_DIRECTORIES:
                issues.append(_issue(relationship, f"{side}_entity_type", "Relationship endpoint must declare a canonical entity type."))
                endpoint_keys.append(None)
                endpoints_valid = False
                continue
            if not isinstance(entity_id, str) or len(endpoints.get((entity_type, entity_id), ())) != 1:
                issues.append(_issue(relationship, f"{side}_entity_id", "Relationship endpoint must resolve uniquely to a published record of its declared type."))
                endpoint_keys.append(None)
                endpoints_valid = False
                continue
            endpoint_keys.append((entity_type, entity_id))
        if len(endpoint_keys) == 2 and endpoint_keys[0] is not None and endpoint_keys[0] == endpoint_keys[1]:
            issues.append(_issue(relationship, "target_entity_id", "Relationship endpoints must refer to different records."))
            endpoints_valid = False
        evidence_valid = _official_evidence(data, sources)
        if not evidence_valid:
            issues.append(_issue(relationship, "evidence_source_id", "Published relationships require one published official HTTPS evidence source."))
        basis = data.get("basis")
        rationale_valid = basis == "official"
        if basis == "analytical":
            rationale = data.get("rationale")
            rationale_valid = isinstance(rationale, str) and bool(rationale.strip())
            if not rationale_valid:
                issues.append(_issue(relationship, "rationale", "Analytical relationships require a nonblank rationale."))
        elif basis != "official":
            issues.append(_issue(relationship, "basis", "Published relationships require an official or analytical basis."))
        eligible[relationship.path.as_posix()] = endpoints_valid and evidence_valid and rationale_valid

    def valid_edge(relationship: LoadedRecord, document_id: str, *, incoming_edge: bool) -> bool:
        data = relationship.data
        other_id = data.get("source_entity_id" if incoming_edge else "target_entity_id")
        other_type = data.get("source_entity_type" if incoming_edge else "target_entity_type")
        return (
            eligible.get(relationship.path.as_posix(), False)
            and isinstance(other_id, str)
            and other_type == "document"
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
