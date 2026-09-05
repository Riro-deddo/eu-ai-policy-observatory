import { expect, test } from '@playwright/test';

test('default group and expanded view render recorded graph scopes', async ({ page }) => {
  await page.goto('policy-map/');
  await expect(page.getByLabel('Policy grouping')).toBeEnabled();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(9);
  await expect(page.locator('[data-policy-map-edge]')).toHaveCount(7);
  await page.getByRole('button', { name: 'All records', exact: true }).click();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(49);
  await expect(page.locator('[data-policy-map-relationship]')).toHaveCount(96);
});

test('selection exposes evidence, complete focus and back navigation', async ({ page }) => {
  await page.goto('policy-map/');
  await page.getByRole('button', { name: 'Fit', exact: true }).click();
  await page.locator('[data-policy-map-node="document:artificial-intelligence-act"]').click();
  await expect(page.getByLabel('Selected document')).toBeVisible();
  await expect(page.getByLabel('Selected document').getByRole('link')).not.toHaveCount(0);
  await page.getByRole('button', { name: 'Focus connections' }).click();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(12);
  await expect(page.locator('[data-policy-map-edge]')).toHaveCount(11);
  await page.getByRole('button', { name: 'Back to group' }).click();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(9);
});

test('search, keyboard selection and map controls are operable', async ({ page }) => {
  await page.goto('policy-map/');
  await page.getByLabel('Find a record').fill('White Paper');
  await page.locator('[data-policy-map-search-results]')
    .getByRole('button', { name: /White Paper on Artificial Intelligence/ })
    .click();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(2);
  await expect(page.locator('[data-policy-map-edge]')).toHaveCount(2);
  await page.locator('[data-policy-map-node="document:white-paper-on-artificial-intelligence"]').focus();
  await page.keyboard.press('Enter');
  await expect(page.getByLabel('Selected document')).toBeVisible();
  await page.getByRole('button', { name: 'Zoom in' }).click();
  await expect(page.getByLabel('Map zoom')).not.toHaveText('100%');
  await page.getByRole('button', { name: 'Fit' }).click();
  await page.getByLabel('Find a record').fill('not a corpus title');
  await expect(page.getByText('No matching linked records. Try another title or year.')).toBeVisible();
});

test('initial camera fit measures the visible canvas', async ({ page }) => {
  await page.goto('policy-map/');
  await expect(page.getByLabel('Policy grouping')).toBeVisible();
  const camera = await page.evaluate(async () => {
    const root = document.querySelector<HTMLElement>('[data-policy-map-root]');
    const viewport = document.querySelector<HTMLElement>('[data-policy-map-viewport]');
    const scene = document.querySelector<SVGGElement>('[data-policy-map-scene]');
    if (!root?.dataset.atlasUrl || !viewport || !scene) throw new Error('Policy Map did not initialise');
    const atlas = await fetch(root.dataset.atlasUrl).then((response) => response.json()) as {
      views: Record<string, { width: number; height: number }>;
    };
    const graph = atlas.views['artificial-intelligence-act-legislative-process:principal'];
    const matrix = scene.transform.baseVal.consolidate()?.matrix;
    if (!graph || !matrix) throw new Error('Policy Map camera is unavailable');
    const viewportBox = viewport.getBoundingClientRect();
    const expectedScale = Math.max(
      .85,
      Math.min(1, (viewportBox.width - 30) / graph.width, (viewportBox.height - 30) / graph.height),
    );
    return {
      actual: { x: matrix.e, y: matrix.f, scaleX: matrix.a, scaleY: matrix.d },
      expected: {
        x: Math.max(12, (viewportBox.width - graph.width * expectedScale) / 2),
        y: Math.max(12, (viewportBox.height - graph.height * expectedScale) / 2),
        scale: expectedScale,
      },
    };
  });
  expect(Number.isFinite(camera.actual.x)).toBe(true);
  expect(Number.isFinite(camera.actual.y)).toBe(true);
  expect(camera.actual.scaleX).toBeGreaterThan(0);
  expect(camera.actual.scaleY).toBeGreaterThan(0);
  expect(camera.actual.scaleX).toBeCloseTo(camera.expected.scale, 5);
  expect(camera.actual.scaleY).toBeCloseTo(camera.expected.scale, 5);
  expect(camera.actual.x).toBeCloseTo(camera.expected.x, 4);
  expect(camera.actual.y).toBeCloseTo(camera.expected.y, 4);
  await expect(page.getByLabel('Map zoom')).not.toHaveText('0%');
});

test('narrow map stays inside the document viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('policy-map/');
  await expect.poll(() => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await expect(page.getByLabel('Selected document')).toBeHidden();
});

test('atlas failure leaves the relationship alternative available', async ({ page }) => {
  await page.route('**/policy-map/atlas.json', (route) => route.fulfill({ json: { model: { nodes: [], edges: [], policies: [] }, views: {}, neighborhoods: {} } }));
  await page.goto('policy-map/');
  await expect(page.getByText('The interactive map could not load.')).toBeVisible();
  await expect(page.getByLabel('Policy grouping')).toBeHidden();
  await expect(page.locator('[data-policy-map-relationship]')).toHaveCount(96);
});

test('no JavaScript hides enhancement UI and preserves the complete relationship list', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto('policy-map/');
  await expect(page.getByLabel('Policy grouping')).toBeHidden();
  await expect(page.getByLabel('Interactive policy relationship map')).toBeHidden();
  await expect(page.locator('[data-policy-map-relationship]')).toHaveCount(96);
  await context.close();
});
