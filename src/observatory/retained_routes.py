"""Active validation for narrowly reviewed retained document routes."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Mapping, Sequence

from observatory.io import LoadedRecord
from observatory.types import ValidationIssue


STATUS = "parent_relationship_under_review"
LANDING_SOURCE_ID = "high-risk-guidelines-draft-commission"
LANDING_LOCATOR = (
    "Publication date; paragraph immediately before Downloads explaining the "
    "separate sections; Downloads 1–3."
)
PDF_LOCATOR = "Pages 1–2 (cover and first body page)."
REVIEWED_DOCUMENTS = {
    "draft-high-risk-classification-guidelines-2026": "commission-newsroom-128559-pdf",
    "draft-high-risk-classification-guidelines-annex-i-2026": "commission-newsroom-128560-pdf",
    "draft-high-risk-classification-guidelines-annex-iii-2026": "commission-newsroom-128561-pdf",
}


def validate_retained_route_notices(
    records: Mapping[str, Sequence[LoadedRecord]], data_root: Path
) -> list[ValidationIssue]:
    """Validate the reviewed missing-parent exception without suppressing lineage holds."""
    issues: list[ValidationIssue] = []
    documents = [
        record
        for record in records.get("documents", ())
        if record.syntax_error is None and isinstance(record.data, Mapping)
    ]
    sources_by_id: dict[str, list[LoadedRecord]] = defaultdict(list)
    for source in records.get("sources", ()):
        if source.syntax_error is not None or not isinstance(source.data, Mapping):
            continue
        source_id = source.data.get("id")
        if isinstance(source_id, str):
            sources_by_id[source_id].append(source)

    unresolved_paths = _unresolved_lineage_paths(records, documents, sources_by_id)
    for record in documents:
        data = record.data
        document_id = data.get("id")
        notice = data.get("retained_route_notice")
        path = _relative_path(record.path, data_root)
        unresolved = record.path.as_posix() in unresolved_paths
        scoped = isinstance(document_id, str) and document_id in REVIEWED_DOCUMENTS
        required = (
            scoped
            and data.get("publication_status") == "published"
            and data.get("record_level") == "attachment"
            and data.get("version_status") == "draft"
            and unresolved
        )

        if notice is None:
            if required:
                issues.append(
                    _issue(
                        path,
                        "retained_route_notice",
                        "This unresolved published section requires its reviewed retained-route notice.",
                    )
                )
            continue
        if not isinstance(notice, Mapping):
            issues.append(
                _issue(path, "retained_route_notice", "Retained-route notice must be an object.")
            )
            continue
        if not scoped:
            issues.append(
                _issue(
                    path,
                    "retained_route_notice",
                    "Retained-route notices are limited to the three reviewed section records.",
                )
            )
        if scoped and (
            data.get("publication_status") != "published"
            or data.get("record_level") != "attachment"
            or data.get("version_status") != "draft"
        ):
            issues.append(
                _issue(
                    path,
                    "retained_route_notice",
                    "The reviewed notice is valid only on a published attachment in draft status.",
                )
            )
        if scoped and not unresolved:
            issues.append(
                _issue(
                    path,
                    "retained_route_notice",
                    "The notice is stale because a valid evidenced parent relationship now exists.",
                )
            )

        if notice.get("status") != STATUS:
            issues.append(
                _issue(
                    path,
                    "retained_route_notice.status",
                    f"Notice status must be {STATUS!r}.",
                )
            )
        _validate_nonblank(notice, "reason", path, issues)
        _validate_nonblank(notice, "reviewed_by", path, issues)
        if notice.get("reviewed_by") != "Codex":
            issues.append(
                _issue(
                    path,
                    "retained_route_notice.reviewed_by",
                    "The reviewed exception must retain its Codex editorial attribution.",
                )
            )
        _validate_reviewed_at(data, notice, path, issues)
        if scoped:
            _validate_evidence(
                data,
                notice,
                REVIEWED_DOCUMENTS[document_id],
                sources_by_id,
                path,
                issues,
            )

    return sorted(issues, key=lambda issue: (issue.record_path, issue.field, issue.message))


def _unresolved_lineage_paths(
    records: Mapping[str, Sequence[LoadedRecord]],
    documents: Sequence[LoadedRecord],
    sources_by_id: Mapping[str, Sequence[LoadedRecord]],
) -> set[str]:
    from observatory.historical_relationships import validate_historical_relationships

    try:
        lineage_issues = validate_historical_relationships(
            records, documents, sources_by_id
        )
    except (AttributeError, KeyError, TypeError, ValueError):
        return set()
    return {
        issue.record_path
        for issue in lineage_issues
        if issue.code == "historical_relationship" and issue.field == "record_level"
    }


def _validate_nonblank(
    notice: Mapping[str, object],
    field: str,
    path: str,
    issues: list[ValidationIssue],
) -> None:
    value = notice.get(field)
    if not isinstance(value, str) or not value.strip():
        issues.append(
            _issue(
                path,
                f"retained_route_notice.{field}",
                f"Notice {field} must be a nonblank string.",
            )
        )


def _validate_reviewed_at(
    document: Mapping[str, object],
    notice: Mapping[str, object],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    reviewed_at = _timestamp(notice.get("reviewed_at"))
    if reviewed_at is None:
        issues.append(
            _issue(
                path,
                "retained_route_notice.reviewed_at",
                "Notice review time must be a timezone-aware ISO timestamp.",
            )
        )
        return
    created_at = _timestamp(document.get("created_at"))
    updated_at = _timestamp(document.get("updated_at"))
    if created_at is not None and reviewed_at < created_at:
        issues.append(
            _issue(
                path,
                "retained_route_notice.reviewed_at",
                "Notice review time must not precede document creation.",
            )
        )
    if updated_at is not None and reviewed_at > updated_at:
        issues.append(
            _issue(
                path,
                "retained_route_notice.reviewed_at",
                "Notice review time must not follow the document update time.",
            )
        )


def _validate_evidence(
    document: Mapping[str, object],
    notice: Mapping[str, object],
    expected_pdf_id: str,
    sources_by_id: Mapping[str, Sequence[LoadedRecord]],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    from observatory.validate import _is_official_source

    evidence = notice.get("evidence")
    if not isinstance(evidence, list):
        issues.append(
            _issue(
                path,
                "retained_route_notice.evidence",
                "Notice evidence must be an ordered list.",
            )
        )
        return
    declared = document.get("source_ids")
    declared_ids = (
        {source_id for source_id in declared if isinstance(source_id, str)}
        if isinstance(declared, list)
        else set()
    )
    seen: set[str] = set()
    locators: dict[str, str] = {}
    for index, item in enumerate(evidence):
        field = f"retained_route_notice.evidence.{index}"
        if not isinstance(item, Mapping):
            issues.append(_issue(path, field, "Evidence entry must be an object."))
            continue
        source_id = item.get("source_id")
        locator = item.get("locator")
        if not isinstance(locator, str) or not locator.strip():
            issues.append(
                _issue(path, f"{field}.locator", "Evidence locator must be nonblank.")
            )
        if not isinstance(source_id, str):
            issues.append(
                _issue(path, f"{field}.source_id", "Evidence source ID must be a string.")
            )
            continue
        if source_id in seen:
            issues.append(
                _issue(path, f"{field}.source_id", "Evidence source IDs must be distinct.")
            )
        seen.add(source_id)
        if isinstance(locator, str):
            locators[source_id] = locator
        if source_id not in declared_ids:
            issues.append(
                _issue(
                    path,
                    f"{field}.source_id",
                    "Evidence source must be declared in this document's source_ids.",
                )
            )
        matches = sources_by_id.get(source_id, ())
        if len(matches) != 1:
            issues.append(
                _issue(
                    path,
                    f"{field}.source_id",
                    "Evidence source must resolve uniquely to one canonical source.",
                )
            )
        elif (
            matches[0].data.get("publication_status") != "published"
            or not _is_official_source(matches[0].data)
        ):
            issues.append(
                _issue(
                    path,
                    f"{field}.source_id",
                    "Evidence source must be a published official HTTPS source.",
                )
            )
    for source_id, locator in (
        (LANDING_SOURCE_ID, LANDING_LOCATOR),
        (expected_pdf_id, PDF_LOCATOR),
    ):
        if source_id not in seen:
            issues.append(
                _issue(
                    path,
                    "retained_route_notice.evidence",
                    f"Notice must cite reviewed source {source_id!r}.",
                )
            )
        elif locators.get(source_id) != locator:
            issues.append(
                _issue(
                    path,
                    "retained_route_notice.evidence",
                    f"Reviewed source {source_id!r} must retain its approved locator.",
                )
            )


def _timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _relative_path(path: Path, data_root: Path) -> str:
    try:
        return path.relative_to(data_root).as_posix()
    except ValueError:
        return path.as_posix()


def _issue(path: str, field: str, message: str) -> ValidationIssue:
    return ValidationIssue("retained_route_notice", path, field, message)
