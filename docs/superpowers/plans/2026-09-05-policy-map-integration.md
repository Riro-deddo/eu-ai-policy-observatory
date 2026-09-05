# Interactive Policy Map Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan. Steps use checkbox syntax for tracking.

**Goal:** Integrate the user-approved local Policy Map into the English static research atlas.

**Architecture:** Generate deterministic ELK geometry at build time from the existing public export. Astro renders the complete citation-friendly relationship list without JavaScript; a small typed client adds grouped overview, selection and direct-neighborhood exploration. Keep graph semantics separate from geometry.

**Tech Stack:** Astro 5.17.1, TypeScript, SVG, ELK.js 0.12.0, Node tests, Vitest, Playwright.

**Spec:** The approved preview is `../policy-map-preview/README.md`, `../policy-map-preview/public/index.html`, `../policy-map-preview/public/style.css`, and `../policy-map-preview/public/app.js`. The user approved it on 2026-09-05. These files are local design evidence, not production dependencies.

## Global Constraints

- All committed code, documentation and user-facing content remain English.
- Do not change database records, legal metadata, publication status, evidence, or researcher classifications.
- Preserve all 93 linked document endpoints and all 88 published relationships in the current export; the Corpus still contains 117 records. Derive counts from the input, not hard-coded production totals.
- Principal views must not infer shortcut edges through hidden records. Expanded views distinguish outside-group context from group membership. Arrows preserve the original semantic source and target.
- Match the approved preview's bounded canvas, group selection, principal/all modes, search, conditional inspector, focus/back, pan, zoom, Fit, 100%, full screen, and official/analytical legend.
- Run ELK at build time only, not in the browser. Do not add a graph service, analytics, React, or an image asset.
- Retain complete evidence-bearing server-rendered relationship text without JavaScript. JavaScript failure must not remove access to the text alternative.
- All internal links and static data routes must work with both `/` and `/eu-ai-policy-observatory/` base paths. No localhost or machine paths in published output.
- Dates are layout hints, not a proportional timeline. Clearly describe research-defined grouping and filtered map scope.

## Workspace and verification

Work in the existing dedicated `eu-ai-policy-observatory-isolated` checkout. Its original `.git` is stale. Use `git --git-dir=work/sdd-gitmeta --work-tree=.` for local status and commits. Base implementation is `316874b20b587952e59ea085bca169dcaf2fb6e5`. Preserve the pre-existing `web/tests/site.spec.ts` metadata-count fix, which already exists on remote main `68dad571faebfa33ae90ee35e3a218a096d44b3a`. Do not push old history. The controller handles remote integration separately using verified tree changes.

Node source baseline tests pass; local Vitest initialization is blocked by esbuild ancestor-directory access before tests execute. The controller will prepare an equivalent temporary verification checkout and run build/browser checks. Do not weaken tests or change application code to accommodate that host limitation.

### Task 1: Ship the approved map as a production Astro feature

**Files:**
- Replace `web/src/lib/policy-map.ts`: typed public graph projection, view selection and build-time layout entry points.
- Create `web/src/lib/policy-map-types.ts`: shared serializable model, geometry and atlas types; no server imports.
- Create `web/src/scripts/policy-map-client.ts`: client interaction only; no ELK import.
- Replace `web/src/components/PolicyMap.astro`: progressive enhancement shell and complete text alternative.
- Create `web/src/pages/policy-map/atlas.json.ts`: static precomputed atlas using `loadPublicData()` and `import.meta.env.BASE_URL`.
- Create `web/src/styles/policy-map.css`: scoped map styling; remove obsolete map SVG rules from `web/src/styles/global.css` without affecting other pages.
- Modify `web/package.json`, `web/pnpm-lock.yaml`: pinned build dependency `elkjs: 0.12.0`.
- Replace `web/tests/policy-map.node.test.mjs`; adapt the map-only tests in `web/tests/timeline-policy-map.source.test.mjs`, `web/tests/site.spec.ts` and `web/tests/no-js.spec.ts`; add `web/tests/policy-map.spec.ts` for new browser behaviors.
- Modify `README.md`: map usage, scope and ELK build-time dependency/license link.
- Modify `.github/workflows/validate.yml`: after website tests/build, upload `web/dist` using `actions/upload-artifact@v7`, artifact name `site-preview`, `if-no-files-found: error`, `retention-days: 7`. This read-only build artifact enables browser QA before main deployment; preserve all existing gates.

**Interfaces:**
- Consumes `PublicData` from `web/src/lib/types.ts` and `loadPublicData()` from `web/src/lib/data.ts`.
- Export `createPolicyMapModel(data: PublicData, base: string)`, `selectPolicyMapView(model, family, mode)` and `buildPolicyMapAtlas(data: PublicData, base: string)` from `policy-map.ts` with concrete return types from `policy-map-types.ts`.
- Use typed node and edge models with evidence/rationale preserved; `mode` is `'principal' | 'all'`. Model nodes include unique id, kind, title, date, record level, stage, membership IDs and base-aware href. Support document and policy endpoint types already supported by the old component; reject unresolved or unsupported endpoints explicitly instead of dropping edges silently.
- Atlas contains the shared model, two layouts per policy group and one immediate-neighborhood layout per node. Geometry can reference shared metadata by IDs to avoid duplicate payloads. The client gets the atlas URL from an Astro data attribute.

