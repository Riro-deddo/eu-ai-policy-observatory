import { expect, test } from '@playwright/test';

test.use({ javaScriptEnabled: false });

test('core atlas content remains readable without JavaScript', async ({ page }) => {
  await page.goto('./');
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

  await page.goto('corpus/');
  const documentRoutes = await page.locator('[data-corpus-list] a').evaluateAll((links) => (
    links.map((link) => link.getAttribute('href')).filter((href): href is string => href !== null)
  ));
  expect(documentRoutes.length).toBeGreaterThan(0);
  for (const route of documentRoutes) {
    await page.goto(route);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  }

  await page.goto('timeline/');
  const serializedEntries = await page.locator('#timeline-entries').textContent();
  if (serializedEntries === null) throw new Error('Timeline public data was not rendered');
  const timelineEntries = JSON.parse(serializedEntries) as Array<{ id: string }>;
  expect(timelineEntries.length).toBeGreaterThan(0);
  await expect(page.locator('[data-timeline-entry]')).toHaveCount(timelineEntries.length);
  await expect(page.locator('[data-timeline-entry][hidden]')).toHaveCount(0);

  await page.goto('policy-map/');
  await expect(page.locator('[data-policy-map-relationship]')).not.toHaveCount(0);
  await expect(page.locator('[data-policy-map-relationship][hidden]')).toHaveCount(0);

  await page.goto('timeline/');
  const policyRoutes = [...new Set(await page.locator('[data-timeline-entry] a[href*="/policies/"]').evaluateAll((links) => (
    links.map((link) => link.getAttribute('href')).filter((href): href is string => href !== null)
  )))];
  expect(policyRoutes.length).toBeGreaterThan(0);
  for (const route of policyRoutes) {
    await page.goto(route);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  }
});
