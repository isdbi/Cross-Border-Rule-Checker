# app/utils/caching.py
from redis import asyncio as aioredis
from app.config.config import settings

class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )

    async def get(self, key: str):
        return await self.redis.get(key)

    async def setex(self, key: str, ttl: int, value: str):
        await self.redis.setex(key, ttl, value)

redis_cache = RedisCache()