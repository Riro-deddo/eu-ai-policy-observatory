"""The reviewed Opinion 15 preserved-original supplement, not an EU source class.

This offline check pins inspected source identities and recorded snapshot hashes.
It does not retrieve URLs or assert that remote bytes were checked at runtime.
"""

from typing import Mapping, Sequence

from observatory.io import LoadedRecord


_ORIGINAL_DOCUMENT = "chief-scientific-advisors-ai-science-opinion-2024-first-edition"
_RELEASE_SOURCE = "gcsa-ai-science-2024-release"
_RELEASE_URL = "https://research-and-innovation.ec.europa.eu/news/all-research-and-innovation-news/commission-receives-scientific-advice-artificial-intelligence-uptake-research-and-innovation-2024-04-15_en"
_REVIEWED_ARCHIVES = {
    "gcsa-ai-science-2024-original-allea-archive": (
        "https://allea.org/wp-content/uploads/2024/04/successful-and-timely-uptake-of-artificial-intelligence-KI0523478ENN.pdf",
        "fc260a451bed2cee18f438c8ec92badc6f7d48c8c3a563b1d97785fb7e235327",
    ),
    "gcsa-ai-science-2024-original-knaw-archive": (
        "https://storage.knaw.nl/2024-04/Successful-and-timely-uptake-of-artificial-intelligence.pdf",
        "21833b9e7be4a0cf5ffb23b9d0eb2f55c342271fb4c994f6c4c8d7facf9d7705",
    ),
}


def is_reviewed_document_supplement(
    document: Mapping[str, object],
    source: Mapping[str, object],
    sources: Mapping[str, Sequence[LoadedRecord]],
    field: str | None = None,
) -> bool:
    """Admit only the pinned original with its independent official release."""
    source_id = source.get("id")
    if (
        document.get("entity_type") != "document"
        or document.get("id") != _ORIGINAL_DOCUMENT
        or not isinstance(source_id, str)
        or source_id not in _REVIEWED_ARCHIVES
        or source.get("source_type") != "institutional_archive"
        or source.get("publication_status") != "published"
        or source.get("entity_type") != "source"
    ):
        return False
    url, digest = _REVIEWED_ARCHIVES[source_id]
    declared = document.get("source_ids")
    archive_matches = sources.get(source_id, ())
    release_matches = sources.get(_RELEASE_SOURCE, ())
    if (
        source.get("url") != url
        or not isinstance(declared, list)
        or source_id not in declared
        or _RELEASE_SOURCE not in declared
        or len(archive_matches) != 1
        or archive_matches[0].data != source
        or len(release_matches) != 1
    ):
        return False
    release = release_matches[0].data
    if (
        release.get("id") != _RELEASE_SOURCE
        or release.get("entity_type") != "source"
        or release.get("publication_status") != "published"
        or release.get("source_type") != "commission_webpage"
        or release.get("url") != _RELEASE_URL
    ):
        return False
    snapshots = document.get("snapshots")
    if not isinstance(snapshots, list) or not any(
        isinstance(snapshot, Mapping)
        and snapshot.get("source_id") == source_id
        and snapshot.get("format") == "pdf"
        and snapshot.get("content_hash") == digest
        for snapshot in snapshots
    ):
        return False
    if field is None:
        return True
    if field == "date_evidence.document_date.source_id":
        return document.get("document_date_kind") == "document_issue"
    if field == "legal_status_evidence.source_id":
        return True
    parts = field.split(".")
    if len(parts) != 3 or not parts[1].isdigit():
        return False
    collection, index, reference = parts[0], int(parts[1]), parts[2]
    expected_references = {
        "classification_evidence": "source_id",
        "bibliographic_authors": "evidence_source_id",
        "institution_roles": "evidence_source_id",
        "additional_dates": "source_id",
    }
    rows = document.get(collection)
    if (
        expected_references.get(collection) != reference
        or not isinstance(rows, list)
        or index >= len(rows)
        or not isinstance(rows[index], Mapping)
    ):
        return False
    row = rows[index]
    if collection == "institution_roles":
        return row.get("role") != "official_host"
    if collection == "additional_dates":
        return row.get("kind") in {"document_issue", "manuscript_completion", "cover_issue"}
    if collection == "classification_evidence":
        return not (row.get("field") == "provenance_tags" and row.get("value") == "officially_published")
    return True