- [ ] Write and run model regression tests before implementation. Expected failure is missing production API or wrong projection/selection, not malformed fixtures. Include this real-export assertion:

```js
const data = JSON.parse(readFileSync(new URL('../../generated/public-data.json', import.meta.url), 'utf8'));
const before = JSON.stringify(data);
const model = createPolicyMapModel(data, '/eu-ai-policy-observatory/');
assert.equal(model.nodes.length, 93);
assert.equal(model.edges.length, 88);
assert.equal(JSON.stringify(data), before);
assert.ok(model.nodes.every((node) => node.href.startsWith('/eu-ai-policy-observatory/')));
```

- [ ] Add tests for principal default (AI Act group: 9 nodes, 7 recorded edges), all-group membership versus context, root and subpath hrefs, unresolved endpoints, empty public relationships, wrapping without lost words, and semantic edge direction. Construct a small explicit synthetic policy/document endpoint fixture for compatibility.
- [ ] Add atlas tests checking non-overlapping node rectangles, every routed edge starting/ending on the original source/target node bounds, complete immediate neighborhoods, and determinism. These tests exercise production output; do not assert ELK private implementation or source text.
- [ ] Implement projection and build-time ELK layout using the approved preview's algorithm. Normalize base paths with `const prefix = base.endsWith('/') ? base : base + '/'`. Position earlier/later endpoints only as geometry inputs, then restore semantic arrow direction. Preserve direct edges and data immutability.
- [ ] Render English controls and the complete relationship list through Astro. Keep `data-policy-map-relationship` and `data-policy-map-relationships` hooks for the unfiltered list. Generate endpoints from typed model data; preserve rationale, basis and evidence links. Leave the text list visible without JavaScript; hide or disable enhancement-only controls until initialization succeeds. A visible load failure message directs users to the list.
- [ ] Implement typed client SVG rendering with safe `textContent`; never interpolate corpus text as HTML. Preserve the approved default group and overview. Nodes must be keyboard operable and visibly focused, with accessible selection state. Search must work by title/year; no-match state is explicit. Focus connections must contain every recorded immediate edge even across groups; Back restores the group. A node with no edge in the current filtered view must not look like a claim of no corpus relationships.
- [ ] Match the prototype's layout and styling inside the existing site navigation and footer. Bound canvas height, reveal inspector on selection, and place inspector below canvas on narrow screens. Maintain readable default scale; Fit may zoom out by explicit user choice. Support pointer panning, keyboard arrows, zoom buttons, full screen and safe unsupported/denied full-screen feedback.
- [ ] Add browser tests before client implementation is considered complete. Include real interactions such as:

```ts
await page.goto('policy-map/');
await expect(page.getByLabel('Policy grouping')).toBeEnabled();
await expect(page.locator('[data-policy-map-node]')).toHaveCount(9);
await expect(page.locator('[data-policy-map-edge]')).toHaveCount(7);
await page.getByRole('button', { name: 'All records', exact: true }).click();
await expect(page.locator('[data-policy-map-node]')).toHaveCount(49);
await expect(page.locator('[data-policy-map-relationship]')).toHaveCount(88);
```

- [ ] Extend browser coverage for selecting AI Act then focus/back, evidence links, search/no results, zoom/Fit, keyboard selection, narrow viewport overflow, failed atlas loading and no-JavaScript relationship access. Replace old tests that assume every edge is on the default canvas, stage-column positions, or node click navigates directly. Retain equivalent accessibility, evidence and route assertions; remove obsolete implementation-shape assertions rather than preserving dead layout code.
- [ ] Pin ELK, update lockfile with pnpm, and document build-time use plus EPL-2.0 upstream notice. Run focused tests while iterating, then full Node/Vitest/Astro checks before the local commit. Do not claim browser tests passed if this host cannot launch Chromium; the controller owns browser QA and hosted CI.
- [ ] Self-review the diff against every global constraint, report test evidence and changed files, then commit only task files with message `feat: integrate focused interactive policy map`. Do not stage unrelated scratch files or the pre-existing site test fix alone; the controller verifies the final tree against remote main before publication.

## Controller release checks

- Verify data hashes unchanged, English-only policy and public-output scanner pass.
- Review the task diff, then perform broad final review after any fixes.
- Build in the temporary verification checkout, validate the exact generated artifact through the in-app browser at desktop and 390 x 844, and reset the viewport afterward.
- Verify default group -> expanded -> search -> select -> focus -> back, evidence, all-map counts, zoom/full screen, and no console errors.
- Present the production integration result for GitHub publication approval if current authorization does not clearly include publishing this change. Never force-push, merge failing CI, or describe a local build as deployed.
