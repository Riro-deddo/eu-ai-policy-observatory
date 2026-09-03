import { defineConfig, devices } from '@playwright/test';

const siteOrigin = process.env.SITE_ORIGIN ?? 'https://eu-ai-policy-observatory.test';
const basePath = process.env.BASE_PATH ?? '/eu-ai-policy-observatory';
const normalizedBasePath = `/${basePath.replace(/^\/+|\/+$/g, '')}/`;
const baseURL = `http://127.0.0.1:4321${normalizedBasePath}`;

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
  use: { baseURL },
  webServer: {
    command: 'pnpm build && pnpm preview --host 127.0.0.1',
    env: {
      ASTRO_TELEMETRY_DISABLED: '1',
      BASE_PATH: basePath,
      SITE_ORIGIN: siteOrigin,
    },
    url: baseURL,
    reuseExistingServer: false,
  },
  projects: [
    { name: 'chromium-desktop', use: { ...devices['Desktop Chrome'] } },
    {
      name: 'chromium-mobile',
      use: { ...devices['Desktop Chrome'], viewport: { width: 390, height: 844 } },
    },
  ],
});
