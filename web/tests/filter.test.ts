import { describe, expect, it } from 'vitest';

import { filterDocuments } from '../src/lib/filter';
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
    const sameDate = {
      ...publishedDocuments[1],
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
