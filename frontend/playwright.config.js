import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? 'github' : 'list',

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    actionTimeout: 5_000
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } }
  ],

  webServer: [
    {
      command: 'cd ../backend && venv\\Scripts\\python -m uvicorn app.main:app --port 8000',
      url: 'http://localhost:8000/health',
      reuseExistingServer: !process.env.CI,
      timeout: 30_000,
      stdout: 'ignore',
      stderr: 'pipe',
            env: {
        TESTING: 'true',
        DEBUG: 'true',
        IP_RATE_PER_MINUTE: '1000',
        IP_RATE_PER_DAY: '100000',
        OTP_RESEND_INTERVAL: '0'
      }
    },
    {
      command: 'npm run dev',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env.CI,
      timeout: 30_000
    }
  ]
})