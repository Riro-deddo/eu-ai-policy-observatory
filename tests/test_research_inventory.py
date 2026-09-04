import copy
import json
from pathlib import Path

import pytest

from observatory.validate import (
    RecordValidationError,
    assert_valid_research_inventory,
    validate_research_inventory,
)


SCHEMA_ROOT = Path("schema")


def _valid_sweep():
    return {
        "generated_at": "2026-09-04T00:00:00Z",
        "sources": [
            {
                "id": "eur-lex-procedure-2021-0106",
                "name": "EUR-Lex procedure 2021/0106/COD",
                "institution": "Publications Office of the European Union",
                "url": "https://eur-lex.europa.eu/procedure/EN/2021_106",
                "scope_note": "Official procedure record and linked documents.",
                "scan_status": "in_progress",
                "checked_at": "2026-09-04T00:00:00Z",
            }
        ],
    }


def _valid_inventory():
    return {
        "generated_at": "2026-09-04T00:00:00Z",
        "candidates": [
            {
                "id": "example-document",
                "source_ids": ["eur-lex-procedure-2021-0106"],
                "official_reference": "COM(2026) 1 final",
                "official_title": "Example document",
                "year": 2026,
                "issuing_institution": "European Commission",
                "record_level": "principal",
                "version_label": "Final",
                "official_source_url": "https://eur-lex.europa.eu/example",
                "decision": "included",
                "decision_reason": "The verified canonical document is within scope.",
                "document_id": "example-document",
                "merged_into_document_id": None,
            }
        ],
    }


def _write_research_files(tmp_path, sweep=None, inventory=None):
    research_root = tmp_path / "research"
    research_root.mkdir()
    (research_root / "source-sweep.json").write_text(
        json.dumps(sweep or _valid_sweep()), encoding="utf-8"
    )
    (research_root / "corpus-inventory.json").write_text(
        json.dumps(inventory or _valid_inventory()), encoding="utf-8"
    )
    return research_root


def test_repository_source_sweep_and_inventory_are_valid_and_auditable():
    assert validate_research_inventory(Path("research"), SCHEMA_ROOT, Path("data")) == []

    sweep = json.loads(Path("research/source-sweep.json").read_text(encoding="utf-8"))
    inventory = json.loads(
        Path("research/corpus-inventory.json").read_text(encoding="utf-8")
    )
    assert {source["scan_status"] for source in sweep["sources"]} <= {
        "pending",
        "in_progress",
        "complete",
    }
    assert {entry["decision"] for entry in inventory["candidates"]} <= {
        "included",
        "merged",
        "excluded",
        "pending",
    }
    assert all(entry["decision_reason"].strip() for entry in inventory["candidates"])


@pytest.mark.parametrize(
    ("mutate", "expected_field", "expected_code"),
    [
        (
            lambda sweep, inventory: sweep["sources"].append(
                copy.deepcopy(sweep["sources"][0])
            ),
            "sources.1.id",
            "duplicate_source_id",
        ),
        (
            lambda sweep, inventory: inventory["candidates"].append(
                copy.deepcopy(inventory["candidates"][0])
            ),
            "candidates.1.id",
            "duplicate_candidate_id",
        ),
        (
            lambda sweep, inventory: inventory["candidates"][0].update(
                {"decision_reason": "   "}
            ),
            "candidates.0.decision_reason",
            "blank_decision_reason",
        ),
        (
            lambda sweep, inventory: inventory["candidates"][0].update(
                {"document_id": "missing-document"}
            ),
            "candidates.0.document_id",
            "missing_inventory_document",
        ),
        (
            lambda sweep, inventory: inventory["candidates"][0].update(
                {"source_ids": ["missing-source"]}
            ),
            "candidates.0.source_ids.0",
            "missing_sweep_source",
        ),
        (
            lambda sweep, inventory: sweep["sources"][0].update(
                {"url": "http://eur-lex.europa.eu/procedure/EN/2021_106"}
            ),
            "sources.0.url",
            "schema",
        ),
        (
            lambda sweep, inventory: sweep["sources"][0].update(
                {"url": "https://example.com/not-an-eu-source"}
            ),
            "sources.0.url",
            "unofficial_url",
        ),
        (
            lambda sweep, inventory: inventory["candidates"][0].update(
                {"official_source_url": "https://example.com/not-an-eu-source"}
            ),
            "candidates.0.official_source_url",
            "unofficial_url",
        ),
    ],
)
def test_inventory_validator_rejects_broken_audit_contracts(
    tmp_path, mutate, expected_field, expected_code
):
    sweep = _valid_sweep()
    inventory = _valid_inventory()
    mutate(sweep, inventory)
    research_root = _write_research_files(tmp_path, sweep, inventory)

    issues = validate_research_inventory(
        research_root, SCHEMA_ROOT, Path("tests/fixtures/valid/data")
    )

    assert any(
        issue.field == expected_field and issue.code == expected_code for issue in issues
    )


@pytest.mark.parametrize(
    ("decision", "document_id", "merged_into", "expected_field"),
    [
        ("included", None, None, "candidates.0.document_id"),
        ("merged", None, None, "candidates.0.merged_into_document_id"),
        ("excluded", "example-document", None, "candidates.0.document_id"),
    ],
)
def test_inventory_decisions_require_consistent_document_links(
    tmp_path, decision, document_id, merged_into, expected_field
):
    inventory = _valid_inventory()
    inventory["candidates"][0].update(
        {
            "decision": decision,
            "document_id": document_id,
            "merged_into_document_id": merged_into,
        }
    )
    research_root = _write_research_files(tmp_path, inventory=inventory)

    issues = validate_research_inventory(
        research_root, SCHEMA_ROOT, Path("tests/fixtures/valid/data")
    )

    assert any(issue.field == expected_field for issue in issues)


