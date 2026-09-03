# EU AI Policy Observatory Static Research Atlas UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the six-page, English-language, read-only research atlas that presents the published EU AI policy database on desktop and mobile.

**Architecture:** Astro generates static HTML from `generated/public-data.json`. Core content and navigation work without JavaScript; small TypeScript modules progressively enhance corpus filtering, timeline filtering and the policy-map view. All pages consume the same exported data contract from the database foundation plan.

**Tech Stack:** Astro static output, TypeScript, vanilla browser APIs, Vitest, Playwright, semantic HTML and CSS custom properties.

**Spec:** `docs/superpowers/specs/2026-09-03-eu-ai-policy-observatory-design.md`

**Dependency:** Complete `docs/superpowers/plans/2026-09-03-database-foundation.md` first.

## Global Constraints

- The database remains the primary project output; the interface is a derived read-only view.
- Public copy uses British academic English.
- The top-level navigation is exactly Home, Policy Map, Timeline, Corpus, Methodology and About.
- Official metadata and research assessment are visually and semantically separate.
- Published records are the only records available to the website build.
- Core content remains readable without JavaScript.
- Search and filters run locally; the website performs no API calls.
- No speculative counts, inferred relationships or automatically generated summaries are displayed.
- No university affiliation is displayed without later explicit authorisation.
- Each task ends with its own tests and commit.

---

## File Structure

```text
web/package.json                         Front-end commands and dependencies
web/astro.config.mjs                    Static GitHub Pages configuration
web/tsconfig.json                        Strict TypeScript configuration
web/src/env.d.ts                         Astro type reference
web/src/lib/data.ts                      Typed build-time public-data loader
web/src/lib/filter.ts                    Pure corpus and timeline filtering
web/src/lib/types.ts                     Public export interfaces
web/src/layouts/BaseLayout.astro         Shared metadata, header and footer
web/src/components/SiteHeader.astro      Six-item primary navigation
web/src/components/SiteFooter.astro      Authorship and provenance footer
web/src/components/ResearchLenses.astro  Four RP-derived concepts
web/src/components/PolicyPathway.astro   Core 2018–2024 pathway
web/src/components/CorpusExplorer.astro  Progressive-enhancement corpus browser
web/src/components/PolicyMap.astro       Relationship graph and text alternative
web/src/components/Timeline.astro        Event chronology and filters
web/src/pages/index.astro                 Home
web/src/pages/policy-map.astro            Policy Map
web/src/pages/timeline.astro              Timeline
web/src/pages/policies/[id].astro         Stable policy pages
web/src/pages/corpus/index.astro           Corpus
web/src/pages/corpus/[slug].astro          Stable document pages
web/src/pages/methodology.astro            Methodology
web/src/pages/about.astro                  About
web/src/styles/global.css                  Responsive editorial design system
web/tests/filter.test.ts                   Pure filtering tests
web/tests/fixtures/documents.ts            Typed published-document fixtures
web/tests/site.spec.ts                     Playwright navigation and accessibility smoke tests
web/tests/no-js.spec.ts                    No-JavaScript content verification
web/playwright.config.ts                   Static preview test configuration
```

### Task 1: Establish the Astro Shell and Typed Data Boundary

**Files:**
- Create: `web/package.json`
- Create: `web/astro.config.mjs`
- Create: `web/tsconfig.json`
- Create: `web/src/env.d.ts`
- Create: `web/src/lib/types.ts`
- Create: `web/src/lib/data.ts`
- Create: `web/src/layouts/BaseLayout.astro`
- Create: `web/src/components/SiteHeader.astro`
- Create: `web/src/components/SiteFooter.astro`
- Create: `web/src/styles/global.css`
- Create: `web/src/pages/index.astro`
- Create: `web/tests/site.spec.ts`
- Create: `web/playwright.config.ts`

**Interfaces:**
- Consumes: `generated/public-data.json` from the database foundation.
- Produces: `loadPublicData(): PublicData` for every page and component.
- Produces: `BaseLayout` props `{ title: string; description: string; canonicalPath: string }`.
- Produces: a responsive shared header and footer.

