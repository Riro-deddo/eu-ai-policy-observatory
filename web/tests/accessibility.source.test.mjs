import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const layout = readFileSync(new URL('../src/layouts/BaseLayout.astro', import.meta.url), 'utf8');
const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');
const siteSpec = readFileSync(new URL('./site.spec.ts', import.meta.url), 'utf8');
const noJavaScriptSpec = readFileSync(new URL('./no-js.spec.ts', import.meta.url), 'utf8');

test('the skip link targets a focusable main landmark', () => {
  assert.match(layout, /<a class="skip-link" href="#main-content">Skip to main content<\/a>/);
  assert.match(layout, /<main id="main-content" tabindex="-1">/);
});

test('keyboard and coarse-pointer controls retain visible focus and usable targets', () => {
  assert.match(stylesheet, /:is\(a, button, input, select, \[tabindex\]\):focus-visible/);
  assert.match(stylesheet, /\.policy-map__graphic:focus-visible/);
  assert.match(
    stylesheet,
    /@media \(pointer: coarse\) \{[\s\S]*?\.corpus-explorer \[data-corpus-list\] a,[\s\S]*?\.timeline-year a,[\s\S]*?\.policy-map__relationships a,[\s\S]*?min-block-size: 44px;/,
  );
});

test('long metadata and source links can wrap within the page width', () => {
  assert.match(
    stylesheet,
    /\.policy-record dd,[\s\S]*?\.document-record li,[\s\S]*?\.policy-record li,[\s\S]*?\.policy-map__relationships li \{[\s\S]*?overflow-wrap: anywhere;/,
  );
});

test('cross-route checks collect non-vacuous policy links from the data-driven timeline', () => {
  assert.match(siteSpec, /page\.goto\('timeline\/'\)/);
  assert.match(siteSpec, /\[data-timeline-entry\] a\[href\*="\/policies\/"\]/);
  assert.match(siteSpec, /expect\(policyRoutes\.length\)\.toBeGreaterThan\(0\)/);
  assert.doesNotMatch(siteSpec, /\[data-policy-map-node\].*?includes\('\/policies\/'\)/s);
});

test('no-JavaScript checks require all fourteen timeline entries and a non-vacuous policy route set', () => {
  assert.match(noJavaScriptSpec, /page\.locator\('\[data-timeline-entry\]'\)\)\.toHaveCount\(14\)/);
  assert.match(noJavaScriptSpec, /page\.locator\('\[data-timeline-entry\]\[hidden\]'\)\)\.toHaveCount\(0\)/);
  assert.match(noJavaScriptSpec, /\[data-timeline-entry\] a\[href\*="\/policies\/"\]/);
  assert.match(noJavaScriptSpec, /expect\(policyRoutes\.length\)\.toBeGreaterThan\(0\)/);
});
