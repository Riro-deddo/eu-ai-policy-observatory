"""Reject non-Latin-script letters in Git-tracked text and path names."""

from __future__ import annotations

import argparse
from collections.abc import Iterator
import json
from pathlib import Path
import subprocess
import sys
from typing import Any
import unicodedata


def _tracked_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [Path(value.decode("utf-8")) for value in result.stdout.split(b"\0") if value]


def _unicode_characters(text: str) -> Iterator[str]:
    """Yield scalar characters, combining any decoded UTF-16 surrogate pair."""
    index = 0
    while index < len(text):
        codepoint = ord(text[index])
        if 0xD800 <= codepoint <= 0xDBFF and index + 1 < len(text):
            low = ord(text[index + 1])
            if 0xDC00 <= low <= 0xDFFF:
                yield chr(0x10000 + ((codepoint - 0xD800) << 10) + low - 0xDC00)
                index += 2
                continue
        yield text[index]
        index += 1


def _is_non_latin_script_letter(character: str) -> bool:
    if not unicodedata.category(character).startswith("L"):
        return False
    return "LATIN" not in unicodedata.name(character, "")


def _finding(path: Path, location: str, character: str) -> str:
    name = unicodedata.name(character, "UNNAMED LETTER")
    return f"{path.as_posix()}: {location}: U+{ord(character):04X} ({name})"


def _text_findings(path: Path, text: str) -> list[str]:
    findings: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        column = 0
        for character in _unicode_characters(line):
            column += 1
            if _is_non_latin_script_letter(character):
                findings.append(_finding(path, f"line {line_number}, column {column}", character))
                break
    return findings


def _json_strings(value: Any, location: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(value, str):
        yield location, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _json_strings(item, f"{location}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield f"{location}.<key>", str(key)
            yield from _json_strings(item, f"{location}.{key}")


def _json_findings(path: Path, text: str) -> list[str]:
    try:
        value = json.loads(text)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []
    findings: list[str] = []
    for location, string in _json_strings(value):
        for character in _unicode_characters(string):
            if _is_non_latin_script_letter(character):
                findings.append(_finding(path, f"JSON string at {location}", character))
                break
    return findings


def find_non_latin_script_in_tracked_files(root: Path) -> list[str]:
    """Return stable locations for non-Latin-script letters in tracked text or paths."""
    repository = Path(root).resolve()
    findings: list[str] = []
    for relative_path in _tracked_paths(repository):
        for character in _unicode_characters(relative_path.as_posix()):
            if _is_non_latin_script_letter(character):
                findings.append(_finding(relative_path, "tracked path", character))
                break

        path = repository / relative_path
        if not path.is_file():
            continue
        content = path.read_bytes()
        if b"\0" in content:
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(_text_findings(relative_path, text))
        if relative_path.suffix.lower() == ".json":
            findings.extend(_json_findings(relative_path, text))
    return sorted(set(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check Git-tracked text and path names for non-Latin-script letters. "
            "Manual review remains necessary to confirm that Latin-script copy is English."
        )
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    arguments = parser.parse_args(argv)
    try:
        findings = find_non_latin_script_in_tracked_files(arguments.root)
    except subprocess.CalledProcessError as error:
        print(f"Unable to list Git-tracked files: {error}", file=sys.stderr)
        return 2
    if findings:
        print("Non-Latin-script letters found in Git-tracked text or path names:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(
        "Repository script guard passed: no non-Latin-script letters in tracked text "
        "or path names. Manual English copy review is still required."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