- [ ] **Step 1: Initialise the front-end package without starter content**

From the repository root run:

```powershell
New-Item -ItemType Directory -Force web
Set-Location web
pnpm init
pnpm add astro
pnpm add -D typescript vitest @playwright/test @astrojs/check
```

Edit `web/package.json` so scripts are exactly:

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro check && astro build",
    "preview": "astro preview",
    "test": "vitest run",
    "test:e2e": "playwright test"
  }
}
```

Commit the generated `pnpm-lock.yaml`; it pins the resolved dependency graph.

- [ ] **Step 2: Write the failing homepage smoke test**

Create `web/tests/site.spec.ts`:

```typescript
import { expect, test } from '@playwright/test';

test('homepage exposes the six primary destinations', async ({ page }) => {
  await page.goto('./');
  const navigation = page.getByRole('navigation', { name: 'Primary' });
  await expect(navigation.getByRole('link')).toHaveCount(6);
  await expect(page.getByRole('heading', { level: 1 })).toContainText(
    'How EU AI policy is formulated, interpreted and transformed',
  );
});
```

- [ ] **Step 3: Configure Playwright and confirm failure**

Create `web/playwright.config.ts` with `webServer.command` set to `pnpm build && pnpm preview --host 127.0.0.1`, `webServer.url` set to `http://127.0.0.1:4321/eu-ai-policy-observatory/`, `use.baseURL` set to the same URL, and projects for Chromium desktop and a 390×844 mobile viewport.

Run:

```powershell
Set-Location web
pnpm exec playwright install chromium
pnpm test:e2e
```

Expected: the test fails because the Astro shell and homepage do not exist.

- [ ] **Step 4: Define the public-data TypeScript interfaces**

In `web/src/lib/types.ts`, define these interfaces matching the public export exactly:

```typescript
export interface PublicData {
  generated_at: string;
  policies: Policy[];
  documents: DocumentRecord[];
  events: PolicyEvent[];
  concepts: Concept[];
  institutions: Institution[];
  relationships: Relationship[];
  sources: Source[];
}

interface PublishedEntity {
  id: string;
  publication_status: 'published';
  created_at: string;
  updated_at: string;
}

export interface Policy extends PublishedEntity {
  name: string;
  short_name: string;
  summary: string;
  policy_family: string;
  policy_status: string;
  scope_note: string;
}

export interface PolicyEvent extends PublishedEntity {
  event_type: string;
  event_date: string;
  title: string;
  description: string;
  policy_id: string;
  document_id: string | null;
  source_id: string;
}

export interface Concept extends PublishedEntity {
  name: string;
  definition: string;
  research_scope: string;
  eurovoc_uri: string | null;
  notes: string;
}

export interface Institution extends PublishedEntity {
  official_name: string;
  short_name: string;
  institution_type: string;
  official_url: string;
}

export interface Source extends PublishedEntity {
  source_type: string;
  url: string;
  publisher: string;
  retrieved_at: string;
  last_verified_at: string;
  verification_note: string;
}

export interface CorpusAssessment {
  document_id: string;
  corpus_tier: string;
  policy_stage: string;
  inclusion_rationale: string;
  researcher_notes: string;
  review_status: string;
  reviewed_by: string;
  reviewed_at: string;
}

export interface Relationship extends PublishedEntity {
  source_entity_type: string;
  source_entity_id: string;
  target_entity_type: string;
  target_entity_id: string;
  relationship_type: string;
  basis: 'official' | 'analytical';
  rationale: string;
  evidence_source_id: string;
  verification_status: string;
}

export interface DocumentRecord {
  id: string;
  slug: string;
  official_title: string;
  short_title: string;
  document_type: string;
  publication_date: string;
  legal_status: string;
  language: string;
  celex: string | null;
  eli: string | null;
  official_summary: string;
  publication_status: 'published';
  created_at: string;
  updated_at: string;
  policies: Policy[];
  concepts: Concept[];
  institutions: Array<Institution & { role: string }>;
  sources: Source[];
  corpus_assessment: CorpusAssessment;
}
```

