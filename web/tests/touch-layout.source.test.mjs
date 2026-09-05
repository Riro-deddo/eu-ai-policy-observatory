import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const stylesheet = readFileSync(new URL('../src/styles/global.css', import.meta.url), 'utf8');
const pathway = readFileSync(new URL('../src/components/PolicyPathway.astro', import.meta.url), 'utf8');
const siteSpec = readFileSync(new URL('./site.spec.ts', import.meta.url), 'utf8');

test('coarse-pointer controls provide 44px touch targets without desktop rules', () => {
  assert.match(
    stylesheet,
    /@media \(pointer: coarse\) \{[\s\S]*?\.research-lenses a, \.atlas-links a, \.primary-nav a \{[\s\S]*?display: inline-flex;[\s\S]*?min-block-size: 44px;[\s\S]*?padding-block: 0\.5rem;/,
  );
});

test('pathway titles have a dedicated class in the mobile grid column', () => {
  assert.match(pathway, /<span class="pathway-list__title">\{item\.title\}<\/span>/);
  assert.match(
    stylesheet,
    /@media \(max-width: 760px\) \{[\s\S]*?\.pathway-list__title \{ grid-column: 2; \}/,
  );
});

test('classification filters and tags can shrink and wrap at narrow widths', () => {
  assert.match(stylesheet, /\.corpus-filters :is\(input, select\)[^{]*\{[\s\S]*?min-inline-size: 0;/);
  assert.match(stylesheet, /\.timeline-filters input[^{]*\{[\s\S]*?min-inline-size: 0;/);
  assert.match(stylesheet, /\.timeline-filters select[^{]*\{[\s\S]*?min-inline-size: 0;/);
  assert.match(stylesheet, /\.tag-list \{[\s\S]*?display: flex;[\s\S]*?flex-wrap: wrap;/);
  assert.match(stylesheet, /\.record-classifications \{[\s\S]*?min-inline-size: 0;/);
  assert.match(siteSpec, /page\.setViewportSize\(\{ width: 375, height: 844 \}\)/);
});
