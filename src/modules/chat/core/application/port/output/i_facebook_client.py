from abc import ABC, abstractmethod
from typing import Dict, Any

class IFacebookClient(ABC):
    
    @abstractmethod
    async def get_page_info(self, access_token: str) -> Dict[str, Any]: ...