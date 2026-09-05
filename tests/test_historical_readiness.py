from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from observatory.historical_readiness import (
    prospective_document_schema,
    validate_historical_readiness,
)
from observatory.io import LoadedRecord
from observatory.types import ENTITY_DIRECTORIES


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PROJECT_ROOT / "schema"
FIXTURE_ROOT = PROJECT_ROOT / "tests" / "fixtures" / "valid" / "data"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _citation(source_id: str = "example-source") -> dict:
    return {
        "source_id": source_id,
        "locator": "Synthetic fixture, section 1",
        "meaning": "Supports the stated date or classification.",
    }


@pytest.fixture
def complete_records() -> dict[str, list[LoadedRecord]]:
    document = deepcopy(_json(FIXTURE_ROOT / "documents" / "example-document.json"))
    document.update(
        {
            "document_type": "resolution",
            "document_date": "2017-02-16",
            "publication_date": "2018-07-18",
            "document_date_kind": "institutional_adoption",
            "temporal_collection": "historical_lineage",
            "relevance_class": "direct_ai_substantive",
            "date_evidence": {
                "document_date": _citation(),
                "publication_date": _citation(),
            },
            "classification_evidence": [
                {
                    "field": field,
                    "value": value,
                    "source_id": "example-source",
                    "locator": "Synthetic fixture, section 2",
                    "rationale": "The official fixture supports this supplied classification.",
                }
                for field, values in (
                    ("relevance_class", ["direct_ai_substantive"]),
                    ("sector_tags", document["sector_tags"]),
                    ("provenance_tags", document["provenance_tags"]),
                )
                for value in values
            ],
            "bibliographic_authors": [],
            "additional_dates": [],
            "institution_roles": [
                {
                    "institution_id": "european-commission",
                    "role": "author",
                    "evidence_source_id": "example-source",
                    "evidence_locator": "Synthetic fixture, title page",
                }
            ],
        }
    )
    document["corpus_assessment"].update(
        {
            "review_status": "verified",
            "reviewed_by": "Researcher",
            "reviewed_at": "2026-09-05T06:00:00Z",
            "inclusion_rationale": "Directly relevant after human review.",
        }
    )
    result = {directory: [] for directory in ENTITY_DIRECTORIES}
    result["documents"] = [LoadedRecord(document, Path("data/documents/example-document.json"))]
    result["sources"] = [
        LoadedRecord(
            deepcopy(_json(FIXTURE_ROOT / "sources" / "example-source.json")),
            Path("data/sources/example-source.json"),
        )
    ]
    result["institutions"] = [
        LoadedRecord(
            deepcopy(_json(FIXTURE_ROOT / "institutions" / "european-commission.json")),
            Path("data/institutions/european-commission.json"),
        )
    ]
    return result


def _issues(records):
    return validate_historical_readiness(records, SCHEMA_ROOT, "2026-09-04")


def _add_document(records, data, name):
    records["documents"].append(LoadedRecord(data, Path(f"data/documents/{name}.json")))


def _add_relationship(records, source_id, target_id, relationship_type, *, evidence="example-source", basis="official", rationale=None):
    data = {
        "id": f"{source_id}-{relationship_type}-{target_id}",
        "entity_type": "relationship",
        "publication_status": "published",
        "created_at": "2026-09-03T12:00:00Z",
        "updated_at": "2026-09-03T12:00:00Z",
        "source_entity_type": "document",
        "source_entity_id": source_id,
        "target_entity_type": "document",
        "target_entity_id": target_id,
        "relationship_type": relationship_type,
        "basis": basis,
        "rationale": rationale,
        "evidence_source_id": evidence,
        "verification_status": "verified",
    }
    records["relationships"].append(LoadedRecord(data, Path(f"data/relationships/{data['id']}.json")))


def test_2017_adoption_with_2018_oj_stays_historical(complete_records):
    assert _issues(complete_records) == []


def test_publication_cannot_be_inferred_from_issue_date(complete_records):
    del complete_records["documents"][0].data["date_evidence"]["publication_date"]
    assert any("date_evidence" in issue.field for issue in _issues(complete_records))


