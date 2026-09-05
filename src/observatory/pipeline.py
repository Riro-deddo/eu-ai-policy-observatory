"""End-to-end, atomic build of canonical Observatory data."""

from dataclasses import dataclass
import argparse
from datetime import datetime, timedelta
import os
from pathlib import Path
import shutil
import sys
import tempfile

from observatory.build_db import build_database
from observatory.coverage import build_public_coverage_summary
from observatory.export_public import export_public
from observatory.historical_publication import validate_historical_publication
from observatory.io import load_records
from observatory.validate import (
    RecordValidationError,
    assert_valid,
    assert_valid_research_inventory,
)


DATABASE_FILENAME = "eu-ai-policy-observatory.sqlite"
PUBLIC_JSON_FILENAME = "public-data.json"


@dataclass(frozen=True, slots=True)
class BuildOutputs:
    """Locations and canonical-record counts produced by a successful build."""

    database: Path
    public_json: Path
    record_counts: dict[str, int]


def run_pipeline(
    project_root: Path, build_timestamp: str, output_root: Path | None = None
) -> BuildOutputs:
    """Validate, build, export, then atomically publish both generated artefacts."""
    _validate_build_timestamp(build_timestamp)
    root = Path(project_root).resolve()
    data_root = root / "data"
    schema_root = root / "schema"
    destination = Path(output_root) if output_root is not None else root / "generated"

    # Validation is deliberately first: a failed validation never changes existing outputs.
    assert_valid(data_root, schema_root / "record.schema.json", schema_root / "controlled-vocabularies.json")
    assert_valid_research_inventory(root / "research", schema_root, data_root)
    audit_summary = build_public_coverage_summary(root / "research")
    records = load_records(data_root)
    historical_issues = validate_historical_publication(
        records,
        schema_root,
        str(audit_summary["coverage_cutoff"]),
        root / "research" / "migrations" / "2026-09-05-public-document-baseline.json",
    )
    if historical_issues:
        raise RecordValidationError(historical_issues)
    record_counts = {directory: len(entries) for directory, entries in records.items()}
    public_records = {
        directory: [
            record
            for record in entries
            if record.data.get("publication_status") == "published"
        ]
        for directory, entries in records.items()
    }

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(tempfile.mkdtemp(prefix=".observatory-build-", dir=destination.parent))
    temporary_database = temporary_root / DATABASE_FILENAME
    temporary_public_json = temporary_root / PUBLIC_JSON_FILENAME
    database = destination / DATABASE_FILENAME
    public_json = destination / PUBLIC_JSON_FILENAME
    try:
        build_database(public_records, schema_root / "database.sql", temporary_database)
        export_public(
            temporary_database,
            temporary_public_json,
            build_timestamp,
            audit_summary,
        )
        destination.mkdir(parents=True, exist_ok=True)
        _publish_output_pair(
            temporary_database,
            temporary_public_json,
            database,
            public_json,
        )
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)
    return BuildOutputs(database, public_json, record_counts)


def _validate_build_timestamp(value: str) -> None:
    """Reject non-UTC timestamps before validation or output-directory mutation."""
    try:
        if "T" not in value:
            raise ValueError
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError(
            "build_timestamp must be an ISO-8601 UTC timestamp "
            "(for example, 2026-09-03T00:00:00Z)."
        ) from None


def _publish_output_pair(
    temporary_database: Path,
    temporary_public_json: Path,
    database: Path,
    public_json: Path,
) -> None:
    """Publish both artefacts or restore the exact prior pair after replacement failure."""
    backups = (
        (database, temporary_database.with_name("previous-database.sqlite")),
        (public_json, temporary_public_json.with_name("previous-public-data.json")),
    )
    existing = {destination: destination.exists() for destination, _ in backups}
    for destination, backup in backups:
        if existing[destination]:
            shutil.copyfile(destination, backup)

    try:
        os.replace(temporary_database, database)
        os.replace(temporary_public_json, public_json)
    except Exception:
        _restore_output_pair(backups, existing)
        raise


def _restore_output_pair(
    backups: tuple[tuple[Path, Path], ...], existing: dict[Path, bool]
) -> None:
    """Best-effort restoration that preserves the publication exception for the caller."""
    for destination, backup in backups:
        try:
            if existing[destination]:
                os.replace(backup, destination)
            elif destination.exists():
                destination.unlink()
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    """Run the project build and print machine-readable-friendly output locations."""
    parser = argparse.ArgumentParser(description="Build the EU AI Policy Observatory data artefacts.")
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument("--timestamp", required=True, help="ISO-8601 build timestamp passed to public JSON.")
    arguments = parser.parse_args(argv)
    try:
        outputs = run_pipeline(arguments.project_root, arguments.timestamp)
    except RecordValidationError as error:
        for issue in error.issues:
            print(
                f"{issue.record_path}: {issue.field}: [{issue.code}] {issue.message}",
                file=sys.stderr,
            )
        return 1
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"database: {outputs.database}")
    print(f"public_json: {outputs.public_json}")
    print("record_counts: " + ", ".join(
        f"{name}={count}" for name, count in sorted(outputs.record_counts.items())
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
