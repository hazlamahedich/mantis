/**
 * Sample E2E test for the home page
 *
 * This test demonstrates basic Playwright usage.
 * Add more E2E tests as the application grows.
 */

import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load the home page', async ({ page }) => {
    // Navigate to the home page
    await page.goto('/');

    // Check that the page loaded successfully
    await expect(page).toHaveTitle(/Mantis/);
  });

  test('should have accessible navigation', async ({ page }) => {
    await page.goto('/');

    // Check for navigation elements (adjust selectors as needed)
    const navigation = page.locator('nav, header nav, [role="navigation"]');
    await expect(navigation).toBeVisible();
  });
});

/**
 * Tips for writing E2E tests:
 *
 * 1. Use Page Object Model for complex pages
 * 2. Use data-testid attributes for stable selectors
 * 3. Test user flows, not implementation details
 * 4. Keep tests independent and reproducible
 * 5. Use fixtures in e2e/fixtures/ for test data
 *
 * Example with fixtures:
 * ```typescript
 * import { test } from '@playwright/test';
 * import { loginAsUser } from './fixtures/auth';
 *
 * test('authenticated user can access dashboard', async ({ page }) => {
 *   await loginAsUser(page, 'test@example.com', 'password123');
 *   await page.goto('/dashboard');
 *   await expect(page).toHaveURL(/.*dashboard/);
 * });
 * ```
 */
