from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.modules.chat.core.application.port.output.i_conversation import ConversationRepositoryInterface
from src.modules.chat.core.domain.entity.conversation import Conversation
from src.modules.chat.adapter.postgresql.model.conversation_model import ConversationModel


class ConversationRepository(ConversationRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, conversation: Conversation) -> None:
        model = ConversationModel(
            id=conversation.id,
            page_id=conversation.page_id,
            customer_id=conversation.customer_id,
            status=conversation.status,
        )
        self.session.add(model)
        await self.session.flush()

    async def find_by_id(self, conversation_id: str) -> Conversation | None:
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return Conversation(
            id=model.id,
            page_id=model.page_id,
            customer_id=model.customer_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    

    async def find_by_customer_id(self, customer_id: str) -> Conversation | None:
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.customer_id == customer_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return Conversation(
            id=model.id,
            page_id=model.page_id,
            customer_id=model.customer_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )