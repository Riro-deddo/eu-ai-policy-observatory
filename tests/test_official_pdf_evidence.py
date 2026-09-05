"""Regression protection for the five actually retrieved Commission PDFs.

Catch missing/misassigned source representations, lost SQLite provenance, and
metadata changes that accidentally alter published identity or draft status.
No network or ignored local binaries are required for the offline test suite.
"""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3

import pytest

from observatory.io import load_records
from observatory.historical_readiness import validate_historical_readiness
from observatory.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/migrations/2026-09-05-official-pdf-evidence.json"
RETAINED_LEDGER = ROOT / "research/migrations/2026-09-05-retained-section-notices.json"
BASELINE = ROOT / "research/migrations/2026-09-05-public-document-baseline.json"
# Hand-checked observations, not values derived by the exporter under test.
FILES = [
    ("draft-guidance-serious-ai-incidents-2025", "119624", "f1d58ecf69004b361d2201ea44e6219f00c27ba249ad5011965152de9167686d", "2026-09-05T08:08:53.261079Z", 341927, 13),
    ("draft-serious-ai-incident-report-template-2025", "119623", "20f90c54a7cd0fb952d08965947dabfa6e423515cab925d9c4b9c81364ed5a82", "2026-09-05T08:08:53.258506Z", 238290, 7),
    ("draft-high-risk-classification-guidelines-2026", "128559", "b127bbdc50b1741bb2d97e8aff5839cccd1a4484445be4e8cca246c12541fc42", "2026-09-05T08:08:53.264585Z", 260362, 6),
    ("draft-high-risk-classification-guidelines-annex-i-2026", "128560", "10f1302c9090d2bcfdb8eacd2b36ff7a09860fc7909f7c1c4b42cc3b9bed3b50", "2026-09-05T08:08:53.458000Z", 337928, 13),
    ("draft-high-risk-classification-guidelines-annex-iii-2026", "128561", "b1df0ffb30310e126c7e060e03c9b5aab97c0a2ab61a2f3e3e00ede3655e2792", "2026-09-05T08:08:53.836269Z", 1547742, 148),
]


@pytest.mark.parametrize("document_id,newsroom,digest,retrieved_at,byte_count,pages", FILES)
def test_canonical_snapshot_identifies_the_actual_official_pdf(
    document_id, newsroom, digest, retrieved_at, byte_count, pages
):
    document = json.loads((ROOT / "data/documents" / f"{document_id}.json").read_text(encoding="utf-8"))
    source_id = f"commission-newsroom-{newsroom}-pdf"
    expected = {
        "id": f"snapshot-newsroom-{newsroom}-20260905",
        "source_id": source_id,
        "retrieved_at": retrieved_at,
        "format": "pdf",
        "content_hash": digest,
        "archived_path": None,
    }
    assert expected in document.get("snapshots", [])
    assert source_id in document["source_ids"]
    source = json.loads((ROOT / "data/sources" / f"{source_id}.json").read_text(encoding="utf-8"))
    assert source["source_type"] == "official_pdf"
    assert source["url"] == f"https://ec.europa.eu/newsroom/dae/redirection/document/{newsroom}"
    assert source["retrieved_at"] == retrieved_at
    assert source["publication_status"] == "published"


def test_pipeline_retains_pdf_provenance_without_adding_documents(tmp_path):
    outputs = run_pipeline(ROOT, "2026-09-05T09:00:00Z", output_root=tmp_path / "output")
    public = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    documents = {item["id"]: item for item in public["documents"]}
    frozen = json.loads(BASELINE.read_text(encoding="utf-8"))["documents"]
    assert {(item["id"], item["slug"]) for item in public["documents"]} == {
        (item["id"], item["slug"]) for item in frozen
    }
    assert outputs.record_counts["documents"] == 117
    assert outputs.record_counts["relationships"] == 95
    with sqlite3.connect(outputs.database) as connection:
        for document_id, newsroom, digest, retrieved_at, _, _ in FILES:
            row = connection.execute(
                "SELECT document_id, source_id, retrieved_at, format, content_hash, archived_path "
                "FROM document_snapshots WHERE id = ?",
                (f"snapshot-newsroom-{newsroom}-20260905",),
            ).fetchone()
            assert row == (document_id, f"commission-newsroom-{newsroom}-pdf",
                           retrieved_at, "pdf", digest, None)
            sources = {source["id"]: source for source in documents[document_id]["sources"]}
            assert sources[f"commission-newsroom-{newsroom}-pdf"]["url"] == (
                f"https://ec.europa.eu/newsroom/dae/redirection/document/{newsroom}"
            )
            # Snapshots are persisted in SQLite; the existing JSON contract omits them.
            assert "snapshots" not in documents[document_id]
    template = documents["draft-serious-ai-incident-report-template-2025"]
    assert template["version_label"] == "1.0.0"
    assert template["version_status"] == "draft"
    assert template["record_level"] == "principal"
    assert template["document_date"] == "2025-09-26"
    assert template["publication_date"] == "2025-09-26"
    assert template["corpus_assessment"]["reviewed_by"] == "Yichen Hao"
    assert template["corpus_assessment"]["reviewed_at"] == "2026-09-04T00:00:00Z"


