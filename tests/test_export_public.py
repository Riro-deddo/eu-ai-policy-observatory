import copy
import json
from pathlib import Path

import pytest

from observatory.build_db import build_database
from observatory.io import LoadedRecord, load_records
from observatory.export_public import export_public


DATA_ROOT = Path("tests/fixtures/valid/data")
SCHEMA_PATH = Path("schema/database.sql")


@pytest.fixture
def built_mixed_status_database(tmp_path):
    """Build published and draft records whose links exercise the export boundary."""
    records = load_records(DATA_ROOT)
    _append_variant(records, "policies", "example-policy", "draft-policy", "Draft policy", "draft")
    _append_variant(records, "concepts", "risk", "draft-concept", "Draft concept", "draft")
    _append_variant(
        records,
        "institutions",
        "european-commission",
        "draft-institution",
        "Draft institution",
        "draft",
    )
    _append_variant(records, "sources", "example-source", "draft-source", "Draft publisher", "draft")
    _append_variant(
        records,
        "sources",
        "example-source",
        "unused-published-source",
        "Unused publisher",
        "published",
    )
    records["documents"][0].data["policy_ids"].append("draft-policy")
    records["documents"][0].data["concept_ids"].append("draft-concept")
    records["documents"][0].data["source_ids"].append("draft-source")
    records["documents"][0].data["institution_roles"].append(
        {"institution_id": "draft-institution", "role": "contributor"}
    )

    draft_document = _variant(records["documents"][0], "draft-document", "Draft document", "draft")
    draft_document.data.update(
        {
            "slug": "draft-document",
            "policy_ids": ["draft-policy"],
            "concept_ids": ["draft-concept"],
            "source_ids": ["draft-source"],
            "institution_roles": [
                {"institution_id": "draft-institution", "role": "author"}
            ],
        }
    )
    records["documents"].append(draft_document)

    records["relationships"].extend(
        [
            _relationship(
                "published-relationship",
                "document",
                "example-document",
                "policy",
                "example-policy",
                "example-source",
                "published",
            ),
            _relationship(
                "relationship-to-draft",
                "document",
                "example-document",
                "document",
                "draft-document",
                "example-source",
                "published",
            ),
            _relationship(
                "relationship-with-draft-evidence",
                "document",
                "example-document",
                "policy",
                "example-policy",
                "draft-source",
                "published",
            ),
            _relationship(
                "relationship-via-hidden-relationship",
                "document",
                "example-document",
                "relationship",
                "relationship-to-draft",
                "example-source",
                "published",
            ),
        ]
    )

    records["events"].extend(
        [
            _event("published-event", "example-policy", "example-document", "example-source"),
            _event("event-with-draft-document", "example-policy", "draft-document", "example-source"),
        ]
    )
    output = tmp_path / "mixed-status.sqlite"
    return build_database(records, SCHEMA_PATH, output)


def test_export_excludes_every_non_published_record(built_mixed_status_database, tmp_path):
    """A publication-boundary regression must never disclose a draft core record."""
    output = tmp_path / "public-data.json"

    export_public(built_mixed_status_database, output, "2026-09-03T00:00:00Z")

    payload = json.loads(output.read_text(encoding="utf-8"))
    for collection in (
        "policies",
        "documents",
        "events",
        "concepts",
        "institutions",
        "relationships",
        "sources",
    ):
        assert {item["publication_status"] for item in payload[collection]} <= {"published"}
    assert "draft-document" not in {item["id"] for item in payload["documents"]}


