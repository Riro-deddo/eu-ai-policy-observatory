import json
from pathlib import Path

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "research/migrations/2026-09-05-expanded-evidence-review.json"
FOLLOWUP_LEDGER_PATH = ROOT / "research/migrations/2026-09-05-remaining-evidence-review.json"
CONTINUATION_LEDGER_PATH = ROOT / "research/migrations/2026-09-05-review-continuation.json"
DOCUMENT_ROOT = ROOT / "data/documents"
SOURCE_ROOT = ROOT / "data/sources"
BUILD_TIMESTAMP = "2026-09-05T18:30:00Z"
HISTORICAL_EXTENSION_FIELDS = {
    "historical_review_status",
    "temporal_collection",
    "relevance_class",
    "document_date_kind",
    "date_evidence",
    "classification_evidence",
    "bibliographic_authors",
    "additional_dates",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_ledger_partitions_the_complete_starting_queue_once():
    """Dropping, duplicating or silently graduating a pending record must fail."""
    ledger = _read_json(LEDGER_PATH)
    baseline_routes = {
        row["id"]: row["slug"] for row in ledger["baseline"]["documents"]
    }
    preexisting_verified = {
        row["id"] for row in ledger["baseline"]["preexisting_verified_records"]
    }
    starting = set(ledger["starting_pending_ids"])
    upgraded = set(ledger["upgraded_ids"])
    held = {row["document_id"] for row in ledger["held_records"]}
    audited = {row["document_id"] for row in ledger["record_audit"]}

    assert len(ledger["starting_pending_ids"]) == len(starting)
    assert len(ledger["upgraded_ids"]) == len(upgraded)
    assert len(ledger["held_records"]) == len(held)
    assert len(ledger["record_audit"]) == len(audited)
    assert len(baseline_routes) == 131
    assert len(preexisting_verified) == 17
    assert len(starting) == 114
    assert len(upgraded) == 77
    assert len(held) == 37
    assert starting == set(baseline_routes) - preexisting_verified
    assert not upgraded & held
    assert starting == upgraded | held
    assert audited == starting
    assert all(row["reasons"] for row in ledger["held_records"])


def test_canonical_records_apply_only_upgrades_and_preserve_holds_and_routes():
    """An upgrade omission, held-record extension or route mutation must fail."""
    ledger = _read_json(LEDGER_PATH)
    documents = {
        path.stem: _read_json(path) for path in DOCUMENT_ROOT.glob("*.json")
    }
    expected_routes = {
        row["id"]: row["slug"] for row in ledger["baseline"]["documents"]
    }
    actual_routes = {identifier: row["slug"] for identifier, row in documents.items()}

    assert expected_routes.items() <= actual_routes.items()
    for identifier in ledger["upgraded_ids"]:
        assert documents[identifier]["historical_review_status"] == "verified"
    followup_upgrades = set(_read_json(FOLLOWUP_LEDGER_PATH)["upgraded_ids"]) | set(
        _read_json(CONTINUATION_LEDGER_PATH)["upgraded_ids"]
    )
    for held in ledger["held_records"]:
        identifier = held["document_id"]
        if identifier in followup_upgrades:
            assert documents[identifier]["historical_review_status"] == "verified"
        else:
            assert HISTORICAL_EXTENSION_FIELDS.isdisjoint(documents[identifier])

    for row in ledger["baseline"]["preexisting_verified_records"]:
        assert documents[row["id"]]["historical_review_status"] == "verified"
    for row in ledger["source_changes"]:
        source = _read_json(SOURCE_ROOT / f"{row['source_id']}.json")
        assert source["id"] == row["source_id"]
        assert source["publication_status"] == "published"
        assert source["url"].startswith("https://")
        assert source["verification_note"].strip()


def test_pipeline_exports_reviewed_upgrades_and_keeps_holds_pending(tmp_path):
    """The public pipeline must expose the reviewed split, not the old 17/114 split."""
    ledger = _read_json(LEDGER_PATH)
    followup = _read_json(CONTINUATION_LEDGER_PATH)
    outputs = run_pipeline(ROOT, BUILD_TIMESTAMP, output_root=tmp_path / "output")
    payload = _read_json(outputs.public_json)
    documents = {row["id"]: row for row in payload["documents"]}

    assert len(documents) >= 131
    assert payload["coverage"]["historical_review"] == followup["expected_after"]["historical_review"]
    assert all(
        documents[identifier]["historical_review_status"] == "verified"
        for identifier in ledger["upgraded_ids"]
    )
    assert all(
        documents[row["document_id"]]["historical_review_status"]
        == "legacy_review_pending"
        for row in followup["held_records"]
    )
    assert {
        row["id"]: row["slug"] for row in ledger["baseline"]["documents"]
    }.items() <= {
        identifier: row["slug"] for identifier, row in documents.items()
    }.items()
