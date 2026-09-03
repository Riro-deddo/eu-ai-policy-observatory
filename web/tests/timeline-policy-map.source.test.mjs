import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const timeline = readFileSync(new URL('../src/components/Timeline.astro', import.meta.url), 'utf8');
const policyMap = readFileSync(new URL('../src/components/PolicyMap.astro', import.meta.url), 'utf8');
const timelinePage = readFileSync(new URL('../src/pages/timeline.astro', import.meta.url), 'utf8');
const policyMapPage = readFileSync(new URL('../src/pages/policy-map.astro', import.meta.url), 'utf8');
const policyRoute = readFileSync(new URL('../src/pages/policies/[id].astro', import.meta.url), 'utf8');
const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');

test('Timeline retains a complete no-JavaScript chronology and escapes embedded data', () => {
  assert.match(timeline, /<div[^>]*data-timeline-list/);
  assert.match(timeline, /<noscript>[\s\S]*?complete chronology is shown below[\s\S]*?<\/noscript>/);
  assert.match(timeline, /aria-live="polite"/);
  assert.match(timeline, /JSON\.stringify\(entries\)\.replaceAll\('<', '\\\\u003c'\)/);
  assert.match(timeline, /data-timeline-entry/);
  assert.match(timelinePage, /<Timeline data=\{data\} \/>/);
});

test('Policy Map has an accessible SVG, explicit relationship legend and text alternative', () => {
  assert.match(policyMap, /<svg[^>]*aria-labelledby=/);
  assert.match(policyMap, /Official relationship/);
  assert.match(policyMap, /Analytical relationship/);
  assert.match(stylesheet, /\.policy-map__edge--analytical \{[\s\S]*?stroke-dasharray:/);
  assert.match(policyMap, /data-policy-map-edge/);
  assert.match(policyMap, /data-policy-map-relationship/);
  assert.match(policyMap, /<ol[^>]*data-policy-map-relationships/);
  assert.match(policyMapPage, /<PolicyMap data=\{data\} \/>/);
});

test('policy routes are generated from published data and distinguish official and analytical content', () => {
  assert.match(policyRoute, /export function getStaticPaths\(\)/);
  assert.match(policyRoute, /data\.policies\.map/);
  assert.match(policyRoute, /Official policy description/);
  assert.match(policyRoute, /Research assessment relationships/);
  assert.match(policyRoute, /import\.meta\.env\.BASE_URL/);
});
