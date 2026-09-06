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
    current = (root / relative_path).read_text(encoding="utf-8")
    if relative_path == "data/documents/council-decision-84-130-eec-esprit.json":
        # Reconstruct the earlier bytes across the two expressly documented
        # bibliography changes. Every other byte must still match its old hash.
        # See research/migrations/2026-09-06-academic-readiness.md.
        record = json.loads(current)
        assert record["oj_reference"] == "OJ L 67, 9.3.1984, pp. 54–59"
        assert record["updated_at"] == "2026-09-06T21:03:47Z"
        current = current.replace('"oj_reference": "OJ L 67, 9.3.1984, pp. 54–59"', '"oj_reference": null')
        current = current.replace('"updated_at": "2026-09-06T21:03:47Z"', '"updated_at": "2026-09-05T11:54:18Z"')
    assert hashlib.sha256(current.encode("utf-8")).hexdigest() == expected
