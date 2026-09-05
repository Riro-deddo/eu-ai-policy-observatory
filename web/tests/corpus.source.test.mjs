import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');
const explorer = readFileSync(new URL('../src/components/CorpusExplorer.astro', import.meta.url), 'utf8');
const documentRoute = readFileSync(new URL('../src/pages/corpus/[slug].astro', import.meta.url), 'utf8');
const methodology = readFileSync(new URL('../src/pages/methodology.astro', import.meta.url), 'utf8');

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

test('Corpus exposes controlled sector and provenance filters with human-readable labels', () => {
  assert.match(explorer, /<label for="corpus-sector">Sector<\/label>[\s\S]*?<select id="corpus-sector" name="sector">/);
  assert.match(explorer, /<label for="corpus-provenance">Provenance<\/label>[\s\S]*?<select id="corpus-provenance" name="provenance">/);
  assert.match(explorer, /document\.sector_tags/);
  assert.match(explorer, /document\.provenance_tags/);
  assert.match(explorer, /vocabularyLabel\(sector\)/);
  assert.match(explorer, /vocabularyLabel\(provenance\)/);
});

test('Corpus result cards separate sector and production provenance labels', () => {
  assert.match(explorer, /<dt>Sectors<\/dt>[\s\S]*?document\.sector_tags\.map/);
  assert.match(explorer, /<dt>Provenance<\/dt>[\s\S]*?document\.provenance_tags\.map/);
});

test('document records separate researcher classifications, production provenance and official sources', () => {
  assert.match(documentRoute, /<h2 id="research-classifications">Research classifications<\/h2>/);
  assert.match(documentRoute, /These are researcher classifications/);
  assert.match(documentRoute, /<h2 id="production-provenance">Production provenance<\/h2>/);
  assert.match(documentRoute, /document\.provenance_tags/);
  assert.match(documentRoute, /document\.institutions/);
  assert.match(documentRoute, /<h2 id="official-sources-and-identifiers">Official sources and identifiers<\/h2>/);
});

test('Methodology publishes the aggregate coverage statement and audit counts', () => {
  assert.match(methodology, /<p>\{data\.coverage\.coverage_statement\}<\/p>/);
  assert.match(methodology, /<dt>Publication cutoff<\/dt><dd>\{data\.coverage\.coverage_cutoff\}<\/dd>/);
  assert.match(methodology, /<dt>Registered source families<\/dt><dd>\{data\.coverage\.source_families\.total\}<\/dd>/);
  assert.match(methodology, /<dt>Reviewed registered families<\/dt><dd>\{data\.coverage\.source_families\.by_status\.reviewed\}<\/dd>/);
  assert.match(methodology, /<dt>Not started<\/dt><dd>\{data\.coverage\.source_families\.by_status\.not_started\}<\/dd>/);
  assert.match(methodology, /<dt>In progress<\/dt><dd>\{data\.coverage\.source_families\.by_status\.in_progress\}<\/dd>/);
  assert.match(methodology, /<dt>Known gaps<\/dt><dd>\{data\.coverage\.source_families\.by_status\.gap_found\}<\/dd>/);
  assert.match(methodology, /<dt>Recheck due<\/dt><dd>\{data\.coverage\.source_families\.by_status\.recheck_due\}<\/dd>/);
  assert.match(methodology, /<dt>Included candidates<\/dt><dd>\{data\.coverage\.inventory\.included\}<\/dd>/);
  assert.match(methodology, /<dt>Merged candidates<\/dt><dd>\{data\.coverage\.inventory\.merged\}<\/dd>/);
  assert.match(methodology, /<dt>Excluded candidates<\/dt><dd>\{data\.coverage\.inventory\.excluded\}<\/dd>/);
  assert.match(methodology, /<dt>Unresolved candidates<\/dt><dd>\{data\.coverage\.unresolved_candidates\}<\/dd>/);
});

test('Corpus distinguishes the active result count from the published total', () => {
  assert.match(explorer, /data-corpus-count aria-live="polite"/);
  assert.match(explorer, /data-corpus-total/);
});

test('Corpus writes stable filter state to browser history without no-op entries', () => {
  assert.match(
    explorer,
    /buildCorpusSearchParams\(\s*new URLSearchParams\(window\.location\.search\),\s*criteria,?\s*\)/,
  );
  assert.match(explorer, /if \(nextUrl === currentUrl\) return;/);
  assert.match(explorer, /window\.history\.pushState\(window\.history\.state, '', nextUrl\)/);
  assert.match(explorer, /window\.history\.replaceState\(window\.history\.state, '', nextUrl\)/);
});

test('Corpus restores defaults and URL criteria on browser history navigation', () => {
  assert.match(explorer, /const hydrateControlsFromUrl = \(criteria: CorpusCriteria\)/);
  assert.match(explorer, /control\.selectedIndex = 0;/);
  assert.match(explorer, /window\.addEventListener\('popstate', readUrlAndApplyFilters\)/);
  assert.match(explorer, /const criteria = parseCorpusCriteria\(new URLSearchParams\(window\.location\.search\)\);[\s\S]*?hydrateControlsFromUrl\(criteria\);[\s\S]*?applyFilters\(readFormCriteria\(\)\);/);
});

test('Corpus updates history for live search, select changes, submit and reset', () => {
  assert.match(explorer, /form\.addEventListener\('input',[\s\S]*?syncHistory\(criteria, 'replace'\)/);
  assert.match(explorer, /form\.addEventListener\('change',[\s\S]*?syncHistory\(criteria, 'push'\)/);
  assert.match(explorer, /form\.addEventListener\('submit',[\s\S]*?syncHistory\(criteria, 'replace'\)/);
  assert.match(explorer, /form\.addEventListener\('reset',[\s\S]*?syncHistory\(criteria, 'push'\)/);
});
