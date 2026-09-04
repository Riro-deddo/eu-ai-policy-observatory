import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const timeline = readFileSync(new URL('../src/components/Timeline.astro', import.meta.url), 'utf8');
const policyMap = readFileSync(new URL('../src/components/PolicyMap.astro', import.meta.url), 'utf8');
const policyMapLayout = readFileSync(new URL('../src/lib/policy-map.ts', import.meta.url), 'utf8');
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
  assert.match(timeline, /documentTypeLabel\(entry\.documentType/);
  assert.match(timeline, /entry\.kind === 'document' \? 'Document date' : 'Event date'/);
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
  assert.match(policyMap, /relationshipTypeLabel\(relationship\.relationship_type\)/);
  assert.match(policyMap, /policyMapStageLabel\(stage\)/);
});

test('policy routes are generated from published data and distinguish official and analytical content', () => {
  assert.match(policyRoute, /export function getStaticPaths\(\)/);
  assert.match(policyRoute, /data\.policies\.map/);
  assert.match(policyRoute, /Research-defined policy grouping/);
  assert.match(policyRoute, /Research assessment relationships/);
  assert.match(policyRoute, /import\.meta\.env\.BASE_URL/);
});

test('the analytical policy grouping is not presented as an official EU policy description', () => {
  assert.match(policyRoute, /Research-defined policy grouping/);
  assert.match(policyRoute, /organises the corpus analytically/);
  assert.match(policyRoute, /not an official EU policy title/);
  assert.doesNotMatch(policyRoute, /Official policy description/);
});

test('focused and hovered policy-map nodes keep their labels legible and visibly focused', () => {
  assert.match(
    stylesheet,
    /\.policy-map__nodes a:hover text, \.policy-map__nodes a:focus text \{[\s\S]*?fill: var\(--canvas\);/,
  );
  assert.match(
    stylesheet,
    /\.policy-map__nodes a:focus rect \{[\s\S]*?stroke: var\(--focus\);/,
  );
});

test('policy-map stages use the controlled semantic column order before deterministic unknown stages', () => {
  assert.match(
    policyMapLayout,
    /const semanticPolicyMapStages = \[\s*'policy',\s*'agenda_setting',\s*'coordination',\s*'consultation',\s*'proposal',\s*'negotiation',\s*'adoption',\s*'implementation',\s*'unclassified',\s*\]/,
  );
  assert.match(policyMapLayout, /const stages = \[.*semanticPolicyMapStages.*unexpectedStages.*\]/s);
});

test('Policy Map binds its rendered SVG dimensions to its computed layout', () => {
  assert.match(policyMap, /layoutPolicyMapNodes/);
  assert.match(policyMap, /<tspan/);
  assert.match(policyMap, /aria-label=\{`\$\{node\.label\} \(\$\{stageLabel\(node\.stage\)\}\)`\}/);
  assert.match(policyMap, /<svg width=\{layout\.width\} height=\{layout\.height\}/);
});

test('policy-map relationships retain positioned geometry at their rendering boundary', () => {
  assert.match(policyMap, /type PositionedMapNode = MapNode & PolicyMapGeometry;/);
  assert.match(policyMap, /source: PositionedMapNode;/);
  assert.match(policyMap, /target: PositionedMapNode;/);
});
