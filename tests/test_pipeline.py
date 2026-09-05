import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import observatory.pipeline as pipeline
from observatory.pipeline import run_pipeline
from observatory.validate import RecordValidationError


def test_repository_build_produces_database_and_public_export(tmp_path):
    outputs = run_pipeline(Path.cwd(), "2026-09-03T00:00:00Z", output_root=tmp_path)
    assert outputs.database.exists()
    assert outputs.public_json.exists()
    with sqlite3.connect(outputs.database) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    payload = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    assert len(payload["documents"]) >= 6
    assert all(item["publication_status"] == "published" for item in payload["documents"])
    assert payload["coverage"]["published_documents"] == len(payload["documents"])
    expected_principal_documents = sum(
        item["record_level"] == "principal" for item in payload["documents"]
    )
    assert payload["coverage"]["principal_documents"] == expected_principal_documents
    assert payload["coverage"]["supporting_files_and_versions"] == (
        len(payload["documents"]) - expected_principal_documents
    )
    assert payload["coverage"]["coverage_cutoff"] == "2026-09-04"
    assert payload["coverage"]["coverage_statement"] == (
        "An expanding corpus of official EU and European Communities AI-related "
        "documents. Verification dates and known coverage gaps are documented."
    )
    assert payload["coverage"]["inventory"] == {
        "included": 117,
        "merged": 18,
        "excluded": 22,
        "pending": 0,
    }
    assert payload["coverage"]["source_families"] == {
        "total": 13,
        "by_status": {
            "not_started": 0,
            "in_progress": 0,
            "reviewed": 13,
            "gap_found": 0,
            "recheck_due": 0,
        },
    }


