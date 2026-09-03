import { afterEach, expect, test } from 'vitest';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

import { loadPublicDataFromPath } from '../src/lib/data';

const temporaryDirectories: string[] = [];

afterEach(() => {
  for (const directory of temporaryDirectories.splice(0)) {
    rmSync(directory, { force: true, recursive: true });
  }
});

function writeFixture(payload: unknown): string {
  const directory = mkdtempSync(join(tmpdir(), 'atlas-public-data-'));
  temporaryDirectories.push(directory);
  const dataPath = join(directory, 'public-data.json');
  writeFileSync(dataPath, JSON.stringify(payload), 'utf8');
  return dataPath;
}

test('reports the resolved path when the public export is missing', () => {
  const missingPath = join(tmpdir(), 'atlas-public-data-missing.json');

  expect(() => loadPublicDataFromPath(missingPath)).toThrow(resolve(missingPath));
});

test('rejects a non-published top-level entity', () => {
  const dataPath = writeFixture({
    generated_at: '2026-09-03T00:00:00Z',
    policies: [{ id: 'draft-policy', publication_status: 'draft' }],
    documents: [],
    events: [],
    concepts: [],
    institutions: [],
    relationships: [],
    sources: [],
  });

  expect(() => loadPublicDataFromPath(dataPath)).toThrow('policies[0]');
});

test('rejects a non-published embedded document dependency', () => {
  const dataPath = writeFixture({
    generated_at: '2026-09-03T00:00:00Z',
    policies: [],
    documents: [
      {
        id: 'published-document',
        publication_status: 'published',
        policies: [{ id: 'draft-policy', publication_status: 'draft' }],
        concepts: [],
        institutions: [],
        sources: [],
      },
    ],
    events: [],
    concepts: [],
    institutions: [],
    relationships: [],
    sources: [],
  });

  expect(() => loadPublicDataFromPath(dataPath)).toThrow('documents[0].policies[0]');
});
