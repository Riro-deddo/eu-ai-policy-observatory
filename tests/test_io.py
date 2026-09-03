from pathlib import Path

from observatory.io import load_records


def test_load_records_preserves_source_path():
    loaded = load_records(Path("tests/fixtures/valid/data"))
    document = loaded["documents"][0]
    assert document.data["id"] == "example-document"
    assert document.path.as_posix().endswith("documents/example-document.json")
