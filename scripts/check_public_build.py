"""Check that generated public output contains only safe, published material."""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import stat
import sys
from pathlib import Path
from typing import Any, Iterable


_WINDOWS_USER_PATH = re.compile(
    r"(?:[A-Za-z]:\\+Users\\+|\\\\Users\\+)", re.IGNORECASE
)
_UNIX_USER_PATH = re.compile(r"\\?/(?:Users|home)\\?/", re.IGNORECASE)
_HTTPS_URL_PREFIX = re.compile(r"https?:\\*/\\*/[^\s\"'<>]*$", re.IGNORECASE)
_URL_TOKEN_BOUNDARY = re.compile(r'''[\s"'<>()\[\]{};,]''')
_LOCALHOST = re.compile(r"\blocalhost\b", re.IGNORECASE)
_TOKEN_PREFIX = re.compile(
    r"(?:gh[oprsu]_|github_pat_|glpat-|(?<![A-Za-z0-9])sk-|AKIA|xox[abprs]-)"
)
_PRIVATE_KEY_HEADER = re.compile(
    r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----", re.IGNORECASE
)
_UNSUPPORTED_COVERAGE = re.compile(
    r"\bComprehensive\s+within\s+the\s+documented\s+inclusion\s+boundary\b",
    re.IGNORECASE,
)


def check_public_build(
    site_root: Path, public_data_path: Path, require_database: bool = False
) -> list[str]:
    """Return sorted errors for unsafe static output or unpublished public data."""

    errors = [* _scan_site(site_root), * _scan_public_data(public_data_path)]
    if require_database:
        errors.extend(_scan_downloadable_database(site_root))
    return sorted(errors)


def _scan_site(site_root: Path) -> list[str]:
    if not site_root.is_dir():
        return [f"site root is missing or unreadable: {site_root}"]

    errors: list[str] = []
    walk_errors: list[OSError] = []
    paths = sorted(
        (
            Path(directory) / filename
            for directory, _, files in os.walk(site_root, onerror=walk_errors.append)
            for filename in files
        ),
        key=lambda path: path.as_posix(),
    )
    errors.extend(f"site root is unreadable: {site_root} ({exc})" for exc in walk_errors)

    for path in paths:
        try:
            content = path.read_bytes()
        except OSError as exc:
            errors.append(f"site file is unreadable: {path} ({exc})")
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            if _looks_binary(content):
                continue
            errors.append(f"site file has a UTF-8 decoding error: {path} ({exc})")
            continue
        errors.extend(_text_errors(path, text))
    return errors


def _looks_binary(content: bytes) -> bool:
    """Recognise undecodable binary bytes without trusting a filename extension."""
    return b"\x00" in content or content.startswith(
        (b"\x89PNG\r\n\x1a\n", b"GIF87a", b"GIF89a", b"\xff\xd8\xff", b"%PDF-")
    )


def _contains_unix_user_path(text: str) -> bool:
    """Distinguish local user paths from ordinary path segments in HTTPS URLs."""
    for match in _UNIX_USER_PATH.finditer(text):
        token_start = max(
            (boundary.end() for boundary in _URL_TOKEN_BOUNDARY.finditer(text, 0, match.start())),
            default=0,
        )
        url_prefix = _HTTPS_URL_PREFIX.fullmatch(text[token_start : match.start()])
        if url_prefix is not None and not any(
            marker in url_prefix.group() for marker in "?#"
        ):
            continue
        return True
    return False


def _text_errors(path: Path, text: str) -> Iterable[str]:
    if _WINDOWS_USER_PATH.search(text) or _contains_unix_user_path(text):
        yield f"local filesystem path found in public output: {path}"
    if _LOCALHOST.search(text):
        yield f"localhost reference found in public output: {path}"
    if _TOKEN_PREFIX.search(text):
        yield f"credential or token prefix found in public output: {path}"
    if _PRIVATE_KEY_HEADER.search(text):
        yield f"private-key header found in public output: {path}"
    if _UNSUPPORTED_COVERAGE.search(text):
        yield f"unsupported corpus-completeness claim found in public output: {path}"


