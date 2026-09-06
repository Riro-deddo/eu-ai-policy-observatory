from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import sqlite3

from observatory.historical_readiness import validate_historical_readiness
from observatory.io import load_records
from observatory.pipeline import run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = PROJECT_ROOT / "data"
SCHEMA_ROOT = PROJECT_ROOT / "schema"
LEDGER_PATH = PROJECT_ROOT / "research" / "migrations" / "2026-09-05-relationship-evidence-migration.json"
FROZEN_BASELINE_PATH = PROJECT_ROOT / "research" / "migrations" / "2026-09-05-public-document-baseline.json"
EXPANDED_LEDGER_PATH = PROJECT_ROOT / "research" / "migrations" / "2026-09-05-expanded-evidence-review.json"
SIX_RECORD_LEDGER_PATH = PROJECT_ROOT / "research" / "migrations" / "2026-09-06-six-record-evidence-update.json"
REVIEW_TIMESTAMP = "2026-09-05T07:35:00Z"

RESOLVED_TARGETS = {
    "gpai-code-final-copyright",
    "gpai-code-final-safety-security",
    "gpai-code-final-transparency",
    "gpai-code-third-draft-commitments",
    "gpai-code-third-draft-copyright",
    "gpai-code-third-draft-safety-security",
    "gpai-code-third-draft-transparency",
    "gpai-code-model-documentation-form-2025",
    "gpai-code-signatory-form-2025",
    "transparency-code-signatory-form-2026",
}
HELD_TARGETS = {
    "draft-high-risk-classification-guidelines-2026",
    "draft-high-risk-classification-guidelines-annex-i-2026",
    "draft-high-risk-classification-guidelines-annex-iii-2026",
    "draft-guidance-serious-ai-incidents-2025",
    "draft-serious-ai-incident-report-template-2025",
}

EXPECTED_EDGES = {
    "gpai-code-final-copyright-version-of-final": (
        "gpai-code-final-copyright",
        "gpai-code-final",
        "part_of",
        "official",
        "gpai-code-final-commission",
    ),
    "gpai-code-final-safety-version-of-final": (
        "gpai-code-final-safety-security",
        "gpai-code-final",
        "part_of",
        "official",
        "gpai-code-final-commission",
    ),
    "gpai-code-final-transparency-version-of-final": (
        "gpai-code-final-transparency",
        "gpai-code-final",
        "part_of",
        "official",
        "gpai-code-final-commission",
    ),
    "gpai-code-third-draft-commitments-part-of-third-draft": (
        "gpai-code-third-draft-commitments",
        "gpai-code-third-draft",
        "part_of",
        "official",
        "gpai-code-third-draft-commission",
    ),
    "gpai-code-third-draft-copyright-part-of-third-draft": (
        "gpai-code-third-draft-copyright",
        "gpai-code-third-draft",
        "part_of",
        "official",
        "gpai-code-third-draft-commission",
    ),
    "gpai-code-third-draft-safety-security-part-of-third-draft": (
        "gpai-code-third-draft-safety-security",
        "gpai-code-third-draft",
        "part_of",
        "official",
        "gpai-code-third-draft-commission",
    ),
    "gpai-code-third-draft-transparency-part-of-third-draft": (
        "gpai-code-third-draft-transparency",
        "gpai-code-third-draft",
        "part_of",
        "official",
        "gpai-code-third-draft-commission",
    ),
    "gpai-code-model-documentation-form-supports-final": (
        "gpai-code-model-documentation-form-2025",
        "gpai-code-final",
        "related_to",
        "official",
        "gpai-code-final-commission",
    ),
    "gpai-code-signatory-form-supports-final": (
        "gpai-code-signatory-form-2025",
        "gpai-code-final",
        "related_to",
        "official",
        "gpai-code-final-commission",
    ),
    "transparency-code-signatory-form-supports-final": (
        "transparency-code-signatory-form-2026",
        "transparency-code-final-2026",
        "related_to",
        "official",
        "transparency-code-signatory-commission",
    ),
}

EXPECTED_SIBLING_EDGES = {
    "high-risk-annex-i-version-of-draft": (
        "draft-high-risk-classification-guidelines-annex-i-2026",
        "draft-high-risk-classification-guidelines-2026",
        "related_to",
        "analytical",
        "high-risk-guidelines-draft-commission",
    ),
    "high-risk-annex-iii-version-of-draft": (
        "draft-high-risk-classification-guidelines-annex-iii-2026",
        "draft-high-risk-classification-guidelines-2026",
        "related_to",
        "analytical",
        "high-risk-guidelines-draft-commission",
    ),
}


def _records_by_id(records: dict[str, list], directory: str) -> dict[str, dict]:
    return {record.data["id"]: record.data for record in records[directory]}


def _edge_tuple(edge: dict) -> tuple[str, str, str, str, str]:
    return (
        edge["source_entity_id"],
        edge["target_entity_id"],
        edge["relationship_type"],
        edge["basis"],
        edge["evidence_source_id"],
    )


