import { expect, test } from '@playwright/test';

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
    'https://eu-ai-policy-observatory.test/eu-ai-policy-observatory/',
  );
  await expect(page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: 'Home' }))
    .toHaveAttribute('href', '/eu-ai-policy-observatory/');
});
