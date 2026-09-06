import { describe, expect, it } from 'vitest';
import { filterDocuments } from '../src/lib/filter';
import { publishedDocuments } from './fixtures/documents';

describe('unknown publication dates', () => {
  const known = publishedDocuments[0]!;
  const unknown = { ...known, id: 'unknown-date', publication_date: null };
  it('keeps undated records in all years and sorts them after dated records', () => {
    expect(filterDocuments([unknown, known], { view: 'all' }).map(d => d.id)).toEqual([known.id, 'unknown-date']);
  });
  it('does not infer publication year from document year', () => {
    const result = filterDocuments([unknown, known], { view: 'all', year: known.document_date.slice(0, 4) });
    expect(result.map(d => d.id)).not.toContain('unknown-date');
  });
});
