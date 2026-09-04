"""Reject CJK ideographs in Git-tracked text intended for the English repository."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


CJK_RANGES = (
    (0x3400, 0x4DBF),
    (0x4E00, 0x9FFF),
    (0xF900, 0xFAFF),
)


def _is_cjk_ideograph(character: str) -> bool:
    codepoint = ord(character)
    return any(start <= codepoint <= end for start, end in CJK_RANGES)


def _tracked_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [Path(value.decode("utf-8")) for value in result.stdout.split(b"\0") if value]


def find_cjk_in_tracked_files(root: Path) -> list[str]:
    """Return stable locations for lines containing CJK ideographs in tracked text."""
    repository = Path(root).resolve()
    findings: list[str] = []
    for relative_path in _tracked_paths(repository):
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
        for line_number, line in enumerate(text.splitlines(), start=1):
            for column, character in enumerate(line, start=1):
                if _is_cjk_ideograph(character):
                    findings.append(
                        f"{relative_path.as_posix()}:{line_number}:{column}: "
                        f"U+{ord(character):04X}"
                    )
                    break
    return sorted(findings)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Git-tracked text for CJK ideographs in this English repository."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    arguments = parser.parse_args(argv)
    try:
        findings = find_cjk_in_tracked_files(arguments.root)
    except subprocess.CalledProcessError as error:
        print(f"Unable to list Git-tracked files: {error}", file=sys.stderr)
        return 2
    if findings:
        print("CJK ideographs found in Git-tracked text:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Repository English guard passed: no CJK ideographs in tracked text.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
