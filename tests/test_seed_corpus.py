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
    expected_version_statuses = {
        "ai-act-proposal": "draft",
        "ai-liability-directive-proposal": "draft",
        "artificial-intelligence-act": "final",
        "artificial-intelligence-for-europe": "final",
        "coordinated-plan-on-artificial-intelligence": "final",
        "ethics-guidelines-for-trustworthy-ai": "final",
        "white-paper-on-artificial-intelligence": "final",
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

    assert expected_id_slug_pairs.keys() <= documents.keys()
    seed_documents = {document_id: documents[document_id] for document_id in expected_id_slug_pairs}
    assert expected_id_slug_pairs.items() <= {
        document_id: document["slug"] for document_id, document in documents.items()
    }.items()
    assert all(document["record_level"] == "principal" for document in seed_documents.values())
    assert all(version_fields <= document.keys() for document in seed_documents.values())
    assert documents["artificial-intelligence-act"]["document_date"] == "2024-06-13"
    assert documents["artificial-intelligence-act"]["publication_date"] == "2024-07-12"
    assert documents["ai-act-proposal"]["official_reference"] == "COM(2021) 206 final"
    assert documents["ai-act-proposal"]["procedure_references"] == ["2021/0106(COD)"]
    assert {document_id: document["version_status"] for document_id, document in seed_documents.items()} == expected_version_statuses


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


def test_2018_to_2021_ai_act_pathway_anchor_documents_are_published():
    documents = {
        document["id"]: document
        for document in (
            json.loads(path.read_text(encoding="utf-8"))
            for path in Path("data/documents").glob("*.json")
        )
    }
    expected = {
        "artificial-intelligence-for-europe": ("COM(2018) 237 final", "52018DC0237"),
        "coordinated-plan-on-artificial-intelligence": ("COM(2018) 795 final", "52018DC0795"),
        "coordinated-plan-2018-annex": ("COM(2018) 795 final", None),
        "ethics-guidelines-for-trustworthy-ai": (None, None),
        "building-trust-human-centric-ai": ("COM(2019) 168 final", "52019DC0168"),
        "report-ai-safety-liability-2020": ("COM(2020) 64 final", "52020DC0064"),
        "white-paper-on-artificial-intelligence": ("COM(2020) 65 final", "52020DC0065"),
        "altai-assessment-list": (None, None),
        "coordinated-plan-2021-review": ("COM(2021) 205 final", "52021DC0205"),
        "coordinated-plan-2021-annex": ("COM(2021) 205 final", None),
        "ai-act-proposal": ("COM(2021) 206 final", "52021PC0206"),
        "ai-act-proposal-annexes": ("COM(2021) 206 final", None),
        "ai-act-impact-assessment-swd-2021-84": ("SWD(2021) 84 final", "52021SC0084"),
        "ai-act-impact-assessment-annexes-swd-2021-84": ("SWD(2021) 84 final", None),
        "ai-act-impact-assessment-executive-summary-swd-2021-85": ("SWD(2021) 85 final", "52021SC0085"),
        "ai-act-regulatory-scrutiny-board-opinion-sec-2021-167": ("SEC(2021) 167 final", None),
        "eesc-opinion-coordinated-plan-2021": ("EESC 2021/02456", "52021AE2456"),
        "eesc-opinion-ai-act-2021": ("EESC 2021/02482", "52021AE2482"),
        "cor-opinion-ai-act-2021": ("COR 2021/02682", "52021AR2682"),
        "ecb-opinion-con-2021-40": ("CON/2021/40", "52021AB0040"),
        "edpb-edps-joint-opinion-5-2021": ("Joint Opinion 5/2021", None),
    }

    assert expected.keys() <= documents.keys()
    for document_id, (official_reference, celex) in expected.items():
        document = documents[document_id]
        assert document["publication_status"] == "published"
        assert document["language"] == "en"
        assert document["official_reference"] == official_reference
        assert document["celex"] == celex
        assert document["source_ids"]
        assert document["corpus_assessment"]["review_status"] == "verified"


def test_2018_to_2021_attachments_and_procedural_steps_are_explicitly_related():
    relationships = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in Path("data/relationships").glob("*.json")
    ]
    relationship_keys = {
        (
            relationship["source_entity_id"],
            relationship["relationship_type"],
            relationship["target_entity_id"],
        )
        for relationship in relationships
    }

    assert {
        (
            "coordinated-plan-2018-annex",
            "annex_to",
            "coordinated-plan-on-artificial-intelligence",
        ),
        (
            "coordinated-plan-2021-annex",
            "annex_to",
            "coordinated-plan-2021-review",
        ),
        ("ai-act-proposal-annexes", "annex_to", "ai-act-proposal"),
        (
            "ai-act-impact-assessment-annexes-swd-2021-84",
            "annex_to",
            "ai-act-impact-assessment-swd-2021-84",
        ),
        (
            "ai-act-impact-assessment-swd-2021-84",
            "procedural_step_for",
            "ai-act-proposal",
        ),
        (
            "ai-act-impact-assessment-executive-summary-swd-2021-85",
            "procedural_step_for",
            "ai-act-proposal",
        ),
        (
            "edpb-edps-joint-opinion-5-2021",
            "procedural_step_for",
            "ai-act-proposal",
        ),
    } <= relationship_keys


def test_2018_to_2021_batch_defines_narrow_policies_and_missing_issuers():
    policies = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in Path("data/policies").glob("*.json")
    }
    institutions = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in Path("data/institutions").glob("*.json")
    }

    assert {
        "coordinated-european-ai-strategy",
        "artificial-intelligence-act-legislative-process",
    } <= policies
    assert {
        "european-economic-and-social-committee",
        "european-committee-of-the-regions",
        "european-central-bank",
        "european-data-protection-board",
        "european-data-protection-supervisor",
    } <= institutions


