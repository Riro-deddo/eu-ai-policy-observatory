import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const workflow = readFileSync(new URL('../../.github/workflows/validate.yml', import.meta.url), 'utf8');
const playwrightConfig = readFileSync(new URL('../playwright.config.ts', import.meta.url), 'utf8');
const packageJson = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'));

test('validation runs the complete configured Playwright project set once', () => {
  const e2eCommands = workflow.match(/^\s+pnpm test:e2e[^\r\n]*$/gm) ?? [];

  assert.deepEqual(e2eCommands.map((command) => command.trim()), ['pnpm test:e2e']);
  assert.doesNotMatch(workflow, /pnpm test:e2e\s+--\s+--project=/);
  assert.match(playwrightConfig, /name: 'chromium-desktop'/);
  assert.match(playwrightConfig, /name: 'chromium-mobile'/);
  assert.match(packageJson.scripts.test, /node --test "tests\/\*\.test\.mjs"/);
  assert.match(packageJson.scripts.test, /vitest run/);
});
