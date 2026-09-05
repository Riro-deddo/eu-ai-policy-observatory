"""Compatibility publication gate for evidence-backed historical metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

from observatory.historical_readiness import validate_historical_readiness
from observatory.io import LoadedRecord
from observatory.types import ValidationIssue


EXTENSION_FIELDS = frozenset(
    {
        "historical_review_status",
        "temporal_collection",
        "relevance_class",
        "document_date_kind",
        "date_evidence",
        "classification_evidence",
        "bibliographic_authors",
        "additional_dates",
    }
)
OPTIONAL_EXTENSION_FIELDS = frozenset({"legal_status_evidence"})


def _issue(record: LoadedRecord, field: str, message: str) -> ValidationIssue:
    return ValidationIssue("historical_publication", record.path.as_posix(), field, message)


def validate_historical_publication(
    records: Mapping[str, Sequence[LoadedRecord]],
    schema_root: Path,
    publication_cutoff: str,
    baseline_path: Path,
) -> list[ValidationIssue]:
    """Allow frozen legacy routes or require a complete evidence extension."""
    baseline = json.loads(Path(baseline_path).read_text(encoding="utf-8"))
    legacy = {
        row["id"]: row["slug"]
        for row in baseline.get("documents", ())
        if isinstance(row, Mapping)
        and isinstance(row.get("id"), str)
        and isinstance(row.get("slug"), str)
    }
    issues: list[ValidationIssue] = []
    extended: list[LoadedRecord] = []
    for record in records.get("documents", ()):
        data = record.data
        if not isinstance(data, Mapping) or data.get("publication_status") != "published":
            continue
        present = EXTENSION_FIELDS.intersection(data)
        roles = data.get("institution_roles")
        has_role_evidence = isinstance(roles, list) and any(
            isinstance(role, Mapping)
            and ("evidence_source_id" in role or "evidence_locator" in role)
            for role in roles
        )
        extension_triggered = bool(
            present or OPTIONAL_EXTENSION_FIELDS.intersection(data) or has_role_evidence
        )
        if extension_triggered and present != EXTENSION_FIELDS:
            issues.append(
                _issue(record, "historical_review_status", "Historical metadata block is partial.")
            )
            continue
        if extension_triggered:
            extended.append(record)
            continue
        identifier, slug = data.get("id"), data.get("slug")
        if not isinstance(identifier, str) or legacy.get(identifier) != slug:
            issues.append(
                _issue(
                    record,
                    "historical_review_status",
                    "A new published document requires complete verified historical metadata.",
                )
            )

    if extended:
        extended_ids = {
            record.data["id"]
            for record in extended
            if isinstance(record.data.get("id"), str)
        }
        issues.extend(
            validate_historical_readiness(
                records, schema_root, publication_cutoff, document_ids=extended_ids
            )
        )
    return sorted(issues, key=lambda item: (item.record_path, item.field, item.code, item.message))
