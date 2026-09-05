"""Read-only evidence-readiness checks reused by the publication gate."""

from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker

from observatory.io import LoadedRecord, load_records
from observatory.historical_relationships import validate_historical_relationships
from observatory.types import ValidationIssue
from observatory.validate import _is_official_source


CONTRACT_VERSION = "historical-readiness-1"
_HISTORICAL_BOUNDARY = date(2018, 1, 1)
_ACT_TYPES = {"regulation", "directive", "decision", "implementing_regulation"}
_ADOPTION_TYPES = {"resolution", "opinion", "conclusions"}
_ISSUER_ROLES = {"author", "proposer", "adopter"}


def prospective_document_schema(schema_root: Path) -> dict:
    """Return a deep-copied document schema; never mutate or write the base."""
    base = json.loads((schema_root / "record.schema.json").read_text(encoding="utf-8"))
    extension = json.loads(
        (schema_root / "historical-document-extension.schema.json").read_text(encoding="utf-8")
    )
    result = deepcopy(base)
    result["oneOf"] = [{"$ref": "#/$defs/document"}]
    result["$defs"].update(deepcopy(extension["$defs"]))
    document = result["$defs"]["document"]["allOf"][1]
    document["properties"].update(deepcopy(extension["properties"]))
    document["required"].extend(deepcopy(extension["required"]))
    document["properties"]["document_type"]["enum"] = sorted(
        set(document["properties"]["document_type"]["enum"]) | {"directive", "conclusions"}
    )
    document["properties"]["legal_status"]["enum"] = sorted(
        set(document["properties"]["legal_status"]["enum"])
        | {"no_longer_in_force", "repealed", "expired"}
    )
    return result


def _issue(code: str, record: LoadedRecord | None, field: str, message: str) -> ValidationIssue:
    return ValidationIssue(
        code=code,
        record_path=record.path.as_posix() if record else "data/documents",
        field=field,
        message=message,
    )


def _exact_date(value: object) -> date | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _schema_field(error) -> str:
    if error.validator == "required":
        match = re.match(r"'([^']+)' is a required property", error.message)
        if match:
            prefix = ".".join(str(part) for part in error.absolute_path)
            return ".".join(part for part in (prefix, match.group(1)) if part)
    return ".".join(str(part) for part in error.absolute_path) or "record"


def _leaf_schema_errors(error) -> Iterable:
    if error.context:
        for child in error.context:
            yield from _leaf_schema_errors(child)
    else:
        yield error


def _schema_issues(record: LoadedRecord, validator: Draft202012Validator) -> list[ValidationIssue]:
    seen: set[tuple[str, str]] = set()
    issues: list[ValidationIssue] = []
    for top_error in validator.iter_errors(record.data):
        for error in _leaf_schema_errors(top_error):
            field = _schema_field(error)
            key = (field, error.validator)
            if key in seen:
                continue
            seen.add(key)
            issues.append(
                _issue(
                    "historical_schema",
                    record,
                    field,
                    f"Prospective document schema constraint failed ({error.validator}).",
                )
            )
    return issues


