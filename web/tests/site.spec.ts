import { expect, test } from '@playwright/test';
import { loadPublicData } from '../src/lib/data';

const publicData = loadPublicData();

const siteOrigin = process.env.SITE_ORIGIN ?? 'https://eu-ai-policy-observatory.test';
const basePath = process.env.BASE_PATH ?? '/eu-ai-policy-observatory';
const canonicalBase = new URL(
  `${basePath.replace(/^\/+|\/+$/g, '')}/`,
  `${siteOrigin.replace(/\/+$/, '')}/`,
);
const expectedBasePath = canonicalBase.pathname;

test('homepage exposes the six primary destinations', async ({ page }) => {
  await page.goto('./');

  const navigation = page.getByRole('navigation', { name: 'Primary' });
  await expect(navigation.getByRole('link')).toHaveCount(6);
  await expect(page.getByRole('heading', { level: 1 })).toContainText(
    'How EU AI policy is formulated, interpreted and transformed',
  );
});

test('homepage preserves the repository base path in navigation and canonical metadata', async ({ page }) => {
  await page.goto('./');

  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
    'href',
    canonicalBase.href,
  );
  await expect(page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: 'Home' }))
    .toHaveAttribute('href', expectedBasePath);
  await expect(page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: 'Policy Map' }))
    .toHaveAttribute('href', `${expectedBasePath}policy-map/`);

  await page.goto('policy-map/');
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
    'href',
    new URL('policy-map/', canonicalBase).href,
  );
});

test('home presents the four research lenses from data', async ({ page }) => {
  await page.goto('./');
  for (const concept of ['Risk', 'Trustworthiness', 'Accountability', 'Compliance']) {
    await expect(page.getByRole('link', { name: concept })).toBeVisible();
  }
});

test('public pages describe the database as research infrastructure', async ({ page }) => {
  const description = 'The database serves as research infrastructure; this atlas presents its published records. The expanding collection brings together a bounded, verified historical lineage with contemporary EU AI policy, the AI Act pathway, and related implementation records.';
  for (const route of ['./', 'about/']) {
    await page.goto(route);
    await expect(page.locator('main')).toContainText(description);
    await expect(page.locator('main')).not.toContainText('primary research output');
  }
  await page.goto('methodology/');
  await expect(page.locator('main')).toContainText('The Observatory treats the database as research infrastructure');
  await expect(page.locator('main')).not.toContainText('database as the research output');
});

test('methodology states the publication boundary', async ({ page }) => {
  await page.goto('methodology/');
  await expect(page.getByText('Only published records appear in the public interface.')).toBeVisible();
  const coverage = await page.locator('#methodology-coverage').evaluate((element) => ({
    statement: element.getAttribute('data-coverage-statement'),
    unresolved: element.getAttribute('data-unresolved-candidates'),
  }));
  if (coverage.statement === null || coverage.unresolved === null) {
    throw new Error('Methodology coverage metadata was not rendered');
  }
  await expect(page.getByText(coverage.statement, { exact: true })).toBeVisible();
  const unresolvedCount = page.locator('#methodology-coverage dt')
    .filter({ hasText: /^Unresolved candidates$/ })
    .locator('xpath=following-sibling::dd[1]');
  await expect(unresolvedCount).toBeVisible();
  await expect(unresolvedCount).toHaveText(coverage.unresolved);
});

test('methodology distinguishes incomplete registered searches from corpus completeness', async ({ page }) => {
  await page.goto('methodology/');
  const section = page.locator('#methodology-coverage');
  await expect(section).toContainText('An expanding corpus');
  await expect(section).not.toContainText('Comprehensive within');
  for (const label of [
    'Publication cutoff', 'Registered source families', 'Reviewed registered families',
    'Not started', 'In progress', 'Known gaps', 'Recheck due',
    'Included candidates', 'Merged candidates', 'Excluded candidates', 'Unresolved candidates',
  ]) {
    const row = section.locator('dt').filter({ hasText: label });
    await expect(row).toHaveCount(1);
    await expect(row.locator('xpath=following-sibling::dd[1]')).toBeVisible();
  }
  await expect(section).toContainText('Unregistered sources and unreviewed periods are not covered by these counts.');
});

test('about uses project-led authorship without university affiliation', async ({ page }) => {
  await page.goto('about/');
  await expect(page.locator('main').getByText('Created and maintained by Yichen Hao', { exact: true })).toBeVisible();
  await expect(page.getByText(/University of Edinburgh/i)).toHaveCount(0);
});

