📚 Full P5.5 補充文件包（三份完整文件）

📄 文件 A：Redis Pub/Sub 實作指南
版本：v1.0
適用範圍：Full P5.5 快取失效機制

A.1 設計原則
A.1.1 為什麼需要 Redis Pub/Sub？
問題：應用層快取會擋住「改了馬上生效」。

解法：Redis Pub/Sub 通知所有服務清快取。

text
管理員改設定 → 寫入 DB → 發布 Redis → 所有服務清快取 → < 1 秒生效
A.1.2 設計原則
原則	說明
單一頻道	所有引擎共用 engine_updated 頻道
訊息帶類型	訊息含 engine_type，訂閱者自行過濾
至少一次送達	Redis Pub/Sub 不保證，但快取失效可容忍重複
失敗降級	Redis 掛了退回 TTL（最長 5 分鐘延遲）
非阻塞	發布不等待訂閱者回應
A.2 頻道與訊息格式
A.2.1 頻道設計
頻道名稱	用途
engine_updated	引擎版本變更
engine_cache_cleared	快取清除確認（可選）
為什麼不用多頻道？

頻道太多難管理

訂閱者訂閱一個頻道，用 engine_type 過濾即可

未來若量大再拆分

A.2.2 訊息格式
json
{
  "event_id": "uuid",
  "engine_type": "llm",
  "version": "v1.4",
  "action": "activated",
  "timestamp": "2026-09-22T10:00:00Z",
  "published_by": "admin_user_uuid"
}
欄位	型別	說明
event_id	String	事件唯一 ID（用於冪等）
engine_type	String	crawler / normalizer / validator / matcher / monte_carlo / llm
version	String	版本號
action	String	activated / archived / deleted
timestamp	String	ISO 8601
published_by	String	發布者 ID
A.3 發布端實作（Python FastAPI）
A.3.1 核心類別
python
# backend/app/core/cache_pubsub.py

import json
import uuid
from datetime import datetime
from typing import Optional
import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger

class CachePubSub:
    """Redis Pub/Sub 封裝"""
    
    CHANNEL = "engine_updated"
    
    def __init__(self):
        self.redis: Optional[redis.Redis] = None
    
    async def connect(self):
        """建立連線（應用啟動時呼叫）"""
        try:
            self.redis = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self.redis.ping()
            logger.info("Redis Pub/Sub connected")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.redis = None
    
    async def disconnect(self):
        """關閉連線（應用關閉時呼叫）"""
        if self.redis:
            await self.redis.close()
    
    async def publish_invalidation(
        self,
        engine_type: str,
        version: str,
        action: str = "activated",
        published_by: Optional[str] = None
    ) -> bool:
        """
        發布快取失效訊息
        
        Returns:
            bool: 是否成功發布
        """
        if not self.redis:
            logger.warning("Redis not available, skip publish")
            return False
        
        message = {
            "event_id": str(uuid.uuid4()),
            "engine_type": engine_type,
            "version": version,
            "action": action,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "published_by": published_by
        }
        
        try:
            await self.redis.publish(self.CHANNEL, json.dumps(message))
            logger.info(f"Published invalidation: {engine_type}/{version}")
            return True
        except Exception as e:
            logger.error(f"Publish failed: {e}")
            return False


# 全域單例
cache_pubsub = CachePubSub()
A.3.2 應用啟動整合
python
# backend/app/main.py

from fastapi import FastAPI
from app.core.cache_pubsub import cache_pubsub

app = FastAPI()

@app.on_event("startup")
async def startup():
    await cache_pubsub.connect()
    # 啟動訂閱者
    asyncio.create_task(cache_subscriber.start())

@app.on_event("shutdown")
async def shutdown():
    await cache_pubsub.disconnect()
A.3.3 發布時機
在 Service 層發布，不在 API 層：

python
# backend/app/services/engine/version_service.py

class VersionService:
    async def activate(self, version_id: str, admin_id: str):
        """啟用版本"""
        version = self.get(version_id)
        
        # 1. 封存舊版本
        old_active = self.get_active(version.engine_type)
        if old_active:
            old_active.status = "archived"
        
        # 2. 啟用新版本
        version.status = "active"
        version.activated_at = datetime.utcnow()
        db.commit()
        
        # 3. 發布快取失效
        await cache_pubsub.publish_invalidation(
            engine_type=version.engine_type,
            version=version.version,
            action="activated",
            published_by=admin_id
        )
        
        return version
為什麼在 Service 層？

確保「DB 寫入成功」才發布

若發布失敗，可記錄但不 rollback DB（快取會在 TTL 後自動失效）

A.4 訂閱端實作
A.4.1 Python FastAPI 訂閱者
python
# backend/app/core/cache_subscriber.py

import json
import asyncio
import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger

