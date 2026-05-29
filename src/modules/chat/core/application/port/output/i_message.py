from abc import ABC, abstractmethod
from src.modules.chat.core.domain.entity.message import Message

class MessageRepositoryInterface(ABC):
    
    @abstractmethod 
    async def save(self, message: Message) -> None: ...

   