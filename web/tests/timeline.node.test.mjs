import assert from 'node:assert/strict';
import test from 'node:test';

import { buildTimelineEntries, filterTimeline } from '../src/lib/filter.ts';

const publishedAt = '2026-09-03T00:00:00Z';
const published = { publication_status: 'published', created_at: publishedAt, updated_at: publishedAt };

const document = (id, date, details = {}) => ({
  ...published,
  id,
  slug: id,
  official_title: id,
  short_title: id,
  document_type: 'communication',
  publication_date: date,
  legal_status: 'non_binding',
  language: 'en',
  celex: null,
  eli: null,
  official_summary: null,
  policies: [],
  concepts: [],
  institutions: [],
  sources: [],
  corpus_assessment: null,
  ...details,
});

const event = (id, date, documentId, eventType = 'publication') => ({
  ...published,
  id,
  event_type: eventType,
  event_date: date,
  title: id,
  description: id,
  policy_id: 'eu-ai-policy-pathway',
  document_id: documentId,
  source_id: 'evidence-source',
});

const data = {
  generated_at: publishedAt,
  policies: [],
  documents: [
    document('document-2018', '2018-04-25'),
    document('document-2024', '2024-07-12', {
      document_type: 'regulation',
      institutions: [{ id: 'european-commission' }],
      corpus_assessment: { policy_stage: 'adoption' },
    }),
  ],
  events: [
    event('event-same-date', '2018-04-25', 'document-2018', 'proposal'),
    event('event-unlinked', '2023-01-01', null),
    event('event-2024', '2024-07-12', 'document-2024'),
  ],
  concepts: [],
  institutions: [],
  relationships: [],
  sources: [],
};

test('timeline entries use base-agnostic paths and deterministic ascending chronology', () => {
  const entries = buildTimelineEntries(data);

  assert.deepEqual(entries.map((entry) => entry.id), [
    'document-2018',
    'event-same-date',
    'event-unlinked',
    'document-2024',
    'event-2024',
  ]);
  assert.equal(entries.find((entry) => entry.id === 'document-2024').href, 'corpus/document-2024/');
  assert.equal(entries.find((entry) => entry.id === 'event-unlinked').href, 'policies/eu-ai-policy-pathway/');
});

test('timeline filtering inherits document metadata, uses AND semantics and preserves inputs', () => {
  const entries = buildTimelineEntries(data);
  const before = entries.map((entry) => entry.id);

  assert.deepEqual(
    filterTimeline(entries, {
      institution: 'EUROPEAN-COMMISSION',
      documentType: 'regulation',
      policyStage: 'adoption',
      eventType: 'publication',
    }).map((entry) => entry.id),
    ['event-2024'],
  );
  assert.deepEqual(filterTimeline(entries, { policyStage: 'adoption' }).map((entry) => entry.id), [
    'document-2024',
    'event-2024',
  ]);
  assert.deepEqual(entries.map((entry) => entry.id), before);
});
