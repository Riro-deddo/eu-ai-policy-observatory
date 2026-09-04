import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const config = readFileSync(new URL('../astro.config.mjs', import.meta.url), 'utf8');
const playwrightConfig = readFileSync(new URL('../playwright.config.ts', import.meta.url), 'utf8');
const explorer = readFileSync(new URL('../src/components/CorpusExplorer.astro', import.meta.url), 'utf8');
const filter = readFileSync(new URL('../src/lib/filter.ts', import.meta.url), 'utf8');
const home = readFileSync(new URL('../src/pages/index.astro', import.meta.url), 'utf8');
const methodology = readFileSync(new URL('../src/pages/methodology.astro', import.meta.url), 'utf8');
const about = readFileSync(new URL('../src/pages/about.astro', import.meta.url), 'utf8');
const map = readFileSync(new URL('../src/components/PolicyMap.astro', import.meta.url), 'utf8');
const mapLayout = readFileSync(new URL('../src/lib/policy-map.ts', import.meta.url), 'utf8');
const pathway = readFileSync(new URL('../src/components/PolicyPathway.astro', import.meta.url), 'utf8');
const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');
const siteSpec = readFileSync(new URL('./site.spec.ts', import.meta.url), 'utf8');

test('canonical browser assertions derive the deployment origin and base path from their environment', () => {
  assert.match(config, /trailingSlash:\s*'always'/);
  assert.match(playwrightConfig, /const siteOrigin = process\.env\.SITE_ORIGIN \?\? 'https:\/\/eu-ai-policy-observatory\.test';/);
  assert.match(playwrightConfig, /const basePath = process\.env\.BASE_PATH \?\? '\/eu-ai-policy-observatory';/);
  assert.match(siteSpec, /const siteOrigin = process\.env\.SITE_ORIGIN \?\? 'https:\/\/eu-ai-policy-observatory\.test';/);
  assert.match(siteSpec, /const basePath = process\.env\.BASE_PATH \?\? '\/eu-ai-policy-observatory';/);
  assert.match(siteSpec, /new URL\('policy-map\/', canonicalBase\)\.href/);
  assert.doesNotMatch(siteSpec, /https:\/\/eu-ai-policy-observatory\.test\/eu-ai-policy-observatory\/policy-map\//);
});

test('Corpus enhancement hydrates a whitelisted query before applying filters', () => {
  assert.match(explorer, /parseCorpusCriteria\(new URLSearchParams\(window\.location\.search\)\)/);
  assert.match(explorer, /form\.elements\.namedItem\(name\)/);
  assert.match(explorer, /hydrateControlsFromUrl\(criteria\);/);
  assert.match(explorer, /applyFilters\(readFormCriteria\(\)\);/);
});

test('the Corpus browser assertion preserves the descending-date filter order', () => {
  assert.match(filter, /second\.publication_date\.localeCompare\(first\.publication_date, 'en-GB'\)/);
  assert.match(
    siteSpec,
    /await expect\(visibleRecords\)\.toContainText\(\[\s*'AI Liability Directive proposal',\s*'Artificial Intelligence Act proposal',\s*'White Paper on Artificial Intelligence',\s*'Ethics Guidelines for Trustworthy AI',\s*'Artificial Intelligence for Europe',\s*\]\);/,
  );
});

test('Policy Map exposes semantic stage headings and linked nodes within a labelled group', () => {
  assert.match(map, /role="group"/);
  assert.match(map, /aria-describedby="policy-map-svg-description"/);
  assert.match(map, /data-policy-map-stage/);
  assert.match(map, /aria-label=\{`\$\{node\.label\} \(\$\{stageLabel\(node\.stage\)\}\)`\}/);
  assert.match(mapLayout, /export function policyMapStageX/);
});

test('Policy Map and filter controls meet the reviewed minimum text sizes', () => {
  assert.match(stylesheet, /\.primary-nav a \{[^}]*font-size: 0\.875rem;/);
  assert.match(stylesheet, /\.corpus-filters label \{[^}]*font-size: 0\.875rem;/);
  assert.match(stylesheet, /\.timeline-filters label \{[^}]*font-size: 0\.875rem;/);
  assert.match(stylesheet, /\.policy-map__nodes text \{[^}]*font-size: 12px;/);
  assert.match(stylesheet, /\.policy-map__nodes text \+ text \{[^}]*font-size: 14px;/);
});

test('end-to-end assertions scope all reviewed potentially ambiguous text selectors', () => {
  assert.match(siteSpec, /page\.locator\('main'\)\.getByText\('Created and maintained by Yichen Hao', \{ exact: true \}\)/);
  assert.match(siteSpec, /getByRole\('link', \{ name: title, exact: true \}\)/);
  assert.match(siteSpec, /const legend = page\.locator\('\.policy-map__legend'\);/);
  assert.match(siteSpec, /legend\.getByText\('Official relationship', \{ exact: true \}\)/);
  assert.match(siteSpec, /legend\.getByText\('Analytical relationship', \{ exact: true \}\)/);
});

test('Home renders current corpus coverage from the generated data contract', () => {
  assert.match(home, /<PolicyPathway[\s\S]*coverage=\{data\.coverage\}/);
  assert.match(pathway, /Coverage: \{coverage\.from_year\}–\{coverage\.to_year\}/);
  assert.match(pathway, /\{coverage\.principal_documents\}/);
  assert.match(pathway, /\{coverage\.supporting_files_and_versions\}/);
  assert.match(pathway, /datetime=\{coverage\.last_verified_date\}/);
  assert.match(pathway, /Pending-review records are excluded from public totals\./);
});

test('public pages no longer describe the active corpus as the seven-document 2018–2024 seed', () => {
  const publicCopy = [home, methodology, about, pathway].join('\n');

  assert.doesNotMatch(publicCopy, /2018[–-]2024/);
  assert.doesNotMatch(publicCopy, /seven (?:reviewed, published )?documents/i);
});

test('Methodology separates implemented corpus work from the planned LLM protocol', () => {
  assert.match(methodology, /Current corpus method/);
  assert.match(methodology, /Planned LLM comparison protocol/);
  assert.match(methodology, /not all EU digital law/);
  assert.match(methodology, /included[\s\S]*merged[\s\S]*excluded[\s\S]*pending/);
});
