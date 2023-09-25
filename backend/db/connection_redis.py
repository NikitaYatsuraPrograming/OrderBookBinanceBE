from typing import AsyncIterator

import redis
from aioredis import from_url, Redis

from settings.redis_setting import REDIS_HOST, REDIS_PORT


async def init_redis_pool() -> AsyncIterator[Redis]:
    session = from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf-8", decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()

connect_redis_sync = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=5)