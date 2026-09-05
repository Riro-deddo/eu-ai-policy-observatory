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

for (const { route, heading, pdfHref } of retainedRoutes) {
  test(heading + ' renders its reviewed parent notice', async ({ page }) => {
    await page.goto(route);

    await expect(page.getByRole('heading', { level: 1, name: heading, exact: true }))
      .toHaveCount(1);
    const notice = page.getByRole('region', { name: 'Parent relationship under review' });
    await expect(notice).toBeVisible();
    await expect(notice).toContainText('This is an editorial notice, not official EU metadata.');
    await expect(notice).toContainText('Codex');
    await expect(notice).toContainText('2026-09-05T08:59:02Z');
    const evidenceLinks = notice.getByRole('link');
    await expect(evidenceLinks).toHaveCount(2);
    await expect(evidenceLinks.nth(0)).toHaveAttribute(
      'href',
      'https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems',
    );
    await expect(evidenceLinks.nth(1)).toHaveAttribute('href', pdfHref);
    await expect(notice).toContainText('Pages 1–2 (cover and first body page).');

    const officialMetadata = page.getByRole('region', { name: 'Official metadata' });
    await expect(
      officialMetadata.locator('dt').filter({ hasText: /^Version status$/ })
        .locator('xpath=following-sibling::dd[1]'),
    ).toHaveText('Draft');
    await expect.poll(() => page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    )).toBe(true);

    await page.getByRole('link', { name: 'Return to the Corpus' }).click();
    await expect(page).toHaveURL(/\/corpus\/$/);
  });
}

test('ordinary AI Act page has no retained-route notice', async ({ page }) => {
  await page.goto('corpus/artificial-intelligence-act/');
  await expect(page.getByRole('region', { name: 'Parent relationship under review' }))
    .toHaveCount(0);
});
