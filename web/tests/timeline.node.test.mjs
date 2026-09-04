import assert from 'node:assert/strict';
import test from 'node:test';

import {
  buildTimelineEntries,
  documentTypeLabel,
  filterTimeline,
  groupDocumentRelationships,
} from '../src/lib/filter.ts';

const publishedAt = '2026-09-03T00:00:00Z';
const published = { publication_status: 'published', created_at: publishedAt, updated_at: publishedAt };

const document = (id, date, details = {}) => ({
  ...published,
  id,
  slug: id,
  official_title: id,
  short_title: id,
  document_type: 'communication',
  record_level: 'principal',
  official_reference: null,
  procedure_references: [],
  oj_reference: null,
  document_date: date,
  version_label: null,
  version_status: 'not_applicable',
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
      document_date: '2024-06-13',
      document_type: 'regulation',
      institutions: [{ id: 'european-commission' }],
      corpus_assessment: { policy_stage: 'adoption' },
    }),
  ],
  events: [
    event('event-duplicate-publication', '2018-04-25', 'document-2018'),
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
  assert.equal(entries.find((entry) => entry.id === 'document-2024').date, '2024-06-13');
  assert.equal(entries.find((entry) => entry.id === 'event-2024').date, '2024-07-12');
  assert.equal(entries.find((entry) => entry.id === 'document-2024').href, 'corpus/document-2024/');
  assert.equal(entries.find((entry) => entry.id === 'event-unlinked').href, 'policies/eu-ai-policy-pathway/');
});

const relationship = (id, sourceId, relationshipType, targetId, basis = 'official') => ({
  ...published,
  id,
  source_entity_type: 'document',
  source_entity_id: sourceId,
  target_entity_type: 'document',
  target_entity_id: targetId,
  relationship_type: relationshipType,
  basis,
  rationale: null,
  evidence_source_id: 'evidence-source',
  verification_status: 'verified',
});

test('timeline document-type labels are readable across the expanded vocabulary', () => {
  assert.equal(documentTypeLabel('staff_working_document'), 'Staff working document');
  assert.equal(documentTypeLabel('institutional_position'), 'Institutional position');
  assert.equal(documentTypeLabel('implementing_regulation'), 'Implementing regulation');
  assert.equal(documentTypeLabel('code_of_practice'), 'Code of practice');
  assert.equal(documentTypeLabel('standardisation_request'), 'Standardisation request');
});

test('document relationships are grouped by direction without duplicating canonical document data', () => {
  const current = document('current', '2024-01-02');
  const previous = document('previous', '2024-01-01');
  const next = document('next', '2024-01-03');
  const parent = document('parent', '2021-04-21');
  const attachment = document('attachment', '2024-01-02');
  const relatedVersion = document('related-version', '2024-02-01');
  const entries = [
    relationship('parent-link', 'current', 'version_of', 'parent'),
    relationship('attachment-link', 'attachment', 'annex_to', 'current'),
    relationship('previous-link', 'current', 'revises', 'previous'),
    relationship('next-link', 'next', 'revises', 'current'),
    relationship('related-version-link', 'related-version', 'version_of', 'current'),
    relationship('other-link', 'current', 'implements', 'attachment', 'analytical'),
  ];

  const groups = groupDocumentRelationships(
    current,
    [current, previous, next, parent, attachment, relatedVersion],
    entries,
  );

  assert.deepEqual(groups.parent.map((entry) => entry.relationship.id), ['parent-link']);
  assert.deepEqual(groups.attachments.map((entry) => entry.relationship.id), ['attachment-link']);
  assert.deepEqual(
    groups.versions.map((entry) => [entry.relationship.id, entry.contextLabel]),
    [
      ['previous-link', 'Previous version'],
      ['next-link', 'Next version'],
      ['related-version-link', 'Related version'],
    ],
  );
  assert.deepEqual(groups.other.map((entry) => entry.id), ['other-link']);
  assert.equal(groups.parent[0].relatedDocument, parent);
  assert.equal(parent.parent_id, undefined);
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
