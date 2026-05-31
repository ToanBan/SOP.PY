from abc import ABC, abstractmethod

class ProcessFacebookMessageInterface(ABC):
    
    @abstractmethod 
    async def execute(self, payload: dict) -> None: ...