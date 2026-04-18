import redis.asyncio as aioredis
from app.core.config import settings

redis_client = None

# Dependency to get Redis client
async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
    return redis_client

# Cleanup function to close Redis connection on shutdown
async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()