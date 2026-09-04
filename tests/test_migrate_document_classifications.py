import json
from pathlib import Path

import pytest

from scripts.migrate_document_classifications import (
    migrate_document,
    provenance_tags_for,
    sector_tags_for,
)


SECTOR_ORDER = [
    "general_cross_sector",
    "health",
    "employment_and_labour",
    "migration_asylum_and_border_management",
    "financial_services",
    "transport_and_mobility",
    "defence_and_security",
    "law_enforcement",
    "justice",
    "education",
    "public_administration",
    "consumer_protection",
    "media_and_culture",
    "intellectual_property",
    "research_and_innovation",
    "industry_and_manufacturing",
    "agriculture_and_environment",
    "critical_infrastructure",
    "cybersecurity",
    "competition_and_markets",
]
PROVENANCE_ORDER = [
    "eu_institution_authored",
    "eu_agency_or_body_authored",
    "eu_expert_group_authored",
    "eu_commissioned_external",
    "joint_institutional",
    "official_consultation_material",
    "officially_published",
]


def test_every_existing_document_receives_required_classifications():
    for path in sorted(Path("data/documents").glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        assert document["sector_tags"]
        assert len(document["sector_tags"]) == len(set(document["sector_tags"]))
        assert document["sector_tags"] == sorted(
            document["sector_tags"], key=SECTOR_ORDER.index
        )
        assert document["provenance_tags"]
        assert "officially_published" in document["provenance_tags"]
        assert document["provenance_tags"] == sorted(
            document["provenance_tags"], key=PROVENANCE_ORDER.index
        )


@pytest.mark.parametrize(
    ("document_id", "expected"),
    [
        (
            "ecb-opinion-con-2021-40",
            ["general_cross_sector", "financial_services"],
        ),
        ("ep-ai-act-cult-opinion-pe-719637", ["education", "media_and_culture"]),
        (
            "ep-ai-act-envi-opinion-pe-699056",
            ["health", "agriculture_and_environment"],
        ),
        (
            "ep-ai-act-itre-opinion-pe-719801",
            ["research_and_innovation", "industry_and_manufacturing"],
        ),
        (
            "ep-ai-act-juri-opinion-pe-719827",
            ["justice", "intellectual_property"],
        ),
        ("ep-ai-act-tran-opinion-pe-730085", ["transport_and_mobility"]),
        ("artificial-intelligence-act", ["general_cross_sector"]),
    ],
)
def test_sector_tags_use_reviewed_overrides_in_vocabulary_order(document_id, expected):
    assert sector_tags_for(document_id) == expected


@pytest.mark.parametrize(
    ("document_id", "institution_ids", "expected"),
    [
        (
            "artificial-intelligence-act",
            {"european-parliament", "council-of-the-european-union"},
            ["eu_institution_authored", "joint_institutional", "officially_published"],
        ),
        (
            "draft-transparency-guidelines-2026",
            {"european-commission"},
            [
                "eu_institution_authored",
                "official_consultation_material",
                "officially_published",
            ],
        ),
        (
            "edpb-edps-joint-opinion-5-2021",
            {"european-data-protection-board", "european-data-protection-supervisor"},
            [
                "eu_agency_or_body_authored",
                "joint_institutional",
                "officially_published",
            ],
        ),
        (
            "ethics-guidelines-for-trustworthy-ai",
            {"high-level-expert-group-on-ai", "european-commission"},
            [
                "eu_institution_authored",
                "eu_expert_group_authored",
                "joint_institutional",
                "officially_published",
            ],
        ),
        (
            "gpai-code-final",
            {"european-ai-office"},
            ["eu_commissioned_external", "officially_published"],
        ),
    ],
)
def test_provenance_tags_derive_origin_and_flags_in_vocabulary_order(
    document_id, institution_ids, expected
):
    assert provenance_tags_for(document_id, institution_ids) == expected


def test_provenance_tags_reject_unknown_origins_with_document_id():
    with pytest.raises(ValueError, match="unknown-document"):
        provenance_tags_for("unknown-document", {"unknown-institution"})


def test_migration_is_idempotent(tmp_path):
    copied = tmp_path / "document.json"
    copied.write_bytes(
        Path("data/documents/artificial-intelligence-act.json").read_bytes()
    )
    migrate_document(copied)
    before = copied.read_bytes()
    assert migrate_document(copied) is False
    assert copied.read_bytes() == before
