export interface PublishedEntity {
  id: string;
  publication_status: 'published';
  created_at: string;
  updated_at: string;
}

export interface Policy extends PublishedEntity {
  name: string;
  short_name: string;
  summary: string;
  policy_family: string;
  policy_status: string;
  scope_note: string;
}

export interface PolicyEvent extends PublishedEntity {
  event_type: string;
  event_date: string;
  title: string;
  description: string;
  policy_id: string;
  document_id: string | null;
  source_id: string;
}

export interface Concept extends PublishedEntity {
  name: string;
  definition: string;
  research_scope: string;
  eurovoc_uri: string | null;
  notes: string;
}

export interface Institution extends PublishedEntity {
  official_name: string;
  short_name: string;
  institution_type: string;
  official_url: string;
}

export interface Source extends PublishedEntity {
  source_type: string;
  url: string;
  publisher: string;
  retrieved_at: string;
  last_verified_at: string;
  verification_note: string;
}

export interface CorpusAssessment {
  document_id: string;
  corpus_tier: string;
  policy_stage: string;
  inclusion_rationale: string;
  researcher_notes: string;
  review_status: string;
  reviewed_by: string;
  reviewed_at: string;
}

export interface Relationship extends PublishedEntity {
  source_entity_type: string;
  source_entity_id: string;
  target_entity_type: string;
  target_entity_id: string;
  relationship_type: string;
  basis: 'official' | 'analytical';
  rationale: string | null;
  evidence_source_id: string | null;
  verification_status: string;
}

export interface DocumentSnapshot extends PublishedEntity {
  document_id: string;
  source_id: string;
  retrieved_at: string;
  format: string;
  content_hash: string;
  archived_path: string | null;
}

export interface DocumentRecord extends PublishedEntity {
  slug: string;
  official_title: string;
  short_title: string;
  document_type: string;
  record_level: 'principal' | 'supporting' | 'version' | 'attachment';
  sector_tags: string[];
  provenance_tags: string[];
  official_reference: string | null;
  procedure_references: string[];
  oj_reference: string | null;
  document_date: string;
  version_label: string | null;
  version_status: 'draft' | 'revised' | 'final' | 'consolidated' | 'not_applicable';
  publication_date: string;
  legal_status: string;
  language: string;
  celex: string | null;
  eli: string | null;
  official_summary: string | null;
  policies: Policy[];
  concepts: Concept[];
  institutions: Array<Institution & { role: string }>;
  sources: Source[];
  corpus_assessment: CorpusAssessment | null;
}

export interface CorpusCoverage {
  from_year: number | null;
  to_year: number | null;
  last_verified_date: string | null;
  published_documents: number;
  principal_documents: number;
  supporting_files_and_versions: number;
  coverage_cutoff: string;
  coverage_statement: string;
  source_families: {
    total: number;
    by_status: Record<'not_started' | 'in_progress' | 'reviewed' | 'gap_found' | 'recheck_due', number>;
  };
  inventory: Record<'included' | 'merged' | 'excluded' | 'pending', number>;
  unresolved_candidates: number;
}

export interface PublicData {
  coverage: CorpusCoverage;
  generated_at: string;
  policies: Policy[];
  documents: DocumentRecord[];
  events: PolicyEvent[];
  concepts: Concept[];
  institutions: Institution[];
  relationships: Relationship[];
  sources: Source[];
}
