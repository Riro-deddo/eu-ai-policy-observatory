"""Deterministic loading for canonical Observatory records."""

from dataclasses import dataclass
import json
from pathlib import Path

from observatory.types import ENTITY_DIRECTORIES


@dataclass(frozen=True, slots=True)
class LoadedRecord:
    """A decoded record together with its canonical source path."""

    data: dict[str, object]
    path: Path
    syntax_error: str | None = None


def load_records(data_root: Path) -> dict[str, list[LoadedRecord]]:
    """Load non-symlinked JSON records in stable entity and path order."""
    records: dict[str, list[LoadedRecord]] = {}
    for directory in ENTITY_DIRECTORIES:
        entity_root = data_root / directory
        if not entity_root.is_dir() or entity_root.is_symlink():
            records[directory] = []
            continue

        paths = sorted(
            (path for path in entity_root.glob("*.json") if not path.is_symlink()),
            key=lambda path: path.as_posix(),
        )
        records[directory] = [_load_record(path) for path in paths]
    return records


def _load_record(path: Path) -> LoadedRecord:
    try:
        return LoadedRecord(json.loads(path.read_text(encoding="utf-8")), path)
    except json.JSONDecodeError as error:
        return LoadedRecord(
            {},
            path,
            f"Invalid JSON syntax: {error.msg} (line {error.lineno}, column {error.colno}).",
        )
