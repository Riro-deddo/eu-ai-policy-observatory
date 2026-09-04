import { expect, test } from '@playwright/test';

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

test('methodology states the publication boundary', async ({ page }) => {
  await page.goto('methodology/');
  await expect(page.getByText('Only published records appear in the public interface.')).toBeVisible();
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

test('research lens links hydrate the matching Corpus concept on arrival', async ({ page }) => {
  await page.goto('./');
  await page.getByRole('link', { name: 'Risk', exact: true }).click();

  expect(new URL(page.url()).search).toBe('?concept=risk');
  await expect(page.getByLabel('Concept')).toHaveValue('risk');
  await expect(page.locator('[data-corpus-list] > li:not([hidden])')).toHaveCount(6);
  await expect(page.locator('[data-corpus-count]')).toHaveText('6 published documents');
});

test('corpus search, combined classifications and reset update the rendered list', async ({ page }) => {
  await page.goto('corpus/');

  const visibleRecords = page.locator('[data-corpus-list] > li:not([hidden])');
  await expect(visibleRecords).toHaveCount(7);

  await page.getByLabel('Search title, CELEX or ELI').fill('32024R1689');
  await expect(visibleRecords).toHaveCount(1);
  await expect(visibleRecords.getByRole('link', { name: 'Artificial Intelligence Act', exact: true })).toBeVisible();

  await page.getByRole('button', { name: 'Reset filters' }).click();
  await expect(visibleRecords).toHaveCount(7);

  await page.getByLabel('Concept').selectOption('risk');
  await page.getByLabel('Institution').selectOption('european-commission');
  await expect(visibleRecords).toHaveCount(5);
  await expect(visibleRecords).toContainText([
    'AI Liability Directive proposal',
    'Artificial Intelligence Act proposal',
    'White Paper on Artificial Intelligence',
    'Ethics Guidelines for Trustworthy AI',
    'Artificial Intelligence for Europe',
  ]);
});

test('the final AI Act detail page separates official and research content', async ({ page }) => {
  await page.goto('corpus/');
  await page.getByRole('link', { name: 'Artificial Intelligence Act', exact: true }).click();

  for (const section of [
    'Official metadata',
    'Institutions and roles',
    'Official sources and identifiers',
    'Policy placement and concepts',
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
  await expect(page.getByRole('link', { name: /Source URL:/ })).toBeVisible();
  await expect(page.getByText('Verification date')).toBeVisible();
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

test('timeline presents every recorded event within the published 2018–2024 boundary', async ({ page }) => {
  await page.goto('timeline/');

  await expect(page.getByRole('heading', { level: 1 })).toContainText('Timeline');
  await expect(page.getByText('2018–2024')).toBeVisible();
  for (const event of [
    'Publication of Artificial Intelligence for Europe',
    'Publication of Coordinated Plan on Artificial Intelligence',
    'Presentation of Ethics Guidelines for Trustworthy AI',
    'Publication of White Paper on Artificial Intelligence',
    'Commission proposal for the Artificial Intelligence Act',
    'Commission proposal for the AI Liability Directive',
    'Official Journal publication of the Artificial Intelligence Act',
  ]) {
    await expect(page.getByText(event)).toBeVisible();
  }
});

test('timeline event-type filtering updates the visible chronology and announces its count', async ({ page }) => {
  await page.goto('timeline/');

  const visibleEntries = page.locator('[data-timeline-entry]:not([hidden])');
  await page.getByLabel('Event type').selectOption('proposal');

  await expect(visibleEntries).toHaveCount(2);
  await expect(visibleEntries).toContainText([
    'Commission proposal for the Artificial Intelligence Act',
    'Commission proposal for the AI Liability Directive',
  ]);
  await expect(page.locator('[data-timeline-count]')).toHaveText('2 timeline entries');
});

test('policy map states both relationship conventions and pairs every visual edge with one text entry', async ({ page }) => {
  await page.goto('policy-map/');

  const legend = page.locator('.policy-map__legend');
  await expect(legend.getByText('Official relationship', { exact: true })).toBeVisible();
  await expect(legend.getByText('Analytical relationship', { exact: true })).toBeVisible();
  const visualRelationships = page.locator('[data-policy-map-edge]');
  const relationshipSection = page.getByRole('region', { name: 'Relationship list' });
  const relationshipList = relationshipSection.locator('[data-policy-map-relationship]');
  await expect(visualRelationships).toHaveCount(3);
  await expect(relationshipList).toHaveCount(3);

  for (const relationshipId of await visualRelationships.evaluateAll((edges) => (
    edges.map((edge) => edge.getAttribute('data-policy-map-edge'))
  ))) {
    await expect(
      relationshipSection.locator(`[data-policy-map-relationship="${relationshipId}"]`),
    ).toHaveCount(1);
  }
});

test('policy map exposes a labelled interactive group with live node links', async ({ page }) => {
  await page.goto('policy-map/');

  const map = page.getByRole('group', { name: 'Published policy and document relationships' });
  await expect(map).toBeVisible();
  await expect(map.getByRole('link').first()).toHaveAttribute('href', /\/(policies|corpus)\//);
});

test('policy map nodes and stable policy pages expose live base-safe routes', async ({ page }) => {
  await page.goto('policy-map/');

  const node = page.locator('[data-policy-map-node]').first();
  await expect(node).toHaveAttribute('href', new RegExp(`${expectedBasePath}(policies|corpus)/`));
  await node.click();
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

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
