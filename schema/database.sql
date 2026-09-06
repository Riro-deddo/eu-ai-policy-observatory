PRAGMA foreign_keys = ON;

CREATE TABLE policies (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    summary TEXT NOT NULL,
    policy_family TEXT NOT NULL,
    policy_status TEXT NOT NULL,
    scope_note TEXT NOT NULL
);

CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    official_title TEXT NOT NULL,
    short_title TEXT NOT NULL,
    document_type TEXT NOT NULL,
    record_level TEXT NOT NULL,
    official_reference TEXT,
    oj_reference TEXT,
    document_date TEXT NOT NULL CHECK (
        length(document_date) = 10
        AND document_date GLOB '????-??-??'
        AND date(document_date, '+0 days') = document_date
    ),
    version_label TEXT,
    version_status TEXT NOT NULL,
    publication_date TEXT CHECK (
        length(publication_date) = 10
        AND publication_date GLOB '????-??-??'
        AND date(publication_date, '+0 days') = publication_date
    ),
    legal_status TEXT NOT NULL,
    celex TEXT,
    eli TEXT,
    language TEXT NOT NULL,
    official_summary TEXT,
    historical_review_status TEXT NOT NULL,
    temporal_collection TEXT,
    relevance_class TEXT,
    document_date_kind TEXT,
    date_evidence TEXT,
    legal_status_evidence TEXT,
    classification_evidence TEXT NOT NULL,
    bibliographic_authors TEXT NOT NULL,
    additional_dates TEXT NOT NULL,
    review_qualification TEXT CHECK (review_qualification IS NULL OR json_valid(review_qualification)),
    CHECK (review_qualification IS NULL OR historical_review_status = 'legacy_review_pending'),
    CHECK (publication_date IS NOT NULL OR (
        historical_review_status = 'legacy_review_pending'
        AND review_qualification IS NOT NULL
        AND COALESCE(json_extract(review_qualification, '$.kind'), '') = 'publication_date_pending'
    )),
    CHECK (COALESCE(json_extract(review_qualification, '$.kind'), '') != 'publication_date_pending' OR publication_date IS NULL)
);

CREATE UNIQUE INDEX documents_celex_unique
    ON documents (celex) WHERE celex IS NOT NULL;
CREATE UNIQUE INDEX documents_eli_unique
    ON documents (eli) WHERE eli IS NOT NULL;

CREATE TABLE concepts (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    name TEXT NOT NULL,
    definition TEXT NOT NULL,
    research_scope TEXT NOT NULL,
    eurovoc_uri TEXT,
    notes TEXT NOT NULL
);

CREATE TABLE institutions (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    official_name TEXT NOT NULL,
    short_name TEXT NOT NULL,
    institution_type TEXT NOT NULL,
    official_url TEXT NOT NULL
);

CREATE TABLE sources (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    source_type TEXT NOT NULL,
    url TEXT NOT NULL,
    publisher TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    last_verified_at TEXT NOT NULL,
    verification_note TEXT NOT NULL
);

CREATE TABLE events (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT NOT NULL CHECK (
        length(event_date) = 10
        AND event_date GLOB '????-??-??'
        AND date(event_date, '+0 days') = event_date
    ),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    policy_id TEXT NOT NULL REFERENCES policies(id),
    document_id TEXT REFERENCES documents(id),
    source_id TEXT NOT NULL REFERENCES sources(id)
);

CREATE TABLE relationships (
    id TEXT PRIMARY KEY,
    publication_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    source_entity_type TEXT NOT NULL,
    source_entity_id TEXT NOT NULL,
    target_entity_type TEXT NOT NULL,
    target_entity_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    basis TEXT NOT NULL,
    rationale TEXT,
    evidence_source_id TEXT REFERENCES sources(id),
    verification_status TEXT NOT NULL
);

CREATE TABLE corpus_assessments (
    document_id TEXT PRIMARY KEY REFERENCES documents(id),
    corpus_tier TEXT NOT NULL,
    policy_stage TEXT NOT NULL,
    inclusion_rationale TEXT NOT NULL,
    researcher_notes TEXT NOT NULL,
    review_status TEXT NOT NULL,
    reviewed_by TEXT NOT NULL,
    reviewed_at TEXT NOT NULL
);

CREATE TABLE document_retained_route_notices (
    document_id TEXT PRIMARY KEY REFERENCES documents(id),
    status TEXT NOT NULL,
    reason TEXT NOT NULL,
    reviewed_by TEXT NOT NULL,
    reviewed_at TEXT NOT NULL
);

CREATE TABLE document_retained_route_evidence (
    document_id TEXT NOT NULL REFERENCES documents(id),
    evidence_order INTEGER NOT NULL CHECK (evidence_order >= 0),
    source_id TEXT NOT NULL REFERENCES sources(id),
    locator TEXT NOT NULL,
    PRIMARY KEY (document_id, evidence_order),
    UNIQUE (document_id, source_id),
    FOREIGN KEY (document_id) REFERENCES document_retained_route_notices(document_id)
);

CREATE TABLE document_institutions (
    document_id TEXT NOT NULL REFERENCES documents(id),
    institution_id TEXT NOT NULL REFERENCES institutions(id),
    role TEXT NOT NULL,
    evidence_source_id TEXT REFERENCES sources(id),
    evidence_locator TEXT,
    PRIMARY KEY (document_id, institution_id, role)
);

CREATE TABLE document_procedure_references (
    document_id TEXT NOT NULL REFERENCES documents(id),
    procedure_reference TEXT NOT NULL,
    PRIMARY KEY (document_id, procedure_reference)
);

CREATE TABLE document_snapshots (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id),
    source_id TEXT NOT NULL REFERENCES sources(id),
    retrieved_at TEXT NOT NULL,
    format TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    archived_path TEXT
);

CREATE TABLE policy_documents (
    policy_id TEXT NOT NULL REFERENCES policies(id),
    document_id TEXT NOT NULL REFERENCES documents(id),
    PRIMARY KEY (policy_id, document_id)
);

CREATE TABLE document_concepts (
    document_id TEXT NOT NULL REFERENCES documents(id),
    concept_id TEXT NOT NULL REFERENCES concepts(id),
    PRIMARY KEY (document_id, concept_id)
);

CREATE TABLE document_sources (
    document_id TEXT NOT NULL REFERENCES documents(id),
    source_id TEXT NOT NULL REFERENCES sources(id),
    PRIMARY KEY (document_id, source_id)
);

CREATE TABLE document_sector_tags (
    document_id TEXT NOT NULL REFERENCES documents(id),
    sector_tag TEXT NOT NULL,
    PRIMARY KEY (document_id, sector_tag)
);

CREATE TABLE document_provenance_tags (
    document_id TEXT NOT NULL REFERENCES documents(id),
    provenance_tag TEXT NOT NULL,
    PRIMARY KEY (document_id, provenance_tag)
);

CREATE TABLE research_subsets (
    id TEXT PRIMARY KEY,
    version INTEGER NOT NULL,
    purpose TEXT NOT NULL
);

CREATE TABLE research_subset_documents (
    subset_id TEXT NOT NULL REFERENCES research_subsets(id),
    document_id TEXT NOT NULL REFERENCES documents(id),
    PRIMARY KEY (subset_id, document_id)
);