def test_retrieval_cannot_be_used_as_document_date_kind(complete_records):
    complete_records["documents"][0].data["document_date_kind"] = "retrieval"
    assert any(issue.field == "document_date_kind" for issue in _issues(complete_records))


def test_preflight_never_fills_missing_classification(complete_records):
    del complete_records["documents"][0].data["relevance_class"]
    before = deepcopy(complete_records)
    issues = _issues(complete_records)
    assert any(issue.field == "relevance_class" for issue in issues)
    assert complete_records == before


def test_undeclared_evidence_is_not_accepted(complete_records):
    complete_records["documents"][0].data["date_evidence"]["document_date"]["source_id"] = "unlisted-source"
    assert any(issue.code == "historical_evidence" for issue in _issues(complete_records))


def test_1975_document_is_eligible(complete_records):
    document = complete_records["documents"][0].data
    document["document_date"] = "1975-01-15"
    document["publication_date"] = "1975-02-01"
    assert _issues(complete_records) == []


@pytest.mark.parametrize("value", ["2025-02-29", "2024-13-01", "2024-2-01"])
def test_invalid_exact_dates_are_rejected(complete_records, value):
    complete_records["documents"][0].data["document_date"] = value
    assert any(issue.code == "historical_date" for issue in _issues(complete_records))


def test_valid_leap_date_is_accepted(complete_records):
    document = complete_records["documents"][0].data
    document["document_date"] = "2016-02-29"
    document["publication_date"] = "2016-03-01"
    assert _issues(complete_records) == []


@pytest.mark.parametrize("field", ["temporal_collection", "relevance_class", "document_date_kind", "date_evidence", "classification_evidence", "bibliographic_authors", "additional_dates"])
def test_required_historical_metadata_is_reported_by_field(complete_records, field):
    del complete_records["documents"][0].data[field]
    assert any(issue.field == field for issue in _issues(complete_records))


def test_wrong_temporal_collection_and_future_publication_fail(complete_records):
    document = complete_records["documents"][0].data
    document["temporal_collection"] = "contemporary_eu_ai_policy"
    document["publication_date"] = "2026-09-05"
    codes = {issue.code for issue in _issues(complete_records)}
    assert {"historical_collection", "historical_date"} <= codes


def test_published_draft_is_eligible(complete_records):
    document = complete_records["documents"][0].data
    document["version_status"] = "draft"
    document["legal_status"] = "proposed"
    assert _issues(complete_records) == []


@pytest.mark.parametrize(
    ("mutate", "field"),
    [
        (lambda d: d["classification_evidence"][0].update(value="not-on-document"), "classification_evidence"),
        (lambda d: d["classification_evidence"][0].update(locator="   "), "classification_evidence.0.locator"),
        (lambda d: d.update(classification_evidence=d["classification_evidence"][1:]), "classification_evidence"),
    ],
)
def test_classification_must_be_exact_nonblank_and_complete(complete_records, mutate, field):
    mutate(complete_records["documents"][0].data)
    assert any(issue.code == "historical_classification" and issue.field.startswith(field) for issue in _issues(complete_records))


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        (lambda records: records["sources"][0].data.update(url="http://commission.europa.eu/item"), "historical_evidence"),
        (lambda records: records["sources"][0].data.update(url="https://commission.europa.eu.evil.example/item"), "historical_evidence"),
        (lambda records: records["sources"].clear(), "historical_evidence"),
        (lambda records: records["sources"][0].data.update(publication_status="pending_review"), "historical_evidence"),
        (lambda records: records["sources"].append(deepcopy(records["sources"][0])), "historical_evidence"),
    ],
)
def test_evidence_requires_unique_published_official_https_source(complete_records, change, expected):
    change(complete_records)
    assert any(issue.code == expected for issue in _issues(complete_records))


