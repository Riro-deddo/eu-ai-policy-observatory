import { describe, expect, it } from 'vitest';

import { buildTimelineEntries, filterDocuments, filterTimeline } from '../src/lib/filter';
import type { DocumentRecord, PolicyEvent, PublicData } from '../src/lib/types';
import { publishedDocuments } from './fixtures/documents';

describe('filterDocuments', () => {
  it('matches titles, CELEX and ELI case-insensitively', () => {
    expect(filterDocuments(publishedDocuments, { query: '32024r1689' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { query: 'ELI/REG/2024' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
  });

  it('combines concept and institution filters with logical AND', () => {
    expect(filterDocuments(publishedDocuments, {
      concept: 'risk',
      institution: 'european-commission',
    }).map((document) => document.id)).toEqual(['artificial-intelligence-act-2024']);
  });

  it('sorts by publication date descending and short title ascending', () => {
    const communication = publishedDocuments[1];
    if (communication === undefined) throw new Error('Expected a communication fixture.');
    const sameDate: DocumentRecord = {
      ...communication,
      id: 'same-date',
      short_title: 'A companion communication',
      publication_date: '2024-07-12',
    };

    expect(filterDocuments([...publishedDocuments, sameDate], {}).map((document) => document.id)).toEqual([
      'same-date',
      'artificial-intelligence-act-2024',
      'artificial-intelligence-for-europe-2018',
    ]);
  });

  it('does not mutate its input array', () => {
    const documents = [...publishedDocuments].reverse();
    const before = documents.map((document) => document.id);

    const result = filterDocuments(documents, {});

    expect(documents.map((document) => document.id)).toEqual(before);
    expect(result).not.toBe(documents);
  });

  it('applies scalar filters without matching documents lacking an assessment', () => {
    expect(filterDocuments(publishedDocuments, { year: '2024' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { documentType: 'regulation' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { legalStatus: 'in_force' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { policyStage: 'adoption' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { corpusTier: 'core' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
  });
});

const publishedAt = '2026-09-03T00:00:00Z';

const timelineEvents: PolicyEvent[] = [
  {
    id: 'event-tie',
    publication_status: 'published',
    created_at: publishedAt,
    updated_at: publishedAt,
    event_type: 'proposal',
    event_date: '2018-04-25',
    title: 'A recorded proposal event',
    description: 'An event linked to the 2018 document.',
    policy_id: 'policy-pathway',
    document_id: 'artificial-intelligence-for-europe-2018',
    source_id: 'source-2018',
  },
  {
    id: 'final-act-publication',
    publication_status: 'published',
    created_at: publishedAt,
    updated_at: publishedAt,
    event_type: 'publication',
    event_date: '2024-07-12',
    title: 'Publication of the final Act',
    description: 'An event linked to the final Act.',
    policy_id: 'policy-pathway',
    document_id: 'artificial-intelligence-act-2024',
    source_id: 'source-2024',
  },
  {
    id: 'unlinked-publication',
    publication_status: 'published',
    created_at: publishedAt,
    updated_at: publishedAt,
    event_type: 'publication',
    event_date: '2023-01-01',
    title: 'An unlinked publication event',
    description: 'An event with no document record.',
    policy_id: 'policy-pathway',
    document_id: null,
    source_id: 'source-unlinked',
  },
];

const timelineData: PublicData = {
  generated_at: publishedAt,
  policies: [],
  documents: publishedDocuments,
  events: timelineEvents,
  concepts: [],
  institutions: [],
  relationships: [],
  sources: [],
};

describe('timeline filtering', () => {
  it('builds every published document and event in ascending ISO-date then ID order', () => {
    expect(buildTimelineEntries(timelineData).map((entry) => entry.id)).toEqual([
      'artificial-intelligence-for-europe-2018',
      'event-tie',
      'unlinked-publication',
      'artificial-intelligence-act-2024',
      'final-act-publication',
    ]);
  });

  it('inherits linked document metadata and keeps unlinked events empty', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(entries.find((entry) => entry.id === 'final-act-publication')).toMatchObject({
      kind: 'event',
      href: 'corpus/artificial-intelligence-act/',
      institutionIds: ['european-commission'],
      documentType: 'regulation',
      policyStage: 'adoption',
      eventType: 'publication',
    });
    expect(entries.find((entry) => entry.id === 'unlinked-publication')).toMatchObject({
      kind: 'event',
      href: 'policies/policy-pathway/',
      institutionIds: [],
      documentType: null,
      policyStage: null,
      eventType: 'publication',
    });
  });

  it('applies timeline criteria with logical AND and normalised values', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(filterTimeline(entries, {
      institution: ' EUROPEAN-COMMISSION ',
      documentType: 'REGULATION',
      policyStage: 'adoption',
      eventType: 'PUBLICATION',
    }).map((entry) => entry.id)).toEqual(['final-act-publication']);
  });

  it('does not treat nullable assessments or unlinked events as matching a policy stage', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(filterTimeline(entries, { policyStage: 'adoption' }).map((entry) => entry.id)).toEqual([
      'artificial-intelligence-act-2024',
      'final-act-publication',
    ]);
  });

  it('returns new arrays without mutating source documents, events or entries', () => {
    const documents = [...timelineData.documents].reverse();
    const events = [...timelineData.events].reverse();
    const beforeDocuments = documents.map((document) => document.id);
    const beforeEvents = events.map((event) => event.id);
    const entries = buildTimelineEntries({ ...timelineData, documents, events });
    const beforeEntries = entries.map((entry) => entry.id);

    const filtered = filterTimeline(entries, { eventType: 'publication' });

    expect(documents.map((document) => document.id)).toEqual(beforeDocuments);
    expect(events.map((event) => event.id)).toEqual(beforeEvents);
    expect(entries.map((entry) => entry.id)).toEqual(beforeEntries);
    expect(entries).not.toBe(documents);
    expect(filtered).not.toBe(entries);
  });
});