def test_pipeline_excludes_unpublished_canonical_records_from_every_public_output(tmp_path):
    project_root = tmp_path / "project"
    shutil.copytree(Path("tests/fixtures/valid/data"), project_root / "data")
    shutil.copytree(Path("schema"), project_root / "schema")
    research_root = project_root / "research"
    research_root.mkdir()
    source_id = json.loads(
        (Path("research/source-sweep.json")).read_text(encoding="utf-8")
    )["sources"][0]["id"]
    (research_root / "source-sweep.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-09-04T00:00:00Z",
                "coverage_cutoff": "2026-09-04",
                "sources": [
                    {
                        "id": source_id,
                        "name": "Test source entrance",
                        "institution": "Publications Office of the European Union",
                        "source_family": "Test source family",
                        "url": "https://eur-lex.europa.eu/",
                        "scope_note": "Isolated pipeline fixture.",
                        "covered_from": "2018-01-01",
                        "covered_through": "2026-09-04",
                        "covered_document_types": ["communication"],
                        "covered_sector_tags": ["general_cross_sector"],
                        "discovery_method": "Reviewed the isolated fixture source.",
                        "scan_status": "reviewed",
                        "checked_at": "2026-09-04T00:00:00Z",
                        "coverage_cutoff": "2026-09-04",
                        "reviewer": "Test researcher",
                        "verification_note": "Fixture review completed.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (research_root / "corpus-inventory.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-09-04T00:00:00Z",
                "candidates": [
                    {
                        "id": "example-document",
                        "source_ids": [source_id],
                        "official_reference": "COM(2026) 1 final",
                        "official_title": "Example document",
                        "year": 2026,
                        "issuing_institution": "European Commission",
                        "record_level": "principal",
                        "version_label": "Final",
                        "official_source_url": "https://eur-lex.europa.eu/example",
                        "commissioning_body": None,
                        "candidate_provenance": "eu_institution_authored",
                        "provisional_sector_tags": ["general_cross_sector"],
                        "discovered_at": "2026-09-04T00:00:00Z",
                        "decision": "included",
                        "decision_reason": "Verified fixture document.",
                        "document_id": "example-document",
                        "merged_into_document_id": None,
                        "reviewed_at": "2026-09-04T00:00:00Z",
                        "reviewed_by": "Test researcher",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    draft_concept = json.loads(
        (project_root / "data" / "concepts" / "risk.json").read_text(encoding="utf-8")
    )
    draft_concept.update(
        {
            "id": "unpublished-concept",
            "publication_status": "draft",
            "name": "Unpublished concept",
        }
    )
    (project_root / "data" / "concepts" / "unpublished-concept.json").write_text(
        json.dumps(draft_concept), encoding="utf-8"
    )

    outputs = run_pipeline(
        project_root, "2026-09-03T00:00:00Z", output_root=tmp_path / "generated"
    )

    assert outputs.record_counts["concepts"] == 2
    with sqlite3.connect(outputs.database) as connection:
        for table in (
            "policies",
            "documents",
            "events",
            "concepts",
            "institutions",
            "relationships",
            "sources",
        ):
            assert connection.execute(
                f"SELECT DISTINCT publication_status FROM {table}"
            ).fetchall() in ([], [("published",)])
        assert connection.execute(
            "SELECT id FROM concepts WHERE id = 'unpublished-concept'"
        ).fetchall() == []
    public_payload = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    assert "unpublished-concept" not in {
        concept["id"] for concept in public_payload["concepts"]
    }


def test_module_cli_builds_repository_outputs(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("cli")
    project_root = _isolated_project_root(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "observatory.pipeline",
            "--project-root",
            str(project_root),
            "--timestamp",
            "2026-09-03T00:00:00Z",
        ],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(Path.cwd() / "src")},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_pipeline_rolls_back_both_outputs_when_public_json_publication_fails(tmp_path_factory, monkeypatch):
    tmp_path = tmp_path_factory.mktemp("rollback")
    output_root = tmp_path / "generated"
    output_root.mkdir()
    database = output_root / pipeline.DATABASE_FILENAME
    public_json = output_root / pipeline.PUBLIC_JSON_FILENAME
    database.write_bytes(b"database before failed publication")
    public_json.write_bytes(b"public JSON before failed publication")
    original_replace = pipeline.os.replace

    def fail_public_json_publication(source, destination):
        if Path(source).name == pipeline.PUBLIC_JSON_FILENAME and Path(destination) == public_json:
            raise OSError("forced public JSON publication failure")
        original_replace(source, destination)

    monkeypatch.setattr(pipeline.os, "replace", fail_public_json_publication)

    with pytest.raises(OSError, match="forced public JSON publication failure"):
        run_pipeline(Path.cwd(), "2026-09-03T00:00:00Z", output_root=output_root)

    assert database.read_bytes() == b"database before failed publication"
    assert public_json.read_bytes() == b"public JSON before failed publication"


def test_malformed_timestamp_does_not_touch_outputs_and_cli_reports_it(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("timestamp")
    output_root = tmp_path / "generated"
    output_root.mkdir()
    database = output_root / pipeline.DATABASE_FILENAME
    public_json = output_root / pipeline.PUBLIC_JSON_FILENAME
    database.write_bytes(b"database before malformed timestamp")
    public_json.write_bytes(b"public JSON before malformed timestamp")

    with pytest.raises(ValueError, match="build_timestamp must be an ISO-8601 UTC timestamp"):
        run_pipeline(Path.cwd(), "not-a-timestamp", output_root=output_root)

    assert database.read_bytes() == b"database before malformed timestamp"
    assert public_json.read_bytes() == b"public JSON before malformed timestamp"

    project_root = _isolated_project_root(tmp_path)
    cli_output = project_root / "generated"
    cli_output.mkdir()
    cli_database = cli_output / pipeline.DATABASE_FILENAME
    cli_public_json = cli_output / pipeline.PUBLIC_JSON_FILENAME
    cli_database.write_bytes(b"CLI database before malformed timestamp")
    cli_public_json.write_bytes(b"CLI public JSON before malformed timestamp")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "observatory.pipeline",
            "--project-root",
            str(project_root),
            "--timestamp",
            "not-a-timestamp",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "build_timestamp must be an ISO-8601 UTC timestamp" in result.stderr
    assert cli_database.read_bytes() == b"CLI database before malformed timestamp"
    assert cli_public_json.read_bytes() == b"CLI public JSON before malformed timestamp"


def test_deployment_workflow_normalises_commit_epoch_to_a_utc_build_timestamp():
    workflow = (Path(__file__).parents[1] / ".github" / "workflows" / "deploy-pages.yml").read_text(
        encoding="utf-8"
    )
    timestamp = datetime.fromtimestamp(1735689600, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    with pytest.raises(ValueError, match="ISO-8601 UTC timestamp"):
        pipeline._validate_build_timestamp("2025-01-01T01:00:00+01:00")
    pipeline._validate_build_timestamp(timestamp)

    assert timestamp == "2025-01-01T00:00:00Z"
    assert "git show -s --format=%ct HEAD" in workflow
    assert 'date -u -d "@$BUILD_EPOCH" +\'%Y-%m-%dT%H:%M:%SZ\'' in workflow
    assert "--format=%cI" not in workflow


@pytest.mark.parametrize("workflow_name", ["validate.yml", "deploy-pages.yml"])
def test_workflows_build_generated_data_before_running_tests(workflow_name: str):
    workflow = (
        Path(__file__).parents[1] / ".github" / "workflows" / workflow_name
    ).read_text(encoding="utf-8")

    build_command = "observatory-build --project-root . --timestamp"
    test_command = "python -m pytest -q"

    assert workflow.index(build_command) < workflow.index(test_command)


def test_invalid_provenance_fails_before_existing_outputs_are_touched(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("provenance")
    project_root = _isolated_project_root(tmp_path)
    source_path = project_root / "data" / "sources" / "ai-act-eur-lex.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["url"] = "file:///private/metadata.txt"
    source_path.write_text(json.dumps(source), encoding="utf-8")
    output_root = project_root / "generated"
    output_root.mkdir()
    database = output_root / pipeline.DATABASE_FILENAME
    public_json = output_root / pipeline.PUBLIC_JSON_FILENAME
    database.write_bytes(b"database before invalid provenance")
    public_json.write_bytes(b"public JSON before invalid provenance")

    with pytest.raises(RecordValidationError):
        run_pipeline(project_root, "2026-09-03T00:00:00Z", output_root=output_root)

    assert database.read_bytes() == b"database before invalid provenance"
    assert public_json.read_bytes() == b"public JSON before invalid provenance"


def test_invalid_inventory_fails_before_existing_outputs_are_touched(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("inventory")
    project_root = _isolated_project_root(tmp_path)
    inventory_path = project_root / "research" / "corpus-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory["candidates"][0]["document_id"] = "missing-document"
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
    output_root = project_root / "generated"
    output_root.mkdir()
    database = output_root / pipeline.DATABASE_FILENAME
    public_json = output_root / pipeline.PUBLIC_JSON_FILENAME
    database.write_bytes(b"database before invalid inventory")
    public_json.write_bytes(b"public JSON before invalid inventory")

    with pytest.raises(RecordValidationError, match="research/corpus-inventory.json"):
        run_pipeline(project_root, "2026-09-03T00:00:00Z", output_root=output_root)

    assert database.read_bytes() == b"database before invalid inventory"
    assert public_json.read_bytes() == b"public JSON before invalid inventory"


def test_malformed_coverage_cutoff_fails_before_existing_outputs_are_touched(
    tmp_path_factory,
):
    tmp_path = tmp_path_factory.mktemp("coverage-cutoff")
    project_root = _isolated_project_root(tmp_path)
    source_sweep_path = project_root / "research" / "source-sweep.json"
    source_sweep = json.loads(source_sweep_path.read_text(encoding="utf-8"))
    source_sweep["coverage_cutoff"] = "4 September 2026"
    source_sweep_path.write_text(json.dumps(source_sweep), encoding="utf-8")
    output_root = project_root / "generated"
    output_root.mkdir()
    database = output_root / pipeline.DATABASE_FILENAME
    public_json = output_root / pipeline.PUBLIC_JSON_FILENAME
    database.write_bytes(b"database before malformed coverage cutoff")
    public_json.write_bytes(b"public JSON before malformed coverage cutoff")

    with pytest.raises(RecordValidationError, match="research/source-sweep.json"):
        run_pipeline(project_root, "2026-09-03T00:00:00Z", output_root=output_root)

    assert database.read_bytes() == b"database before malformed coverage cutoff"
    assert public_json.read_bytes() == b"public JSON before malformed coverage cutoff"


def test_pending_inventory_candidate_is_absent_from_public_output(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("pending-inventory")
    project_root = _isolated_project_root(tmp_path)
    inventory_path = project_root / "research" / "corpus-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory["candidates"].append(
        {
            "id": "pending-secret-candidate",
            "source_ids": [inventory["candidates"][0]["source_ids"][0]],
            "official_reference": None,
            "official_title": "Pending candidate must not be published",
            "year": 2026,
            "issuing_institution": "European Commission",
            "record_level": "supporting",
            "version_label": None,
            "official_source_url": "https://commission.europa.eu/example-pending",
            "commissioning_body": None,
            "candidate_provenance": "unknown_pending_review",
            "provisional_sector_tags": [],
            "discovered_at": "2026-09-04T00:00:00Z",
            "decision": "pending",
            "decision_reason": "Metadata verification is not yet complete.",
            "document_id": None,
            "merged_into_document_id": None,
            "reviewed_at": None,
            "reviewed_by": None,
        }
    )
    inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

    outputs = run_pipeline(
        project_root, "2026-09-03T00:00:00Z", output_root=tmp_path / "generated"
    )

    public_text = outputs.public_json.read_text(encoding="utf-8")
    assert "Pending candidate must not be published" not in public_text
    assert "https://commission.europa.eu/example-pending" not in public_text
    assert "Metadata verification is not yet complete." not in public_text
    assert "pending-secret-candidate" not in public_text
    assert json.loads(public_text)["coverage"]["inventory"]["pending"] == 1


def _isolated_project_root(tmp_path):
    project_root = tmp_path / "project"
    shutil.copytree(Path.cwd() / "data", project_root / "data")
    shutil.copytree(Path.cwd() / "schema", project_root / "schema")
    shutil.copytree(Path.cwd() / "research", project_root / "research")
    return project_root
