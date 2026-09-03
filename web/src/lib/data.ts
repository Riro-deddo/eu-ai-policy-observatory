import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import type { PublicData } from './types';

const collectionNames = [
  'policies',
  'documents',
  'events',
  'concepts',
  'institutions',
  'relationships',
  'sources',
] as const;

type CollectionName = (typeof collectionNames)[number];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPublicData(value: unknown): value is PublicData {
  return (
    isRecord(value) &&
    typeof value.generated_at === 'string' &&
    collectionNames.every((collectionName) => Array.isArray(value[collectionName]))
  );
}

function assertPublished(value: unknown, path: string): void {
  if (!isRecord(value) || value.publication_status !== 'published') {
    throw new Error(`Public data contains a non-published entity at ${path}.`);
  }
}

function assertPublishedEntities(value: unknown, path: string): void {
  if (!Array.isArray(value)) {
    throw new Error(`Public data collection is not an array at ${path}.`);
  }

  value.forEach((entity, index) => {
    assertPublished(entity, `${path}[${index}]`);

    if (isRecord(entity)) {
      for (const nestedName of ['policies', 'concepts', 'institutions', 'sources']) {
        const nested = entity[nestedName];
        if (nested !== undefined) {
          assertPublishedEntities(nested, `${path}[${index}].${nestedName}`);
        }
      }
    }
  });
}

export function loadPublicDataFromPath(publicDataPath: string): PublicData {
  const resolvedPublicDataPath = resolve(publicDataPath);

  if (!existsSync(resolvedPublicDataPath)) {
    throw new Error(`Public data file is missing: ${resolvedPublicDataPath}`);
  }

  const parsed: unknown = JSON.parse(readFileSync(resolvedPublicDataPath, 'utf8'));
  if (!isPublicData(parsed)) {
    throw new Error(`Public data must be an object: ${resolvedPublicDataPath}`);
  }

  for (const collectionName of collectionNames) {
    assertPublishedEntities(parsed[collectionName], collectionName);
  }

  return parsed;
}

export function loadPublicData(): PublicData {
  return loadPublicDataFromPath(
    resolve(process.cwd(), '..', 'generated', 'public-data.json'),
  );
}
