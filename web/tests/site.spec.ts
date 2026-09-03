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
    await expect(page.getByRole('link', { name: title })).toBeVisible();
  }
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
    'Artificial Intelligence Act proposal',
    'AI Liability Directive proposal',
    'Artificial Intelligence for Europe',
    'Ethics Guidelines for Trustworthy AI',
    'White Paper on Artificial Intelligence',
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
  await expect(page.getByText('32024R1689')).toBeVisible();
  await expect(page.getByRole('link', { name: /Source URL:/ })).toBeVisible();
  await expect(page.getByText('Verification date')).toBeVisible();
});
