"""Guard evidence-backed exports against date, status and attribution regressions."""
import json
import os
import tempfile
from pathlib import Path

import pytest
from observatory.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
MDCG = "medical-device-ai-interplay-mdcg-2025-6"
EIOPA = "eiopa-ai-governance-consultation-2025"
HORIZON = "horizon-europe-specific-programme-decision-2021-764"


@pytest.fixture(scope="module")
def exported():
    with tempfile.TemporaryDirectory(prefix="euai-backfill-", dir=os.environ.get("TEMP")) as out:
        result = run_pipeline(ROOT, "2026-09-06T22:13:28Z", output_root=Path(out))
        return json.loads(result.public_json.read_text(encoding="utf-8"))


def test_backfill_is_exported_without_manufactured_dates(exported):
    rows = {d["id"]: d for d in exported["documents"]}
    assert {MDCG, EIOPA, HORIZON} <= rows.keys()
    assert (rows[MDCG]["document_date"], rows[MDCG]["document_date_kind"]) == ("2025-06-19", "publication")
    assert (rows[EIOPA]["document_date"], rows[EIOPA]["publication_date"]) == ("2025-02-10", "2025-02-11")
    assert rows[EIOPA]["version_status"] == "draft"
    assert (rows[HORIZON]["document_date"], rows[HORIZON]["publication_date"]) == ("2021-05-10", "2021-05-12")


def test_joint_guidance_does_not_become_commission_authored(exported):
    rows = {d["id"]: d for d in exported["documents"]}
    assert MDCG in rows
    roles = {(r["id"], r["role"]) for r in rows[MDCG]["institutions"]}
    assert ("european-commission", "author") not in roles
    assert ("medical-device-coordination-group", "author") in roles
    assert ("european-artificial-intelligence-board", "author") in roles
    assert rows[MDCG]["legal_status"] == "non_binding"


def test_horizon_repeal_survives_export_with_savings_evidence(exported):
    row = next(d for d in exported["documents"] if d["id"] == "horizon-2020-specific-programme-decision-2013-743-eu")
    assert row["legal_status"] == "repealed"
    assert row["legal_status_evidence"]["source_id"] == HORIZON + "-eur-lex"
    assert "16" in row["legal_status_evidence"]["locator"]


@pytest.mark.parametrize("identifier", [
    "council-decision-88-279-eec-esprit-ii", "council-decision-88-417-eec-delta",
    "council-decision-89-415-eec-doses", "council-decision-94-802-ec-esprit",
    "horizon-2020-specific-programme-decision-2013-743-eu", "sixth-framework-programme-decision-1513-2002-ec",
])
def test_assigned_oj_citations_are_available_to_citation_users(exported, identifier):
    row = next(d for d in exported["documents"] if d["id"] == identifier)
    assert row["oj_reference"] and row["oj_reference"].startswith("OJ L ")


def test_defence_records_preserve_publication_and_personal_authorship(exported):
    rows = {d["id"]: d for d in exported["documents"]}
    ep = rows["ep-autonomous-weapon-systems-resolution-2018"]
    assert (ep["document_date"], ep["publication_date"]) == ("2018-09-12", "2019-12-23")
    assert "2019/C 433/11" in ep["oj_reference"]
    eda = rows["eda-trustworthiness-ai-defence-white-paper-2025"]
    assert eda["official_reference"] is None  # TAID WG is a body, not a document ID.
    assert eda["document_date"] == eda["publication_date"] == "2025-05-12"
    assert eda["additional_dates"][0]["value"] == "2025-05-09"
    assert len(eda["bibliographic_authors"]) == 16
    assert eda["bibliographic_authors"][0]["name"] == "Isidoros Monogioudis"


def test_pending_discoveries_do_not_enter_public_documents(exported):
    rows = {d["id"] for d in exported["documents"]}
    assert exported["coverage"]["unresolved_candidates"] == 34
    assert "gpai-provider-guidelines-c-2025-7719" not in rows
    assert "jrc-ai-watch-defining-ai-2020" not in rows
    assert len(rows) == 192
