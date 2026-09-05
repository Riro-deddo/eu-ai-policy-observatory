from copy import deepcopy
import json
from pathlib import Path
import shutil
import sqlite3

import pytest

from observatory.historical_publication import validate_historical_publication
from observatory.io import LoadedRecord, load_records
from observatory.pipeline import run_pipeline


def test_historical_batch_round_trips_without_losing_old_routes(tmp_path):
    outputs = run_pipeline(
        Path.cwd(),
        "2026-09-05T12:00:00Z",
        output_root=tmp_path,
    )
    payload = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    docs = {row["id"]: row for row in payload["documents"]}
    baseline = json.loads(
        Path("research/migrations/2026-09-05-public-document-baseline.json").read_text(
            encoding="utf-8"
        )
    )

    assert all(docs[row["id"]]["slug"] == row["slug"] for row in baseline["documents"])
    esprit = docs["council-decision-84-130-eec-esprit"]
    assert esprit["document_date"] == "1984-02-28"
    assert esprit["temporal_collection"] == "historical_lineage"
    assert esprit["relevance_class"] == "ai_related_precursor"
    assert esprit["date_evidence"]["publication_date"]["locator"]
    robotics = docs["civil-law-rules-on-robotics-resolution-2017"]
    assert robotics["document_date"] == "2017-02-16"
    assert robotics["publication_date"] == "2018-07-18"
    assert robotics["temporal_collection"] == "historical_lineage"
    assert sum(row["celex"] == "52017IP0051" for row in docs.values()) == 1
    with sqlite3.connect(outputs.database) as connection:
        assert connection.execute(
            "SELECT document_id FROM research_subset_documents "
            "WHERE subset_id = 'database-seed-v1' ORDER BY document_id"
        ).fetchall() == [
            ("ai-act-proposal",),
            ("ai-liability-directive-proposal",),
            ("artificial-intelligence-act",),
            ("artificial-intelligence-for-europe",),
            ("coordinated-plan-on-artificial-intelligence",),
            ("ethics-guidelines-for-trustworthy-ai",),
            ("white-paper-on-artificial-intelligence",),
        ]


def test_legacy_role_evidence_cannot_bypass_complete_extension_gate(tmp_path):
    data_root = tmp_path / "data"
    shutil.copytree(Path("data"), data_root)
    document_path = data_root / "documents" / "white-paper-on-artificial-intelligence.json"
    document = json.loads(document_path.read_text(encoding="utf-8"))
    document["institution_roles"][0].update(
        {
            "evidence_source_id": document["source_ids"][0],
            "evidence_locator": "Official title block",
        }
    )
    document_path.write_text(json.dumps(document), encoding="utf-8")

    issues = validate_historical_publication(
        load_records(data_root),
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )

    assert any(
        issue.field == "historical_review_status"
        and "partial" in issue.message.lower()
        for issue in issues
    )


def test_unknown_new_legacy_like_document_is_rejected():
    records = load_records(Path("data"))
    legacy = next(
        record
        for record in records["documents"]
        if record.data.get("id") == "white-paper-on-artificial-intelligence"
    )
    legacy.data["id"] = "unlisted-new-document"
    legacy.data["slug"] = "unlisted-new-document"

    issues = validate_historical_publication(
        records,
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )

    assert any(
        issue.field == "historical_review_status"
        and "new published document" in issue.message.lower()
        for issue in issues
    )


def test_scalar_only_historical_extension_is_rejected_as_partial():
    records = load_records(Path("data"))
    legacy = next(
        record
        for record in records["documents"]
        if record.data.get("id") == "white-paper-on-artificial-intelligence"
    )
    legacy.data["historical_review_status"] = "verified"

    issues = validate_historical_publication(
        records,
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )

    assert any(
        issue.field == "historical_review_status"
        and "partial" in issue.message.lower()
        for issue in issues
    )


@pytest.mark.parametrize(
    "publication_status",
    [
        pytest.param("pending_review", id="pending"),
        pytest.param("draft", id="unverified"),
    ],
)
def test_gate_rejects_pending_or_unverified_evidence_source(publication_status):
    records = load_records(Path("data"))
    document = _document(records, "council-decision-84-130-eec-esprit")
    source_id = document.data["date_evidence"]["document_date"]["source_id"]
    source = next(row for row in records["sources"] if row.data.get("id") == source_id)
    source.data["publication_status"] = publication_status

    issues = _publication_issues(records)

    assert any(
        issue.code == "historical_evidence"
        and "must be published" in issue.message.lower()
        for issue in issues
    )


