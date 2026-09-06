"""Regressions for the four 6 September evidence-backed admissions."""

import json
from pathlib import Path

import pytest

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DATES_AND_PUBLICATION_URLS = (
    (
        "ai-act-regulatory-scrutiny-board-opinion-sec-2021-167",
        "2021-03-22",
        "2021-04-23",
        "https://op.europa.eu/en/publication-detail/-/publication/ee0d5478-a428-11eb-9585-01aa75ed71a1/language-en",
    ),
    (
        "ecb-technical-working-document-con-2026-10",
        "2026-03-13",
        "2026-03-13",
        "https://op.europa.eu/en/publication-detail/-/publication/c249d527-34cb-11f1-be39-01aa75ed71a1/language-en",
    ),
    (
        "ai-omnibus-council-adoption-statements-st-10752-add-1",
        "2026-06-22",
        "2026-06-22",
        "https://op.europa.eu/en/publication-detail/-/publication/e69a1045-6fa1-11f1-ae88-01aa75ed71a1/language-en",
    ),
    (
        "gpai-provider-guidelines-2025",
        "2025-07-18",
        "2025-08-27",
        "https://ai-act-service-desk.ec.europa.eu/en/resources?page=1",
    ),
)


@pytest.fixture(scope="module")
def payload(tmp_path_factory):
    output = tmp_path_factory.mktemp("four-evidence-admissions")
    result = run_pipeline(ROOT, "2026-09-06T07:00:00Z", output_root=output)
    return json.loads(result.public_json.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "document_id,issue_date,publication_date,publication_url",
    EXPECTED_DATES_AND_PUBLICATION_URLS,
)
def test_four_admissions_publish_complete_evidence_without_route_changes(
    payload, document_id, issue_date, publication_date, publication_url
):
    """Catch a missing extension, date transfer, unofficial citation or route mutation."""
    documents = {row["id"]: row for row in payload["documents"]}
    document = documents[document_id]
    assert document["id"] == document_id
    assert document["slug"] == document_id
    assert document["historical_review_status"] == "verified"
    assert document["document_date"] == issue_date
    assert document["publication_date"] == publication_date
    assert document["document_date_kind"] == "document_issue"
    assert document["temporal_collection"] == "contemporary_eu_ai_policy"
    assert document["relevance_class"] == "direct_ai_substantive"
    assert document["classification_evidence"]
    assert document["bibliographic_authors"] is not None
    assert document["additional_dates"] is not None
    citation = document["date_evidence"]["publication_date"]
    sources = {row["id"]: row for row in document["sources"]}
    assert sources[citation["source_id"]]["url"] == publication_url


def test_gpai_route_remains_the_original_content_approved_draft_annex(payload):
    """Catch substitution of the November final guidelines for the July draft annex."""
    document = next(
        row for row in payload["documents"] if row["id"] == "gpai-provider-guidelines-2025"
    )
    assert document["record_level"] == "attachment"
    assert document["version_status"] == "draft"
    assert document["version_label"] == "Content-approved draft annex"
    assert document["official_reference"] == "C(2025) 5045 final ANNEX"
    assert document["legal_status"] == "non_binding"
    assert "draft Communication from the Commission" in document["official_title"]
    assert any(
        row["source_entity_id"] == document["id"]
        and row["target_entity_id"]
        == "gpai-provider-guidelines-approval-communication-2025"
        and row["relationship_type"] == "annex_to"
        and row["basis"] == "official"
        for row in payload["relationships"]
    )


def test_ecb_companion_is_not_modelled_as_a_literal_official_annex(payload):
    """Catch an official-basis claim that the separate TWD is inside the OJ opinion."""
    relationship = next(
        row
        for row in payload["relationships"]
        if row["id"] == "ecb-technical-working-document-annex-to-opinion"
    )
    assert relationship["source_entity_id"] == "ecb-technical-working-document-con-2026-10"
    assert relationship["target_entity_id"] == "ecb-opinion-con-2026-10"
    assert relationship["relationship_type"] == "annex_to"
    assert relationship["basis"] == "analytical"
    assert "separate companion" in relationship["rationale"].lower()


def test_add1_preserves_named_statement_authors_and_separate_council_roles(payload):
    """Catch replacing Belgium and Commission authorship with the Council host."""
    document = next(
        row
        for row in payload["documents"]
        if row["id"] == "ai-omnibus-council-adoption-statements-st-10752-add-1"
    )
    assert {row["name"] for row in document["bibliographic_authors"]} == {
        "Belgium",
        "European Commission",
    }
    roles = {(row["id"], row["role"]) for row in document["institutions"]}
    assert ("european-commission", "author") in roles
    assert ("council-of-the-european-union", "publisher") in roles
    assert ("general-secretariat-of-the-council", "cover_note_sender") in roles
    assert ("council-of-the-european-union", "author") not in roles
    assert "mixed en/fr" in document["corpus_assessment"]["researcher_notes"].lower()

