import { expect, test } from '@playwright/test';

test('unknown publication is explicit and excluded from publication-year filtering', async ({ page }) => {
  await page.goto('./corpus/?view=all');
  const record = page.locator('[data-document-id="standardisation-request-c-2025-3871"]');
  await expect(record).toContainText('Publication date not yet confirmed');
  await expect(record).toContainText('Official final text and adoption');
  await page.getByLabel('Publication year', { exact: true }).selectOption('2025');
  await expect(record).toBeHidden();
  await page.getByLabel('Publication year', { exact: true }).selectOption('');
  await expect(record).toBeVisible();
  await record.getByRole('link').click();
  const metadata = page.locator('section[aria-labelledby="official-metadata"]');
  await expect(metadata.locator('dt').filter({ hasText: /^Publication date$/ }).locator('+ dd')).toHaveText('Publication date not yet confirmed');
  await expect(metadata).toContainText('2025-06-23');
  await expect(page.locator('section[aria-labelledby="verification"]')).toContainText('Publication date not yet confirmed');
});

for (const slug of ['gpai-training-content-explanatory-notice-2025', 'gpai-training-content-template-2025']) {
  test(`${slug} separates confirmed text from the parent gap`, async ({ page }) => {
    await page.goto(`./corpus/${slug}/`);
    await expect(page.getByRole('heading', { name: 'Original text and publication confirmed; parent evidence pending', exact: true })).toBeVisible();
    await expect(page.locator('aside[aria-labelledby="qualified-evidence-review"]')).toContainText('MAIN');
  });
}

test('Council version conflict is retained as a conflict', async ({ page }) => {
  await page.goto('./corpus/ai-act-council-third-compromise-part-one-st-12206-2022-init/');
  await expect(page.getByRole('heading', { name: 'Official version information conflicts', exact: true })).toBeVisible();
  await expect(page.locator('aside[aria-labelledby="qualified-evidence-review"]')).toContainText('7 September');
});
