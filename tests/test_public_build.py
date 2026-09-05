from base64 import b64decode
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.check_public_build import check_public_build
from scripts.check_repository_english import find_non_latin_script_in_tracked_files


PROJECT_ROOT = Path(__file__).parents[1]


def write_public_data(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_public_coverage_copy_uses_generated_values_and_rejects_seed_scope():
    payload = json.loads(
        (PROJECT_ROOT / "generated" / "public-data.json").read_text(encoding="utf-8")
    )
    coverage = payload["coverage"]
    documents = payload["documents"]
    home = (PROJECT_ROOT / "web" / "src" / "pages" / "index.astro").read_text(
        encoding="utf-8"
    )
    methodology = (
        PROJECT_ROOT / "web" / "src" / "pages" / "methodology.astro"
    ).read_text(encoding="utf-8")
    about = (PROJECT_ROOT / "web" / "src" / "pages" / "about.astro").read_text(
        encoding="utf-8"
    )
    pathway = (
        PROJECT_ROOT / "web" / "src" / "components" / "PolicyPathway.astro"
    ).read_text(encoding="utf-8")
    public_copy = "\n".join((home, methodology, about, pathway))

    assert coverage["principal_documents"] == sum(
        document["record_level"] == "principal" for document in documents
    )
    assert coverage["supporting_files_and_versions"] == sum(
        document["record_level"] != "principal" for document in documents
    )
    assert "coverage={data.coverage}" in home
    assert "{coverage.principal_documents}" in pathway
    assert "{coverage.supporting_files_and_versions}" in pathway
    assert "{coverage.last_verified_date}" in pathway
    assert "Pending-review records are excluded from public totals." in pathway
    assert "2018–2024" not in public_copy
    assert "seven reviewed, published documents" not in public_copy


def test_public_documents_expose_classifications_and_exact_coverage_cutoff():
    payload = json.loads(
        (PROJECT_ROOT / "generated" / "public-data.json").read_text(encoding="utf-8")
    )

    assert payload["coverage"]["coverage_cutoff"] == "2026-09-04"
    assert payload["documents"]
    for document in payload["documents"]:
        assert document["sector_tags"]
        assert document["provenance_tags"]
        assert "third_party_submission" not in document["provenance_tags"]
        assert "unknown_pending_review" not in document["provenance_tags"]


def test_contributor_dictionary_documents_expanded_corpus_contract():
    dictionary = (PROJECT_ROOT / "docs" / "data-dictionary.md").read_text(
        encoding="utf-8"
    )
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    documented_contract = f"{dictionary}\n{readme}"

    for field in (
        "record_level",
        "official_reference",
        "procedure_references",
        "oj_reference",
        "document_date",
        "version_label",
        "version_status",
    ):
        assert f"`{field}`" in dictionary

    for decision in ("included", "merged", "excluded", "pending"):
        assert f"`{decision}`" in documented_contract

    assert "duplicate document identity" in documented_contract.lower()
    assert "research/corpus-inventory.json" in documented_contract
    assert "research/source-sweep.json" in documented_contract
    assert "observatory-build --project-root ." in documented_contract
    assert "--require-database" in documented_contract
    assert "official" in documented_contract.lower()


def test_contributor_documentation_defines_stage_one_coverage_contract():
    dictionary = (PROJECT_ROOT / "docs" / "data-dictionary.md").read_text(
        encoding="utf-8"
    )
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    vocabularies = json.loads(
        (PROJECT_ROOT / "schema" / "controlled-vocabularies.json").read_text(
            encoding="utf-8"
        )
    )

    for value in (*vocabularies["sector_tag"], *vocabularies["provenance_tag"]):
        assert f"`{value}`" in dictionary
    for value in ("third_party_submission", "unknown_pending_review"):
        assert f"`{value}`" in dictionary
        assert "inventory-only" in dictionary
    for field in ("publication_status", "version_status", "legal_status"):
        assert f"`{field}`" in dictionary
    for status in (
        "not_started",
        "in_progress",
        "reviewed",
        "gap_found",
        "recheck_due",
    ):
        assert f"`{status}`" in dictionary
    assert "empty `covered_document_types`" in dictionary
    assert "empty `covered_sector_tags`" in dictionary
    assert "formal publication" in dictionary.lower()
    assert "principal" in dictionary and "all records" in dictionary.lower()
    assert "Stage 1" in readme and "Stage 2" in readme and "Stage 3" in readme
    assert "schema and interface" in readme.lower()
    assert (
        "Comprehensive within the documented inclusion boundary, "
        "verified through 4 September 2026."
    ) in readme


def test_repository_english_guard_rejects_non_latin_scripts_and_escaped_json(
    tmp_path: Path,
):
    repository = tmp_path / "repository"
    repository.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
    tracked_files = {
        "README.md": "English copy with José.\n",
        "kana.md": f"English then {chr(0x3042)}.\n",
        "hangul.md": f"English then {chr(0xD55C)}.\n",
        "cyrillic.md": f"English then {chr(0x0416)}.\n",
        "arabic.md": f"English then {chr(0x0639)}.\n",
        "greek.md": f"English then {chr(0x03A9)}.\n",
        "astral-han.md": f"English then {chr(0x20000)}.\n",
        "escaped.json": json.dumps({"title": chr(0x4E2D)}, ensure_ascii=True),
        "escaped-astral.json": json.dumps({"title": chr(0x20000)}, ensure_ascii=True),
    }
    for filename, contents in tracked_files.items():
        (repository / filename).write_text(contents, encoding="utf-8")
    non_latin_filename = f"report-{chr(0x0434)}.md"
    (repository / non_latin_filename).write_text("English body.\n", encoding="utf-8")
    (repository / "scratch.md").write_text(
        f"Untracked {chr(0x4E2D)}.\n", encoding="utf-8"
    )
    subprocess.run(
        ["git", "add", *tracked_files, non_latin_filename], cwd=repository, check=True
    )

    findings = find_non_latin_script_in_tracked_files(repository)

    for codepoint in (
        "U+3042",
        "U+D55C",
        "U+0416",
        "U+0639",
        "U+03A9",
        "U+20000",
        "U+4E2D",
        "U+0434",
    ):
        assert any(codepoint in finding for finding in findings)
    assert not any("README.md" in finding for finding in findings)
    assert not any("scratch.md" in finding for finding in findings)
    assert any("tracked path" in finding for finding in findings)
    assert any("escaped.json" in finding and "JSON string" in finding for finding in findings)
    assert any(
        "escaped-astral.json" in finding and "U+20000" in finding
        for finding in findings
    )


def test_actual_repository_passes_non_latin_script_guard():
    assert find_non_latin_script_in_tracked_files(PROJECT_ROOT) == []


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


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("users-literal.txt", "/Users/Researcher/secret"),
        ("home-literal.txt", "/home/name/secret"),
        ("users-escaped.txt", r"\/Users\/Researcher\/secret"),
        ("home-escaped.txt", r"\/home\/name\/secret"),
    ],
)
def test_scanner_rejects_literal_and_escaped_unix_user_paths(
    tmp_path: Path, filename: str, content: str
):
    site = tmp_path / "site"
    site.mkdir()
    (site / filename).write_text(content, encoding="utf-8")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data)

    assert any("local filesystem path" in error and filename in error for error in errors)


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