def test_evidence_ledger_preserves_inspection_limits_and_applied_changes():
    assert LEDGER.is_file(), "The applied PDF evidence batch needs its audit ledger"
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    files = {item["document_id"]: item for item in ledger["files"]}
    assert set(files) == {item[0] for item in FILES}
    for document_id, newsroom, digest, retrieved_at, byte_count, pages in FILES:
        evidence = files[document_id]
        assert (evidence["newsroom_id"], evidence["sha256"], evidence["retrieved_at"],
                evidence["byte_count"], evidence["page_count"]) == (
                    newsroom, digest, retrieved_at, byte_count, pages
                )
        assert evidence["http_status"] == 200
        assert evidence["response_content_type"] == "/"
        assert evidence["detected_format"] == "pdf"
        assert evidence["committed_archive_path"] is None
        assert set(evidence["pages_text_reviewed"]) <= set(range(1, pages + 1))
    assert files["draft-high-risk-classification-guidelines-annex-iii-2026"]["full_text_reviewed"] is False
    assert ledger["whole_guidelines_identity_lead"]["public_endpoint_added"] is False
    assert ledger["review"]["publication_cutoff"] == "2026-09-04"
    assert ledger["changes"]
    identity_review = json.loads(
        (ROOT / "research/migrations/2026-09-05-incident-instrument-identity.json").read_text(encoding="utf-8")
    )
    retained_review = json.loads(RETAINED_LEDGER.read_text(encoding="utf-8"))
    retained_changes = {
        item["document_id"]: item for item in retained_review["documents"]
    }
    later_changes = {item["before"]["id"]: item for item in identity_review["documents"]}
    for change in ledger["changes"]:
        record = json.loads((ROOT / change["path"]).read_text(encoding="utf-8"))
        # Reverse only the subsequent retained-route correction in this local copy.
        # Fields absent before the correction are removed, not replaced wholesale.
        if record.get("entity_type") == "document" and record["id"] in retained_changes:
            retained = retained_changes[record["id"]]
            for field, expected in retained["after_changes"].items():
                assert record[field] == expected
                if field in retained["before"]:
                    record[field] = retained["before"][field]
                else:
                    del record[field]
        # Reverse only the subsequent declared corrections in this local copy.
        # Keep real current snapshots/sources under the original B3 assertions.
        if record.get("entity_type") == "document" and record["id"] in later_changes:
            later = later_changes[record["id"]]
            for dotted, expected in later["after_changes"].items():
                target, previous = record, later["before"]
                parts = dotted.split(".")
                for part in parts[:-1]:
                    target, previous = target[part], previous[part]
                assert target[parts[-1]] == expected
                target[parts[-1]] = previous[parts[-1]]
        if "added_record" in change:
            assert record == change["added_record"]
            continue
        for field in change["fields"]:
            actual = record
            for part in field["field"].split("."):
                actual = actual[part]
            assert actual == field["after"], (change["path"], field["field"])


def test_pdf_acquisition_alone_does_not_fabricate_relationship_readiness():
    records = load_records(ROOT / "data")
    # Recreate B3's pre-identity-review levels in memory, without editing data.
    for record in records["documents"]:
        if record.data["id"] in {
            "draft-guidance-serious-ai-incidents-2025",
            "draft-serious-ai-incident-report-template-2025",
        }:
            record.data["record_level"] = "version"
    issues = validate_historical_readiness(records, ROOT / "schema", "2026-09-04")
    holds = {
        Path(issue.record_path).stem
        for issue in issues
        if issue.code == "historical_relationship" and issue.field == "record_level"
    }
    assert holds == {item[0] for item in FILES}
