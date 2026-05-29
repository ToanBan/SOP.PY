from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.modules.chat.core.application.port.output.i_customer import CustomerRepositoryInterface
from src.modules.chat.core.domain.entity.customer import Customer
from src.modules.chat.adapter.postgresql.model.customer_model import CustomerModel


class CustomerRepository(CustomerRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, customer: Customer) -> None:
        model = CustomerModel(
            id=customer.id,
            page_id=customer.page_id,
            sender_id=customer.sender_id,
            name=customer.name,
        )
        self.session.add(model)
        await self.session.flush()

    async def find_by_id(self, customer_id: str) -> Customer | None:
        result = await self.session.execute(
            select(CustomerModel).where(CustomerModel.id == customer_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return Customer(
            id=model.id,
            page_id=model.page_id,
            sender_id=model.sender_id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    

    async def find_by_psid(self, sender_id: str) -> Customer | None:
        result = await self.session.execute(
            select(CustomerModel).where(CustomerModel.sender_id == sender_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return Customer(
            id=model.id,
            page_id=model.page_id,
            sender_id=model.sender_id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
    )