def test_2022_to_2024_ai_act_negotiation_and_implementation_records_are_published():
    documents = {
        document["id"]: document
        for document in (
            json.loads(path.read_text(encoding="utf-8"))
            for path in Path("data/documents").glob("*.json")
        )
    }
    expected_references = {
        "ai-act-council-first-consolidated-compromise-st-10069-2022": "ST 10069/22",
        "ai-act-council-second-compromise-st-11124-2022": "ST 11124/22",
        "ai-act-council-third-compromise-part-one-st-12206-2022-rev-1": "ST 12206/1/22 REV 1",
        "ai-act-council-third-compromise-part-two-st-12549-2022": "ST 12549/22",
        "ai-act-council-fourth-compromise-st-13102-2022": "ST 13102/22",
        "ai-act-council-final-compromise-st-13955-2022": "ST 13955/22",
        "ai-act-council-coreper-general-approach-st-14336-2022": "ST 14336/22",
        "ai-act-council-general-approach-st-14954-2022": "ST 14954/22",
        "ai-act-council-general-approach-st-15698-2022": "ST 15698/22",
        "ai-act-provisional-agreement-st-5662-2024": "ST 5662/24",
        "ep-ai-act-draft-report-pe-731563": "PE731.563",
        "ep-joint-committee-report-a9-0188-2023": "A9-0188/2023",
        "ep-position-p9-ta-2023-0236": "P9_TA(2023)0236",
        "ep-position-p9-ta-2024-0138": "P9_TA(2024)0138",
        "ai-act-pe-cons-24-2024": "PE-CONS 24/24",
        "ai-act-pe-cons-24-2024-rev-1": "PE-CONS 24/1/24 REV 1",
        "commission-decision-ai-office-2024": "C(2024) 390",
        "boosting-startups-innovation-trustworthy-ai": "COM(2024) 28 final",
        "ai-standardisation-request-c-2023-3215": "C(2023) 3215 final",
    }

    assert expected_references.keys() <= documents.keys()
    for document_id, official_reference in expected_references.items():
        document = documents[document_id]
        assert document["publication_status"] == "published"
        assert document["language"] == "en"
        assert document["official_reference"] == official_reference
        assert document["source_ids"]
        assert document["corpus_assessment"]["review_status"] == "verified"

    assert documents["ep-position-p9-ta-2023-0236"]["celex"] == "52023AP0236"
    assert documents["ep-position-p9-ta-2024-0138"]["celex"] == "52024AP0138"
    assert documents["commission-decision-ai-office-2024"]["eli"] == (
        "https://data.europa.eu/eli/C/2024/1459/oj"
    )
    assert documents["boosting-startups-innovation-trustworthy-ai"]["celex"] == (
        "52024DC0028"
    )


def test_2022_to_2024_formal_versions_and_positions_have_explicit_relationships():
    relationships = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in Path("data/relationships").glob("*.json")
    ]
    relationship_keys = {
        (
            relationship["source_entity_id"],
            relationship["relationship_type"],
            relationship["target_entity_id"],
        )
        for relationship in relationships
    }

    assert {
        ("ai-act-proposal", "adopted_as", "artificial-intelligence-act"),
        (
            "ai-act-council-second-compromise-st-11124-2022",
            "revises",
            "ai-act-council-first-consolidated-compromise-st-10069-2022",
        ),
        (
            "ai-act-council-fourth-compromise-st-13102-2022",
            "revises",
            "ai-act-council-third-compromise-part-two-st-12549-2022",
        ),
        (
            "ai-act-council-coreper-general-approach-st-14336-2022",
            "revises",
            "ai-act-council-final-compromise-st-13955-2022",
        ),
        (
            "ep-position-p9-ta-2023-0236",
            "procedural_step_for",
            "ai-act-proposal",
        ),
        (
            "ep-position-p9-ta-2024-0138",
            "revises",
            "ep-position-p9-ta-2023-0236",
        ),
        (
            "ep-position-p9-ta-2024-0138",
            "procedural_step_for",
            "ai-act-proposal",
        ),
        (
            "ai-act-pe-cons-24-2024-rev-1",
            "revises",
            "ai-act-pe-cons-24-2024",
        ),
        (
            "ai-act-council-general-approach-german-statement-14954-add-1",
            "annex_to",
            "ai-act-council-general-approach-st-14954-2022",
        ),
    } <= relationship_keys


def test_ai_act_and_liability_events_keep_distinct_document_and_event_dates():
    events = {
        event["id"]: event
        for event in (
            json.loads(path.read_text(encoding="utf-8"))
            for path in Path("data/events").glob("*.json")
        )
    }
    ai_act = json.loads(
        Path("data/documents/artificial-intelligence-act.json").read_text(
            encoding="utf-8"
        )
    )
    liability = json.loads(
        Path("data/documents/ai-liability-directive-proposal.json").read_text(
            encoding="utf-8"
        )
    )

    assert ai_act["document_date"] == "2024-06-13"
    assert ai_act["publication_date"] == "2024-07-12"
    assert events["artificial-intelligence-act-entry-into-force"]["event_date"] == (
        "2024-08-01"
    )
    assert events["artificial-intelligence-act-entry-into-force"]["event_type"] == (
        "entry_into_force"
    )
    assert liability["publication_date"] == "2022-09-28"
    assert events["ai-liability-directive-withdrawal"]["event_date"] == "2025-10-06"
    assert events["ai-liability-directive-withdrawal"]["event_type"] == "withdrawal"
