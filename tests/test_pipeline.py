import json
import sqlite3
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import observatory.pipeline as pipeline
from observatory.pipeline import run_pipeline


def test_repository_build_produces_database_and_public_export(tmp_path):
    outputs = run_pipeline(Path.cwd(), "2026-09-03T00:00:00Z", output_root=tmp_path)
    assert outputs.database.exists()
    assert outputs.public_json.exists()
    with sqlite3.connect(outputs.database) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
    payload = json.loads(outputs.public_json.read_text(encoding="utf-8"))
    assert len(payload["documents"]) >= 6
    assert all(item["publication_status"] == "published" for item in payload["documents"])


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


def _isolated_project_root(tmp_path):
    project_root = tmp_path / "project"
    shutil.copytree(Path.cwd() / "data", project_root / "data")
    shutil.copytree(Path.cwd() / "schema", project_root / "schema")
    return project_root
