import json
from pathlib import Path
import shutil
import sqlite3

from observatory.historical_publication import validate_historical_publication
from observatory.io import load_records
from observatory.pipeline import run_pipeline


def test_historical_batch_round_trips_without_losing_old_routes(tmp_path):
    outputs = run_pipeline(
        Path.cwd(),
        "2026-09-05T12:00:00Z",
        output_root=tmp_path,
    )
    payload = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    docs = {row["id"]: row for row in payload["documents"]}
    baseline = json.loads(
        Path("research/migrations/2026-09-05-public-document-baseline.json").read_text(
            encoding="utf-8"
        )
    )

    assert all(docs[row["id"]]["slug"] == row["slug"] for row in baseline["documents"])
    esprit = docs["council-decision-84-130-eec-esprit"]
    assert esprit["document_date"] == "1984-02-28"
    assert esprit["temporal_collection"] == "historical_lineage"
    assert esprit["relevance_class"] == "ai_related_precursor"
    assert esprit["date_evidence"]["publication_date"]["locator"]
    robotics = docs["civil-law-rules-on-robotics-resolution-2017"]
    assert robotics["document_date"] == "2017-02-16"
    assert robotics["publication_date"] == "2018-07-18"
    assert robotics["temporal_collection"] == "historical_lineage"
    assert sum(row["celex"] == "52017IP0051" for row in docs.values()) == 1
    with sqlite3.connect(outputs.database) as connection:
        assert connection.execute(
            "SELECT document_id FROM research_subset_documents "
            "WHERE subset_id = 'database-seed-v1' ORDER BY document_id"
        ).fetchall() == [
            ("ai-act-proposal",),
            ("ai-liability-directive-proposal",),
            ("artificial-intelligence-act",),
            ("artificial-intelligence-for-europe",),
            ("coordinated-plan-on-artificial-intelligence",),
            ("ethics-guidelines-for-trustworthy-ai",),
            ("white-paper-on-artificial-intelligence",),
        ]


def test_legacy_role_evidence_cannot_bypass_complete_extension_gate(tmp_path):
    data_root = tmp_path / "data"
    shutil.copytree(Path("data"), data_root)
    document_path = data_root / "documents" / "white-paper-on-artificial-intelligence.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["institution_roles"][0].update(
        {
            "evidence_source_id": document["source_ids"][0],
            "evidence_locator": "Official title block",
        }
    )
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_historical_publication(
        load_records(data_root),
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )

    assert any(
        issue.field == "historical_review_status"
        and "partial" in issue.message.lower()
        for issue in issues
    )


def test_unknown_new_legacy_like_document_is_rejected():
    records = load_records(Path("data"))
    legacy = next(
        record
        for record in records["documents"]
        if record.data.get("id") == "white-paper-on-artificial-intelligence"
    )
    legacy.data["id"] = "unlisted-new-document"
    legacy.data["slug"] = "unlisted-new-document"

    issues = validate_historical_publication(
        records,
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )

    assert any(
        issue.field == "historical_review_status"
        and "new published document" in issue.message.lower()
        for issue in issues
    )


def test_scalar_only_historical_extension_is_rejected_as_partial():
    records = load_records(Path("data"))
    legacy = next(
        record
        for record in records["documents"]
        if record.data.get("id") == "white-paper-on-artificial-intelligence"
    )
    legacy.data["historical_review_status"] = "verified"

    issues = validate_historical_publication(
        records,
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )

    assert any(
        issue.field == "historical_review_status"
        and "partial" in issue.message.lower()
        for issue in issues
    )
