from abc import ABC, abstractmethod
from src.modules.chat.core.domain.entity.channel_account import ChannelAccount

class ChannelAccountRepositoryInterface(ABC):
    
    @abstractmethod 
    async def save(self, channel_account: ChannelAccount) -> None: ...

    @abstractmethod
    async def find_by_page_id(self, page_id: str) -> ChannelAccount | None: ...