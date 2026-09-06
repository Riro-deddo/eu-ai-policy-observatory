"""Catch malformed audit ledgers and loss of candidate decision history."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "research/reviews/2026-09-06-release-closure"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_release_review_ledgers_resolve_to_preserved_records_and_sources():
    retained = read(REVIEW / "retained-records.json")
    candidates = read(REVIEW / "candidate-decisions.json")
    inventory = {row["id"]: row for row in read(ROOT / "research/corpus-inventory.json")["candidates"]}
    assert len(retained["decisions"]) == 4
    assert len({row["document_id"] for row in retained["decisions"]}) == 4
    assert len(candidates["decisions"]) == 12
    assert len({row["candidate_id"] for row in candidates["decisions"]}) == 12
    source_pairs = {(row["url"], row["sha256"]) for row in candidates["sources"]}
    for row in retained["decisions"]:
        document = read(ROOT / "data/documents" / (row["document_id"] + ".json"))
        assert document.get("historical_review_status") != "verified"
        assert row["unresolved"] and row["reopen_when"]
    for row in candidates["decisions"]:
        candidate = inventory[row["candidate_id"]]
        assert row["decision"] == "pending"
        assert any(previous["decision"] == "pending" for previous in candidate["decision_history"])
        if row["candidate_id"].startswith("ep-ai-act-committee-amendments-"):
            assert candidate["decision"] == "included"
            assert candidate["document_id"] == row["candidate_id"]
        else:
            assert candidate["decision"] == "pending"
            assert candidate["document_id"] is None
        assert (row["official_source_url"], row["pdf_sha256"]) in source_pairs
        assert re.fullmatch(r"[0-9a-f]{64}", row["pdf_sha256"])
        assert candidate["decision_history"][0]["decision"] == "excluded"
        assert candidate["decision_history"][-1]["decision"] == "pending"
        assert candidate["decision_history"][-1]["reviewed_at"] < candidate["reviewed_at"]
        assert row["unresolved"] and row["reopen_when"]
