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

export interface PublicData {
  generated_at: string;
  policies: Policy[];
  documents: DocumentRecord[];
  events: PolicyEvent[];
  concepts: Concept[];
  institutions: Institution[];
  relationships: Relationship[];
  sources: Source[];
}