def _timestamp_is_aware(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _source_index(records: Mapping[str, Sequence[LoadedRecord]]) -> dict[str, list[LoadedRecord]]:
    result: dict[str, list[LoadedRecord]] = defaultdict(list)
    for source in records.get("sources", ()):
        if not isinstance(source.data, Mapping):
            continue
        source_id = source.data.get("id")
        if isinstance(source_id, str):
            result[source_id].append(source)
    return result


def _check_evidence_source(
    source_id: object,
    declared_ids: set[str],
    sources: Mapping[str, Sequence[LoadedRecord]],
    record: LoadedRecord,
    field: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(source_id, str):
        return
    matches = sources.get(source_id, ())
    if source_id not in declared_ids:
        issues.append(_issue("historical_evidence", record, field, "Evidence source is not declared in source_ids."))
    if len(matches) != 1:
        issues.append(_issue("historical_evidence", record, field, "Evidence source must resolve to exactly one source record."))
        return
    source = matches[0].data
    if source.get("publication_status") != "published" or not _is_official_source(source):
        issues.append(_issue("historical_evidence", record, field, "Evidence source must be published and use an official HTTPS source."))


def _document_evidence_references(data: Mapping[str, object]) -> Iterable[tuple[str, object]]:
    date_evidence = data.get("date_evidence")
    if isinstance(date_evidence, Mapping):
        for key in ("document_date", "publication_date"):
            citation = date_evidence.get(key)
            if isinstance(citation, Mapping):
                yield f"date_evidence.{key}.source_id", citation.get("source_id")
    classification = data.get("classification_evidence")
    if isinstance(classification, list):
        for index, item in enumerate(classification):
            if isinstance(item, Mapping):
                yield f"classification_evidence.{index}.source_id", item.get("source_id")
    authors = data.get("bibliographic_authors")
    if isinstance(authors, list):
        for index, author in enumerate(authors):
            if isinstance(author, Mapping):
                yield f"bibliographic_authors.{index}.evidence_source_id", author.get("evidence_source_id")
    additional = data.get("additional_dates")
    if isinstance(additional, list):
        for index, item in enumerate(additional):
            if isinstance(item, Mapping):
                yield f"additional_dates.{index}.source_id", item.get("source_id")
    roles = data.get("institution_roles")
    if isinstance(roles, list):
        for index, role in enumerate(roles):
            if isinstance(role, Mapping):
                yield f"institution_roles.{index}.evidence_source_id", role.get("evidence_source_id")
    status = data.get("legal_status_evidence")
    if isinstance(status, Mapping):
        yield "legal_status_evidence.source_id", status.get("source_id")


def _validate_dates(record: LoadedRecord, cutoff: date, issues: list[ValidationIssue]) -> None:
    data = record.data
    document_date = _exact_date(data.get("document_date"))
    publication_date = _exact_date(data.get("publication_date"))
    for field, parsed in (("document_date", document_date), ("publication_date", publication_date)):
        if parsed is None:
            issues.append(_issue("historical_date", record, field, "Date must be an exact valid calendar date."))
        elif parsed > cutoff:
            issues.append(_issue("historical_date", record, field, "Date is after the explicit publication cutoff."))
    if document_date is not None:
        expected = "historical_lineage" if document_date < _HISTORICAL_BOUNDARY else "contemporary_eu_ai_policy"
        if data.get("temporal_collection") != expected:
            issues.append(_issue("historical_collection", record, "temporal_collection", "Temporal collection does not match the supplied document date."))
    kind = data.get("document_date_kind")
    document_type = data.get("document_type")
    version_status = data.get("version_status")
    invalid_kind = (
        (kind == "official_act_date" and (not isinstance(document_type, str) or document_type not in _ACT_TYPES))
        or (kind == "institutional_adoption" and (not isinstance(document_type, str) or document_type not in _ADOPTION_TYPES))
        or (kind == "consolidation" and version_status != "consolidated")
        or (version_status == "consolidated" and kind != "consolidation")
    )
    if kind == "publication" and document_date != publication_date:
        invalid_kind = True
    if invalid_kind:
        issues.append(_issue("historical_date", record, "document_date_kind", "Document date kind is incompatible with the supplied document record."))
    additional = data.get("additional_dates")
    if isinstance(additional, list):
        for index, item in enumerate(additional):
            if not isinstance(item, Mapping):
                continue
            value, precision = item.get("value"), item.get("precision")
            valid = False
            if precision == "day":
                valid = _exact_date(value) is not None
            elif precision == "month" and isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}", value):
                valid = 1 <= int(value[5:]) <= 12 and value[:4] != "0000"
            elif precision == "year" and isinstance(value, str) and re.fullmatch(r"\d{4}", value):
                valid = value != "0000"
            if not valid:
                issues.append(_issue("historical_date", record, f"additional_dates.{index}.value", "Additional date value must match its calendar precision."))


def _validate_classification(record: LoadedRecord, issues: list[ValidationIssue]) -> None:
    data = record.data
    expected: set[tuple[str, str]] = set()
    relevance = data.get("relevance_class")
    if isinstance(relevance, str):
        expected.add(("relevance_class", relevance))
    for field in ("sector_tags", "provenance_tags"):
        values = data.get(field)
        if isinstance(values, list):
            expected.update((field, value) for value in values if isinstance(value, str))
    supplied: set[tuple[str, str]] = set()
    evidence = data.get("classification_evidence")
    if isinstance(evidence, list):
        for index, item in enumerate(evidence):
            if not isinstance(item, Mapping):
                continue
            field_name, item_value = item.get("field"), item.get("value")
            pair = (field_name, item_value)
            if isinstance(field_name, str) and isinstance(item_value, str):
                supplied.add((field_name, item_value))
            if not isinstance(field_name, str) or not isinstance(item_value, str) or pair not in expected:
                issues.append(_issue("historical_classification", record, f"classification_evidence.{index}.value", "Classification evidence value is absent from the document."))
            for key in ("value", "locator", "rationale"):
                value = item.get(key)
                if not isinstance(value, str) or not value.strip():
                    issues.append(_issue("historical_classification", record, f"classification_evidence.{index}.{key}", "Classification evidence values must be nonblank."))
    for missing in expected - supplied:
        issues.append(_issue("historical_classification", record, "classification_evidence", f"Classification evidence does not cover {missing[0]}."))
    corpus = data.get("corpus_assessment")
    if isinstance(corpus, Mapping):
        if corpus.get("review_status") != "verified":
            issues.append(_issue("historical_classification", record, "corpus_assessment.review_status", "Corpus assessment must be verified."))
        for field in ("reviewed_by", "inclusion_rationale"):
            value = corpus.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(_issue("historical_classification", record, f"corpus_assessment.{field}", "Reviewed classification metadata must be nonblank."))
        if not _timestamp_is_aware(corpus.get("reviewed_at")):
            issues.append(_issue("historical_classification", record, "corpus_assessment.reviewed_at", "Review timestamp must include a timezone."))


def _validate_attribution(record: LoadedRecord, institution_counts: Mapping[str, int], issues: list[ValidationIssue]) -> None:
    data = record.data
    roles = data.get("institution_roles")
    pairs: set[tuple[object, object]] = set()
    commissioners = 0
    if isinstance(roles, list):
        for index, role in enumerate(roles):
            if not isinstance(role, Mapping):
                continue
            institution_id, role_name = role.get("institution_id"), role.get("role")
            if isinstance(institution_id, str) and isinstance(role_name, str):
                pair = (institution_id, role_name)
                if pair in pairs:
                    issues.append(_issue("historical_attribution", record, f"institution_roles.{index}", "Institution and role pairs must be unique."))
                pairs.add(pair)
            if not isinstance(institution_id, str) or institution_counts.get(institution_id, 0) != 1:
                issues.append(_issue("historical_attribution", record, f"institution_roles.{index}.institution_id", "Institution role must resolve to exactly one institution record."))
            if role_name == "commissioner":
                commissioners += 1
    if isinstance(data.get("provenance_tags"), list) and "eu_commissioned_external" in data["provenance_tags"]:
        authors = data.get("bibliographic_authors")
        named = isinstance(authors, list) and any(isinstance(author, Mapping) and isinstance(author.get("name"), str) and author["name"].strip() for author in authors)
        if not named or commissioners == 0:
            issues.append(_issue("historical_attribution", record, "bibliographic_authors", "Externally commissioned work requires a named author and commissioner role."))


def _identity_issues(documents: Sequence[LoadedRecord]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for field in ("id", "slug", "celex", "eli"):
        grouped: dict[str, list[LoadedRecord]] = defaultdict(list)
        for record in documents:
            value = record.data.get(field)
            if isinstance(value, str) and value:
                grouped[value].append(record)
        for matches in grouped.values():
            if len(matches) > 1:
                issues.extend(_issue("historical_identity", record, field, f"Published document {field} must be unique.") for record in matches)
    identities: dict[tuple[object, object, object, tuple[str, ...]], list[LoadedRecord]] = defaultdict(list)
    for record in documents:
        data = record.data
        reference = data.get("official_reference")
        if not isinstance(reference, str) or not reference.strip():
            continue
        label = data.get("version_label")
        normalized_label = " ".join(label.split()).casefold() if isinstance(label, str) else None
        roles = data.get("institution_roles")
        issuers = tuple(sorted(role["institution_id"] for role in roles if isinstance(role, Mapping) and isinstance(role.get("role"), str) and role.get("role") in _ISSUER_ROLES and isinstance(role.get("institution_id"), str))) if isinstance(roles, list) else ()
        language = data.get("language")
        if isinstance(language, str):
            identities[(reference, language, normalized_label, issuers)].append(record)
    for matches in identities.values():
        if len(matches) > 1:
            issues.extend(_issue("historical_identity", record, "official_reference", "Version-aware document identity occurs more than once.") for record in matches)
    return issues


def validate_historical_readiness(
    records: Mapping[str, Sequence[LoadedRecord]],
    schema_root: Path,
    publication_cutoff: str,
    document_ids: set[str] | None = None,
) -> list[ValidationIssue]:
    """Assess published documents and their evidence; never infer or modify fields."""
    cutoff = _exact_date(publication_cutoff)
    if cutoff is None:
        return [_issue("historical_input", None, "publication_cutoff", "Publication cutoff must be an exact valid calendar date.")]
    issues: list[ValidationIssue] = []
    for group in records.values():
        for record in group:
            if record.syntax_error:
                issues.append(_issue("historical_input", record, "record", "Canonical record contains malformed JSON."))
            elif not isinstance(record.data, Mapping):
                issues.append(_issue("historical_input", record, "record", "Canonical record must decode to a JSON object."))
    documents = [record for record in records.get("documents", ()) if isinstance(record.data, Mapping) and record.data.get("publication_status") == "published"]
    if not documents:
        issues.append(_issue("historical_input", None, "documents", "At least one published document is required."))
        return sorted(issues, key=lambda item: (item.record_path, item.field, item.code, item.message))
    validator = Draft202012Validator(prospective_document_schema(schema_root), format_checker=FormatChecker())
    sources = _source_index(records)
    institution_counts: dict[str, int] = defaultdict(int)
    for institution in records.get("institutions", ()):
        if isinstance(institution.data, Mapping) and isinstance(institution.data.get("id"), str):
            institution_counts[institution.data["id"]] += 1
    target_documents = [
        record
        for record in documents
        if document_ids is None or record.data.get("id") in document_ids
    ]
    for record in target_documents:
        issues.extend(_schema_issues(record, validator))
        _validate_dates(record, cutoff, issues)
        _validate_classification(record, issues)
        _validate_attribution(record, institution_counts, issues)
        declared = {value for value in record.data.get("source_ids", ()) if isinstance(value, str)} if isinstance(record.data.get("source_ids"), list) else set()
        for field, source_id in _document_evidence_references(record.data):
            _check_evidence_source(source_id, declared, sources, record, field, issues)
        legal_status = record.data.get("legal_status")
        if isinstance(legal_status, str) and legal_status in {"no_longer_in_force", "repealed", "expired"} and not isinstance(record.data.get("legal_status_evidence"), Mapping):
            issues.append(_issue("historical_evidence", record, "legal_status_evidence", "Historical validity status requires its own official citation."))
    issues.extend(_identity_issues(documents))
    issues.extend(
        validate_historical_relationships(
            records, documents, sources, target_document_ids=document_ids
        )
    )
    return sorted(issues, key=lambda item: (item.record_path, item.field, item.code, item.message))


def main(argv: list[str] | None = None) -> int:
    """Print deterministic JSON; 0 ready, 1 gaps, 2 invalid invocation/input."""
    parser = argparse.ArgumentParser(description="Run the inactive historical readiness preflight.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--publication-cutoff", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return int(error.code)
    if _exact_date(args.publication_cutoff) is None:
        print("Error: publication cutoff must be an exact valid calendar date (YYYY-MM-DD).", file=sys.stderr)
        return 2
    try:
        records = load_records(args.project_root / "data")
        malformed = sorted(record.path.resolve().relative_to(args.project_root.resolve()).as_posix() for group in records.values() for record in group if record.syntax_error)
        if malformed:
            print(f"Error: malformed canonical JSON input: {', '.join(malformed)}.", file=sys.stderr)
            return 2
        nonobjects = sorted(record.path.resolve().relative_to(args.project_root.resolve()).as_posix() for group in records.values() for record in group if not isinstance(record.data, Mapping))
        if nonobjects:
            print(f"Error: canonical JSON records must decode to objects: {', '.join(nonobjects)}.", file=sys.stderr)
            return 2
        published = [record for record in records.get("documents", ()) if record.data.get("publication_status") == "published"]
        if not published:
            print("Error: canonical input contains no published documents.", file=sys.stderr)
            return 2
        issues = validate_historical_readiness(records, args.project_root / "schema", args.publication_cutoff)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: invalid project input ({type(error).__name__}).", file=sys.stderr)
        return 2
    issue_paths = {issue.record_path for issue in issues}
    relationship_documents: dict[str, set[str]] = {}
    for record in records.get("relationships", ()):
        endpoint_ids = {
            record.data.get(f"{side}_entity_id")
            for side in ("source", "target")
            if record.data.get(f"{side}_entity_type") == "document"
            and isinstance(record.data.get(f"{side}_entity_id"), str)
        }
        relationship_documents[record.path.as_posix()] = endpoint_ids
    affected_ids = set().union(*(relationship_documents[path] for path in issue_paths if path in relationship_documents))
    ready = sum(record.path.as_posix() not in issue_paths and isinstance(record.data.get("id"), str) and record.data.get("id") not in affected_ids for record in published)
    payload = {
        "contract_version": CONTRACT_VERSION,
        "publication_contract_active": False,
        "publication_cutoff": args.publication_cutoff,
        "documents_checked": len(published),
        "documents_ready": ready,
        "issues": [asdict(issue) for issue in issues],
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=False, separators=(",", ":")))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
