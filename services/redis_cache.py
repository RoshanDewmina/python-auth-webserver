import redis.asyncio as redis
import json
from decouple import config

REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default=6379)

class RedisCache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

    async def set(self, key: str, value: dict, expire: int = 3600):
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def get(self, key: str):
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def close(self):
        await self.redis.close()

redis_cache = RedisCache()
