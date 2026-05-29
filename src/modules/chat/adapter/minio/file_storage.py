import httpx
import io
from src.pkg.minio.client import minio_client, ensure_bucket_exists
from src.pkg.config.settings import settings


class MinioFileStorage:
    async def upload_from_url(self, file_url: str, file_name: str, content_type: str = "application/octet-stream") -> str:
        await ensure_bucket_exists()

        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            file_data = response.content


        await minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=file_name,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type=content_type,
        )

        return f"{settings.MINIO_URL}/{settings.MINIO_BUCKET}/{file_name}"