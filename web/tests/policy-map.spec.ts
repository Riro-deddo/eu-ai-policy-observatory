import { expect, test } from '@playwright/test';

test('default group and expanded view render recorded graph scopes', async ({ page }) => {
  await page.goto('policy-map/');
  await expect(page.getByLabel('Policy grouping')).toBeEnabled();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(9);
  await expect(page.locator('[data-policy-map-edge]')).toHaveCount(7);
  await page.getByRole('button', { name: 'All records', exact: true }).click();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(49);
  await expect(page.locator('[data-policy-map-relationship]')).toHaveCount(88);
});

test('selection exposes evidence, complete focus and back navigation', async ({ page }) => {
  await page.goto('policy-map/');
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
  await page.getByLabel('Find a document').fill('White Paper');
  await page.getByRole('button', { name: /White Paper on Artificial Intelligence/ }).click();
  await expect(page.locator('[data-policy-map-node]')).toHaveCount(2);
  await expect(page.locator('[data-policy-map-edge]')).toHaveCount(2);
  await page.locator('[data-policy-map-node]').first().focus();
  await page.keyboard.press('Enter');
  await expect(page.getByLabel('Selected document')).toBeVisible();
  await page.getByRole('button', { name: 'Zoom in' }).click();
  await expect(page.getByLabel('Map zoom')).not.toHaveText('100%');
  await page.getByRole('button', { name: 'Fit' }).click();
  await page.getByLabel('Find a document').fill('not a corpus title');
  await expect(page.getByText('No matching linked documents. Try another title or year.')).toBeVisible();
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
  await expect(page.locator('[data-policy-map-relationship]')).toHaveCount(88);
});
