from src.pkg.broker import broker
from src.pkg.database.database import async_session_maker

from src.modules.chat.adapter.postgresql.repo.customer_repo import CustomerRepository
from src.modules.chat.adapter.postgresql.repo.conversation_repo import ConversationRepository
from src.modules.chat.adapter.postgresql.repo.message_repo import MessageRepository
from src.modules.chat.adapter.postgresql.repo.message_file_repo import MessageFileRepository
from src.modules.chat.adapter.postgresql.repo.channel_account_repo import ChannelAccountRepository
from src.modules.chat.core.application.usecase.find_channel_account import FindChannelAccountByChannelAccountUseCase
from src.modules.chat.core.application.usecase.process_facebook_message import ProcessFacebookMessageUseCase


@broker.task
async def process_facebook_webhook(data: dict) -> None:
    print("Processing Facebook webhook data:", data)

    async with async_session_maker() as session:
        try:
            customer_repo = CustomerRepository(session)
            conversation_repo = ConversationRepository(session)
            message_repo = MessageRepository(session)
            message_file_repo = MessageFileRepository(session)
            channel_account_repo = ChannelAccountRepository(session)

            find_channel_use_case = FindChannelAccountByChannelAccountUseCase(channel_account_repo)

            use_case = ProcessFacebookMessageUseCase(
                conversation_repository=conversation_repo,
                message_repository=message_repo,
                customer_repository=customer_repo,
                message_file_repository=message_file_repo,
                find_channel_by_id_use_case=find_channel_use_case,
            )

            await use_case.execute(data)
            await session.commit()

        except Exception as e:
            await session.rollback()
            print("Worker error:", e)