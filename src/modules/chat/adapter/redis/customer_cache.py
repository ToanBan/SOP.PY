import json
from src.pkg.redis.client import redis_client
from src.modules.chat.core.domain.entity.customer import Customer

CACHE_TTL = 3600  

class CustomerCache:
    async def get(self, sender_id: str) -> Customer | None:
        data = await redis_client.get(f"customer:{sender_id}")
        if data is None:
            return None
        raw = json.loads(data)
        return Customer(
            id=raw["id"],
            page_id=raw["page_id"],
            sender_id=raw["sender_id"],
            name=raw["name"],
        )

    async def set(self, customer: Customer) -> None:
        await redis_client.set(
            f"customer:{customer.sender_id}",
            json.dumps({
                "id": customer.id,
                "page_id": customer.page_id,
                "sender_id": customer.sender_id,
                "name": customer.name,
            }),
            ex=CACHE_TTL
        )

    async def delete(self, sender_id: str) -> None:
        await redis_client.delete(f"customer:{sender_id}")