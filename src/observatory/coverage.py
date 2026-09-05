"""Aggregate publication-safe coverage metadata from the research audit."""

from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
from typing import Mapping, cast


SOURCE_STATUSES = (
    "not_started",
    "in_progress",
    "reviewed",
    "gap_found",
    "recheck_due",
)
SOURCE_STATUS_PRIORITY = ("gap_found", "recheck_due", "in_progress", "not_started")
INVENTORY_DECISIONS = ("included", "merged", "excluded", "pending")
PUBLIC_COVERAGE_STATEMENT = (
    "An expanding corpus of official EU and European Communities AI-related "
    "documents. Verification dates and known coverage gaps are documented."
)


def build_public_coverage_summary(research_root: Path) -> dict[str, object]:
    """Return aggregate-only coverage metadata from validated audit files."""
    root = Path(research_root)
    source_sweep = cast(
        Mapping[str, object],
        json.loads((root / "source-sweep.json").read_text(encoding="utf-8")),
    )
    inventory = cast(
        Mapping[str, object],
        json.loads((root / "corpus-inventory.json").read_text(encoding="utf-8")),
    )

    family_rows: dict[str, list[str]] = defaultdict(list)
    for source in cast(list[Mapping[str, object]], source_sweep["sources"]):
        family_rows[cast(str, source["source_family"])].append(
            cast(str, source["scan_status"])
        )
    family_counts = Counter(_family_status(statuses) for statuses in family_rows.values())

    decision_counts = Counter(
        cast(str, candidate["decision"])
        for candidate in cast(list[Mapping[str, object]], inventory["candidates"])
    )
    candidates = cast(list[Mapping[str, object]], inventory["candidates"])
    pending_by_source = Counter(
        source_id
        for candidate in candidates
        if candidate.get("decision") == "pending"
        and isinstance(candidate.get("source_ids"), list)
        for source_id in cast(list[object], candidate["source_ids"])
        if isinstance(source_id, str)
    )
    cutoff_text = cast(str, source_sweep["coverage_cutoff"])
    date.fromisoformat(cutoff_text)

    return {
        "coverage_cutoff": cutoff_text,
        "coverage_statement": PUBLIC_COVERAGE_STATEMENT,
        "source_families": {
            "total": len(family_rows),
            "by_status": {
                status: family_counts[status] for status in SOURCE_STATUSES
            },
        },
        "inventory": {
            decision: decision_counts[decision] for decision in INVENTORY_DECISIONS
        },
        "unresolved_candidates": decision_counts["pending"],
        "source_scopes": [
            {
                key: source.get(key)
                for key in (
                    "id",
                    "name",
                    "source_family",
                    "institution",
                    "covered_from",
                    "covered_through",
                    "covered_document_types",
                    "covered_sector_tags",
                    "scan_status",
                    "coverage_cutoff",
                )
            }
            | {"pending_candidate_count": pending_by_source[cast(str, source["id"])]}
            for source in cast(list[Mapping[str, object]], source_sweep["sources"])
        ],
    }


def _family_status(statuses: list[str]) -> str:
    if all(status == "reviewed" for status in statuses):
        return "reviewed"
    return next(status for status in SOURCE_STATUS_PRIORITY if status in statuses)
