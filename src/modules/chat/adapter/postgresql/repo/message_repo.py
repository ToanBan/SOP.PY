from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.chat.core.application.port.output.i_message import MessageRepositoryInterface
from src.modules.chat.core.domain.entity.message import Message
from src.modules.chat.adapter.postgresql.model.message_model import MessageModel


class MessageRepository(MessageRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message: Message) -> None:
        model = MessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            sender_id=message.sender_id,
            message_id=message.message_id,
            message_type=message.message_type,
            text=message.text,
            timestamp=message.timestamp,
        )
        self.session.add(model)
        await self.session.flush()