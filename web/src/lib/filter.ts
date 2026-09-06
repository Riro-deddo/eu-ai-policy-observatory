import type { DocumentRecord, PublicData, Relationship } from './types';

export interface CorpusCriteria {
  view?: 'principal' | 'all';
  query?: string;
  collection?: string;
  relevance?: string;
  year?: string;
  institution?: string;
  documentType?: string;
  legalStatus?: string;
  sector?: string;
  provenance?: string;
  policyStage?: string;
  concept?: string;
  corpusTier?: string;
  recordLevel?: string;
  versionStatus?: string;
  policy?: string;
}

const corpusStringCriteriaKeys = [
  'query',
  'collection',
  'relevance',
  'year',
  'institution',
  'documentType',
  'legalStatus',
  'sector',
  'provenance',
  'policyStage',
  'concept',
  'corpusTier',
  'recordLevel',
  'versionStatus',
  'policy',
] as const;
const corpusCriteriaKeys = ['view', ...corpusStringCriteriaKeys] as const;

type CorpusStringCriteriaKey = (typeof corpusStringCriteriaKeys)[number];

function isCorpusStringCriteriaKey(value: string): value is CorpusStringCriteriaKey {
  return corpusStringCriteriaKeys.includes(value as CorpusStringCriteriaKey);
}

export function parseCorpusCriteria(search: URLSearchParams): CorpusCriteria {
  const criteria: CorpusCriteria = {};

  for (const [key, value] of search) {
    if (value.trim() === '') continue;

    if (key === 'view' && criteria.view === undefined && (value === 'principal' || value === 'all')) {
      criteria.view = value;
    } else if (isCorpusStringCriteriaKey(key) && criteria[key] === undefined) {
      criteria[key] = value;
    }
  }

  return criteria;
}

export function buildCorpusSearchParams(
  current: URLSearchParams,
  criteria: CorpusCriteria,
): URLSearchParams {
  const next = new URLSearchParams(current);

  for (const key of corpusCriteriaKeys) next.delete(key);

  if (criteria.view === 'all') next.append('view', 'all');
  for (const key of corpusStringCriteriaKeys) {
    const value = criteria[key];
    if (value !== undefined && value.trim() !== '') next.append(key, value);
  }

  return next;
}

export interface TimelineCriteria {
  view?: 'principal' | 'all';
  institution?: string;
  documentType?: string;
  policyStage?: string;
  eventType?: string;
}

export interface TimelineEntry {
  id: string;
  kind: 'document' | 'event';
  date: string;
  title: string;
  href: string;
  institutionIds: string[];
  documentType: string | null;
  policyStage: string | null;
  eventType: string | null;
  recordLevel: DocumentRecord['record_level'] | null;
  dateKind: DocumentRecord['document_date_kind'] | null;
}

const provenanceLabels = new Map<string, string>([
  ['eu_institution_authored', 'Authored by an EU institution'],
  ['eu_agency_or_body_authored', 'Authored by an EU agency or body'],
  ['eu_expert_group_authored', 'Authored by an EU expert group'],
]);

const historicalLabels = new Map<string, string>([
  ['historical_lineage', 'Historical lineage'],
  ['contemporary_eu_ai_policy', 'Contemporary EU AI policy'],
  ['legacy_review_pending', 'Expanded evidence review pending'],
  ['direct_ai_substantive', 'Direct AI relevance'],
  ['ai_related_precursor', 'AI-related precursor'],
  ['indirect_adm_legal_context', 'Automated-decision legal context'],
]);

export function vocabularyLabel(value: string): string {
  const label = provenanceLabels.get(value) ?? historicalLabels.get(value);
  if (label !== undefined) return label;
  const readable = value.replaceAll('_', ' ').replace(/\beu\b/gi, 'EU');
  return `${readable.charAt(0).toLocaleUpperCase('en-GB')}${readable.slice(1)}`;
}

export const documentTypeLabel = vocabularyLabel;

export interface DocumentRelationshipLink {
  relationship: Relationship;
  relatedDocument: DocumentRecord;
  contextLabel: string;
}

export interface DocumentRelationshipGroups {
  parent: DocumentRelationshipLink[];
  attachments: DocumentRelationshipLink[];
  versions: DocumentRelationshipLink[];
  other: Relationship[];
}