test('corpus renders every published seed document as a normal link', async ({ page }) => {
  await page.goto('corpus/');

  for (const title of [
    'Artificial Intelligence Act',
    'Artificial Intelligence Act proposal',
    'AI Liability Directive proposal',
    'Artificial Intelligence for Europe',
    'Coordinated Plan on Artificial Intelligence',
    'Ethics Guidelines for Trustworthy AI',
    'White Paper on Artificial Intelligence',
  ]) {
    await expect(page.getByRole('link', { name: title, exact: true })).toBeVisible();
  }
});

test('the original seed corpus routes remain available', async ({ page }) => {
  for (const { route, heading } of [
    { route: 'corpus/ai-act-proposal/', heading: 'Artificial Intelligence Act proposal' },
    { route: 'corpus/ai-liability-directive-proposal/', heading: 'AI Liability Directive proposal' },
    { route: 'corpus/artificial-intelligence-act/', heading: 'Artificial Intelligence Act' },
    { route: 'corpus/artificial-intelligence-for-europe/', heading: 'Artificial Intelligence for Europe' },
    { route: 'corpus/coordinated-plan-on-artificial-intelligence/', heading: 'Coordinated Plan on Artificial Intelligence' },
    { route: 'corpus/ethics-guidelines-for-trustworthy-ai/', heading: 'Ethics Guidelines for Trustworthy AI' },
    { route: 'corpus/white-paper-on-artificial-intelligence/', heading: 'White Paper on Artificial Intelligence' },
  ]) {
    await page.goto(route);
    await expect(page.getByRole('heading', { level: 1, name: heading, exact: true })).toBeVisible();
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      new URL(route, canonicalBase).href,
    );
  }
});

test('research lens links hydrate the matching Corpus concept on arrival', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('link', { name: 'Risk', exact: true }).click();

  expect(new URL(page.url()).search).toBe('?concept=risk');
  await expect(page.getByLabel('Concept')).toHaveValue('risk');
  const riskPrincipalCount = await page.locator('#corpus-documents').evaluate((element) => {
    const documents = JSON.parse(element.textContent ?? '[]') as Array<{
      concepts: Array<{ id: string }>;
      record_level: string;
    }>;
    return documents.filter((document) => document.record_level === 'principal'
      && document.concepts.some((concept) => concept.id === 'risk')).length;
  });
  await expect(page.locator('[data-corpus-list] > li:not([hidden])')).toHaveCount(riskPrincipalCount);
  await expect(page.locator('[data-corpus-count]')).toContainText(
    `${riskPrincipalCount} principal documents shown`,
  );
});

test('corpus search, combined classifications and reset update the rendered list', async ({ page }) => {
  await page.goto('corpus/');

  const visibleRecords = page.locator('[data-corpus-list] > li:not([hidden])');
  const principalCount = await page.locator('#corpus-documents').evaluate((element) => {
    const documents = JSON.parse(element.textContent ?? '[]') as Array<{ record_level: string }>;
    return documents.filter((document) => document.record_level === 'principal').length;
  });
  await expect(visibleRecords).toHaveCount(principalCount);

  await page.getByLabel('Search title, CELEX or ELI').fill('32024R1689');
  await expect(visibleRecords).toHaveCount(1);
  await expect(visibleRecords.getByRole('link', { name: 'Artificial Intelligence Act', exact: true })).toBeVisible();

  await page.getByRole('button', { name: 'Reset filters' }).click();
  await expect(visibleRecords).toHaveCount(principalCount);

  await page.getByLabel('Concept').selectOption('risk');
  await page.getByLabel('Institution').selectOption('european-commission');
  const matchingIds = await page.locator('#corpus-documents').evaluate((element) => {
    const documents = JSON.parse(element.textContent ?? '[]') as Array<{
      concepts: Array<{ id: string }>;
      id: string;
      institutions: Array<{ id: string }>;
      record_level: string;
    }>;
    return documents.filter((document) => document.record_level === 'principal'
      && document.concepts.some((concept) => concept.id === 'risk')
      && document.institutions.some((institution) => institution.id === 'european-commission'))
      .map((document) => document.id);
  });
  await expect(visibleRecords).toHaveCount(matchingIds.length);
  expect(matchingIds.length).toBeGreaterThan(0);
  for (const documentId of matchingIds) {
    await expect(page.locator(`[data-document-id="${documentId}"]`)).toBeVisible();
  }
  const visibleDates = await visibleRecords.locator('span').evaluateAll((elements) => (
    elements.map((element) => element.textContent?.match(/Publication date (\d{4}-\d{2}-\d{2})/)?.[1] ?? '')
  ));
  expect(visibleDates).toEqual(
    [...visibleDates].sort((first, second) => second.localeCompare(first, 'en-GB')),
  );
});