def test_unknown_institution_and_duplicate_role_fail(complete_records):
    roles = complete_records["documents"][0].data["institution_roles"]
    roles[0]["institution_id"] = "unknown-body"
    roles.append(deepcopy(roles[0]))
    codes = {issue.code for issue in _issues(complete_records)}
    assert {"historical_attribution"} <= codes
    assert sum(issue.code == "historical_attribution" for issue in _issues(complete_records)) >= 2


def test_institution_role_must_resolve_uniquely(complete_records):
    complete_records["institutions"].append(deepcopy(complete_records["institutions"][0]))
    assert any(
        issue.code == "historical_attribution"
        and issue.field == "institution_roles.0.institution_id"
        for issue in _issues(complete_records)
    )


def test_externally_authored_study_accepts_ordered_people_and_commissioner(complete_records):
    document = complete_records["documents"][0].data
    document.update(document_type="study", document_date_kind="publication", document_date="2018-07-18", temporal_collection="contemporary_eu_ai_policy")
    document["provenance_tags"] = ["eu_commissioned_external", "officially_published"]
    document["classification_evidence"] = [item for item in document["classification_evidence"] if item["field"] != "provenance_tags"] + [
        {"field": "provenance_tags", "value": value, "source_id": "example-source", "locator": "credits", "rationale": "Explicitly credited."}
        for value in document["provenance_tags"]
    ]
    document["bibliographic_authors"] = [
        {"name": "First Person", "affiliation": "Example Institute", "evidence_source_id": "example-source", "evidence_locator": "p. 2"},
        {"name": "Second Person", "affiliation": None, "evidence_source_id": "example-source", "evidence_locator": "p. 2"},
    ]
    document["institution_roles"][0]["role"] = "commissioner"
    assert _issues(complete_records) == []
    assert [author["name"] for author in document["bibliographic_authors"]] == ["First Person", "Second Person"]


def test_external_commission_requires_named_author_and_commissioner(complete_records):
    document = complete_records["documents"][0].data
    document["provenance_tags"].append("eu_commissioned_external")
    document["classification_evidence"].append({"field": "provenance_tags", "value": "eu_commissioned_external", "source_id": "example-source", "locator": "credits", "rationale": "Commissioned work."})
    assert any(issue.code == "historical_attribution" for issue in _issues(complete_records))


def test_month_level_additional_date_is_retained_without_coercion(complete_records):
    document = complete_records["documents"][0].data
    document["additional_dates"] = [{"kind": "cover_issue", "value": "2017-02", "precision": "month", "source_id": "example-source", "locator": "cover"}]
    before = deepcopy(document["additional_dates"])
    assert _issues(complete_records) == []
    assert document["additional_dates"] == before


def test_additional_date_precision_must_match_value(complete_records):
    complete_records["documents"][0].data["additional_dates"] = [{"kind": "cover_issue", "value": "2017-02", "precision": "day", "source_id": "example-source", "locator": "cover"}]
    assert any(issue.code == "historical_date" and issue.field.startswith("additional_dates") for issue in _issues(complete_records))


def test_expired_status_requires_official_status_evidence(complete_records):
    complete_records["documents"][0].data["legal_status"] = "expired"
    assert any(issue.field == "legal_status_evidence" for issue in _issues(complete_records))
    complete_records["documents"][0].data["legal_status_evidence"] = _citation()
    assert _issues(complete_records) == []


def test_duplicate_2017_2018_manifestation_identity_is_rejected(complete_records):
    duplicate = deepcopy(complete_records["documents"][0].data)
    duplicate.update(id="example-document-oj", slug="example-document-oj", publication_date="2018-08-01")
    _add_document(complete_records, duplicate, "example-document-oj")
    assert any(issue.code == "historical_identity" for issue in _issues(complete_records))


@pytest.mark.parametrize(("level", "link_type"), [("version", "version_of"), ("attachment", "annex_to")])
def test_version_and_attachment_require_outgoing_parent_link(complete_records, level, link_type):
    complete_records["documents"][0].data["record_level"] = level
    assert any(issue.code == "historical_relationship" for issue in _issues(complete_records))
    parent = deepcopy(complete_records["documents"][0].data)
    parent.update(id="parent-document", slug="parent-document", record_level="principal", official_reference="PARENT", version_label=None)
    _add_document(complete_records, parent, "parent-document")
    _add_relationship(complete_records, "example-document", "parent-document", link_type)
    assert not any(issue.code == "historical_relationship" for issue in _issues(complete_records))


