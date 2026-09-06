import { expect, test } from '@playwright/test';
import { loadPublicData } from '../src/lib/data';

const publicData = loadPublicData();
const sampleSlugs = [
  'ai-omnibus-regulation-2026-1744',
  'ai-act-council-general-approach-st-15698-2022',
  'building-a-european-data-economy',
] as const;

for (const slug of sampleSlugs) {
  const sample = publicData.documents.find((document) => document.slug === slug)!;
  test(`${sample.short_title} shows project review credit without changing verification facts`, async ({ request }) => {
    const assessment = sample.corpus_assessment;
    if (assessment === null) {
      throw new Error(`Review-credit sample lacks a corpus assessment: ${sample.slug}`);
    }
    const response = await request.get(`corpus/${sample.slug}/`);
    expect(response.ok()).toBe(true);
    const html = await response.text();

    expect(html).toContain(`<h1>${sample.short_title}</h1>`);
    expect(html).toContain('<dt>Reviewed by</dt><dd>Yichen Hao</dd>');
    expect(html).toContain(`<dt>Verification date</dt><dd>${assessment.reviewed_at}</dd>`);
    const reviewStatus = sample.historical_review_status === 'verified'
      ? 'Verified'
      : 'Expanded evidence review pending';
    expect(html).toContain(`<dt>Expanded evidence review</dt><dd>${reviewStatus}</dd>`);
  });
}