Do not use `any` anywhere in the data boundary.

- [ ] **Step 5: Implement a fail-fast build-time data loader**

`loadPublicData()` resolves `../generated/public-data.json` from the `web/` build working directory with `resolve(process.cwd(), '..', 'generated', 'public-data.json')`. It must throw an error containing the resolved path if the file is missing and must reject any entity in any exported collection whose publication status is not `published`.

- [ ] **Step 6: Build the shared semantic shell**

Configure Astro with an environment-driven origin and a fixed repository base path:

```javascript
const site = process.env.SITE_ORIGIN ?? 'https://eu-ai-policy-observatory.test';
const base = process.env.BASE_PATH ?? '/eu-ai-policy-observatory';

export default defineConfig({ output: 'static', site, base });
```

Create `BaseLayout.astro` with:

- One `main` landmark.
- A skip link.
- `SiteHeader` and `SiteFooter`.
- Per-page title, description and canonical URL.
- No tracking script.

Create the six-link header in this exact order: Home, Policy Map, Timeline, Corpus, Methodology, About. The footer contains “Created and maintained by Yichen Hao” and a link to Methodology.

Prefix every internal link with `import.meta.env.BASE_URL`; do not hard-code root-relative links that would bypass the GitHub Pages repository base path.

- [ ] **Step 7: Implement the editorial design tokens and responsive shell**

In `global.css`, define colour, spacing, type, measure and border tokens for light and dark system preferences. Use a restrained editorial serif for headings with a system sans-serif for metadata. Preserve visible focus indicators, minimum 44-pixel coarse-pointer targets, readable line lengths and layouts that reflow at 760 pixels. Do not use fixed viewport-height sections or horizontal page scrolling.

- [ ] **Step 8: Add the minimal homepage and run tests**

Create `index.astro` with the approved project heading and a short database-first explanation. Run:

```powershell
pnpm build
pnpm test:e2e
```

Expected: Astro build succeeds and the desktop and mobile homepage tests pass.

- [ ] **Step 9: Commit the site foundation**

```powershell
git add web
git commit -m "feat: establish static research atlas shell"
```

### Task 2: Build Home, Methodology and About Pages

**Files:**
- Create: `web/src/components/ResearchLenses.astro`
- Create: `web/src/components/PolicyPathway.astro`
- Modify: `web/src/pages/index.astro`
- Create: `web/src/pages/methodology.astro`
- Create: `web/src/pages/about.astro`
- Modify: `web/tests/site.spec.ts`

**Interfaces:**
- Consumes: `loadPublicData()` from Task 1.
- Produces: `ResearchLenses({ concepts: Concept[] })`.
- Produces: `PolicyPathway({ documents: DocumentRecord[]; events: PolicyEvent[] })`.
- Produces static pages at `/`, `/methodology/` and `/about/`.

- [ ] **Step 1: Write failing content tests**

Add Playwright tests:

```typescript
test('home presents the four research lenses from data', async ({ page }) => {
  await page.goto('./');
  for (const concept of ['Risk', 'Trustworthiness', 'Accountability', 'Compliance']) {
    await expect(page.getByRole('link', { name: concept })).toBeVisible();
  }
});

test('methodology states the publication boundary', async ({ page }) => {
  await page.goto('methodology/');
  await expect(page.getByText('Only published records appear in the public interface.')).toBeVisible();
});

test('about uses project-led authorship without university affiliation', async ({ page }) => {
  await page.goto('about/');
  await expect(page.getByText('Created and maintained by Yichen Hao')).toBeVisible();
  await expect(page.getByText(/University of Edinburgh/i)).toHaveCount(0);
});
```

- [ ] **Step 2: Run the focused tests and confirm failure**

Run `pnpm test:e2e --grep "research lenses|publication boundary|project-led"`.

Expected: all three tests fail because the approved content is absent.

