from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.pkg.database.database import get_db_session
from src.modules.chat.adapter.postgresql.repo.channel_account_repo import ChannelAccountRepository
from src.modules.chat.adapter.http.facebook_client import FacebookClient
from src.modules.chat.core.application.usecase.save_facebook_usecase import SaveFacebookTokenUseCase
from src.modules.chat.core.application.usecase.find_channel_account import FindChannelAccountByChannelAccountUseCase


def get_channel_account_repository(
    session: AsyncSession = Depends(get_db_session)
) -> ChannelAccountRepository:
    return ChannelAccountRepository(session=session)


def get_facebook_client() -> FacebookClient:
    return FacebookClient()


def get_save_facebook_token_use_case(
    repository: ChannelAccountRepository = Depends(get_channel_account_repository),
    facebook_client: FacebookClient = Depends(get_facebook_client)
) -> SaveFacebookTokenUseCase:
    return SaveFacebookTokenUseCase(
        repository=repository,
        facebook_client=facebook_client
    )


def get_find_channel_account_use_case(
    repository: ChannelAccountRepository = Depends(get_channel_account_repository)
) -> FindChannelAccountByChannelAccountUseCase:
    return FindChannelAccountByChannelAccountUseCase(repository=repository)