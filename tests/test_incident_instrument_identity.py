"""Protect standalone identity without conflating principal and final status."""
from copy import deepcopy
import json
from pathlib import Path
import sqlite3

from observatory.historical_readiness import validate_historical_readiness
from observatory.io import load_records
from observatory.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/migrations/2026-09-05-incident-instrument-identity.json"
TITLES = {
    "draft-guidance-serious-ai-incidents-2025": "DRAFT GUIDANCE ARTICLE 73 AI ACT- INCIDENT REPORTING (HIGH-RISK AI SYSTEMS)",
    "draft-serious-ai-incident-report-template-2025": "Incident Report for Serious Incidents under the AI Act (High-risk AI systems)",
}
HELD = {
    "draft-high-risk-classification-guidelines-2026",
    "draft-high-risk-classification-guidelines-annex-i-2026",
    "draft-high-risk-classification-guidelines-annex-iii-2026",
}


def test_pipeline_presents_two_standalone_instruments_without_new_records(tmp_path):
    outputs = run_pipeline(ROOT, "2026-09-05T09:00:00Z", output_root=tmp_path / "output")
    public = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    documents = {item["id"]: item for item in public["documents"]}
    frozen = json.loads((ROOT / "research/migrations/2026-09-05-public-document-baseline.json").read_text(encoding="utf-8"))
    assert {(item["id"], item["slug"]) for item in documents.values()} == {
        (item["id"], item["slug"]) for item in frozen["documents"]
    }
    assert len(documents) == 117
    assert len(public["relationships"]) == 95
    assert public["coverage"]["principal_documents"] == 35
    with sqlite3.connect(outputs.database) as connection:
        for doc_id, title in TITLES.items():
            document = documents[doc_id]
            assert document["record_level"] == "principal"
            assert document["official_title"] == title
            assert document["version_status"] == "draft"
            assert document["document_date"] == document["publication_date"] == "2025-09-26"
            assert document["legal_status"] == "non_binding"
            assert connection.execute(
                "SELECT record_level, official_title, version_status FROM documents WHERE id = ?", (doc_id,)
            ).fetchone() == ("principal", title, "draft")
            assert connection.execute(
                "SELECT COUNT(*) FROM document_snapshots WHERE document_id = ?", (doc_id,)
            ).fetchone()[0] == 1
    assert documents["draft-serious-ai-incident-report-template-2025"]["version_label"] == "1.0.0"
    assert documents["draft-guidance-serious-ai-incidents-2025"]["version_label"] == "Consultation draft"


def test_only_three_section_parent_holds_remain():
    issues = validate_historical_readiness(load_records(ROOT / "data"), ROOT / "schema", "2026-09-04")
    assert {Path(issue.record_path).stem for issue in issues
            if issue.code == "historical_relationship" and issue.field == "record_level"} == HELD


def test_inventory_reconciliation_keeps_the_same_included_identities():
    inventory = json.loads((ROOT / "research/corpus-inventory.json").read_text(encoding="utf-8"))
    candidates = {item["id"]: item for item in inventory["candidates"]}
    for doc_id, title in TITLES.items():
        candidate = candidates[doc_id]
        assert candidate["record_level"] == "principal"
        assert candidate["official_title"] == title
        assert candidate["decision"] == "included"
        assert candidate["document_id"] == doc_id
        assert candidate["reviewed_by"] == "Yichen Hao"
        assert candidate["reviewed_at"] == candidate["discovered_at"] == "2026-09-04T00:00:00Z"
    assert candidates["draft-serious-ai-incident-report-template-2025"]["version_label"] == "1.0.0"


def test_identity_ledger_accounts_for_every_changed_document_field():
    assert LEDGER.is_file(), "The editorial correction must have its own evidence ledger"
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert {item["before"]["id"] for item in ledger["documents"]} == set(TITLES)
    guidance = next(item for item in ledger["documents"]
                    if item["before"]["id"] == "draft-guidance-serious-ai-incidents-2025")
    assert guidance["evidence"]["page_locators"][0] == (
        "Page 1: title; section 1 (BACKGROUND AND OBJECTIVES) and section 2 (DEFINITIONS); "
        "Article 73 high-risk scope."
    )
    for item in ledger["documents"]:
        before = item["before"]
        expected = deepcopy(before)
        assert set(item["after_changes"]) == {
            "official_title", "record_level", "updated_at", "corpus_assessment.researcher_notes"
        }
        for dotted, value in item["after_changes"].items():
            target = expected
            parts = dotted.split(".")
            for part in parts[:-1]:
                target = target[part]
            target[parts[-1]] = value
        current = json.loads((ROOT / "data/documents" / f'{before["id"]}.json').read_text(encoding="utf-8"))
        assert current == expected
        assert item["evidence"]["source_id"] in current["source_ids"]
        assert item["evidence"]["page_locators"]
        assert current["snapshots"] == before["snapshots"]
        assert current["corpus_assessment"]["reviewed_by"] == before["corpus_assessment"]["reviewed_by"]
    candidates = {item["id"]: item for item in json.loads(
        (ROOT / "research/corpus-inventory.json").read_text(encoding="utf-8")
    )["candidates"]}
    assert len(ledger["inventory_changes"]) == 2
    for item in ledger["inventory_changes"]:
        assert candidates[item["before"]["id"]] == item["after"]
    assert ledger["relationship_changes"] == []
    assert set(ledger["remaining_relationship_holds"]) == HELD