class CacheSubscriber:
    """訂閱快取失效訊息"""
    
    def __init__(self):
        self.redis: redis.Redis = None
        self.pubsub = None
        self._running = False
    
    async def start(self):
        """啟動訂閱"""
        self._running = True
        
        while self._running:
            try:
                await self._subscribe_loop()
            except Exception as e:
                logger.error(f"Subscriber crashed: {e}, retry in 5s")
                await asyncio.sleep(5)
    
    async def _subscribe_loop(self):
        """訂閱迴圈"""
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe("engine_updated")
        
        logger.info("Subscribed to engine_updated")
        
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                await self._handle_message(message["data"])
    
    async def _handle_message(self, data: str):
        """處理訊息"""
        try:
            msg = json.loads(data)
            engine_type = msg["engine_type"]
            version = msg["version"]
            
            logger.info(f"Received invalidation: {engine_type}/{version}")
            
            # 清除本地快取
            from app.services.engine.cache_service import cache_service
            await cache_service.clear_engine_cache(engine_type)
            
        except Exception as e:
            logger.error(f"Handle message failed: {e}")
    
    async def stop(self):
        """停止訂閱"""
        self._running = False
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.close()


cache_subscriber = CacheSubscriber()
A.4.2 Node.js BFF 訂閱者
javascript
// backend-node/src/subscribers/engineCacheSubscriber.js

const redis = require('redis');
const { clearEngineCache } = require('../services/cacheService');

const subscriber = redis.createClient({
  url: process.env.REDIS_URL
});

async function startEngineCacheSubscriber() {
  await subscriber.connect();
  
  await subscriber.subscribe('engine_updated', async (message) => {
    try {
      const msg = JSON.parse(message);
      console.log(`Received invalidation: ${msg.engine_type}/${msg.version}`);
      
      await clearEngineCache(msg.engine_type);
    } catch (err) {
      console.error('Handle message failed:', err);
    }
  });
  
  console.log('Subscribed to engine_updated');
}

module.exports = { startEngineCacheSubscriber };
A.4.3 Java 金流服務訂閱者
java
// billing-service/src/main/java/com/example/billing/subscriber/EngineCacheSubscriber.java

@Component
public class EngineCacheSubscriber {
    
    private final RedisMessageListenerContainer container;
    private final StringRedisTemplate redisTemplate;
    
    public EngineCacheSubscriber(
        RedisConnectionFactory connectionFactory,
        StringRedisTemplate redisTemplate
    ) {
        this.redisTemplate = redisTemplate;
        this.container = new RedisMessageListenerContainer();
        this.container.setConnectionFactory(connectionFactory);
        
        // 訂閱頻道
        this.container.addMessageListener(
            new MessageListener() {
                @Override
                public void onMessage(Message message, byte[] pattern) {
                    handleMessage(new String(message.getBody()));
                }
            },
            new ChannelTopic("engine_updated")
        );
        
        this.container.start();
    }
    
    private void handleMessage(String message) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode node = mapper.readTree(message);
            String engineType = node.get("engine_type").asText();
            
            // 清除本地快取
            clearEngineCache(engineType);
            
            log.info("Cache cleared for engine: {}", engineType);
        } catch (Exception e) {
            log.error("Handle message failed", e);
        }
    }
}
A.5 快取清除邏輯
A.5.1 快取 Key 設計
Key 格式	用途	TTL
engine:{type}:active	當前啟用版本	300s
engine:{type}:versions	版本列表	60s
engine:{type}:config:{version}	特定版本設定	300s
A.5.2 清除邏輯
python
# backend/app/services/engine/cache_service.py

class CacheService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def get_active_version(self, engine_type: str) -> Optional[dict]:
        """取得啟用版本（優先從快取）"""
        cache_key = f"engine:{engine_type}:active"
        
        # 1. 查快取
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # 2. 查 DB
        version = db.query(EngineVersion).filter(
            EngineVersion.engine_type == engine_type,
            EngineVersion.status == "active"
        ).first()
        
        if version:
            # 3. 寫快取
            await self.redis.setex(
                cache_key,
                300,  # 5 分鐘 TTL
                json.dumps(version.to_dict())
            )
        
        return version
    
    async def clear_engine_cache(self, engine_type: str):
        """清除指定引擎的快取"""
        pattern = f"engine:{engine_type}:*"
        
        # 掃描並刪除
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)
        
        logger.info(f"Cache cleared for engine: {engine_type}")
A.5.3 TTL 降級策略
python
class CacheService:
    async def get_active_version(self, engine_type: str) -> Optional[dict]:
        cache_key = f"engine:{engine_type}:active"
        
        # 若 Redis 掛了，直接查 DB
        try:
            cached = await self.redis.get(cache_key)
            if cached:
                return json.loads(cached)
        except redis.ConnectionError:
            logger.warning("Redis unavailable, fallback to DB")
        
        # 查 DB
        version = db.query(EngineVersion).filter(...).first()
        
        # 嘗試寫快取（失敗不影響）
        try:
            if version:
                await self.redis.setex(cache_key, 300, json.dumps(version.to_dict()))
        except redis.ConnectionError:
            pass
        
        return version
