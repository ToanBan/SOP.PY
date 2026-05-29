from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.chat.core.application.port.output.i_message_file import MessageFileRepositoryInterface
from src.modules.chat.core.domain.entity.message_file import MessageFile
from src.modules.chat.adapter.postgresql.model.message_file_model import MessageFileModel


class MessageFileRepository(MessageFileRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message_file: MessageFile) -> None:
        model = MessageFileModel(
            id=message_file.id,
            message_id=message_file.message_id,
            file_url=message_file.file_url,
            file_type=message_file.file_type,
        )
        self.session.add(model)
        await self.session.flush()