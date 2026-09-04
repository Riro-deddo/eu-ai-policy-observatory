import type { DocumentRecord, PublicData } from './types';

export interface CorpusCriteria {
  view?: 'principal' | 'all';
  query?: string;
  year?: string;
  institution?: string;
  documentType?: string;
  legalStatus?: string;
  policyStage?: string;
  concept?: string;
  corpusTier?: string;
  recordLevel?: string;
  versionStatus?: string;
  policy?: string;
}

const corpusStringCriteriaKeys = [
  'query',
  'year',
  'institution',
  'documentType',
  'legalStatus',
  'policyStage',
  'concept',
  'corpusTier',
  'recordLevel',
  'versionStatus',
  'policy',
] as const;

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

export interface TimelineCriteria {
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

      return (criteria.view === 'all' || document.record_level === 'principal')
        && queryMatches
        && (criteria.year === undefined || document.publication_date.startsWith(criteria.year))
        && hasMatchingId(document.institutions, criteria.institution)
        && matchesValue(document.document_type, criteria.documentType)
        && matchesValue(document.legal_status, criteria.legalStatus)
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
      second.publication_date.localeCompare(first.publication_date, 'en-GB')
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
      date: document.publication_date,
      title: document.short_title,
      href: `corpus/${document.slug}/`,
      institutionIds: document.institutions.map((institution) => institution.id),
      documentType: document.document_type,
      policyStage: document.corpus_assessment?.policy_stage ?? null,
      eventType: null,
    }));
  const events: TimelineEntry[] = data.events
    .filter((event) => event.publication_status === 'published')
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
      };
    });

  return sortTimelineEntries([...documents, ...events]);
}

export function filterTimeline(
  entries: TimelineEntry[],
  criteria: TimelineCriteria,
): TimelineEntry[] {
  return sortTimelineEntries(entries.filter((entry) => (
    (criteria.institution === undefined
      || entry.institutionIds.some((institutionId) => matchesValue(institutionId, criteria.institution)))
    && (criteria.documentType === undefined
      || entry.documentType !== null && matchesValue(entry.documentType, criteria.documentType))
    && (criteria.policyStage === undefined
      || entry.policyStage !== null && matchesValue(entry.policyStage, criteria.policyStage))
    && (criteria.eventType === undefined
      || entry.eventType !== null && matchesValue(entry.eventType, criteria.eventType))
  )));
}