- [ ] **Step 3: Build the research-lens and pathway components**

Render only concept records with IDs `risk`, `trustworthiness`, `accountability` and `compliance`, in that order. Each lens links to the Corpus with a query parameter but remains a normal link without JavaScript. The pathway sorts the selected core documents and events by ISO date and never inserts an event not present in the data.

- [ ] **Step 4: Complete the homepage**

Use the approved hierarchy:

```text
Project argument
Research lenses
Core policy pathway
Links to Policy Map and Corpus
```

Use the sentence “The database is the primary research output; this interface is a view of it.” Avoid unverified counts and “live” status language.

- [ ] **Step 5: Create Methodology and About**

Methodology explains inclusion criteria, `draft → pending_review → verified → published`, official versus analytical data, provenance, and the planned LLM comparison as future research. About states project purpose, current 2018–2024 scope, limitations and authorship. Do not reproduce the full research proposal.

- [ ] **Step 6: Run the focused and full browser tests**

Run:

```powershell
pnpm build
pnpm test:e2e
```

Expected: all tests pass in both configured viewports.

- [ ] **Step 7: Commit the explanatory pages**

```powershell
git add web/src web/tests/site.spec.ts
git commit -m "feat: add research context pages"
```

### Task 3: Build the Searchable Corpus and Stable Document Pages

**Files:**
- Create: `web/src/lib/filter.ts`
- Create: `web/src/components/CorpusExplorer.astro`
- Create: `web/src/pages/corpus/index.astro`
- Create: `web/src/pages/corpus/[slug].astro`
- Create: `web/tests/filter.test.ts`
- Create: `web/tests/fixtures/documents.ts`
- Modify: `web/tests/site.spec.ts`

**Interfaces:**
- Consumes: `DocumentRecord[]` from `PublicData`.
- Produces: `filterDocuments(documents: DocumentRecord[], criteria: CorpusCriteria) -> DocumentRecord[]`.
- Produces: `CorpusCriteria` with optional string properties `query`, `year`, `institution`, `documentType`, `legalStatus`, `policyStage`, `concept` and `corpusTier`.
- Produces static routes `/corpus/` and `/corpus/<slug>/`.

Define the criteria exactly as:

```typescript
export interface CorpusCriteria {
  query?: string;
  year?: string;
  institution?: string;
  documentType?: string;
  legalStatus?: string;
  policyStage?: string;
  concept?: string;
  corpusTier?: string;
}
```

- [ ] **Step 1: Write failing pure filter tests**

Create `web/tests/filter.test.ts`:

```typescript
import { describe, expect, it } from 'vitest';
import { filterDocuments } from '../src/lib/filter';
import { publishedDocuments } from './fixtures/documents';

describe('filterDocuments', () => {
  it('matches title and CELEX case-insensitively', () => {
    expect(filterDocuments(publishedDocuments, { query: '32024r1689' }).map(d => d.id))
      .toEqual(['artificial-intelligence-act-2024']);
  });

  it('combines concept and institution filters', () => {
    const result = filterDocuments(publishedDocuments, {
      concept: 'risk',
      institution: 'european-commission',
    });
    expect(result.every(d => d.concepts.some(c => c.id === 'risk'))).toBe(true);
    expect(result.every(d => d.institutions.some(i => i.id === 'european-commission'))).toBe(true);
  });
});
```

Add a typed `web/tests/fixtures/documents.ts` containing two compact published records.

- [ ] **Step 2: Run unit tests and confirm failure**

Run `pnpm test`.

Expected: tests fail because `filterDocuments` does not exist.

- [ ] **Step 3: Implement deterministic filtering**

Normalise text with `toLocaleLowerCase('en-GB')`. Treat omitted criteria as no restriction. Search `official_title`, `short_title`, non-null `celex` and non-null `eli`. Combine separate filters with logical AND. Return a new array sorted by publication date descending and then short title ascending; never mutate input.

- [ ] **Step 4: Run unit tests**

Run `pnpm test`.

Expected: all filter tests pass.