def test_scanner_does_not_treat_high_risk_hyphenation_as_a_token(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(
        "Draft high-risk-classification guidelines",
        encoding="utf-8",
    )
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    assert check_public_build(site, data) == []


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


def test_scanner_requires_downloadable_database(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data, require_database=True)

    assert any("downloadable SQLite database" in error for error in errors)


def test_scanner_accepts_valid_downloadable_database(tmp_path: Path):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE documents (id TEXT PRIMARY KEY)")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})
    original_bytes = database.read_bytes()

    assert check_public_build(site, data, require_database=True) == []
    assert database.read_bytes() == original_bytes


def test_scanner_rejects_downloadable_database_with_non_published_entity_row(
    tmp_path: Path,
):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE documents (id TEXT PRIMARY KEY, publication_status TEXT NOT NULL)"
        )
        connection.execute("INSERT INTO documents VALUES ('draft-document', 'draft')")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data, require_database=True)

    assert any(
        "non-published row in downloadable SQLite database: documents/draft-document"
        in error
        for error in errors
    )


def test_scanner_reports_draft_rows_in_hostile_table_names(tmp_path: Path):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute(
            'CREATE TABLE "draft records""; --" '
            "(id TEXT PRIMARY KEY, publication_status TEXT NOT NULL)"
        )
        connection.execute(
            'INSERT INTO "draft records""; --" VALUES (?, ?)',
            ("draft-row", "draft"),
        )
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data, require_database=True)

    assert errors == [
        "non-published row in downloadable SQLite database: "
        "draft records\"; --/draft-row ('draft')"
    ]


