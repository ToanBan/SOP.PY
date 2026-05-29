from abc import ABC, abstractmethod
from src.modules.chat.core.domain.entity.message_file import MessageFile

class MessageFileRepositoryInterface(ABC):
    
    @abstractmethod 
    async def save(self, message_file: MessageFile) -> None: ...

  