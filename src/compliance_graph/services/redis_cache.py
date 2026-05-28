import json
from typing import Any


class RedisCache:
    def __init__(self, url: str = "redis://localhost:6379"):
        self.url = url
        self._client = self._init_client()

    def _init_client(self) -> Any:
        try:
            import redis.asyncio as aioredis
            return aioredis.from_url(self.url, decode_responses=True)
        except ImportError:
            try:
                import redis
                return redis.from_url(self.url, decode_responses=True)
            except ImportError:
                return None

    async def get(self, key: str) -> str | None:
        if self._client:
            return await self._client.get(f"cg:{key}")
        return None

    async def set(self, key: str, value: Any, ttl: int = 300):
        if self._client:
            await self._client.setex(f"cg:{key}", ttl, json.dumps(value, default=str))

    async def cached_query(self, key: str, query_fn: callable, ttl: int = 300):
        cached = await self.get(key)
        if cached:
            return json.loads(cached)
        result = await query_fn()
        await self.set(key, result, ttl)
        return result