def test_inventory_errors_raise_with_actionable_research_paths(tmp_path):
    inventory = _valid_inventory()
    inventory["candidates"][0]["document_id"] = "missing-document"
    research_root = _write_research_files(tmp_path, inventory=inventory)

    with pytest.raises(
        RecordValidationError,
        match=r"research/corpus-inventory\.json: candidates\.0\.document_id",
    ):
        assert_valid_research_inventory(
            research_root, SCHEMA_ROOT, Path("tests/fixtures/valid/data")
        )


def test_2018_to_2021_inventory_has_a_decision_for_every_published_anchor():
    inventory = json.loads(
        Path("research/corpus-inventory.json").read_text(encoding="utf-8")
    )
    candidates = {candidate["id"]: candidate for candidate in inventory["candidates"]}
    required_ids = {
        "coordinated-plan-2018-annex",
        "building-trust-human-centric-ai",
        "report-ai-safety-liability-2020",
        "altai-assessment-list",
        "coordinated-plan-2021-review",
        "coordinated-plan-2021-annex",
        "ai-act-proposal-annexes",
        "ai-act-impact-assessment-swd-2021-84",
        "ai-act-impact-assessment-annexes-swd-2021-84",
        "ai-act-impact-assessment-executive-summary-swd-2021-85",
        "ai-act-regulatory-scrutiny-board-opinion-sec-2021-167",
        "eesc-opinion-coordinated-plan-2021",
        "eesc-opinion-ai-act-2021",
        "cor-opinion-ai-act-2021",
        "ecb-opinion-con-2021-40",
        "edpb-edps-joint-opinion-5-2021",
    }

    assert required_ids <= candidates.keys()
    for candidate_id in required_ids:
        candidate = candidates[candidate_id]
        assert candidate["decision"] == "included"
        assert candidate["document_id"] == candidate_id
        assert candidate["merged_into_document_id"] is None


def test_2021_0106_procedure_sweep_is_complete_and_has_no_pending_candidates():
    sweep = json.loads(Path("research/source-sweep.json").read_text(encoding="utf-8"))
    inventory = json.loads(
        Path("research/corpus-inventory.json").read_text(encoding="utf-8")
    )
    sources = {source["id"]: source for source in sweep["sources"]}
    procedure_source_ids = {
        "eur-lex-procedure-2021-0106",
        "ep-oeil-2021-0106",
        "ep-adopted-texts-2021-0106",
        "council-register-2021-0106",
    }
    procedure_candidates = [
        candidate
        for candidate in inventory["candidates"]
        if procedure_source_ids & set(candidate["source_ids"])
    ]

    assert all(sources[source_id]["scan_status"] == "complete" for source_id in procedure_source_ids)
    assert procedure_candidates
    assert all(candidate["decision"] != "pending" for candidate in procedure_candidates)


def test_2022_to_2024_inventory_reconciles_required_official_records():
    inventory = json.loads(
        Path("research/corpus-inventory.json").read_text(encoding="utf-8")
    )
    candidates = {candidate["id"]: candidate for candidate in inventory["candidates"]}
    required_included_ids = {
        "ai-act-council-first-consolidated-compromise-st-10069-2022",
        "ai-act-council-second-compromise-st-11124-2022",
        "ai-act-council-third-compromise-part-one-st-12206-2022-rev-1",
        "ai-act-council-third-compromise-part-two-st-12549-2022",
        "ai-act-council-fourth-compromise-st-13102-2022",
        "ai-act-council-final-compromise-st-13955-2022",
        "ai-act-council-coreper-general-approach-st-14336-2022",
        "ai-act-council-general-approach-st-14954-2022",
        "council-general-approach-st-15698-2022",
        "ai-act-provisional-agreement-st-5662-2024",
        "ep-ai-act-draft-report-pe-731563",
        "ep-ai-act-envi-opinion-pe-699056",
        "ep-ai-act-itre-opinion-pe-719801",
        "ep-ai-act-cult-opinion-pe-719637",
        "ep-ai-act-tran-opinion-pe-730085",
        "ep-ai-act-juri-opinion-pe-719827",
        "ep-joint-committee-report-a9-0188-2023",
        "ep-position-p9-ta-2023-0236",
        "ep-position-p9-ta-2024-0138",
        "commission-decision-ai-office-2024",
        "standardisation-request-c-2023-3215",
    }

    assert required_included_ids <= candidates.keys()
    for candidate_id in required_included_ids:
        candidate = candidates[candidate_id]
        assert candidate["decision"] == "included"
        expected_document_id = (
            "ai-act-council-general-approach-st-15698-2022"
            if candidate_id == "council-general-approach-st-15698-2022"
            else (
                "ai-standardisation-request-c-2023-3215"
                if candidate_id == "standardisation-request-c-2023-3215"
                else candidate_id
            )
        )
        assert candidate["document_id"] == expected_document_id
        assert candidate["merged_into_document_id"] is None

    assert candidates["ai-act-corrigendum-2025-non-english"]["decision"] == "excluded"
    assert candidates["ai-act-corrigendum-2025-non-english"]["document_id"] is None
