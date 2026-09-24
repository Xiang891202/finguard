import { test, expect } from '@playwright/test'

const ADMIN_EMAIL = 'ah891202@gmail.com'
const ADMIN_PASSWORD = 'ah891202'   // ← 改成你實際建立的密碼


test('管理員可用 Email + 密碼登入', async ({ page }) => {
  await page.goto('/admin/login')
  await expect(page.locator('h1')).toContainText('FinGuard')

  // 填表
  await page.locator('input[type="email"]').fill(ADMIN_EMAIL)
  await page.locator('input[type="password"]').fill(ADMIN_PASSWORD)

  // 點登入
  await page.getByRole('button', { name: /登入/ }).click()

  // 應跳轉到 /admin/dashboard
  await expect(page).toHaveURL(/\/admin\/dashboard/, { timeout: 10_000 })
})


test('管理員錯誤密碼 → 顯示錯誤訊息', async ({ page }) => {
  await page.goto('/admin/login')

  await page.locator('input[type="email"]').fill(ADMIN_EMAIL)
  await page.locator('input[type="password"]').fill('definitely-wrong-password')

  await page.getByRole('button', { name: /登入/ }).click()

  // 紅框應顯示錯誤
  await expect(
    page.locator('text=/密碼錯誤|認證失敗|Email 或密碼|鎖定/')
  ).toBeVisible({ timeout: 10_000 })

  // URL 不變
  await expect(page).toHaveURL(/\/admin\/login/)
})


test('未登入存取 /admin/dashboard → 踢回登入', async ({ page }) => {
  await page.goto('/admin/dashboard')
  await expect(page).toHaveURL(/\/admin\/login/, { timeout: 5_000 })
})