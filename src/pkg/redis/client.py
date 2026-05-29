import redis.asyncio as redis
from src.pkg.config.settings import settings

redis_client: redis.Redis = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

async def get_redis() -> redis.Redis:
    return redis_client