def _scan_public_data(public_data_path: Path) -> list[str]:
    try:
        text = public_data_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"public data file is missing: {public_data_path}"]
    except UnicodeDecodeError as exc:
        return [f"public data file has a UTF-8 decoding error: {public_data_path} ({exc})"]
    except OSError as exc:
        return [f"public data file is unreadable: {public_data_path} ({exc})"]

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"public data file contains invalid JSON: {public_data_path} ({exc})"]

    return [*_publication_errors(payload, "$"), *_text_errors(public_data_path, text)]


def _scan_downloadable_database(site_root: Path) -> list[str]:
    """Validate the required downloadable SQLite database without modifying it."""
    database_path = site_root / "downloads" / "eu-ai-policy-observatory.sqlite"
    try:
        database_stat = database_path.lstat()
    except FileNotFoundError:
        return [f"downloadable SQLite database is missing: {database_path}"]
    except OSError:
        return [f"downloadable SQLite database is unreadable: {database_path}"]

    if not stat.S_ISREG(database_stat.st_mode):
        return [f"downloadable SQLite database is not a regular file: {database_path}"]
    if database_stat.st_size == 0:
        return [f"downloadable SQLite database is empty: {database_path}"]

    try:
        with database_path.open("rb") as database_file:
            if database_file.read(16) != b"SQLite format 3\x00":
                return [f"downloadable SQLite database is not a SQLite database: {database_path}"]
    except OSError:
        return [f"downloadable SQLite database is unreadable: {database_path}"]

    connection: sqlite3.Connection | None = None
    try:
        database_uri = f"{database_path.resolve().as_uri()}?mode=ro"
        connection = sqlite3.connect(database_uri, uri=True)
        integrity_rows = connection.execute("PRAGMA integrity_check").fetchall()
        if integrity_rows != [("ok",)]:
            return [f"downloadable SQLite database failed integrity check: {database_path}"]
        return _database_publication_errors(connection, database_path)
    except (OSError, sqlite3.Error):
        return [
            f"downloadable SQLite database is corrupt or unreadable: {database_path}"
        ]
    finally:
        if connection is not None:
            connection.close()



def _database_publication_errors(
    connection: sqlite3.Connection, database_path: Path
) -> list[str]:
    """Return deterministic errors for non-published rows in public SQLite tables."""
    try:
        tables = [
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]
        errors: list[str] = []
        for table in tables:
            quoted_table = _quote_sql_identifier(table)
            columns = {
                row[1]
                for row in connection.execute(f"PRAGMA table_info({quoted_table})")
            }
            if "publication_status" not in columns:
                continue
            if "id" in columns:
                rows = connection.execute(
                    f"SELECT id, publication_status FROM {quoted_table} "
                    "WHERE publication_status IS NULL OR publication_status != ? ORDER BY id",
                    ("published",),
                )
                errors.extend(
                    "non-published row in downloadable SQLite database: "
                    f"{table}/{identifier} ({status!r})"
                    for identifier, status in rows
                )
            else:
                rows = connection.execute(
                    f"SELECT publication_status FROM {quoted_table} "
                    "WHERE publication_status IS NULL OR publication_status != ? "
                    "ORDER BY publication_status",
                    ("published",),
                )
                errors.extend(
                    "non-published row in downloadable SQLite database: "
                    f"{table} ({status!r})"
                    for (status,) in rows
                )
        return errors
    except sqlite3.Error:
        return [
            f"downloadable SQLite database schema is unreadable: {database_path}"
        ]


def _quote_sql_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _publication_errors(value: Any, location: str) -> Iterable[str]:
    if isinstance(value, dict):
        if "publication_status" in value and value["publication_status"] != "published":
            yield (
                f"non-published record at {location}: publication_status is "
                f"{value['publication_status']!r}"
            )
        for key in sorted(value):
            yield from _publication_errors(value[key], f"{location}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _publication_errors(item, f"{location}[{index}]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", required=True, type=Path, help="Static site output directory")
    parser.add_argument("--data", required=True, type=Path, help="Public JSON data file")
    parser.add_argument(
        "--require-database",
        action="store_true",
        help="Require a valid downloadable SQLite database in the static site output",
    )
    args = parser.parse_args(argv)

    errors = check_public_build(args.site, args.data, args.require_database)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
