"""Assert historical fingerprints across an explicitly recorded label-only change."""
import hashlib
import json


def assert_preserved_lf_hash(root, relative_path, original_hash):
    ledger = json.loads(
        (root / "research/migrations/2026-09-06-neutral-review-labels.json").read_text(encoding="utf-8")
    )
    normalization = ledger["normalized_file_hashes"].get(relative_path)
    expected = original_hash
    if normalization is not None:
        assert normalization["original_sha256_lf"] == original_hash
        expected = normalization["normalized_sha256_lf"]
    current = (root / relative_path).read_text(encoding="utf-8").encode("utf-8")
    assert hashlib.sha256(current).hexdigest() == expected
