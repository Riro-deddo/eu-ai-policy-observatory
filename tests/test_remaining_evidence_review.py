import json
import hashlib
from collections import Counter
from pathlib import Path

import pytest

from observatory.pipeline import run_pipeline


ROOT = Path(__file__).resolve().parents[1]
ST10069_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-st10069-evidence-admission.json"
LEDGER_PATH = ROOT / "research/migrations/2026-09-05-remaining-evidence-review.json"
CONTINUATION_LEDGER_PATH = ROOT / "research/migrations/2026-09-05-review-continuation.json"
EVIDENCE_CORRECTIONS_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-evidence-corrections.json"
FOUR_ADMISSIONS_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-four-evidence-admissions.json"
SIX_RECORD_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-six-record-evidence-update.json"
SEVEN_ADMISSIONS_LEDGER_PATH = ROOT / "research/migrations/2026-09-06-seven-evidence-admissions.json"
COUNCIL_UPGRADES = (
    "ai-act-council-general-approach-st-14954-2022",
    "ai-act-council-general-approach-german-statement-14954-add-1",
)
PRESS_URL = (
    "https://www.consilium.europa.eu/en/press/press-releases/2022/12/06/"
    "artificial-intelligence-act-council-calls-for-promoting-safe-ai-that-respects-fundamental-rights/"
)

LATER_COUNCIL_DATES = (
    ("ai-act-pe-cons-24-2024", "2024-05-14", "2024-05-21", "document_issue"),
    ("ai-act-pe-cons-24-2024-rev-1", "2024-06-13", "2024-07-12", "official_act_date"),
    ("ai-act-provisional-agreement-st-5662-2024", "2024-01-26", "2024-02-02", "document_issue"),
    ("ai-omnibus-pe-cons-30-2026", "2026-06-18", "2026-06-29", "document_issue"),
    ("ai-omnibus-pe-cons-30-2026-rev-1", "2026-07-08", "2026-07-24", "official_act_date"),
)


@pytest.fixture(scope="module")
def public_payload(tmp_path_factory):
    output = tmp_path_factory.mktemp("remaining-review-output")
    result = run_pipeline(ROOT, "2026-09-05T20:00:00Z", output_root=output)
    return json.loads(result.public_json.read_text(encoding="utf-8"))


@pytest.mark.parametrize("document_id", COUNCIL_UPGRADES)
def test_dated_council_publication_upgrades_keep_issue_date_distinct(public_payload, document_id):
    """Catch a missing upgrade or the old issue-date-as-publication transcription."""
    documents = {row["id"]: row for row in public_payload["documents"]}
    record = documents[document_id]
    assert record["historical_review_status"] == "verified"
    assert record["document_date"] == "2022-11-25"
    assert record["publication_date"] == "2022-12-06"
    assert record["document_date_kind"] == "document_issue"
    publication_source_id = record["date_evidence"]["publication_date"]["source_id"]
    sources = {source["id"]: source for source in record["sources"]}
    assert sources[publication_source_id]["url"] == PRESS_URL


def test_initial_compromise_keeps_its_own_issue_date_without_false_upgrade(public_payload):
    """Catch copying the revised version's date into the initial version."""
    documents = {row["id"]: row for row in public_payload["documents"]}
    initial = documents["ai-act-council-third-compromise-part-one-st-12206-2022-init"]
    revised = documents["ai-act-council-third-compromise-part-one-st-12206-2022-rev-1"]
    assert initial["document_date"] == "2022-09-07"
    assert revised["document_date"] == "2022-09-16"
    assert initial["historical_review_status"] == "legacy_review_pending"


def test_first_compromise_keeps_multilingual_file_after_dated_access_admission(public_payload):
    """Catch reintroducing the broken English-only manifestation URL."""
    documents = {row["id"]: row for row in public_payload["documents"]}
    record = documents["ai-act-council-first-consolidated-compromise-st-10069-2022"]
    assert any(
        source["url"] == "https://data.consilium.europa.eu/doc/document/ST-10069-2022-INIT/x/pdf"
        for source in record["sources"]
    )
    assert record["historical_review_status"] == "verified"
    assert record["publication_date"] == "2022-06-20"
    assert "not first-ever" in record["date_evidence"]["publication_date"]["meaning"]


@pytest.mark.parametrize("document_id,issue_date,publication_date,date_kind", LATER_COUNCIL_DATES)
def test_exact_council_versions_keep_evidenced_date_semantics(
    public_payload, document_id, issue_date, publication_date, date_kind
):
    documents = {row["id"]: row for row in public_payload["documents"]}
    record = documents[document_id]
    assert record["historical_review_status"] == "verified"
    assert record["document_date"] == issue_date
    assert record["publication_date"] == publication_date
    assert record["document_date_kind"] == date_kind


