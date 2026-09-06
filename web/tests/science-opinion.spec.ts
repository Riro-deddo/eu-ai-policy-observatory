import { expect, test } from '@playwright/test';

test('preserved originals are supplementary, while the corrected opinion links back to its first edition', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(error.message));
  await page.goto('corpus/chief-scientific-advisors-ai-science-opinion-2024-first-edition/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('AI');
  const official = page.getByRole('region', { name: 'Official sources and identifiers' });
  await expect(official.getByRole('link', { name: 'Official source', exact: true })).toHaveCount(1);
  const supplement = page.getByRole('region', { name: 'Supplementary preserved originals' });
  await expect(supplement).toContainText('not official EU hosts');
  await expect(supplement.getByRole('link')).toHaveCount(2);
  await expect(supplement.getByRole('link', { name: /ALLEA/ })).toHaveAttribute('href', /^https:\/\/allea\.org\//);
  await expect(supplement.getByRole('link', { name: /KNAW/ })).toHaveAttribute('href', /^https:\/\/storage\.knaw\.nl\//);
  await page.getByRole('region', { name: 'Previous and next versions' }).getByRole('link').click();
  await expect(page).toHaveURL(/\/corpus\/chief-scientific-advisors-ai-science-opinion-2024\/$/);
  await expect(page.getByRole('region', { name: 'Supplementary preserved originals' })).toHaveCount(0);
  await expect(page.getByRole('region', { name: 'Official sources and identifiers' }).getByRole('link', { name: 'Official source', exact: true })).toHaveCount(3);
  await page.getByRole('region', { name: 'Previous and next versions' }).getByRole('link').click();
  await expect(page).toHaveURL(/\/corpus\/chief-scientific-advisors-ai-science-opinion-2024-first-edition\/$/);
  expect(errors).toEqual([]);
});
