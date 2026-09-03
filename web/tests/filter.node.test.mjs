import assert from 'node:assert/strict';
import test from 'node:test';

import { filterDocuments } from '../src/lib/filter.ts';

const publishedAt = '2026-09-03T00:00:00Z';
const document = (id, shortTitle, publicationDate, details = {}) => ({
  id,
  slug: id,
  official_title: shortTitle,
  short_title: shortTitle,
  document_type: 'regulation',
  publication_date: publicationDate,
  legal_status: 'in_force',
  language: 'en',
  celex: null,
  eli: null,
  official_summary: null,
  publication_status: 'published',
  created_at: publishedAt,
  updated_at: publishedAt,
  policies: [],
  concepts: [],
  institutions: [],
  sources: [],
  corpus_assessment: null,
  ...details,
});

const documents = [
  document('communication', 'Artificial Intelligence for Europe', '2018-04-25', {
    document_type: 'communication',
    legal_status: 'non_binding',
  }),
  document('final-ai-act', 'Artificial Intelligence Act', '2024-07-12', {
    celex: '32024R1689',
    eli: 'https://data.europa.eu/eli/reg/2024/1689/oj',
    concepts: [{ id: 'risk' }],
    institutions: [{ id: 'european-commission' }],
    corpus_assessment: { corpus_tier: 'core', policy_stage: 'adoption' },
  }),
  document('same-date', 'A companion communication', '2024-07-12'),
];

test('filters published documents by case-insensitive metadata with AND semantics', () => {
  assert.deepEqual(
    filterDocuments(documents, {
      query: '32024r1689',
      concept: 'risk',
      institution: 'european-commission',
    }).map((entry) => entry.id),
    ['final-ai-act'],
  );
  assert.deepEqual(
    filterDocuments(documents, { query: 'ELI/REG/2024' }).map((entry) => entry.id),
    ['final-ai-act'],
  );
});

test('returns a new deterministic sorted array without mutating input', () => {
  const input = [...documents].reverse();
  const before = input.map((entry) => entry.id);
  const result = filterDocuments(input, {});

  assert.deepEqual(input.map((entry) => entry.id), before);
  assert.notStrictEqual(result, input);
  assert.deepEqual(result.map((entry) => entry.id), ['same-date', 'final-ai-act', 'communication']);
});

test('filters scalar criteria and excludes records without a research assessment', () => {
  assert.deepEqual(
    filterDocuments(documents, { year: '2018' }).map((entry) => entry.id),
    ['communication'],
  );
  assert.deepEqual(
    filterDocuments(documents, { documentType: 'communication' }).map((entry) => entry.id),
    ['communication'],
  );
  assert.deepEqual(
    filterDocuments(documents, { legalStatus: 'in_force' }).map((entry) => entry.id),
    ['same-date', 'final-ai-act'],
  );
  assert.doesNotThrow(() => filterDocuments(documents, { policyStage: 'adoption' }));
  assert.deepEqual(
    filterDocuments(documents, { policyStage: 'adoption' }).map((entry) => entry.id),
    ['final-ai-act'],
  );
  assert.deepEqual(
    filterDocuments(documents, { corpusTier: 'core' }).map((entry) => entry.id),
    ['final-ai-act'],
  );
});