export function groupDocumentRelationships(
  document: DocumentRecord,
  documents: DocumentRecord[],
  relationships: Relationship[],
): DocumentRelationshipGroups {
  const documentsById = new Map(documents.map((entry) => [entry.id, entry]));
  const relevantRelationships = relationships.filter((relationship) => (
    relationship.source_entity_type === 'document' && relationship.source_entity_id === document.id
    || relationship.target_entity_type === 'document' && relationship.target_entity_id === document.id
  ));
  const isCurrentSource = (relationship: Relationship) => (
    relationship.source_entity_type === 'document' && relationship.source_entity_id === document.id
  );
  const relatedDocument = (relationship: Relationship): DocumentRecord | undefined => {
    if (isCurrentSource(relationship) && relationship.target_entity_type === 'document') {
      return documentsById.get(relationship.target_entity_id);
    }
    if (relationship.target_entity_type === 'document' && relationship.target_entity_id === document.id
      && relationship.source_entity_type === 'document') {
      return documentsById.get(relationship.source_entity_id);
    }
    return undefined;
  };
  const sortLinks = (entries: DocumentRelationshipLink[]) => entries.sort((first, second) => (
    first.relatedDocument.document_date.localeCompare(second.relatedDocument.document_date, 'en-GB')
    || first.relatedDocument.short_title.localeCompare(second.relatedDocument.short_title, 'en-GB')
    || first.relationship.id.localeCompare(second.relationship.id, 'en-GB')
  ));
  const parentRelationshipTypes = new Set(['annex_to', 'part_of', 'procedural_step_for', 'version_of']);
  const parent = sortLinks(relevantRelationships.flatMap((relationship) => {
    const related = relatedDocument(relationship);
    return isCurrentSource(relationship) && related !== undefined
      && parentRelationshipTypes.has(relationship.relationship_type)
      ? [{ relationship, relatedDocument: related, contextLabel: 'Parent or principal record' }]
      : [];
  }));
  const attachments = sortLinks(relevantRelationships.flatMap((relationship) => {
    const related = relatedDocument(relationship);
    return !isCurrentSource(relationship) && related !== undefined && relationship.relationship_type === 'annex_to'
      ? [{ relationship, relatedDocument: related, contextLabel: 'Attachment' }]
      : [];
  }));
  const versionRelationshipTypes = new Set(['adopted_as', 'precedes', 'replaces', 'revises', 'supersedes']);
  const versionContextLabel = (relationship: Relationship): string => {
    const currentIsSource = isCurrentSource(relationship);
    if (relationship.relationship_type === 'version_of') return 'Related version';
    if (relationship.relationship_type === 'precedes') return currentIsSource ? 'Next version' : 'Previous version';
    if (relationship.relationship_type === 'adopted_as') return currentIsSource ? 'Adopted text' : 'Earlier proposal';
    if (['replaces', 'revises', 'supersedes'].includes(relationship.relationship_type)) {
      return currentIsSource ? 'Previous version' : 'Next version';
    }
    return 'Related version';
  };
  const versions = sortLinks(relevantRelationships.flatMap((relationship) => {
    const related = relatedDocument(relationship);
    const incomingVersion = !isCurrentSource(relationship) && relationship.relationship_type === 'version_of';
    return related !== undefined && (incomingVersion || versionRelationshipTypes.has(relationship.relationship_type))
      ? [{ relationship, relatedDocument: related, contextLabel: versionContextLabel(relationship) }]
      : [];
  }));
  const groupedRelationshipIds = new Set([...parent, ...attachments, ...versions]
    .map((entry) => entry.relationship.id));

  return {
    parent,
    attachments,
    versions,
    other: relevantRelationships.filter((relationship) => !groupedRelationshipIds.has(relationship.id)),
  };
}

function normalise(value: string): string {
  return value.trim().toLocaleLowerCase('en-GB');
}

function matchesValue(value: string, criterion: string | undefined): boolean {
  return criterion === undefined || normalise(value) === normalise(criterion);
}

function hasMatchingId(entries: Array<{ id: string }>, criterion: string | undefined): boolean {
  return criterion === undefined || entries.some((entry) => matchesValue(entry.id, criterion));
}

