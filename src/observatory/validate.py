"""Offline structural and cross-record validation for canonical records."""

from collections import defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
from typing import Iterable, Mapping
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

from observatory.io import LoadedRecord, load_records
from observatory.types import ValidationIssue


ENTITY_DIRECTORY_BY_TYPE = {
    "policy": "policies",
    "document": "documents",
    "event": "events",
    "concept": "concepts",
    "institution": "institutions",
    "relationship": "relationships",
    "source": "sources",
}

_VOCABULARY_FIELDS = {
    "publication_status": "publication_status",
    "policy_status": "policy_status",
    "document_type": "document_type",
    "legal_status": "legal_status",
    "event_type": "event_type",
    "relationship_type": "relationship_type",
    "basis": "relationship_basis",
    "verification_status": "verification_status",
    "source_type": "source_type",
}


class RecordValidationError(ValueError):
    """Raised when canonical records contain one or more validation issues."""

    def __init__(self, issues: Iterable[ValidationIssue]) -> None:
        self.issues = tuple(issues)
        message = "\n".join(
            f"{issue.record_path}: {issue.field}: [{issue.code}] {issue.message}"
            for issue in self.issues
        )
        super().__init__(message)


def validate_records(
    data_root: Path, schema_path: Path, vocabulary_path: Path
) -> list[ValidationIssue]:
    """Validate canonical records without making any network requests."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    vocabulary = json.loads(vocabulary_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    entity_validators = {
        entity_type: _entity_validator(schema, entity_type)
        for entity_type in ENTITY_DIRECTORY_BY_TYPE
    }
    entity_properties = {
        entity_type: _entity_property_names(schema, entity_type)
        for entity_type in ENTITY_DIRECTORY_BY_TYPE
    }
    loaded_by_directory = load_records(data_root)
    loaded = [record for records in loaded_by_directory.values() for record in records]
    issues: list[ValidationIssue] = []

    records_by_type: dict[str, dict[str, list[LoadedRecord]]] = defaultdict(
        lambda: defaultdict(list)
    )
    records_by_id: dict[str, list[LoadedRecord]] = defaultdict(list)

    for record in loaded:
        path = _relative_path(record.path, data_root)
        if record.syntax_error is not None:
            issues.append(_issue("json_syntax", path, "$", record.syntax_error))
            continue
        if not isinstance(record.data, Mapping):
            issues.append(_issue("schema", path, "$", "A record must be a JSON object."))
            continue

        entity_type = record.data.get("entity_type")
        schema_validator = (
            entity_validators.get(entity_type, validator)
            if isinstance(entity_type, str)
            else validator
        )
        for error in _leaf_schema_errors(schema_validator.iter_errors(record.data)):
            issues.append(
                _issue(
                    "schema",
                    path,
                    _schema_error_field(error),
                    _schema_error_message(error),
                )
            )
        if isinstance(entity_type, str):
            for property_name in _unexpected_entity_properties(
                record.data, entity_properties.get(entity_type, set())
            ):
                issues.append(
                    _issue(
                        "schema",
                        path,
                        property_name,
                        f"Record contains unsupported property {property_name!r}.",
                    )
                )

        _validate_vocabulary(record, path, vocabulary, issues)
        identifier = record.data.get("id")
        if isinstance(entity_type, str) and isinstance(identifier, str):
            records_by_type[entity_type][identifier].append(record)
            records_by_id[identifier].append(record)
            _validate_canonical_location(record, path, entity_type, identifier, issues)
        _validate_timestamp_order(record, path, issues)

    _validate_duplicate_ids(records_by_id, data_root, issues)
    _validate_duplicate_legal_identifiers(records_by_type, data_root, issues)
    _validate_duplicate_slugs(records_by_type, data_root, issues)
    _validate_snapshots(records_by_type, data_root, issues)

    for record in loaded:
        if record.syntax_error is not None or not isinstance(record.data, Mapping):
            continue
        path = _relative_path(record.path, data_root)
        references = list(_references(record.data))
        _validate_references(record, path, references, records_by_type, issues)
        _validate_source_evidence(record, path, records_by_type, issues)
        _validate_relationship(record, path, records_by_type, issues)

    return sorted(issues, key=lambda issue: (issue.record_path, issue.field, issue.code))


def assert_valid(data_root: Path, schema_path: Path, vocabulary_path: Path) -> None:
    """Raise an actionable error if offline record validation finds issues."""
    issues = validate_records(data_root, schema_path, vocabulary_path)
    if issues:
        raise RecordValidationError(issues)


def _issue(code: str, record_path: str, field: str, message: str) -> ValidationIssue:
    return ValidationIssue(code, record_path, field, message)


def _relative_path(path: Path, data_root: Path) -> str:
    try:
        return path.relative_to(data_root).as_posix()
    except ValueError:
        return path.as_posix()


def _error_field(error: object) -> str:
    absolute_path = getattr(error, "absolute_path", ())
    return ".".join(str(part) for part in absolute_path) or "$"


def _entity_validator(schema: Mapping[str, object], entity_type: str) -> Draft202012Validator:
    """Build a validator for one record kind, avoiding root oneOf diagnostics."""
    entity_schema = {
        "$defs": schema["$defs"],
        "$ref": f"#/$defs/{entity_type}",
    }
    return Draft202012Validator(entity_schema, format_checker=FormatChecker())


def _entity_property_names(schema: Mapping[str, object], entity_type: str) -> set[str]:
    """Return the top-level properties permitted by one canonical entity schema."""
    definitions = schema["$defs"]
    common = definitions["common_envelope"]
    entity = definitions[entity_type]
    properties: set[str] = set()
    for definition in (common, entity):
        if not isinstance(definition, Mapping):
            continue
        for component in definition.get("allOf", [definition]):
            if not isinstance(component, Mapping):
                continue
            referenced = component.get("$ref")
            if isinstance(referenced, str) and referenced.startswith("#/$defs/"):
                component = definitions.get(referenced.rsplit("/", 1)[-1], {})
            component_properties = component.get("properties", {})
            if isinstance(component_properties, Mapping):
                properties.update(
                    name for name in component_properties if isinstance(name, str)
                )
    return properties


def _unexpected_entity_properties(
    data: Mapping[str, object], permitted_properties: set[str]
) -> list[str]:
    """Return unsupported root fields without reporting their potentially private values."""
    return sorted(
        property_name
        for property_name in data
        if property_name not in permitted_properties
    )


def _leaf_schema_errors(errors: Iterable[object]) -> Iterable[object]:
    """Yield actionable leaf errors rather than noisy composition wrappers."""
    for error in errors:
        contexts = getattr(error, "context", ())
        if contexts and getattr(error, "validator", None) in {"oneOf", "anyOf"}:
            yield from _leaf_schema_errors(contexts)
            continue
        yield error


_MISSING_PROPERTY = re.compile(r"'([^']+)' is a required property")


def _schema_error_field(error: object) -> str:
    """Return the failing leaf path, including a missing required property."""
    field = _error_field(error)
    if getattr(error, "validator", None) == "required":
        match = _MISSING_PROPERTY.search(str(getattr(error, "message", "")))
        if match:
            missing = match.group(1)
            return missing if field == "$" else f"{field}.{missing}"
    return field


def _schema_error_message(error: object) -> str:
    """Describe schema failures without echoing canonical record values."""
    validator = getattr(error, "validator", None)
    if validator == "required":
        return str(getattr(error, "message", "Required property is missing."))
    if validator == "type":
        expected = getattr(error, "validator_value", "the required type")
        return f"Value must be of type {expected!r}."
    if validator == "format":
        return "Value does not match the required format."
    if validator == "pattern":
        return "Value does not match the required pattern."
    if validator in {"enum", "const"}:
        return "Value is not an allowed value."
    if validator == "minLength":
        return "Value is shorter than the required minimum length."
    if validator == "uniqueItems":
        return "Array items must be unique."
    if validator == "unevaluatedProperties":
        return "Record contains unsupported properties."
    return "Value does not satisfy the schema."


def _validate_vocabulary(
    record: LoadedRecord,
    path: str,
    vocabulary: Mapping[str, object],
    issues: list[ValidationIssue],
) -> None:
    data = record.data
    for field, vocabulary_name in _VOCABULARY_FIELDS.items():
        value = data.get(field)
        _validate_vocabulary_value(path, field, value, vocabulary_name, vocabulary, issues)

    corpus = data.get("corpus_assessment")
    if isinstance(corpus, Mapping):
        _validate_vocabulary_value(
            path,
            "corpus_assessment.corpus_tier",
            corpus.get("corpus_tier"),
            "corpus_tier",
            vocabulary,
            issues,
        )
        _validate_vocabulary_value(
            path,
            "corpus_assessment.policy_stage",
            corpus.get("policy_stage"),
            "policy_stage",
            vocabulary,
            issues,
        )
        _validate_vocabulary_value(
            path,
            "corpus_assessment.review_status",
            corpus.get("review_status"),
            "verification_status",
            vocabulary,
            issues,
        )

    roles = data.get("institution_roles")
    if isinstance(roles, list):
        for index, role in enumerate(roles):
            if isinstance(role, Mapping):
                _validate_vocabulary_value(
                    path,
                    f"institution_roles.{index}.role",
                    role.get("role"),
                    "institution_role",
                    vocabulary,
                    issues,
                )


def _validate_vocabulary_value(
    path: str,
    field: str,
    value: object,
    vocabulary_name: str,
    vocabulary: Mapping[str, object],
    issues: list[ValidationIssue],
) -> None:
    choices = vocabulary.get(vocabulary_name)
    if isinstance(value, str) and isinstance(choices, list) and value not in choices:
        issues.append(
            _issue(
                "vocabulary",
                path,
                field,
                f"{value!r} is not in the {vocabulary_name!r} controlled vocabulary.",
            )
        )


def _validate_canonical_location(
    record: LoadedRecord,
    path: str,
    entity_type: str,
    identifier: str,
    issues: list[ValidationIssue],
) -> None:
    expected_directory = ENTITY_DIRECTORY_BY_TYPE.get(entity_type)
    if expected_directory is not None and record.path.parent.name != expected_directory:
        issues.append(
            _issue(
                "directory_mismatch",
                path,
                "entity_type",
                f"A {entity_type!r} record must be stored in {expected_directory!r}.",
            )
        )
    expected_filename = f"{identifier}.json"
    if record.path.name != expected_filename:
        issues.append(
            _issue(
                "filename_mismatch",
                path,
                "id",
                f"Record id {identifier!r} requires filename {expected_filename!r}.",
            )
        )


def _validate_timestamp_order(record: LoadedRecord, path: str, issues: list[ValidationIssue]) -> None:
    created_value = record.data.get("created_at")
    updated_value = record.data.get("updated_at")
    for field, value in (("created_at", created_value), ("updated_at", updated_value)):
        if _is_offset_naive_timestamp(value):
            issues.append(
                _issue(
                    "schema",
                    path,
                    field,
                    "Timestamps must include a UTC offset.",
                )
            )
    created_at = _parse_timestamp(created_value)
    updated_at = _parse_timestamp(updated_value)
    if created_at is not None and updated_at is not None and updated_at < created_at:
        issues.append(
            _issue(
                "timestamp_order",
                path,
                "updated_at",
                "updated_at must not be earlier than created_at.",
            )
        )


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return timestamp if timestamp.tzinfo is not None else None
    except ValueError:
        return None


def _is_offset_naive_timestamp(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is None
    except ValueError:
        return False


def _validate_duplicate_ids(
    records_by_id: Mapping[str, list[LoadedRecord]], data_root: Path, issues: list[ValidationIssue]
) -> None:
    for identifier, records in records_by_id.items():
        if len(records) < 2:
            continue
        locations = ", ".join(sorted(_relative_path(record.path, data_root) for record in records))
        for record in records:
            issues.append(
                _issue(
                    "duplicate_id",
                    _relative_path(record.path, data_root),
                    "id",
                    f"Identifier {identifier!r} occurs more than once: {locations}.",
                )
            )


def _validate_duplicate_legal_identifiers(
    records_by_type: Mapping[str, Mapping[str, list[LoadedRecord]]],
    data_root: Path,
    issues: list[ValidationIssue],
) -> None:
    documents = [
        record
        for records in records_by_type.get("document", {}).values()
        for record in records
    ]
    for field, code in (("celex", "duplicate_celex"), ("eli", "duplicate_eli")):
        grouped: dict[str, list[LoadedRecord]] = defaultdict(list)
        for record in documents:
            value = record.data.get(field)
            if isinstance(value, str) and value:
                grouped[value].append(record)
        for value, records in grouped.items():
            if len(records) < 2:
                continue
            for record in records:
                issues.append(
                    _issue(
                        code,
                        _relative_path(record.path, data_root),
                        field,
                        f"{field.upper()} value {value!r} occurs in more than one document.",
                    )
                )


def _validate_duplicate_slugs(
    records_by_type: Mapping[str, Mapping[str, list[LoadedRecord]]],
    data_root: Path,
    issues: list[ValidationIssue],
) -> None:
    grouped: dict[str, list[LoadedRecord]] = defaultdict(list)
    for records in records_by_type.get("document", {}).values():
        for record in records:
            slug = record.data.get("slug")
            if isinstance(slug, str) and slug:
                grouped[slug].append(record)
    for slug, records in grouped.items():
        if len(records) < 2:
            continue
        for record in records:
            issues.append(
                _issue(
                    "duplicate_slug",
                    _relative_path(record.path, data_root),
                    "slug",
                    f"Document slug {slug!r} occurs in more than one document.",
                )
            )


def _validate_snapshots(
    records_by_type: Mapping[str, Mapping[str, list[LoadedRecord]]],
    data_root: Path,
    issues: list[ValidationIssue],
) -> None:
    """Enforce the database snapshot key and validate archived provenance files."""
    repository_root = data_root.resolve().parent
    by_identifier: dict[str, list[tuple[LoadedRecord, int]]] = defaultdict(list)
    for records in records_by_type.get("document", {}).values():
        for record in records:
            snapshots = record.data.get("snapshots")
            if not isinstance(snapshots, list):
                continue
            for index, snapshot in enumerate(snapshots):
                if not isinstance(snapshot, Mapping):
                    continue
                identifier = snapshot.get("id")
                if isinstance(identifier, str):
                    by_identifier[identifier].append((record, index))
                _validate_snapshot_archive(
                    record, index, snapshot, repository_root, data_root, issues
                )

    for identifier, locations in by_identifier.items():
        if len(locations) < 2:
            continue
        for record, index in locations:
            issues.append(
                _issue(
                    "duplicate_snapshot_id",
                    _relative_path(record.path, data_root),
                    f"snapshots.{index}.id",
                    f"Snapshot id {identifier!r} occurs more than once in canonical documents.",
                )
            )


def _validate_snapshot_archive(
    record: LoadedRecord,
    index: int,
    snapshot: Mapping[str, object],
    repository_root: Path,
    data_root: Path,
    issues: list[ValidationIssue],
) -> None:
    archived_path = snapshot.get("archived_path")
    if archived_path is None:
        return
    path = _relative_path(record.path, data_root)
    archive_field = f"snapshots.{index}.archived_path"
    hash_field = f"snapshots.{index}.content_hash"
    if not isinstance(archived_path, str) or not _is_safe_archive_path(archived_path):
        issues.append(
            _issue(
                "invalid_snapshot_archive",
                path,
                archive_field,
                "archived_path must be a safe repository-relative file path.",
            )
        )
        return

    archive = (repository_root / PurePosixPath(archived_path)).resolve()
    try:
        archive.relative_to(repository_root)
    except ValueError:
        issues.append(
            _issue(
                "invalid_snapshot_archive",
                path,
                archive_field,
                "archived_path must resolve within the repository root.",
            )
        )
        return
    if not archive.is_file():
        issues.append(
            _issue(
                "invalid_snapshot_archive",
                path,
                archive_field,
                "archived_path must identify an existing regular file.",
            )
        )
        return

    content_hash = snapshot.get("content_hash")
    if isinstance(content_hash, str):
        actual_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual_hash != content_hash:
            issues.append(
                _issue(
                    "snapshot_hash_mismatch",
                    path,
                    hash_field,
                    "content_hash does not match the archived file SHA-256.",
                )
            )


def _is_safe_archive_path(value: str) -> bool:
    """Accept only portable repository-relative POSIX paths."""
    parsed = urlparse(value)
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    return (
        bool(value)
        and "\\" not in value
        and not parsed.scheme
        and not posix.is_absolute()
        and not windows.is_absolute()
        and not windows.drive
        and ".." not in posix.parts
    )


def _references(data: Mapping[str, object]) -> Iterable[tuple[str, str, str]]:
    entity_type = data.get("entity_type")
    if entity_type == "document":
        yield from _id_list_references(data, "policy_ids", "policy")
        yield from _id_list_references(data, "concept_ids", "concept")
        yield from _id_list_references(data, "source_ids", "source")
        roles = data.get("institution_roles")
        if isinstance(roles, list):
            for index, role in enumerate(roles):
                if isinstance(role, Mapping):
                    identifier = role.get("institution_id")
                    if isinstance(identifier, str):
                        yield (f"institution_roles.{index}.institution_id", "institution", identifier)
        snapshots = data.get("snapshots")
        if isinstance(snapshots, list):
            for index, snapshot in enumerate(snapshots):
                if isinstance(snapshot, Mapping):
                    identifier = snapshot.get("source_id")
                    if isinstance(identifier, str):
                        yield (f"snapshots.{index}.source_id", "source", identifier)
    elif entity_type == "event":
        yield from _single_reference(data, "policy_id", "policy")
        yield from _single_reference(data, "document_id", "document")
        yield from _single_reference(data, "source_id", "source")
    elif entity_type == "relationship":
        yield from _relationship_endpoint(data, "source")
        yield from _relationship_endpoint(data, "target")
        yield from _single_reference(data, "evidence_source_id", "source")


def _id_list_references(
    data: Mapping[str, object], field: str, target_type: str
) -> Iterable[tuple[str, str, str]]:
    identifiers = data.get(field)
    if isinstance(identifiers, list):
        for index, identifier in enumerate(identifiers):
            if isinstance(identifier, str):
                yield (f"{field}.{index}", target_type, identifier)


def _single_reference(
    data: Mapping[str, object], field: str, target_type: str
) -> Iterable[tuple[str, str, str]]:
    identifier = data.get(field)
    if isinstance(identifier, str):
        yield (field, target_type, identifier)


def _relationship_endpoint(
    data: Mapping[str, object], side: str
) -> Iterable[tuple[str, str, str]]:
    target_type = data.get(f"{side}_entity_type")
    identifier = data.get(f"{side}_entity_id")
    if isinstance(target_type, str) and isinstance(identifier, str):
        yield (f"{side}_entity_id", target_type, identifier)


def _validate_references(
    record: LoadedRecord,
    path: str,
    references: Iterable[tuple[str, str, str]],
    records_by_type: Mapping[str, Mapping[str, list[LoadedRecord]]],
    issues: list[ValidationIssue],
) -> None:
    is_published = record.data.get("publication_status") == "published"
    for field, target_type, identifier in references:
        targets = records_by_type.get(target_type, {}).get(identifier, [])
        if not targets:
            issues.append(
                _issue(
                    "missing_reference",
                    path,
                    field,
                    f"Referenced {target_type} {identifier!r} does not exist.",
                )
            )
        elif is_published and any(
            target.data.get("publication_status") != "published" for target in targets
        ):
            issues.append(
                _issue(
                    "publication_boundary",
                    path,
                    field,
                    f"Published records may reference only published {target_type} records; {identifier!r} is not published.",
                )
            )


def _validate_source_evidence(
    record: LoadedRecord,
    path: str,
    records_by_type: Mapping[str, Mapping[str, list[LoadedRecord]]],
    issues: list[ValidationIssue],
) -> None:
    if record.data.get("publication_status") not in {"published", "verified"}:
        return
    entity_type = record.data.get("entity_type")
    if entity_type == "document":
        source_ids = record.data.get("source_ids")
        valid_source_ids = [
            identifier
            for identifier in source_ids if isinstance(identifier, str)
        ] if isinstance(source_ids, list) else []
        if not valid_source_ids or not any(
            records_by_type.get("source", {}).get(identifier) for identifier in valid_source_ids
        ):
            issues.append(
                _issue(
                    "missing_evidence",
                    path,
                    "source_ids",
                    "Published or verified documents require at least one existing source record.",
                )
            )
    elif entity_type == "event":
        source_id = record.data.get("source_id")
        if not isinstance(source_id, str) or not records_by_type.get("source", {}).get(source_id):
            issues.append(
                _issue(
                    "missing_evidence",
                    path,
                    "source_id",
                    "Published or verified events require an existing source record.",
                )
            )
    elif entity_type == "relationship":
        source_id = record.data.get("evidence_source_id")
        if not isinstance(source_id, str) or not records_by_type.get("source", {}).get(source_id):
            issues.append(
                _issue(
                    "missing_evidence",
                    path,
                    "evidence_source_id",
                    "Published or verified relationships require an existing evidence source.",
                )
            )


def _validate_relationship(
    record: LoadedRecord,
    path: str,
    records_by_type: Mapping[str, Mapping[str, list[LoadedRecord]]],
    issues: list[ValidationIssue],
) -> None:
    data = record.data
    if data.get("entity_type") != "relationship":
        return
    evidence_source_id = data.get("evidence_source_id")
    rationale = data.get("rationale")
    if data.get("basis") == "analytical" and (
        not isinstance(rationale, str)
        or not rationale.strip()
        or not isinstance(evidence_source_id, str)
    ):
        issues.append(
            _issue(
                "analytical_evidence",
                path,
                "rationale",
                "Analytical relationships require both a rationale and an evidence source.",
            )
        )
    if data.get("basis") == "official" and isinstance(evidence_source_id, str):
        sources = records_by_type.get("source", {}).get(evidence_source_id, [])
        if sources and any(not _is_official_source(source.data) for source in sources):
            issues.append(
                _issue(
                    "official_evidence",
                    path,
                    "evidence_source_id",
                    "Official relationships require evidence from an official HTTPS source.",
                )
            )


def _is_official_source(data: Mapping[str, object]) -> bool:
    url = data.get("url")
    source_type = data.get("source_type")
    if not isinstance(url, str) or not isinstance(source_type, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and source_type in {
        "eur_lex",
        "eli",
        "commission_webpage",
        "official_pdf",
        "publications_office",
    }
