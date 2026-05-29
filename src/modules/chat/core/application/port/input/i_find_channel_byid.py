from abc import ABC, abstractmethod
from src.modules.chat.core.domain.entity.channel_account import ChannelAccount

class FindChannelByIdUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, page_id: str) -> ChannelAccount: ...