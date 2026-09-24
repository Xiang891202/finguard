import { test, expect } from '@playwright/test'

async function login(page) {
  const email = `e2e-hp-${Date.now()}@example.com`
  await page.goto('/login')
  await page.getByPlaceholder('you@example.com').fill(email)

  const sendBtn = page.getByRole('button', { name: /發送驗證碼/ })
  await expect(sendBtn).toBeEnabled({ timeout: 5_000 })
  await sendBtn.click()

  const devBox = page.locator('text=/開發模式驗證碼/')
  await expect(devBox).toBeVisible({ timeout: 15_000 })
  const code = (await devBox.textContent()).match(/(\d{6})/)[1]

  await page.getByPlaceholder('000000').fill(code)
  await page.getByRole('button', { name: /^登入/ }).click()
  await expect(page).toHaveURL(/\/app\/account\/health/, { timeout: 10_000 })
}

test('填寫生日 + 性別 → 完成度 80% → 儲存', async ({ page }) => {
  await login(page)

  await page.fill('input[type="date"]', '1985-06-15')
  await page.getByRole('button', { name: '男' }).click()

  await expect(page.locator('text=/80%/')).toBeVisible({ timeout: 3_000 })

  await page.getByRole('button', { name: /^儲存/ }).click()
  await expect(page.locator('text=/健康檔案已儲存/')).toBeVisible({ timeout: 10_000 })
})