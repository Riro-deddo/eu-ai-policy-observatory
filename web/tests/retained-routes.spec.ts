import { expect, test } from '@playwright/test';

const retainedRoutes = [
  {
    route: 'corpus/draft-high-risk-classification-guidelines-2026/',
    heading: 'Draft high-risk classification guidelines — General principles',
    pdfHref: 'https://ec.europa.eu/newsroom/dae/redirection/document/128559',
  },
  {
    route: 'corpus/draft-high-risk-classification-guidelines-annex-i-2026/',
    heading: 'Draft Annex I high-risk classification guidelines',
    pdfHref: 'https://ec.europa.eu/newsroom/dae/redirection/document/128560',
  },
  {
    route: 'corpus/draft-high-risk-classification-guidelines-annex-iii-2026/',
    heading: 'Draft Annex III high-risk classification guidelines',
    pdfHref: 'https://ec.europa.eu/newsroom/dae/redirection/document/128561',
  },
] as const;

const parentHeading = 'Draft high-risk classification guidelines — Complete consultation work';
const parentRoute = 'corpus/draft-high-risk-classification-guidelines-consultation-work-2026/';
const libraryHref = 'https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems';

for (const { route, heading, pdfHref } of retainedRoutes) {
  test(heading + ' links to its verified whole-work parent', async ({ page }) => {
    await page.goto(route);

    await expect(page.getByRole('heading', { level: 1, name: heading, exact: true }))
      .toHaveCount(1);
    await expect(page.getByRole('region', { name: 'Parent relationship under review' }))
      .toHaveCount(0);
    await expect(page.getByRole('heading', { name: 'Expanded evidence review pending', exact: true }))
      .toHaveCount(0);
    const sources = page.getByRole('region', { name: 'Official sources and identifiers' });
    await expect(sources.locator(`a[href="${libraryHref}"]`)).toHaveCount(1);
    await expect(sources.locator(`a[href="${pdfHref}"]`)).toHaveCount(1);
    const verification = page.getByRole('region', { name: 'Verification', exact: true });
    await expect(verification.locator('dt').filter({ hasText: /^Expanded evidence review$/ })
      .locator('xpath=following-sibling::dd[1]')).toHaveText('Verified');
    await expect(verification.locator('dt').filter({ hasText: /^Reviewed by$/ })
      .locator('xpath=following-sibling::dd[1]')).toHaveText('Yichen Hao');

    const officialMetadata = page.getByRole('region', { name: 'Official metadata' });
    await expect(officialMetadata.getByText('Version status', { exact: true })).toHaveCount(0);
    const classifications = page.getByRole('region', { name: 'Research classifications' });
    await expect(
      classifications.locator('dt').filter({ hasText: /^Version status$/ })
        .locator('xpath=following-sibling::dd[1]'),
    ).toHaveText('Draft');
    await expect.poll(() => page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    )).toBe(true);

    const parent = page.getByRole('region', { name: 'Parent or principal record' });
    await expect(parent).toContainText('Part of · Official relationship · Verified');
    const parentLink = parent.getByRole('link', { name: parentHeading, exact: true });
    await expect(parentLink).toHaveAttribute('href', `/eu-ai-policy-observatory/${parentRoute}`);
    await parentLink.click();
    await expect(page).toHaveURL(new RegExp(`/${parentRoute}$`));
    await expect(page.getByRole('heading', { level: 1, name: parentHeading, exact: true }))
      .toHaveCount(1);
    // Incoming part_of links appear under Relationships; Attachments is for annex_to.
    const parts = page.getByRole('region', { name: 'Relationships', exact: true });
    for (const section of retainedRoutes) {
      await expect(parts.getByRole('link', { name: section.heading, exact: true }))
        .toHaveAttribute('href', `/eu-ai-policy-observatory/${section.route}`);
    }
    await parts.getByRole('link', { name: heading, exact: true }).click();
    await expect(page).toHaveURL(new RegExp(`/${route}$`));
    await expect(page.getByRole('heading', { level: 1, name: heading, exact: true }))
      .toHaveCount(1);

    await page.getByRole('link', { name: 'Return to the Corpus' }).click();
    await expect(page).toHaveURL(/\/corpus\/$/);
  });
}

test('ordinary AI Act page has no retained-route notice', async ({ page }) => {
  await page.goto('corpus/artificial-intelligence-act/');
  await expect(page.getByRole('region', { name: 'Parent relationship under review' }))
    .toHaveCount(0);
});
