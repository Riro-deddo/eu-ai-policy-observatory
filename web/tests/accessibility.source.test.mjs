import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const layout = readFileSync(new URL('../src/layouts/BaseLayout.astro', import.meta.url), 'utf8');
const pathway = readFileSync(new URL('../src/components/PolicyPathway.astro', import.meta.url), 'utf8');
const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');
const siteSpec = readFileSync(new URL('./site.spec.ts', import.meta.url), 'utf8');
const noJavaScriptSpec = readFileSync(new URL('./no-js.spec.ts', import.meta.url), 'utf8');

function testBlock(source, name) {
  const start = source.indexOf(`test('${name}'`);
  assert.notEqual(start, -1, `Could not find test block: ${name}`);
  const next = source.indexOf("\ntest(", start + 1);
  return source.slice(start, next === -1 ? undefined : next);
}

function assertPolicyRouteCoverage(block, routeConsumption) {
  assert.match(block, /page\.goto\('timeline\/'\)/);
  assert.match(block, /\[data-timeline-entry\] a\[href\*="\/policies\/"\]/);
  assert.match(block, /expect\(policyRoutes\.length\)\.toBeGreaterThan\(0\)/);
  assert.match(block, routeConsumption);
}

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

test('cross-route and mobile checks independently collect and navigate policy routes from the Timeline', () => {
  const crossRouteBlock = testBlock(
    siteSpec,
    'every generated route has one main heading, one main landmark, a working skip link and no console errors',
  );
  const mobileBlock = testBlock(siteSpec, 'mobile routes do not make the document body horizontally overflow');

  assertPolicyRouteCoverage(crossRouteBlock, /for \(const route of policyRoutes\) await assertRouteAccessibility\(route\)/);
  assertPolicyRouteCoverage(mobileBlock, /const routes = \[[\s\S]*?\.\.\.policyRoutes,[\s\S]*?for \(const route of routes\) \{/);
});

test('the no-JavaScript block derives its timeline count from serialized public data and consumes Timeline policy routes', () => {
  const noJavaScriptBlock = testBlock(noJavaScriptSpec, 'core atlas content remains readable without JavaScript');

  assert.match(noJavaScriptBlock, /page\.locator\('#timeline-entries'\)\.textContent\(\)/);
  assert.match(noJavaScriptBlock, /JSON\.parse\(serializedEntries\)/);
  assert.match(noJavaScriptBlock, /page\.locator\('\[data-timeline-entry\]'\)\)\.toHaveCount\(timelineEntries\.length\)/);
  assert.match(noJavaScriptBlock, /page\.locator\('\[data-timeline-entry\]\[hidden\]'\)\)\.toHaveCount\(0\)/);
  assertPolicyRouteCoverage(noJavaScriptBlock, /for \(const route of policyRoutes\) \{[\s\S]*?await page\.goto\(route\)/);
});

test('classification controls use native keyboard-reachable form elements', () => {
  assert.match(siteSpec, /page\.getByLabel\('Sector'\)\.selectOption\('financial_services'\)/);
  assert.match(siteSpec, /page\.getByRole\('radio', \{ name: 'All documents and versions' \}\)\.check\(\)/);
  assert.match(stylesheet, /:is\(a, button, input, select, \[tabindex\]\):focus-visible/);
});

test('the scoped policy-route guard rejects an in-memory collection that is never navigated', () => {
  const deliberatelyRegressedBlock = `
    test('regressed', async ({ page }) => {
      await page.goto('timeline/');
      const policyRoutes = await page.locator('[data-timeline-entry] a[href*="/policies/"]');
      expect(policyRoutes.length).toBeGreaterThan(0);
    });
  `;

  assert.throws(
    () => assertPolicyRouteCoverage(deliberatelyRegressedBlock, /for \(const route of policyRoutes\) await page\.goto\(route\)/),
    assert.AssertionError,
  );
});

test('the coverage summary has a labelled section, a description list and a machine-readable date', () => {
  assert.match(pathway, /<section[\s\S]*aria-labelledby="core-policy-pathway"/);
  assert.match(pathway, /<h2 id="core-policy-pathway">/);
  assert.match(pathway, /<dl class="coverage-summary"/);
  assert.match(pathway, /<dt>Principal documents<\/dt>[\s\S]*?<dd>\{coverage\.principal_documents\}<\/dd>/);
  assert.match(
    pathway,
    /<dt>Supporting files and versions<\/dt>[\s\S]*?<dd>\{coverage\.supporting_files_and_versions\}<\/dd>/,
  );
  assert.match(pathway, /<time datetime=\{coverage\.last_verified_date\}>/);
});
