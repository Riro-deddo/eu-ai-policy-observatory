"""Regressions for the seven 6 September evidence-backed admissions."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]
COUNCIL_DISCLOSURE_ID = "council-st-15322-2024-annex-6-disclosure"
COUNCIL_REGISTER_ID = "council-register-st-12206-2022-versions"
JRC_EXACT_DATE_ID = "ai-standardisation-request-c-2023-3215-jrc-exact-publication"
REPEAL_ID = "ai-standardisation-request-c-2023-3215-repeal-decision"

COUNCIL_ADMISSIONS = {
    "ai-act-council-second-compromise-st-11124-2022": "2022-07-15",
    "ai-act-council-third-compromise-part-one-st-12206-2022-rev-1": "2022-09-16",
    "ai-act-council-third-compromise-part-two-st-12549-2022": "2022-09-23",
    "ai-act-council-fourth-compromise-st-13102-2022": "2022-10-19",
    "ai-act-council-final-compromise-st-13955-2022": "2022-11-03",
    "ai-act-council-coreper-general-approach-st-14336-2022": "2022-11-11",
}
COUNCIL_EVIDENCE_SOURCES = {
    "ai-act-council-second-compromise-st-11124-2022": "council-st-11124-2022",
    "ai-act-council-third-compromise-part-one-st-12206-2022-rev-1": "council-st-12206-2022-rev-1",
    "ai-act-council-third-compromise-part-two-st-12549-2022": "council-st-12549-2022",
    "ai-act-council-fourth-compromise-st-13102-2022": "council-st-13102-2022",
    "ai-act-council-final-compromise-st-13955-2022": "council-st-13955-2022",
    "ai-act-council-coreper-general-approach-st-14336-2022": "council-st-14336-2022",
}
COREPER_DOCUMENT = "ai-act-council-coreper-general-approach-st-14336-2022"
STANDARDISATION_ADMISSION = "ai-standardisation-request-c-2023-3215"
ADMISSIONS = {*COUNCIL_ADMISSIONS, STANDARDISATION_ADMISSION}
HOLDS = {
    "ai-act-council-third-compromise-part-one-st-12206-2022-init",
    "standardisation-request-c-2025-3871",
    "gpai-training-content-explanatory-notice-2025",
    "gpai-training-content-template-2025",
}


@pytest.fixture(scope="module")
def payload():
    """Build into a unique short Windows temp path to avoid path-length failures."""
    with tempfile.TemporaryDirectory(prefix="euai-seven-", dir=os.environ.get("TEMP")) as output:
        result = run_pipeline(ROOT, "2026-09-06T20:00:00Z", output_root=Path(output))
        return json.loads(result.public_json.read_text(encoding="utf-8"))


def test_seven_admissions_remain_verified_after_st10069_admission(payload):
    """Catch an omitted upgrade, an unauthorized hold upgrade, or a route-count change."""
    documents = {row["id"]: row for row in payload["documents"]}
    assert len(documents) == 187
    assert payload["coverage"]["historical_review"] == {
        "verified": 183,
        "legacy_review_pending": 4,
    }
    assert {identifier for identifier, row in documents.items() if row["historical_review_status"] == "legacy_review_pending"} == HOLDS
    assert all(documents[identifier]["historical_review_status"] == "verified" for identifier in ADMISSIONS)
    assert all(documents[identifier]["slug"] == identifier for identifier in ADMISSIONS | HOLDS)


@pytest.mark.parametrize("document_id,issue_date", COUNCIL_ADMISSIONS.items())
def test_council_issue_dates_remain_separate_from_later_disclosure(
    payload, document_id, issue_date
):
    """Catch transfer of the 2024 disclosure date to issue or first-publication claims."""
    document = next(row for row in payload["documents"] if row["id"] == document_id)
    assert document["document_date"] == issue_date
    assert document["document_date_kind"] == "document_issue"
    assert document["publication_date"] == "2024-10-28"
    assert document["date_evidence"]["document_date"]["source_id"] != COUNCIL_DISCLOSURE_ID
    disclosure = document["date_evidence"]["publication_date"]
    assert disclosure["source_id"] == COUNCIL_DISCLOSURE_ID
    assert "later" in disclosure["meaning"].lower()
    assert "not first-ever" in disclosure["meaning"].lower()
    sources = {row["id"]: row for row in document["sources"]}
    assert sources[COUNCIL_DISCLOSURE_ID]["url"] == (
        "https://data.consilium.europa.eu/doc/document/ST-15322-2024-INIT/en/pdf"
    )
    assert document["bibliographic_authors"][0]["name"] == (
        "Presidency of the Council of the European Union"
    )
    notes = document["corpus_assessment"]["researcher_notes"].lower()
    assert "recipient" in notes
    assert "disclosure" in notes


def test_council_presidency_records_export_council_authorship_without_recipient_mislabel(
    payload,
):
    """Catch loss of Council discovery or conflation of authorship, sender, and recipient."""
    documents = {row["id"]: row for row in payload["documents"]}

    for document_id, evidence_source_id in COUNCIL_EVIDENCE_SOURCES.items():
        document = documents[document_id]
        roles = {(row["id"], row["role"]): row for row in document["institutions"]}
        expected_roles = {("council-of-the-european-union", "author")}
        if document_id == COREPER_DOCUMENT:
            expected_roles.add(
                ("general-secretariat-of-the-council", "cover_note_sender")
            )
        assert set(roles) == expected_roles

        council_author = roles[("council-of-the-european-union", "author")]
        assert council_author["evidence_source_id"] == evidence_source_id
        assert "presidency" in council_author["evidence_locator"].lower()
        assert "without implying council adoption" in council_author[
            "evidence_locator"
        ].lower()
        assert evidence_source_id in {row["id"] for row in document["sources"]}
        assert len(document["bibliographic_authors"]) == 1
        presidency_author = document["bibliographic_authors"][0]
        assert presidency_author["name"] == (
            "Presidency of the Council of the European Union"
        )
        assert presidency_author["affiliation"] == "Czech Presidency"
        assert presidency_author["evidence_source_id"] == evidence_source_id
        assert "presidency" in presidency_author["evidence_locator"].lower()

    coreper_roles = {
        (row["id"], row["role"]): row
        for row in documents[COREPER_DOCUMENT]["institutions"]
    }
    gsc_sender = coreper_roles[
        ("general-secretariat-of-the-council", "cover_note_sender")
    ]
    assert gsc_sender["evidence_source_id"] == "council-st-14336-2022"
    assert "from general secretariat" in gsc_sender["evidence_locator"].lower()


def test_c2023_request_uses_exact_jrc_locator_and_explicit_repeal(payload):
    """Catch a return to month-only publication evidence or an inferred repeal date."""
    document = next(
        row for row in payload["documents"] if row["id"] == STANDARDISATION_ADMISSION
    )
    assert document["document_date"] == "2023-05-22"
    assert document["publication_date"] == "2023-05-22"
    assert document["document_date_kind"] == "document_issue"
    assert document["legal_status"] == "repealed"
    assert document["bibliographic_authors"] == []
    assert document["additional_dates"] == []

    publication = document["date_evidence"]["publication_date"]
    assert publication["source_id"] == JRC_EXACT_DATE_ID
    assert "pdf p. 6 / printed p. 3" in publication["locator"].lower()
    sources = {row["id"]: row for row in document["sources"]}
    assert sources[JRC_EXACT_DATE_ID]["url"] == (
        "https://publications.jrc.ec.europa.eu/repository/bitstream/JRC134461/JRC134461_01.pdf"
    )
    assert "pdf pp. 8 and 16" in sources[JRC_EXACT_DATE_ID]["verification_note"].lower()

    repeal = document["legal_status_evidence"]
    assert repeal["source_id"] == REPEAL_ID
    assert "article 4" in repeal["locator"].lower()
    assert sources[REPEAL_ID]["url"] == (
        "https://ec.europa.eu/transparency/documents-register/api/files/"
        "C(2025)3871_0/de00000001072818"
    )
    assert "exact repeal date" in repeal["meaning"].lower()
    assert "not" in repeal["meaning"].lower()


def test_rev1_edges_use_exact_evidence_and_unsupported_init_edge_is_quarantined(payload):
    """Catch restoration of the mismatched INIT assertion or loss of REV1 lineage."""
    relationships = {row["id"]: row for row in payload["relationships"]}
    assert len(relationships) == 114
    assert "ai-act-council-third-part-one-revises-second" not in relationships

    predecessor = relationships["ai-act-council-third-part-one-rev-1-revises-second"]
    assert predecessor["source_entity_id"] == (
        "ai-act-council-third-compromise-part-one-st-12206-2022-rev-1"
    )
    assert predecessor["target_entity_id"] == (
        "ai-act-council-second-compromise-st-11124-2022"
    )
    assert predecessor["evidence_source_id"] == "council-st-12206-2022-rev-1"
    assert "paragraph 7" in predecessor["rationale"].lower()

    version = relationships["ai-act-council-third-part-one-rev-1-revises-init"]
    assert version["evidence_source_id"] == COUNCIL_REGISTER_ID
    assert "separate" in version["rationale"].lower()

    pending = json.loads(
        (
            ROOT
            / "data/relationships/ai-act-council-third-part-one-revises-second.json"
        ).read_text(encoding="utf-8")
    )
    assert pending["publication_status"] == "pending_review"
    assert pending["verification_status"] == "pending"
    assert "identity conflict" in pending["rationale"].lower()
