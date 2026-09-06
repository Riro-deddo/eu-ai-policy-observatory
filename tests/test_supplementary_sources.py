"""The approved preserved original can supplement, never replace, EU evidence."""

from copy import deepcopy
from pathlib import Path

import pytest

from observatory.io import LoadedRecord
from observatory.historical_readiness import _check_evidence_source
from observatory.validate import _is_official_source, _validate_source_evidence


ORIGINAL = "chief-scientific-advisors-ai-science-opinion-2024-first-edition"
RELEASE = "gcsa-ai-science-2024-release"
RELEASE_URL = "https://research-and-innovation.ec.europa.eu/news/all-research-and-innovation-news/commission-receives-scientific-advice-artificial-intelligence-uptake-research-and-innovation-2024-04-15_en"
ARCHIVES = [
    ("gcsa-ai-science-2024-original-allea-archive", "https://allea.org/wp-content/uploads/2024/04/successful-and-timely-uptake-of-artificial-intelligence-KI0523478ENN.pdf", "fc260a451bed2cee18f438c8ec92badc6f7d48c8c3a563b1d97785fb7e235327"),
    ("gcsa-ai-science-2024-original-knaw-archive", "https://storage.knaw.nl/2024-04/Successful-and-timely-uptake-of-artificial-intelligence.pdf", "21833b9e7be4a0cf5ffb23b9d0eb2f55c342271fb4c994f6c4c8d7facf9d7705"),
]


def fixture(archive=ARCHIVES[0]):
    source_id, url, digest = archive
    document = {
        "id": ORIGINAL,
        "entity_type": "document",
        "publication_status": "published",
        "document_date_kind": "document_issue",
        "source_ids": [RELEASE, source_id],
        "snapshots": [{"id": "original-snapshot", "source_id": source_id,
                       "format": "pdf", "content_hash": digest,
                       "archived_path": None}],
        "institution_roles": [{"institution_id": "gcsa", "role": "author"}],
    }
    sources = {
        RELEASE: [LoadedRecord({"id": RELEASE, "entity_type": "source",
                                "publication_status": "published",
                                "source_type": "commission_webpage", "url": RELEASE_URL}, Path("release.json"))],
        source_id: [LoadedRecord({"id": source_id, "entity_type": "source",
                                  "publication_status": "published",
                                  "source_type": "institutional_archive", "url": url}, Path("archive.json"))],
    }
    return LoadedRecord(document, Path("original.json")), sources, source_id


def issues_for(record, sources, source_id, field="date_evidence.document_date.source_id"):
    issues = []
    _validate_source_evidence(record, "original.json", {"source": sources}, issues)
    _check_evidence_source(source_id, set(record.data["source_ids"]), sources, record, field, issues)
    return issues


@pytest.mark.parametrize("archive", ARCHIVES)
def test_reviewed_original_accepts_preserved_issue_date_with_official_release(archive):
    record, sources, source_id = fixture(archive)
    assert issues_for(record, sources, source_id) == []


@pytest.mark.parametrize("mutation", [
    "unrelated_document", "corrected_document", "fake_archive_url", "unknown_archive_id",
    "missing_release", "unpublished_release", "duplicate_release", "undeclared_release",
    "wrong_release_url", "wrong_release_type", "unpublished_archive", "duplicate_archive",
    "missing_snapshot", "wrong_snapshot_hash",
])
def test_archive_exception_rejects_changed_scope_or_missing_joint_evidence(mutation):
    record, sources, source_id = fixture()
    if mutation == "unrelated_document":
        record.data["id"] = "unrelated-opinion"
    elif mutation == "corrected_document":
        record.data["id"] = "chief-scientific-advisors-ai-science-opinion-2024"
    elif mutation == "fake_archive_url":
        sources[source_id][0].data["url"] = "https://allea.org/unreviewed.pdf"
    elif mutation == "unknown_archive_id":
        sources[source_id][0].data["id"] = "unreviewed-archive"
    elif mutation == "missing_release":
        del sources[RELEASE]
    elif mutation == "unpublished_release":
        sources[RELEASE][0].data["publication_status"] = "draft"
    elif mutation == "duplicate_release":
        sources[RELEASE].append(deepcopy(sources[RELEASE][0]))
    elif mutation == "undeclared_release":
        record.data["source_ids"].remove(RELEASE)
    elif mutation == "wrong_release_url":
        sources[RELEASE][0].data["url"] = "https://ec.europa.eu/unrelated-announcement"
    elif mutation == "wrong_release_type":
        sources[RELEASE][0].data["source_type"] = "official_pdf"
    elif mutation == "unpublished_archive":
        sources[source_id][0].data["publication_status"] = "draft"
    elif mutation == "duplicate_archive":
        sources[source_id].append(deepcopy(sources[source_id][0]))
    elif mutation == "missing_snapshot":
        record.data["snapshots"] = []
    elif mutation == "wrong_snapshot_hash":
        record.data["snapshots"][0]["content_hash"] = "0" * 64
    issues = issues_for(record, sources, source_id)
    assert any(issue.code == "official_evidence" for issue in issues)
    assert any(issue.code == "historical_evidence" for issue in issues)


def test_archive_cannot_evidence_publication_date():
    record, sources, source_id = fixture()
    issues = issues_for(record, sources, source_id, "date_evidence.publication_date.source_id")
    assert any(issue.code == "historical_evidence" for issue in issues)


def test_archive_cannot_evidence_primary_date_when_kind_is_publication():
    record, sources, source_id = fixture()
    record.data.update(document_date_kind="publication", document_date="2024-04-15",
                       publication_date="2024-04-15")
    issues = issues_for(record, sources, source_id)
    assert any(issue.code == "historical_evidence" for issue in issues)


def test_archive_cannot_evidence_official_host_role():
    record, sources, source_id = fixture()
    record.data["institution_roles"][0]["role"] = "official_host"
    issues = issues_for(record, sources, source_id, "institution_roles.0.evidence_source_id")
    assert any(issue.code == "historical_evidence" for issue in issues)


def test_archive_remains_nonofficial_and_cannot_support_an_event():
    record, sources, source_id = fixture()
    assert _is_official_source(sources[source_id][0].data) is False
    record.data.update(entity_type="event", source_id=source_id)
    issues = []
    _validate_source_evidence(record, "event.json", {"source": sources}, issues)
    assert any(issue.code == "official_evidence" for issue in issues)