- [ ] **Step 5: Write failing Corpus browser tests**

Add tests that:

- Open `corpus/` relative to the configured base URL and find every published seed document as a normal link.
- Search `32024R1689` and leave only the final AI Act visible.
- Combine the Risk concept and European Commission filters.
- Reset filters and restore the complete list.
- Follow the AI Act link and find official metadata, Research assessment, source URL, CELEX and verification date sections.

- [ ] **Step 6: Build the progressively enhanced Corpus page**

Server-render the complete published list inside a semantic list or table. Use a GET-style form with labelled native controls. A small TypeScript module intercepts input, calls the same filtering semantics as `filterDocuments`, updates `hidden` attributes and announces the result count through `aria-live="polite"`. With JavaScript disabled, all records and links remain visible.

- [ ] **Step 7: Generate stable document routes**

Use Astro `getStaticPaths()` from `loadPublicData().documents`. Each page sets its canonical path from the record slug and renders separate sections in this order:

```text
Official metadata
Institutions and roles
Official sources and identifiers
Policy placement and concepts
Research assessment
Relationships
Verification
```

Render absent CELEX or ELI as “Not assigned”. Label every analytical field as research assessment. External official links open normally without forcing a new tab.

- [ ] **Step 8: Run all UI tests**

Run:

```powershell
pnpm test
pnpm build
pnpm test:e2e
```

Expected: all unit and browser tests pass.

- [ ] **Step 9: Commit Corpus browsing**

```powershell
git add web/src/lib web/src/components/CorpusExplorer.astro web/src/pages/corpus web/tests
git commit -m "feat: add searchable policy corpus"
```

### Task 4: Build Timeline and Policy Map Views

**Files:**
- Create: `web/src/components/Timeline.astro`
- Create: `web/src/components/PolicyMap.astro`
- Create: `web/src/pages/timeline.astro`
- Create: `web/src/pages/policy-map.astro`
- Create: `web/src/pages/policies/[id].astro`
- Modify: `web/src/lib/filter.ts`
- Modify: `web/tests/filter.test.ts`
- Modify: `web/tests/site.spec.ts`

**Interfaces:**
- Consumes: published events, policies, documents and relationships.
- Produces: `buildTimelineEntries(data: PublicData) -> TimelineEntry[]` and `filterTimeline(entries: TimelineEntry[], criteria: TimelineCriteria) -> TimelineEntry[]`.
- Produces an accessible graph plus equivalent relationship list.
- Produces stable policy routes at `/policies/<id>/`.

Define the timeline filter contract as:

```typescript
export interface TimelineCriteria {
  institution?: string;
  documentType?: string;
  policyStage?: string;
  eventType?: string;
}

export interface TimelineEntry {
  id: string;
  kind: 'document' | 'event';
  date: string;
  title: string;
  href: string;
  institutionIds: string[];
  documentType: string | null;
  policyStage: string | null;
  eventType: string | null;
}
```

- [ ] **Step 1: Write failing event-filter tests**

Add Vitest cases proving that events sort by date ascending, combined institution and event-type filters use logical AND, and input arrays are not mutated.

- [ ] **Step 2: Run unit tests and confirm failure**

Run `pnpm test`.

Expected: new timeline-filter tests fail because `buildTimelineEntries` and `filterTimeline` do not exist.

- [ ] **Step 3: Implement event filtering**

Build entries from both published documents and events. Document entries carry their own institutions, document type and corpus-assessment policy stage. Events associated with a document inherit those three fields; events without a document use empty or null values. Use the same normalisation helpers as corpus filtering. Support `institution`, `documentType`, `policyStage` and `eventType`. Return ISO-date ascending order with ID as the deterministic tie-breaker.

- [ ] **Step 4: Write failing browser tests for both views**

Add tests that:

- Timeline displays the 2018–2024 boundary and every published event.
- Selecting `adoption` hides non-adoption events and announces the result count.
- Policy Map legend contains “Official relationship” and “Analytical relationship”.
- Every visual relationship has an equivalent text-list entry.
- A policy or document node links to a stable page rather than acting as a dead graphic.

