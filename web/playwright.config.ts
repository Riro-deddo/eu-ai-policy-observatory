import { defineConfig, devices } from '@playwright/test';

const baseURL = 'http://127.0.0.1:4321/eu-ai-policy-observatory/';

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
  use: { baseURL },
  webServer: {
    command: 'pnpm build && pnpm preview --host 127.0.0.1',
    env: { ASTRO_TELEMETRY_DISABLED: '1' },
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
