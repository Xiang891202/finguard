import { test, expect } from '@playwright/test'

function uniqueEmail() {
  return `e2e-${Date.now()}-${Math.floor(Math.random() * 1000)}@example.com`
}

test('用戶可用 Email + OTP 登入', async ({ page }) => {
  const email = uniqueEmail()

  await page.goto('/login')
  await expect(page.locator('h1')).toContainText('FinGuard')

  // 輸入 email
  await page.getByPlaceholder('you@example.com').fill(email)

  // 等按鈕啟用（computed emailValid 生效）
  const sendBtn = page.getByRole('button', { name: /發送驗證碼/ })
  await expect(sendBtn).toBeEnabled({ timeout: 5_000 })
  await sendBtn.click()

  // 等黃框出現
  const devBox = page.locator('text=/開發模式驗證碼/')
  await expect(devBox).toBeVisible({ timeout: 15_000 })

  const code = (await devBox.textContent()).match(/(\d{6})/)[1]
  expect(code).toHaveLength(6)

  // 輸入 OTP
  await page.getByPlaceholder('000000').fill(code)
  await page.getByRole('button', { name: /^登入/ }).click()

  // 跳轉到健康檔案
  await expect(page).toHaveURL(/\/app\/account\/health/, { timeout: 10_000 })

  // 驗證完成度環顯示 0%（用 .first() 避開 strict mode）
  await expect(page.locator('text=/0%/').first()).toBeVisible()
})