def test_valid_parent_is_not_overwritten_by_later_invalid_matching_edge(complete_records):
    complete_records["documents"][0].data["record_level"] = "version"
    parent = deepcopy(complete_records["documents"][0].data)
    parent.update(id="parent-document", slug="parent-document", record_level="principal", official_reference="PARENT", version_label=None)
    _add_document(complete_records, parent, "parent-document")
    _add_relationship(complete_records, "example-document", "parent-document", "version_of")
    _add_relationship(complete_records, "example-document", "parent-document", "revises", evidence="missing-source")
    complete_records["relationships"][-1] = LoadedRecord(
        {**complete_records["relationships"][-1].data, "id": "later-invalid-parent-edge"},
        Path("data/relationships/later-invalid-parent-edge.json"),
    )
    issues = _issues(complete_records)
    assert any(issue.record_path.endswith("later-invalid-parent-edge.json") for issue in issues)
    assert not any(issue.record_path.endswith("example-document.json") and issue.field == "record_level" for issue in issues)


def test_version_accepts_incoming_revises_from_nonattachment_peer(complete_records):
    complete_records["documents"][0].data["record_level"] = "version"
    later = deepcopy(complete_records["documents"][0].data)
    later.update(id="later-document", slug="later-document", record_level="principal", official_reference="LATER", version_label=None)
    _add_document(complete_records, later, "later-document")
    _add_relationship(complete_records, "later-document", "example-document", "revises")
    issues = _issues(complete_records)
    assert not any(issue.record_path.endswith("example-document.json") and issue.field == "record_level" for issue in issues)


def test_attachment_accepts_outgoing_part_of_parent(complete_records):
    complete_records["documents"][0].data["record_level"] = "attachment"
    parent = deepcopy(complete_records["documents"][0].data)
    parent.update(id="parent-document", slug="parent-document", record_level="principal", official_reference="PARENT", version_label=None)
    _add_document(complete_records, parent, "parent-document")
    _add_relationship(complete_records, "example-document", "parent-document", "part_of")
    issues = _issues(complete_records)
    assert not any(issue.record_path.endswith("example-document.json") and issue.field == "record_level" for issue in issues)


def test_attachment_version_accepts_outgoing_version_link_to_attachment(complete_records):
    complete_records["documents"][0].data["record_level"] = "attachment"
    prior_attachment = deepcopy(complete_records["documents"][0].data)
    prior_attachment.update(id="prior-attachment", slug="prior-attachment", official_reference="PRIOR-ATTACHMENT", version_label=None)
    _add_document(complete_records, prior_attachment, "prior-attachment")
    parent = deepcopy(complete_records["documents"][0].data)
    parent.update(id="parent-document", slug="parent-document", record_level="principal", official_reference="PARENT", version_label=None)
    _add_document(complete_records, parent, "parent-document")
    _add_relationship(complete_records, "example-document", "prior-attachment", "version_of")
    _add_relationship(complete_records, "prior-attachment", "parent-document", "annex_to")
    issues = _issues(complete_records)
    assert not any(issue.record_path.endswith("example-document.json") and issue.field == "record_level" for issue in issues)


def test_incoming_child_attachment_link_does_not_establish_parent_lineage(complete_records):
    complete_records["documents"][0].data["record_level"] = "attachment"
    child = deepcopy(complete_records["documents"][0].data)
    child.update(id="child-attachment", slug="child-attachment", official_reference="CHILD-ATTACHMENT", version_label=None)
    _add_document(complete_records, child, "child-attachment")
    _add_relationship(complete_records, "child-attachment", "example-document", "annex_to")
    issues = _issues(complete_records)
    assert any(issue.record_path.endswith("example-document.json") and issue.field == "record_level" for issue in issues)


