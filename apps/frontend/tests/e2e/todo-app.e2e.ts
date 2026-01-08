import { test, expect } from '@playwright/test';

test.describe('Todo App End-to-End Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Assuming the app is running on localhost:3000
    await page.goto('http://localhost:3000');
  });

  test('User registration and task management workflow', async ({ page }) => {
    // Navigate to registration page
    await page.getByRole('link', { name: 'Sign Up' }).click();

    // Fill in registration form
    await page.locator('input[name="email"]').fill('testuser@example.com');
    await page.locator('input[name="first_name"]').fill('Test');
    await page.locator('input[name="last_name"]').fill('User');
    await page.locator('input[name="password"]').fill('SecurePassword123!');
    await page.locator('input[name="confirm_password"]').fill('SecurePassword123!');

    // Submit registration
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // Verify successful registration and redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText('Welcome, Test!')).toBeVisible();

    // Create a new task
    await page.locator('input[placeholder="Add a new task..."]').fill('My first task');
    await page.getByRole('button', { name: 'Add Task' }).click();

    // Verify task appears in the list
    await expect(page.getByText('My first task')).toBeVisible();

    // Edit the task
    await page.getByRole('button', { name: 'Edit' }).first().click();
    await page.locator('input[placeholder="Task title"]').fill('Updated task title');
    await page.getByRole('button', { name: 'Save' }).click();

    // Verify task was updated
    await expect(page.getByText('Updated task title')).toBeVisible();

    // Mark task as completed
    const taskCheckbox = page.locator('input[type="checkbox"]').first();
    await taskCheckbox.click();

    // Verify task is marked as completed
    await expect(page.locator('p:has-text("Updated task title")').first()).toHaveClass(/line-through/);

    // Delete the task
    await page.getByRole('button', { name: 'Del' }).first().click();

    // Verify task is removed
    await expect(page.getByText('Updated task title')).not.toBeVisible();
  });

  test('User login and authentication workflow', async ({ page }) => {
    // Navigate to login page
    await page.getByRole('link', { name: 'Sign In' }).click();

    // Fill in login form
    await page.locator('input[name="email"]').fill('testuser@example.com');
    await page.locator('input[name="password"]').fill('SecurePassword123!');

    // Submit login
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Verify successful login and redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByText('Welcome')).toBeVisible();

    // Verify that protected routes are accessible
    await page.getByRole('link', { name: 'Profile' }).click();
    await expect(page).toHaveURL(/.*profile/);

    // Log out
    await page.getByRole('button', { name: 'Logout' }).click();

    // Verify redirect to home page after logout
    await expect(page).toHaveURL(/^http:\/\/localhost:3000\/?$/);
  });

  test('Task filtering and search functionality', async ({ page }) => {
    // Assuming user is already logged in
    await page.goto('http://localhost:3000/dashboard');

    // Create multiple tasks
    const tasks = [
      { title: 'High priority task', priority: 'high' },
      { title: 'Medium priority task', priority: 'medium' },
      { title: 'Low priority task', priority: 'low' },
      { title: 'Completed task', priority: 'medium' }
    ];

    for (const task of tasks) {
      await page.locator('input[placeholder="Add a new task..."]').fill(task.title);
      await page.getByRole('button', { name: 'Add Task' }).click();
    }

    // Mark one task as completed
    const completedTaskCheckbox = page.locator('input[type="checkbox"]').nth(3);
    await completedTaskCheckbox.click();

    // Test filtering by completion status
    await page.getByRole('button', { name: 'Filter' }).click();
    await page.getByText('Show Completed').click();

    // Verify only completed tasks are shown
    await expect(page.getByText('Completed task')).toBeVisible();
    await expect(page.getByText('High priority task')).not.toBeVisible();

    // Test filtering by priority
    await page.getByRole('button', { name: 'Filter' }).click();
    await page.getByText('High Priority').click();

    // Verify only high priority tasks are shown
    await expect(page.getByText('High priority task')).toBeVisible();
  });
});