def test_component_and_supporting_edges_are_exact_and_verified():
    records = load_records(DATA_ROOT)
    relationships = _records_by_id(records, "relationships")

    for relationship_id, expected in EXPECTED_EDGES.items():
        relationship = relationships[relationship_id]
        assert _edge_tuple(relationship) == expected
        assert relationship["publication_status"] == "published"
        assert relationship["verification_status"] == "verified"
        assert relationship["updated_at"] == REVIEW_TIMESTAMP


def test_record_levels_statuses_and_published_identity_routes_are_preserved():
    records = load_records(DATA_ROOT)
    documents = _records_by_id(records, "documents")
    baseline = json.loads(FROZEN_BASELINE_PATH.read_text(encoding="utf-8"))
    expanded = json.loads(EXPANDED_LEDGER_PATH.read_text(encoding="utf-8"))
    expanded_audit = {
        item["document_id"]: item for item in expanded["record_audit"]
    }

    expected_forms = {
        "gpai-code-model-documentation-form-2025": "final",
        "gpai-code-signatory-form-2025": "final",
        "transparency-code-signatory-form-2026": "final",
    }
    for document_id, version_status in expected_forms.items():
        document = documents[document_id]
        audit = expanded_audit[document_id]
        assert document["record_level"] == "supporting"
        assert document["version_status"] == version_status
        assert audit["decision"] == "upgrade"
        assert audit["before"]["updated_at"] == REVIEW_TIMESTAMP
        assert audit["before"]["corpus_reviewed_by"] == "Yichen Hao"
        assert audit["before"]["corpus_reviewed_at"] == "2026-09-04T00:00:00Z"
        assert document["updated_at"] == audit["after"]["updated_at"]
        assert "Codex" in document["corpus_assessment"]["researcher_notes"]
        assert document["corpus_assessment"]["reviewed_by"] == audit["after"]["corpus_reviewed_by"]
        assert document["corpus_assessment"]["reviewed_at"] == audit["after"]["corpus_reviewed_at"]

    published_routes = {
        (record.data["id"], record.data["slug"])
        for record in records["documents"]
        if record.data["publication_status"] == "published"
    }
    baseline_routes = {(document["id"], document["slug"]) for document in baseline["documents"]}
    reviewed_routes = {(document["id"], document["slug"])
                       for document in expanded["baseline"]["documents"]}
    assert len(reviewed_routes) == 131
    assert reviewed_routes <= published_routes
    assert baseline_routes <= published_routes


def test_general_principles_and_siblings_preserve_old_hold_then_gain_real_parent():
    records = load_records(DATA_ROOT)
    documents = _records_by_id(records, "documents")
    relationships = _records_by_id(records, "relationships")

    general = documents["draft-high-risk-classification-guidelines-2026"]
    assert general["record_level"] == "attachment"
    assert general["version_status"] == "draft"
    assert datetime.fromisoformat(general["updated_at"]) >= datetime.fromisoformat(REVIEW_TIMESTAMP)
    for relationship_id, expected in EXPECTED_SIBLING_EDGES.items():
        relationship = relationships[relationship_id]
        assert _edge_tuple(relationship) == expected
        assert "sibling sections" in relationship["rationale"]
        assert "not versions or annexes" in relationship["rationale"]

    issues = validate_historical_readiness(records, SCHEMA_ROOT, "2026-09-04")
    relationship_holds = {
        Path(issue.record_path).stem
        for issue in issues
        if issue.code == "historical_relationship" and issue.field == "record_level"
    }
    # The 5 September ledger remains an immutable hold decision. The later
    # chronological ledger resolves the three section holds through a real parent.
    old_ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    old_held = {row["document_id"] for row in old_ledger["targets"] if row["status"] == "held"}
    upgraded = set(json.loads(SIX_RECORD_LEDGER_PATH.read_text(encoding="utf-8"))["upgraded_existing_ids"])
    assert upgraded <= old_held
    assert relationship_holds & upgraded == set()
    for document_id in upgraded:
        edge_id = f"{document_id}-part-of-consultation-work"
        edge = relationships[edge_id]
        assert edge["target_entity_id"] == "draft-high-risk-classification-guidelines-consultation-work-2026"
        assert edge["relationship_type"] == "part_of"
        assert edge["basis"] == "official"


