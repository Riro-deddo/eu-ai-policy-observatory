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
    publication_date TEXT NOT NULL CHECK (
        length(publication_date) = 10
        AND publication_date GLOB '????-??-??'
        AND date(publication_date, '+0 days') = publication_date
    ),
    legal_status TEXT NOT NULL,
    celex TEXT,
    eli TEXT,
    language TEXT NOT NULL,
    official_summary TEXT
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

CREATE TABLE document_institutions (
    document_id TEXT NOT NULL REFERENCES documents(id),
    institution_id TEXT NOT NULL REFERENCES institutions(id),
    role TEXT NOT NULL,
    PRIMARY KEY (document_id, institution_id, role)
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
