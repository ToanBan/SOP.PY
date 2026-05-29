from src.modules.chat.core.application.port.input.i_save_token_usecase import SaveFacebookTokeUseCaseInterface
from src.modules.chat.core.application.port.output.i_facebook_client import IFacebookClient
from src.modules.chat.core.application.port.output.i_channel_account import ChannelAccountRepositoryInterface
from src.modules.chat.core.domain.entity.channel_account import ChannelAccount
from src.modules.chat.adapter.http.dtos.channel_account_schema import AddChannelAccountRequest


class SaveFacebookTokenUseCase(SaveFacebookTokeUseCaseInterface):
    def __init__(
        self,
        repository: ChannelAccountRepositoryInterface,
        facebook_client: IFacebookClient
    ):
        self.repository = repository
        self.facebook_client = facebook_client

    async def execute(self, dto) -> None:
        page_info = await self.facebook_client.get_page_info(dto.page_access_token)

        channel_account = ChannelAccount(
            page_id=page_info["id"],
            page_name=page_info["name"],
            page_access_token=dto.page_access_token,
            is_active=True
        )

        await self.repository.save(channel_account)