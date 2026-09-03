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
