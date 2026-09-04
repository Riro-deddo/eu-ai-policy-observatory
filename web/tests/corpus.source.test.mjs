import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');
const explorer = readFileSync(new URL('../src/components/CorpusExplorer.astro', import.meta.url), 'utf8');

test('Corpus filters have responsive layout and 44px coarse-pointer controls', () => {
  assert.match(stylesheet, /\.corpus-filters \{[\s\S]*?display: grid;/);
  assert.match(stylesheet, /@media \(max-width: 760px\) \{[\s\S]*?\.corpus-filters \{[\s\S]*?grid-template-columns: 1fr;/);
  assert.match(
    stylesheet,
    /@media \(pointer: coarse\) \{[\s\S]*?\.corpus-filters input, \.corpus-filters select, \.corpus-filters button \{[\s\S]*?min-block-size: 44px;/,
  );
});

test('Corpus serialisation protects a closing-script sequence', () => {
  const safelySerialised = JSON.stringify({ title: '</script>' }).replaceAll('<', '\\u003c');

  assert.doesNotMatch(safelySerialised, /<\/script>/i);
  assert.match(
    explorer,
    /JSON\.stringify\(documents\)\.replaceAll\('<', '\\\\u003c'\)/,
  );
});

test('Corpus explains that JavaScript enables interactive filtering', () => {
  assert.match(explorer, /<noscript>[\s\S]*?Interactive filtering requires JavaScript[\s\S]*?<\/noscript>/);
});

test('Corpus filtering hides any enhanced list item missing its document ID', () => {
  assert.match(
    explorer,
    /const documentId = item\.dataset\.documentId;\s*item\.hidden = documentId === undefined \|\| !visibleIds\.has\(documentId\);/,
  );
});

test('Corpus renders the complete record list before JavaScript applies the principal default', () => {
  assert.match(explorer, /filterDocuments\(documents, \{ view: 'all' \}\)/);
  assert.match(explorer, /<noscript>[\s\S]*?complete published corpus is shown below[\s\S]*?<\/noscript>/);
});

test('Corpus exposes labelled view and version-aware filter controls', () => {
  assert.match(explorer, /<option value="principal">Principal documents<\/option>/);
  assert.match(explorer, /<option value="all">All files and versions<\/option>/);
  assert.match(explorer, /<label for="corpus-record-level">Record level<\/label>/);
  assert.match(explorer, /<label for="corpus-version-status">Version status<\/label>/);
  assert.match(explorer, /<label for="corpus-policy">Policy process<\/label>/);
});

test('Corpus distinguishes the active result count from the published total', () => {
  assert.match(explorer, /data-corpus-count aria-live="polite"/);
  assert.match(explorer, /data-corpus-total/);
});
