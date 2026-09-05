import json

import pytest

from observatory.coverage import build_public_coverage_summary


def test_coverage_summary_counts_source_families_and_inventory_decisions(tmp_path):
    research_root = tmp_path / "research"
    research_root.mkdir()
    sources = [
        _source("reviewed-family-a", "Reviewed family", "reviewed"),
        _source("reviewed-family-b", "Reviewed family", "reviewed"),
        _source("not-started-family-a", "Not started family", "reviewed"),
        _source("not-started-family-b", "Not started family", "not_started"),
        _source("in-progress-family", "In progress family", "in_progress"),
        _source("gap-family-a", "Gap family", "recheck_due"),
        _source("gap-family-b", "Gap family", "gap_found"),
        _source("recheck-family", "Recheck family", "recheck_due"),
    ]
    candidates = [
        _candidate("included", "included"),
        _candidate("merged", "merged"),
        _candidate("excluded", "excluded"),
        _candidate("pending", "pending"),
    ]
    (research_root / "source-sweep.json").write_text(
        json.dumps(
            {
                "coverage_cutoff": "2026-09-04",
                "sources": sources,
            }
        ),
        encoding="utf-8",
    )
    (research_root / "corpus-inventory.json").write_text(
        json.dumps({"candidates": candidates}), encoding="utf-8"
    )

    summary = build_public_coverage_summary(research_root)

    assert summary == {
        "coverage_cutoff": "2026-09-04",
        "coverage_statement": (
            "An expanding corpus of official EU and European Communities AI-related "
            "documents. Verification dates and known coverage gaps are documented."
        ),
        "source_families": {
            "total": 5,
            "by_status": {
                "not_started": 1,
                "in_progress": 1,
                "reviewed": 1,
                "gap_found": 1,
                "recheck_due": 1,
            },
        },
        "inventory": {"included": 1, "merged": 1, "excluded": 1, "pending": 1},
        "unresolved_candidates": 1,
    }
    public_text = json.dumps(summary)
    for candidate in candidates:
        assert candidate["official_title"] not in public_text
        assert candidate["official_source_url"] not in public_text
        assert candidate["decision_reason"] not in public_text
    assert "Scope for reviewed-family-a only" not in public_text
    assert "covered_document_types" not in public_text
    assert "covered_sector_tags" not in public_text


@pytest.mark.parametrize(
    "status",
    ["not_started", "in_progress", "reviewed", "gap_found", "recheck_due"],
)
@pytest.mark.parametrize("decision", ["excluded", "pending"])
def test_cutoff_never_implies_completeness(tmp_path, status, decision):
    sweep = {
        "coverage_cutoff": "2026-09-04",
        "sources": [_source("bounded-search", "One family", status)],
    }
    inventory = {"candidates": [_candidate("private-candidate", decision)]}
    (tmp_path / "source-sweep.json").write_text(json.dumps(sweep), encoding="utf-8")
    (tmp_path / "corpus-inventory.json").write_text(
        json.dumps(inventory), encoding="utf-8"
    )
    result = build_public_coverage_summary(tmp_path)
    assert result["coverage_statement"] == (
        "An expanding corpus of official EU and European Communities AI-related "
        "documents. Verification dates and known coverage gaps are documented."
    )
    assert result["coverage_cutoff"] == "2026-09-04"
    assert result["unresolved_candidates"] == int(decision == "pending")
    assert "private-candidate" not in json.dumps(result)


def _source(identifier: str, source_family: str, scan_status: str) -> dict[str, object]:
    return {
        "id": identifier,
        "source_family": source_family,
        "scope_note": f"Scope for {identifier} only",
        "covered_through": "2026-09-04",
        "coverage_cutoff": "2026-09-04",
        "covered_document_types": [],
        "covered_sector_tags": [],
        "scan_status": scan_status,
    }


def _candidate(identifier: str, decision: str) -> dict[str, str]:
    return {
        "id": identifier,
        "official_title": f"Private title for {identifier}",
        "official_source_url": f"https://example.europa.eu/{identifier}",
        "decision": decision,
        "decision_reason": f"Private reason for {identifier}",
    }
