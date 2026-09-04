import json
from pathlib import Path


def test_seed_corpus_preserves_stable_identifiers_and_version_metadata():
    documents = {
        document["id"]: document
        for document in (
            json.loads(path.read_text(encoding="utf-8"))
            for path in Path("data/documents").glob("*.json")
        )
    }
    expected_id_slug_pairs = {
        "ai-act-proposal": "ai-act-proposal",
        "ai-liability-directive-proposal": "ai-liability-directive-proposal",
        "artificial-intelligence-act": "artificial-intelligence-act",
        "artificial-intelligence-for-europe": "artificial-intelligence-for-europe",
        "coordinated-plan-on-artificial-intelligence": "coordinated-plan-on-artificial-intelligence",
        "ethics-guidelines-for-trustworthy-ai": "ethics-guidelines-for-trustworthy-ai",
        "white-paper-on-artificial-intelligence": "white-paper-on-artificial-intelligence",
    }
    version_fields = {
        "record_level",
        "official_reference",
        "procedure_references",
        "oj_reference",
        "document_date",
        "version_label",
        "version_status",
    }

    assert {document_id: document["slug"] for document_id, document in documents.items()} == expected_id_slug_pairs
    assert all(document["record_level"] == "principal" for document in documents.values())
    assert all(version_fields <= document.keys() for document in documents.values())
    assert documents["artificial-intelligence-act"]["document_date"] == "2024-06-13"
    assert documents["artificial-intelligence-act"]["publication_date"] == "2024-07-12"
    assert documents["ai-act-proposal"]["official_reference"] == "COM(2021) 206 final"
    assert documents["ai-act-proposal"]["procedure_references"] == ["2021/0106(COD)"]
    assert documents["ai-act-proposal"]["version_status"] == "draft"
    assert documents["ai-liability-directive-proposal"]["version_status"] == "draft"
    assert all(
        documents[document_id]["version_status"] == "final"
        for document_id in set(documents) - {"ai-act-proposal", "ai-liability-directive-proposal"}
    )


def test_seed_corpus_uses_current_withdrawn_status_and_no_editorial_official_summaries():
    documents = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in Path("data/documents").glob("*.json")
    ]
    liability = next(document for document in documents if document["id"] == "ai-liability-directive-proposal")
    events = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in Path("data/events").glob("*.json")
    ]
    sources = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in Path("data/sources").glob("*.json")
    ]

    assert liability["legal_status"] == "withdrawn"
    assert "ai-liability-proposal-history-eur-lex" in liability["source_ids"]
    assert all(document["official_summary"] is None for document in documents)
    assert any(
        event["id"] == "ai-liability-proposal-publication"
        and event["event_type"] == "proposal"
        and event["event_date"] == "2022-09-28"
        for event in events
    )
    history = next(source for source in sources if source["id"] == "ai-liability-proposal-history-eur-lex")
    assert history["url"] == "https://eur-lex.europa.eu/legal-content/EN/HIS/?uri=CELEX:52022PC0496"
    assert "withdrawal" in history["verification_note"].lower()
    assert "6 October 2025" in history["verification_note"]
