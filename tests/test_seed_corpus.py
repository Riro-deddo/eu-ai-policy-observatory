import json
from pathlib import Path


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