def test_analytical_relationship_rejects_unofficial_evidence(complete_records):
    source = deepcopy(complete_records["sources"][0].data)
    source.update(id="blog-source", source_type="official_pdf", url="https://example.com/blog")
    complete_records["sources"].append(LoadedRecord(source, Path("data/sources/blog-source.json")))
    _add_relationship(complete_records, "example-document", "example-document", "related_to", evidence="blog-source", basis="analytical", rationale="Researcher interpretation.")
    assert any(issue.code == "historical_relationship" for issue in _issues(complete_records))


def test_validation_does_not_mutate_any_input(complete_records):
    before = deepcopy(complete_records)
    _issues(complete_records)
    assert complete_records == before


def test_malformed_nested_shapes_report_issues_instead_of_crashing(complete_records):
    document = complete_records["documents"][0].data
    document["relevance_class"] = []
    document["sector_tags"] = [["invalid"]]
    document["classification_evidence"][0]["value"] = {"invalid": True}
    document["institution_roles"][0]["institution_id"] = ["invalid"]
    document["language"] = {"invalid": True}
    assert any(issue.code == "historical_schema" for issue in _issues(complete_records))


def test_prospective_schema_is_document_only_and_does_not_mutate_active_schema():
    schema_path = SCHEMA_ROOT / "record.schema.json"
    before = schema_path.read_bytes()
    active = json.loads(before)
    prospective = prospective_document_schema(SCHEMA_ROOT)
    complete = deepcopy(_json(FIXTURE_ROOT / "documents" / "example-document.json"))
    complete.update({
        "temporal_collection": "historical_lineage", "relevance_class": "direct_ai_substantive", "document_date_kind": "publication",
        "date_evidence": {"document_date": _citation(), "publication_date": _citation()}, "classification_evidence": [{"field": "relevance_class", "value": "direct_ai_substantive", "source_id": "example-source", "locator": "x", "rationale": "x"}],
        "bibliographic_authors": [], "additional_dates": [],
    })
    assert len(prospective["$defs"]) >= 7
    assert list(prospective["oneOf"]) == [{"$ref": "#/$defs/document"}]
    assert not Draft202012Validator(active, format_checker=FormatChecker()).is_valid(complete)
    assert schema_path.read_bytes() == before


def test_extension_schema_resolves_its_local_references():
    extension = _json(SCHEMA_ROOT / "historical-document-extension.schema.json")
    candidate = {
        "temporal_collection": "historical_lineage",
        "relevance_class": "direct_ai_substantive",
        "document_date_kind": "publication",
        "date_evidence": {"document_date": _citation(), "publication_date": _citation()},
        "classification_evidence": [{"field": "relevance_class", "value": "direct_ai_substantive", "source_id": "example-source", "locator": "p. 1", "rationale": "Explicit."}],
        "bibliographic_authors": [],
        "additional_dates": [],
    }
    assert Draft202012Validator(extension, format_checker=FormatChecker()).is_valid(candidate)


def _baseline_pairs(payload):
    return {(item["id"], item["slug"]) for item in payload["documents"]}


def _published_pairs(records):
    return {(record.data.get("id"), record.data.get("slug")) for record in records["documents"] if record.data.get("publication_status") == "published"}


def test_route_baseline_is_preserved_but_allows_additions():
    baseline = _json(PROJECT_ROOT / "research" / "migrations" / "2026-09-05-public-document-baseline.json")
    from observatory.io import load_records
    current = load_records(PROJECT_ROOT / "data")
    expected = _baseline_pairs(baseline)
    assert len(expected) == 117
    assert expected <= _published_pairs(current)
    added = deepcopy(current)
    added["documents"].append(LoadedRecord({"id": "future-document", "slug": "future-document", "publication_status": "published"}, Path("future.json")))
    assert expected <= _published_pairs(added)
    removed = deepcopy(current)
    removed["documents"] = removed["documents"][1:]
    assert not expected <= _published_pairs(removed)
    changed = deepcopy(current)
    changed["documents"][0].data["slug"] = "changed-route"
    assert not expected <= _published_pairs(changed)