- [ ] **Step 5: Build the Timeline**

Render a semantic ordered list grouped by year before enhancement. Each event includes date, type, title, associated policy or document and evidence source. Enhance native selects locally; do not recalculate or invent dates in the browser.

- [ ] **Step 6: Build the Policy Map**

Generate a restrained inline SVG from published relationship records at build time. Use solid strokes for `official`, dashed strokes for `analytical`, and pair line style with explicit labels so colour is never the only distinction. Provide a normal HTML list immediately after the graphic containing source entity, relationship label, target entity, basis, rationale and evidence link.

For the small seed corpus, use deterministic predefined columns by policy stage rather than a force-directed runtime simulation. This avoids unstable layouts and preserves no-JavaScript legibility.

Generate one `/policies/<id>/` page for each published policy. Each policy page renders its summary, family, status, scope note, related documents and relationships. Policy nodes link to these routes; document nodes link to their Corpus record routes.

- [ ] **Step 7: Run the complete front-end suite**

Run:

```powershell
pnpm test
pnpm build
pnpm test:e2e
```

Expected: all tests pass in desktop and mobile projects.

- [ ] **Step 8: Commit the policy exploration views**

```powershell
git add web/src web/tests
git commit -m "feat: add policy map and timeline"
```

### Task 5: Complete Accessibility, Responsive and Cross-Page Verification

**Files:**
- Modify: `web/src/styles/global.css`
- Modify: `web/src/layouts/BaseLayout.astro`
- Modify: `web/src/components/*.astro`
- Modify: `web/tests/site.spec.ts`
- Create: `web/tests/no-js.spec.ts`

**Interfaces:**
- Consumes: all UI routes from Tasks 1–4.
- Produces: a release-ready static `web/dist/` directory.

- [ ] **Step 1: Add failing cross-page assertions**

Add Playwright tests that visit all six top-level pages and every generated document route. Assert one visible `h1`, one `main`, a working skip link, no horizontal overflow at 390 pixels, and no browser console errors.

Create `no-js.spec.ts` with JavaScript disabled and assert that Home, Corpus, every document page, Timeline and the Policy Map relationship list remain readable.

- [ ] **Step 2: Run browser tests and record failures**

Run `pnpm test:e2e`.

Expected: at least the new no-JavaScript or responsive assertions fail before final remediation.

- [ ] **Step 3: Fix semantics and responsive layout**

Correct heading order, visible labels, focus behaviour, table overflow, touch-target spacing and narrow-screen stacking. Keep essential text outside hover-only interactions. Do not reduce essential text below 14 CSS pixels or supporting text below 12 CSS pixels.

- [ ] **Step 4: Verify production output contains no local-only paths or origins**

Run:

```powershell
$unsafeOutput = rg -n -e "C:\\\\Users\\\\" -e "/Users/" -e "/home/" -e "localhost" web/dist
if ($LASTEXITCODE -eq 0) { $unsafeOutput; throw "Local-only value found in static output" }
if ($LASTEXITCODE -gt 1) { throw "Static-output scan failed" }
```

Expected: no local filesystem paths and no localhost URLs. The database export tests already enforce that canonical `draft`, `pending_review` and `verified` records do not enter the website data; Methodology may still name those workflow states in explanatory prose.

- [ ] **Step 5: Run the complete UI gate**

Run:

```powershell
pnpm test
pnpm build
pnpm test:e2e
```

Expected: all commands exit 0.

- [ ] **Step 6: Commit the completed UI**

```powershell
git add web
git commit -m "test: verify accessible responsive atlas"
```

## Plan 2 Completion Gate

Do not begin deployment work until:

- All six approved pages build as static HTML.
- At least six document routes are generated from the public export.
- Search, filters, timeline and policy-map links pass Playwright tests.
- Core content remains readable without JavaScript.
- No unpublished record or local path enters `web/dist/`.
- Desktop and 390-pixel mobile test projects pass.
