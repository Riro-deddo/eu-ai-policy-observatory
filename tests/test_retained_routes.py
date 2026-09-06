"""Regression coverage for the three reviewed retained section routes."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import sqlite3

import pytest

from observatory.historical_readiness import validate_historical_readiness
from observatory.io import load_records
from observatory.pipeline import RecordValidationError, run_pipeline
from observatory.validate import validate_records


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema/record.schema.json"
VOCABULARY = ROOT / "schema/controlled-vocabularies.json"
LEDGER = ROOT / "research/migrations/2026-09-05-retained-section-notices.json"
BASELINE = ROOT / "research/migrations/2026-09-05-public-document-baseline.json"
REVIEWED_AT = "2026-09-05T08:59:02Z"
LANDING_SOURCE = "high-risk-guidelines-draft-commission"
HELD = {
    "draft-high-risk-classification-guidelines-2026": (
        "commission-newsroom-128559-pdf",
        "General principles",
    ),
    "draft-high-risk-classification-guidelines-annex-i-2026": (
        "commission-newsroom-128560-pdf",
        "Article 6(1) and AI Act Annex I",
    ),
    "draft-high-risk-classification-guidelines-annex-iii-2026": (
        "commission-newsroom-128561-pdf",
        "Article 6(2) and AI Act Annex III",
    ),
}
LANDING_LOCATOR = (
    "Publication date; paragraph immediately before Downloads explaining the "
    "separate sections; Downloads 1–3."
)
PDF_LOCATOR = "Pages 1–2 (cover and first body page)."


def _notice(document_id: str) -> dict[str, object]:
    pdf_source, section = HELD[document_id]
    reason = (
        f"This record contains the {section} section of the draft Commission "
        "guidelines. The Observatory has not admitted a separate record for the "
        "whole guidelines; the parent relationship remains under review. This "
        "existing route is retained for access. The document remains a consultation draft."
    )
    if "Annex" in section:
        reason += (
            " The annex designation identifies the AI Act annex addressed; it does "
            "not make this file an annex to the General principles section."
        )
    return {
        "status": "parent_relationship_under_review",
        "reason": reason,
        "reviewed_by": "Codex",
        "reviewed_at": REVIEWED_AT,
        "evidence": [
            {"source_id": LANDING_SOURCE, "locator": LANDING_LOCATOR},
            {"source_id": pdf_source, "locator": PDF_LOCATOR},
        ],
    }


def _copy_data(tmp_path: Path) -> Path:
    destination = tmp_path / "data"
    shutil.copytree(ROOT / "data", destination)
    return destination


def _inject_valid_notices(data_root: Path) -> None:
    for document_id in HELD:
        path = data_root / "documents" / f"{document_id}.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        document["updated_at"] = REVIEWED_AT
        document["retained_route_notice"] = _notice(document_id)
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def _document(data_root: Path, document_id: str) -> tuple[Path, dict[str, object]]:
    path = data_root / "documents" / f"{document_id}.json"
    return path, json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _issues(data_root: Path):
    return validate_records(data_root, SCHEMA, VOCABULARY)


def _notice_issues(data_root: Path):
    return [issue for issue in _issues(data_root) if issue.code == "retained_route_notice"]


def test_scoped_published_sections_require_a_notice(tmp_path):
    data_root = _copy_data(tmp_path)
    for document_id in HELD:
        path, document = _document(data_root, document_id)
        document.pop("retained_route_notice")
        _save(path, document)
    assert {
        Path(issue.record_path).stem
        for issue in _notice_issues(data_root)
        if issue.field == "retained_route_notice"
    } == set(HELD)


def test_exact_reviewed_notices_are_accepted(tmp_path):
    data_root = _copy_data(tmp_path)
    _inject_valid_notices(data_root)
    assert _notice_issues(data_root) == []


def test_malformed_nested_source_ids_return_issues_without_throwing(tmp_path):
    data_root = _copy_data(tmp_path)
    path, document = _document(data_root, next(iter(HELD)))
    document["source_ids"] = [{"not": "hashable"}]
    _save(path, document)

    issues = _issues(data_root)

    assert any(issue.code == "schema" and issue.field.startswith("source_ids") for issue in issues)
    assert any(
        issue.code == "retained_route_notice"
        and issue.field.startswith("retained_route_notice.evidence")
        for issue in issues
    )


@pytest.mark.parametrize(
    ("mutation", "field"),
    [
        (lambda notice: notice.update(status="pending"), "retained_route_notice.status"),
        (lambda notice: notice.pop("reason"), "retained_route_notice.reason"),
        (lambda notice: notice.update(reason="   "), "retained_route_notice.reason"),
        (lambda notice: notice.pop("reviewed_by"), "retained_route_notice.reviewed_by"),
        (lambda notice: notice.update(reviewed_by=""), "retained_route_notice.reviewed_by"),
        (
            lambda notice: notice["evidence"][0].pop("locator"),
            "retained_route_notice.evidence.0.locator",
        ),
        (
            lambda notice: notice["evidence"][0].update(locator=" \t "),
            "retained_route_notice.evidence.0.locator",
        ),
        (
            lambda notice: notice.update(reviewed_at="2026-09-05T08:59:02"),
            "retained_route_notice.reviewed_at",
        ),
        (
            lambda notice: notice.update(reviewed_at="2026-09-03T23:59:59Z"),
            "retained_route_notice.reviewed_at",
        ),
        (
            lambda notice: notice.update(reviewed_at="2026-09-05T09:00:00Z"),
            "retained_route_notice.reviewed_at",
        ),
        (lambda notice: notice.update(extra="not allowed"), "retained_route_notice"),
    ],
)
def test_notice_shape_and_review_window_are_strict(tmp_path, mutation, field):
    data_root = _copy_data(tmp_path)
    _inject_valid_notices(data_root)
    path, document = _document(data_root, next(iter(HELD)))
    mutation(document["retained_route_notice"])
    _save(path, document)
    assert any(issue.field.startswith(field) for issue in _issues(data_root))


@pytest.mark.parametrize(
    "case",
    [
        "missing_source",
        "unpublished_source",
        "nonofficial_source",
        "unlinked_source",
        "duplicate_evidence",
        "duplicate_source_record",
        "wrong_pdf",
    ],
)
def test_notice_evidence_must_be_exact_linked_unique_published_and_official(
    tmp_path, case
):
    data_root = _copy_data(tmp_path)
    _inject_valid_notices(data_root)
    document_id = next(iter(HELD))
    pdf_source = HELD[document_id][0]
    path, document = _document(data_root, document_id)
    notice = document["retained_route_notice"]
    if case == "missing_source":
        notice["evidence"][1]["source_id"] = "missing-source"
    elif case == "unpublished_source":
        source_path = data_root / "sources" / f"{pdf_source}.json"
        source = json.loads(source_path.read_text(encoding="utf-8"))
        source["publication_status"] = "pending_review"
        _save(source_path, source)
    elif case == "nonofficial_source":
        source_path = data_root / "sources" / f"{pdf_source}.json"
        source = json.loads(source_path.read_text(encoding="utf-8"))
        source["url"] = "https://example.com/not-official.pdf"
        _save(source_path, source)
    elif case == "unlinked_source":
        document["source_ids"].remove(pdf_source)
    elif case == "duplicate_evidence":
        notice["evidence"][1] = deepcopy(notice["evidence"][0])
    elif case == "duplicate_source_record":
        source_path = data_root / "sources" / f"{pdf_source}.json"
        shutil.copyfile(source_path, data_root / "sources" / "duplicate-source.json")
    elif case == "wrong_pdf":
        wrong = HELD["draft-high-risk-classification-guidelines-annex-i-2026"][0]
        notice["evidence"][1]["source_id"] = wrong
        document["source_ids"].append(wrong)
    _save(path, document)
    assert any(
        issue.field.startswith("retained_route_notice.evidence")
        for issue in _notice_issues(data_root)
    )


def test_non_object_notice_returns_issues_without_throwing(tmp_path):
    data_root = _copy_data(tmp_path)
    path, document = _document(data_root, next(iter(HELD)))
    document["retained_route_notice"] = "under review"
    _save(path, document)

    issues = _issues(data_root)

    assert any(issue.code == "schema" for issue in issues)
    assert any(
        issue.code == "retained_route_notice"
        and issue.field == "retained_route_notice"
        for issue in issues
    )


@pytest.mark.parametrize(
    ("document_id", "mutate"),
    [
        (
            "artificial-intelligence-act",
            lambda document: document.update(
                retained_route_notice=_notice(next(iter(HELD))),
                updated_at=REVIEWED_AT,
            ),
        ),
        (next(iter(HELD)), lambda document: document.update(record_level="principal")),
        (next(iter(HELD)), lambda document: document.update(version_status="final")),
        (next(iter(HELD)), lambda document: document.update(publication_status="pending_review")),
    ],
)
def test_notice_is_rejected_outside_the_reviewed_record_contract(
    tmp_path, document_id, mutate
):
    data_root = _copy_data(tmp_path)
    _inject_valid_notices(data_root)
    path, document = _document(data_root, document_id)
    mutate(document)
    _save(path, document)
    assert any(
        Path(issue.record_path).stem == document_id for issue in _notice_issues(data_root)
    )


def test_notice_is_stale_after_a_genuine_evidenced_parent_link(tmp_path):
    data_root = _copy_data(tmp_path)
    _inject_valid_notices(data_root)
    document_id = next(iter(HELD))
    _, section = _document(data_root, document_id)
    parent_id = "draft-high-risk-classification-guidelines-whole-2026"
    parent = deepcopy(section)
    parent.update(
        id=parent_id,
        slug=parent_id,
        official_title="Draft Commission Guidelines on the classification of high-risk AI systems",
        short_title="Draft high-risk classification guidelines — complete work",
        record_level="principal",
        version_label="Consultation draft — complete work",
        source_ids=[LANDING_SOURCE],
        snapshots=[],
    )
    parent.pop("retained_route_notice")
    _save(data_root / "documents" / f"{parent_id}.json", parent)
    relationship = {
        "id": "reviewed-section-part-of-ai-act",
        "entity_type": "relationship",
        "publication_status": "published",
        "created_at": REVIEWED_AT,
        "updated_at": REVIEWED_AT,
        "source_entity_type": "document",
        "source_entity_id": document_id,
        "target_entity_type": "document",
        "target_entity_id": parent_id,
        "relationship_type": "part_of",
        "basis": "official",
        "rationale": None,
        "evidence_source_id": LANDING_SOURCE,
        "verification_status": "verified",
    }
    _save(data_root / "relationships" / "reviewed-section-part-of-ai-act.json", relationship)
    assert any(
        Path(issue.record_path).stem == document_id
        and issue.field == "retained_route_notice"
        for issue in _notice_issues(data_root)
    )


def test_real_pipeline_round_trips_notices_without_changing_routes_or_holds(tmp_path):
    first = run_pipeline(ROOT, "2026-09-05T09:00:00Z", output_root=tmp_path / "first")
    second = run_pipeline(ROOT, "2026-09-05T09:00:00Z", output_root=tmp_path / "second")
    public = json.loads(first.public_json.read_text(encoding="utf-8"))
    documents = {document["id"]: document for document in public["documents"]}
    frozen = json.loads(BASELINE.read_text(encoding="utf-8"))["documents"]
    canonical = load_records(ROOT / "data")
    for entity in ("documents", "relationships"):
        assert sorted(item["id"] for item in public[entity]) == sorted(
            record.data["id"] for record in canonical[entity]
            if record.data["publication_status"] == "published"
        )
    assert {(row["id"], row["slug"]) for row in frozen} <= {
        (row["id"], row["slug"]) for row in public["documents"]
    }
    assert {
        key
        for key, row in documents.items()
        if row["retained_route_notice"] is not None
    } == set(HELD)
    assert documents["artificial-intelligence-act"]["retained_route_notice"] is None
    assert first.public_json.read_bytes() == second.public_json.read_bytes()

    with sqlite3.connect(first.database) as connection:
        evidence_foreign_keys = {
            row[2]
            for row in connection.execute(
                "PRAGMA foreign_key_list(document_retained_route_evidence)"
            )
        }
        notice_rows = connection.execute(
            "SELECT document_id, status, reason, reviewed_by, reviewed_at "
            "FROM document_retained_route_notices ORDER BY document_id"
        ).fetchall()
        evidence_rows = connection.execute(
            "SELECT document_id, evidence_order, source_id, locator "
            "FROM document_retained_route_evidence ORDER BY document_id, evidence_order"
        ).fetchall()
    assert {"documents", "document_retained_route_notices", "sources"} <= evidence_foreign_keys
    assert [row[0] for row in notice_rows] == sorted(HELD)
    assert all(row[1] == "parent_relationship_under_review" for row in notice_rows)
    assert all(row[3:] == ("Codex", REVIEWED_AT) for row in notice_rows)
    assert len(evidence_rows) == 6
    for document_id in sorted(HELD):
        expected = _notice(document_id)
        assert documents[document_id]["retained_route_notice"] == expected
        assert [row[1:] for row in evidence_rows if row[0] == document_id] == [
            (index, item["source_id"], item["locator"])
            for index, item in enumerate(expected["evidence"])
        ]

    historical = validate_historical_readiness(
        load_records(ROOT / "data"), ROOT / "schema", "2026-09-04"
    )
    assert {
        Path(issue.record_path).stem
        for issue in historical
        if issue.code == "historical_relationship" and issue.field == "record_level"
    } == set(HELD)


def test_invalid_notice_blocks_pipeline_without_replacing_outputs(tmp_path):
    project = tmp_path / "project"
    for directory in ("data", "schema", "research"):
        shutil.copytree(ROOT / directory, project / directory)
    output = tmp_path / "output"
    run_pipeline(project, "2026-09-05T09:00:00Z", output_root=output)
    prior = {path.name: path.read_bytes() for path in output.iterdir()}
    path, document = _document(project / "data", next(iter(HELD)))
    document["retained_route_notice"]["evidence"][0]["locator"] = " "
    _save(path, document)

    with pytest.raises(RecordValidationError):
        run_pipeline(project, "2026-09-05T09:01:00Z", output_root=output)

    assert {path.name: path.read_bytes() for path in output.iterdir()} == prior


def test_migration_ledger_replays_only_declared_document_changes():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert ledger["review"]["reviewed_by"] == "Codex"
    assert ledger["review"]["reviewed_at"] == REVIEWED_AT
    assert ledger["existing_state"] == {
        "published_documents": 117,
        "published_relationships": 95,
        "historical_relationship_holds": sorted(HELD),
    }
    assert {item["document_id"] for item in ledger["documents"]} == set(HELD)
    for item in ledger["documents"]:
        current = json.loads((ROOT / item["path"]).read_text(encoding="utf-8"))
        replayed = deepcopy(item["before"])
        replayed.update(item["after_changes"])
        assert current == replayed
        assert set(item["after_changes"]) <= {
            "updated_at",
            "short_title",
            "retained_route_notice",
        }
