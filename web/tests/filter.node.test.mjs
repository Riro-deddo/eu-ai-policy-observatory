import assert from 'node:assert/strict';
import test from 'node:test';

import { buildCorpusSearchParams, filterDocuments } from '../src/lib/filter.ts';

const filterModule = await import('../src/lib/filter.ts');

const publishedAt = '2026-09-03T00:00:00Z';
const document = (id, shortTitle, publicationDate, details = {}) => ({
  id,
  slug: id,
  official_title: shortTitle,
  short_title: shortTitle,
  document_type: 'regulation',
  record_level: 'principal',
  sector_tags: [],
  provenance_tags: [],
  official_reference: null,
  procedure_references: [],
  oj_reference: null,
  document_date: publicationDate,
  version_label: 'Final',
  version_status: 'final',
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
    sector_tags: ['financial_services'],
    provenance_tags: ['eu_institution_authored'],
  }),
  document('same-date', 'A companion communication', '2024-07-12'),
  document('draft-version', 'First Presidency compromise', '2022-06-15', {
    record_level: 'version',
    official_reference: 'ST 10069/22',
    version_status: 'draft',
    policies: [{ id: 'ai-act-legislative-process' }],
  }),
  document('draft-attachment', 'Presidency compromise annex', '2022-06-15', {
    record_level: 'attachment',
    version_status: 'draft',
    policies: [{ id: 'ai-act-legislative-process' }],
  }),
  document('revised-version', 'Earlier Presidency compromise', '2022-05-15', {
    record_level: 'version',
    version_status: 'revised',
    policies: [{ id: 'ai-act-legislative-process' }],
  }),
  document('other-policy-version', 'Transparency code draft', '2022-04-15', {
    record_level: 'version',
    version_status: 'draft',
    policies: [{ id: 'ai-generated-content-transparency' }],
  }),
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

test('filters sector and provenance tags and serialises them in stable order', () => {
  assert.deepEqual(
    filterDocuments(documents, {
      sector: 'financial_services',
      provenance: 'eu_institution_authored',
    }).map((entry) => entry.id),
    ['final-ai-act'],
  );
  assert.equal(
    buildCorpusSearchParams(new URLSearchParams('ref=phd'), {
      sector: 'health',
      provenance: 'eu_agency_or_body_authored',
    }).toString(),
    'ref=phd&sector=health&provenance=eu_agency_or_body_authored',
  );
});

test('defaults to principal records and exposes every published record only in the all view', () => {
  assert.deepEqual(
    filterDocuments(documents, {}).map((entry) => entry.id),
    ['same-date', 'final-ai-act', 'communication'],
  );
  assert.deepEqual(
    filterDocuments(documents, { view: 'all' }).map((entry) => entry.id),
    [
      'same-date',
      'final-ai-act',
      'draft-version',
      'draft-attachment',
      'revised-version',
      'other-policy-version',
      'communication',
    ],
  );
});

test('combines record level, version status and policy filters with logical AND', () => {
  assert.deepEqual(
    filterDocuments(documents, {
      view: 'all',
      recordLevel: 'version',
      versionStatus: 'draft',
      policy: 'ai-act-legislative-process',
    }).map((entry) => entry.id),
    ['draft-version'],
  );
});

test('searches the general official reference case-insensitively', () => {
  assert.deepEqual(
    filterDocuments(documents, { view: 'all', query: 'st 10069/22' }).map((entry) => entry.id),
    ['draft-version'],
  );
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

test('parses only named Corpus criteria and discards blank or unsupported query parameters', () => {
  assert.equal(typeof filterModule.parseCorpusCriteria, 'function');
  assert.deepEqual(
    filterModule.parseCorpusCriteria(new URLSearchParams(
      'view=all&recordLevel=version&versionStatus=draft&policy=ai-act-legislative-process&year=&eventType=proposal&unknown=value&query=AI',
    )),
    {
      view: 'all',
      recordLevel: 'version',
      versionStatus: 'draft',
      policy: 'ai-act-legislative-process',
      query: 'AI',
    },
  );
});

test('builds a stable Corpus query while preserving unrelated parameters', () => {
  const current = new URLSearchParams(
    'campaign=research&view=principal&query=old&recordLevel=principal&unrelated=keep',
  );

  assert.equal(
    buildCorpusSearchParams(current, {
      view: 'all',
      query: 'AI Act',
      recordLevel: 'version',
      versionStatus: 'draft',
      policy: 'ai-act-legislative-process',
    }).toString(),
    'campaign=research&unrelated=keep&view=all&query=AI+Act&recordLevel=version&versionStatus=draft&policy=ai-act-legislative-process',
  );
  assert.equal(
    current.toString(),
    'campaign=research&view=principal&query=old&recordLevel=principal&unrelated=keep',
  );
});

test('omits the principal default and removes stale Corpus criteria from a shareable query', () => {
  assert.equal(
    buildCorpusSearchParams(
      new URLSearchParams('campaign=research&view=all&query=old&versionStatus=draft'),
      { view: 'principal' },
    ).toString(),
    'campaign=research',
  );
});
