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