export function filterDocuments(
  documents: DocumentRecord[],
  criteria: CorpusCriteria,
): DocumentRecord[] {
  const query = criteria.query === undefined ? undefined : normalise(criteria.query);

  return documents
    .filter((document) => {
      const queryMatches = query === undefined || query === '' || [
        document.official_title,
        document.short_title,
        document.celex,
        document.eli,
        document.official_reference,
      ].some((value) => value !== null && normalise(value).includes(query));
      const assessment = document.corpus_assessment;
      const collectionMatches = criteria.collection === undefined
        || (criteria.collection === 'legacy_review_pending'
          ? document.historical_review_status === 'legacy_review_pending'
          : matchesValue(document.temporal_collection ?? '', criteria.collection));
      const relevanceMatches = criteria.relevance === undefined
        || (criteria.relevance === 'legacy_review_pending'
          ? document.historical_review_status === 'legacy_review_pending'
          : matchesValue(document.relevance_class ?? '', criteria.relevance));

      return (criteria.view === 'all' || document.record_level === 'principal')
        && queryMatches
        && collectionMatches
        && relevanceMatches
        && (criteria.year === undefined || (document.publication_date?.startsWith(criteria.year) ?? false))
        && hasMatchingId(document.institutions, criteria.institution)
        && matchesValue(document.document_type, criteria.documentType)
        && matchesValue(document.legal_status, criteria.legalStatus)
        && (criteria.sector === undefined
          || document.sector_tags.some((sector) => matchesValue(sector, criteria.sector)))
        && (criteria.provenance === undefined
          || document.provenance_tags.some((provenance) => matchesValue(provenance, criteria.provenance)))
        && matchesValue(document.record_level, criteria.recordLevel)
        && matchesValue(document.version_status, criteria.versionStatus)
        && hasMatchingId(document.policies, criteria.policy)
        && (criteria.policyStage === undefined
          || assessment?.policy_stage !== undefined
            && matchesValue(assessment.policy_stage, criteria.policyStage))
        && hasMatchingId(document.concepts, criteria.concept)
        && (criteria.corpusTier === undefined
          || assessment?.corpus_tier !== undefined
            && matchesValue(assessment.corpus_tier, criteria.corpusTier));
    })
    .sort((first, second) => (
      (second.publication_date ?? '').localeCompare(first.publication_date ?? '', 'en-GB')
      || first.short_title.localeCompare(second.short_title, 'en-GB')
      || first.id.localeCompare(second.id, 'en-GB')
    ));
}

function sortTimelineEntries(entries: TimelineEntry[]): TimelineEntry[] {
  return [...entries].sort((first, second) => (
    first.date.localeCompare(second.date, 'en-GB')
    || first.id.localeCompare(second.id, 'en-GB')
  ));
}

export function buildTimelineEntries(data: PublicData): TimelineEntry[] {
  const documentsById = new Map(data.documents.map((document) => [document.id, document]));
  const documents: TimelineEntry[] = data.documents
    .filter((document) => document.publication_status === 'published')
    .map((document) => ({
      id: document.id,
      kind: 'document',
      date: document.document_date,
      title: document.short_title,
      href: `corpus/${document.slug}/`,
      institutionIds: document.institutions.map((institution) => institution.id),
      documentType: document.document_type,
      policyStage: document.corpus_assessment?.policy_stage ?? null,
      eventType: null,
      recordLevel: document.record_level,
      dateKind: document.document_date_kind,
    }));
  const events: TimelineEntry[] = data.events
    .filter((event) => event.publication_status === 'published')
    .filter((event) => {
      const document = event.document_id === null ? undefined : documentsById.get(event.document_id);
      return document === undefined
        || event.event_type !== 'publication'
        || event.event_date !== document.document_date
        || event.event_date !== document.publication_date;
    })
    .map((event) => {
      const document = event.document_id === null ? undefined : documentsById.get(event.document_id);

      return {
        id: event.id,
        kind: 'event',
        date: event.event_date,
        title: event.title,
        href: document === undefined ? `policies/${event.policy_id}/` : `corpus/${document.slug}/`,
        institutionIds: document?.institutions.map((institution) => institution.id) ?? [],
        documentType: document?.document_type ?? null,
        policyStage: document?.corpus_assessment?.policy_stage ?? null,
        eventType: event.event_type,
        recordLevel: document?.record_level ?? null,
        dateKind: null,
      };
    });

  return sortTimelineEntries([...documents, ...events]);
}

export function filterTimeline(
  entries: TimelineEntry[],
  criteria: TimelineCriteria,
): TimelineEntry[] {
  return sortTimelineEntries(entries.filter((entry) => (
    (criteria.view === 'all' || entry.recordLevel === null || entry.recordLevel === 'principal')
    && (criteria.institution === undefined
      || entry.institutionIds.some((institutionId) => matchesValue(institutionId, criteria.institution)))
    && (criteria.documentType === undefined
      || entry.documentType !== null && matchesValue(entry.documentType, criteria.documentType))
    && (criteria.policyStage === undefined
      || entry.policyStage !== null && matchesValue(entry.policyStage, criteria.policyStage))
    && (criteria.eventType === undefined
      || entry.eventType !== null && matchesValue(entry.eventType, criteria.eventType))
  )));
}
