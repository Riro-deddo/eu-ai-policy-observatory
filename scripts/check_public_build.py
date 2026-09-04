"""Check that generated public output contains only safe, published material."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable


_WINDOWS_USER_PATH = re.compile(
    r"(?:[A-Za-z]:\\+Users\\+|\\\\Users\\+)", re.IGNORECASE
)
_UNIX_USER_PATH = re.compile(r"/(?:Users|home)/", re.IGNORECASE)
_LOCALHOST = re.compile(r"\blocalhost\b", re.IGNORECASE)
_TOKEN_PREFIX = re.compile(r"(?:ghp_|github_pat_|glpat-|sk-|AKIA|xox[abprs]-)")
_PRIVATE_KEY_HEADER = re.compile(
    r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY(?: BLOCK)?-----", re.IGNORECASE
)
_BINARY_SUFFIXES = {
    ".avif",
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".sqlite",
    ".svgz",
    ".webp",
    ".woff",
    ".woff2",
}


def check_public_build(site_root: Path, public_data_path: Path) -> list[str]:
    """Return sorted errors for unsafe static output or unpublished public data."""

    errors = [* _scan_site(site_root), * _scan_public_data(public_data_path)]
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
        if path.suffix.lower() in _BINARY_SUFFIXES:
            continue
        try:
            content = path.read_bytes()
        except OSError as exc:
            errors.append(f"site file is unreadable: {path} ({exc})")
            continue
        if _looks_binary(content):
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"site file has a UTF-8 decoding error: {path} ({exc})")
            continue
        errors.extend(_text_errors(path, text))
    return errors


def _looks_binary(content: bytes) -> bool:
    return b"\x00" in content or content.startswith(
        (b"\x89PNG\r\n\x1a\n", b"GIF87a", b"GIF89a", b"\xff\xd8\xff", b"%PDF-")
    )


def _text_errors(path: Path, text: str) -> Iterable[str]:
    if _WINDOWS_USER_PATH.search(text) or _UNIX_USER_PATH.search(text):
        yield f"local filesystem path found in public output: {path}"
    if _LOCALHOST.search(text):
        yield f"localhost reference found in public output: {path}"
    if _TOKEN_PREFIX.search(text):
        yield f"credential or token prefix found in public output: {path}"
    if _PRIVATE_KEY_HEADER.search(text):
        yield f"private-key header found in public output: {path}"


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

    return list(_publication_errors(payload, "$"))


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
    args = parser.parse_args(argv)

    errors = check_public_build(args.site, args.data)
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
