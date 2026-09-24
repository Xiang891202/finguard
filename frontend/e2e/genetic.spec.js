import { test, expect } from '@playwright/test'

async function loginAndSetup(page) {
  const email = `e2e-gen-${Date.now()}@example.com`
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

  // 填基本資料
  await page.fill('input[type="date"]', '1985-06-15')
  await page.getByRole('button', { name: '男' }).click()
  await page.getByRole('button', { name: /^儲存/ }).click()
  await expect(page.locator('text=/健康檔案已儲存/')).toBeVisible({ timeout: 10_000 })
}

test('基因檢測兩層折疊 + 新增 BRCA1', async ({ page }) => {
  await loginAndSetup(page)

  // 不勾時，不該有同意區
  await expect(page.locator('text=/我同意 FinGuard/')).not.toBeVisible()

  // 勾第一層
  await page.locator('label:has-text("我做過基因檢測")').click()

  // 出現同意 checkbox
  await expect(page.locator('text=/我同意 FinGuard/')).toBeVisible()

  // 勾第二層
  await page.locator('label:has-text("我同意 FinGuard")').click()

  // 等點位下拉出現
  const markerSelect = page.locator('select').first()
  await expect(markerSelect).toBeVisible()
  await expect(markerSelect.locator('option')).toHaveCount(9)   // 8 + 「請選擇」

  // 選 BRCA1
  await markerSelect.selectOption({ index: 1 })

  // 點新增
  await page.getByRole('button', { name: '新增' }).click()

  // 列表出現 BRCA1
  await expect(page.locator('text=/BRCA1 基因/')).toBeVisible()

  // 完成度應該 90%（基本 80 + 基因勾選 10）
  await expect(page.locator('text=/90%/').first()).toBeVisible()

  // 儲存
  await page.getByRole('button', { name: /^儲存/ }).click()
  await expect(page.locator('text=/健康檔案已儲存/')).toBeVisible({ timeout: 10_000 })
})