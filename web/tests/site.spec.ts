import { expect, test } from '@playwright/test';

test('homepage exposes the six primary destinations', async ({ page }) => {
  await page.goto('./');

  const navigation = page.getByRole('navigation', { name: 'Primary' });
  await expect(navigation.getByRole('link')).toHaveCount(6);
  await expect(page.getByRole('heading', { level: 1 })).toContainText(
    'How EU AI policy is formulated, interpreted and transformed',
  );
});
