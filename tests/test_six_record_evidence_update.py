"""Regressions for the bounded six-record evidence update."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]
PARENT_ID = "draft-high-risk-classification-guidelines-consultation-work-2026"
SECTIONS = {
    "draft-high-risk-classification-guidelines-2026": {"general_cross_sector"},
    "draft-high-risk-classification-guidelines-annex-i-2026": {
        "general_cross_sector",
        "health",
        "transport_and_mobility",
        "industry_and_manufacturing",
    },
    "draft-high-risk-classification-guidelines-annex-iii-2026": {
        "general_cross_sector",
        "critical_infrastructure",
        "transport_and_mobility",
        "education",
        "employment_and_labour",
        "public_administration",
        "financial_services",
        "health",
        "law_enforcement",
        "migration_asylum_and_border_management",
        "justice",
    },
}
OPTIONAL_EXTENSION_FIELDS = {
    "temporal_collection",
    "relevance_class",
    "document_date_kind",
    "date_evidence",
    "classification_evidence",
    "bibliographic_authors",
    "additional_dates",
    "legal_status_evidence",
}


@pytest.fixture(scope="module")
def payload(tmp_path_factory):
    output = tmp_path_factory.mktemp("six-record-evidence-update")
    result = run_pipeline(ROOT, "2026-09-06T18:00:00Z", output_root=output)
    return json.loads(result.public_json.read_text(encoding="utf-8"))


def test_pipeline_publishes_real_complete_guidelines_work_and_original_routes(payload):
    """Catch a cloned section, invented reference, route replacement, or incomplete gate."""
    documents = {row["id"]: row for row in payload["documents"]}
    parent = documents[PARENT_ID]
    assert len(documents) == 187
    assert payload["coverage"]["historical_review"] == {
        "verified": 183,
        "legacy_review_pending": 4,
    }
    assert parent["slug"] == PARENT_ID
    assert parent["official_title"] == "Draft Commission Guidelines on the classification of high-risk AI systems"
    assert parent["short_title"] == "Draft high-risk classification guidelines — Complete consultation work"
    assert parent["record_level"] == "principal"
    assert parent["document_type"] == "guidelines"
    assert parent["version_status"] == "draft"
    assert parent["version_label"] == "Consultation draft — Complete work"
    assert parent["legal_status"] == "non_binding"
    assert parent["document_date"] == parent["publication_date"] == "2026-05-19"
    assert parent["document_date_kind"] == "publication"
    assert parent["official_reference"] is None
    assert parent["celex"] is None
    assert parent["eli"] is None
    assert parent["oj_reference"] is None

    for document_id in [PARENT_ID, *SECTIONS]:
        document = documents[document_id]
        assert document["historical_review_status"] == "verified"
        assert document["temporal_collection"] == "contemporary_eu_ai_policy"
        assert document["relevance_class"] == "direct_ai_substantive"
        assert document["bibliographic_authors"] == []
        assert document["additional_dates"] == []
        assert set(document["date_evidence"]) == {"document_date", "publication_date"}
        assert {(row["field"], row["value"]) for row in document["classification_evidence"]} == {
            ("relevance_class", document["relevance_class"]),
            *(("sector_tags", value) for value in document["sector_tags"]),
            *(("provenance_tags", value) for value in document["provenance_tags"]),
        }
        commission_author = next(row for row in document["institutions"] if row["role"] == "author")
        assert commission_author["id"] == "european-commission"
        assert commission_author["evidence_source_id"] in {row["id"] for row in document["sources"]}

    assert parent["corpus_assessment"]["reviewed_by"] == "AI-assisted reviewer"
    assert parent["corpus_assessment"]["reviewed_at"] == "2026-09-06T17:05:16Z"

    for document_id, expected_sectors in SECTIONS.items():
        section = documents[document_id]
        assert section["corpus_assessment"]["reviewed_by"] == "Yichen Hao"
        assert section["corpus_assessment"]["reviewed_at"] == "2026-09-04T00:00:00Z"
        assert section["slug"] == document_id
        assert section["record_level"] == "attachment"
        assert section["version_status"] == "draft"
        assert section["legal_status"] == "non_binding"
        assert section["official_reference"] is None
        assert section["document_date"] == section["publication_date"] == "2026-05-19"
        assert section["retained_route_notice"] is None
        assert set(section["sector_tags"]) == expected_sectors


def test_sections_have_three_official_part_of_edges_without_replacing_sibling_edges(payload):
    """Catch missing lineage or mislabelling a prospective communication as the parent."""
    relationships = {row["id"]: row for row in payload["relationships"]}
    part_of = [
        row
        for row in relationships.values()
        if row["source_entity_id"] in SECTIONS
        and row["target_entity_id"] == PARENT_ID
        and row["relationship_type"] == "part_of"
    ]
    assert len(part_of) == 3
    assert {row["source_entity_id"] for row in part_of} == set(SECTIONS)
    assert all(row["basis"] == "official" for row in part_of)
    assert all(row["evidence_source_id"] == "high-risk-guidelines-draft-commission" for row in part_of)
    assert all("consultation work" in row["rationale"].lower() for row in part_of)
    assert all("prospective" in row["rationale"].lower() for row in part_of)
    assert "high-risk-annex-i-version-of-draft" in relationships
    assert "high-risk-annex-iii-version-of-draft" in relationships


@pytest.mark.parametrize(
    "document_id,source_id,url,unchanged",
    [
        (
            "gpai-training-content-explanatory-notice-2025",
            "gpai-training-summary-july-publication-oj-2026",
            "https://eur-lex.europa.eu/eli/C/2026/4006/oj/eng/pdf",
            ("supporting", "Final notice", "final", "2025-07-24", "2025-07-24", "non_binding", None),
        ),
        (
            "gpai-training-content-template-2025",
            "gpai-training-summary-july-publication-oj-2026",
            "https://eur-lex.europa.eu/eli/C/2026/4006/oj/eng/pdf",
            ("principal", "Final template", "final", "2025-07-24", "2025-07-24", "non_binding", None),
        ),
    ],
)
def test_evidence_only_records_remain_pending_without_partial_extensions(
    payload, document_id, source_id, url, unchanged
):
    """Catch a false verification, date/status rewrite, or partial extension."""
    document = next(row for row in payload["documents"] if row["id"] == document_id)
    assert document["historical_review_status"] == "legacy_review_pending"
    canonical = json.loads(
        (ROOT / "data/documents" / f"{document_id}.json").read_text(encoding="utf-8")
    )
    assert OPTIONAL_EXTENSION_FIELDS.isdisjoint(canonical)
    assert document["temporal_collection"] is None
    assert document["relevance_class"] is None
    assert document["document_date_kind"] is None
    assert document["date_evidence"] is None
    assert document["classification_evidence"] == []
    assert document["bibliographic_authors"] == []
    assert document["additional_dates"] == []
    assert document["legal_status_evidence"] is None
    assert (
        document["record_level"],
        document["version_label"],
        document["version_status"],
        document["document_date"],
        document["publication_date"],
        document["legal_status"],
        document["official_reference"],
    ) == unchanged
    source = next(row for row in document["sources"] if row["id"] == source_id)
    assert source["url"] == url
    notes = document["corpus_assessment"]["researcher_notes"].lower()
    assert "legacy" in notes and "pending" in notes


def test_evidence_only_notes_lead_with_their_decisive_limits(payload):
    """Catch source claims that overstate work, manifestation, date, or status evidence."""
    documents = {row["id"]: row for row in payload["documents"]}
    notice = documents["gpai-training-content-explanatory-notice-2025"]["corpus_assessment"]["researcher_notes"].lower()
    template = documents["gpai-training-content-template-2025"]["corpus_assessment"]["researcher_notes"].lower()
    standards = documents["ai-standardisation-request-c-2023-3215"]["corpus_assessment"]["researcher_notes"].lower()
    assert "work-level" in notice and "parent" in notice and "lacks" in notice and "december" in notice
    assert "internal template" in template and "parent" in template and "docx" in template and "in-force" in template
    assert "22 may 2023" in standards and "corrective" in standards
    assert "repeal" in standards and "no exact operative repeal date" in standards
