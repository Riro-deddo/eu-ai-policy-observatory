import { defineConfig } from 'astro/config';

const site = process.env.SITE_ORIGIN ?? 'https://eu-ai-policy-observatory.test';
const base = process.env.BASE_PATH ?? '/eu-ai-policy-observatory';

export default defineConfig({ output: 'static', site, base, trailingSlash: 'always' });
