from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.pkg.database.database import get_db_session
from src.cmd.server.container import (
    provide_channel_account_repo,
    provide_customer_repo,
    provide_conversation_repo,
    provide_message_repo,
    provide_message_file_repo,
    provide_facebook_client,
)
from src.modules.chat.core.application.port.output.i_channel_account import ChannelAccountRepositoryInterface
from src.modules.chat.core.application.port.input.i_save_token_usecase import SaveFacebookTokeUseCaseInterface
from src.modules.chat.core.application.port.input.i_find_channel_byid import FindChannelByIdUseCaseInterface
from src.modules.chat.core.application.usecase.save_facebook_usecase import SaveFacebookTokenUseCase
from src.modules.chat.core.application.usecase.find_channel_account import FindChannelAccountByChannelAccountUseCase
from src.modules.chat.core.application.port.input.i_process_facebook_message import ProcessFacebookMessageInterface
from src.modules.chat.core.application.usecase.process_facebook_message import ProcessFacebookMessageUseCase
from src.modules.chat.core.application.port.input.i_enqueue_facebook_webhook import EnqueueFacebookWebhookUseCaseInterface
from src.modules.chat.core.application.usecase.enqueue_facebook_webhook import EnqueueFacebookWebhookUseCase
def get_channel_account_repository(
    session: AsyncSession = Depends(get_db_session)
) -> ChannelAccountRepositoryInterface:
    return provide_channel_account_repo(session)


def get_save_facebook_token_use_case(
    session: AsyncSession = Depends(get_db_session)
) -> SaveFacebookTokeUseCaseInterface:
    return SaveFacebookTokenUseCase(
        repository=provide_channel_account_repo(session),
        facebook_client=provide_facebook_client()
    )


def get_find_channel_account_use_case(
    session: AsyncSession = Depends(get_db_session)
) -> FindChannelByIdUseCaseInterface:
    return FindChannelAccountByChannelAccountUseCase(
        repository=provide_channel_account_repo(session)
    )


def get_process_message_use_case(
    session: AsyncSession = Depends(get_db_session)
) -> ProcessFacebookMessageInterface:
    return ProcessFacebookMessageUseCase(
        conversation_repository=provide_conversation_repo(session),
        message_repository=provide_message_repo(session),
        customer_repository=provide_customer_repo(session),
        message_file_repository=provide_message_file_repo(session),
        find_channel_by_id_use_case=FindChannelAccountByChannelAccountUseCase(
            provide_channel_account_repo(session)
        ),
    )


def get_enqueue_facebook_webhook_use_case(
) -> EnqueueFacebookWebhookUseCaseInterface:
    return EnqueueFacebookWebhookUseCase()