def test_evidence_ledger_covers_exact_review_scope_with_concrete_sources():
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    targets = ledger["targets"]
    target_ids = {target["document_id"] for target in targets}

    assert len(targets) == 15
    assert target_ids == RESOLVED_TARGETS | HELD_TARGETS
    assert {target["document_id"] for target in targets if target["status"] == "resolved"} == RESOLVED_TARGETS
    assert {target["document_id"] for target in targets if target["status"] == "held"} == HELD_TARGETS
    assert all(target["before_record_level"] in {"version", "attachment"} for target in targets)
    assert all(target["after_record_level"] in {"version", "attachment", "supporting"} for target in targets)
    assert all(target["action_rationale"].strip() for target in targets)
    assert all(target.get("hold_reason", "").strip() for target in targets if target["status"] == "held")

    assert ledger["review"] == {
        "reviewed_at": REVIEW_TIMESTAMP,
        "publication_cutoff": "2026-09-04",
        "reviewer": "Codex",
        "base_commit": "f4085fdf6ada9da4954f815738ff2b8bffe81ec0",
    }
    evidence = {item["source_id"]: item for item in ledger["source_evidence"]}
    assert set(evidence) == {
        "gpai-code-final-commission",
        "gpai-code-third-draft-commission",
        "high-risk-guidelines-draft-commission",
        "transparency-code-signatory-commission",
        "high-risk-incident-consultation-commission",
    }
    assert all(item["url"].startswith("https://digital-strategy.ec.europa.eu/") for item in evidence.values())
    assert evidence["transparency-code-signatory-commission"]["corroborating_url"] == "https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content"
    assert all(item["locators"] and all(locator.strip() for locator in item["locators"]) for item in evidence.values())
    assert all(item["binary_interiors_verified"] is False for item in evidence.values())
    assert all(item["source_snapshot_retained"] is False for item in evidence.values())
    assert ledger["generated_artifacts"]["status"] == "pre-migration_pending_controlled_rebuild"


def test_pipeline_exports_migration_to_json_and_sqlite_without_identity_drift(tmp_path):
    outputs = run_pipeline(PROJECT_ROOT, REVIEW_TIMESTAMP, output_root=tmp_path / "output")
    public_data = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    baseline = json.loads(FROZEN_BASELINE_PATH.read_text(encoding="utf-8"))
    documents = {document["id"]: document for document in public_data["documents"]}
    relationships = {relationship["id"]: relationship for relationship in public_data["relationships"]}

    canonical = load_records(DATA_ROOT)
    published_ids = {
        entity: {record.data["id"] for record in canonical[entity]
                 if record.data["publication_status"] == "published"}
        for entity in ("documents", "relationships")
    }
    for entity in ("documents", "relationships"):
        assert outputs.record_counts[entity] == len(canonical[entity])
        assert sorted(item["id"] for item in public_data[entity]) == sorted(published_ids[entity])
    assert {(item["id"], item["slug"]) for item in baseline["documents"]} <= {
        (item["id"], item["slug"]) for item in public_data["documents"]
    }
    assert documents["gpai-code-model-documentation-form-2025"]["record_level"] == "supporting"
    assert documents["gpai-code-signatory-form-2025"]["record_level"] == "supporting"
    assert documents["transparency-code-signatory-form-2026"]["record_level"] == "supporting"
    assert documents["draft-high-risk-classification-guidelines-2026"]["record_level"] == "attachment"
    for relationship_id, expected in EXPECTED_EDGES.items():
        assert _edge_tuple(relationships[relationship_id]) == expected
    for relationship_id, expected in EXPECTED_SIBLING_EDGES.items():
        assert _edge_tuple(relationships[relationship_id]) == expected

    with sqlite3.connect(outputs.database) as connection:
        assert {row[0] for row in connection.execute("SELECT id FROM documents")} == published_ids["documents"]
        assert {row[0] for row in connection.execute("SELECT id FROM relationships")} == published_ids["relationships"]
        sqlite_routes = set(connection.execute("SELECT id, slug FROM documents"))
        sqlite_levels = dict(
            connection.execute(
                "SELECT id, record_level FROM documents WHERE id IN (?, ?, ?, ?)",
                (
                    "gpai-code-model-documentation-form-2025",
                    "gpai-code-signatory-form-2025",
                    "transparency-code-signatory-form-2026",
                    "draft-high-risk-classification-guidelines-2026",
                ),
            )
        )
        expected_sqlite_edges = {**EXPECTED_EDGES, **EXPECTED_SIBLING_EDGES}
        sqlite_edges = {
            row[0]: row[1:]
            for row in connection.execute(
                "SELECT id, source_entity_id, target_entity_id, relationship_type, basis, evidence_source_id "
                "FROM relationships WHERE id IN ({})".format(",".join("?" for _ in expected_sqlite_edges)),
                tuple(expected_sqlite_edges),
            )
        }

    assert sqlite_routes == {
        (item["id"], item["slug"]) for item in public_data["documents"]
    }
    assert {(item["id"], item["slug"]) for item in baseline["documents"]} <= sqlite_routes
    assert sqlite_levels == {
        "draft-high-risk-classification-guidelines-2026": "attachment",
        "gpai-code-model-documentation-form-2025": "supporting",
        "gpai-code-signatory-form-2025": "supporting",
        "transparency-code-signatory-form-2026": "supporting",
    }
    assert sqlite_edges == expected_sqlite_edges