def test_scanner_accepts_downloadable_database_with_only_published_entity_rows(
    tmp_path: Path,
):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE documents (id TEXT PRIMARY KEY, publication_status TEXT NOT NULL)"
        )
        connection.execute("INSERT INTO documents VALUES ('published-document', 'published')")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    assert check_public_build(site, data, require_database=True) == []


def test_scanner_rejects_directory_at_downloadable_database_path(tmp_path: Path):
    site = tmp_path / "site"
    database = site / "downloads" / "eu-ai-policy-observatory.sqlite"
    database.mkdir(parents=True)
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data, require_database=True)

    assert any("downloadable SQLite database is not a regular file" in error for error in errors)


@pytest.mark.skipif(
    os.name == "nt",
    reason="Windows ACL semantics cannot reliably make a test-owned file unreadable with chmod.",
)
def test_scanner_rejects_genuinely_unreadable_downloadable_database(tmp_path: Path):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE documents (id TEXT PRIMARY KEY)")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})
    original_mode = database.stat().st_mode
    database.chmod(0)
    try:
        if os.access(database, os.R_OK):
            pytest.skip("The test process retains read access after chmod(0).")
        errors = check_public_build(site, data, require_database=True)
    finally:
        database.chmod(original_mode)

    assert any("downloadable SQLite database is unreadable" in error for error in errors)


@pytest.mark.skipif(
    os.name != "nt",
    reason="Windows-only fallback for ACL environments where chmod cannot prove unreadability.",
)
def test_scanner_reports_windows_database_access_denial(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE documents (id TEXT PRIMARY KEY)")
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})
    path_open = Path.open

    def deny_database_read(path: Path, *args: object, **kwargs: object):
        if path == database:
            raise PermissionError("test access denial")
        return path_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_database_read)

    errors = check_public_build(site, data, require_database=True)

    assert any("downloadable SQLite database is unreadable" in error for error in errors)


@pytest.mark.parametrize(
    ("contents", "expected_error"),
    [
        (b"", "is empty"),
        (b"this is not a SQLite database", "is not a SQLite database"),
    ],
)
def test_scanner_rejects_empty_or_non_sqlite_downloadable_database(
    tmp_path: Path, contents: bytes, expected_error: str
):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    (downloads / "eu-ai-policy-observatory.sqlite").write_bytes(contents)
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data, require_database=True)

    assert any(expected_error in error for error in errors)


def test_scanner_rejects_downloadable_database_that_fails_integrity_check(
    tmp_path: Path,
):
    site = tmp_path / "site"
    downloads = site / "downloads"
    downloads.mkdir(parents=True)
    database = downloads / "eu-ai-policy-observatory.sqlite"
    with sqlite3.connect(database) as connection:
        connection.execute("CREATE TABLE documents (id TEXT PRIMARY KEY)")
        connection.execute("INSERT INTO documents VALUES ('first')")
    with database.open("r+b") as database_file:
        database_file.seek(36)
        database_file.write((1).to_bytes(4, "big"))
    data = tmp_path / "public-data.json"
    write_public_data(data, {"documents": []})

    errors = check_public_build(site, data, require_database=True)

    assert any("failed integrity check" in error for error in errors)
