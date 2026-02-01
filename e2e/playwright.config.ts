/**
 * Playwright E2E Test Configuration
 *
 * This configuration supports both local development and CI/CD execution.
 * Tests can be run locally with `pnpm run test:e2e` or in CI with proper browsers.
 */

import { defineConfig, devices } from '@playwright/test';

/**
 * Read environment variables from .env file for local development
 */
const baseURL = process.env.BASE_URL || 'http://localhost:3000';
const isCI = process.env.CI === 'true';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: !isCI, // Run tests in parallel locally, serially in CI
  forbidOnly: !!process.env.CI, // Fail on `only` in CI
  retries: process.env.CI ? 2 : 0, // Retry in CI, no retries locally
  workers: process.env.CI ? 1 : undefined, // Single worker in CI, parallel locally

  reporter: [
    ['html', { open: 'never' }],
    ['junit', { outputFile: 'e2e-results.xml' }],
  ],

  use: {
    baseURL,
    trace: 'on-first-retry', // Trace on first retry for debugging
    screenshot: 'only-on-failure', // Screenshot on failure
    video: 'retain-on-failure', // Video on failure
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    /* Test against mobile viewports */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120 * 1000,
  // },
});
