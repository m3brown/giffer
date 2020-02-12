import os

import aioredis


class Cache:
    async def startup(self):
        self.redis = await aioredis.create_redis_pool(os.environ["REDIS_URL"])

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def get(self, *args, **kwargs):
        return await self.redis.get(*args, **kwargs)

    async def set(self, *args, **kwargs):
        return await self.redis.set(*args, **kwargs)


cache = Cache()
