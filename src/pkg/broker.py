from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend
from src.pkg.config.settings import settings

broker = AioPikaBroker(settings.RABBITMQ_URL).with_result_backend(
    RedisAsyncResultBackend(settings.REDIS_URL)
)