"""Repository-level admission traceability, independent of document counts."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_every_published_document_has_an_included_inventory_decision():
    """Catch an admitted document silently omitted from the screening ledger."""
    inventory = json.loads((ROOT / "research/corpus-inventory.json").read_text(encoding="utf-8"))
    included = {
        candidate["document_id"]
        for candidate in inventory["candidates"]
        if candidate["decision"] == "included"
    }
    published = {
        document["id"]
        for path in (ROOT / "data/documents").glob("*.json")
        for document in [json.loads(path.read_text(encoding="utf-8"))]
        if document["publication_status"] == "published"
    }
    assert published - included == set(), "Published documents missing their inclusion decision"
