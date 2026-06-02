

from abc import ABC, abstractmethod

class EnqueueFacebookWebhookUseCaseInterface(ABC):

    @abstractmethod
    async def execute(self, payload: dict) -> str:
        ...