import json
from src.pkg.redis.client import redis_client
from src.modules.chat.core.domain.entity.channel_account import ChannelAccount

CACHE_TTL = 3600  

class ChannelAccountCache:
    async def get(self, page_id: str) -> ChannelAccount | None:
        data = await redis_client.get(f"channel_account:{page_id}")
        if data is None:
            return None
        raw = json.loads(data)
        return ChannelAccount(
            page_id=raw["page_id"],
            page_name=raw["page_name"],
            page_access_token=raw["page_access_token"],
            is_active=raw["is_active"],
        )

    async def set(self, channel_account: ChannelAccount) -> None:
        await redis_client.set(
            f"channel_account:{channel_account.page_id}",
            json.dumps({
                "page_id": channel_account.page_id,
                "page_name": channel_account.page_name,
                "page_access_token": channel_account.page_access_token,
                "is_active": channel_account.is_active,
            }),
            ex=CACHE_TTL
        )

    async def delete(self, page_id: str) -> None:
        await redis_client.delete(f"channel_account:{page_id}")