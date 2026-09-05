import { expect, test } from '@playwright/test';

const samples = [
  {
    slug: 'ai-omnibus-regulation-2026-1744',
    title: 'Digital Omnibus Regulation',
    status: 'Verified',
    verificationDate: '2026-09-05T18:06:34Z',
  },
  {
    slug: 'ai-act-council-general-approach-st-15698-2022',
    title: 'Council General Approach on the AI Act',
    status: 'Expanded evidence review pending',
    verificationDate: '2026-09-04T00:00:00Z',
  },
  {
    slug: 'building-a-european-data-economy',
    title: 'Building a European data economy',
    status: 'Verified',
    verificationDate: '2026-09-05T06:37:06.8601555Z',
  },
] as const;

for (const sample of samples) {
  test(`${sample.title} shows project review credit without changing verification facts`, async ({ request }) => {
    const response = await request.get(`corpus/${sample.slug}/`);
    expect(response.ok()).toBe(true);
    const html = await response.text();

    expect(html).toContain(`<h1>${sample.title}</h1>`);
    expect(html).toContain('<dt>Reviewed by</dt><dd>Yichen Hao</dd>');
    expect(html).toContain(`<dt>Verification date</dt><dd>${sample.verificationDate}</dd>`);
    expect(html).toContain(`<dt>Expanded evidence review</dt><dd>${sample.status}</dd>`);
  });
}
