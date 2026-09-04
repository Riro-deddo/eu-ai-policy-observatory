from base64 import b64decode
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_public_build import check_public_build


def write_public_data(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_scanner_rejects_local_paths_and_non_published_payloads(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(r"C:\\Users\\Researcher\\secret", encoding="utf-8")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": [{"publication_status": "draft"}]})

    errors = check_public_build(site, data)

    assert any("local filesystem path" in error for error in errors)
    assert any("non-published record" in error for error in errors)


def test_scanner_rejects_ordinary_and_escaped_windows_user_paths(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "ordinary.txt").write_text(
        r"c:\Users\Researcher\secret", encoding="utf-8"
    )
    (site / "escaped.txt").write_text(
        r"Z:\\Users\\Researcher\\secret", encoding="utf-8"
    )
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("ordinary.txt" in error for error in errors)
    assert any("escaped.txt" in error for error in errors)


def test_scanner_rejects_common_private_key_headers(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    headers = {
        "private.pem": "-----BEGIN PRIVATE KEY-----",
        "rsa.pem": "-----BEGIN RSA PRIVATE KEY-----",
        "ec.pem": "-----BEGIN EC PRIVATE KEY-----",
        "openssh.pem": "-----BEGIN OPENSSH PRIVATE KEY-----",
        "pgp.asc": "-----BEGIN PGP PRIVATE KEY BLOCK-----",
    }
    for filename, header in headers.items():
        (site / filename).write_text(header, encoding="utf-8")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    for filename in headers:
        assert any(filename in error for error in errors)


def test_scanner_checks_each_public_text_boundary(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "leaks.txt").write_text(
        "\n".join(
            [
                "/Users/researcher/private",
                "/home/researcher/private",
                "http://localhost:3000",
                "ghp_exampletoken",
                "-----BEGIN PRIVATE KEY-----",
            ]
        ),
        encoding="utf-8",
    )
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("local filesystem path" in error for error in errors)
    assert any("localhost" in error for error in errors)
    assert any("credential or token" in error for error in errors)
    assert any("private-key header" in error for error in errors)
    assert errors == sorted(errors)


def test_scanner_inspects_utf8_text_disguised_as_a_png(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "leak.png").write_text(
        r"C:\Users\Researcher\secret\nghp_exampletoken", encoding="utf-8"
    )
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("local filesystem path" in error and "leak.png" in error for error in errors)
    assert any("credential or token" in error and "leak.png" in error for error in errors)


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("fake.gif", b"GIF89aghp_exampletoken"),
        ("fake.pdf", b"%PDF-ghp_exampletoken"),
        ("nul.txt", b"\x00ghp_exampletoken"),
    ],
)
def test_scanner_inspects_valid_utf8_text_with_binary_markers(
    tmp_path: Path, filename: str, content: bytes
):
    site = tmp_path / "site"
    site.mkdir()
    (site / filename).write_bytes(content)
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("credential or token" in error and filename in error for error in errors)


@pytest.mark.parametrize("token_prefix", ["ghp_", "gho_", "ghu_", "ghs_", "ghr_"])
def test_scanner_rejects_common_github_token_prefixes(
    tmp_path: Path, token_prefix: str
):
    site = tmp_path / "site"
    site.mkdir()
    filename = f"{token_prefix[:-1]}.txt"
    (site / filename).write_text(f"{token_prefix}exampletoken", encoding="utf-8")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("credential or token" in error and filename in error for error in errors)


def test_scanner_reports_every_non_published_record_without_rejecting_methodology_prose(
    tmp_path: Path,
):
    site = tmp_path / "site"
    site.mkdir()
    (site / "methodology.html").write_text(
        "Draft records and pending_review records are excluded from the corpus.",
        encoding="utf-8",
    )
    data = tmp_path / "public-data.json"
    write_public_data(
        data,
        {
            "documents": [
                {"id": "draft-document", "publication_status": "draft"},
                {"id": "published-document", "publication_status": "published"},
            ],
            "nested": {"publication_status": "pending_review"},
        },
    )

    errors = check_public_build(site, data)

    non_published = [error for error in errors if "non-published record" in error]
    assert len(non_published) == 2
    assert all("methodology" not in error for error in errors)


def test_scanner_reports_invalid_and_missing_inputs_without_crashing(tmp_path: Path):
    missing_site = tmp_path / "missing-site"
    invalid_data = tmp_path / "public-data.json"
    invalid_data.write_text("{", encoding="utf-8")

    errors = check_public_build(missing_site, invalid_data)

    assert any("site root" in error for error in errors)
    assert any("invalid JSON" in error for error in errors)


def test_scanner_reports_text_decoding_errors_and_ignores_real_binary_png(
    tmp_path: Path,
):
    site = tmp_path / "site"
    site.mkdir()
    (site / "invalid.txt").write_bytes(b"\xff\xfe")
    (site / "image.png").write_bytes(
        b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB"
            "9Wl0mAAAAABJRU5ErkJggg=="
        )
    )
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("UTF-8 decoding" in error for error in errors)
    assert not any("image.png" in error for error in errors)


def test_scanner_cli_returns_nonzero_when_public_output_is_unsafe(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("localhost", encoding="utf-8")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_public_build.py",
            "--site",
            str(site),
            "--data",
            str(data),
        ],
        cwd=Path(__file__).parents[1],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "localhost" in result.stdout
