"""Pipeline regressions for the 6 September bounded evidence corrections."""

import gzip
import hashlib
import json
from pathlib import Path

import pytest

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/migrations/2026-09-06-evidence-corrections.json"

EXPECTED_PUBLICATIONS = {
    "ai-act-council-general-approach-st-15698-2022": ("2022-12-06", "fd86e2b0-758c-11ed-9887-01aa75ed71a1"),
    "ai-act-council-adoption-note-st-9645-2024-rev-1": ("2024-05-15", "e80c49bd-12d8-11ef-a251-01aa75ed71a1"),
    "ai-act-council-adoption-statements-st-9645-add-1-rev-2": ("2024-05-15", "b1da3f85-143f-11ef-a251-01aa75ed71a1"),
    "ai-omnibus-council-adoption-note-st-10752-2026": ("2026-06-22", "10220a8a-6fa1-11f1-ae88-01aa75ed71a1"),
    "ai-omnibus-council-adoption-statement-st-10752-add-2": ("2026-06-24", "f76aad95-7089-11f1-9800-01aa75ed71a1"),
    "ai-omnibus-council-information-note-st-10599-2026": ("2026-06-17", "37937497-6b1d-11f1-ae88-01aa75ed71a1"),
    "ai-act-consolidated-2026-07-27": ("2026-07-27", "b1730fb2-8f1c-11f1-9262-01aa75ed71a1"),
}


@pytest.fixture(scope="module")
def payload(tmp_path_factory):
    result = run_pipeline(ROOT, "2026-09-06T05:00:00Z", output_root=tmp_path_factory.mktemp("evidence-corrections"))
    return json.loads(result.public_json.read_text(encoding="utf-8"))


@pytest.mark.parametrize("document_id,expected", EXPECTED_PUBLICATIONS.items())
def test_new_admissions_link_exact_op_publication_evidence(payload, document_id, expected):
    date, uuid = expected
    document = next(row for row in payload["documents"] if row["id"] == document_id)
    assert document["historical_review_status"] == "verified"
    assert document["publication_date"] == date
    citation = document["date_evidence"]["publication_date"]
    assert citation["source_id"] == f"{document_id}-op-publication"
    source = next(row for row in document["sources"] if row["id"] == citation["source_id"])
    assert source["url"] == f"https://op.europa.eu/en/publication-detail/-/publication/{uuid}/language-en"


def test_statement_authors_are_not_replaced_by_the_council_host(payload):
    documents = {row["id"]: row for row in payload["documents"]}
    authors_2024 = {row["name"] for row in documents["ai-act-council-adoption-statements-st-9645-add-1-rev-2"]["bibliographic_authors"]}
    authors_2026 = {row["name"] for row in documents["ai-omnibus-council-adoption-statement-st-10752-add-2"]["bibliographic_authors"]}
    assert authors_2024 == {"France", "Austria"}
    assert authors_2026 == {"Greece"}
    assert documents["ai-act-council-adoption-statements-st-9645-add-1-rev-2"]["provenance_tags"] == ["officially_published"]
    assert documents["ai-omnibus-council-adoption-statement-st-10752-add-2"]["provenance_tags"] == ["officially_published"]


def test_consolidation_keeps_underlying_status_without_claiming_new_joint_authorship(payload):
    document = next(row for row in payload["documents"] if row["id"] == "ai-act-consolidated-2026-07-27")
    assert document["document_date_kind"] == "consolidation"
    assert document["legal_status"] == "in_force"
    assert document["provenance_tags"] == ["officially_published"]
    assert "no independent legal effect" in document["corpus_assessment"]["researcher_notes"].lower()
    roles = {(row["id"], row["role"]): row for row in document["institutions"]}
    assert ("publications-office-of-the-european-union", "publisher") in roles
    assert "underlying" in roles[("european-parliament", "adopter")]["evidence_locator"].lower()
    assert "underlying" in roles[("council-of-the-european-union", "adopter")]["evidence_locator"].lower()


def test_information_note_distinguishes_wrapper_from_parliament_resolution(payload):
    document = next(row for row in payload["documents"] if row["id"] == "ai-omnibus-council-information-note-st-10599-2026")
    assert document["document_date"] == "2026-06-17"
    assert any(row["kind"] == "institutional_adoption" and row["value"] == "2026-06-16" for row in document["additional_dates"])
    assert "wrapper" in document["corpus_assessment"]["researcher_notes"].lower()
    assert "parliament" in document["corpus_assessment"]["researcher_notes"].lower()


def test_ledger_preserves_routes_and_retains_unadmitted_holds(payload):
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    documents = {row["id"]: row for row in payload["documents"]}
    assert ledger["before_counts"] == {"verified": 160, "legacy_review_pending": 26, "total": 186}
    assert ledger["after_counts"] == {"verified": 167, "legacy_review_pending": 19, "total": 186}
    assert len(ledger["dispositions"]) == 26
    assert {row["document_id"] for row in ledger["dispositions"]} == set(ledger["starting_pending_ids"])
    baseline = json.loads((ROOT / ledger["route_identity_baseline"]["path"]).read_text(encoding="utf-8"))
    routes = {row["id"]: row["slug"] for row in baseline["documents"]}
    routes.update({row["id"]: row["slug"] for row in ledger["route_identity_baseline"]["subsequent_preserved_routes"]})
    assert routes == {row["id"]: row["slug"] for row in documents.values()}
    receipts = {row["document_id"]: row for row in ledger["evidence_receipts"]}
    assert set(receipts) == set(ledger["upgraded_ids"])
    for receipt in receipts.values():
        evidence_path = (ROOT / receipt["local_path"]).resolve()
        assert evidence_path.is_relative_to(ROOT)
        assert receipt["compression"] == "gzip"
        evidence_bytes = gzip.decompress(evidence_path.read_bytes())
        assert hashlib.sha256(evidence_bytes).hexdigest() == receipt["sha256"]
        assert receipt["retrieved_at"]
    preservation = ledger["prior_verified_preservation"]
    assert preservation["count"] == 160
    assert preservation["changed_ids"] == []
    proof_path = (ROOT / preservation["comparison_artifact"]).resolve()
    assert proof_path.is_relative_to(ROOT)
    proof_lf_bytes = proof_path.read_text(encoding="utf-8").encode("utf-8")
    assert hashlib.sha256(proof_lf_bytes).hexdigest() == preservation["comparison_artifact_sha256_lf"]
    for row in ledger["dispositions"]:
        expected = "verified" if row["disposition"] == "admitted" else "legacy_review_pending"
        assert documents[row["document_id"]]["historical_review_status"] == expected
