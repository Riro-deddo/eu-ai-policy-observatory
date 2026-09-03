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
  await expect(page.locator('[data-timeline-entry]')).not.toHaveCount(0);
  await expect(page.locator('[data-timeline-entry][hidden]')).toHaveCount(0);

  await page.goto('policy-map/');
  await expect(page.locator('[data-policy-map-relationship]')).not.toHaveCount(0);
  await expect(page.locator('[data-policy-map-relationship][hidden]')).toHaveCount(0);

  const policyRoutes = await page.locator('[data-policy-map-node]').evaluateAll((nodes) => (
    nodes.map((node) => node.getAttribute('href'))
      .filter((href): href is string => href?.includes('/policies/') ?? false)
  ));
  expect(policyRoutes.length).toBeGreaterThan(0);
  for (const route of policyRoutes) {
    await page.goto(route);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  }
});
