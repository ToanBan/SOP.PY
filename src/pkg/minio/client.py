from miniopy_async import Minio
from src.pkg.config.settings import settings

minio_client = Minio(
    settings.MINIO_URL.replace("http://", "").replace("https://", ""),
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False  
)

async def ensure_bucket_exists():
    found = await minio_client.bucket_exists(settings.MINIO_BUCKET)
    if not found:
        await minio_client.make_bucket(settings.MINIO_BUCKET)