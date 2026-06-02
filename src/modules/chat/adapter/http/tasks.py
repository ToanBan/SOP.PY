from src.pkg.broker import broker
from src.pkg.database.database import async_session_maker
from src.cmd.server.container import (
    provide_conversation_repo,
    provide_message_repo,
    provide_customer_repo,
    provide_message_file_repo,
    provide_channel_account_repo,
)

from src.modules.chat.core.application.usecase.process_facebook_message import ProcessFacebookMessageUseCase
from src.modules.chat.core.application.usecase.find_channel_account import FindChannelAccountByChannelAccountUseCase

@broker.task
async def process_facebook_webhook(data: dict) -> None:
    async with async_session_maker() as session:
        try:
            use_case = ProcessFacebookMessageUseCase(
                conversation_repository=provide_conversation_repo(session),
                message_repository=provide_message_repo(session),
                customer_repository=provide_customer_repo(session),
                message_file_repository=provide_message_file_repo(session),
                find_channel_by_id_use_case=FindChannelAccountByChannelAccountUseCase(
                    provide_channel_account_repo(session)
                ),
            )

            await use_case.execute(data)
            await session.commit()

        except Exception as e:
            await session.rollback()
            print("Worker error:", e)