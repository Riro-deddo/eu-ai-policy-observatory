import json
import sqlite3
from pathlib import Path
import subprocess
import sys

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


def test_module_cli_builds_repository_outputs(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "observatory.pipeline",
            "--project-root",
            str(Path.cwd()),
            "--timestamp",
            "2026-09-03T00:00:00Z",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
