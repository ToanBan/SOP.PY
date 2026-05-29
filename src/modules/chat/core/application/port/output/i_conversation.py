from abc import ABC, abstractmethod
from src.modules.chat.core.domain.entity.conversation import Conversation
class ConversationRepositoryInterface(ABC):
    
    @abstractmethod 
    async def save(self, conversation) -> None: ...

    @abstractmethod
    async def find_by_id(self, conversation_id: str) -> Conversation : ...


    @abstractmethod
    async def find_by_customer_id(self, customer_id: str) -> Conversation | None: ...