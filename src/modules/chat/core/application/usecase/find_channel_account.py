from src.modules.chat.core.application.port.output.i_channel_account import ChannelAccountRepositoryInterface
from src.modules.chat.core.domain.entity.channel_account import ChannelAccount


class FindChannelAccountByChannelAccountUseCase:
    def __init__(self, repository: ChannelAccountRepositoryInterface):
        self.repository = repository

    async def execute(self, page_id: str) -> ChannelAccount | None:
        return await self.repository.find_by_page_id(page_id)