def test_gate_rejects_undeclared_evidence_source():
    records = load_records(Path("data"))
    document = _document(records, "council-decision-84-130-eec-esprit")
    source_id = document.data["date_evidence"]["document_date"]["source_id"]
    document.data["source_ids"].remove(source_id)

    issues = _publication_issues(records)

    assert any(
        issue.code == "historical_evidence"
        and "not declared" in issue.message.lower()
        for issue in issues
    )


@pytest.mark.parametrize(
    ("missing_citation", "expected_code", "field_fragment"),
    [
        ("tag", "historical_classification", "classification_evidence"),
        ("date", "historical_schema", "date_evidence.publication_date"),
        ("role", "historical_schema", "institution_roles.0.evidence_locator"),
    ],
)
def test_gate_rejects_missing_tag_date_or_role_citation(
    missing_citation, expected_code, field_fragment
):
    records = load_records(Path("data"))
    document = _document(records, "council-decision-84-130-eec-esprit")
    if missing_citation == "tag":
        document.data["classification_evidence"].pop(0)
    elif missing_citation == "date":
        document.data["date_evidence"].pop("publication_date")
    else:
        document.data["institution_roles"][0].pop("evidence_locator")

    issues = _publication_issues(records)

    assert any(
        issue.code == expected_code and field_fragment in issue.field
        for issue in issues
    )


def test_gate_rejects_publication_after_cutoff():
    records = load_records(Path("data"))
    document = _document(records, "council-decision-84-130-eec-esprit")
    document.data["publication_date"] = "2026-09-05"

    issues = _publication_issues(records)

    assert any(
        issue.code == "historical_date" and issue.field == "publication_date"
        for issue in issues
    )


def test_gate_rejects_historical_identity_duplicate():
    records = load_records(Path("data"))
    original = _document(records, "council-decision-84-130-eec-esprit")
    duplicate = deepcopy(original.data)
    duplicate.update(
        id="council-decision-84-130-eec-esprit-duplicate",
        slug="council-decision-84-130-eec-esprit-duplicate",
    )
    records["documents"].append(
        LoadedRecord(
            duplicate,
            Path("data/documents/council-decision-84-130-eec-esprit-duplicate.json"),
        )
    )

    issues = _publication_issues(records)

    assert any(issue.code == "historical_identity" for issue in issues)


def test_gate_accepts_fully_evidenced_pre_1984_fixture():
    records = load_records(Path("tests/fixtures/valid/data"))
    document = _document(records, "example-document")
    citation = {
        "source_id": "example-source",
        "locator": "Synthetic official fixture, title page",
        "meaning": "The fixture supplies this historical publication date.",
    }
    document.data.update(
        historical_review_status="verified",
        temporal_collection="historical_lineage",
        relevance_class="direct_ai_substantive",
        document_date_kind="publication",
        document_date="1975-01-15",
        publication_date="1975-01-15",
        date_evidence={
            "document_date": deepcopy(citation),
            "publication_date": deepcopy(citation),
        },
        classification_evidence=[
            {
                "field": field,
                "value": value,
                "source_id": "example-source",
                "locator": "Synthetic official fixture, section 1",
                "rationale": "The fixture supports this supplied classification.",
            }
            for field, values in (
                ("relevance_class", ["direct_ai_substantive"]),
                ("sector_tags", document.data["sector_tags"]),
                ("provenance_tags", document.data["provenance_tags"]),
            )
            for value in values
        ],
        bibliographic_authors=[],
        additional_dates=[],
    )
    document.data["institution_roles"][0].update(
        evidence_source_id="example-source",
        evidence_locator="Synthetic official fixture, title page",
    )

    assert _publication_issues(records) == []


def _document(records, document_id):
    return next(
        row for row in records["documents"] if row.data.get("id") == document_id
    )


def _publication_issues(records):
    return validate_historical_publication(
        records,
        Path("schema"),
        "2026-09-04",
        Path("research/migrations/2026-09-05-public-document-baseline.json"),
    )
