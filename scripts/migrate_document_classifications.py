"""Deterministically classify the canonical EU AI document corpus."""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Mapping
import json
from pathlib import Path


MIGRATION_UPDATED_AT = "2026-09-04T00:00:00Z"

SECTOR_TAG_ORDER = [
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

PROVENANCE_TAG_ORDER = [
    "eu_institution_authored",
    "eu_agency_or_body_authored",
    "eu_expert_group_authored",
    "eu_commissioned_external",
    "joint_institutional",
    "official_consultation_material",
    "officially_published",
]

SECTOR_OVERRIDES = {
    "ecb-opinion-con-2021-40": ["general_cross_sector", "financial_services"],
    "ecb-opinion-con-2026-10": ["general_cross_sector", "financial_services"],
    "ecb-technical-working-document-con-2026-10": [
        "general_cross_sector",
        "financial_services",
    ],
    "ep-ai-act-cult-opinion-pe-719637": ["education", "media_and_culture"],
    "ep-ai-omnibus-cult-opinion-pe-784261": ["education", "media_and_culture"],
    "ep-ai-act-envi-opinion-pe-699056": ["agriculture_and_environment", "health"],
    "ep-ai-act-itre-opinion-pe-719801": [
        "industry_and_manufacturing",
        "research_and_innovation",
    ],
    "ep-ai-act-juri-opinion-pe-719827": ["intellectual_property", "justice"],
    "ep-ai-omnibus-juri-opinion-pe-784179": ["intellectual_property", "justice"],
    "ep-ai-act-tran-opinion-pe-730085": ["transport_and_mobility"],
}

EU_INSTITUTIONS = {
    "european-commission",
    "european-parliament",
    "council-of-the-european-union",
    "european-central-bank",
}
EU_BODIES = {
    "european-economic-and-social-committee",
    "european-data-protection-supervisor",
    "european-data-protection-board",
    "european-committee-of-the-regions",
    "european-artificial-intelligence-board",
}
EU_EXPERT_GROUPS = {"high-level-expert-group-on-ai"}
EU_INSTITUTION_SERVICES = {"european-ai-office"}
PRODUCTION_ROLES = {"author", "proposer", "adopter", "contributor"}

OFFICIAL_CONSULTATION_DOCUMENTS = {
    "draft-guidance-serious-ai-incidents-2025",
    "draft-serious-ai-incident-report-template-2025",
    "draft-high-risk-classification-guidelines-2026",
    "draft-high-risk-classification-guidelines-annex-i-2026",
    "draft-high-risk-classification-guidelines-annex-iii-2026",
    "draft-transparency-guidelines-2026",
}


def _in_vocabulary_order(values: Iterable[str], order: list[str]) -> list[str]:
    selected = set(values)
    return [value for value in order if value in selected]


def sector_tags_for(document_id: str) -> list[str]:
    """Return reviewed sector classifications in controlled-vocabulary order."""
    tags = SECTOR_OVERRIDES.get(document_id, ["general_cross_sector"])
    return _in_vocabulary_order(tags, SECTOR_TAG_ORDER)


def provenance_tags_for(
    document_id: str, institution_roles: Iterable[Mapping[str, str]]
) -> list[str]:
    """Derive production provenance without treating publishers as authors."""
    institution_ids = {
        institution_role["institution_id"]
        for institution_role in institution_roles
        if institution_role.get("role") in PRODUCTION_ROLES
    }
    tags: set[str] = set()
    if institution_ids & EU_INSTITUTIONS:
        tags.add("eu_institution_authored")
    if institution_ids & EU_BODIES:
        tags.add("eu_agency_or_body_authored")
    if institution_ids & EU_EXPERT_GROUPS:
        tags.add("eu_expert_group_authored")
    if institution_ids & EU_INSTITUTION_SERVICES:
        tags.add("eu_commissioned_external")

    if institution_ids and not tags:
        institutions = ", ".join(sorted(institution_ids)) or "none"
        raise ValueError(
            f"Document {document_id!r} has no known authoring origin "
            f"for institutions: {institutions}"
        )

    if len(institution_ids) > 1:
        tags.add("joint_institutional")
    if document_id in OFFICIAL_CONSULTATION_DOCUMENTS:
        tags.add("official_consultation_material")
    tags.add("officially_published")
    return _in_vocabulary_order(tags, PROVENANCE_TAG_ORDER)


def migrate_document(path: Path) -> bool:
    """Apply classifications to one document, returning whether bytes changed."""
    record = json.loads(path.read_text(encoding="utf-8"))
    document_id = record["id"]
    sector_tags = sector_tags_for(document_id)
    provenance_tags = provenance_tags_for(document_id, record["institution_roles"])

    if (
        record.get("sector_tags") == sector_tags
        and record.get("provenance_tags") == provenance_tags
    ):
        return False

    record["sector_tags"] = sector_tags
    record["provenance_tags"] = provenance_tags
    record["updated_at"] = MIGRATION_UPDATED_AT
    rendered = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    encoded = rendered.encode("utf-8")
    if encoded == path.read_bytes():
        return False
    path.write_bytes(encoded)
    return True


def migrate_documents(data_root: Path) -> list[str]:
    """Migrate every JSON document and return changed IDs in sorted order."""
    changed_ids: list[str] = []
    for path in sorted(data_root.glob("*.json")):
        document_id = json.loads(path.read_text(encoding="utf-8"))["id"]
        if migrate_document(path):
            changed_ids.append(document_id)
    return sorted(changed_ids)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify canonical EU AI document records."
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data/documents"),
        help="Document directory (default: data/documents)",
    )
    args = parser.parse_args()

    for document_id in migrate_documents(args.data_root):
        print(document_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
