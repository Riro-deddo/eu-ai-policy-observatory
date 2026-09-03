"""End-to-end, atomic build of canonical Observatory data."""

from dataclasses import dataclass
import argparse
import os
from pathlib import Path
import shutil
import sys
import tempfile

from observatory.build_db import build_database
from observatory.export_public import export_public
from observatory.io import load_records
from observatory.validate import RecordValidationError, assert_valid


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
    root = Path(project_root).resolve()
    data_root = root / "data"
    schema_root = root / "schema"
    destination = Path(output_root) if output_root is not None else root / "generated"

    # Validation is deliberately first: a failed validation never changes existing outputs.
    assert_valid(data_root, schema_root / "record.schema.json", schema_root / "controlled-vocabularies.json")
    records = load_records(data_root)
    record_counts = {directory: len(entries) for directory, entries in records.items()}

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(tempfile.mkdtemp(prefix=".observatory-build-", dir=destination.parent))
    temporary_database = temporary_root / DATABASE_FILENAME
    temporary_public_json = temporary_root / PUBLIC_JSON_FILENAME
    database = destination / DATABASE_FILENAME
    public_json = destination / PUBLIC_JSON_FILENAME
    try:
        build_database(records, schema_root / "database.sql", temporary_database)
        export_public(temporary_database, temporary_public_json, build_timestamp)
        destination.mkdir(parents=True, exist_ok=True)
        os.replace(temporary_database, database)
        os.replace(temporary_public_json, public_json)
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)
    return BuildOutputs(database, public_json, record_counts)


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
    print(f"database: {outputs.database}")
    print(f"public_json: {outputs.public_json}")
    print("record_counts: " + ", ".join(
        f"{name}={count}" for name, count in sorted(outputs.record_counts.items())
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
