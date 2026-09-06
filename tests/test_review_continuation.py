"""Regressions for independently evidenced third-pass admissions."""

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "research/migrations/2026-09-05-review-continuation.json"
EVIDENCE_CORRECTIONS_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-evidence-corrections.json"
FOUR_ADMISSIONS_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-four-evidence-admissions.json"
SIX_RECORD_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-six-record-evidence-update.json"
SEVEN_ADMISSIONS_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-seven-evidence-admissions.json"


@pytest.fixture(scope="module")
def public_payload(tmp_path_factory):
    result = run_pipeline(
        ROOT, "2026-09-05T20:40:00Z",
        output_root=tmp_path_factory.mktemp("continuation-output"),
    )
    return json.loads(result.public_json.read_text(encoding="utf-8"))


def test_parliament_adopted_amendments_keep_adoption_and_oj_dates(public_payload):
    document = next(d for d in public_payload["documents"] if d["id"] == "ep-position-p9-ta-2023-0236")
    assert document["historical_review_status"] == "verified"
    assert document["document_type"] == "institutional_position"
    assert document["document_date_kind"] == "institutional_adoption"
    assert document["document_date"] == "2023-06-14"
    assert document["publication_date"] == "2024-01-23"
    assert document["legal_status"] == "adopted"


@pytest.mark.parametrize("document_id,reference,pdf_id", [
    ("ai-system-definition-guidelines-2025", "C(2025) 5053 final", "ai-act-service-desk-definition-c5053-pdf"),
    ("prohibited-ai-practices-guidelines-2025", "C(2025) 5052 final", "ai-act-service-desk-prohibited-c5052-pdf"),
])
def test_later_official_guideline_manifestations_keep_issue_and_publication_distinct(
    public_payload, document_id, reference, pdf_id
):
    document = next(d for d in public_payload["documents"] if d["id"] == document_id)
    assert document["historical_review_status"] == "verified"
    assert document["official_reference"] == reference
    assert document["document_date"] == "2025-07-29"
    assert document["document_date_kind"] == "document_issue"
    assert document["publication_date"] == "2026-05-06"
    assert document["record_level"] == "principal"
    assert document["version_status"] == "final"
    assert document["legal_status"] == "non_binding"
    assert document["date_evidence"]["document_date"]["source_id"] == pdf_id
    publication = document["date_evidence"]["publication_date"]
    sources = {s["id"]: s for s in document["sources"]}
    assert sources[publication["source_id"]]["url"] == "https://ai-act-service-desk.ec.europa.eu/en/resources?page=1"
    assert "2026-05-06T16:" in publication["locator"]
    assert "first" in publication["meaning"]


def test_transparency_route_represents_the_evidenced_draft_annex(public_payload):
    documents = {d["id"]: d for d in public_payload["documents"]}
    annex = documents["final-transparency-guidelines-2026"]
    assert annex["historical_review_status"] == "verified"
    assert annex["record_level"] == "attachment"
    assert annex["version_status"] == "draft"
    assert annex["legal_status"] == "non_binding"
    assert annex["institutions"]
    assert all(role["role"] != "adopter" for role in annex["institutions"])
    assert annex["official_reference"] == "C(2026) 5054 final"
    assert annex["document_date"] == annex["publication_date"] == "2026-07-20"
    assert documents["draft-transparency-guidelines-2026"]["historical_review_status"] == "verified"
    relationships = public_payload["relationships"]
    assert any(
        r["source_entity_id"] == annex["id"]
        and r["target_entity_id"] == "transparency-guidelines-approval-communication-2026"
        and r["relationship_type"] == "annex_to"
        and r["evidence_source_id"] == "commission-newsroom-131215-pdf"
        for r in relationships
    )
    assert any(
        r["source_entity_id"] == annex["id"]
        and r["target_entity_id"] == "draft-transparency-guidelines-2026"
        and r["relationship_type"] == "revises"
        and r["evidence_source_id"] == "commission-newsroom-131215-pdf"
        for r in relationships
    )


def test_continuation_accounts_for_every_starting_record_once(public_payload):
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    previous = json.loads((ROOT / "research/migrations/2026-09-05-remaining-evidence-review.json").read_text(encoding="utf-8"))
    starting = ledger["starting_pending_ids"]
    upgraded = ledger["upgraded_ids"]
    held = [row["document_id"] for row in ledger["held_records"]]
    audited = [row["document_id"] for row in ledger["record_audit"]]
    assert len(starting) == len(set(starting)) == 30
    assert set(starting) == {row["document_id"] for row in previous["held_records"]}
    assert len(upgraded) == len(set(upgraded)) == ledger["expected_after"]["upgraded"]
    assert len(held) == len(set(held)) == ledger["expected_after"]["held"]
    assert not set(upgraded) & set(held)
    assert set(starting) == set(upgraded) | set(held)
    assert len(audited) == len(set(audited)) == 30
    assert set(audited) == set(starting)
    assert all(row["reasons"] for row in ledger["held_records"])
    documents = {d["id"]: d for d in public_payload["documents"]}
    corrections = json.loads(EVIDENCE_CORRECTIONS_LEDGER_PATH.read_text(encoding="utf-8"))
    four_admissions = json.loads(FOUR_ADMISSIONS_LEDGER_PATH.read_text(encoding="utf-8"))
    six_record_update = json.loads(SIX_RECORD_LEDGER_PATH.read_text(encoding="utf-8"))
    seven_admissions = json.loads(SEVEN_ADMISSIONS_LEDGER_PATH.read_text(encoding="utf-8"))
    later_upgrades = (
        set(corrections["upgraded_ids"])
        | set(four_admissions["upgraded_ids"])
        | set(six_record_update["upgraded_existing_ids"])
        | set(seven_admissions["upgraded_ids"])
    )
    for document_id in upgraded:
        assert documents[document_id]["historical_review_status"] == "verified"
    for document_id in held:
        expected = "verified" if document_id in later_upgrades else "legacy_review_pending"
        assert documents[document_id]["historical_review_status"] == expected
    assert Counter(
        documents[row["id"]]["historical_review_status"]
        for row in ledger["baseline"]["documents"]
    ) == {
        "verified": ledger["expected_after"]["historical_review"]["verified"] + len(later_upgrades),
        "legacy_review_pending": ledger["expected_after"]["historical_review"]["legacy_review_pending"] - len(later_upgrades),
    }
    assert {d["id"]: d["slug"] for d in ledger["baseline"]["documents"]}.items() <= {
        d["id"]: d["slug"] for d in documents.values()
    }.items()
    for row in ledger["record_audit"]:
        handoff = json.loads((ROOT / row["handoff_path"]).read_text(encoding="utf-8"))
        assert handoff["records"][row["handoff_record_index"]]["document_id"] == row["document_id"]
        assert row["checked_urls"]


def test_continuation_preserves_all_prior_verified_records_and_second_pass_ledger():
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    previous_path = ROOT / "research/migrations/2026-09-05-remaining-evidence-review.json"
    assert hashlib.sha256(previous_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest() == ledger["baseline"]["prior_ledger_sha256_lf"]
    previous_verified = [d for d in ledger["baseline"]["documents"] if d["historical_review_status"] == "verified"]
    assert len(previous_verified) == 101
    for row in previous_verified:
        document = ROOT / "data/documents" / f"{row['id']}.json"
        assert hashlib.sha256(document.read_text(encoding="utf-8").encode("utf-8")).hexdigest() == row["sha256_lf"]