test('corpus sector filtering shows only matching human-readable classification tags', async ({ page }) => {
  await page.goto('corpus/');

  await page.getByLabel('Corpus view').selectOption('all');
  await page.getByLabel('Sector').selectOption('financial_services');
  const visibleRecords = page.locator('[data-corpus-list] > li:not([hidden])');
  expect(await visibleRecords.count()).toBeGreaterThan(0);
  for (const record of await visibleRecords.all()) {
    await expect(record.getByText('Financial services', { exact: true })).toBeVisible();
  }
});

test('the final AI Act detail page separates official and research content', async ({ page }) => {
  await page.goto('corpus/');
  await page.getByRole('link', { name: 'Artificial Intelligence Act', exact: true }).click();

  for (const section of [
    'Official metadata',
    'Research classifications',
    'Production provenance',
    'Official sources and identifiers',
    'Research assessment',
    'Relationships',
    'Verification',
  ]) {
    await expect(page.getByRole('heading', { name: section })).toBeVisible();
  }
  await expect(
    page
      .getByRole('region', { name: 'Official sources and identifiers' })
      .getByText('32024R1689', { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole('region', { name: 'Official sources and identifiers' })
      .getByRole('link', { name: 'Official source' }).first(),
  ).toBeVisible();
  await expect(page.getByText('Verification date')).toBeVisible();
});

test('version records expose version-aware official metadata without null placeholders', async ({ page }) => {
  await page.goto('corpus/ai-act-consolidated-2026-07-27/');

  const officialMetadata = page.getByRole('region', { name: 'Official metadata' });
  for (const value of [
    'Regulation (EU) 2024/1689',
    '2026-07-27',
    'Consolidated text, 27 July 2026',
  ]) {
    await expect(officialMetadata.getByText(value, { exact: true }).first()).toBeVisible();
  }
  await expect(officialMetadata.getByText('Document date', { exact: true })).toBeVisible();
  await expect(officialMetadata.getByText('Publication date', { exact: true })).toBeVisible();
  await expect(officialMetadata.getByText('Record level', { exact: true })).toHaveCount(0);
  await expect(officialMetadata.getByText('Version status', { exact: true })).toHaveCount(0);
  const classifications = page.getByRole('region', { name: 'Research classifications' });
  await expect(
    classifications.locator('dt').filter({ hasText: /^Record level$/ })
      .locator('xpath=following-sibling::dd[1]'),
  ).toHaveText('Version');
  await expect(
    classifications.locator('dt').filter({ hasText: /^Version status$/ })
      .locator('xpath=following-sibling::dd[1]'),
  ).toHaveText('Consolidated');
  await expect(page.getByText('null', { exact: true })).toHaveCount(0);
  await expect(page.getByText('OJ reference', { exact: true })).toHaveCount(0);
});

test('record relationships expose parent, attachment, version and procedure navigation', async ({ page }) => {
  await page.goto('corpus/ai-act-impact-assessment-swd-2021-84/');
  const parent = page.getByRole('region', { name: 'Parent or principal record' });
  await expect(parent.getByRole('link', { name: 'Artificial Intelligence Act proposal' })).toHaveAttribute(
    'href',
    `${expectedBasePath}corpus/ai-act-proposal/`,
  );
  await expect(parent.getByText('Official relationship', { exact: false })).toBeVisible();
  const attachments = page.getByRole('region', { name: 'Attachments' });
  await expect(attachments.getByRole('link', { name: 'Annexes to the AI Act proposal impact assessment' }))
    .toHaveAttribute('href', `${expectedBasePath}corpus/ai-act-impact-assessment-annexes-swd-2021-84/`);

  await page.goto('corpus/ai-act-council-third-compromise-part-one-st-12206-2022-init/');
  const versions = page.getByRole('region', { name: 'Previous and next versions' });
  await expect(versions.getByRole('link', { name: 'Second Council Presidency compromise' })).toHaveCount(0);
  const revision = versions.getByRole('link', { name: 'Third Council compromise, part one', exact: true });
  await expect(revision).toHaveAttribute(
    'href', `${expectedBasePath}corpus/ai-act-council-third-compromise-part-one-st-12206-2022-rev-1/`,
  );
  await revision.click();
  await expect(page).toHaveURL(/\/corpus\/ai-act-council-third-compromise-part-one-st-12206-2022-rev-1\/$/);
  const revisedVersions = page.getByRole('region', { name: 'Previous and next versions' });
  await expect(revisedVersions.getByRole('link', { name: 'Second Council Presidency compromise' })).toHaveAttribute(
    'href', `${expectedBasePath}corpus/ai-act-council-second-compromise-st-11124-2022/`,
  );
  await expect(revisedVersions.getByRole('link', { name: 'Third Council compromise, part one — initial version' })).toHaveAttribute(
    'href', `${expectedBasePath}corpus/ai-act-council-third-compromise-part-one-st-12206-2022-init/`,
  );

  await page.goto('corpus/ai-act-proposal/');
  const procedure = page.getByRole('region', { name: 'Formal procedure' });
  await expect(procedure.getByText('2021/0106(COD)', { exact: true })).toBeVisible();
});

test('document records prioritise a readable short title while retaining the official title', async ({ page }) => {
  await page.goto('corpus/artificial-intelligence-for-europe/');

  const recordTitle = page.getByRole('heading', {
    level: 1,
    name: 'Artificial Intelligence for Europe',
    exact: true,
  });
  await expect(recordTitle).toBeVisible();

  const officialMetadata = page.getByRole('region', { name: 'Official metadata' });
  await expect(officialMetadata.getByText('Official title', { exact: true })).toBeVisible();
  await expect(officialMetadata.getByText(
    'COMMUNICATION FROM THE COMMISSION TO THE EUROPEAN PARLIAMENT, THE EUROPEAN COUNCIL, THE COUNCIL, THE EUROPEAN ECONOMIC AND SOCIAL COMMITTEE AND THE COMMITTEE OF THE REGIONS Artificial Intelligence for Europe',
    { exact: true },
  )).toBeVisible();

  const titleSize = Number.parseFloat(await recordTitle.evaluate((element) => (
    window.getComputedStyle(element).fontSize
  )));
  const maximumTitleSize = page.viewportSize()!.width <= 390 ? 48 : 72;
  expect(titleSize).toBeLessThanOrEqual(maximumTitleSize);
});

test('timeline separates document dates from distinct policy events across the published boundary', async ({ page }) => {
  await page.goto('timeline/');

  await expect(page.getByRole('heading', { level: 1 })).toContainText('Timeline');
  await expect(page.getByText('1984–2026')).toBeVisible();
  await expect(page.getByRole('heading', { level: 2, name: '1984' })).toBeVisible();
  for (const document of [
    'Artificial Intelligence for Europe',
    'Coordinated Plan on Artificial Intelligence',
    'Ethics Guidelines for Trustworthy AI',
    'White Paper on Artificial Intelligence',
  ]) {
    await expect(page.getByRole('heading', { level: 3, name: document, exact: true })).toBeVisible();
  }
  for (const event of [
    'Commission proposal for the Artificial Intelligence Act',
    'Commission proposal for the AI Liability Directive',
    'Artificial Intelligence Act signed',
    'Official Journal publication of the Artificial Intelligence Act',
    'Artificial Intelligence Act enters into force',
    'AI Act general application date',
  ]) {
    await expect(page.getByText(event)).toBeVisible();
  }
  await expect(page.getByText('Publication of Artificial Intelligence for Europe', { exact: true })).toHaveCount(0);
});

test('timeline event-type filtering updates the visible chronology and announces its count', async ({ page }) => {
  await page.goto('timeline/');

  const visibleEntries = page.locator('[data-timeline-entry]:not([hidden])');
  await page.getByLabel('Event type').selectOption('proposal');

  await expect(visibleEntries).toHaveCount(3);
  await expect(visibleEntries).toContainText([
    'Commission proposal for the Artificial Intelligence Act',
    'Commission proposal for the AI Liability Directive',
    'Commission proposes Digital Omnibus amendments to the AI Act',
  ]);
  await expect(page.locator('[data-timeline-count]')).toHaveText('3 timeline entries');
});

test('timeline all-records view never reduces the visible chronology', async ({ page }) => {
  await page.goto('timeline/');

  const visibleEntries = page.locator('[data-timeline-entry]:not([hidden])');
  const principalCount = await visibleEntries.count();
  await page.getByRole('radio', { name: 'All documents and versions' }).check();
  const allCount = await visibleEntries.count();

  expect(allCount).toBeGreaterThanOrEqual(principalCount);
});

test('stable policy pages expose live base-safe routes', async ({ page }) => {
  await page.goto('policies/european-ai-policy-pathway/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('European Union artificial intelligence policy pathway');
  await expect(page.getByRole('heading', { name: 'Research-defined policy grouping' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Research assessment relationships' })).toBeVisible();
});

test('every generated route has one main heading, one main landmark, a working skip link and no console errors', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  const assertRouteAccessibility = async (path: string) => {
    await page.goto(path);
    await expect(page.locator('main')).toHaveCount(1);
    await expect(page.locator('h1:visible')).toHaveCount(1);
    const skipLink = page.getByRole('link', { name: 'Skip to main content' });
    await skipLink.focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
  };

  for (const route of ['./', 'policy-map/', 'timeline/', 'corpus/', 'methodology/', 'about/']) {
    await assertRouteAccessibility(route);
  }

  await page.goto('corpus/');
  const documentRoutes = await page.locator('[data-corpus-list] a').evaluateAll((links) => (
    links.map((link) => link.getAttribute('href')).filter((href): href is string => href !== null)
  ));
  for (const route of documentRoutes) await assertRouteAccessibility(route);

  await page.goto('timeline/');
  const policyRoutes = [...new Set(await page.locator('[data-timeline-entry] a[href*="/policies/"]').evaluateAll((links) => (
    links.map((link) => link.getAttribute('href')).filter((href): href is string => href !== null)
  )))];
  expect(policyRoutes.length).toBeGreaterThan(0);
  for (const route of policyRoutes) await assertRouteAccessibility(route);

  expect(consoleErrors).toEqual([]);
});

test('mobile routes do not make the document body horizontally overflow', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 844 });
  await page.goto('corpus/');
  const documentRoutes = await page.locator('[data-corpus-list] a').evaluateAll((links) => (
    links.map((link) => link.getAttribute('href')).filter((href): href is string => href !== null)
  ));

  await page.goto('timeline/');
  const policyRoutes = [...new Set(await page.locator('[data-timeline-entry] a[href*="/policies/"]').evaluateAll((links) => (
    links.map((link) => link.getAttribute('href')).filter((href): href is string => href !== null)
  )))];
  expect(policyRoutes.length).toBeGreaterThan(0);
  const routes = [
    './',
    'policy-map/',
    'timeline/',
    'corpus/',
    'methodology/',
    'about/',
    ...documentRoutes,
    ...policyRoutes,
  ];

  for (const route of routes) {
    await page.goto(route);
    await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  }
});

test('corpus filters historical classifications independently from pending legacy review', async ({ page }) => {
  await page.goto('corpus/');
  const documents = await page.locator('#corpus-documents').evaluate((element) => JSON.parse(
    element.textContent ?? '[]',
  ) as Array<{
    historical_review_status: string;
    id: string;
    record_level: string;
    relevance_class: string | null;
    temporal_collection: string | null;
  }>);
  const principalDocuments = documents.filter((document) => document.record_level === 'principal');
  const pendingPrincipal = principalDocuments.filter(
    (document) => document.historical_review_status === 'legacy_review_pending',
  );
  const directHistorical = principalDocuments.filter((document) => (
    document.temporal_collection === 'historical_lineage'
      && document.relevance_class === 'direct_ai_substantive'
  ));
  const visibleRecords = page.locator('[data-corpus-list] > li:not([hidden])');

  await expect(visibleRecords).toHaveCount(principalDocuments.length);
  await expect(page.locator('[data-corpus-count]')).toHaveText(
    `${principalDocuments.length} principal documents shown · ${pendingPrincipal.length}/${principalDocuments.length} shown records pending expanded evidence review`,
  );
  await page.getByLabel('Collection').selectOption('historical_lineage');
  await page.getByLabel('Relevance').selectOption('direct_ai_substantive');
  await expect(visibleRecords).toHaveCount(directHistorical.length);
  for (const document of directHistorical) {
    await expect(page.locator(`[data-document-id="${document.id}"]`)).toBeVisible();
  }

  await page.getByRole('button', { name: 'Reset filters' }).click();
  await expect(visibleRecords).toHaveCount(principalDocuments.length);
  await page.getByLabel('Relevance').selectOption('legacy_review_pending');
  await expect(visibleRecords).toHaveCount(pendingPrincipal.length);
  await expect(page.locator('[data-corpus-count]')).toHaveText(
    `${pendingPrincipal.length} principal documents shown · ${pendingPrincipal.length}/${pendingPrincipal.length} shown records pending expanded evidence review`,
  );
});

test('historical record pages render official date evidence and research classification evidence', async ({ page }) => {
  await page.goto('corpus/building-a-european-data-economy/');

  await expect(page.getByRole('heading', { level: 1, name: 'Building a European data economy' })).toBeVisible();
  const officialMetadata = page.getByRole('region', { name: 'Official metadata' });
  await expect(officialMetadata.getByText('Document date kind', { exact: true })).toBeVisible();
  await expect(officialMetadata.getByText('Publication-date evidence', { exact: true })).toBeVisible();
  await expect(officialMetadata.getByText('Record level', { exact: true })).toHaveCount(0);
  await expect(officialMetadata.getByText('Version status', { exact: true })).toHaveCount(0);
  const classifications = page.getByRole('region', { name: 'Research classifications' });
  await expect(
    classifications.locator('dt').filter({ hasText: /^Record level$/ })
      .locator('xpath=following-sibling::dd[1]'),
  ).toHaveText('Principal');
  await expect(
    classifications.locator('dt').filter({ hasText: /^Version status$/ })
      .locator('xpath=following-sibling::dd[1]'),
  ).toHaveText('Final');
  await expect(classifications.getByText('Historical lineage', { exact: true })).toBeVisible();
  await expect(classifications.getByText('AI-related precursor', { exact: true })).toBeVisible();
  await expect(classifications.getByRole('heading', { name: 'Classification evidence' })).toBeVisible();
});

test('pending legacy records show a separate expanded-review notice without inferred classes', async ({ page }) => {
  const pending = publicData.documents.find(
    (document) => document.historical_review_status === 'legacy_review_pending'
      && document.publication_status === 'published'
      && document.record_level === 'principal'
      && document.version_status === 'final',
  )!;
  await page.goto(`corpus/${pending.slug}/`);

  if (pending.review_qualification) {
    const notice = page.locator('aside[aria-labelledby="qualified-evidence-review"]');
    await expect(notice).toBeVisible();
    await expect(notice).toContainText(pending.review_qualification.confirmed);
    await expect(notice).toContainText(pending.review_qualification.unresolved);
    await expect(notice).toContainText('not a completed expanded verification');
  } else {
    const notice = page.getByRole('complementary', { name: 'Expanded evidence review pending' });
    await expect(notice).toBeVisible();
    await expect(notice).toContainText('no temporal collection or relevance class is inferred');
  }
  await expect(page.getByRole('region', { name: 'Verification', exact: true }))
    .toContainText('Expanded evidence review pending');
  const classifications = page.getByRole('region', { name: 'Research classifications' });
  await expect(
    classifications.locator('dt').filter({ hasText: /^Record level$/ })
      .locator('xpath=following-sibling::dd[1]'),
  ).toHaveText('Principal');
  await expect(
    classifications.locator('dt').filter({ hasText: /^Version status$/ })
      .locator('xpath=following-sibling::dd[1]'),
  ).toHaveText('Final');
  await expect(classifications.getByText('Expanded evidence review pending', { exact: true })).toHaveCount(2);
  await expect(classifications.getByText('Historical lineage', { exact: true })).toHaveCount(0);
  await expect(classifications.getByText('Direct AI relevance', { exact: true })).toHaveCount(0);
});

test('methodology renders bounded source scopes and incomplete review semantics', async ({ page }) => {
  await page.goto('methodology/');

  const review = page.getByRole('region', { name: 'Expanded evidence review' });
  await expect(review).toContainText(`${publicData.coverage.historical_review.verified} published records`);
  await expect(review).toContainText(`${publicData.coverage.historical_review.legacy_review_pending} retained records`);
  const scopes = page.getByRole('region', { name: 'Bounded source scopes' });
  await expect(scopes.locator(':scope > ol > li')).toHaveCount(publicData.coverage.source_scopes.length);
  await expect(scopes).toContainText('Partial · in progress');
  await expect(scopes).toContainText('Unspecified');
  await expect(scopes).toContainText('2026-09-04');
  await expect(scopes).toContainText('zero pending count');
  await expect(page.getByRole('region', { name: 'Database seed and analytical samples' }))
    .toContainText('not the frozen all-route baseline');
});
