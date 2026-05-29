from abc import ABC, abstractmethod

class ProcessFacebookMessageInterface(ABC):
    
    @abstractmethod 
    async def process(self, message: dict) -> None: ...