降級優先順序：

Redis 快取（< 10ms）

Redis 掛 → DB（< 100ms）

DB 掛 → 返回錯誤

A.6 測試策略
A.6.1 單元測試
python
# tests/unit/test_cache_pubsub.py

import pytest
from unittest.mock import AsyncMock, patch
from app.core.cache_pubsub import CachePubSub

@pytest.mark.asyncio
async def test_publish_invalidation():
    pubsub = CachePubSub()
    pubsub.redis = AsyncMock()
    
    result = await pubsub.publish_invalidation("llm", "v1.4", "activated")
    
    assert result is True
    pubsub.redis.publish.assert_called_once()
    
    # 驗證訊息格式
    call_args = pubsub.redis.publish.call_args
    channel, message = call_args[0]
    assert channel == "engine_updated"
    
    import json
    msg = json.loads(message)
    assert msg["engine_type"] == "llm"
    assert msg["version"] == "v1.4"
    assert msg["action"] == "activated"

@pytest.mark.asyncio
async def test_publish_fails_when_redis_down():
    pubsub = CachePubSub()
    pubsub.redis = None
    
    result = await pubsub.publish_invalidation("llm", "v1.4")
    
    assert result is False  # 不拋錯，只返回 False
A.6.2 整合測試
python
# tests/integration/test_cache_invalidation.py

import pytest
import asyncio
from app.core.cache_pubsub import cache_pubsub

@pytest.mark.asyncio
async def test_end_to_end_invalidation(redis_client, db):
    """測試：啟用版本 → 快取失效 → < 1 秒生效"""
    
    # 1. 預先寫入快取
    await redis_client.set(
        "engine:llm:active",
        json.dumps({"version": "v1.3"})
    )
    
    # 2. 啟用新版本（觸發 Pub/Sub）
    start = time.time()
    await version_service.activate("uuid-v1.4", admin_id)
    
    # 3. 等待快取清除
    await asyncio.sleep(0.5)
    elapsed = time.time() - start
    
    # 4. 驗證快取已清除
    cached = await redis_client.get("engine:llm:active")
    assert cached is None
    assert elapsed < 1.0, f"Invalidation took {elapsed}s, expected < 1s"
A.6.3 負載測試
python
# tests/performance/test_pubsub_load.py

@pytest.mark.asyncio
async def test_1000_messages():
    """測試 1000 則訊息下的延遲"""
    subscriber = MockSubscriber()
    await subscriber.start()
    
    start = time.time()
    for i in range(1000):
        await cache_pubsub.publish_invalidation("llm", f"v{i}")
    
    await asyncio.sleep(2)
    elapsed = time.time() - start
    
    assert subscriber.received_count == 1000
    assert elapsed < 5.0
A.7 監控與告警
A.7.1 監控指標
指標	說明	閾值
pubsub_publish_total	發布總數	-
pubsub_publish_failed	發布失敗數	> 10/分 → 告警
pubsub_subscribe_lag_ms	訂閱延遲	> 1000ms → 告警
cache_hit_rate	快取命中率	< 80% → 檢視
cache_clear_total	快取清除次數	-
A.7.2 告警規則
yaml
# alerts/pubsub.yml
groups:
  - name: cache_pubsub
    rules:
      - alert: PublishFailureRateHigh
        expr: rate(pubsub_publish_failed[5m]) > 0.1
        annotations:
          summary: "Redis Pub/Sub 發布失敗率 > 10%"
      
      - alert: SubscribeLagHigh
        expr: pubsub_subscribe_lag_ms > 1000
        annotations:
          summary: "訂閱延遲 > 1 秒"
A.8 常見問題
Q1：Redis 掛了怎麼辦？
A：退回 TTL 快取（最長 5 分鐘延遲）。不影響功能，只影響「即時性」。

Q2：訊息遺失怎麼辦？
A：Redis Pub/Sub 不保證送達，但快取失效可容忍：

遺失 → TTL 到期自動失效（最長 5 分鐘）

重複 → 重複清除無害

Q3：多服務同時訂閱會衝突嗎？
A：不會。Redis Pub/Sub 是廣播機制，所有訂閱者都會收到。

Q4：訂閱者處理太慢怎麼辦？
A：Pub/Sub 是非阻塞的，發布者不等待。訂閱者用背景任務處理。

Q5：如何避免重複發布？
A：用 event_id 做冪等。訂閱者記錄最近 100 個 event_id，重複則忽略。

A.9 實作檢查清單
□ cache_pubsub.py 實作完成
□ cache_subscriber.py 實作完成
□ 應用啟動時連接 Redis
□ Service 層在變更後發布
□ 所有服務訂閱 engine_updated
□ 快取 Key 命名一致
□ TTL 降級策略實作
□ 單元測試 ≥ 80%
□ 整合測試通過
□ 監控指標上報
□ 告警規則設定
文件 A 結束