def _write_cli_project(root: Path, complete_records, *, include_document=True):
    (root / "schema").mkdir(parents=True)
    for name in ("record.schema.json", "historical-document-extension.schema.json"):
        (root / "schema" / name).write_bytes((SCHEMA_ROOT / name).read_bytes())
    for directory in ENTITY_DIRECTORIES:
        (root / "data" / directory).mkdir(parents=True)
        for record in complete_records[directory]:
            if directory == "documents" and not include_document:
                continue
            (root / "data" / directory / record.path.name).write_text(json.dumps(record.data), encoding="utf-8")


def _tree_bytes(root: Path):
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def _run_cli(root: Path, cutoff="2026-09-04"):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "observatory.historical_readiness", "--project-root", str(root), "--publication-cutoff", cutoff],
        cwd=PROJECT_ROOT, capture_output=True, text=True, check=False, env=environment,
    )


def test_cli_ready_output_is_deterministic_and_read_only(tmp_path, complete_records):
    _write_cli_project(tmp_path, complete_records)
    before = _tree_bytes(tmp_path)
    result = _run_cli(tmp_path)
    assert result.returncode == 0
    assert json.loads(result.stdout) == {
        "contract_version": "historical-readiness-1", "publication_contract_active": False,
        "publication_cutoff": "2026-09-04", "documents_checked": 1, "documents_ready": 1, "issues": [],
    }
    assert _tree_bytes(tmp_path) == before


def test_cli_incomplete_record_reports_issue_and_exit_one(tmp_path, complete_records):
    del complete_records["documents"][0].data["relevance_class"]
    _write_cli_project(tmp_path, complete_records)
    result = _run_cli(tmp_path)
    payload = json.loads(result.stdout)
    assert result.returncode == 1
    assert payload["documents_checked"] == 1 and payload["documents_ready"] == 0
    assert payload["issues"] == sorted(payload["issues"], key=lambda item: (item["record_path"], item["field"], item["code"], item["message"]))


def test_cli_relationship_issue_makes_source_document_not_ready(tmp_path, complete_records):
    _add_relationship(
        complete_records,
        "example-document",
        "example-document",
        "related_to",
        evidence="missing-source",
        basis="analytical",
        rationale="Synthetic analytical edge.",
    )
    _write_cli_project(tmp_path, complete_records)
    result = _run_cli(tmp_path)
    payload = json.loads(result.stdout)
    assert result.returncode == 1
    assert payload["documents_checked"] == 1 and payload["documents_ready"] == 0


@pytest.mark.parametrize("cutoff", ["2026-9-04", "2026-02-29", "today"])
def test_cli_rejects_malformed_cutoff_without_traceback(tmp_path, complete_records, cutoff):
    _write_cli_project(tmp_path, complete_records)
    result = _run_cli(tmp_path, cutoff)
    assert result.returncode == 2
    assert "error" in result.stderr.lower() and "traceback" not in result.stderr.lower()


def test_cli_empty_or_malformed_input_fails_closed(tmp_path, complete_records):
    empty = tmp_path / "empty"
    _write_cli_project(empty, complete_records, include_document=False)
    result = _run_cli(empty)
    assert result.returncode == 2 and "error" in result.stderr.lower()
    malformed = tmp_path / "malformed"
    _write_cli_project(malformed, complete_records)
    (malformed / "data" / "documents" / "example-document.json").write_text("{broken", encoding="utf-8")
    result = _run_cli(malformed)
    assert result.returncode == 2 and "traceback" not in result.stderr.lower()


def test_cli_non_object_json_fails_closed_without_traceback(tmp_path, complete_records):
    _write_cli_project(tmp_path, complete_records)
    (tmp_path / "data" / "documents" / "example-document.json").write_text("[]", encoding="utf-8")
    result = _run_cli(tmp_path)
    assert result.returncode == 2
    assert "error" in result.stderr.lower() and "traceback" not in result.stderr.lower()
