import { expect, test } from '@playwright/test';
import { loadPublicData } from '../src/lib/data';

const data = loadPublicData();

test('corpus explains missing annotations before and after filtering', async ({ page }) => {
  await page.goto('corpus/');
  const disclosure = page.getByRole('note', { name: 'Annotation coverage' });
  await expect(disclosure).toBeVisible();
  await expect(disclosure).toContainText('not evidence of absence');
  await disclosure.getByRole('link', { name: 'Annotation coverage and limits' }).click();
  const coverage = page.locator('#annotation-coverage');
  await expect(coverage).toBeVisible();
  const emptyConcepts = data.documents.filter((record) => record.concepts.length === 0).length;
  await expect(coverage.locator('dt').filter({ hasText: /^Without assigned research concepts$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText(String(emptyConcepts));
  const emptyPolicies = data.documents.filter((record) => record.policies.length === 0).length;
  await expect(coverage.locator('dt').filter({ hasText: /^Without assigned policy groupings$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText(String(emptyPolicies));
  const unlinked = data.documents.filter((record) => !data.relationships.some((relationship) =>
    (relationship.source_entity_type === 'document' && relationship.source_entity_id === record.id)
    || (relationship.target_entity_type === 'document' && relationship.target_entity_id === record.id),
  )).length;
  await expect(coverage.locator('dt').filter({ hasText: /^Without a recorded relationship endpoint$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText(String(unlinked));
  await page.goto('corpus/');
  await page.getByLabel('Search title, CELEX or ELI').fill('Artificial Intelligence Act');
  await expect(page.getByRole('note', { name: 'Annotation coverage' })).toBeVisible();
});

test('methodology distinguishes pending candidates from retained published records', async ({ page }) => {
  await page.goto('methodology/');
  const queues = page.locator('#review-queues');
  await expect(queues.getByRole('heading')).toHaveText('Separate review queues');
  await expect(queues.locator('dt').filter({ hasText: /^Unpublished candidates awaiting a decision$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText(String(data.coverage.unresolved_candidates));
  await expect(queues.locator('dt').filter({ hasText: /^Published records awaiting expanded evidence review$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText(String(data.coverage.historical_review.legacy_review_pending));
});

test('public reviewer credit does not relabel an evidence timestamp as human approval', async ({ page }) => {
  await page.goto('corpus/artificial-intelligence-act/');
  const verification = page.getByRole('region', { name: 'Verification', exact: true });
  await expect(verification.locator('dt').filter({ hasText: /^Reviewed by$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText('Yichen Hao');
  const record = data.documents.find((item) => item.id === 'artificial-intelligence-act')!;
  await expect(verification.locator('dt').filter({ hasText: /^Evidence review date$/ })
    .locator('xpath=following-sibling::dd[1]')).toHaveText(record.corpus_assessment!.reviewed_at);
  await expect(verification).toContainText('not a separate human sign-off date');
});