def test_export_filters_unpublished_dependencies_and_embeds_document_page_data(
    built_mixed_status_database, tmp_path
):
    """Export must not retain IDs or embedded rows from unpublished dependencies."""
    output = tmp_path / "public-data.json"

    export_public(built_mixed_status_database, output, "2026-09-03T00:00:00Z")

    payload = json.loads(output.read_text(encoding="utf-8"))
    document = next(item for item in payload["documents"] if item["id"] == "example-document")
    assert [item["id"] for item in document["policies"]] == ["example-policy"]
    assert [item["id"] for item in document["concepts"]] == ["risk"]
    assert document["institutions"] == [
        {
            "id": "european-commission",
            "role": "author",
            "publication_status": "published",
            "official_name": "European Commission",
            "short_name": "Commission",
            "institution_type": "European Union institution",
            "official_url": "https://commission.europa.eu/",
            "created_at": "2026-09-03T12:00:00Z",
            "updated_at": "2026-09-03T12:00:00Z",
        }
    ]
    assert document["corpus_assessment"] == {
        "corpus_tier": "core",
        "policy_stage": "proposal",
        "inclusion_rationale": "Directly relevant to the example policy.",
        "researcher_notes": "Complete corpus assessment for the fixture.",
        "review_status": "verified",
        "reviewed_by": "Researcher",
        "reviewed_at": "2026-09-03T12:00:00Z",
    }
    assert [item["id"] for item in document["sources"]] == ["example-source"]
    assert [item["id"] for item in payload["relationships"]] == ["published-relationship"]
    assert [item["id"] for item in payload["events"]] == ["published-event"]
    assert [item["id"] for item in payload["sources"]] == ["example-source"]


def test_export_is_stable_and_uses_the_caller_timestamp(built_mixed_status_database, tmp_path):
    """Static-site builds require byte-identical output for the same database and timestamp."""
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    assert export_public(built_mixed_status_database, first, "2026-09-03T00:00:00Z") == first
    export_public(built_mixed_status_database, second, "2026-09-03T00:00:00Z")

    content = first.read_text(encoding="utf-8")
    payload = json.loads(content)
    assert first.read_bytes() == second.read_bytes()
    assert payload["generated_at"] == "2026-09-03T00:00:00Z"
    assert list(payload) == sorted(payload)
    assert content.endswith("\n")
    for collection in ("policies", "documents", "events", "concepts", "institutions", "relationships", "sources"):
        assert [item["id"] for item in payload[collection]] == sorted(
            item["id"] for item in payload[collection]
        )


def _append_variant(records, collection, source_id, new_id, replacement_name, status):
    variant = _variant(
        next(item for item in records[collection] if item.data["id"] == source_id),
        new_id,
        replacement_name,
        status,
    )
    records[collection].append(variant)


def _variant(record, new_id, replacement_name, status):
    variant = copy.deepcopy(record)
    variant.data["id"] = new_id
    variant.data["publication_status"] = status
    for field in ("name", "official_name", "publisher", "official_title", "short_title"):
        if field in variant.data:
            variant.data[field] = replacement_name
    return LoadedRecord(variant.data, Path(f"generated/{new_id}.json"))


def _relationship(identifier, source_type, source_id, target_type, target_id, evidence_source_id, status):
    return LoadedRecord(
        {
            "id": identifier,
            "publication_status": status,
            "created_at": "2026-09-03T12:00:00Z",
            "updated_at": "2026-09-03T12:00:00Z",
            "source_entity_type": source_type,
            "source_entity_id": source_id,
            "target_entity_type": target_type,
            "target_entity_id": target_id,
            "relationship_type": "related_to",
            "basis": "official",
            "rationale": None,
            "evidence_source_id": evidence_source_id,
            "verification_status": "verified",
        },
        Path(f"generated/{identifier}.json"),
    )


def _event(identifier, policy_id, document_id, source_id):
    return LoadedRecord(
        {
            "id": identifier,
            "publication_status": "published",
            "created_at": "2026-09-03T12:00:00Z",
            "updated_at": "2026-09-03T12:00:00Z",
            "event_type": "proposal",
            "event_date": "2026-09-03",
            "title": identifier,
            "description": "An event used to test the public export.",
            "policy_id": policy_id,
            "document_id": document_id,
            "source_id": source_id,
        },
        Path(f"generated/{identifier}.json"),
    )
