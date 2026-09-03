import sqlite3
from pathlib import Path

import pytest

from observatory.build_db import build_database
from observatory.io import load_records


def test_build_database_normalises_document_links(tmp_path):
    output = tmp_path / "observatory.sqlite"
    build_database(
        load_records(Path("tests/fixtures/valid/data")),
        Path("schema/database.sql"),
        output,
    )
    with sqlite3.connect(output) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert connection.execute("SELECT COUNT(*) FROM documents").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM policy_documents").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM document_concepts").fetchone() == (1,)
        assert connection.execute("SELECT COUNT(*) FROM document_sources").fetchone() == (1,)


def test_schema_rejects_an_impossible_iso_calendar_date():
    connection = sqlite3.connect(":memory:")
    connection.executescript(Path("schema/database.sql").read_text(encoding="utf-8"))

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute(
            "INSERT INTO documents "
            "(id, publication_status, created_at, updated_at, slug, official_title, short_title, "
            "document_type, publication_date, legal_status, language) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "invalid-date-document",
                "draft",
                "2026-09-03T12:00:00Z",
                "2026-09-03T12:00:00Z",
                "invalid-date-document",
                "Invalid date document",
                "Invalid date",
                "communication",
                "2026-02-29",
                "non_binding",
                "en",
            ),
        )
