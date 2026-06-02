from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.modules.chat.core.application.port.output.i_channel_account import (
    ChannelAccountRepositoryInterface,
)

from src.modules.chat.core.domain.entity.channel_account import (
    ChannelAccount,
)

from src.modules.chat.adapter.postgresql.model.channel_account_model import (
    ChannelAccountModel,
)


class ChannelAccountRepository(ChannelAccountRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(
        self,
        channel_account: ChannelAccount,
    ) -> None:

        model = ChannelAccountModel(
            page_id=channel_account.page_id,
            page_access_token=channel_account.page_access_token,
            page_name=channel_account.page_name,
            is_active=channel_account.is_active,
            created_at=channel_account.created_at,
            updated_at=channel_account.updated_at,
        )

        self.session.add(model)

        await self.session.flush()

    async def find_by_page_id(
        self,
        page_id: str,
    ) -> ChannelAccount | None:

        result = await self.session.execute(
            select(ChannelAccountModel).where(
                ChannelAccountModel.page_id == page_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return ChannelAccount(
            page_id=model.page_id,
            page_access_token=model.page_access_token,
            page_name=model.page_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    

    async def find_channel_account_by_token(
        self,
        page_access_token: str,
    ) -> ChannelAccount | None:

        result = await self.session.execute(
            select(ChannelAccountModel).where(
                ChannelAccountModel.page_access_token == page_access_token
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return ChannelAccount(
            page_id=model.page_id,
            page_access_token=model.page_access_token,
            page_name=model.page_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    