def test_second_pass_accounts_for_every_hold_and_only_the_reviewed_upgrades(public_payload):
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    previous = json.loads((ROOT / "research/migrations/2026-09-05-expanded-evidence-review.json").read_text(encoding="utf-8"))
    starting = ledger["starting_pending_ids"]
    upgraded = ledger["upgraded_ids"]
    held = [row["document_id"] for row in ledger["held_records"]]
    audited = [row["document_id"] for row in ledger["record_audit"]]
    expected_upgrades = set(COUNCIL_UPGRADES) | {row[0] for row in LATER_COUNCIL_DATES}
    assert len(starting) == len(set(starting)) == 37
    assert set(starting) == {row["document_id"] for row in previous["held_records"]}
    assert len(upgraded) == len(set(upgraded)) == 7
    assert set(upgraded) == expected_upgrades
    assert len(held) == len(set(held)) == 30
    assert not set(upgraded) & set(held)
    assert set(starting) == set(upgraded) | set(held)
    assert len(audited) == len(set(audited)) == 37
    assert set(audited) == set(starting)
    assert all(row["reasons"] for row in ledger["held_records"])
    continuation = json.loads(CONTINUATION_LEDGER_PATH.read_text(encoding="utf-8"))
    corrections = json.loads(EVIDENCE_CORRECTIONS_LEDGER_PATH.read_text(encoding="utf-8"))
    four_admissions = json.loads(FOUR_ADMISSIONS_LEDGER_PATH.read_text(encoding="utf-8"))
    six_record_update = json.loads(SIX_RECORD_LEDGER_PATH.read_text(encoding="utf-8"))
    seven_admissions = json.loads(SEVEN_ADMISSIONS_LEDGER_PATH.read_text(encoding="utf-8"))
    st10069 = json.loads(ST10069_LEDGER_PATH.read_text(encoding="utf-8"))
    documents = {row["id"]: row for row in public_payload["documents"]}
    current = Counter(
        documents[row["id"]]["historical_review_status"]
        for row in ledger["baseline"]["documents"]
    )
    assert current == {
        "verified": continuation["expected_after"]["historical_review"]["verified"] + len(corrections["upgraded_ids"]) + len(four_admissions["upgraded_ids"]) + len(six_record_update["upgraded_existing_ids"]) + len(seven_admissions["upgraded_ids"]) + len(st10069["upgraded_ids"]),
        "legacy_review_pending": continuation["expected_after"]["historical_review"]["legacy_review_pending"] - len(corrections["upgraded_ids"]) - len(four_admissions["upgraded_ids"]) - len(six_record_update["upgraded_existing_ids"]) - len(seven_admissions["upgraded_ids"]) - len(st10069["upgraded_ids"]),
    }
    assert {row["id"]: row["slug"] for row in ledger["baseline"]["documents"]}.items() <= {
        row["id"]: row["slug"] for row in public_payload["documents"]
    }.items()


def test_previous_verified_documents_and_previous_audit_remain_unchanged():
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    previous_path = "research/migrations/2026-09-05-expanded-evidence-review.json"
    normalized = (ROOT / previous_path).read_text(encoding="utf-8").encode("utf-8")
    assert hashlib.sha256(normalized).hexdigest() == ledger["baseline"]["prior_ledger_sha256_lf"]
    previous_verified = [row for row in ledger["baseline"]["documents"] if row["historical_review_status"] == "verified"]
    assert len(previous_verified) == 94
    for row in previous_verified:
        raw = (ROOT / "data/documents" / f"{row['id']}.json").read_text(encoding="utf-8").encode("utf-8")
        assert hashlib.sha256(raw).hexdigest() == row["sha256_lf"]


def test_transparency_upgrade_preserves_the_historical_lineage_hold_decision(public_payload):
    documents = {row["id"]: row for row in public_payload["documents"]}
    record = documents["final-transparency-guidelines-2026"]
    assert record["historical_review_status"] == "verified"
    assert documents["draft-transparency-guidelines-2026"]["historical_review_status"] == "verified"
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    held = {row["document_id"]: row for row in ledger["held_records"]}
    assert held[record["id"]]["category"] == "contract_lineage_dependency"
    continuation = json.loads(CONTINUATION_LEDGER_PATH.read_text(encoding="utf-8"))
    assert record["id"] in continuation["upgraded_ids"]
