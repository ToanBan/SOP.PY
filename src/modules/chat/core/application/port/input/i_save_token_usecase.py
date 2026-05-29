from abc import ABC, abstractmethod
from src.modules.chat.core.application.dtos.save_facebook_token import SaveFacebookTokenDTO
class SaveFacebookTokeUseCaseInterface(ABC):
    @abstractmethod
    async def execute(self, dto: SaveFacebookTokenDTO) -> None: ...
        

