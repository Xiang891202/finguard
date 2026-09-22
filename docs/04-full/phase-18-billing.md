Full Phase 18：金流模組
版本：v1.0
所屬：完整版
依賴 MVP Phase：無直接依賴
預計工時：12 天

🔗 依賴 MVP 哪個 Phase
依賴 MVP P0：subscriptions 表已建立

依賴 MVP P1：用戶認證已存在

🔄 與 MVP 的差異
項目	MVP	完整版
金流	完全關閉	管理員可開關
Java 服務	無	有
Stripe	無	整合
Email 模板	無	10 種
服務條款	無	4 份
發票	無	電子發票
📦 本 Phase 產出檔案
Java 服務（billing-service/）：

檔案路徑	動作
billing-service/src/main/java/com/example/billing/controller/BillingController.java	新增
billing-service/src/main/java/com/example/billing/controller/WebhookController.java	新增
billing-service/src/main/java/com/example/billing/service/SubscriptionService.java	新增
billing-service/src/main/java/com/example/billing/service/StripeService.java	新增
billing-service/src/main/java/com/example/billing/service/InvoiceService.java	新增
billing-service/src/main/java/com/example/billing/service/EmailNotification.java	新增
billing-service/src/main/java/com/example/billing/repository/SubscriptionRepository.java	新增
billing-service/src/main/java/com/example/billing/model/Subscription.java	新增
billing-service/src/main/java/com/example/billing/dto/CheckoutRequest.java	新增
billing-service/src/main/java/com/example/billing/dto/CheckoutResponse.java	新增
billing-service/src/main/java/com/example/billing/config/StripeConfig.java	新增
billing-service/src/main/java/com/example/billing/config/SecurityConfig.java	新增
billing-service/src/main/resources/application.yml	新增
billing-service/src/main/resources/templates/payment-success.html	新增
billing-service/src/main/resources/templates/payment-failed.html	新增
billing-service/src/main/resources/templates/grace-period.html	新增
billing-service/pom.xml	新增
billing-service/Dockerfile	新增
前端：

檔案路徑	動作
frontend/src/views/app/BillingView.vue	新增
frontend/src/views/admin/BillingAdminView.vue	新增
frontend/src/views/app/TermsView.vue	新增
frontend/src/views/app/PrivacyView.vue	新增
frontend/src/views/app/RefundPolicyView.vue	新增
frontend/src/views/app/SubscriptionTermsView.vue	新增
frontend/src/components/billing/PlanCard.vue	新增
frontend/src/components/billing/CheckoutForm.vue	新增
frontend/src/api/billing.js	新增
後端 Python（主框架）：

檔案路徑	動作
backend/app/api/v1/billing_proxy.py	新增
backend/app/services/billing_service.py	新增
backend/tests/unit/test_billing.py	新增
1. 目標
建立金流訂閱系統（Java + Stripe）。

2. 前置條件
□ MVP 完成
□ Stripe 帳號已設定
□ Java 17+ 已安裝
3. 前端畫面
3.1 頁面清單
頁面	路由	說明
BillingView	/app/billing	訂閱方案
BillingAdminView	/admin/billing	金流開關
TermsView	/terms	服務條款
PrivacyView	/privacy	隱私政策
RefundPolicyView	/refund-policy	退款政策
SubscriptionTermsView	/subscription-terms	訂閱條款
3.2 UI 草圖
BillingView：

text
┌─────────────────────────────────────┐
│  💳 訂閱方案                         │
├─────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐       │
│  │ 免費版     │ │ 專業版     │       │
│  │ $0/月      │ │ NT$299/月  │       │
│  │ 2 模型     │ │ 4 模型     │       │
│  │ [目前]     │ │ [升級]     │       │
│  └───────────┘ └───────────┘       │
│                                     │
│  ☐ 啟用自動扣款                     │
│  ☑ 我已閱讀並同意服務條款           │
└─────────────────────────────────────┘
BillingAdminView：

text
┌─────────────────────────────────────┐
│  💰 金流開關                         │
├─────────────────────────────────────┤
│  狀態：❌ 關閉                       │
│  [開啟金流]                          │
│                                     │
│  開啟後：                            │
│  - 用戶將看到「升級」按鈕            │
│  - 現有用戶自動進入試用期（30 天）   │
└─────────────────────────────────────┘
4. 後端邏輯
4.1 API 端點
方法	路徑	服務	說明
POST	/api/v1/billing/checkout	Java	建立 Checkout
POST	/api/v1/billing/webhook	Java	Stripe Webhook
GET	/api/v1/billing/subscription	Java	訂閱狀態
GET	/api/v1/billing/invoices	Java	發票
POST	/api/v1/billing/cancel	Java	取消
POST	/api/v1/billing/refund	Java	退款
GET	/api/v1/admin/billing	Python	開關狀態
POST	/api/v1/admin/billing/toggle	Python	切換
4.2 請求/回應範例
POST /api/v1/billing/checkout：

json
{
  "plan": "pro",
  "auto_renew": true
}
回應：

json
{
  "success": true,
  "data": {
    "checkout_url": "https://checkout.stripe.com/...",
    "session_id": "cs_..."
  }
}
4.3 資料庫變更
使用表：subscriptions

4.4 環境變數
變數	說明
STRIPE_SECRET_KEY	Stripe 密鑰
STRIPE_WEBHOOK_SECRET	Webhook 密鑰
STRIPE_PRICE_PRO	專業版價格 ID
BILLING_SERVICE_URL	Java 服務 URL
5. 單元測試
5.1 後端測試（Java）
java
@Test
public void testCreateCheckoutSession() {
    CheckoutRequest request = new CheckoutRequest("pro", true);
    CheckoutResponse response = billingService.createCheckout(request, userId);
    assertNotNull(response.getCheckoutUrl());
}
5.2 前端測試
javascript
describe('CheckoutForm', () => {
  it('requires terms consent', async () => {
    const wrapper = mount(CheckoutForm)
    await wrapper.find('form').trigger('submit')
    expect(wrapper.text()).toContain('請同意服務條款')
  })
})
5.3 整合測試
python
def test_billing_toggle():
    # 管理員切換為開啟
    response = admin_client.post("/api/v1/admin/billing/toggle", json={"enabled": True})
    assert response.status_code == 200
    
    # 用戶端看到升級按鈕
    response = user_client.get("/api/v1/app/billing/plan")
    assert response.json()["data"]["show_upgrade"] is True
6. 驗收標準
□ 金流開關運作
□ Stripe Checkout 成功
□ Webhook 處理正確
□ 10 種 Email 模板
□ 4 份服務條款
□ 電子發票
□ 寬限期 30 天
□ 資料分級刪除
□ Java 單元測試通過
□ 整合測試通過
7. 交付物清單
（略）