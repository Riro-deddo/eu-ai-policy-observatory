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
        ("ecb-opinion-con-2021-40", ["general_cross_sector", "financial_services"]),
        ("ecb-opinion-con-2026-10", ["general_cross_sector", "financial_services"]),
        (
            "ecb-technical-working-document-con-2026-10",
            ["general_cross_sector", "financial_services"],
        ),
        ("ep-ai-act-cult-opinion-pe-719637", ["education", "media_and_culture"]),
        (
            "ep-ai-omnibus-cult-opinion-pe-784261",
            ["education", "media_and_culture"],
        ),
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
        (
            "ep-ai-omnibus-juri-opinion-pe-784179",
            ["justice", "intellectual_property"],
        ),
        ("ep-ai-act-tran-opinion-pe-730085", ["transport_and_mobility"]),
    ],
)
def test_sector_tags_use_reviewed_overrides_in_vocabulary_order(document_id, expected):
    assert sector_tags_for(document_id) == expected


def test_sector_tags_use_reviewed_cross_sector_default():
    assert sector_tags_for("artificial-intelligence-act") == ["general_cross_sector"]


@pytest.mark.parametrize(
    ("document_id", "institution_roles", "expected"),
    [
        (
            "artificial-intelligence-act",
            [
                {"institution_id": "european-parliament", "role": "adopter"},
                {
                    "institution_id": "council-of-the-european-union",
                    "role": "adopter",
                },
            ],
            ["eu_institution_authored", "joint_institutional", "officially_published"],
        ),
        (
            "draft-transparency-guidelines-2026",
            [{"institution_id": "european-commission", "role": "author"}],
            [
                "eu_institution_authored",
                "official_consultation_material",
                "officially_published",
            ],
        ),
        (
            "edpb-edps-joint-opinion-5-2021",
            [
                {
                    "institution_id": "european-data-protection-board",
                    "role": "author",
                },
                {
                    "institution_id": "european-data-protection-supervisor",
                    "role": "author",
                },
            ],
            [
                "eu_agency_or_body_authored",
                "joint_institutional",
                "officially_published",
            ],
        ),
        (
            "ethics-guidelines-for-trustworthy-ai",
            [
                {"institution_id": "high-level-expert-group-on-ai", "role": "author"},
                {"institution_id": "european-commission", "role": "publisher"},
            ],
            [
                "eu_expert_group_authored",
                "officially_published",
            ],
        ),
        (
            "gpai-code-final",
            [{"institution_id": "european-ai-office", "role": "publisher"}],
            ["officially_published"],
        ),
        (
            "ai-act-council-adoption-statements-st-9645-add-1-rev-2",
            [
                {
                    "institution_id": "council-of-the-european-union",
                    "role": "publisher",
                }
            ],
            ["officially_published"],
        ),
    ],
)
def test_provenance_tags_derive_origin_and_flags_in_vocabulary_order(
    document_id, institution_roles, expected
):
    assert provenance_tags_for(document_id, institution_roles) == expected


def test_provenance_tags_reject_unknown_origins_with_document_id():
    with pytest.raises(ValueError, match="unknown-document"):
        provenance_tags_for(
            "unknown-document",
            [{"institution_id": "unknown-institution", "role": "author"}],
        )


@pytest.mark.parametrize("starting_tags", [None, ["financial_services"]])
def test_migration_primary_write_changes_only_classifications_and_timestamp(
    tmp_path, starting_tags
):
    copied = tmp_path / "document.json"
    # Exercise the old migration on the immutable pre-expanded-review record,
    # not today's evidence-bearing record, which must remain protected.
    ledger = json.loads(
        Path("research/migrations/2026-09-05-retained-section-notices.json")
        .read_text(encoding="utf-8")
    )
    record = next(
        item["before"] for item in ledger["documents"]
        if item["document_id"] == "draft-high-risk-classification-guidelines-2026"
    )
    record["updated_at"] = "2026-09-03T00:00:00Z"
    if starting_tags is None:
        record.pop("sector_tags")
        record.pop("provenance_tags")
    else:
        record["sector_tags"] = starting_tags
        record["provenance_tags"] = ["officially_published"]
    copied.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
    before = json.loads(copied.read_text(encoding="utf-8"))

    assert migrate_document(copied) is True

    after_bytes = copied.read_bytes()
    after = json.loads(after_bytes.decode("utf-8"))
    allowed_changes = {"sector_tags", "provenance_tags", "updated_at"}
    assert {key: value for key, value in after.items() if key not in allowed_changes} == {
        key: value for key, value in before.items() if key not in allowed_changes
    }
    assert after["sector_tags"] == ["general_cross_sector"]
    assert after["provenance_tags"] == [
        "eu_institution_authored",
        "official_consultation_material",
        "officially_published",
    ]
    assert after["updated_at"] == "2026-09-04T00:00:00Z"
    assert after_bytes == (
        json.dumps(after, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    assert after_bytes.endswith(b"\n")
    assert "—".encode("utf-8") in after_bytes

    before_second_run = copied.read_bytes()
    assert migrate_document(copied) is False
    assert copied.read_bytes() == before_second_run


def test_migration_is_idempotent(tmp_path):
    copied = tmp_path / "document.json"
    copied.write_bytes(
        Path("data/documents/artificial-intelligence-act.json").read_bytes()
    )
    migrate_document(copied)
    before = copied.read_bytes()
    assert migrate_document(copied) is False
    assert copied.read_bytes() == before


@pytest.mark.parametrize("document_id", [
    "council-decision-84-130-eec-esprit",
    "draft-high-risk-classification-guidelines-2026",
])
def test_migration_never_rewrites_verified_evidence_bearing_document(tmp_path, document_id):
    copied = tmp_path / "historical-document.json"
    copied.write_bytes(
        Path(f"data/documents/{document_id}.json").read_bytes()
    )
    before = copied.read_bytes()

    assert migrate_document(copied) is False
    assert copied.read_bytes() == before
