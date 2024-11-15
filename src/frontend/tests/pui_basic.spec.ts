import { expect, test } from './baseFixtures.js';
import { baseUrl, user } from './defaults.js';
import { doLogin, doQuickLogin } from './login.js';

test('Basic Login Test', async ({ page }) => {
  await doLogin(page);

  // Check that the username is provided
  await page.getByText(user.username);

  await expect(page).toHaveTitle(RegExp('^InvenTree'));

  // Go to the dashboard
  await page.goto(baseUrl);
  await page.waitForURL('**/platform');

  await page.getByText('InvenTree Demo Server').waitFor();

  // Check that the username is provided
  await page.getByText(user.username);

  await expect(page).toHaveTitle(RegExp('^InvenTree'));

  // Go to the dashboard
  await page.goto(baseUrl);
  await page.waitForURL('**/platform');

  // Logout (via menu)
  await page.getByRole('button', { name: 'Ally Access' }).click();
  await page.getByRole('menuitem', { name: 'Logout' }).click();

  await page.waitForURL('**/platform/login');
  await page.getByLabel('username');
});

test('Quick Login Test', async ({ page }) => {
  await doQuickLogin(page);

  // Check that the username is provided
  await page.getByText(user.username);

  await expect(page).toHaveTitle(RegExp('^InvenTree'));

  // Go to the dashboard
  await page.goto(baseUrl);
  await page.waitForURL('**/platform');

  await page.getByText('InvenTree Demo Server').waitFor();

  // Logout (via URL)
  await page.goto(`${baseUrl}/logout/`);
  await page.waitForURL('**/platform/login');
  await page.getByLabel('username');
});
